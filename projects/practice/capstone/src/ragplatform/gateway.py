"""Gateway: a semantic-ish cache + failover across two llmlab clients."""
from __future__ import annotations

from llmlab import span


class Gateway:
    def __init__(self, primary, fallback=None):
        self.primary, self.fallback = primary, fallback
        self._cache: dict[str, object] = {}
        self.stats = {"hits": 0, "misses": 0, "failovers": 0}

    def chat(self, messages, **kw):
        # TODO (wrap in `with span("gateway.chat"):`):
        #   key = the last user message content (exact-match cache is fine for the capstone)
        #   on cache hit -> stats["hits"] += 1, return cached
        #   else stats["misses"] += 1; try self.primary.chat(messages, **kw)
        #     on Exception, if self.fallback: stats["failovers"] += 1, use it; else re-raise
        #   cache and return the response
        raise NotImplementedError
