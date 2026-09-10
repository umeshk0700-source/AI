from llmlab import FakeLLM
from triage.evaluate import TriageEval
from triage.service import TriageService
from testing_helpers import load_gold


def test_score_one():
    ev = TriageEval([])
    class R:
        from triage.schemas import Category, Priority
        category = Category.billing
        priority = Priority.p2
        needs_human = True
        route_to_team = "billing-ops"
    gold = {"category": "billing", "priority": "P3", "needs_human": True, "team": "billing-ops"}
    s = ev.score_one(R(), gold)
    assert s["category_ok"] and s["priority_within_1"] and s["needs_human_ok"] and s["team_ok"]


def test_run_produces_report():
    gold = load_gold()
    # a FakeLLM that always says billing/P3 — the report should still populate every field
    svc = TriageService(FakeLLM(responder=lambda m, **k: {
        "category": "billing", "priority": "P3", "sentiment": "neutral",
        "needs_human": False, "draft_reply": "Hi.", "confidence": 0.8}))
    rep = TriageEval(gold).run(svc)
    assert rep.n == len(gold)
    assert 0.0 <= rep.category_acc <= 1.0
    assert len(rep.rows) == len(gold)
