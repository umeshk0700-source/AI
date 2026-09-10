
"""Route a Requirement to prompt / RAG / fine-tune, with a cost model."""
from __future__ import annotations

from .schemas import Missing, Recommendation, Requirement

# illustrative blended $/1M tokens and per-approach overheads
PRICE_PER_MTOK = 4.0
FINETUNE_FIXED_USD = 4_000.0          # labelling + training + eval + hosting, one-off, / 12 mo
CONTEXT_OVERHEAD = {"prompt": 1.0, "rag": 0.15, "finetune": 0.03}  # fraction of corpus in ctx


class CostModel:
    @staticmethod
    def monthly(approach: str, req: Requirement) -> float:
        # TODO: monthly $ for `approach` given req.calls_per_month and
        #       req.knowledge_volume_tokens.
        #   per-call input tokens ~= knowledge_volume_tokens * CONTEXT_OVERHEAD[approach] + 400
        #   per-call output tokens ~= 250
        #   cost = calls * (in + out) / 1e6 * PRICE_PER_MTOK
        #   for "finetune", ADD FINETUNE_FIXED_USD / 12 (amortised).
        in_tok = req.knowledge_volume_tokens * CONTEXT_OVERHEAD[approach] + 400
        out_tok = 250
        variable = req.calls_per_month * (in_tok + out_tok) / 1e6 * PRICE_PER_MTOK
        return variable + (FINETUNE_FIXED_USD / 12 if approach == "finetune" else 0.0)


class CapabilityRouter:
    def recommend(self, req: Requirement) -> Recommendation:
        # TODO: apply the decision rules (Day 07), in order:
        #   1. missing is knowledge (or both) AND knowledge_changes  -> "rag"
        #      reason: facts that change belong in retrieval, not weights
        #   2. missing is knowledge (or both) AND volume too big for a prompt
        #      (knowledge_volume_tokens > 20_000)                    -> "rag"
        #   3. missing is behaviour AND have_labeled_data AND calls_per_month >= 100_000
        #                                                            -> "finetune"
        #   4. missing is behaviour AND latency_sensitive AND have_labeled_data -> "finetune"
        #      reason: bake the instructions into weights -> short prompt -> lower latency
        #   5. otherwise                                             -> "prompt"
        #   Fill projected_monthly_usd via CostModel.monthly(approach, req), and list the
        #   other two approaches in `alternatives`.
        m, reasons = req.missing, []
        if m in (Missing.knowledge, Missing.both) and req.knowledge_changes:
            approach = "rag"
            reasons.append("knowledge changes often -> keep it in retrieval, not frozen weights")
        elif m in (Missing.knowledge, Missing.both) and req.knowledge_volume_tokens > 20_000:
            approach = "rag"
            reasons.append("corpus too large to fit every prompt -> retrieve the relevant slice")
        elif m in (Missing.behaviour, Missing.both) and req.have_labeled_data and req.calls_per_month >= 100_000:
            approach = "finetune"
            reasons.append("consistent behaviour at high volume amortises the training cost")
        elif m in (Missing.behaviour, Missing.both) and req.latency_sensitive and req.have_labeled_data:
            approach = "finetune"
            reasons.append("baking instructions into weights shortens the prompt -> lower latency")
        else:
            approach = "prompt"
            reasons.append("start with prompt engineering; escalate only if it plateaus")
        alt = [a for a in ("prompt", "rag", "finetune") if a != approach]
        return Recommendation(
            approach=approach, reasons=reasons,
            projected_monthly_usd=round(CostModel.monthly(approach, req), 2),
            alternatives=alt,
        )
