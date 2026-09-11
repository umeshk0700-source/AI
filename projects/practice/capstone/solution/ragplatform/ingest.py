"""Ingest: turn raw documents into overlapping, traceable chunks."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    doc_id: str
    ord: int
    text: str
    @property
    def cite(self) -> str:
        return f"{self.doc_id}#{self.ord}"


def chunk_doc(doc_id: str, text: str, *, size: int = 240, overlap: int = 40) -> list[Chunk]:
    words = text.split()
    chunks, cur, ln = [], [], 0
    step = max(1, size - overlap)
    joined = " ".join(words)
    i = 0
    while i < len(joined):
        piece = joined[i:i + size]
        if len(piece) == size and " " in piece:            # don't cut mid-word
            piece = piece.rsplit(" ", 1)[0]
        piece = piece.strip()
        if piece:
            chunks.append(Chunk(doc_id, len(chunks), piece))
        i += max(step, len(piece) - overlap) if piece else step
    return chunks
