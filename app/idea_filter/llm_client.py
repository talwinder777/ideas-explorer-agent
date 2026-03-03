from __future__ import annotations

import json
from dataclasses import dataclass

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - handled gracefully at runtime
    OpenAI = None  # type: ignore[assignment]

from app.idea_filter.prompt_templates import PAIN_SIGNAL_PROMPT_V1, build_pain_signal_user_prompt
from config.settings import Settings, get_settings


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
    """OpenAI-backed LLM client wrapper for pain-signal filtering."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._client = None
        if OpenAI is not None and self.settings.openai_api_key:
            self._client = OpenAI(api_key=self.settings.openai_api_key)

    def evaluate(self, title: str, text: str = "") -> dict:
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
            payload = json.loads(raw_text)
            return _normalize_result(payload).to_dict()
        except Exception as e:
            return _fallback(str(e))
