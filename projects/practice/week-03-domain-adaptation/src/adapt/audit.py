
"""Pre-flight data checks for a fine-tuning set (Day 09)."""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass


@dataclass
class AuditReport:
    n: int
    duplicate_pairs: list[tuple[int, int]]
    leaked_ids: list
    format_consistency: float
    ok: bool

    def summary(self) -> dict:
        return {"n": self.n, "duplicates": len(self.duplicate_pairs),
                "leaked": len(self.leaked_ids),
                "format_consistency": round(self.format_consistency, 3), "ok": self.ok}


class DatasetAudit:
    def __init__(self, template: str = r"Answer:\s"):
        self.template = template

    def duplicates(self, rows: list[dict]) -> list[tuple[int, int]]:
        # rows: [{"prompt":..., "completion":...}]  TODO: return (i, j) index pairs that are
        #       exact duplicates on (prompt, completion) (hash them; j > i).
        raise NotImplementedError("implement this")

    def leakage(self, train: list[dict], test: list[dict]) -> list:
        # TODO: return the ids (or indices) of test rows whose `prompt` also appears in train.
        raise NotImplementedError("return the ids (or indices) of test rows whose `prompt` also appears in train.")

    def format_consistency(self, rows: list[dict]) -> float:
        # TODO: fraction of completions matching self.template (regex search).
        raise NotImplementedError("fraction of completions matching self.template (regex search).")

    def run(self, train: list[dict], test: list[dict] | None = None) -> AuditReport:
        # TODO: assemble an AuditReport. ok is True iff no duplicates, no leakage,
        #       and format_consistency >= 0.95.
        raise NotImplementedError("assemble an AuditReport. ok is True iff no duplicates, no leakage,")
