from __future__ import annotations

from typing import Any


def build_evidence(
    problem_id: str,
    candidate_id: str,
    source: str,
    assumptions: list[str],
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "candidate_id": candidate_id,
        "source": source,
        "assumptions": assumptions,
        "metadata": metadata or {},
        "causal_status": "CAUSAL_EFFECT_NOT_ESTABLISHED",
    }
