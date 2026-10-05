from __future__ import annotations

from typing import Any


def compare_benchmark_runs(runs: list[dict[str, Any]], protocol: dict[str, Any]) -> dict[str, Any]:
    if not runs:
        return {"status": "VALIDATION_NOT_AVAILABLE", "runs": [], "reason": "NO_MODEL_RUNS_SUPPLIED"}
    expected = {key: protocol.get(key) for key in ("dataset_version", "target", "horizon", "split_id")}
    compatible = []
    incompatible = []
    for run in runs:
        differences = [key for key, value in expected.items() if value is not None and run.get(key) != value]
        (incompatible if differences else compatible).append({**run, "protocol_differences": differences})
    return {"status": "MEASURED_PROTOCOL_CHECK", "compatible_runs": compatible, "excluded_runs": incompatible, "comparison_protocol": expected, "ranking": "NOT_PROVIDED"}
