
"""Given."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EvalCase:
    id: str
    inputs: dict                 # passed to the system under test
    reference: str = ""          # gold answer (for reference-based scorers)
    must_contain: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


@dataclass
class CaseResult:
    id: str
    output: str
    scores: dict[str, float]     # scorer name -> 0..1
    tags: list[str]


@dataclass
class Report:
    n: int
    by_scorer: dict[str, float]              # mean score per scorer
    by_tag: dict[str, dict[str, float]]      # tag -> {scorer -> mean}
    rows: list[CaseResult] = field(default_factory=list)

    def metric(self, name: str) -> float:
        return self.by_scorer.get(name, 0.0)


@dataclass
class Verdict:
    passed: bool
    deltas: dict[str, float]
    blocking: list[str]
    notes: list[str] = field(default_factory=list)
