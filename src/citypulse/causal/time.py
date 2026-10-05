from __future__ import annotations

from datetime import datetime


def validate_time_window(start: datetime, end: datetime) -> dict[str, str | datetime]:
    if start >= end:
        raise ValueError("Causal time windows must define a valid start before end.")
    return {"start": start, "end": end, "status": "VALID_TIME_WINDOW"}
