from __future__ import annotations

from citypulse.decision.schemas import CandidateResult


def explain_candidate(result: CandidateResult) -> dict[str, object]:
    return {
        "candidate_id": result.candidate_id,
        "status": result.status,
        "feasible": result.feasible,
        "objective_values": result.objective_values,
        "constraint_findings": [constraint.model_dump() for constraint in result.constraints],
        "interpretation": "Model-based decision analysis; not a policy recommendation.",
    }
