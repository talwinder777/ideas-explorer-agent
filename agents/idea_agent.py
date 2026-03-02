from __future__ import annotations

import json
from pathlib import Path

from app.idea_scraper.reddit_scraper import collect_reddit_items
from app.persistence.models import RawItem


def run_idea_agent(
    reddit_subreddit: str = "SaaS",
    reddit_limit: int = 20,
    out_path: Path = Path("data/raw_items.json"),
) -> list[RawItem]:
    """Collect Reddit items and persist normalized JSON output."""
    items = collect_reddit_items(
        reddit_subreddit=reddit_subreddit,
        reddit_limit=reddit_limit,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps([item.to_dict() for item in items], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return items
