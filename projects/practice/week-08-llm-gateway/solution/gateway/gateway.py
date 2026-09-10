
"""The gateway: cache -> primary (via breaker) -> fallback, with per-tenant budgets."""
from __future__ import annotations

import json
from dataclasses import dataclass

from llmlab import CostTracker, LLMClient, LLMResponse, span

from .breaker import CircuitBreaker, CircuitOpen
from .cache import SemanticCache


@dataclass
class GatewayResponse:
    text: str
    served_by: str            # "cache" | primary provider | fallback provider
    cost_usd: float
    cached: bool


class Gateway:
    def __init__(self, primary: LLMClient, fallback: LLMClient, cache: SemanticCache,
                 *, breaker: CircuitBreaker | None = None):
        self.primary = primary
        self.fallback = fallback
        self.cache = cache
        self.breaker = breaker or CircuitBreaker()
        self._budgets: dict[str, CostTracker] = {}

    def set_budget(self, tenant: str, usd: float) -> None:
        self._budgets[tenant] = CostTracker(cap_usd=usd)

    def _prompt_key(self, messages, system) -> str:
        return json.dumps({"s": system, "m": messages}, sort_keys=True)

    def chat(self, tenant: str, messages: list[dict], *, system: str | None = None,
             max_tokens: int = 512) -> GatewayResponse:
        # TODO:
        #   key = self._prompt_key(messages, system)
        #   1. cached = self.cache.get(key)  -> if not None: return GatewayResponse(cached, "cache", 0.0, True)
        #   2. define _primary() -> self.primary.chat(messages, system=system, max_tokens=max_tokens)
        #      try resp = self.breaker.call(_primary); served = self.primary.provider
        #      except (CircuitOpen, Exception):
        #        resp = self.fallback.chat(...); served = self.fallback.provider
        #   3. charge the tenant: budget = self._budgets.get(tenant); if budget:
        #        budget.record(resp.model, resp.input_tokens, resp.output_tokens)   # may raise BudgetExceeded
        #   4. self.cache.put(key, resp.text); return GatewayResponse(resp.text, served, resp.cost_usd, False)
        #   Wrap in span("gateway.chat", tenant=tenant).
        with span("gateway.chat", kind="chain", tenant=tenant):
            key = self._prompt_key(messages, system)
            cached = self.cache.get(key)
            if cached is not None:
                return GatewayResponse(text=cached, served_by="cache", cost_usd=0.0, cached=True)

            def _primary():
                return self.primary.chat(messages, system=system, max_tokens=max_tokens)

            try:
                resp = self.breaker.call(_primary)
                served = self.primary.provider
            except Exception:  # noqa: BLE001  (CircuitOpen or a provider error)
                resp = self.fallback.chat(messages, system=system, max_tokens=max_tokens)
                served = self.fallback.provider

            budget = self._budgets.get(tenant)
            if budget is not None:
                budget.record(resp.model, resp.input_tokens, resp.output_tokens)

            self.cache.put(key, resp.text)
            return GatewayResponse(text=resp.text, served_by=served,
                                   cost_usd=resp.cost_usd, cached=False)
