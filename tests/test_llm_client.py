from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from app.idea_filter.llm_client import LLMClient, _normalize_result, _parse_json_payload
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
        client = LLMClient(settings=Settings(llm_provider="openai", openai_api_key=""))
        result = client.evaluate(title="Hard to edit social posts", text="takes too much time")

        self.assertIn("is_pain_signal", result)
        self.assertIn("pain_signal_score", result)
        self.assertIn("entrepreneur_opportunity_score", result)
        self.assertIn("reasoning_short", result)
        self.assertIn("evidence_snippet", result)
        self.assertIn("error", result)

    def test_parse_json_payload_handles_wrapped_json(self):
        payload = _parse_json_payload(
            "Some preface text {\"is_pain_signal\": true, \"pain_signal_score\": 8} trailing text"
        )
        self.assertIsNotNone(payload)
        self.assertTrue(payload["is_pain_signal"])
        self.assertEqual(payload["pain_signal_score"], 8)

    @patch("app.idea_filter.llm_client.requests.post")
    def test_ollama_success_path_returns_normalized_result(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "message": {
                "content": (
                    '{"is_pain_signal": true, "pain_signal_score": 9, '
                    '"entrepreneur_opportunity_score": 7, '
                    '"reasoning_short": "Clear repetitive pain", '
                    '"evidence_snippet": "takes hours every week"}'
                )
            }
        }
        mock_post.return_value = mock_response

        client = LLMClient(
            settings=Settings(
                llm_provider="ollama",
                ollama_base_url="http://localhost:11434",
                ollama_model="qwen3:14b",
            )
        )
        result = client.evaluate(title="Manual reporting is painful", text="I spend hours weekly")

        self.assertTrue(result["is_pain_signal"])
        self.assertEqual(result["pain_signal_score"], 9)
        self.assertEqual(result["entrepreneur_opportunity_score"], 7)
        self.assertEqual(result["error"], None)

    @patch("app.idea_filter.llm_client.requests.post")
    def test_ollama_invalid_json_returns_fallback(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"message": {"content": "not-json"}}
        mock_post.return_value = mock_response

        client = LLMClient(settings=Settings(llm_provider="ollama"))
        result = client.evaluate(title="Pain", text="text")

        self.assertFalse(result["is_pain_signal"])
        self.assertEqual(result["pain_signal_score"], 0)
        self.assertIn("valid JSON", result["error"])

    def test_unsupported_provider_returns_fallback(self):
        client = LLMClient(settings=Settings(llm_provider="unknown"))
        result = client.evaluate(title="Pain", text="text")

        self.assertFalse(result["is_pain_signal"])
        self.assertIn("Unsupported LLM_PROVIDER", result["error"])


if __name__ == "__main__":
    unittest.main()
