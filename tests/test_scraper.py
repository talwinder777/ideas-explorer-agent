from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.idea_scraper.reddit_scraper import collect_reddit_items


class TestRedditScraper(unittest.TestCase):
    @patch("app.idea_scraper.reddit_scraper.feedparser.parse")
    def test_collect_reddit_items_dedupes_and_filters_invalid(self, mock_parse):
        mock_parse.return_value = SimpleNamespace(
            entries=[
                SimpleNamespace(
                    title="Need better content editing",
                    link="https://reddit.com/post/1",
                    summary="Editing social posts is hard",
                    author="alice",
                    published="2026-03-01",
                ),
                # duplicate URL should be dropped
                SimpleNamespace(
                    title="Duplicate",
                    link="https://reddit.com/post/1",
                    summary="duplicate",
                    author="bob",
                    published="2026-03-01",
                ),
                # invalid (missing title) should be dropped
                SimpleNamespace(
                    title="",
                    link="https://reddit.com/post/2",
                    summary="invalid",
                    author="charlie",
                    published="2026-03-01",
                ),
            ]
        )

        items = collect_reddit_items(reddit_subreddit="SaaS", reddit_limit=10)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].url, "https://reddit.com/post/1")
        self.assertEqual(items[0].source_type, "rss")


if __name__ == "__main__":
    unittest.main()
