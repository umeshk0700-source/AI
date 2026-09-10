
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
        seen, dups = {}, []
        for i, r in enumerate(rows):
            h = hashlib.md5((r["prompt"] + "\x00" + r["completion"]).encode()).hexdigest()
            if h in seen:
                dups.append((seen[h], i))
            else:
                seen[h] = i
        return dups

    def leakage(self, train: list[dict], test: list[dict]) -> list:
        # TODO: return the ids (or indices) of test rows whose `prompt` also appears in train.
        train_prompts = {r["prompt"] for r in train}
        return [r.get("id", i) for i, r in enumerate(test) if r["prompt"] in train_prompts]

    def format_consistency(self, rows: list[dict]) -> float:
        # TODO: fraction of completions matching self.template (regex search).
        return sum(bool(re.search(self.template, r["completion"])) for r in rows) / max(1, len(rows))

    def run(self, train: list[dict], test: list[dict] | None = None) -> AuditReport:
        # TODO: assemble an AuditReport. ok is True iff no duplicates, no leakage,
        #       and format_consistency >= 0.95.
        dups = self.duplicates(train)
        leak = self.leakage(train, test) if test else []
        fmt = self.format_consistency(train)
        return AuditReport(n=len(train), duplicate_pairs=dups, leaked_ids=leak,
                           format_consistency=fmt,
                           ok=(not dups and not leak and fmt >= 0.95))
