from __future__ import annotations

from pathlib import Path

from citypulse.streaming.broker import LocalEventBroker
from citypulse.streaming.replay import replay_events
from citypulse.streaming.schemas import ReplayRequest, StreamStatus, UrbanEvent
from citypulse.streaming.state import UrbanStateStore
from citypulse.streaming.topics import ALL_TOPICS


class StreamingService:
    def __init__(self) -> None:
        self.broker = LocalEventBroker()
        self.state = UrbanStateStore()
        self.processed_ids: set[str] = set()

    def status(self) -> StreamStatus:
        dead_letters = self.broker.dead_letters()
        return StreamStatus(broker="local_file_compatibility", connected=False, status="STREAM NOT CONNECTED", topics=ALL_TOPICS, accepted_events=self.broker.accepted, rejected_events=self.broker.rejected, dead_letter_events=len(dead_letters), processed_event_ids=len(self.processed_ids), guarantee="at-least-once")

    def publish(self, topic: str, event: UrbanEvent) -> None:
        self.broker.publish(topic, event)
        self.state.apply(event)

    def replay(self, request: ReplayRequest) -> dict:
        return replay_events(self.broker, request)

    def current_state(self) -> dict:
        return self.state.get()
