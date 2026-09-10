"""Real Claude few-shot on the handbook task = the baseline the router is judged against."""
import os
import pytest
from llmlab import get_client, settings
from adapt.schemas import Requirement, Missing
from adapt.router import CapabilityRouter, CostModel

pytestmark = pytest.mark.live

_LIVE = os.getenv("LLM_LIVE") == "1"

HANDBOOK = (
    "Cirrus handbook (excerpt): Full-time staff accrue 1.75 vacation days per month. "
    "Expenses of $75+ need a receipt within 14 days. Remote work is up to 3 days/week with "
    "manager approval. Referral bonus is $2,000 after the hire completes probation."
)
HOUSE_STYLE = 'Always answer as: "Per the handbook: <one sentence>."'


@pytest.mark.skipif(not (_LIVE and settings.has("anthropic")), reason="live anthropic")
def test_fewshot_baseline_and_router_agree():
    llm = get_client("anthropic")
    r = llm.chat(
        [{"role": "user", "content": f"{HANDBOOK}\n\nQuestion: How many vacation days do I accrue per month?"}],
        system=f"You answer Cirrus employee questions. {HOUSE_STYLE}", max_tokens=60)
    print("\nfew-shot answer:", r.text, "| cost $", round(r.cost_usd, 6))
    assert "1.75" in r.text and r.text.lower().startswith("per the handbook")

    # the requirement: house style, high volume, labelled data available, latency matters
    req = Requirement(description="handbook assistant house style", missing=Missing.behaviour,
                      knowledge_changes=False, knowledge_volume_tokens=1500,
                      calls_per_month=500_000, have_labeled_data=True, latency_sensitive=True)
    rec = CapabilityRouter().recommend(req)
    print("router:", rec.approach, rec.projected_monthly_usd, rec.reasons)
    assert rec.approach == "finetune"
    assert rec.projected_monthly_usd < CostModel.monthly("prompt", req)
