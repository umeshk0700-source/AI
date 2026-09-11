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
    # TODO: split `text` into ~`size`-char chunks that overlap by `overlap` chars, on
    # whitespace boundaries where possible. Return Chunk(doc_id, ord=0,1,2,..., text=...).
    raise NotImplementedError
