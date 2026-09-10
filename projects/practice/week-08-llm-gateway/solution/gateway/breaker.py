
"""A circuit breaker: stop hammering a failing dependency, probe it periodically."""
from __future__ import annotations

import time
from typing import Callable


class CircuitOpen(RuntimeError):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, reset_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = "closed"          # closed | open | half_open
        self.failures = 0
        self.opened_at = 0.0

    def call(self, fn: Callable, *args, **kwargs):
        # TODO:
        #   - state "open": if time.monotonic() - self.opened_at >= reset_timeout -> set
        #     state to "half_open" and continue; otherwise raise CircuitOpen.
        #   - try fn(*args, **kwargs):
        #       success -> reset (state="closed", failures=0), return the result.
        #       exception -> self.failures += 1; if self.failures >= failure_threshold OR
        #         state == "half_open": state="open", opened_at=now. re-raise.
        if self.state == "open":
            if time.monotonic() - self.opened_at >= self.reset_timeout:
                self.state = "half_open"
            else:
                raise CircuitOpen("circuit is open")
        try:
            result = fn(*args, **kwargs)
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold or self.state == "half_open":
                self.state = "open"
                self.opened_at = time.monotonic()
            raise
        self.state = "closed"
        self.failures = 0
        return result
