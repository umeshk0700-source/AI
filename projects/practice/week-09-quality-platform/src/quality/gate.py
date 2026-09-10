
"""Regression gate: compare a candidate Report to a frozen baseline."""
from __future__ import annotations

from typing import Callable

from .schemas import Report, Verdict


class RegressionGate:
    def __init__(self, baseline: Report, *,
                 must_not_regress: tuple[str, ...] = ("judge", "contains"),
                 tolerance: float = 0.03,
                 hard_assertions: list[Callable[[Report], tuple[bool, str]]] | None = None):
        self.baseline = baseline
        self.must_not_regress = must_not_regress
        self.tolerance = tolerance
        self.hard_assertions = hard_assertions or []

    def check(self, candidate: Report) -> Verdict:
        # TODO:
        #   deltas[m] = candidate.metric(m) - baseline.metric(m)  for every scorer in the baseline
        #   run each hard assertion on `candidate`: (ok, msg) -> if not ok, it's blocking
        #     ("HARD: <msg>") and the verdict fails regardless of deltas.
        #   for each m in must_not_regress: if deltas[m] < -self.tolerance -> blocking.append(m)
        #   passed = not blocking. notes: a one-line summary per must_not_regress metric.
        raise NotImplementedError("#   deltas[m] = candidate.metric(m) - baseline.metric(m)  for every scorer in the baseline")
