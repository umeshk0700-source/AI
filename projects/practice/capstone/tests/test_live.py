"""End-to-end against real Claude + a real judge. Costs ~$0.10. `make live`."""
import pytest

pytestmark = pytest.mark.live

from llmlab import get_client
from llmlab.testing import live
from ragplatform import RagPlatform, EvalGate
from kb import DOCS, EVAL_CASES


@live("anthropic")
def test_platform_passes_its_own_eval_gate():
    llm = get_client("anthropic")
    plat = RagPlatform(DOCS, llm)
    gate = EvalGate(llm, tolerance=0.1)
    result = gate.check(lambda q: plat.ask(q), EVAL_CASES, baseline=None)
    assert result.mean >= 0.6
    # the out-of-scope case should be refused, not hallucinated
    assert plat.ask("Do you offer a free hardware trial?").strip().lower().startswith("i don't know")
