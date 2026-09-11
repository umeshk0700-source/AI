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
        with span("rag.answer", question=question):
            hits = [(c, s) for c, s in self.index.search(question, self.k) if s >= self.min_score]
            if not hits:
                return Answer("I don't know", [], grounded=True)
            lines, cites = [], []
            for i, (c, _) in enumerate(hits, 1):
                lines.append(f"[{i}] {c.text}")
                cites.append(c.cite)
            context = "\n".join(lines)
            resp = self.llm.chat(
                [{"role": "user", "content": f"{context}\n\nQ: {question}"}], system=SYSTEM)
            used = sorted({int(m) for m in _markers(resp.text) if 1 <= int(m) <= len(cites)})
            citations = [cites[n - 1] for n in used]
            return Answer(resp.text, citations, self.faithful(resp.text, hits))

    @staticmethod
    def faithful(answer_text: str, chunks) -> bool:
        if answer_text.strip().lower().startswith("i don't know"):
            return True
        return bool(_markers(answer_text))
