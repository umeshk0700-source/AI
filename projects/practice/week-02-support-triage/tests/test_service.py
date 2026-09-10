"""Exercises the service's business logic with a FakeLLM (no API)."""
import json
from datetime import datetime, timezone

from llmlab import FakeLLM
from triage.schemas import Ticket
from triage.service import TriageService, TEAM_BY_CATEGORY


def _fake(label: dict):
    base = {"category": "bug", "priority": "P3", "sentiment": "neutral",
            "needs_human": False, "draft_reply": "Thanks, we're looking into it.",
            "confidence": 0.9}
    base.update(label)
    return FakeLLM(responder=lambda messages, **kw: base)


def test_happy_path_routing_and_sla():
    svc = TriageService(_fake({"category": "billing", "priority": "P3"}))
    t = Ticket(id="1", subject="Invoice question", body="Can I get a copy of last month's invoice?")
    r = svc.triage(t)
    assert r.route_to_team == TEAM_BY_CATEGORY[r.category] == "billing-ops"
    assert (r.sla_due_at - t.created_at).total_seconds() == 24 * 3600
    assert r.rules_applied == []


def test_security_forces_p1_and_human():
    svc = TriageService(_fake({"category": "security", "priority": "P4", "needs_human": False}))
    r = svc.triage(Ticket(id="2", subject="Possible breach", body="I see logins I don't recognise."))
    assert r.priority.value == "P1" and r.needs_human is True
    assert "security_or_legal_p1" in r.rules_applied


def test_enterprise_negative_escalates():
    svc = TriageService(_fake({"category": "bug", "priority": "P3", "sentiment": "angry"}))
    r = svc.triage(Ticket(id="3", subject="Broken", body="This is unacceptable.",
                          customer_tier="enterprise"))
    assert r.priority.value == "P2"
    assert "enterprise_negative_escalation" in r.rules_applied


def test_sensitive_keyword_needs_human():
    svc = TriageService(_fake({"category": "billing", "needs_human": False}))
    r = svc.triage(Ticket(id="4", subject="Money", body="I want a refund for this charge."))
    assert r.needs_human is True and "sensitive_keyword_needs_human" in r.rules_applied


def test_low_confidence_review():
    svc = TriageService(_fake({"confidence": 0.4}))
    r = svc.triage(Ticket(id="5", subject="Vague", body="It doesn't work."))
    assert r.needs_human is True and "low_confidence_review" in r.rules_applied


def test_batch_survives_a_bad_ticket():
    class Boom(FakeLLM):
        def chat(self, *a, **k):
            raise RuntimeError("model down")
    good = TriageService(_fake({}))
    bad = TriageService(Boom())
    ts = [Ticket(id=str(i), subject="s", body="body text here") for i in range(3)]
    assert len(good.triage_batch(ts)) == 3
    assert bad.triage_batch(ts) == []
