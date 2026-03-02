from __future__ import annotations

from pathlib import Path

from agents.idea_agent import run_idea_agent
from app.persistence.models import RawItem


def run_pipeline(
    reddit_subreddit: str = "SaaS",
    reddit_limit: int = 20,
    out_path: Path = Path("data/raw_items.json"),
) -> list[RawItem]:
    """Run current pipeline (Reddit scout only) and persist raw items."""
    return run_idea_agent(
        reddit_subreddit=reddit_subreddit,
        reddit_limit=reddit_limit,
        out_path=out_path,
    )
