# CITYPULSE Realtime Final Report

## Architecture

Phase 18 adds a local append-only event broker adapter, validated event schemas, topic registry, idempotent consumer, current-state store, dead-letter records, replay filtering, streaming APIs, assistant status integration, and a realtime frontend workspace.

## Broker and guarantees

Broker: `local_file_compatibility`.

Guarantee: `at-least-once` processing shape with event-ID idempotency. Kafka/Redpanda is not connected.

## Processing

Events are validated by Pydantic, written to topic logs, applied to bounded current state, and failed handlers are routed to dead letter. Event time and ingestion time remain separate.

## API

- `/api/v1/streaming/status`
- `/api/v1/streaming/topics`
- `/api/v1/streaming/health`
- `/api/v1/streaming/data-quality`
- `/api/v1/streaming/dead-letter`
- `/api/v1/streaming/replay`
- `/api/v1/streaming/state`

## Frontend

Added `/realtime` with broker status, topic registry, event counters, and explicit disconnected/no-data states.

## Assistant

The assistant can answer stream-health questions from the actual local service status.

## Not measured or active

No live sources, Kafka/Redpanda, Redis, WebSocket stream, stream processor cluster, model inference stream, risk stream, Prometheus, Grafana, Kubernetes, cloud deployment, throughput, lag, latency, or load benchmarks are active.
