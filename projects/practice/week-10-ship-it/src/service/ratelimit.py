
"""A token-bucket rate limiter, keyed by API key."""
from __future__ import annotations

import time


class TokenBucket:
    def __init__(self, rate_per_sec: float, burst: int):
        self.rate = rate_per_sec
        self.burst = burst
        self._state: dict[str, tuple[float, float]] = {}   # key -> (tokens, last_ts)

    def allow(self, key: str) -> bool:
        # TODO: classic token bucket.
        #   now = time.monotonic()
        #   tokens, last = self._state.get(key, (self.burst, now))
        #   tokens = min(self.burst, tokens + (now - last) * self.rate)   # refill
        #   if tokens >= 1: consume one, store (tokens-1, now), return True
        #   else: store (tokens, now), return False
        raise NotImplementedError("classic token bucket.")
