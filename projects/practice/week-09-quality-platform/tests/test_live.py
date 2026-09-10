import os
import pytest
import numpy as np
from llmlab import get_client, settings
from quality.schemas import EvalCase
from quality.scorers import LLMJudge, Contains
from quality.suite import EvalSuite
from quality.gate import RegressionGate

pytestmark = pytest.mark.live
_LIVE = os.getenv("LLM_LIVE") == "1"

# (reference, candidate, hand_label 1-5)
GRADED = [
  ("Refunds are issued within 5 business days.",
   "You'll get your refund within 5 business days.", 5),
  ("Refunds are issued within 5 business days.",
   "Refunds usually take about a week.", 3),
  ("Refunds are issued within 5 business days.",
   "We don't offer refunds.", 1),
  ("The meal per diem is $90 international.",
   "For international travel the per diem is $90.", 5),
  ("The meal per diem is $90 international.",
   "The per diem is $60.", 1),
  ("Passwords rotate every 90 days.",
   "Passwords must be changed roughly every quarter.", 4),
]


def _spearman(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


@pytest.mark.skipif(not _LIVE, reason="live")
def test_judge_correlates_with_human():
    prov = "anthropic" if settings.has("anthropic") else "openai"
    model = "claude-sonnet-4-5" if prov == "anthropic" else "gpt-4o"
    judge = LLMJudge(get_client(prov, model=model))
    preds, humans = [], []
    for ref, cand, h in GRADED:
        s = judge.score(cand, EvalCase(id="x", inputs={}, reference=ref))
        preds.append(s); humans.append(h)
    rho = _spearman(preds, humans)
    print(f"\njudge scores: {[round(p, 2) for p in preds]}  human: {humans}  rho={rho:.2f}")
    assert rho >= 0.7, f"judge rank-correlation with humans only {rho:.2f}"


@pytest.mark.skipif(not _LIVE, reason="live")
def test_gate_flags_a_seeded_regression():
    prov = "anthropic" if settings.has("anthropic") else "openai"
    judge = LLMJudge(get_client(prov))
    cases = [EvalCase(id=str(i), inputs={"i": i}, reference=ref, must_contain=[])
             for i, (ref, _, _) in enumerate(GRADED)]
    good = EvalSuite(cases, [judge]).run(lambda i: GRADED[i][0])          # answer == reference
    bad = EvalSuite(cases, [judge]).run(lambda i: "We don't cover that.")  # always wrong
    v = RegressionGate(good, must_not_regress=("judge",), tolerance=0.1).check(bad)
    print("\n", v)
    assert not v.passed and "judge" in v.blocking
