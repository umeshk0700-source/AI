
"""RAG evaluation: correctness, faithfulness, abstention (Day 18 / 25)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .schemas import REFUSAL


def faithfulness(answer: str, context_texts: list[str]) -> float:
    # every answer sentence should be textually supported by SOME context passage.
    # a cheap proxy: >= 60% of the sentence's content words appear in one passage.
    # TODO: return the fraction of answer sentences that are supported. A REFUSAL is
    #   trivially faithful (return 1.0). Empty answer -> 1.0.
    raise NotImplementedError("return the fraction of answer sentences that are supported. A REFUSAL is")


@dataclass
class RAGReport:
    n: int
    correctness: float
    faithfulness: float
    oos_abstention: float
    cost_usd: float
    rows: list[dict] = field(default_factory=list)

    def summary(self) -> dict:
        return {k: (round(v, 3) if isinstance(v, float) else v)
                for k, v in self.__dict__.items() if k != "rows"}


class RAGEval:
    def __init__(self, pipeline):
        self.p = pipeline

    def run(self, cases: list[dict], oos: list[str]) -> RAGReport:
        # cases: [{"q": str, "fact": <substring the answer must contain>}]
        # TODO:
        #   for each case: ans = self.p.answer(q); correct = fact.lower() in ans.text.lower();
        #     faithful = faithfulness(ans.text, [r.text for r in ans.retrieved]);
        #   for each oos question: abstained = (answer is gated OR text == REFUSAL)
        #   correctness = mean(correct); faithfulness = mean(faithful over cases);
        #   oos_abstention = mean(abstained); cost_usd = delta of llmlab.default_cost total.
        #   keep per-case rows.
        raise NotImplementedError("#   for each case: ans = self.p.answer(q); correct = fact.lower() in ans.text.lower();")
