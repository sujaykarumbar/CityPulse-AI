from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from citypulse.streaming.broker import LocalEventBroker
from citypulse.streaming.schemas import DeadLetterRecord, UrbanEvent


class EventConsumer:
    def __init__(self, broker: LocalEventBroker, state_path: Path = Path("artifacts/streaming/processed_ids.txt")) -> None:
        self.broker = broker
        self.state_path = state_path
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.processed_ids = set(self.state_path.read_text(encoding="utf-8").splitlines()) if self.state_path.exists() else set()

    def consume(self, topic: str, handler: Callable[[UrbanEvent], None], max_events: int | None = None) -> int:
        processed = 0
        for event in self.broker.read(topic)[:max_events]:
            if event.event_id in self.processed_ids:
                continue
            try:
                handler(event)
                self.processed_ids.add(event.event_id)
                with self.state_path.open("a", encoding="utf-8") as handle:
                    handle.write(event.event_id + "\n")
                processed += 1
            except Exception as exc:
                self.broker.dead_letter(DeadLetterRecord(event_id=event.event_id, original_topic=topic, error_code="PROCESSING_FAILED", error_message=type(exc).__name__, attempt_count=1))
        return processed
