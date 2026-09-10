
"""Given."""
from __future__ import annotations

from dataclasses import dataclass, field
from pydantic import BaseModel, Field


class Extraction(BaseModel):
    vendor: str
    invoice_number: str
    total: float
    currency: str
    due_date: str            # ISO yyyy-mm-dd or "" if absent
    line_item_count: int

    def fields(self) -> dict:
        return self.model_dump()


@dataclass
class ModelResult:
    label: str
    field_accuracy: float          # mean over fields over invoices
    exact_match_rate: float        # fraction of invoices with ALL fields right
    mean_latency_s: float
    p95_latency_s: float
    cost_usd: float
    per_invoice: list[dict] = field(default_factory=list)


@dataclass
class SelectionMemo:
    recommended: str
    rationale: list[str]
    min_accuracy: float
    table: list[dict]              # one row per model: label, accuracy, $/1k, p95_s
    runner_up: str | None = None
