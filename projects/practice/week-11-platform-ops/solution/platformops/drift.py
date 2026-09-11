"""DriftMonitor — Population Stability Index + KS test over a reference vs current sample."""
from __future__ import annotations

import numpy as np
from scipy.stats import ks_2samp


def psi(reference, current, bins: int = 10) -> float:
    ref = np.asarray(reference, float)
    cur = np.asarray(current, float)
    edges = np.quantile(ref, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    ref_pct = np.clip(np.histogram(ref, edges)[0] / len(ref), 1e-6, None)
    cur_pct = np.clip(np.histogram(cur, edges)[0] / len(cur), 1e-6, None)
    return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))


def categorical_psi(ref_labels, cur_labels) -> float:
    cats = sorted(set(ref_labels) | set(cur_labels))
    ref = np.array([np.mean([l == c for l in ref_labels]) for c in cats])
    cur = np.array([np.mean([l == c for l in cur_labels]) for c in cats])
    ref = np.clip(ref, 1e-6, None)
    cur = np.clip(cur, 1e-6, None)
    return float(np.sum((cur - ref) * np.log(cur / ref)))


def ks_drift(reference, current, alpha: float = 0.01) -> dict:
    stat, p = ks_2samp(reference, current)
    return {"ks_stat": round(float(stat), 4), "p_value": float(p), "drift": bool(p < alpha)}


class DriftMonitor:
    """Holds a reference window; .assess(current) -> a verdict dict."""
    def __init__(self, reference, *, psi_limit: float = 0.25):
        self.reference = np.asarray(reference, float)
        self.psi_limit = psi_limit

    def assess(self, current) -> dict:
        p = psi(self.reference, current)
        ks = ks_drift(self.reference, current)
        return {"psi": round(p, 4), "psi_limit": self.psi_limit,
                "ks": ks, "drift": bool(p > self.psi_limit or ks["drift"])}
