
"""Given."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Chunk:
    id: int
    doc: str          # source doc / section name
    text: str


@dataclass
class Retrieved(Chunk):
    score: float = 0.0


@dataclass
class Answer:
    text: str
    sources: list[str] = field(default_factory=list)
    gated: bool = False
    confidence: float = 0.0
    retrieved: list[Retrieved] = field(default_factory=list)


REFUSAL = "I don't know based on the handbook."

SYSTEM = (
    "You are the Cirrus HR assistant. Answer ONLY from the numbered context passages. "
    "Be concise (1-3 sentences). If the passages do not contain the answer, reply exactly: "
    f"{REFUSAL!r} (without the quotes). Do not use outside knowledge."
)
