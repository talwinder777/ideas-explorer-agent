from __future__ import annotations

from typing import Optional

import feedparser

from .models import RawItem


def _safe_text(entry) -> str:
    if hasattr(entry, "summary") and entry.summary:
        return str(entry.summary).strip()
    if hasattr(entry, "description") and entry.description:
        return str(entry.description).strip()
    return ""


def _safe_author(entry) -> Optional[str]:
    if hasattr(entry, "author") and entry.author:
        return str(entry.author).strip()
    return None


def _safe_published(entry) -> Optional[str]:
    if hasattr(entry, "published") and entry.published:
        return str(entry.published).strip()
    if hasattr(entry, "updated") and entry.updated:
        return str(entry.updated).strip()
    return None


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
                text=_safe_text(e),
                author=_safe_author(e),
                created_at=_safe_published(e),
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
