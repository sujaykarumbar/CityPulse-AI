from __future__ import annotations

from threading import Lock
from typing import Any

from citypulse.streaming.schemas import UrbanEvent


class UrbanStateStore:
    """Bounded current-state store; durable history remains in the broker."""

    def __init__(self) -> None:
        self._values: dict[str, UrbanEvent] = {}
        self._lock = Lock()

    def apply(self, event: UrbanEvent) -> None:
        key = f"{event.entity_type or 'unknown'}:{event.entity_id or event.event_id}"
        with self._lock:
            self._values[key] = event

    def get(self) -> dict[str, dict[str, Any]]:
        with self._lock:
            return {key: event.model_dump(mode="json") for key, event in self._values.items()}

    def clear(self) -> None:
        with self._lock:
            self._values.clear()
