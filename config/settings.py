from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    reddit_subreddit: str = "SaaS"
    reddit_limit: int = 20
    raw_items_path: Path = Path("data/raw_items.json")
    llm_provider: str = "openai"
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    openai_timeout_seconds: int = 30
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:14b"
    ollama_timeout_seconds: int = 180
    pain_signal_threshold: int = 6


def get_settings() -> Settings:
    return Settings(
        llm_provider=os.getenv("LLM_PROVIDER", "openai"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        openai_timeout_seconds=int(os.getenv("OPENAI_TIMEOUT_SECONDS", "30")),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "qwen3:14b"),
        ollama_timeout_seconds=int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "180")),
        pain_signal_threshold=int(os.getenv("PAIN_SIGNAL_THRESHOLD", "6")),
    )
