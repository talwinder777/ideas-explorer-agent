from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.idea_filter.pipeline import analyze_raw_items
from config.settings import get_settings


def main() -> None:
    parser = argparse.ArgumentParser(description="Run LLM pain-signal filtering on raw items")
    parser.add_argument("--in", dest="in_path", type=Path, default=Path("data/raw_items.json"))
    parser.add_argument("--out", dest="out_path", type=Path, default=Path("data/pain_candidates.json"))
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

    if not args.in_path.exists():
        raise FileNotFoundError(f"Input file not found: {args.in_path}")

    raw_items = json.loads(args.in_path.read_text(encoding="utf-8"))
    settings = get_settings()
    threshold = args.threshold if args.threshold is not None else settings.pain_signal_threshold

    analyzed = analyze_raw_items(
        raw_items=raw_items,
        pain_signal_threshold=threshold,
        include_all=args.include_all,
    )

    args.out_path.parent.mkdir(parents=True, exist_ok=True)
    args.out_path.write_text(json.dumps(analyzed, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Analyzed {len(raw_items)} items; wrote {len(analyzed)} rows to {args.out_path}")
    print("LLM path used: app.idea_filter.evaluator -> app.idea_filter.llm_client")


if __name__ == "__main__":
    main()
