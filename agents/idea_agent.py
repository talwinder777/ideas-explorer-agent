from __future__ import annotations

import argparse
import json
from pathlib import Path

from config.settings import get_settings
from idea_agent_app.idea_filter_agent.pipeline import analyze_raw_items
from idea_agent_app.idea_scraper.reddit_scraper import collect_reddit_items
from idea_agent_app.models import RawItem


def run_idea_agent(
    reddit_subreddit: str = "SaaS",
    reddit_limit: int = 20,
    out_path: Path = Path("data/raw_items.json"),
) -> list[RawItem]:
    """Collect Reddit items and persist normalized JSON output (compat mode)."""
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


def run_idea_agent_full(
    reddit_subreddit: str = "SaaS",
    reddit_limit: int = 20,
    raw_out_path: Path = Path("data/raw_items.json"),
    analyzed_out_path: Path = Path("data/pain_candidates.json"),
    pain_signal_threshold: int = 6,
    include_all: bool = False,
) -> dict[str, object]:
    """Run full idea-agent flow: scrape Reddit -> run LLM pain filtering."""
    raw_items = run_idea_agent(
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Run idea agent (scrape + pain-filter)")
    parser.add_argument("--reddit-subreddit", type=str, default="SaaS", help="Subreddit for RSS fetch")
    parser.add_argument("--reddit-limit", type=int, default=20, help="Reddit RSS items to fetch")
    parser.add_argument(
        "--raw-out",
        type=Path,
        default=Path("data/raw_items.json"),
        help="Output JSON path for raw scraped items",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data/pain_candidates.json"),
        help="Output JSON path for analyzed pain candidates",
    )
    parser.add_argument(
        "--include-all",
        action="store_true",
        help="Include non-candidates as well (with analysis and is_candidate=false)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=None,
        help="Pain signal threshold override (default from PAIN_SIGNAL_THRESHOLD env)",
    )
    args = parser.parse_args()

    settings = get_settings()
    threshold = args.threshold if args.threshold is not None else settings.pain_signal_threshold
    result = run_idea_agent_full(
        reddit_subreddit=args.reddit_subreddit,
        reddit_limit=args.reddit_limit,
        raw_out_path=args.raw_out,
        analyzed_out_path=args.out,
        pain_signal_threshold=threshold,
        include_all=args.include_all,
    )
    print(
        f"Scraped {len(result['raw_items'])} items to {result['raw_out_path']}; "
        f"wrote {len(result['analyzed_items'])} analyzed rows to {result['analyzed_out_path']}"
    )


__all__ = ["run_idea_agent", "run_idea_agent_full", "main"]


if __name__ == "__main__":
    main()
