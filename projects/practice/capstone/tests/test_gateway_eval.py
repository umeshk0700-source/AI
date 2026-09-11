import pytest
from llmlab import FakeLLM
from ragplatform import Gateway, EvalGate

def _boom():
    def r(messages, **kw):
        raise RuntimeError("provider down")
    return FakeLLM(r)

def test_gateway_cache_hit():
    gw = Gateway(FakeLLM(lambda m, **k: "hello"))
    gw.chat([{"role": "user", "content": "hi"}])
    gw.chat([{"role": "user", "content": "hi"}])
    assert gw.stats == {"hits": 1, "misses": 1, "failovers": 0}

def test_gateway_failover():
    gw = Gateway(_boom(), FakeLLM(lambda m, **k: "from backup"))
    r = gw.chat([{"role": "user", "content": "hi"}])
    assert r.text == "from backup" and gw.stats["failovers"] == 1

def test_gateway_reraises_without_fallback():
    with pytest.raises(RuntimeError):
        Gateway(_boom()).chat([{"role": "user", "content": "hi"}])

def test_eval_gate_baseline_then_regression():
    judge_llm = FakeLLM(lambda m, **k: ("tool", "emit", {"score": 0.9, "reasoning": "ok"}))
    gate = EvalGate(judge_llm)
    cases = [("q1", "a1"), ("q2", "a2")]
    base = gate.check(lambda q: "answer", cases, baseline=None)
    assert base.ok
    bad_judge = FakeLLM(lambda m, **k: ("tool", "emit", {"score": 0.2, "reasoning": "bad"}))
    res = EvalGate(bad_judge).check(lambda q: "answer", cases, baseline=base.per_case)
    assert res.ok is False
