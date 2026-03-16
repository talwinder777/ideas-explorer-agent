from __future__ import annotations

"""Backward-compatible orchestrator exports.

Canonical location: `idea_agent_app.orchestrator.agent_manager`.
"""

from idea_agent_app.orchestrator.agent_manager import run_full_pipeline, run_pipeline

__all__ = ["run_pipeline", "run_full_pipeline"]
