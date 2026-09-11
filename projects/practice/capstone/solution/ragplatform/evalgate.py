"""EvalGate: run cases through the platform, judge them, compare to a baseline."""
from __future__ import annotations

from dataclasses import dataclass

from llmlab import judge


@dataclass
class GateResult:
    ok: bool
    mean: float
    baseline_mean: float
    per_case: dict


class EvalGate:
    def __init__(self, judge_llm, *, tolerance: float = 0.05, pass_mark: float = 0.6):
        self.judge_llm, self.tolerance, self.pass_mark = judge_llm, tolerance, pass_mark

    def score(self, answer_fn, cases) -> dict:
        out = {}
        for question, reference in cases:
            cand = answer_fn(question)
            out[question] = judge(self.judge_llm, question, reference, cand)["score"]
        return out

    def check(self, answer_fn, cases, baseline: dict | None) -> GateResult:
        scores = self.score(answer_fn, cases)
        mean = sum(scores.values()) / len(scores)
        if baseline is None:
            return GateResult(True, mean, mean, scores)
        base_mean = sum(baseline.values()) / len(baseline)
        regressed = any(baseline.get(q, 0) >= self.pass_mark > s for q, s in scores.items())
        ok = mean >= base_mean - self.tolerance and not regressed
        return GateResult(ok, mean, base_mean, scores)
