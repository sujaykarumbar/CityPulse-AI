from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvidenceProfile:
    causal: dict[str, Any] = field(default_factory=dict)
    simulation: dict[str, Any] = field(default_factory=dict)
    predictive: dict[str, Any] = field(default_factory=dict)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    provenance: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "causal": self.causal,
            "simulation": self.simulation,
            "predictive": self.predictive,
            "assumptions": self.assumptions,
            "limitations": self.limitations,
            "provenance": self.provenance,
        }


def normalize_evidence(evidence: dict[str, Any] | None = None) -> EvidenceProfile:
    payload = evidence or {}
    return EvidenceProfile(
        causal=payload.get("causal", {"status": "NOT_AVAILABLE"}),
        simulation=payload.get("simulation", {"status": "NOT_RUN"}),
        predictive=payload.get("predictive", {"status": "NOT_RUN"}),
        assumptions=payload.get("assumptions", []),
        limitations=payload.get("limitations", []),
        provenance=payload.get("provenance", []),
    )
