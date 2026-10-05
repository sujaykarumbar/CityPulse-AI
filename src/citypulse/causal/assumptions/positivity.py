from __future__ import annotations


def check_positivity(overlap: float | None = None) -> dict[str, str | float | list[str]]:
    if overlap is None:
        return {"status": "NOT_CHECKED", "assumption": "positivity"}
    if overlap < 0.05:
        return {"status": "VIOLATED", "assumption": "positivity", "overlap": overlap}
    return {"status": "SUPPORTED", "assumption": "positivity", "overlap": overlap}
