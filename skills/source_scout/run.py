from __future__ import annotations

import argparse
import json
from pathlib import Path

from .collect import collect_raw_items


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Source Scout collection")
    parser.add_argument("--hn-limit", type=int, default=30, help="HN front-page items to fetch")
    parser.add_argument("--reddit-subreddit", type=str, default="SaaS", help="Subreddit for RSS fetch")
    parser.add_argument("--reddit-limit", type=int, default=20, help="Reddit RSS items to fetch")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data/raw_items.json"),
        help="Output JSON path",
    )
    args = parser.parse_args()

    items = collect_raw_items(
        hn_limit=args.hn_limit,
        reddit_subreddit=args.reddit_subreddit,
        reddit_limit=args.reddit_limit,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps([item.to_dict() for item in items], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote {len(items)} items to {args.out}")


if __name__ == "__main__":
    main()
