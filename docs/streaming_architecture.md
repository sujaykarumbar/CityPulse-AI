# Phase 18 Streaming Architecture

The selected development broker is a local append-only file compatibility adapter. It preserves the event contract and at-least-once processing shape without claiming Kafka, Redpanda, Redis, or cloud connectivity.

```mermaid
flowchart LR
    Source[Verified source] --> Producer[Validated producer]
    Producer --> Broker[Local broker adapter]
    Broker --> Consumer[Idempotent consumer]
    Consumer --> State[Current urban state]
    Consumer --> DLQ[Dead letter]
    Broker --> Replay[Dry-run replay]
```

Production migration can replace the broker adapter with Kafka/Redpanda. Event ordering is only per source/topic implementation; global ordering is not guaranteed.
