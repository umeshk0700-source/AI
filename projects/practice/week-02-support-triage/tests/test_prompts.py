from triage.prompts import (
    ZeroShotStrategy, FewShotStrategy, ChainOfThoughtStrategy, BASE_SYSTEM,
)
from triage.schemas import Ticket

TICKET = Ticket(id="1", subject="Login broken", body="Cannot sign in since this morning.")


def test_zero_shot_shape():
    sysp, msgs = ZeroShotStrategy().build(TICKET)
    assert sysp == BASE_SYSTEM
    assert len(msgs) == 1 and msgs[0]["role"] == "user"
    assert "Login broken" in msgs[0]["content"]


def test_few_shot_includes_examples_then_ticket():
    sysp, msgs = FewShotStrategy().build(TICKET)
    assert msgs[-1]["role"] == "user" and "Login broken" in msgs[-1]["content"]
    roles = [m["role"] for m in msgs[:-1]]
    assert roles == ["user", "assistant"] * 3          # 3 worked examples, alternating
    assert any("account" in m["content"] for m in msgs if m["role"] == "assistant")


def test_cot_prompt_asks_for_reasoning():
    sysp, msgs = ChainOfThoughtStrategy().build(TICKET)
    assert "step by step" in sysp.lower()
    assert "priority" in sysp.lower() and "sentiment" in sysp.lower()
    assert len(msgs) == 1
