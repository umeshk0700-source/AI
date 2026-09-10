
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
        return {
            "category_ok": result.category.value == gold["category"],
            "priority_within_1": abs(_PRIO_RANK[result.priority.value]
                                     - _PRIO_RANK[gold["priority"]]) <= 1,
            "needs_human_ok": result.needs_human == gold["needs_human"],
            "team_ok": result.route_to_team == gold["team"],
        }

    def run(self, service: TriageService) -> Report:
        # TODO: for each gold item build a Ticket, time service.triage(), score it.
        #   category_acc        = mean(category_ok)
        #   priority_within_1   = mean(priority_within_1)
        #   needs_human_recall  = TP / (TP + FN) over items whose gold needs_human is True
        #   team_acc            = mean(team_ok)
        #   cost_usd            = default_cost().total_usd delta across the run
        #   Keep per-item rows (id + the score dict + latency).
        rows, lat = [], []
        cost0 = default_cost().total_usd
        tp = fn = 0
        for g in self.gold:
            t = Ticket(id=g["id"], subject=g["subject"], body=g["body"],
                       customer_tier=g.get("customer_tier", "free"))
            t0 = time.perf_counter()
            r = service.triage(t)
            dt = time.perf_counter() - t0
            s = self.score_one(r, g["gold"])
            if g["gold"]["needs_human"]:
                tp += int(s["needs_human_ok"])
                fn += int(not s["needs_human_ok"])
            rows.append({"id": g["id"], **s, "latency_s": round(dt, 3)})
            lat.append(dt)
        mean = lambda k: sum(row[k] for row in rows) / len(rows)
        return Report(
            n=len(rows),
            category_acc=mean("category_ok"),
            priority_within_1=mean("priority_within_1"),
            needs_human_recall=(tp / (tp + fn)) if (tp + fn) else 1.0,
            team_acc=mean("team_ok"),
            mean_latency_s=sum(lat) / len(lat),
            cost_usd=default_cost().total_usd - cost0,
            rows=rows,
        )
