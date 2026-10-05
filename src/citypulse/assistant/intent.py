from __future__ import annotations

from citypulse.assistant.schemas import Entity, IntentName


def classify_intent(message: str) -> IntentName:
    text = message.lower()
    if any(word in text for word in ("validation", "validated", "backtest", "benchmark", "robustness")):
        return "VALIDATION_STATUS"
    if any(word in text for word in ("traffic", "congestion", "road", "speed")):
        return "TRAFFIC_STATUS"
    if any(word in text for word in ("energy", "power", "load")):
        return "ENERGY_STATUS"
    if any(word in text for word in ("mobility", "trip", "od", "transit", "travel")):
        return "MOBILITY_STATUS"
    if any(word in text for word in ("risk", "anomaly", "evidence")):
        return "RISK_STATUS"
    if any(word in text for word in ("what if", "scenario", "close road", "increase traffic")):
        return "SCENARIO_CREATE"
    if any(word in text for word in ("pareto", "decision", "trade-off", "tradeoff", "objective")):
        return "DECISION_ANALYSIS"
    if any(word in text for word in ("model", "drift", "validation", "trained", "deployed", "lineage", "retraining")):
        return "MODEL_INFORMATION"
    if any(word in text for word in ("stream", "live data", "event lag", "consumer", "broker")):
        return "STREAM_STATUS"
    if any(word in text for word in ("system", "api", "health", "available")):
        return "SYSTEM_STATUS"
    if any(word in text for word in ("citypulse", "platform", "model", "data")):
        return "GENERAL_PROJECT_QUERY"
    return "UNKNOWN"


def extract_entities(message: str) -> list[Entity]:
    entities: list[Entity] = []
    words = message.replace("#", " ").replace(",", " ").split()
    for index, word in enumerate(words):
        normalized = word.strip("?.:;()[]")
        if normalized.lower() in {"zone", "road", "segment", "building", "station"} and index + 1 < len(words):
            value = words[index + 1].strip("?.:;()[]")
            entities.append(Entity(kind=f"{normalized.lower()}_id", value=value, confidence=0.8))
    for word in words:
        normalized = word.strip("?.:;()[]")
        if normalized.isdigit() and not any(entity.value == normalized for entity in entities):
            entities.append(Entity(kind="numeric_reference", value=normalized, confidence=0.5))
    return entities
