"""RagPlatform: wire ingest -> index -> RAG -> agent -> gateway into one object."""
from __future__ import annotations

from .agent import Agent
from .gateway import Gateway
from .index import VectorIndex
from .ingest import chunk_doc
from .rag import RAGPipeline


class RagPlatform:
    def __init__(self, docs: dict[str, str], llm, *, fallback_llm=None, embedder=None):
        self.gateway = Gateway(llm, fallback_llm)
        self.index = VectorIndex(embedder)
        for doc_id, text in docs.items():
            self.index.add(chunk_doc(doc_id, text))
        self.rag = RAGPipeline(self.index, self.gateway)
        self.agent = Agent(self.rag, self.gateway)

    def ask(self, question: str, *, agentic: bool = False) -> str:
        return self.agent.run(question) if agentic else self.rag.answer(question).text
