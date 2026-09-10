
"""The RAG service."""
from __future__ import annotations

import re

import numpy as np

from llmlab import Embedder, LLMClient, span

from .schemas import REFUSAL, SYSTEM, Answer, Chunk, Retrieved


def _split(text: str, size: int = 320, overlap: int = 40) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    step = max(1, size - overlap)
    return [text[i:i + size] for i in range(0, len(text), step)]


class RAGPipeline:
    def __init__(self, embedder: Embedder, llm: LLMClient, *, k: int = 3,
                 min_score: float = 0.30, max_tokens: int = 250):
        self.embedder = embedder
        self.llm = llm
        self.k = k
        self.min_score = min_score
        self.max_tokens = max_tokens
        self.chunks: list[Chunk] = []
        self._X: np.ndarray | None = None

    def ingest(self, docs: dict[str, str]) -> "RAGPipeline":
        self.chunks = [Chunk(id=len(self.chunks) + i, doc=name, text=c)
                       for name, body in docs.items()
                       for i, c in enumerate(_split(body))]
        # reindex ids to be contiguous
        for i, ch in enumerate(self.chunks):
            ch.id = i
        self._X = self.embedder.embed([c.text for c in self.chunks])
        return self

    def _retrieve(self, question: str) -> list[Retrieved]:
        # TODO: embed the question, cosine against self._X, return the top self.k chunks
        #   as Retrieved(..., score=float). Wrap in span("retrieve").
        with span("retrieve", kind="retriever", q=question, k=self.k):
            q = self.embedder.embed([question])[0]
            sims = self._X @ q
            out = []
            for i in np.argsort(-sims)[: self.k]:
                c = self.chunks[i]
                out.append(Retrieved(id=c.id, doc=c.doc, text=c.text, score=float(sims[i])))
            return out

    def _build_prompt(self, question: str, chunks: list[Retrieved]) -> list[dict]:
        # TODO: one user message: numbered context passages "[1] (doc) text" then
        #   "Question: ...". (SYSTEM is passed separately.)
        ctx = "\n\n".join(f"[{i + 1}] ({c.doc}) {c.text}" for i, c in enumerate(chunks))
        return [{"role": "user", "content": f"Context:\n{ctx}\n\nQuestion: {question}"}]

    def _attribute(self, answer: str, chunks: list[Retrieved]) -> list[str]:
        # TODO: for each answer sentence (len > 15), find the chunk with the highest
        #   embedding cosine; if >= 0.35 count that chunk's `doc` as a source. Return the
        #   unique source doc names, most-supported first. (If the answer is the REFUSAL,
        #   return [].)
        if answer.strip() == REFUSAL or not chunks:
            return []
        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", answer) if len(s.strip()) > 15]
        if not sents:
            return []
        sv = self.embedder.embed(sents)
        cv = self.embedder.embed([c.text for c in chunks])
        seen: dict[str, float] = {}
        for row in sv @ cv.T:
            j = int(np.argmax(row))
            if row[j] >= 0.35:
                seen[chunks[j].doc] = max(seen.get(chunks[j].doc, 0.0), float(row[j]))
        return [d for d, _ in sorted(seen.items(), key=lambda kv: -kv[1])]

    def answer(self, question: str) -> Answer:
        # TODO:
        #   retrieve; if the top score < self.min_score -> return the gated refusal Answer
        #     (gated=True, no LLM call), still attaching `retrieved`.
        #   else call self.llm.chat(prompt, system=SYSTEM, max_tokens=self.max_tokens),
        #     build sources via self._attribute, confidence = top score.
        #   wrap the whole thing in span("answer", kind="chain").
        with span("answer", kind="chain", q=question):
            chunks = self._retrieve(question)
            if not chunks or chunks[0].score < self.min_score:
                return Answer(text=REFUSAL, gated=True, confidence=chunks[0].score if chunks else 0.0,
                              retrieved=chunks)
            resp = self.llm.chat(self._build_prompt(question, chunks), system=SYSTEM,
                                 max_tokens=self.max_tokens)
            return Answer(text=resp.text.strip(),
                          sources=self._attribute(resp.text, chunks),
                          gated=False, confidence=chunks[0].score, retrieved=chunks)
