from __future__ import annotations

import json
import re
from dataclasses import dataclass

import requests

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - handled gracefully at runtime
    OpenAI = None  # type: ignore[assignment]

from config.settings import Settings, get_settings
from idea_agent_app.idea_filter_agent.prompt_templates import (
    PAIN_SIGNAL_PROMPT_V1,
    build_pain_signal_user_prompt,
)


@dataclass
class PainSignalResult:
    is_pain_signal: bool
    pain_signal_score: int
    entrepreneur_opportunity_score: int
    reasoning_short: str
    evidence_snippet: str
    error: str | None = None

    def to_dict(self) -> dict:
        return {
            "is_pain_signal": self.is_pain_signal,
            "pain_signal_score": self.pain_signal_score,
            "entrepreneur_opportunity_score": self.entrepreneur_opportunity_score,
            "reasoning_short": self.reasoning_short,
            "evidence_snippet": self.evidence_snippet,
            "error": self.error,
        }


def _clamp_score(value: object) -> int:
    try:
        return max(0, min(10, int(value)))
    except Exception:
        return 0


def _normalize_result(payload: dict) -> PainSignalResult:
    return PainSignalResult(
        is_pain_signal=bool(payload.get("is_pain_signal", False)),
        pain_signal_score=_clamp_score(payload.get("pain_signal_score", 0)),
        entrepreneur_opportunity_score=_clamp_score(payload.get("entrepreneur_opportunity_score", 0)),
        reasoning_short=str(payload.get("reasoning_short", "")).strip() or "No reasoning provided",
        evidence_snippet=str(payload.get("evidence_snippet", "")).strip(),
        error=None,
    )


def _fallback(error: str) -> dict:
    return PainSignalResult(
        is_pain_signal=False,
        pain_signal_score=0,
        entrepreneur_opportunity_score=0,
        reasoning_short="Unable to evaluate pain signal",
        evidence_snippet="",
        error=error,
    ).to_dict()


class LLMClient:
    """Provider-agnostic LLM client wrapper for pain-signal filtering."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.provider = (self.settings.llm_provider or "openai").strip().lower()
        self._client = None
        if self.provider == "openai" and OpenAI is not None and self.settings.openai_api_key:
            self._client = OpenAI(api_key=self.settings.openai_api_key)

    def evaluate(self, title: str, text: str = "") -> dict:
        if self.provider == "ollama":
            return self._evaluate_ollama(title=title, text=text)
        if self.provider == "openai":
            return self._evaluate_openai(title=title, text=text)
        return _fallback(f"Unsupported LLM_PROVIDER: {self.provider}")

    def _evaluate_openai(self, title: str, text: str = "") -> dict:
        if OpenAI is None:
            return _fallback("openai package is not installed")
        if not self._client:
            return _fallback("OPENAI_API_KEY is not configured")

        user_prompt = build_pain_signal_user_prompt(title=title, text=text)

        try:
            response = self._client.responses.create(
                model=self.settings.openai_model,
                input=[
                    {"role": "system", "content": PAIN_SIGNAL_PROMPT_V1},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                timeout=self.settings.openai_timeout_seconds,
            )
            raw_text = getattr(response, "output_text", "") or ""
            payload = _parse_json_payload(raw_text)
            if payload is None:
                return _fallback("Model did not return valid JSON payload")
            return _normalize_result(payload).to_dict()
        except Exception as e:
            return _fallback(str(e))

    def _evaluate_ollama(self, title: str, text: str = "") -> dict:
        user_prompt = build_pain_signal_user_prompt(title=title, text=text)
        base_url = (self.settings.ollama_base_url or "http://localhost:11434").rstrip("/")
        endpoint = f"{base_url}/api/chat"

        try:
            response = requests.post(
                endpoint,
                json={
                    "model": self.settings.ollama_model,
                    "messages": [
                        {"role": "system", "content": PAIN_SIGNAL_PROMPT_V1},
                        {"role": "user", "content": user_prompt},
                    ],
                    "stream": False,
                    "format": "json",
                    "options": {"temperature": 0},
                },
                timeout=self.settings.ollama_timeout_seconds,
            )
            response.raise_for_status()
            response_payload = response.json()
            raw_text = (
                response_payload.get("message", {}).get("content")
                or response_payload.get("response")
                or ""
            )
            payload = _parse_json_payload(str(raw_text))
            if payload is None:
                return _fallback("Ollama response did not contain valid JSON payload")
            return _normalize_result(payload).to_dict()
        except Exception as e:
            return _fallback(str(e))


def _parse_json_payload(raw_text: str) -> dict | None:
    candidate = (raw_text or "").strip()
    if not candidate:
        return None

    try:
        parsed = json.loads(candidate)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    match = re.search(r"\{.*\}", candidate, re.DOTALL)
    if not match:
        return None

    try:
        parsed = json.loads(match.group(0))
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        return None
    return None
