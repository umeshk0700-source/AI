
"""Run an eval suite against a system under test."""
from __future__ import annotations

from collections import defaultdict

import numpy as np

from .schemas import CaseResult, Report, EvalCase


class EvalSuite:
    def __init__(self, cases: list[EvalCase], scorers: list):
        self.cases = cases
        self.scorers = scorers

    def run(self, system) -> Report:
        # `system` is any callable: system(**case.inputs) -> str
        # TODO:
        #   for each case: out = system(**case.inputs); score with every scorer;
        #     collect a CaseResult.
        #   by_scorer[name] = mean score across all cases
        #   by_tag[tag][name] = mean score across cases carrying `tag`
        rows: list[CaseResult] = []
        acc: dict[str, list[float]] = defaultdict(list)
        tag_acc: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
        for case in self.cases:
            out = system(**case.inputs)
            scores = {s.name: float(s.score(out, case)) for s in self.scorers}
            rows.append(CaseResult(id=case.id, output=out, scores=scores, tags=case.tags))
            for name, v in scores.items():
                acc[name].append(v)
                for t in case.tags:
                    tag_acc[t][name].append(v)
        return Report(
            n=len(rows),
            by_scorer={k: float(np.mean(v)) for k, v in acc.items()},
            by_tag={t: {k: float(np.mean(v)) for k, v in d.items()} for t, d in tag_acc.items()},
            rows=rows,
        )
