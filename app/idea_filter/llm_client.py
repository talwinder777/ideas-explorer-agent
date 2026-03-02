from __future__ import annotations


class LLMClient:
    """Placeholder LLM client wrapper for future pain-signal filtering."""

    def evaluate(self, text: str) -> dict:
        return {
            "is_pain_signal": False,
            "pain_signal_score": 0,
            "reason": "LLM filter not implemented yet",
            "text": text,
        }
