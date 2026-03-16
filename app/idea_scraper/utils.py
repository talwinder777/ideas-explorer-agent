"""Backward-compatible scraper utility exports.

Canonical location: `idea_agent_app.idea_scraper.utils`.
"""

from idea_agent_app.idea_scraper.utils import dedupe_by_url, safe_author, safe_published, safe_text

__all__ = ["safe_text", "safe_author", "safe_published", "dedupe_by_url"]
