from __future__ import annotations

from pathlib import Path

from citypulse.decision.schemas import DecisionResult


def write_decision_report(result: DecisionResult, directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{result.problem_id}.json"
    path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    return path
