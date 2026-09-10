
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
        deltas = {m: round(candidate.metric(m) - self.baseline.metric(m), 4)
                  for m in self.baseline.by_scorer}
        blocking: list[str] = []
        notes: list[str] = []
        for assertion in self.hard_assertions:
            ok, msg = assertion(candidate)
            if not ok:
                blocking.append(f"HARD: {msg}")
        for m in self.must_not_regress:
            d = deltas.get(m, 0.0)
            notes.append(f"{m}: {self.baseline.metric(m):.3f} -> {candidate.metric(m):.3f} "
                         f"({d:+.3f})")
            if d < -self.tolerance:
                blocking.append(m)
        return Verdict(passed=not blocking, deltas=deltas, blocking=blocking, notes=notes)
