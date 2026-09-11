"""DriftMonitor — Population Stability Index + KS test over a reference vs current sample."""
from __future__ import annotations

import numpy as np
from scipy.stats import ks_2samp


def psi(reference, current, bins: int = 10) -> float:
    # TODO:
    #   edges = quantiles of `reference` at linspace(0,1,bins+1); set edges[0]=-inf, edges[-1]=+inf
    #   ref_pct / cur_pct = histogram share per bin, clipped to >= 1e-6
    #   return sum( (cur_pct - ref_pct) * ln(cur_pct / ref_pct) )
    raise NotImplementedError


def categorical_psi(ref_labels, cur_labels) -> float:
    # TODO: same formula but over the proportion of each category label
    raise NotImplementedError


def ks_drift(reference, current, alpha: float = 0.01) -> dict:
    # TODO: stat, p = ks_2samp(...); return {"ks_stat", "p_value", "drift": p < alpha}
    raise NotImplementedError


class DriftMonitor:
    """Holds a reference window; .assess(current) -> a verdict dict."""
    def __init__(self, reference, *, psi_limit: float = 0.25):
        self.reference = np.asarray(reference, float)
        self.psi_limit = psi_limit

    def assess(self, current) -> dict:
        # TODO: compute psi + ks_drift vs self.reference;
        #   "drift" is True if psi > psi_limit OR ks says drift
        raise NotImplementedError
