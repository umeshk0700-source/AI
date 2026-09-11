"""End-to-end: a real judge scores two candidate bundles, the gate decides. Costs a few cents."""
import pytest

pytestmark = pytest.mark.live

from llmlab import get_client
from llmlab.testing import live, judge
from platformops import EvalReport, ReleaseGate

CASES = [
    ("What is the refund window?", "Refunds are accepted within 30 days of purchase."),
    ("How do I reset my password?", "Use the 'forgot password' link on the sign-in page."),
]

@live("anthropic")
def test_real_judge_feeds_the_gate():
    llm = get_client("anthropic")
    good = {q: judge(llm, q, ref, ref)["score"] for q, ref in CASES}
    bad = {q: judge(llm, q, ref, "I am not sure, please contact support.")["score"]
           for q, ref in CASES}
    baseline = EvalReport("baseline", good)
    assert ReleaseGate(baseline).check(EvalReport("cand-good", good)).ok is True
    assert ReleaseGate(baseline).check(EvalReport("cand-bad", bad)).ok is False
