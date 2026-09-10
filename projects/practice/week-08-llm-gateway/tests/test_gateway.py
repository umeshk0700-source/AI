import pytest
from llmlab import FakeLLM, BudgetExceeded
from gateway.gateway import Gateway
from gateway.cache import SemanticCache
from gateway.breaker import CircuitBreaker
from tests.test_cache import ToyEmbedder


def _gw(primary, fallback, **kw):
    return Gateway(primary, fallback, SemanticCache(ToyEmbedder(), threshold=0.9), **kw)


def test_serves_from_primary_then_cache():
    p = FakeLLM(text="primary says hi")
    f = FakeLLM(text="fallback says hi")
    gw = _gw(p, f)
    r1 = gw.chat("acme", [{"role": "user", "content": "hello there friend"}])
    assert r1.served_by == "fake" and r1.cached is False
    r2 = gw.chat("acme", [{"role": "user", "content": "hello there friend"}])
    assert r2.cached is True and r2.served_by == "cache" and r2.cost_usd == 0.0


def test_falls_back_when_primary_raises():
    class Down(FakeLLM):
        def chat(self, *a, **k):
            raise RuntimeError("provider incident")
    Down.provider = "anthropic"
    good = FakeLLM(text="gpt to the rescue")
    good.provider = "openai"
    gw = _gw(Down(), good, breaker=CircuitBreaker(failure_threshold=1))
    r = gw.chat("acme", [{"role": "user", "content": "unique question one"}])
    assert r.served_by == "openai" and "rescue" in r.text


def test_tenant_budget_enforced():
    gw = _gw(FakeLLM(text="answer"), FakeLLM(text="answer"))
    gw.set_budget("acme", 0.0)               # zero budget
    # FakeLLM reports 10/10 tokens on a priced model -> record() should trip the cap
    from llmlab.cost import price
    # monkeypatch model on the response path: FakeLLM uses model="fake" (price 0) -> won't trip.
    # so give the primary a real model id:
    gw.primary = FakeLLM(text="answer")
    gw.primary.chat = lambda *a, **k: __import__("llmlab").LLMResponse(
        text="answer", model="gpt-4o", provider="openai", stop_reason="end_turn",
        input_tokens=1000, output_tokens=1000, cost_usd=0.0)
    with pytest.raises(BudgetExceeded):
        gw.chat("acme", [{"role": "user", "content": "some brand new prompt here"}])
