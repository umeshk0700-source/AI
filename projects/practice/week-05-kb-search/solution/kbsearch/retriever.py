
"""The production retriever: dense + BM25, fused with RRF."""
from __future__ import annotations

import numpy as np

from llmlab import Embedder, span

from .chunk import recursive_split
from .index import BM25, FlatIndex, IVFIndex


class HybridRetriever:
    def __init__(self, embedder: Embedder, docs: list[str], *, use_ivf: bool = False,
                 nlist: int = 32):
        self.embedder = embedder
        self.docs = docs
        self.X = embedder.embed(docs)
        self.dense = IVFIndex(self.X).build(min(nlist, max(2, len(docs) // 4))) if use_ivf \
            else FlatIndex(self.X)
        self.use_ivf = use_ivf
        self.bm25 = BM25().index(docs)

    def _dense_ranking(self, query: str) -> list[int]:
        q = self.embedder.embed([query])[0]
        if self.use_ivf:
            return self.dense.search(q, k=len(self.docs), nprobe=8)
        return self.dense.search(q, k=len(self.docs))

    def search(self, query: str, k: int = 5, c: int = 60) -> list[int]:
        # TODO: Reciprocal Rank Fusion of the dense ranking (self._dense_ranking) and the
        #   BM25 ranking (self.bm25.search(query, k=len(self.docs))).
        #   score(doc) = 1/(c + rank_dense[doc]) + 1/(c + rank_bm25[doc])   (missing -> large rank)
        #   return the top-k doc ids by fused score. Wrap in span("retrieve").
        with span("retrieve", kind="retriever", query=query, k=k):
            d_rank = {doc: r for r, doc in enumerate(self._dense_ranking(query))}
            b_rank = {doc: r for r, doc in enumerate(self.bm25.search(query, k=len(self.docs)))}
            big = len(self.docs) + 1
            fused = {i: 1 / (c + d_rank.get(i, big)) + 1 / (c + b_rank.get(i, big))
                     for i in range(len(self.docs))}
            return sorted(fused, key=lambda i: -fused[i])[:k]
