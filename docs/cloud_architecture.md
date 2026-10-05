# Cloud Architecture

The local implementation is intentionally provider-neutral. A production deployment would replace the broker adapter with Kafka/Redpanda, move current state to Redis, retain history in PostgreSQL/object storage, expose authenticated WebSockets, and deploy consumers independently. Kubernetes manifests and autoscaling are not operationally verified in this checkout.
