
"""Given — request/response contract."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    gated: bool
    confidence: float
    trace_id: str
    latency_ms: float


class ErrorResponse(BaseModel):
    error: str
    trace_id: str
