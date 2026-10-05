from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_application_images_use_non_root_runtime_users() -> None:
    api_dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    frontend_dockerfile = (ROOT / "frontend" / "Dockerfile").read_text(encoding="utf-8")

    assert "USER 10001:10001" in api_dockerfile
    assert "nginxinc/nginx-unprivileged:" in frontend_dockerfile
    assert "HEALTHCHECK" in api_dockerfile
    assert "HEALTHCHECK" in frontend_dockerfile


def test_compose_keeps_optional_dependencies_profile_gated() -> None:
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text(encoding="utf-8"))
    services = compose["services"]

    assert {"api", "frontend"}.issubset(services)
    for name in ("postgres", "redis", "redpanda", "prometheus", "grafana"):
        assert services[name].get("profiles")


def test_compose_images_do_not_use_floating_latest_tags() -> None:
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text(encoding="utf-8"))

    for service in compose["services"].values():
        image = service.get("image")
        if image:
            assert not image.endswith(":latest")