"""Gateway: a semantic-ish cache + failover across two llmlab clients."""
from __future__ import annotations

from llmlab import span


class Gateway:
    def __init__(self, primary, fallback=None):
        self.primary, self.fallback = primary, fallback
        self._cache: dict[str, object] = {}
        self.stats = {"hits": 0, "misses": 0, "failovers": 0}

    def chat(self, messages, **kw):
        with span("gateway.chat"):
            key = next((m["content"] for m in reversed(messages) if m.get("role") == "user"), "")
            if key in self._cache:
                self.stats["hits"] += 1
                return self._cache[key]
            self.stats["misses"] += 1
            try:
                resp = self.primary.chat(messages, **kw)
            except Exception:
                if not self.fallback:
                    raise
                self.stats["failovers"] += 1
                resp = self.fallback.chat(messages, **kw)
            self._cache[key] = resp
            return resp
