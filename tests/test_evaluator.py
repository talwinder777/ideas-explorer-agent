from __future__ import annotations

import unittest
from unittest.mock import patch

from app.idea_filter.evaluator import evaluate_pain_signal


class TestEvaluator(unittest.TestCase):
    @patch("app.idea_filter.evaluator.LLMClient.evaluate")
    def test_evaluator_returns_expected_shape(self, mock_evaluate):
        mock_evaluate.return_value = {
            "is_pain_signal": True,
            "pain_signal_score": 8,
            "entrepreneur_opportunity_score": 7,
            "reasoning_short": "Users repeatedly mention manual editing burden.",
            "evidence_snippet": "editing content is too hard",
            "error": None,
        }

        result = evaluate_pain_signal("Editing content is too hard", "Need faster workflow")
        self.assertIn("is_pain_signal", result)
        self.assertIn("pain_signal_score", result)
        self.assertIn("entrepreneur_opportunity_score", result)
        self.assertIn("reasoning_short", result)
        self.assertIn("evidence_snippet", result)
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
