from __future__ import annotations

import json
from pathlib import Path

from idea_agent_app.idea_filter_agent.pipeline import analyze_raw_items
from idea_agent_app.idea_scraper.reddit_scraper import collect_reddit_items
from idea_agent_app.models import RawItem


def run_pipeline(
    reddit_subreddit: str = "SaaS",
    reddit_limit: int = 20,
    out_path: Path = Path("data/raw_items.json"),
) -> list[RawItem]:
    """Backward-compatible pipeline: scrape Reddit and persist raw items."""
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


def run_full_pipeline(
    reddit_subreddit: str = "SaaS",
    reddit_limit: int = 20,
    raw_out_path: Path = Path("data/raw_items.json"),
    analyzed_out_path: Path = Path("data/pain_candidates.json"),
    pain_signal_threshold: int = 6,
    include_all: bool = False,
) -> dict[str, object]:
    """Run scrape + pain-signal analysis and persist both outputs."""
    raw_items = run_pipeline(
        reddit_subreddit=reddit_subreddit,
        reddit_limit=reddit_limit,
        out_path=raw_out_path,
    )
    analyzed_items = analyze_raw_items(
        raw_items=[item.to_dict() for item in raw_items],
        pain_signal_threshold=pain_signal_threshold,
        include_all=include_all,
    )
    analyzed_out_path.parent.mkdir(parents=True, exist_ok=True)
    analyzed_out_path.write_text(
        json.dumps(analyzed_items, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return {
        "raw_items": raw_items,
        "analyzed_items": analyzed_items,
        "raw_out_path": raw_out_path,
        "analyzed_out_path": analyzed_out_path,
    }
