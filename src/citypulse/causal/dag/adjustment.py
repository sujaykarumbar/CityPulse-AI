from __future__ import annotations


def identify_adjustment_set(treatment: str, outcome: str, confounders: list[str] | None = None) -> dict[str, object]:
    confounders = confounders or []
    if not confounders:
        return {
            "status": "NO_VALID_ADJUSTMENT_SET_IDENTIFIED",
            "recommended_adjustment_set": [],
            "blocked_paths": [],
            "remaining_paths": ["treatment -> outcome without identifiable confounder blocking"],
            "assumptions": ["No valid adjustment set could be identified from available metadata."],
        }

    return {
        "status": "VALID",
        "recommended_adjustment_set": confounders,
        "blocked_paths": [f"{treatment} <- confounder -> {outcome}"],
        "remaining_paths": [],
        "assumptions": ["Confounders are measured and must be adjusted for under the backdoor criterion."],
    }
