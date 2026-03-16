from __future__ import annotations

from llm_clients.llm_client import LLMClient


def evaluate_pain_signal(title: str, text: str = "") -> dict:
    """Evaluate whether a post indicates a pain signal using configured LLM client."""
    client = LLMClient()
    return client.evaluate(title=title, text=text)
