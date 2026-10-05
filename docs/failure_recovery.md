# Streaming Failure Recovery

Consumer handlers use at-least-once semantics and persisted event IDs for idempotency. Handler failures are written to a dead-letter log with event ID, topic, error code, attempt count, and timestamp. Broker, Redis, database, network recovery, and distributed checkpointing are not active in the local compatibility implementation.
