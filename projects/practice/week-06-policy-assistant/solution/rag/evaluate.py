
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
    if answer.strip() == REFUSAL or not answer.strip():
        return 1.0
    sents = [s for s in re.split(r"(?<=[.!?])\s+", answer.strip()) if len(s.split()) >= 3]
    if not sents:
        return 1.0
    ctx_words = [set(re.findall(r"[a-z0-9]+", c.lower())) for c in context_texts]
    ok = 0
    for s in sents:
        w = set(re.findall(r"[a-z0-9]+", s.lower()))
        w = {x for x in w if len(x) > 2}
        if w and any(len(w & cw) / len(w) >= 0.6 for cw in ctx_words):
            ok += 1
    return ok / len(sents)


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
        from llmlab import default_cost
        cost0 = default_cost().total_usd
        rows, corr, faith = [], [], []
        for c in cases:
            a = self.p.answer(c["q"])
            ok = c["fact"].lower() in a.text.lower()
            f = faithfulness(a.text, [r.text for r in a.retrieved])
            corr.append(ok); faith.append(f)
            rows.append({"q": c["q"], "correct": ok, "faithful": round(f, 2),
                         "sources": a.sources})
        abst = []
        for q in oos:
            a = self.p.answer(q)
            abst.append(a.gated or a.text.strip() == REFUSAL)
        return RAGReport(
            n=len(cases),
            correctness=sum(corr) / len(corr) if corr else 0.0,
            faithfulness=sum(faith) / len(faith) if faith else 1.0,
            oos_abstention=sum(abst) / len(abst) if abst else 1.0,
            cost_usd=default_cost().total_usd - cost0, rows=rows,
        )
