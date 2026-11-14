import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db


@pytest.fixture(autouse=True)
def setup_database():
    init_db()


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "active_provider" in data


def test_get_settings():
    with TestClient(app) as client:
        response = client.get("/api/settings")
        assert response.status_code == 200
        data = response.json()
        assert "llm_provider" in data
        assert "default_quality_threshold" in data


def test_get_analytics():
    with TestClient(app) as client:
        response = client.get("/api/analytics")
        assert response.status_code == 200
        data = response.json()
        assert "total_generated" in data
        assert "average_quality_score" in data
        assert "dimension_averages" in data


def test_list_content():
    with TestClient(app) as client:
        response = client.get("/api/content")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_generate_content_api():
    with TestClient(app) as client:
        payload = {
            "topic": "Graph Neural Networks in Drug Discovery",
            "target_audience": "Bioinformatics Researchers",
            "education_level": "Graduate / PhD",
            "learning_objectives": ["Message passing on molecular graphs"],
            "content_type": "lesson",
            "quality_threshold": 80.0,
            "max_retries": 3
        }
        response = client.post("/api/content/generate", json=payload)
        assert response.status_code == 202
        data = response.json()
        assert "request_id" in data
        assert data["status"] == "pending"
