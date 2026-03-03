from __future__ import annotations

import unittest

from app.idea_filter.llm_client import LLMClient, _normalize_result
from config.settings import Settings


class TestLLMClient(unittest.TestCase):
    def test_normalize_result_clamps_and_defaults(self):
        normalized = _normalize_result(
            {
                "is_pain_signal": True,
                "pain_signal_score": 99,
                "entrepreneur_opportunity_score": -3,
                "reasoning_short": "",
                "evidence_snippet": "Users keep complaining",
            }
        ).to_dict()

        self.assertTrue(normalized["is_pain_signal"])
        self.assertEqual(normalized["pain_signal_score"], 10)
        self.assertEqual(normalized["entrepreneur_opportunity_score"], 0)
        self.assertEqual(normalized["reasoning_short"], "No reasoning provided")
        self.assertEqual(normalized["evidence_snippet"], "Users keep complaining")

    def test_evaluate_without_key_returns_safe_fallback(self):
        client = LLMClient(settings=Settings(openai_api_key=""))
        result = client.evaluate(title="Hard to edit social posts", text="takes too much time")

        self.assertIn("is_pain_signal", result)
        self.assertIn("pain_signal_score", result)
        self.assertIn("entrepreneur_opportunity_score", result)
        self.assertIn("reasoning_short", result)
        self.assertIn("evidence_snippet", result)
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
