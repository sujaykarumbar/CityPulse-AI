from __future__ import annotations

from threading import Lock

from citypulse.agents.schemas import Evidence


class EvidenceBus:
    def __init__(self) -> None:
        self._items: list[Evidence] = []
        self._lock = Lock()

    def publish(self, evidence: Evidence) -> None:
        with self._lock:
            self._items.append(evidence)

    def collect(self) -> list[Evidence]:
        with self._lock:
            return list(self._items)

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
