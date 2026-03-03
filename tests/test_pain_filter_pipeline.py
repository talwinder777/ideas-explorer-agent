from __future__ import annotations

import unittest
from unittest.mock import patch

from app.idea_filter.pipeline import analyze_raw_items


class TestPainFilterPipeline(unittest.TestCase):
    @patch("app.idea_filter.pipeline.evaluate_pain_signal")
    def test_analyze_raw_items_filters_candidates(self, mock_eval):
        mock_eval.side_effect = [
            {
                "is_pain_signal": True,
                "pain_signal_score": 8,
                "entrepreneur_opportunity_score": 7,
                "reasoning_short": "Clear recurring pain.",
                "evidence_snippet": "too hard",
                "error": None,
            },
            {
                "is_pain_signal": False,
                "pain_signal_score": 2,
                "entrepreneur_opportunity_score": 1,
                "reasoning_short": "No recurring pain.",
                "evidence_snippet": "",
                "error": None,
            },
        ]

        raw_items = [
            {"title": "Editing social content is hard", "text": "Painful workflow"},
            {"title": "Show and tell", "text": "Just sharing"},
        ]

        out = analyze_raw_items(raw_items=raw_items, pain_signal_threshold=6, include_all=False)

        self.assertEqual(len(out), 1)
        self.assertTrue(out[0]["is_candidate"])
        self.assertIn("analysis", out[0])

    @patch("app.idea_filter.pipeline.evaluate_pain_signal")
    def test_analyze_raw_items_include_all(self, mock_eval):
        mock_eval.return_value = {
            "is_pain_signal": False,
            "pain_signal_score": 1,
            "entrepreneur_opportunity_score": 1,
            "reasoning_short": "No",
            "evidence_snippet": "",
            "error": None,
        }

        raw_items = [{"title": "Low signal", "text": "n/a"}]
        out = analyze_raw_items(raw_items=raw_items, pain_signal_threshold=6, include_all=True)

        self.assertEqual(len(out), 1)
        self.assertFalse(out[0]["is_candidate"])


if __name__ == "__main__":
    unittest.main()
