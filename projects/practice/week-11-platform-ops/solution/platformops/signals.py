"""SignalAggregator — the golden signals for an LLM service over a rolling trace window."""
from __future__ import annotations

import numpy as np

from .schemas import Signals

# claude-haiku-4-5, USD per token
PRICE = {"in": 0.80 / 1e6, "out": 4.00 / 1e6}


class SignalAggregator:
    def __init__(self, window: int = 500):
        self.window = window
        self.buf: list[dict] = []

    def observe(self, event: dict) -> None:
        self.buf.append(event)
        if len(self.buf) > self.window:
            self.buf.pop(0)

    def signals(self) -> Signals:
        e = self.buf
        lat = np.array([x["latency_ms"] for x in e])
        cost = np.array([x["tokens_in"] * PRICE["in"] + x["tokens_out"] * PRICE["out"] for x in e])
        return Signals(
            n=len(e),
            p95_ms=round(float(np.percentile(lat, 95))),
            error_rate=round(float(np.mean([x["error"] for x in e])), 4),
            grounded_rate=round(float(np.mean([x["grounded"] for x in e])), 4),
            thumbs_down_rate=round(float(np.mean([x["thumbs_down"] for x in e])), 4),
            cost_per_req_usd=round(float(np.mean(cost)), 6),
        )
