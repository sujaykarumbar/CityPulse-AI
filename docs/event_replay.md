# Event Replay

Replay supports topic, time range, event type, entity, destination, speed, and dry-run selection. Dry-run is the default to prevent accidental production mutation. The current implementation selects events from local append-only logs and does not publish to an external broker.
