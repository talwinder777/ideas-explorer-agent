from __future__ import annotations

from typing import Iterable, Optional

from idea_agent_app.models import RawItem


def safe_text(entry) -> str:
    if hasattr(entry, "summary") and entry.summary:
        return str(entry.summary).strip()
    if hasattr(entry, "description") and entry.description:
        return str(entry.description).strip()
    return ""


def safe_author(entry) -> Optional[str]:
    if hasattr(entry, "author") and entry.author:
        return str(entry.author).strip()
    return None


def safe_published(entry) -> Optional[str]:
    if hasattr(entry, "published") and entry.published:
        return str(entry.published).strip()
    if hasattr(entry, "updated") and entry.updated:
        return str(entry.updated).strip()
    return None


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
