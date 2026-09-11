"""Typed results shared across the platform-ops components."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EvalReport:
    """Aggregate + per-case scores from one run of the eval suite."""
    bundle_id: str
    per_case: dict[str, float]

    @property
    def mean(self) -> float:
        return sum(self.per_case.values()) / len(self.per_case) if self.per_case else 0.0

    def regressions(self, baseline: "EvalReport", pass_mark: float) -> list[str]:
        """Cases that went from >= pass_mark in `baseline` to < pass_mark here."""
        out = []
        for case, score in self.per_case.items():
            if baseline.per_case.get(case, 0.0) >= pass_mark > score:
                out.append(case)
        return sorted(out)


@dataclass(frozen=True)
class GateVerdict:
    ok: bool
    delta: float
    unexpected_regressions: list[str]
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Signals:
    n: int
    p95_ms: float
    error_rate: float
    grounded_rate: float
    thumbs_down_rate: float
    cost_per_req_usd: float


@dataclass(frozen=True)
class CanaryResult:
    outcome: str                 # "promoted" | "rolled_back"
    final_pct: int
    steps: list[dict]


@dataclass(frozen=True)
class RefreshDecision:
    refresh: bool
    reasons: list[str]
