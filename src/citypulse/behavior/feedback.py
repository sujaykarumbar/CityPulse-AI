from __future__ import annotations


def feedback_loop(
    first_variable: str,
    second_variable: str,
    third_variable: str,
    fourth_variable: str,
) -> dict[str, str]:
    """Classify and annotate a simple feedback loop structure."""

    loop_type = "reinforcing" if first_variable == fourth_variable else "balancing"
    return {
        "loop_type": loop_type,
        "variables": [first_variable, second_variable, third_variable, fourth_variable],
        "status": "GRAPHED",
    }
