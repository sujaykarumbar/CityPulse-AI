from __future__ import annotations

from typing import Any


def drop_modalities(sample: dict[str, Any], modalities: list[str]) -> dict[str, Any]:
    """Remove requested modalities and emit explicit availability flags."""

    result = dict(sample)
    available = dict(result.get("modality_available", {}))
    for modality in modalities:
        result.pop(modality, None)
        available[modality] = False
    for modality in sample:
        if modality != "modality_available":
            available.setdefault(modality, True)
    result["modality_available"] = available
    result["perturbation_origin"] = "SYNTHETIC_ROBUSTNESS_TEST"
    return result
