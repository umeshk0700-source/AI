
"""Given — recursive character splitter (Day 17)."""
from __future__ import annotations

import re


def recursive_split(text: str, max_chars: int = 500,
                    seps: tuple[str, ...] = ("\n## ", "\n\n", ". ", " ")) -> list[str]:
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    sep = next((s for s in seps if s in text), None)
    if sep is None:
        return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
    out, cur = [], ""
    for part in text.split(sep):
        piece = (sep + part) if (cur or out) else part
        if len(cur) + len(piece) <= max_chars:
            cur += piece
        else:
            if cur.strip():
                out.append(cur.strip())
            cur = piece if len(piece) <= max_chars else ""
            if len(piece) > max_chars:
                out += recursive_split(piece, max_chars, seps)
    if cur.strip():
        out.append(cur.strip())
    return [re.sub(r"\s+", " ", c).strip() for c in out if c.strip()]
