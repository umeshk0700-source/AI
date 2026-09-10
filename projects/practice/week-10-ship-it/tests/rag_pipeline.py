"""Minimal RAG pipeline for the live test only (mirrors Week 6)."""
from __future__ import annotations
import re
from dataclasses import dataclass, field
import numpy as np
from llmlab import span

REFUSAL = "I don't know based on the handbook."
SYSTEM = ("You are the HR assistant. Answer ONLY from the numbered context passages, concisely. "
          f"If they don't contain the answer, reply exactly: {REFUSAL!r} without quotes.")


@dataclass
class _Ans:
    text: str
    sources: list = field(default_factory=list)
    gated: bool = False
    confidence: float = 0.0


def _split(t, size=320, overlap=40):
    t = re.sub(r"\s+", " ", t).strip()
    return [t[i:i+size] for i in range(0, len(t), max(1, size-overlap))]


class RAGPipeline:
    def __init__(self, embedder, llm, *, k=3, min_score=0.3, max_tokens=200):
        self.e, self.llm, self.k, self.min_score, self.max_tokens = embedder, llm, k, min_score, max_tokens

    def ingest(self, docs):
        self.chunks = [(name, c) for name, body in docs.items() for c in _split(body)]
        self.X = self.e.embed([c for _, c in self.chunks])
        return self

    def answer(self, q):
        with span("answer", kind="chain"):
            qv = self.e.embed([q])[0]
            sims = self.X @ qv
            idx = np.argsort(-sims)[:self.k]
            top = float(sims[idx[0]])
            if top < self.min_score:
                return _Ans(REFUSAL, [], True, top)
            ctx = "\n".join(f"[{i+1}] ({self.chunks[j][0]}) {self.chunks[j][1]}"
                            for i, j in enumerate(idx))
            r = self.llm.chat([{"role": "user", "content": f"Context:\n{ctx}\n\nQuestion: {q}"}],
                              system=SYSTEM, max_tokens=self.max_tokens)
            srcs = [] if r.text.strip() == REFUSAL else sorted(
                {self.chunks[j][0] for j in idx[:2]})
            return _Ans(r.text.strip(), srcs, False, top)
