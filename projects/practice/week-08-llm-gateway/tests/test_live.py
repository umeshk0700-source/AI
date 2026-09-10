import os
import pytest
from llmlab import get_client, get_embedder, default_cost, settings
from gateway.gateway import Gateway
from gateway.cache import SemanticCache
from gateway.breaker import CircuitBreaker

pytestmark = pytest.mark.live
_LIVE = os.getenv("LLM_LIVE") == "1"


@pytest.mark.skipif(not (_LIVE and settings.has("anthropic") and settings.has("openai")),
                    reason="live needs both providers")
def test_cache_saves_a_second_call():
    emb = get_embedder("openai")
    gw = Gateway(get_client("anthropic"), get_client("openai"),
                 SemanticCache(emb, threshold=0.9))
    msg = [{"role": "user", "content": "In one sentence, what is a circuit breaker in software?"}]
    c0 = default_cost().total_usd
    r1 = gw.chat("t", msg, max_tokens=80)
    mid = default_cost().total_usd
    r2 = gw.chat("t", msg, max_tokens=80)
    end = default_cost().total_usd
    print(f"\ncall1 served_by={r1.served_by} cost=${mid - c0:.5f}")
    print(f"call2 served_by={r2.served_by} cost=${end - mid:.5f} (embedding only)")
    assert r1.cached is False and r2.cached is True
    assert (end - mid) < (mid - c0)          # second call is far cheaper


@pytest.mark.skipif(not (_LIVE and settings.has("openai")), reason="live openai")
def test_fallback_serves_when_primary_forced_down():
    class Down:
        provider = "anthropic"
        def chat(self, *a, **k):
            raise RuntimeError("simulated Anthropic incident")
    gw = Gateway(Down(), get_client("openai"),
                 SemanticCache(get_embedder("local"), threshold=0.99),
                 breaker=CircuitBreaker(failure_threshold=1))
    r = gw.chat("t", [{"role": "user", "content": "Say the word: resilient"}], max_tokens=10)
    assert r.served_by == "openai" and "resilient" in r.text.lower()
