from __future__ import annotations

import argparse
from pathlib import Path

from app.agent_manager import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run agentic idea scout pipeline")
    parser.add_argument("--reddit-subreddit", type=str, default="SaaS", help="Subreddit for RSS fetch")
    parser.add_argument("--reddit-limit", type=int, default=20, help="Reddit RSS items to fetch")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data/raw_items.json"),
        help="Output JSON path",
    )
    args = parser.parse_args()

    items = run_pipeline(
        reddit_subreddit=args.reddit_subreddit,
        reddit_limit=args.reddit_limit,
        out_path=args.out,
    )
    print(f"Wrote {len(items)} items to {args.out}")


if __name__ == "__main__":
    main()
