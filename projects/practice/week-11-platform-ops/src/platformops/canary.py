"""CanaryController — ramp traffic to a candidate while guardrail metrics hold, else roll back."""
from __future__ import annotations

from typing import Callable

from .schemas import CanaryResult

# SLOs the candidate must satisfy at every step.
DEFAULT_SLO = {"p95_latency_s": 2.0, "error_rate": 0.03, "min_quality": 0.75}


class CanaryController:
    def __init__(self, measure: Callable[[str, int], dict], *,
                 stable: str, candidate: str,
                 steps: tuple[int, ...] = (5, 25, 50, 100),
                 slo: dict | None = None):
        # `measure(version, n)` -> {"p95_latency_s", "error_rate", "quality"}
        self.measure = measure
        self.stable = stable
        self.candidate = candidate
        self.steps = steps
        self.slo = slo or dict(DEFAULT_SLO)

    def _healthy(self, m: dict) -> bool:
        # TODO: True iff p95 <= slo p95, error_rate <= slo error_rate, quality >= slo min_quality
        raise NotImplementedError

    def roll_out(self, n_per_step: int = 400) -> CanaryResult:
        # TODO:
        #   for pct in self.steps:
        #     m = self.measure(self.candidate, n_per_step); record {"pct", **m, "healthy": ...}
        #     if not healthy -> return CanaryResult("rolled_back", 0, steps)
        #   return CanaryResult("promoted", 100, steps)
        raise NotImplementedError
