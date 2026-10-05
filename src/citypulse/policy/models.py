from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PolicyIntervention:
    policy_id: str
    name: str
    category: str
    description: str = ""
    treatment_variable: str | None = None
    target_population: str | None = None
    target_geography: str | None = None
    implementation_start: str | None = None
    implementation_end: str | None = None
    intensity: float | None = None
    budget: float | None = None
    constraints: list[str] = field(default_factory=list)
    expected_outcomes: list[str] = field(default_factory=list)
    evidence_sources: list[str] = field(default_factory=list)
    evidence_level: str = "NOT_AVAILABLE"
    assumptions: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyPackage:
    package_id: str
    policies: list[str]
    dependencies: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    budget: float | None = None
    constraints: list[str] = field(default_factory=list)


def validate_policy_package(package: PolicyPackage) -> dict[str, Any]:
    if not package.package_id:
        return {"status": "INVALID", "reason": "Missing package_id."}
    if not package.policies:
        return {"status": "INVALID", "reason": "A policy package requires at least one policy."}
    if package.conflicts:
        return {"status": "REVIEW_REQUIRED", "reason": "Package contains conflicts that require human review."}
    return {"status": "VALID", "package_id": package.package_id}
