from citypulse.governance.classification import DataClassification, classify_dataset
from citypulse.governance.retention import RetentionPolicy, evaluate_retention
from citypulse.operations.health import aggregate_health
from citypulse.security.authorization import Role, authorize
from citypulse.security.authentication import validate_token


def test_jwt_validation_rejects_missing_claims() -> None:
    result = validate_token({"sub": "user-1"})

    assert result["valid"] is False
    assert result["reason"] == "missing_required_claims"


def test_rbac_allows_admin_but_denies_viewer_for_sensitive_action() -> None:
    assert authorize(Role.ADMIN, "manage:security") == True
    assert authorize(Role.VIEWER, "manage:security") == False


def test_governance_classification_and_retention_are_explicit() -> None:
    label = classify_dataset({"classification": "restricted"})
    policy = RetentionPolicy(name="raw-events", classification=DataClassification.RESTRICTED, days=90)

    assert label == DataClassification.RESTRICTED
    assert evaluate_retention(policy, 30)["status"] == "retain"


def test_health_summary_is_evidence_based() -> None:
    report = aggregate_health({"api": "HEALTHY", "database": "UNKNOWN", "redis": "DEGRADED"})

    assert report["status"] == "DEGRADED"
    assert report["components"]["database"] == "UNKNOWN"
