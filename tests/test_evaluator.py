from __future__ import annotations

import unittest

from app.idea_filter.evaluator import evaluate_pain_signal


class TestEvaluator(unittest.TestCase):
    def test_evaluator_returns_expected_shape(self):
        result = evaluate_pain_signal("Editing content is too hard", "Need faster workflow")
        self.assertIn("is_pain_signal", result)
        self.assertIn("pain_signal_score", result)
        self.assertIn("reason", result)


if __name__ == "__main__":
    unittest.main()
