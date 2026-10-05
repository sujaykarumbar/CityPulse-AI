from __future__ import annotations

from typing import Any

from citypulse.policy.evidence import normalize_evidence
from citypulse.policy.robustness import robustness_report
from citypulse.policy.transferability import assess_transferability


class PolicyExperimentEngine:
    def evaluate(
        self,
        *,
        policy_id: str,
        city_id: str,
        baseline: dict[str, Any] | None = None,
        simulation: dict[str, Any] | None = None,
        evidence: dict[str, Any] | None = None,
        objectives: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        profile = normalize_evidence(evidence)
        causal_status = profile.causal.get("status", "NOT_AVAILABLE")
        if causal_status in {"NOT_AVAILABLE", "NOT_RUN", "INSUFFICIENT_DATA"}:
            return {
                "status": "REVIEW_REQUIRED",
                "policy_id": policy_id,
                "city_id": city_id,
                "baseline": baseline or {},
                "simulation": simulation or {},
                "evidence_status": "INSUFFICIENT_DATA",
                "evidence": profile.as_dict(),
                "objectives": objectives or [],
                "limitations": ["The available evidence is insufficient to support a causal policy recommendation."],
            }

        return {
            "status": "EVALUATED",
            "policy_id": policy_id,
            "city_id": city_id,
            "baseline": baseline or {},
            "simulation": simulation or {},
            "evidence_status": "SUPPORTED",
            "evidence": profile.as_dict(),
            "objectives": objectives or [],
            "limitations": [],
        }

    def transferability(self, *, source_city: str, target_city: str, overlap: dict[str, Any] | None = None) -> dict[str, Any]:
        return assess_transferability(source_city=source_city, target_city=target_city, overlap=overlap)

    def robustness(self, *, policy_id: str, scenarios: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        return robustness_report(policy_id=policy_id, scenarios=scenarios)
