
"""Domain types for the triage service. Given — you don't edit this."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Category(str, Enum):
    billing = "billing"
    bug = "bug"
    how_to = "how_to"
    account = "account"
    security = "security"
    feature_request = "feature_request"
    legal = "legal"
    other = "other"


class Priority(str, Enum):
    p1 = "P1"   # outage / data loss / security — 1h
    p2 = "P2"   # major impairment — 4h
    p3 = "P3"   # normal — 1 business day
    p4 = "P4"   # low / cosmetic — 3 business days

    @property
    def sla_hours(self) -> int:
        return {"P1": 1, "P2": 4, "P3": 24, "P4": 72}[self.value]

    def bump(self) -> "Priority":
        order = ["P4", "P3", "P2", "P1"]
        i = order.index(self.value)
        return Priority(order[min(i + 1, len(order) - 1)])


class Sentiment(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"
    angry = "angry"


class CustomerTier(str, Enum):
    free = "free"
    pro = "pro"
    enterprise = "enterprise"


class Ticket(BaseModel):
    id: str
    subject: str
    body: str
    customer_tier: CustomerTier = CustomerTier.free
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("body")
    @classmethod
    def _nonempty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("ticket body is empty")
        return v


class Classification(BaseModel):
    """What the LLM returns — the raw read, before business rules."""
    category: Category
    priority: Priority
    sentiment: Sentiment
    needs_human: bool
    draft_reply: str
    confidence: float = Field(ge=0.0, le=1.0)


class TriageResult(BaseModel):
    """The final decision the routing system consumes."""
    ticket_id: str
    category: Category
    priority: Priority
    sentiment: Sentiment
    needs_human: bool
    route_to_team: str
    sla_due_at: datetime
    draft_reply: str
    confidence: float
    rules_applied: list[str] = Field(default_factory=list)

    @classmethod
    def sla_from(cls, created_at: datetime, priority: Priority) -> datetime:
        return created_at + timedelta(hours=priority.sla_hours)
