
"""Run a lineup on the same task and pick a winner."""
from __future__ import annotations

import numpy as np

from llmlab import LLMClient, default_cost, price

from .extractor import Extractor
from .schemas import Extraction, ModelResult, SelectionMemo


def _norm(v):
    if isinstance(v, str):
        return v.strip().lower()
    if isinstance(v, float):
        return round(v, 2)
    return v


class ModelBench:
    def __init__(self, gold: list[dict]):
        """gold: [{"text": <invoice>, "fields": {vendor, invoice_number, total, currency,
        due_date, line_item_count}}]"""
        self.gold = gold

    def _score_one(self, got: Extraction, want: dict) -> tuple[float, bool]:
        # TODO: compare field-by-field (use _norm on both sides).
        #   return (fraction of fields correct, all_correct_bool)
        raise NotImplementedError("compare field-by-field (use _norm on both sides).")

    def run(self, models: dict[str, LLMClient]) -> list[ModelResult]:
        # TODO: for each (label, client): extract every gold invoice, score it, and build a
        #   ModelResult with field_accuracy (mean), exact_match_rate, mean & p95 latency,
        #   and cost_usd = the delta in default_cost().total_usd across that model's run.
        #   Keep per_invoice rows {idx, field_acc, exact, latency_s}.
        raise NotImplementedError("for each (label, client): extract every gold invoice, score it, and build a")

    def select(self, results: list[ModelResult], *, min_accuracy: float = 0.9) -> SelectionMemo:
        # TODO: recommend the CHEAPEST (by cost_usd) model whose field_accuracy >= min_accuracy.
        #   If none clear the bar, recommend the most accurate one and say so.
        #   table: rows {label, accuracy, cost_per_1k, p95_s}, sorted by accuracy desc.
        #   cost_per_1k = cost_usd / len(gold) * 1000
        #   runner_up = the next-best option by the same criterion.
        raise NotImplementedError("recommend the CHEAPEST (by cost_usd) model whose field_accuracy >= min_accuracy.")
