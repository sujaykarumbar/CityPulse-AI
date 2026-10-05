from __future__ import annotations

from citypulse.streaming.broker import LocalEventBroker
from citypulse.streaming.schemas import ReplayRequest, UrbanEvent


def replay_events(broker: LocalEventBroker, request: ReplayRequest) -> dict[str, int | str | bool]:
    events = broker.read(request.topic)
    selected: list[UrbanEvent] = []
    for event in events:
        if request.start_time and event.timestamp < request.start_time:
            continue
        if request.end_time and event.timestamp > request.end_time:
            continue
        if request.event_type and event.event_type != request.event_type:
            continue
        if request.entity_id and event.entity_id != request.entity_id:
            continue
        selected.append(event)
    return {"status": "DRY_RUN" if request.dry_run else "REPLAY_REQUESTED", "selected_events": len(selected), "destination": request.destination or request.topic, "speed": request.speed}
