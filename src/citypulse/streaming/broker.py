from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Iterable

from citypulse.streaming.schemas import DeadLetterRecord, UrbanEvent
from citypulse.streaming.topics import ALL_TOPICS, Topic


class LocalEventBroker:
    """Append-only local broker for development and deterministic tests.

    It models at-least-once delivery. Kafka/Redpanda can replace this adapter without changing event schemas.
    """

    def __init__(self, root: Path = Path("artifacts/streaming")) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = Lock()
        self.accepted = 0
        self.rejected = 0

    def publish(self, topic: str, event: UrbanEvent) -> None:
        if topic not in ALL_TOPICS:
            self.rejected += 1
            raise ValueError("UNKNOWN_TOPIC")
        path = self.root / f"{topic.replace('.', '_')}.jsonl"
        with self.lock, path.open("a", encoding="utf-8") as handle:
            handle.write(event.model_dump_json() + "\n")
        self.accepted += 1

    def read(self, topic: str) -> list[UrbanEvent]:
        path = self.root / f"{topic.replace('.', '_')}.jsonl"
        if not path.exists():
            return []
        return [UrbanEvent.model_validate_json(line) for line in path.read_text(encoding="utf-8").splitlines() if line]

    def dead_letter(self, record: DeadLetterRecord) -> None:
        path = self.root / f"{Topic.DEAD_LETTER.replace('.', '_')}.jsonl"
        with self.lock, path.open("a", encoding="utf-8") as handle:
            handle.write(record.model_dump_json() + "\n")

    def dead_letters(self) -> list[DeadLetterRecord]:
        path = self.root / f"{Topic.DEAD_LETTER.replace('.', '_')}.jsonl"
        if not path.exists():
            return []
        return [DeadLetterRecord.model_validate_json(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
