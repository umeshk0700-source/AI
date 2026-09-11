"""RefreshTrigger — fuse drift + quality decay + feedback into a refresh decision."""
from __future__ import annotations

from .schemas import RefreshDecision, Signals


class RefreshTrigger:
    def __init__(self, *, psi_limit: float = 0.25, grounded_floor: float = 0.75,
                 eval_decay: float = 0.05, thumbs_down_ceiling: float = 0.10,
                 min_reasons: int = 2):
        self.psi_limit = psi_limit
        self.grounded_floor = grounded_floor
        self.eval_decay = eval_decay
        self.thumbs_down_ceiling = thumbs_down_ceiling
        self.min_reasons = min_reasons

    def decide(self, *, psi_value: float, signals: Signals,
               eval_score: float, baseline_eval: float) -> RefreshDecision:
        reasons: list[str] = []
        if psi_value > self.psi_limit:
            reasons.append(f"input drift PSI={psi_value:.2f}")
        if signals.grounded_rate < self.grounded_floor:
            reasons.append(f"grounded_rate={signals.grounded_rate:.2f}")
        if baseline_eval - eval_score > self.eval_decay:
            reasons.append(f"eval decay {baseline_eval:.2f}->{eval_score:.2f}")
        if signals.thumbs_down_rate > self.thumbs_down_ceiling:
            reasons.append(f"thumbs_down={signals.thumbs_down_rate:.2f}")
        return RefreshDecision(refresh=len(reasons) >= self.min_reasons, reasons=reasons)
