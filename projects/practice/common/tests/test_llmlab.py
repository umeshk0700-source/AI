"""Tests for the shared toolkit itself. Offline unit tests always run; the
`live` ones ping each provider once (cheap) when LLM_LIVE=1 + keys are set."""
import pytest

from llmlab import CostTracker, ToolSpec, get_client, live, span, flatten
from llmlab.client import _is_transient
from llmlab.cost import BudgetExceeded, price


# --------------------------- offline unit tests ---------------------------

def test_pricing_math():
    assert price("gpt-4o-mini", 1_000_000, 0) == pytest.approx(0.15)
    assert price("claude-haiku-4-5", 0, 1_000_000) == pytest.approx(5.00)
    assert price("unknown-model", 999, 999) == 0.0


def test_cost_tracker_accumulates_and_caps():
    ct = CostTracker(cap_usd=0.001)
    ct.record("gpt-4o-mini", 1000, 200)
    assert ct.calls == 1 and ct.total_usd > 0
    with pytest.raises(BudgetExceeded):
        ct.record("claude-opus-4-5", 500_000, 500_000)


def test_transient_classification():
    class RateLimitError(Exception):
        pass

    class BadRequestError(Exception):
        status_code = 400

    class ServerErr(Exception):
        status_code = 503

    assert _is_transient(RateLimitError())
    assert _is_transient(ServerErr())
    assert not _is_transient(BadRequestError())
    assert not _is_transient(ValueError("nope"))


def test_anthropic_message_translation():
    from llmlab.client import AnthropicClient
    tool_msg = {"role": "tool", "tool_call_id": "t1", "content": {"ok": True}}
    out = AnthropicClient._to_anthropic(tool_msg)
    assert out["role"] == "user"
    assert out["content"][0]["type"] == "tool_result"
    assert out["content"][0]["tool_use_id"] == "t1"


def test_tool_spec_and_response_json():
    from llmlab.client import LLMResponse, ToolCall
    r = LLMResponse(text="", model="m", provider="p", stop_reason="tool_use",
                    input_tokens=1, output_tokens=1, cost_usd=0.0,
                    tool_calls=[ToolCall("id", "emit", {"a": 1})])
    assert r.json == {"a": 1}
    r2 = LLMResponse(text='noise {"b": 2} tail', model="m", provider="p", stop_reason="end_turn",
                     input_tokens=1, output_tokens=1, cost_usd=0.0)
    assert r2.json == {"b": 2}


def test_trace_nesting():
    with span("root") as r:
        with span("child_a") as a:
            a.outputs = {"x": 1}
        with span("child_b"):
            with span("grandchild"):
                pass
    rows = flatten(r)
    assert [x["name"] for x in rows] == ["root", "child_a", "child_b", "grandchild"]
    assert rows[3]["parent"] == rows[2]["span_id"]


def test_get_client_rejects_unknown():
    with pytest.raises(ValueError):
        get_client("cohere")


# ------------------------------ live tests -------------------------------

@live("anthropic")
def test_anthropic_ping():
    llm = get_client("anthropic")
    r = llm.chat([{"role": "user", "content": "Reply with exactly: pong"}], max_tokens=10)
    assert "pong" in r.text.lower()
    assert r.input_tokens > 0 and r.cost_usd > 0


@live("openai")
def test_openai_ping():
    llm = get_client("openai")
    r = llm.chat([{"role": "user", "content": "Reply with exactly: pong"}], max_tokens=10)
    assert "pong" in r.text.lower()
    assert r.output_tokens > 0


@live("anthropic")
def test_structured_output_anthropic():
    llm = get_client("anthropic")
    schema = {"type": "object", "properties": {"sentiment": {"type": "string"}},
              "required": ["sentiment"]}
    r = llm.chat([{"role": "user", "content": "Classify: 'I love this'"}],
                 json_schema=schema, max_tokens=100)
    assert r.json["sentiment"] in {"positive", "negative", "neutral", "mixed"}
