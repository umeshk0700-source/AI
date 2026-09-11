"""ReleaseGate — block a candidate bundle that regresses quality vs the shipped baseline."""
from __future__ import annotations

from .schemas import EvalReport, GateVerdict


class ReleaseGate:
    def __init__(self, baseline: EvalReport, *, tolerance: float = 0.03,
                 pass_mark: float = 0.7, allow_regress: tuple[str, ...] = ()):
        self.baseline = baseline
        self.tolerance = tolerance
        self.pass_mark = pass_mark
        self.allow_regress = set(allow_regress)

    def check(self, candidate: EvalReport) -> GateVerdict:
        # TODO:
        #   delta = candidate.mean - self.baseline.mean
        #   regressions = candidate.regressions(self.baseline, self.pass_mark),
        #     minus anything in self.allow_regress
        #   ok = delta >= -self.tolerance AND no unexpected regressions
        #   notes: one line for the aggregate move, one for the regression count
        delta = round(candidate.mean - self.baseline.mean, 4)
        regressions = [c for c in candidate.regressions(self.baseline, self.pass_mark)
                       if c not in self.allow_regress]
        ok = (delta >= -self.tolerance) and not regressions
        notes = [
            f"aggregate {self.baseline.mean:.3f} -> {candidate.mean:.3f} ({delta:+.3f})",
            f"{len(regressions)} unexpected regression(s)",
        ]
        return GateVerdict(ok=ok, delta=delta, unexpected_regressions=regressions, notes=notes)
