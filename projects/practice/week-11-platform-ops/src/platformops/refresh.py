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
        # TODO: collect a reason string for each breached condition:
        #   psi_value > psi_limit
        #   signals.grounded_rate < grounded_floor
        #   baseline_eval - eval_score > eval_decay
        #   signals.thumbs_down_rate > thumbs_down_ceiling
        # refresh = len(reasons) >= self.min_reasons
        raise NotImplementedError
