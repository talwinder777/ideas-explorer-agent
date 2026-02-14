from __future__ import annotations

from typing import Any

import requests

from .models import RawItem

HN_FRONT_PAGE_URL = "https://hn.algolia.com/api/v1/search"


def fetch_hn_front_page(limit: int = 30, timeout_seconds: int = 15) -> list[RawItem]:
    params = {
        "tags": "front_page",
        "hitsPerPage": max(1, min(limit, 100)),
        "page": 0
    }
    response = requests.get(HN_FRONT_PAGE_URL, params=params, timeout=timeout_seconds)
    response.raise_for_status()
    payload: dict[str, Any] = response.json()

    items: list[RawItem] = []
    for hit in payload.get("hits", []):
        title = (hit.get("title") or "").strip()
        url = (hit.get("url") or hit.get("story_url") or "").strip()
        if not title or not url:
            continue

        item = RawItem(
            source="hn",
            source_type="api",
            title=title,
            url=url,
            text=(hit.get("story_text") or hit.get("comment_text") or "").strip(),
            author=hit.get("author"),
            created_at=hit.get("created_at"),
            score=hit.get("points"),
            comments_count=hit.get("num_comments"),
            tags=["front_page", "tech", "startup", "painpoint_candidate"],
            extra={
                "object_id": hit.get("objectID"),
                "hn_item_url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}" if hit.get("objectID") else None,
            },
        )
        items.append(item)

    return items
