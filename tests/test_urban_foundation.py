from fastapi.testclient import TestClient

from citypulse.main import app
from citypulse.models.urban_foundation.service import UrbanFoundationService
from citypulse.models.urban_foundation.schemas import UrbanRepresentationRecord


def test_urban_foundation_status_is_honest() -> None:
    status = UrbanFoundationService().status()

    assert status.status == "NOT TRAINED"
    assert status.training_ready is False
    assert status.modalities


def test_urban_foundation_index_and_search_work_locally() -> None:
    service = UrbanFoundationService()
    record = UrbanRepresentationRecord(
        record_id="r1",
        entity_type="road_segment",
        entity_id="segment-42",
        modality="TRAFFIC",
        embedding=[0.1, -0.2, 0.3, 0.5],
        metadata={"zone": "downtown", "source": "simulated"},
    )

    service.index_embeddings([record])
    result = service.search("traffic segment", top_k=5)

    assert result["total"] >= 1
    assert result["items"][0]["record_id"] == "r1"


def test_urban_foundation_router_status_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/urban-foundation/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "NOT TRAINED"
