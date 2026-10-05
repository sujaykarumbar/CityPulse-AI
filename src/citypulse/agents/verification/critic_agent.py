from __future__ import annotations

from typing import Any

from citypulse.agents.schemas import Evidence


def verify_outputs(outputs: list[dict[str, Any]], evidence: list[Evidence]) -> dict[str, Any]:
    supported_sources = {item.source_id for item in evidence}
    factual_claims = []
    for output in outputs:
        claim = str(output.get("claim", ""))
        if not claim:
            continue
        source_id = output.get("source_id")
        factual_claims.append({
            "claim": claim,
            "source_id": source_id,
            "status": "SUPPORTED" if source_id in supported_sources else "NOT VERIFIED",
        })
    causal_claims = [claim["claim"] for claim in factual_claims if any(word in claim["claim"].lower() for word in (" caused ", " causes ", "caused by"))]
    return {
        "status": "VERIFIED" if factual_claims and all(item["status"] == "SUPPORTED" for item in factual_claims) and not causal_claims else "PARTIAL",
        "claims": factual_claims,
        "causal_claims_unverified": causal_claims,
        "limitations": ["Agent statements are not evidence.", "Temporal association does not establish causality."],
    }
