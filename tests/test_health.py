from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_200():
    """Test that the health check endpoint returns a 200 status code."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_schema():
    """Response body must contain the expected typed fields."""
    response = client.get("/health")
    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "Smart Business Agent"
    assert data["version"] == "0.1.0"
    assert set(data.keys()) == {"status", "service", "version"}


def test_unknown_route_returns_404():
    """Edge case: unknown routes should 404, not crash."""
    response = client.get("/does-not-exist")
    assert response.status_code == 404
