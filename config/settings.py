from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    reddit_subreddit: str = "SaaS"
    reddit_limit: int = 20
    raw_items_path: Path = Path("data/raw_items.json")


def get_settings() -> Settings:
    return Settings()
