
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
        raise NotImplementedError("#   for each case: out = system(**case.inputs); score with every scorer;")
