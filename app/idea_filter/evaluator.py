from __future__ import annotations

from app.idea_filter.llm_client import LLMClient


def evaluate_pain_signal(title: str, text: str = "") -> dict:
    """Placeholder evaluator that will call the LLM client in future iterations."""
    client = LLMClient()
    return client.evaluate(f"{title}\n\n{text}".strip())
