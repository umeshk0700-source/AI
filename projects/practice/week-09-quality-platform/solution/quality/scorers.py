
"""Scorers: reference-based + an LLM-as-judge."""
from __future__ import annotations

from abc import ABC, abstractmethod

from llmlab import LLMClient


class Scorer(ABC):
    name: str

    @abstractmethod
    def score(self, output: str, case) -> float:   # -> 0.0 .. 1.0
        ...


class ExactMatch(Scorer):
    name = "exact_match"

    def score(self, output: str, case) -> float:
        return float(output.strip().lower() == case.reference.strip().lower())


class Contains(Scorer):
    name = "contains"

    def score(self, output: str, case) -> float:
        # TODO: fraction of case.must_contain substrings present in output (case-insensitive).
        #   if case.must_contain is empty -> 1.0.
        needles = case.must_contain
        if not needles:
            return 1.0
        o = output.lower()
        return sum(n.lower() in o for n in needles) / len(needles)


JUDGE_RUBRIC = (
    "You grade a CANDIDATE answer against a REFERENCE for a policy-assistant bot. "
    "Score correctness_and_faithfulness 1-5: 5 = says what the reference says and adds nothing "
    "unsupported; 3 = partially right or missing detail; 1 = wrong, or invents policy. "
    'Reply as JSON: {"score": <int 1-5>, "reason": "<one sentence>"}.'
)


class LLMJudge(Scorer):
    name = "judge"

    def __init__(self, judge_llm: LLMClient, rubric: str = JUDGE_RUBRIC):
        self.llm = judge_llm
        self.rubric = rubric

    def score(self, output: str, case) -> float:
        # TODO: call self.llm.chat with a user message containing REFERENCE and CANDIDATE,
        #   system=self.rubric, json_schema for {score:int, reason:str}, max_tokens=200.
        #   Parse resp.json["score"] (1-5) and return it normalised to 0..1 as (score-1)/4.
        #   On any parse error return 0.0.
        schema = {"type": "object",
                  "properties": {"score": {"type": "integer"}, "reason": {"type": "string"}},
                  "required": ["score", "reason"]}
        try:
            r = self.llm.chat(
                [{"role": "user",
                  "content": f"REFERENCE: {case.reference}\n\nCANDIDATE: {output}"}],
                system=self.rubric, json_schema=schema, max_tokens=200)
            s = int(r.json["score"])
            return max(0.0, min(1.0, (s - 1) / 4))
        except Exception:  # noqa: BLE001
            return 0.0
