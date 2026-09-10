from dataclasses import dataclass, field

import pytest
from fastapi.testclient import TestClient

from service.app import create_app
from service.ratelimit import TokenBucket


@dataclass
class _Ans:
    text: str = "Full-time staff accrue 1.75 vacation days per month."
    sources: list = field(default_factory=lambda: ["Time Off"])
    gated: bool = False
    confidence: float = 0.71


class FakeRAG:
    def __init__(self, raiser=None):
        self._raiser = raiser

    def answer(self, question: str):
        if self._raiser:
            raise self._raiser
        if "stock price" in question:
            return _Ans(text="I don't know based on the handbook.", sources=[], gated=True,
                       confidence=0.1)
        return _Ans()


KEYS = {"good-key": "acme"}


def _client(rag=None, limiter=None):
    return TestClient(create_app(rag or FakeRAG(), api_keys=KEYS, limiter=limiter))


def test_healthz():
    r = _client().get("/healthz")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_no_key_is_401():
    assert _client().post("/ask", json={"question": "hi"}).status_code == 401


def test_wrong_key_is_401():
    r = _client().post("/ask", json={"question": "hi"}, headers={"x-api-key": "nope"})
    assert r.status_code == 401 and "trace_id" in r.json()


def test_valid_request_returns_answer_and_trace_id():
    r = _client().post("/ask", json={"question": "how many vacation days"},
                       headers={"x-api-key": "good-key"})
    assert r.status_code == 200
    body = r.json()
    assert "1.75" in body["answer"] and body["sources"] == ["Time Off"]
    assert len(body["trace_id"]) == 16 and body["latency_ms"] >= 0


def test_empty_question_is_422():
    r = _client().post("/ask", json={"question": ""}, headers={"x-api-key": "good-key"})
    assert r.status_code == 422


def test_rate_limit_is_429_with_retry_after():
    limiter = TokenBucket(rate_per_sec=0.0, burst=2)     # 2 then nothing
    c = _client(limiter=limiter)
    h = {"x-api-key": "good-key"}
    assert c.post("/ask", json={"question": "q"}, headers=h).status_code == 200
    assert c.post("/ask", json={"question": "q"}, headers=h).status_code == 200
    r = c.post("/ask", json={"question": "q"}, headers=h)
    assert r.status_code == 429 and r.headers.get("retry-after") == "1"


def test_upstream_error_is_503_not_500():
    r = _client(FakeRAG(raiser=RuntimeError("bedrock exploded"))).post(
        "/ask", json={"question": "q"}, headers={"x-api-key": "good-key"})
    assert r.status_code == 503 and "trace_id" in r.json()
    assert "bedrock" not in r.json()["error"].lower()    # no leaking internals


def test_value_error_from_pipeline_is_400():
    r = _client(FakeRAG(raiser=ValueError("bad question"))).post(
        "/ask", json={"question": "q"}, headers={"x-api-key": "good-key"})
    assert r.status_code == 400 and r.json()["error"] == "bad question"
