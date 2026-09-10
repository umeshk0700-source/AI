
"""The triage service: LLM classification + deterministic business rules."""
from __future__ import annotations

from datetime import datetime, timezone

from llmlab import LLMClient, span

from .prompts import PromptStrategy, ZeroShotStrategy
from .schemas import (
    Category, Classification, CustomerTier, Priority, Sentiment, Ticket, TriageResult,
)

# category -> owning team (hard routing, not the model's call)
TEAM_BY_CATEGORY: dict[Category, str] = {
    Category.billing: "billing-ops",
    Category.bug: "engineering",
    Category.how_to: "support-tier1",
    Category.account: "support-tier1",
    Category.security: "security",
    Category.feature_request: "product",
    Category.legal: "legal",
    Category.other: "support-tier1",
}

_CLASSIFICATION_SCHEMA = Classification.model_json_schema()


class TriageService:
    def __init__(self, llm: LLMClient, strategy: PromptStrategy | None = None,
                 *, max_tokens: int = 400):
        self.llm = llm
        self.strategy = strategy or ZeroShotStrategy()
        self.max_tokens = max_tokens

    # -- step 1: the model read -------------------------------------------
    def _classify(self, ticket: Ticket) -> Classification:
        # TODO: build the prompt with self.strategy, call self.llm.chat(...) with
        #       json_schema=_CLASSIFICATION_SCHEMA and self.max_tokens, then parse
        #       response.json into a Classification. Wrap the call in span("classify").
        system, messages = self.strategy.build(ticket)
        with span("classify", kind="llm", strategy=self.strategy.name):
            resp = self.llm.chat(messages, system=system, json_schema=_CLASSIFICATION_SCHEMA,
                                 max_tokens=self.max_tokens)
        return Classification.model_validate(resp.json)

    # -- step 2: business rules -----------------------------------------
    def _apply_rules(self, ticket: Ticket, c: Classification) -> TriageResult:
        # TODO: starting from the model's classification, apply, in order, and record
        #       each rule name you fire in `rules_applied`:
        #   R1 security or legal category  -> force priority P1, needs_human=True
        #   R2 enterprise tier AND sentiment in {negative, angry} -> priority.bump()
        #   R3 body mentions "refund", "chargeback", "cancel my account", "gdpr",
        #      "data deletion", or "lawyer" (case-insensitive) -> needs_human=True
        #   R4 confidence < 0.55 -> needs_human=True  (rule "low_confidence_review")
        #   route_to_team = TEAM_BY_CATEGORY[category]
        #   sla_due_at = TriageResult.sla_from(ticket.created_at, final priority)
        priority, needs_human, rules = c.priority, c.needs_human, []
        if c.category in (Category.security, Category.legal):
            priority, needs_human = Priority.p1, True
            rules.append("security_or_legal_p1")
        if (ticket.customer_tier == CustomerTier.enterprise
                and c.sentiment in (Sentiment.negative, Sentiment.angry)):
            priority = priority.bump()
            rules.append("enterprise_negative_escalation")
        triggers = ("refund", "chargeback", "cancel my account", "gdpr",
                    "data deletion", "lawyer")
        if any(t in ticket.body.lower() for t in triggers):
            needs_human = True
            rules.append("sensitive_keyword_needs_human")
        if c.confidence < 0.55:
            needs_human = True
            rules.append("low_confidence_review")
        return TriageResult(
            ticket_id=ticket.id, category=c.category, priority=priority,
            sentiment=c.sentiment, needs_human=needs_human,
            route_to_team=TEAM_BY_CATEGORY[c.category],
            sla_due_at=TriageResult.sla_from(ticket.created_at, priority),
            draft_reply=c.draft_reply, confidence=c.confidence, rules_applied=rules,
        )

    # -- public API -----------------------------------------------------
    def triage(self, ticket: Ticket) -> TriageResult:
        # TODO: classify then apply rules, all inside span("triage", ticket_id=...).
        with span("triage", kind="chain", ticket_id=ticket.id):
            return self._apply_rules(ticket, self._classify(ticket))

    def triage_batch(self, tickets: list[Ticket]) -> list[TriageResult]:
        # TODO: triage each ticket; on a per-ticket error, skip it and keep going
        #       (a bad ticket must not take down the batch). Return the successes.
        out: list[TriageResult] = []
        for t in tickets:
            try:
                out.append(self.triage(t))
            except Exception:  # noqa: BLE001
                continue
        return out
