from __future__ import annotations

from typing import Optional

import feedparser

from app.idea_scraper.utils import dedupe_by_url, safe_author, safe_published, safe_text
from app.persistence.models import RawItem


def fetch_rss(
    feed_url: str,
    source_name: str,
    limit: int = 20,
    tags: Optional[list[str]] = None,
) -> list[RawItem]:
    fp = feedparser.parse(feed_url)
    entries = fp.entries[:limit]

    out: list[RawItem] = []
    for e in entries:
        title = (getattr(e, "title", "") or "").strip()
        url = (getattr(e, "link", "") or "").strip()
        if not title or not url:
            continue

        out.append(
            RawItem(
                source=source_name,
                source_type="rss",
                title=title,
                url=url,
                text=safe_text(e),
                author=safe_author(e),
                created_at=safe_published(e),
                score=None,
                comments_count=None,
                tags=tags or [],
                extra={},
            )
        )
    return out


def fetch_reddit_rss(subreddit: str = "SaaS", limit: int = 20) -> list[RawItem]:
    clean_subreddit = subreddit.strip().lstrip("r/")
    feed_url = f"https://www.reddit.com/r/{clean_subreddit}/new/.rss"
    return fetch_rss(
        feed_url=feed_url,
        source_name=f"reddit_rss_{clean_subreddit.lower()}",
        limit=limit,
        tags=["reddit", clean_subreddit.lower(), "painpoint_candidate"],
    )


def collect_reddit_items(
    reddit_subreddit: str = "SaaS",
    reddit_limit: int = 20,
) -> list[RawItem]:
    items = fetch_reddit_rss(subreddit=reddit_subreddit, limit=reddit_limit)
    valid_items = [i for i in items if i.title.strip() and i.url.strip()]
    return dedupe_by_url(valid_items)
