from __future__ import annotations

from datetime import datetime


def validate_temporal_order(*, treatment_timestamp: datetime, outcome_timestamp: datetime, covariate_timestamp: datetime | None = None) -> dict[str, str]:
    if treatment_timestamp >= outcome_timestamp:
        raise ValueError("Treatment must occur before the measured outcome when temporal ordering is required.")
    if covariate_timestamp is not None and covariate_timestamp > outcome_timestamp:
        raise ValueError("Covariates must be measured up to the outcome time, not after it.")
    return {"status": "TEMPORAL_ORDER_VALID"}
