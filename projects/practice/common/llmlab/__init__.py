"""llmlab — shared toolkit for the practice labs.

Real provider clients (Anthropic + OpenAI) behind one interface, with retries,
cost accounting, tracing, embeddings, and pytest helpers.
"""
from .client import (
    AnthropicClient,
    LLMClient,
    LLMResponse,
    Message,
    OpenAIClient,
    ToolCall,
    ToolSpec,
    default_cost,
    get_client,
)
from .config import settings
from .cost import BudgetExceeded, CostTracker, PRICING, price
from .embeddings import Embedder, get_embedder
from .testing import FakeLLM, judge, live, load_jsonl
from .trace import Span, flatten, render, span, traced

__all__ = [
    "get_client", "LLMClient", "AnthropicClient", "OpenAIClient", "LLMResponse",
    "Message", "ToolSpec", "ToolCall", "default_cost",
    "settings", "CostTracker", "BudgetExceeded", "PRICING", "price",
    "get_embedder", "Embedder",
    "span", "traced", "flatten", "render", "Span",
    "live", "load_jsonl", "judge", "FakeLLM",
]
