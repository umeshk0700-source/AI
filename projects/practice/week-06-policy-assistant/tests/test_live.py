import os
import pytest
from llmlab import get_client, get_embedder, settings
from rag.pipeline import RAGPipeline
from rag.evaluate import RAGEval

pytestmark = pytest.mark.live
_LIVE = os.getenv("LLM_LIVE") == "1"

HANDBOOK = {
  "Time Off": "Full-time employees accrue 1.75 vacation days per month, to a maximum balance of 30 days. Unused days above the cap are forfeited at year end. Sick leave is separate and uncapped; absences over three consecutive days need a doctor's note.",
  "Remote Work": "Employees may work remotely up to three days per week with manager approval. Fully remote arrangements require VP sign-off. The company provides a one-time $500 home office stipend.",
  "Expenses": "Expenses under $75 need no receipt. Expenses of $75 or more require an itemised receipt submitted within 14 days. The meal per diem is $60 domestic and $90 international. Alcohol is not reimbursable.",
  "Equipment": "New hires receive a laptop and a $200 accessories budget. Laptops are replaced every three years. Lost or stolen equipment must be reported to IT within 24 hours.",
  "Security": "Passwords must be at least 14 characters and are rotated every 90 days. Multi-factor authentication is mandatory. Laptops lock after five minutes of inactivity and use full-disk encryption.",
  "Referrals": "The employee referral bonus is $2,000, paid after the referred hire completes the 90-day probation period.",
}

CASES = [
  {"q": "how many vacation days do I accrue each month", "fact": "1.75"},
  {"q": "what's the maximum vacation balance", "fact": "30"},
  {"q": "how many days a week can I work from home", "fact": "three"},
  {"q": "do I need a receipt for a $40 taxi", "fact": "no receipt"},
  {"q": "what is the international meal per diem", "fact": "$90"},
  {"q": "how often are passwords rotated", "fact": "90 days"},
  {"q": "when must I report a stolen laptop", "fact": "24 hours"},
  {"q": "what is the referral bonus", "fact": "$2,000"},
]
OOS = ["what is the company's stock price", "who is the CEO", "can I bring my dog to the office"]


@pytest.mark.skipif(not (_LIVE and settings.has("anthropic")), reason="live anthropic")
def test_rag_quality():
    emb = get_embedder("openai" if settings.has("openai") else "local")
    p = RAGPipeline(emb, get_client("anthropic"), k=3, min_score=0.28).ingest(HANDBOOK)
    rep = RAGEval(p).run(CASES, OOS)
    print("\n" + str(rep.summary()))
    for r in rep.rows:
        print("  ", r)
    assert rep.correctness >= 0.7, rep.summary()
    assert rep.faithfulness >= 0.9, rep.summary()
    assert rep.oos_abstention == 1.0, rep.summary()
    assert rep.cost_usd < 0.05
