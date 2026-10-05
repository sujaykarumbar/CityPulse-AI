from __future__ import annotations

from collections.abc import Mapping


def demand_response(
    policy_change: Mapping[str, float] | None,
    baseline_demand: Mapping[str, float] | None,
    elasticity: Mapping[str, float] | None,
) -> dict[str, object]:
    """Estimate a simulated demand response to a policy intervention.

    The implementation remains deliberately conservative and synthetic: it models
    demand as a function of policy intensity and elasticity without asserting real
    world truth claims.
    """

    policy = dict(policy_change or {})
    baseline = dict(baseline_demand or {})
    elasticities = dict(elasticity or {})

    response: dict[str, object] = {"status": "SIMULATED"}

    for segment, demand in baseline.items():
        price_change = float(policy.get("fare", 0.0))
        e = float(elasticities.get(segment, 0.0))
        projected = float(demand) * (1.0 + (e * price_change))
        delta = projected - float(demand)
        segment_response = {
            "baseline": float(demand),
            "projected": projected,
            "delta": delta,
            "elasticity": e,
        }
        response[segment] = segment_response
        response.setdefault("items", {})[segment] = segment_response

    return response
