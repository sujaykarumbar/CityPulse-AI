# Event Schema

Events contain event ID, event type, source, event time, ingestion time, schema version, optional city/entity identifiers, payload, and metadata. Event time and processing time remain distinct.

Invalid topics are rejected. Failed handlers are written to the dead-letter log. Consumers use persisted event IDs for idempotent at-least-once processing.
