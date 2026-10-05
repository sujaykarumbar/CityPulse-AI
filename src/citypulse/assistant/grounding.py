from __future__ import annotations

from typing import Any


def grounded_unavailable(domain: str, tool_error: str | None) -> str:
    detail = tool_error or "no registered tool is available"
    return f"I cannot provide a grounded {domain} answer because {detail}."


def collect_evidence(tool_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [evidence for result in tool_results for evidence in result.get("evidence", [])]
