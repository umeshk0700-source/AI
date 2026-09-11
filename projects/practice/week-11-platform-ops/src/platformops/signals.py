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
        # TODO: append event; keep only the last self.window events
        raise NotImplementedError

    def signals(self) -> Signals:
        # TODO: build a Signals from self.buf:
        #   p95_ms  = 95th percentile of latency_ms
        #   error_rate / grounded_rate / thumbs_down_rate = means of those bool fields
        #   cost_per_req_usd = mean(tokens_in*PRICE["in"] + tokens_out*PRICE["out"])
        raise NotImplementedError
