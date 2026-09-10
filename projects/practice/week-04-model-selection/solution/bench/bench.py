
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
        g = got.fields()
        hits = [_norm(g[k]) == _norm(want[k]) for k in want]
        return sum(hits) / len(hits), all(hits)

    def run(self, models: dict[str, LLMClient]) -> list[ModelResult]:
        # TODO: for each (label, client): extract every gold invoice, score it, and build a
        #   ModelResult with field_accuracy (mean), exact_match_rate, mean & p95 latency,
        #   and cost_usd = the delta in default_cost().total_usd across that model's run.
        #   Keep per_invoice rows {idx, field_acc, exact, latency_s}.
        results = []
        for label, client in models.items():
            ex = Extractor(client)
            accs, exacts, lats, rows = [], [], [], []
            cost0 = default_cost().total_usd
            for i, item in enumerate(self.gold):
                try:
                    got, dt = ex.extract(item["text"])
                    fa, allok = self._score_one(got, item["fields"])
                except Exception:  # noqa: BLE001
                    fa, allok, dt = 0.0, False, 0.0
                accs.append(fa); exacts.append(allok); lats.append(dt)
                rows.append({"idx": i, "field_acc": round(fa, 3), "exact": allok,
                             "latency_s": round(dt, 3)})
            results.append(ModelResult(
                label=label, field_accuracy=float(np.mean(accs)),
                exact_match_rate=float(np.mean(exacts)),
                mean_latency_s=float(np.mean(lats)),
                p95_latency_s=float(np.percentile(lats, 95)) if lats else 0.0,
                cost_usd=default_cost().total_usd - cost0, per_invoice=rows))
        return results

    def select(self, results: list[ModelResult], *, min_accuracy: float = 0.9) -> SelectionMemo:
        # TODO: recommend the CHEAPEST (by cost_usd) model whose field_accuracy >= min_accuracy.
        #   If none clear the bar, recommend the most accurate one and say so.
        #   table: rows {label, accuracy, cost_per_1k, p95_s}, sorted by accuracy desc.
        #   cost_per_1k = cost_usd / len(gold) * 1000
        #   runner_up = the next-best option by the same criterion.
        n = max(1, len(self.gold))
        clearing = sorted((r for r in results if r.field_accuracy >= min_accuracy),
                          key=lambda r: r.cost_usd)
        rationale = []
        if clearing:
            best = clearing[0]
            runner = clearing[1].label if len(clearing) > 1 else None
            rationale.append(f"{best.label} is the cheapest model clearing {min_accuracy:.0%} "
                             f"accuracy (got {best.field_accuracy:.1%})")
        else:
            best = max(results, key=lambda r: r.field_accuracy)
            others = sorted((r for r in results if r is not best),
                            key=lambda r: -r.field_accuracy)
            runner = others[0].label if others else None
            rationale.append(f"no model cleared {min_accuracy:.0%}; {best.label} is the most "
                             f"accurate at {best.field_accuracy:.1%} — do not ship without review")
        table = [{"label": r.label, "accuracy": round(r.field_accuracy, 3),
                  "cost_per_1k": round(r.cost_usd / n * 1000, 4),
                  "p95_s": round(r.p95_latency_s, 3)}
                 for r in sorted(results, key=lambda r: -r.field_accuracy)]
        return SelectionMemo(recommended=best.label, rationale=rationale,
                             min_accuracy=min_accuracy, table=table, runner_up=runner)
