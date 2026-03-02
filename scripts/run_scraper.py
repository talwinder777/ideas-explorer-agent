from __future__ import annotations

import argparse
from pathlib import Path

from app.agent_manager import run_pipeline


def run() -> None:
    parser = argparse.ArgumentParser(description="Run reddit scraper pipeline")
    parser.add_argument("--reddit-subreddit", type=str, default="SaaS")
    parser.add_argument("--reddit-limit", type=int, default=20)
    parser.add_argument("--out", type=str, default="data/raw_items.json")
    args = parser.parse_args()

    items = run_pipeline(
        reddit_subreddit=args.reddit_subreddit,
        reddit_limit=args.reddit_limit,
        out_path=Path(args.out),
    )
    print(f"Wrote {len(items)} items to {args.out}")


if __name__ == "__main__":
    run()
