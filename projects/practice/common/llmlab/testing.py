"""pytest helpers shared by every lab's test suite.

- `live(provider)`  : a decorator/marker that skips a test unless the provider's
  key is set AND `LLM_LIVE=1` (so unit tests never spend money by accident).
- `load_jsonl(path)`: read a fixtures file.
- `judge(...)`      : LLM-as-judge scoring for the eval labs.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from .config import settings


def live(provider: str = "anthropic"):
    """Use as: `@live("openai")` on a test function, or `pytestmark = live()`."""
    enabled = os.getenv("LLM_LIVE") == "1" and settings.has(provider)
    reason = (f"live {provider} test — set LLM_LIVE=1 and {provider.upper()}_API_KEY to run"
              if not enabled else "")
    return pytest.mark.skipif(not enabled, reason=reason)


def load_jsonl(path: str | Path) -> list[dict]:
    p = Path(path)
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


class FakeLLM:
    """A test double with the LLMClient surface. Give it a `responder(messages, **kw) -> str`
    (returning the model's text, JSON or otherwise) so unit tests can exercise the
    non-LLM logic of a service without spending money."""

    provider = "fake"

    def __init__(self, responder=None, *, text: str = "ok"):
        self._responder = responder or (lambda messages, **kw: text)
        self.calls: list[dict] = []

    def chat(self, messages, *, system=None, model="fake", max_tokens=1024,
             tools=None, temperature=None, json_schema=None):
        from .client import LLMResponse, ToolCall
        self.calls.append({"messages": messages, "system": system, "tools": tools,
                           "json_schema": json_schema})
        out = self._responder(messages, system=system, json_schema=json_schema, tools=tools)
        # a responder may return: str | dict (json) | ("tool", name, args) | [("tool", ...), ...]
        if isinstance(out, tuple) and out and out[0] == "tool":
            out = [out]
        if isinstance(out, list) and out and isinstance(out[0], tuple):
            calls = [ToolCall(id=f"call_{i}", name=n, arguments=a)
                     for i, (_, n, a) in enumerate(out)]
            return LLMResponse(text="", model=model, provider="fake", stop_reason="tool_use",
                               input_tokens=10, output_tokens=10, cost_usd=0.0, tool_calls=calls)
        return LLMResponse(text=out if isinstance(out, str) else json.dumps(out),
                           model=model, provider="fake", stop_reason="end_turn",
                           input_tokens=10, output_tokens=10, cost_usd=0.0)


JUDGE_SYSTEM = (
    "You are a strict evaluator. Given a QUESTION, a REFERENCE answer, and a CANDIDATE "
    "answer, score the candidate 1-5 for correctness against the reference (5 = fully "
    'correct, 1 = wrong or missing). Reply as JSON: {"score": <int>, "reason": "<short>"}.'
)


def judge(llm, question: str, reference: str, candidate: str) -> dict:
    """Return {'score': 1-5, 'reason': str} from an LLM judge."""
    r = llm.chat(
        [{"role": "user",
          "content": f"QUESTION: {question}\nREFERENCE: {reference}\nCANDIDATE: {candidate}"}],
        system=JUDGE_SYSTEM,
        json_schema={"type": "object",
                     "properties": {"score": {"type": "integer"}, "reason": {"type": "string"}},
                     "required": ["score", "reason"]},
        max_tokens=200,
    )
    return r.json
