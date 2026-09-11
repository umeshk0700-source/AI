"""A small tool-using agent: it can search the KB (RAG) and do arithmetic."""
from __future__ import annotations

from llmlab import span

from .rag import RAGPipeline


class Agent:
    def __init__(self, rag: RAGPipeline, llm, *, max_steps: int = 4):
        self.rag, self.llm, self.max_steps = rag, llm, max_steps

    def _tools(self):
        return [
            {"name": "kb_search", "description": "Look up an answer in the knowledge base.",
             "input_schema": {"type": "object", "properties": {"q": {"type": "string"}},
                              "required": ["q"]}},
            {"name": "calc", "description": "Evaluate a simple arithmetic expression.",
             "input_schema": {"type": "object", "properties": {"expr": {"type": "string"}},
                              "required": ["expr"]}},
        ]

    def _run_tool(self, name, args):
        if name == "kb_search":
            return self.rag.answer(args["q"]).text
        if name == "calc":
            return str(eval(args["expr"], {"__builtins__": {}}, {}))   # guarded: no builtins
        return f"unknown tool {name}"

    def run(self, task: str) -> str:
        # TODO (wrap in `with span("agent.run"):`):
        #   messages = [{"role": "user", "content": task}]
        #   loop up to self.max_steps:
        #     resp = self.llm.chat(messages, tools=self._tools())
        #     if not resp.tool_calls: return resp.text
        #     for tc in resp.tool_calls: obs = self._run_tool(tc.name, tc.arguments)
        #       append the tool call + a {"role": "tool", ...} observation to messages
        #   return "step budget exhausted"
        raise NotImplementedError
