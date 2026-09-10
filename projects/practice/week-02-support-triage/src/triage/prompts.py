
"""Prompting strategies. Each turns a Ticket into (system_prompt, messages)."""
from __future__ import annotations

from abc import ABC, abstractmethod

from .schemas import Ticket

_CATS = "billing, bug, how_to, account, security, feature_request, legal, other"
_PRIOS = "P1 (outage/security), P2 (major), P3 (normal), P4 (low)"

BASE_SYSTEM = (
    "You are a support-ticket triage assistant for a B2B SaaS product. "
    f"Categories: {_CATS}. Priorities: {_PRIOS}. "
    "Sentiment: positive, neutral, negative, angry. "
    "Return the classification via the provided schema. The draft_reply is a concise, "
    "professional first response the agent can edit (2-4 sentences, no promises about refunds "
    "or timelines you can't verify). confidence is your certainty 0-1."
)


class PromptStrategy(ABC):
    name: str = "base"

    @abstractmethod
    def build(self, ticket: Ticket) -> tuple[str, list[dict]]:
        ...

    @staticmethod
    def _ticket_block(t: Ticket) -> str:
        return (f"Customer tier: {t.customer_tier.value}\n"
                f"Subject: {t.subject}\n"
                f"Body: {t.body}")


class ZeroShotStrategy(PromptStrategy):
    name = "zero_shot"

    def build(self, ticket):
        return BASE_SYSTEM, [{"role": "user", "content": self._ticket_block(ticket)}]


# Three worked examples (subject, body, tier) -> the ideal classification dict.
FEWSHOT_EXAMPLES: list[tuple[str, str, str, dict]] = [
    ("Can't log in after password reset", "The reset link says expired every time. Demo in 20 min!!",
     "enterprise",
     {"category": "account", "priority": "P2", "sentiment": "angry", "needs_human": True}),
    ("Invoice VAT number wrong", "Our finance team needs the VAT id on invoice #4471 corrected.",
     "pro",
     {"category": "billing", "priority": "P3", "sentiment": "neutral", "needs_human": True}),
    ("Idea: dark mode", "Would love a dark theme for the dashboard some day.", "free",
     {"category": "feature_request", "priority": "P4", "sentiment": "positive", "needs_human": False}),
]


class FewShotStrategy(PromptStrategy):
    name = "few_shot"

    def __init__(self, examples=None):
        self.examples = examples or FEWSHOT_EXAMPLES

    def build(self, ticket):
        # TODO: return (system, messages) where `messages` is an alternating
        #       user/assistant transcript of the examples (assistant turns are the
        #       JSON of the example dict), followed by the real ticket as the final
        #       user turn. Reuse BASE_SYSTEM. Reuse self._ticket_block for each example.
        raise NotImplementedError("return (system, messages) where `messages` is an alternating")


class ChainOfThoughtStrategy(PromptStrategy):
    name = "chain_of_thought"

    def build(self, ticket):
        # TODO: same single-turn shape as ZeroShot, but the system prompt must instruct
        #       the model to reason step by step about (a) what the customer wants,
        #       (b) business impact -> priority, (c) tone -> sentiment, (d) whether a
        #       human must act, BEFORE emitting the schema. Keep BASE_SYSTEM's rules.
        raise NotImplementedError("same single-turn shape as ZeroShot, but the system prompt must instruct")
