#!/usr/bin/env python3
"""Strip outputs + execution counts from a notebook. Stdlib only.

Usage:
    strip_notebook.py path/to/nb.ipynb [more.ipynb ...]   # in place
    strip_notebook.py --stdin < nb.ipynb                   # -> stdout   (git clean filter)

Practice notebooks can embed real API responses (which cost money to produce and
may contain fixture data) once run with LLM_LIVE=1. We never commit those outputs.
"""
import json
import sys


def strip(nb: dict) -> dict:
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
        cell.get("metadata", {}).pop("execution", None)
    md = nb.setdefault("metadata", {})
    md.pop("widgets", None)
    return nb


def main() -> int:
    args = sys.argv[1:]
    if args == ["--stdin"] or not args:
        data = sys.stdin.read()
        if not data.strip():
            return 0
        json.dump(strip(json.loads(data)), sys.stdout, indent=1, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    for path in args:
        with open(path, encoding="utf-8") as fh:
            nb = json.load(fh)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(strip(nb), fh, indent=1, ensure_ascii=False)
            fh.write("\n")
        print(f"stripped {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
