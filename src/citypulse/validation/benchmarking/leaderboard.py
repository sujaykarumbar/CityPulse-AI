from __future__ import annotations

from typing import Any


def build_leaderboard(runs: list[dict[str, Any]], required_protocol: dict[str, Any]) -> dict[str, Any]:
    if not runs:
        return {"status": "NOT_MEASURED", "entries": [], "ranking": "NOT_PROVIDED"}
    included = []
    excluded = []
    for run in runs:
        mismatches = [key for key, value in required_protocol.items() if run.get(key) != value]
        (excluded if mismatches else included).append({"run": run, "protocol_mismatches": mismatches})
    return {"status": "MEASURED_PROTOCOL_FILTER", "entries": included, "excluded": excluded, "ranking": "NOT_PROVIDED"}
