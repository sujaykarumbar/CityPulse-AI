from __future__ import annotations


def event_study(pre_effects: list[float], post_effects: list[float]) -> dict[str, object]:
    if not pre_effects and not post_effects:
        return {"status": "NOT_IDENTIFIED", "method": "event_study", "reason": "Event study requires pre- and/or post-treatment coefficients."}
    event_time = {"pre": pre_effects, "post": post_effects}
    return {
        "status": "MEASURED",
        "method": "event_study",
        "event_time_coefficient": event_time,
        "assumptions": ["no_anticipation", "parallel_trends_partial"],
    }
