from __future__ import annotations

from typing import Any


def negative_transfer_status(*, local_mae: float | None = None, transferred_mae: float | None = None) -> str:
    if local_mae is None or transferred_mae is None:
        return "INSUFFICIENT_EVIDENCE"
    if local_mae <= 0:
        return "TRANSFER_HELPFUL"
    if transferred_mae > local_mae:
        return "NEGATIVE_TRANSFER"
    return "TRANSFER_HELPFUL"


def transfer_experiment(
    source_city: str,
    target_city: str,
    local_results: dict[str, Any],
    transfer_results: dict[str, Any],
) -> dict[str, Any]:
    if not local_results or not transfer_results:
        return {
            "status": "TRANSFER_NOT_EVALUATED",
            "source_city": source_city,
            "target_city": target_city,
            "ground_truth_status": "GROUND_TRUTH_NOT_AVAILABLE",
            "negative_transfer": "INSUFFICIENT_EVIDENCE",
            "limitations": ["Transfer evaluation requires measured target ground truth and a local baseline."],
        }

    local_mae = local_results.get("local_mae")
    transferred_mae = transfer_results.get("transferred_mae")
    if local_mae is None or transferred_mae is None:
        return {
            "status": "TRANSFER_NOT_EVALUATED",
            "source_city": source_city,
            "target_city": target_city,
            "ground_truth_status": "GROUND_TRUTH_NOT_AVAILABLE",
            "negative_transfer": "INSUFFICIENT_EVIDENCE",
        }

    return {
        "status": "MEASURED",
        "source_city": source_city,
        "target_city": target_city,
        "ground_truth_status": "AVAILABLE",
        "negative_transfer": negative_transfer_status(local_mae=float(local_mae), transferred_mae=float(transferred_mae)),
        "local_mae": float(local_mae),
        "transferred_mae": float(transferred_mae),
    }
