from __future__ import annotations

from pathlib import Path
from typing import Any

from citypulse.mlops.schemas import ModelRecord, ValidationCheck, ValidationResult


def validate_model(record: ModelRecord, gates: dict[str, Any] | None = None) -> ValidationResult:
    checks: list[ValidationCheck] = []
    checks.append(ValidationCheck(name="artifact_uri", status="PASS" if record.artifact_uri else "WARN", message="Artifact URI supplied" if record.artifact_uri else "Artifact URI not configured"))
    checks.append(ValidationCheck(name="lineage_metadata", status="PASS" if record.dataset_version and record.feature_version else "WARN", message="Dataset and feature lineage supplied" if record.dataset_version and record.feature_version else "Lineage is incomplete"))
    if record.artifact_uri and record.artifact_uri.startswith("file:"):
        path = Path(record.artifact_uri.removeprefix("file:"))
        checks.append(ValidationCheck(name="artifact_integrity", status="PASS" if path.exists() else "FAIL", message="Artifact exists" if path.exists() else "Artifact path does not exist"))
    for metric, rule in (gates or {}).items():
        observed = record.metrics.get(metric)
        threshold = rule.get("threshold")
        operator = rule.get("operator")
        if observed is None or threshold is None:
            checks.append(ValidationCheck(name=f"metric_gate:{metric}", status="WARN", message="VALIDATION_THRESHOLD_NOT_CONFIGURED or metric unavailable", observed_value=observed, threshold=threshold))
            continue
        passed = (observed <= threshold) if operator == "<=" else (observed >= threshold) if operator == ">=" else False
        checks.append(ValidationCheck(name=f"metric_gate:{metric}", status="PASS" if passed else "FAIL", message="Metric gate evaluated", observed_value=observed, threshold=threshold))
    status = "FAIL" if any(check.status == "FAIL" for check in checks) else "WARN" if any(check.status == "WARN" for check in checks) else "PASS"
    return ValidationResult(model_id=record.model_id, status=status, checks=checks)
