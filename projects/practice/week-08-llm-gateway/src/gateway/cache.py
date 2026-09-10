
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
        raise NotImplementedError("if the cache is empty -> miss. Otherwise embed `prompt`, cosine against every")

    def put(self, prompt: str, value: str) -> None:
        # TODO: store (prompt, its embedding, value). Evict the oldest entry when over
        #   self.max_entries.
        raise NotImplementedError("store (prompt, its embedding, value). Evict the oldest entry when over")

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0
