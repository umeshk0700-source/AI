
"""Offline-style evaluation of the triage service against labelled tickets."""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from llmlab import default_cost

from .schemas import Priority, Ticket
from .service import TriageService

_PRIO_RANK = {"P1": 3, "P2": 2, "P3": 1, "P4": 0}


@dataclass
class Report:
    n: int
    category_acc: float
    priority_within_1: float
    needs_human_recall: float
    team_acc: float
    mean_latency_s: float
    cost_usd: float
    rows: list[dict] = field(default_factory=list)

    def summary(self) -> dict:
        return {k: (round(v, 3) if isinstance(v, float) else v)
                for k, v in self.__dict__.items() if k != "rows"}


class TriageEval:
    def __init__(self, gold: list[dict]):
        """gold: dicts with keys id, subject, body, customer_tier and a `gold` sub-dict
        {category, priority, sentiment, needs_human, team}."""
        self.gold = gold

    def score_one(self, result, gold: dict) -> dict:
        # TODO: return a dict with booleans:
        #   category_ok      : result.category.value == gold["category"]
        #   priority_within_1: abs(rank(result.priority) - rank(gold priority)) <= 1
        #   needs_human_ok   : result.needs_human == gold["needs_human"]
        #   team_ok          : result.route_to_team == gold["team"]
        #   (use _PRIO_RANK for the priority ranks)
        raise NotImplementedError("return a dict with booleans:")

    def run(self, service: TriageService) -> Report:
        # TODO: for each gold item build a Ticket, time service.triage(), score it.
        #   category_acc        = mean(category_ok)
        #   priority_within_1   = mean(priority_within_1)
        #   needs_human_recall  = TP / (TP + FN) over items whose gold needs_human is True
        #   team_acc            = mean(team_ok)
        #   cost_usd            = default_cost().total_usd delta across the run
        #   Keep per-item rows (id + the score dict + latency).
        raise NotImplementedError("for each gold item build a Ticket, time service.triage(), score it.")
