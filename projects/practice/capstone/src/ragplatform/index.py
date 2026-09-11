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
        # TODO: store chunks; embed their .text with self.embedder.embed([...]) and keep the
        # matrix (already L2-normalised by the embedder) for cosine search.
        raise NotImplementedError

    def search(self, query: str, k: int = 4) -> list[tuple[Chunk, float]]:
        # TODO: embed the query, cosine-score against self._mat, return the top-k
        # (Chunk, score) pairs sorted by score desc.
        raise NotImplementedError
