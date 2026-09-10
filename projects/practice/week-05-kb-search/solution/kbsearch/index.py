
"""Vector indexes + BM25."""
from __future__ import annotations

import math
import re
from collections import Counter

import numpy as np


class FlatIndex:
    """Exact brute-force cosine search. Given."""

    def __init__(self, vectors: np.ndarray):
        self.X = vectors                       # (N, d), assumed L2-normalised

    def search(self, q: np.ndarray, k: int = 10) -> list[int]:
        return [int(i) for i in np.argsort(-(self.X @ q))[:k]]


def _kmeans(X: np.ndarray, k: int, iters: int = 25, seed: int = 0):
    r = np.random.default_rng(seed)
    C = X[r.choice(len(X), k, replace=False)].copy()
    for _ in range(iters):
        assign = np.argmax(X @ C.T, axis=1)
        for j in range(k):
            m = X[assign == j]
            if len(m):
                v = m.mean(0)
                C[j] = v / (np.linalg.norm(v) + 1e-9)
    return C, np.argmax(X @ C.T, axis=1)


class IVFIndex:
    """Inverted-file ANN: cluster, then probe the nearest `nprobe` cells."""

    def __init__(self, vectors: np.ndarray):
        self.X = vectors
        self.C = None                          # (nlist, d) centroids
        self.lists: list[np.ndarray] = []      # lists[j] = vector ids in cell j

    def build(self, nlist: int = 32) -> "IVFIndex":
        # TODO: run _kmeans(self.X, nlist) -> centroids C and per-vector assignment.
        #   store self.C and self.lists (self.lists[j] = np.where(assign == j)[0]).
        self.C, assign = _kmeans(self.X, nlist)
        self.lists = [np.where(assign == j)[0] for j in range(nlist)]
        return self

    def search(self, q: np.ndarray, k: int = 10, nprobe: int = 4) -> list[int]:
        # TODO: pick the nprobe centroids closest to q, gather their vector ids,
        #   rank those candidates by exact cosine (self.X[cand] @ q), return top-k ids.
        #   handle the empty-candidate case (return []).
        cells = np.argsort(-(self.C @ q))[:nprobe]
        cand = np.concatenate([self.lists[c] for c in cells]) if len(cells) else np.array([], int)
        if len(cand) == 0:
            return []
        order = np.argsort(-(self.X[cand] @ q))[:k]
        return [int(cand[i]) for i in order]


_TOK = re.compile(r"[a-z0-9]+")


class BM25:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.docs: list[list[str]] = []
        self.idf: dict[str, float] = {}
        self.avgdl = 0.0

    def index(self, corpus: list[str]) -> "BM25":
        # TODO: tokenise each doc with _TOK.findall(lower). Compute:
        #   self.docs, self.avgdl (mean doc length),
        #   self.idf[w] = log(1 + (N - df + 0.5) / (df + 0.5))   for each term w.
        self.docs = [_TOK.findall(d.lower()) for d in corpus]
        n = len(self.docs)
        self.avgdl = float(np.mean([len(d) for d in self.docs])) if self.docs else 0.0
        df = Counter(w for d in self.docs for w in set(d))
        self.idf = {w: math.log(1 + (n - c + 0.5) / (c + 0.5)) for w, c in df.items()}
        return self

    def search(self, query: str, k: int = 10) -> list[int]:
        # TODO: BM25 score every doc for `query`, return the top-k doc ids by score
        #   (descending). Score of doc i for query term w with freq f and doc length dl:
        #   idf[w] * f*(k1+1) / (f + k1*(1 - b + b*dl/avgdl)).
        q = _TOK.findall(query.lower())
        scores = np.zeros(len(self.docs))
        for i, d in enumerate(self.docs):
            tf, dl, s = Counter(d), len(d), 0.0
            for w in q:
                if w in self.idf and tf[w]:
                    f = tf[w]
                    s += self.idf[w] * f * (self.k1 + 1) / (
                        f + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
            scores[i] = s
        return [int(i) for i in np.argsort(-scores)[:k]]
