from __future__ import annotations

from typing import Any

from idea_agent_app.idea_filter_agent.evaluator import evaluate_pain_signal


def analyze_raw_items(
    raw_items: list[dict[str, Any]],
    pain_signal_threshold: int = 6,
    include_all: bool = False,
) -> list[dict[str, Any]]:
    """Evaluate raw items with LLM pain-signal analysis.

    Returns either only pain candidates (default) or all items with analysis,
    based on `include_all`.
    """

    analyzed: list[dict[str, Any]] = []
    for item in raw_items:
        title = str(item.get("title", ""))
        text = str(item.get("text", ""))
        analysis = evaluate_pain_signal(title=title, text=text)

        enriched = {**item, "analysis": analysis}
        is_candidate = bool(analysis.get("is_pain_signal", False)) and int(
            analysis.get("pain_signal_score", 0)
        ) >= int(pain_signal_threshold)
        enriched["is_candidate"] = is_candidate

        if include_all or is_candidate:
            analyzed.append(enriched)

    return analyzed
