from __future__ import annotations

import json
from pathlib import Path

from citypulse.simulation.schemas import SimulationResult


def write_report(result: SimulationResult, directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / f"{result.scenario_id}.json"
    output.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    return output
