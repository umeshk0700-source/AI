
"""Semantic response cache — a repeated *meaning* is a hit, not just a repeated string."""
from __future__ import annotations

import numpy as np

from llmlab import Embedder, span


class SemanticCache:
    def __init__(self, embedder: Embedder, threshold: float = 0.92, max_entries: int = 1000):
        self.embedder = embedder
        self.threshold = threshold
        self.max_entries = max_entries
        self._keys: list[str] = []
        self._vecs: list[np.ndarray] = []
        self._vals: list[str] = []
        self.hits = 0
        self.misses = 0

    def get(self, prompt: str) -> str | None:
        # TODO: if the cache is empty -> miss. Otherwise embed `prompt`, cosine against every
        #   stored vector; if the best similarity >= self.threshold, count a hit and return
        #   the stored value; else count a miss and return None. Wrap in span("cache.get").
        with span("cache.get", kind="cache") as s:
            if not self._vecs:
                self.misses += 1
                s.outputs = {"hit": False}
                return None
            q = self.embedder.embed([prompt])[0]
            sims = np.stack(self._vecs) @ q
            j = int(np.argmax(sims))
            if sims[j] >= self.threshold:
                self.hits += 1
                s.outputs = {"hit": True, "sim": round(float(sims[j]), 3)}
                return self._vals[j]
            self.misses += 1
            s.outputs = {"hit": False, "best_sim": round(float(sims[j]), 3)}
            return None

    def put(self, prompt: str, value: str) -> None:
        # TODO: store (prompt, its embedding, value). Evict the oldest entry when over
        #   self.max_entries.
        self._keys.append(prompt)
        self._vecs.append(self.embedder.embed([prompt])[0])
        self._vals.append(value)
        if len(self._keys) > self.max_entries:
            self._keys.pop(0); self._vecs.pop(0); self._vals.pop(0)

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0
