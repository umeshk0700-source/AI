import os
import pytest
from fastapi.testclient import TestClient
from llmlab import get_client, get_embedder, settings
from service.app import create_app

pytestmark = pytest.mark.live
_LIVE = os.getenv("LLM_LIVE") == "1"

HANDBOOK = {
  "Time Off": "Full-time employees accrue 1.75 vacation days per month, to a maximum of 30 days.",
  "Expenses": "Expenses of $75 or more require a receipt within 14 days. Meal per diem is $90 international.",
  "Security": "Passwords are rotated every 90 days and MFA is mandatory.",
}


@pytest.mark.skipif(not (_LIVE and settings.has("anthropic")), reason="live anthropic")
def test_app_with_real_rag():
    from rag_pipeline import RAGPipeline   # provided in tests/ for the live test
    p = RAGPipeline(get_embedder("openai" if settings.has("openai") else "local"),
                    get_client("anthropic"), k=3, min_score=0.28).ingest(HANDBOOK)
    c = TestClient(create_app(p, api_keys={"k": "t"}))
    r = c.post("/ask", json={"question": "how many vacation days do I accrue each month"},
               headers={"x-api-key": "k"})
    assert r.status_code == 200, r.text
    body = r.json()
    print("\n", body)
    assert "1.75" in body["answer"]
    assert body["sources"] and body["gated"] is False
    # out of scope -> gated
    r2 = c.post("/ask", json={"question": "what is the company's valuation"},
                headers={"x-api-key": "k"})
    assert r2.json()["gated"] is True
