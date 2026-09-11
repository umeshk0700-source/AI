"""Vector index over chunks, using an llmlab embedder (local by default)."""
from __future__ import annotations

import numpy as np

from llmlab import get_embedder

from .ingest import Chunk


class VectorIndex:
    def __init__(self, embedder=None):
        self.embedder = embedder or get_embedder("local")
        self.chunks: list[Chunk] = []
        self._mat: np.ndarray | None = None

    def add(self, chunks: list[Chunk]) -> None:
        self.chunks.extend(chunks)
        vecs = self.embedder.embed([c.text for c in self.chunks])
        self._mat = np.asarray(vecs, dtype=float)

    def search(self, query: str, k: int = 4) -> list[tuple[Chunk, float]]:
        q = np.asarray(self.embedder.embed([query])[0], dtype=float)
        scores = self._mat @ q
        order = np.argsort(scores)[::-1][:k]
        return [(self.chunks[i], float(scores[i])) for i in order]
