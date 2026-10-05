from datetime import datetime, timezone

from citypulse.streaming.broker import LocalEventBroker
from citypulse.streaming.consumer import EventConsumer
from citypulse.streaming.replay import replay_events
from citypulse.streaming.schemas import ReplayRequest, UrbanEvent
from citypulse.streaming.service import StreamingService
from citypulse.streaming.topics import Topic


def event(event_id: str = "e1") -> UrbanEvent:
    return UrbanEvent(event_id=event_id, event_type="TRAFFIC_UPDATE", source="test", timestamp=datetime.now(timezone.utc), entity_type="road_segment", entity_id="r1", payload={"speed": 20})


def test_event_publish_consume_is_idempotent(tmp_path) -> None:
    broker = LocalEventBroker(tmp_path)
    broker.publish(Topic.TRAFFIC_RAW, event())
    seen: list[str] = []
    consumer = EventConsumer(broker, tmp_path / "processed.txt")

    assert consumer.consume(Topic.TRAFFIC_RAW, lambda item: seen.append(item.event_id)) == 1
    assert consumer.consume(Topic.TRAFFIC_RAW, lambda item: seen.append(item.event_id)) == 0
    assert seen == ["e1"]


def test_failed_processing_goes_to_dead_letter(tmp_path) -> None:
    broker = LocalEventBroker(tmp_path)
    broker.publish(Topic.TRAFFIC_RAW, event())
    consumer = EventConsumer(broker, tmp_path / "processed.txt")

    consumer.consume(Topic.TRAFFIC_RAW, lambda _: (_ for _ in ()).throw(ValueError("bad")))

    assert len(broker.dead_letters()) == 1
    assert broker.dead_letters()[0].error_code == "PROCESSING_FAILED"


def test_replay_defaults_to_dry_run(tmp_path) -> None:
    broker = LocalEventBroker(tmp_path)
    broker.publish(Topic.TRAFFIC_RAW, event())

    result = replay_events(broker, ReplayRequest(topic=Topic.TRAFFIC_RAW))

    assert result["status"] == "DRY_RUN"
    assert result["selected_events"] == 1


def test_stream_status_is_honest() -> None:
    status = StreamingService().status()

    assert status.connected is False
    assert status.status == "STREAM NOT CONNECTED"
    assert status.guarantee == "at-least-once"
