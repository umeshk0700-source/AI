
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
        raise NotImplementedError("build the prompt with self.strategy, call self.llm.chat(...) with")

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
        raise NotImplementedError("starting from the model's classification, apply, in order, and record")

    # -- public API -----------------------------------------------------
    def triage(self, ticket: Ticket) -> TriageResult:
        # TODO: classify then apply rules, all inside span("triage", ticket_id=...).
        raise NotImplementedError("classify then apply rules, all inside span('triage', ticket_id=...).")

    def triage_batch(self, tickets: list[Ticket]) -> list[TriageResult]:
        # TODO: triage each ticket; on a per-ticket error, skip it and keep going
        #       (a bad ticket must not take down the batch). Return the successes.
        raise NotImplementedError("triage each ticket; on a per-ticket error, skip it and keep going")
