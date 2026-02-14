from __future__ import annotations

from typing import Iterable

from .fetch_hn import fetch_hn_front_page
from .fetch_rss import fetch_reddit_rss
from .models import RawItem


def dedupe_by_url(items: Iterable[RawItem]) -> list[RawItem]:
    seen: set[str] = set()
    deduped: list[RawItem] = []
    for item in items:
        key = item.url.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def collect_raw_items(
    hn_limit: int = 30,
    reddit_subreddit: str = "SaaS",
    reddit_limit: int = 20,
) -> list[RawItem]:
    all_items: list[RawItem] = []

    # Best-effort source collection: continue if one source fails.
    try:
        all_items.extend(fetch_hn_front_page(limit=hn_limit))
    except Exception:
        pass

    try:
        all_items.extend(fetch_reddit_rss(subreddit=reddit_subreddit, limit=reddit_limit))
    except Exception:
        pass

    # Drop invalid items and dedupe.
    valid_items = [i for i in all_items if i.title.strip() and i.url.strip()]
    return dedupe_by_url(valid_items)
