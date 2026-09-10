
"""The agent loop with guards."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Callable

from llmlab import LLMClient, span

from .tools import ToolRegistry

SYSTEM = (
    "You are an on-call ops assistant. Use tools to look things up. Do NOT file a new incident "
    "unless the user explicitly asks you to. When you have the answer, state it plainly with "
    "the concrete steps."
)


@dataclass
class AgentRun:
    answer: str
    steps: int
    tool_calls: list[dict] = field(default_factory=list)
    aborted: str | None = None


class Agent:
    def __init__(self, llm: LLMClient, registry: ToolRegistry, *, max_steps: int = 6,
                 tool_budget: int = 5, max_repeats: int = 2,
                 approver: Callable[[str, dict], bool] | None = None):
        self.llm = llm
        self.registry = registry
        self.max_steps = max_steps
        self.tool_budget = tool_budget
        self.max_repeats = max_repeats
        self.approver = approver or (lambda name, args: False)   # deny destructive by default

    def _execute(self, name: str, args: dict) -> dict:
        # TODO: look up the tool in self.registry.
        #   - unknown tool -> {"error": "unknown tool <name>"}
        #   - destructive tool -> call self.approver(name, args); if it returns False,
        #     return {"error": "denied by policy", "_denied": True} WITHOUT running it.
        #   - otherwise call tool.fn(**args) and return its dict (catch exceptions ->
        #     {"error": repr(e)}).
        tool = self.registry.get(name)
        if tool is None:
            return {"error": f"unknown tool {name}"}
        if tool.destructive and not self.approver(name, args):
            return {"error": "denied by policy", "_denied": True}
        try:
            return tool.fn(**args)
        except Exception as e:  # noqa: BLE001
            return {"error": repr(e)}

    def run(self, goal: str) -> AgentRun:
        # TODO: the loop.
        #   messages = [{"role": "user", "content": goal}]
        #   for step in range(self.max_steps):
        #     resp = self.llm.chat(messages, system=SYSTEM, tools=self.registry.specs(), max_tokens=500)
        #     if not resp.tool_calls: return AgentRun(answer=resp.text, steps=step, ...)
        #     append the assistant turn as {"role": "assistant", "content": resp.text or "(tool call)"}
        #     for each call:
        #       - budget guard: total executed calls > self.tool_budget -> AgentRun(aborted="tool_budget")
        #       - repeat guard: same (name, sorted-json args) seen > self.max_repeats -> aborted="loop"
        #       - result = self._execute(name, args); record {step, name, args, result}
        #       - append {"role": "tool", "tool_call_id": call.id, "content": result}
        #   return AgentRun(answer="...max steps...", aborted="max_steps")
        #   Wrap the whole run in span("agent.run", goal=goal).
        with span("agent.run", kind="chain", goal=goal):
            messages = [{"role": "user", "content": goal}]
            executed, seen, calls = 0, {}, []
            for step in range(self.max_steps):
                resp = self.llm.chat(messages, system=SYSTEM, tools=self.registry.specs(),
                                     max_tokens=500)
                if not resp.tool_calls:
                    return AgentRun(answer=resp.text.strip(), steps=step, tool_calls=calls)
                messages.append({"role": "assistant", "content": resp.text or "(tool call)"})
                for call in resp.tool_calls:
                    executed += 1
                    if executed > self.tool_budget:
                        return AgentRun(answer="tool budget exhausted", steps=step,
                                        tool_calls=calls, aborted="tool_budget")
                    key = (call.name, json.dumps(call.arguments, sort_keys=True))
                    seen[key] = seen.get(key, 0) + 1
                    if seen[key] > self.max_repeats:
                        return AgentRun(answer=f"stuck repeating {call.name}", steps=step,
                                        tool_calls=calls, aborted="loop")
                    result = self._execute(call.name, call.arguments)
                    calls.append({"step": step, "name": call.name, "args": call.arguments,
                                  "result": result})
                    messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
            return AgentRun(answer="reached max steps without a final answer",
                            steps=self.max_steps, tool_calls=calls, aborted="max_steps")
