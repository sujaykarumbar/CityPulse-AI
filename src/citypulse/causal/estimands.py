from __future__ import annotations


def estimand_summary(estimate: float, baseline: float | None = None, *, estimand: str = "ATE") -> dict[str, float | str]:
    if baseline is None:
        return {"estimand": estimand, "estimate": float(estimate), "status": "MEASURED"}

    absolute_effect = float(estimate - baseline)
    return {
        "estimand": estimand,
        "estimate": float(estimate),
        "absolute_effect": absolute_effect,
        "relative_effect": float((estimate - baseline) / baseline) if baseline != 0 else 0.0,
        "status": "MEASURED",
    }
