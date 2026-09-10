
"""Given — the decision inputs and outputs."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Missing(str, Enum):
    knowledge = "knowledge"     # facts the model doesn't have
    behaviour = "behaviour"     # tone / format / a skill
    both = "both"


@dataclass
class Requirement:
    description: str
    missing: Missing
    knowledge_changes: bool          # does the underlying knowledge change often?
    knowledge_volume_tokens: int     # size of the corpus that would go in context
    calls_per_month: int
    have_labeled_data: bool
    latency_sensitive: bool = False


@dataclass
class Recommendation:
    approach: str                    # "prompt" | "rag" | "finetune"
    reasons: list[str] = field(default_factory=list)
    projected_monthly_usd: float = 0.0
    alternatives: list[str] = field(default_factory=list)
