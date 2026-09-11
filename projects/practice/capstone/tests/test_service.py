from fastapi.testclient import TestClient
from ragplatform import create_app, chunk_doc, VectorIndex, RagPlatform
from kb import DOCS
from helpers import kb_fake

def _client():
    plat = RagPlatform(DOCS, kb_fake())
    return TestClient(create_app(plat, api_key="secret", rate=100, burst=100))

def test_healthz():
    assert _client().get("/healthz").json() == {"ok": True}

def test_ask_requires_key():
    assert _client().post("/ask", json={"question": "refund window?"}).status_code == 401

def test_ask_ok():
    r = _client().post("/ask", json={"question": "how long for a refund?"},
                       headers={"x-api-key": "secret"})
    assert r.status_code == 200 and "30 days" in r.json()["answer"]

def test_rate_limit():
    plat = RagPlatform(DOCS, kb_fake())
    from fastapi.testclient import TestClient
    c = TestClient(create_app(plat, api_key="secret", rate=0.0, burst=1))
    h = {"x-api-key": "secret"}
    codes = [c.post("/ask", json={"question": "refund?"}, headers=h).status_code for _ in range(3)]
    assert 429 in codes
