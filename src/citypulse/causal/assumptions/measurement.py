from __future__ import annotations


def check_measurement_quality(measurement_error: float | None = None) -> dict[str, str | float | list[str]]:
    if measurement_error is None:
        return {"status": "NOT_CHECKED", "assumption": "measurement"}
    if measurement_error > 0.2:
        return {"status": "PARTIALLY_SUPPORTED", "assumption": "measurement", "measurement_error": measurement_error}
    return {"status": "SUPPORTED", "assumption": "measurement", "measurement_error": measurement_error}
