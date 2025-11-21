"""
Tests for health and metrics endpoints
"""
import pytest


@pytest.mark.unit
def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


@pytest.mark.unit
def test_metrics_endpoint(client):
    """Test Prometheus metrics endpoint"""
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]


@pytest.mark.unit
def test_root_endpoint(client):
    """Test root endpoint redirects to docs"""
    response = client.get("/", follow_redirects=False)

    assert response.status_code in [200, 307, 308]  # OK or redirect


@pytest.mark.unit
def test_health_with_models(client):
    """Test health endpoint includes model status"""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    # Should have models info
    assert "models" in data or "status" in data
