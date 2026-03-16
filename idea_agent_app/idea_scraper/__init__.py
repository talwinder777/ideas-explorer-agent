"""Idea scraper package (source collection layer)."""

from .reddit_scraper import collect_reddit_items, fetch_reddit_rss
from .utils import dedupe_by_url

__all__ = ["fetch_reddit_rss", "collect_reddit_items", "dedupe_by_url"]
