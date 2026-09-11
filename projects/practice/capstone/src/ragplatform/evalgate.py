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
        # TODO: for each (question, reference) in cases:
        #   cand = answer_fn(question); s = judge(self.judge_llm, question, reference, cand)["score"]
        # return {question: s}
        raise NotImplementedError

    def check(self, answer_fn, cases, baseline: dict | None) -> GateResult:
        # TODO: scores = self.score(answer_fn, cases); mean = avg
        #   if baseline is None -> ok=True (this run *is* the baseline)
        #   else ok = mean >= baseline_mean - self.tolerance AND no case drops
        #        from >= pass_mark to < pass_mark
        raise NotImplementedError
