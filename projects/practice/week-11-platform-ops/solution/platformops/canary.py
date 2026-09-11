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
        return (m["p95_latency_s"] <= self.slo["p95_latency_s"]
                and m["error_rate"] <= self.slo["error_rate"]
                and m["quality"] >= self.slo["min_quality"])

    def roll_out(self, n_per_step: int = 400) -> CanaryResult:
        # TODO:
        steps: list[dict] = []
        for pct in self.steps:
            m = self.measure(self.candidate, n_per_step)
            healthy = self._healthy(m)
            steps.append({"pct": pct, **m, "healthy": healthy})
            if not healthy:
                return CanaryResult(outcome="rolled_back", final_pct=0, steps=steps)
        return CanaryResult(outcome="promoted", final_pct=100, steps=steps)
