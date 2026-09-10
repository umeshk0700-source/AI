"""Provider-neutral LLM client with retries, cost accounting and tracing.

    from llmlab import get_client
    llm = get_client("anthropic")                     # or "openai"
    r = llm.chat([{"role": "user", "content": "hi"}], system="Be terse.")
    print(r.text, r.usage, r.cost_usd)

Structured output:  llm.chat(..., json_schema=MySchema.model_json_schema())  -> r.json
Tool use:           llm.chat(..., tools=[ToolSpec(...)])                     -> r.tool_calls
Streaming:          for chunk in llm.stream(...): ...   then stream.final()
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Iterator

from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from .config import settings
from .cost import CostTracker, price
from .trace import span

# ------------------------------- data types ----------------------------------

Message = dict[str, Any]  # {"role": "user"|"assistant"|"tool"|"system", "content": ...}


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    parameters: dict  # JSON Schema for the arguments object


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict


@dataclass
class LLMResponse:
    text: str
    model: str
    provider: str
    stop_reason: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    tool_calls: list[ToolCall] = field(default_factory=list)
    raw: Any = None

    @property
    def usage(self) -> dict:
        return {"input_tokens": self.input_tokens, "output_tokens": self.output_tokens}

    @property
    def json(self) -> Any:
        """Parse `text` (or the first tool call's arguments) as JSON."""
        if self.tool_calls:
            return self.tool_calls[0].arguments
        import re
        m = re.search(r"[\[{].*[\]}]", self.text, re.DOTALL)
        return json.loads(m.group(0) if m else self.text)


# ------------------------------- retry policy -------------------------------

def _is_transient(exc: BaseException) -> bool:
    name = type(exc).__name__
    if name in {"RateLimitError", "APIConnectionError", "APITimeoutError", "InternalServerError"}:
        return True
    status = getattr(exc, "status_code", None) or getattr(getattr(exc, "response", None), "status_code", None)
    return isinstance(status, int) and status >= 500


def _retry():
    return retry(
        retry=retry_if_exception(_is_transient),
        wait=wait_exponential(multiplier=1, min=1, max=20),
        stop=stop_after_attempt(settings.max_retries),
        reraise=True,
    )


# ------------------------------- base client -------------------------------

class LLMClient:
    provider = "base"

    def __init__(self, model: str | None = None, cost: CostTracker | None = None):
        self.model = model
        self.cost = cost or _default_cost

    # public API ----------------------------------------------------------
    def chat(
        self,
        messages: list[Message],
        *,
        system: str | None = None,
        model: str | None = None,
        max_tokens: int = 1024,
        tools: list[ToolSpec] | None = None,
        temperature: float | None = None,
        json_schema: dict | None = None,
    ) -> LLMResponse:
        model = model or self.model or self._default_model()
        with span("llm.chat", kind="llm", provider=self.provider, model=model) as s:
            resp = self._chat(messages, system, model, max_tokens, tools, temperature, json_schema)
            resp.cost_usd = self.cost.record(model, resp.input_tokens, resp.output_tokens)
            s.outputs = {"stop_reason": resp.stop_reason, **resp.usage, "cost_usd": resp.cost_usd}
            return resp

    def stream(self, messages, *, system=None, model=None, max_tokens=1024, temperature=None):
        raise NotImplementedError

    # to override --------------------------------------------------------
    def _chat(self, messages, system, model, max_tokens, tools, temperature, json_schema) -> LLMResponse:
        raise NotImplementedError

    def _default_model(self) -> str:
        raise NotImplementedError


# ------------------------------- Anthropic ---------------------------------

class AnthropicClient(LLMClient):
    provider = "anthropic"

    def __init__(self, model: str | None = None, cost: CostTracker | None = None):
        super().__init__(model, cost)
        import anthropic
        if not settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set (see projects/practice/.env.example)")
        self._c = anthropic.Anthropic(timeout=settings.request_timeout_s, max_retries=0)

    def _default_model(self) -> str:
        return settings.anthropic_model

    @_retry()
    def _chat(self, messages, system, model, max_tokens, tools, temperature, json_schema):
        kwargs: dict = dict(model=model, max_tokens=max_tokens,
                            messages=[self._to_anthropic(m) for m in messages])
        if system:
            kwargs["system"] = system
        if temperature is not None:
            kwargs["temperature"] = temperature
        api_tools = [self._tool_schema(t) for t in (tools or [])]
        if json_schema is not None:
            api_tools.append({
                "name": "emit", "description": "Return the answer in this exact structure.",
                "input_schema": json_schema,
            })
            kwargs["tool_choice"] = {"type": "tool", "name": "emit"}
        if api_tools:
            kwargs["tools"] = api_tools
        r = self._c.messages.create(**kwargs)
        text = "".join(b.text for b in r.content if b.type == "text")
        calls = [ToolCall(id=b.id, name=b.name, arguments=dict(b.input))
                 for b in r.content if b.type == "tool_use"]
        return LLMResponse(
            text=text, model=model, provider=self.provider, stop_reason=r.stop_reason,
            input_tokens=r.usage.input_tokens, output_tokens=r.usage.output_tokens,
            cost_usd=0.0, tool_calls=calls, raw=r,
        )

    def stream(self, messages, *, system=None, model=None, max_tokens=1024, temperature=None):
        model = model or self.model or self._default_model()
        client = self._c
        cost = self.cost

        class _Stream:
            def __iter__(self_):
                kwargs = dict(model=model, max_tokens=max_tokens,
                              messages=[AnthropicClient._to_anthropic(m) for m in messages])
                if system:
                    kwargs["system"] = system
                with client.messages.stream(**kwargs) as st:
                    for t in st.text_stream:
                        yield t
                    self_._final = st.get_final_message()
                    cost.record(model, self_._final.usage.input_tokens,
                                self_._final.usage.output_tokens)

            def final(self_) -> LLMResponse:
                f = self_._final
                return LLMResponse(
                    text="".join(b.text for b in f.content if b.type == "text"),
                    model=model, provider="anthropic", stop_reason=f.stop_reason,
                    input_tokens=f.usage.input_tokens, output_tokens=f.usage.output_tokens,
                    cost_usd=price(model, f.usage.input_tokens, f.usage.output_tokens), raw=f)

        return _Stream()

    @staticmethod
    def _to_anthropic(m: Message) -> Message:
        if m["role"] == "tool":
            return {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": m["tool_call_id"],
                 "content": m["content"] if isinstance(m["content"], str) else json.dumps(m["content"])}]}
        return {"role": m["role"], "content": m["content"]}

    @staticmethod
    def _tool_schema(t: ToolSpec) -> dict:
        return {"name": t.name, "description": t.description, "input_schema": t.parameters}


# ------------------------------- OpenAI -----------------------------------

class OpenAIClient(LLMClient):
    provider = "openai"

    def __init__(self, model: str | None = None, cost: CostTracker | None = None):
        super().__init__(model, cost)
        from openai import OpenAI
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not set (see projects/practice/.env.example)")
        self._c = OpenAI(timeout=settings.request_timeout_s, max_retries=0)

    def _default_model(self) -> str:
        return settings.openai_model

    @_retry()
    def _chat(self, messages, system, model, max_tokens, tools, temperature, json_schema):
        msgs: list[Message] = []
        if system:
            msgs.append({"role": "system", "content": system})
        for m in messages:
            if m["role"] == "tool":
                msgs.append({"role": "tool", "tool_call_id": m["tool_call_id"],
                             "content": m["content"] if isinstance(m["content"], str) else json.dumps(m["content"])})
            else:
                msgs.append({"role": m["role"], "content": m["content"]})
        kwargs: dict = dict(model=model, max_tokens=max_tokens, messages=msgs)
        if temperature is not None:
            kwargs["temperature"] = temperature
        if tools:
            kwargs["tools"] = [{"type": "function",
                                "function": {"name": t.name, "description": t.description,
                                             "parameters": t.parameters}} for t in tools]
        if json_schema is not None:
            kwargs["response_format"] = {"type": "json_schema",
                                         "json_schema": {"name": "answer", "schema": json_schema,
                                                         "strict": False}}
        r = self._c.chat.completions.create(**kwargs)
        choice = r.choices[0]
        calls = [ToolCall(id=tc.id, name=tc.function.name, arguments=json.loads(tc.function.arguments))
                 for tc in (choice.message.tool_calls or [])]
        return LLMResponse(
            text=choice.message.content or "", model=model, provider=self.provider,
            stop_reason=choice.finish_reason,
            input_tokens=r.usage.prompt_tokens, output_tokens=r.usage.completion_tokens,
            cost_usd=0.0, tool_calls=calls, raw=r,
        )

    def stream(self, messages, *, system=None, model=None, max_tokens=1024, temperature=None):
        model = model or self.model or self._default_model()
        client, cost = self._c, self.cost
        msgs = ([{"role": "system", "content": system}] if system else []) + list(messages)

        class _Stream:
            _text = ""
            _usage = None

            def __iter__(self_):
                r = client.chat.completions.create(model=model, messages=msgs, max_tokens=max_tokens,
                                                   stream=True, stream_options={"include_usage": True})
                for ev in r:
                    if ev.usage:
                        self_._usage = ev.usage
                    if ev.choices and ev.choices[0].delta.content:
                        self_._text += ev.choices[0].delta.content
                        yield ev.choices[0].delta.content
                if self_._usage:
                    cost.record(model, self_._usage.prompt_tokens, self_._usage.completion_tokens)

            def final(self_) -> LLMResponse:
                u = self_._usage
                return LLMResponse(text=self_._text, model=model, provider="openai",
                                   stop_reason="stop",
                                   input_tokens=u.prompt_tokens if u else 0,
                                   output_tokens=u.completion_tokens if u else 0,
                                   cost_usd=price(model, u.prompt_tokens if u else 0,
                                                  u.completion_tokens if u else 0))

        return _Stream()


# ------------------------------- factory ---------------------------------

_default_cost = CostTracker(cap_usd=settings.per_run_usd_cap)


def get_client(provider: str = "anthropic", *, model: str | None = None,
               cost: CostTracker | None = None) -> LLMClient:
    provider = provider.lower()
    if provider == "anthropic":
        return AnthropicClient(model=model, cost=cost)
    if provider == "openai":
        return OpenAIClient(model=model, cost=cost)
    raise ValueError(f"unknown provider {provider!r} (use 'anthropic' or 'openai')")


def default_cost() -> CostTracker:
    return _default_cost
