"""Runtime configuration for the practice labs.

Loads a `.env` file (searched from the current directory upward, then
`projects/practice/.env`) and exposes typed settings. Never hard-code a key.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# Load .env: nearest one walking up, plus the shared practice/.env as a fallback.
_here = Path(__file__).resolve()
for _p in [Path.cwd(), *Path.cwd().parents]:
    if (_p / ".env").is_file():
        load_dotenv(_p / ".env")
        break
_practice_env = _here.parents[2] / ".env"  # .../projects/practice/.env
if _practice_env.is_file():
    load_dotenv(_practice_env, override=False)


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str | None = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    openai_api_key: str | None = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    voyage_api_key: str | None = field(default_factory=lambda: os.getenv("VOYAGE_API_KEY"))

    # Default models — small/cheap by design (see the per-lab budget).
    anthropic_model: str = field(default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"))
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    embed_model_openai: str = field(default_factory=lambda: os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small"))

    # Guard rails
    per_run_usd_cap: float = field(default_factory=lambda: float(os.getenv("LAB_USD_CAP", "0.25")))
    request_timeout_s: float = field(default_factory=lambda: float(os.getenv("LLM_TIMEOUT", "60")))
    max_retries: int = field(default_factory=lambda: int(os.getenv("LLM_MAX_RETRIES", "4")))

    def has(self, provider: str) -> bool:
        return {
            "anthropic": bool(self.anthropic_api_key),
            "openai": bool(self.openai_api_key),
            "voyage": bool(self.voyage_api_key),
        }.get(provider, False)


settings = Settings()
