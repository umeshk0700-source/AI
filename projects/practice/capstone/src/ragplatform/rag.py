"""RAG with citations + a faithfulness check."""
from __future__ import annotations

from dataclasses import dataclass

from llmlab import span

import re

from .index import VectorIndex


def _markers(text: str):
    return re.findall(r"\[(\d+)\]", text)

SYSTEM = (
    "Answer ONLY from the numbered context. Cite every claim as [n] using the context "
    "numbers. If the context does not contain the answer, reply exactly: I don't know."
)


@dataclass
class Answer:
    text: str
    citations: list[str]
    grounded: bool


class RAGPipeline:
    def __init__(self, index: VectorIndex, llm, *, k: int = 4, min_score: float = 0.15):
        self.index, self.llm, self.k, self.min_score = index, llm, k, min_score

    def answer(self, question: str) -> Answer:
        # TODO (wrap the whole thing in `with span("rag.answer"):`):
        #   hits = self.index.search(question, self.k) filtered to score >= self.min_score
        #   if no hits -> Answer("I don't know", [], grounded=True)
        #   build a context block "[1] <text>\n[2] <text> ..." and matching cite list
        #   resp = self.llm.chat([{"role":"user","content": f"{context}\n\nQ: {question}"}],
        #                        system=SYSTEM)
        #   citations = the [n] markers that actually appear in resp.text, mapped to chunk.cite
        #   grounded = self.faithful(resp.text, [c for c,_ in hits])
        raise NotImplementedError

    @staticmethod
    def faithful(answer_text: str, chunks) -> bool:
        # TODO: crude check — "I don't know" is always faithful; otherwise require at least
        # one [n] citation marker in the answer.
        raise NotImplementedError
