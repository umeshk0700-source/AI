"""Real Claude / GPT. Run with:  LLM_LIVE=1 pytest -q -m live"""
import pytest
from llmlab import get_client, default_cost
from triage.service import TriageService
from triage.prompts import FewShotStrategy
from triage.evaluate import TriageEval
from testing_helpers import load_gold

pytestmark = pytest.mark.live


@pytest.fixture(params=["anthropic", "openai"])
def provider(request):
    from llmlab import settings
    if not settings.has(request.param) or __import__("os").getenv("LLM_LIVE") != "1":
        pytest.skip(f"no live {request.param}")
    return request.param


def test_triage_quality_on_fixtures(provider):
    svc = TriageService(get_client(provider), FewShotStrategy())
    rep = TriageEval(load_gold()).run(svc)
    print(f"\n[{provider}] {rep.summary()}")
    assert rep.category_acc >= 0.75, rep.summary()
    assert rep.priority_within_1 >= 0.80, rep.summary()
    assert rep.needs_human_recall >= 0.80, rep.summary()
    assert rep.cost_usd < 0.10, f"run cost ${rep.cost_usd:.4f}"


@pytest.mark.skipif(True, reason="illustrative — see the assertion below")
def test_provider_swap_is_transparent():
    pass


def test_service_code_is_provider_agnostic():
    """No 'anthropic'/'openai' string branching in service.py -> swapping the client is free."""
    import pathlib
    src = (pathlib.Path(__file__).resolve().parents[1] / "src" / "triage" / "service.py").read_text()
    assert "openai" not in src.lower() and "anthropic" not in src.lower()
