"""Backward-compatible prompt exports.

Canonical location: `idea_agent_app.idea_filter_agent.prompt_templates`.
"""

from idea_agent_app.idea_filter_agent.prompt_templates import (
    PAIN_SIGNAL_PROMPT_V1,
    build_pain_signal_user_prompt,
)

__all__ = ["PAIN_SIGNAL_PROMPT_V1", "build_pain_signal_user_prompt"]
