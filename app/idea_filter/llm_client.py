"""Backward-compatible LLM client exports.

Canonical location: `llm_clients.llm_client`.
"""

import requests as requests

from llm_clients.llm_client import (
    LLMClient,
    PainSignalResult,
    _normalize_result,
    _parse_json_payload,
)

__all__ = ["LLMClient", "PainSignalResult", "_normalize_result", "_parse_json_payload"]
