from llmlab import FakeLLM
from quality.schemas import EvalCase
from quality.scorers import ExactMatch, Contains, LLMJudge


def test_exact_match():
    c = EvalCase(id="1", inputs={}, reference="Paris")
    assert ExactMatch().score("paris", c) == 1.0
    assert ExactMatch().score("London", c) == 0.0


def test_contains():
    c = EvalCase(id="1", inputs={}, must_contain=["1.75", "vacation"])
    assert Contains().score("You accrue 1.75 vacation days.", c) == 1.0
    assert Contains().score("You accrue 1.75 days.", c) == 0.5
    assert Contains().score("anything", EvalCase(id="2", inputs={})) == 1.0


def test_llm_judge_normalises_score():
    j = LLMJudge(FakeLLM(responder=lambda m, **k: {"score": 5, "reason": "matches"}))
    assert j.score("candidate", EvalCase(id="1", inputs={}, reference="ref")) == 1.0
    j2 = LLMJudge(FakeLLM(responder=lambda m, **k: {"score": 3, "reason": "partial"}))
    assert j2.score("c", EvalCase(id="1", inputs={}, reference="r")) == 0.5
    j3 = LLMJudge(FakeLLM(responder=lambda m, **k: "not json"))
    assert j3.score("c", EvalCase(id="1", inputs={}, reference="r")) == 0.0
