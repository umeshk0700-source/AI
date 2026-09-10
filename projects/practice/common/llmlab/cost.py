"""Token pricing and per-run cost accounting.

Prices are USD per 1M tokens, checked against public pricing pages at time of
writing. Update `PRICING` if a lab's numbers look off — the exact figures matter
less than the shape of the reasoning.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock

# provider/model -> (input $/1M, output $/1M)
PRICING: dict[str, tuple[float, float]] = {
    # Anthropic
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-sonnet-4-5": (3.00, 15.00),
    "claude-opus-4-5": (5.00, 25.00),
    "claude-3-5-haiku-latest": (0.80, 4.00),
    # OpenAI
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4o": (2.50, 10.00),
    "gpt-4.1-mini": (0.40, 1.60),
    # Embeddings (output price unused)
    "text-embedding-3-small": (0.02, 0.0),
    "text-embedding-3-large": (0.13, 0.0),
    "voyage-3": (0.06, 0.0),
}


def price(model: str, input_tokens: int, output_tokens: int = 0) -> float:
    pin, pout = PRICING.get(model, (0.0, 0.0))
    return (input_tokens * pin + output_tokens * pout) / 1_000_000


class BudgetExceeded(RuntimeError):
    """Raised when accumulated spend crosses the configured cap."""


@dataclass
class CostTracker:
    """Accumulates spend across calls; optionally trips a hard cap."""

    cap_usd: float | None = None
    total_usd: float = 0.0
    calls: int = 0
    by_model: dict[str, float] = field(default_factory=dict)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def record(self, model: str, input_tokens: int, output_tokens: int = 0) -> float:
        c = price(model, input_tokens, output_tokens)
        with self._lock:
            self.total_usd += c
            self.calls += 1
            self.by_model[model] = self.by_model.get(model, 0.0) + c
            if self.cap_usd is not None and self.total_usd > self.cap_usd:
                raise BudgetExceeded(
                    f"spend ${self.total_usd:.4f} exceeded cap ${self.cap_usd:.4f} "
                    f"after {self.calls} calls"
                )
        return c

    def summary(self) -> dict:
        return {
            "total_usd": round(self.total_usd, 6),
            "calls": self.calls,
            "by_model": {k: round(v, 6) for k, v in self.by_model.items()},
        }
