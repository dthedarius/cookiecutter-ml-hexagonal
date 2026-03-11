import pytest
from fastapi.testclient import TestClient

from {{ cookiecutter.project_slug }}.adapters.inbound.api import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.mark.integration
def test_predict_endpoint(client: TestClient) -> None:
    response = client.post("/predict", json={"text": "test input"})
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data


@pytest.mark.integration
def test_predict_empty_text_returns_422(client: TestClient) -> None:
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422


@pytest.mark.integration
def test_health_ready(client: TestClient) -> None:
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data


@pytest.mark.integration
def test_health_live(client: TestClient) -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"
