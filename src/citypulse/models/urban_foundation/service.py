from __future__ import annotations

from datetime import datetime, timezone
from difflib import SequenceMatcher
from typing import Any

import numpy as np

from citypulse.models.urban_foundation.schemas import (
    ObjectiveName,
    UrbanFoundationObjective,
    UrbanFoundationSearchResponse,
    UrbanFoundationStatus,
    UrbanRepresentationRecord,
    UrbanResearchExperiment,
)


class UrbanFoundationService:
    def __init__(self) -> None:
        self.modalities: list[str] = ["TRAFFIC", "ENERGY", "MOBILITY", "GEOGRAPHY", "SENSING", "TEXT", "IMAGERY"]
        self.objectives: list[UrbanFoundationObjective] = [
            UrbanFoundationObjective(
                name="masked_modality_prediction",
                description="Predict masked urban modality tokens from observed multimodal context.",
                enabled=False,
            ),
            UrbanFoundationObjective(
                name="contrastive_cross_modal_alignment",
                description="Align paired traffic, mobility, energy, and spatial context embeddings.",
                enabled=False,
            ),
            UrbanFoundationObjective(
                name="temporal_imputation",
                description="Impute missing urban signals over time using neighboring observations.",
                enabled=False,
            ),
            UrbanFoundationObjective(
                name="spatial_context_prediction",
                description="Infer neighborhood context for zones, roads, and buildings from spatial priors.",
                enabled=False,
            ),
            UrbanFoundationObjective(
                name="multimodal_trajectory_matching",
                description="Match trajectories, events, and place embeddings for retrieval-style urban analysis.",
                enabled=False,
            ),
        ]
        self._index: dict[str, UrbanRepresentationRecord] = {}
        self._experiments: list[UrbanResearchExperiment] = []

    def status(self) -> UrbanFoundationStatus:
        return UrbanFoundationStatus(
            status="NOT TRAINED",
            training_ready=False,
            modalities=self.modalities,
            objectives=self.objectives,
            index_size=len(self._index),
            last_updated=datetime.now(timezone.utc) if self._index else None,
            notes="This repository contains a local urban-representation compatibility layer; no large-scale pretrained foundation model is present.",
        )

    def register_experiment(self, name: str, objective: ObjectiveName, description: str, **metadata: Any) -> UrbanResearchExperiment:
        experiment = UrbanResearchExperiment(
            experiment_id=f"exp-{len(self._experiments) + 1:04d}",
            name=name,
            objective=objective,
            description=description,
            status="PLANNED",
            metadata=metadata,
        )
        self._experiments.append(experiment)
        return experiment

    def list_experiments(self) -> list[UrbanResearchExperiment]:
        return list(self._experiments)

    def index_embeddings(self, records: list[UrbanRepresentationRecord]) -> list[UrbanRepresentationRecord]:
        stored: list[UrbanRepresentationRecord] = []
        for record in records:
            self._index[record.record_id] = record
            stored.append(record)
        return stored

    def search(self, query: str, top_k: int = 5) -> dict[str, Any]:
        if not self._index:
            return {"query": query, "total": 0, "items": []}

        query_tokens = {token.lower() for token in query.replace("-", " ").split() if token}
        ranked: list[tuple[float, UrbanRepresentationRecord]] = []
        for record in self._index.values():
            text_blob = " ".join(
                [
                    record.entity_type,
                    record.entity_id,
                    record.modality,
                    *(str(value).lower() for value in record.metadata.values()),
                ]
            ).lower()
            lexical = SequenceMatcher(None, query.lower(), text_blob).ratio()
            token_overlap = len(query_tokens & {token.lower() for token in text_blob.split()}) / max(1, len(query_tokens))
            score = max(lexical, token_overlap)
            if record.embedding:
                vector = np.asarray(record.embedding, dtype=float)
                token_hashes = np.asarray([self._hash_token(token) for token in query_tokens], dtype=float)
                if token_hashes.size:
                    token_hashes = token_hashes[: vector.size]
                    if vector.size == token_hashes.size:
                        vector_norm = np.linalg.norm(vector)
                        query_norm = np.linalg.norm(token_hashes)
                        if vector_norm > 0 and query_norm > 0:
                            score = max(score, float(np.dot(vector / vector_norm, token_hashes / query_norm)))
            ranked.append((score, record))

        ranked.sort(key=lambda item: item[0], reverse=True)
        items = [
            {
                "record_id": record.record_id,
                "entity_type": record.entity_type,
                "entity_id": record.entity_id,
                "modality": record.modality,
                "score": round(score, 6),
                "metadata": record.metadata,
            }
            for score, record in ranked[:top_k]
        ]
        return {"query": query, "total": len(items), "items": items}

    @staticmethod
    def _hash_token(token: str) -> float:
        return float(abs(hash(token)) % 1000) / 1000.0

    def modalities_available(self) -> list[str]:
        return list(self.modalities)

    def objectives_available(self) -> list[dict[str, Any]]:
        return [objective.model_dump(mode="json") for objective in self.objectives]
