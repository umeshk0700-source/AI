import os
import pytest
from llmlab import get_client, default_cost, settings
from opsagent.agent import Agent
from opsagent.tools import default_registry

pytestmark = pytest.mark.live
_LIVE = os.getenv("LLM_LIVE") == "1"


@pytest.mark.skipif(not (_LIVE and settings.has("anthropic")), reason="live anthropic")
def test_agent_answers_from_runbook_without_filing():
    c0 = default_cost().total_usd
    run = Agent(get_client("anthropic"), default_registry(),
                approver=lambda n, a: False).run(
        "The payments API is returning 5xx errors. What are the rollback steps?")
    print(f"\nsteps={run.steps} aborted={run.aborted} cost=${default_cost().total_usd - c0:.5f}")
    for c in run.tool_calls:
        print("  ", c["name"], c["args"])
    print("  answer:", run.answer[:200])
    assert run.aborted is None
    assert run.steps <= 3
    assert any(c["name"] == "search_runbook" for c in run.tool_calls)
    assert not any(c["name"] == "create_incident" for c in run.tool_calls)
    assert "rollback" in run.answer.lower() or "roll back" in run.answer.lower()
    assert default_cost().total_usd - c0 < 0.03
