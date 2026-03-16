from __future__ import annotations

import argparse
from pathlib import Path

from agents.idea_agent import run_idea_agent_full
from config.settings import get_settings


def main() -> None:
    parser = argparse.ArgumentParser(description="Run agentic idea scout pipeline (compat entrypoint)")
    parser.add_argument("--reddit-subreddit", type=str, default="SaaS", help="Subreddit for RSS fetch")
    parser.add_argument("--reddit-limit", type=int, default=20, help="Reddit RSS items to fetch")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data/raw_items.json"),
        help="Output JSON path for raw items (legacy behavior)",
    )
    parser.add_argument(
        "--analyzed-out",
        type=Path,
        default=Path("data/pain_candidates.json"),
        help="Output JSON path for analyzed items",
    )
    parser.add_argument(
        "--include-all",
        action="store_true",
        help="Include non-candidates in analyzed output",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=None,
        help="Pain signal threshold override",
    )
    args = parser.parse_args()

    settings = get_settings()
    threshold = args.threshold if args.threshold is not None else settings.pain_signal_threshold
    result = run_idea_agent_full(
        reddit_subreddit=args.reddit_subreddit,
        reddit_limit=args.reddit_limit,
        raw_out_path=args.out,
        analyzed_out_path=args.analyzed_out,
        pain_signal_threshold=threshold,
        include_all=args.include_all,
    )
    print(
        f"Wrote {len(result['raw_items'])} raw items to {args.out} and "
        f"{len(result['analyzed_items'])} analyzed rows to {args.analyzed_out}"
    )


if __name__ == "__main__":
    main()
