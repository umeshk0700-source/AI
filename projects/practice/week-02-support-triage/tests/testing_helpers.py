"""tiny shared test helper — load the fixture tickets with their gold labels."""
import pathlib
from llmlab import load_jsonl

_FIX = pathlib.Path(__file__).resolve().parents[1] / "fixtures" / "tickets.jsonl"


def load_gold() -> list[dict]:
    return load_jsonl(_FIX)
