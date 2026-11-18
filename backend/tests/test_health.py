"""
HAZARDX AI — Backend Health Endpoint Tests
"""

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ONLINE"
    assert "version" in data
    assert data["api_v1_prefix"] == "/api/v1"

def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["models_loaded"] == 12
    assert len(data["operational_models"]) == 8
    assert len(data["experimental_models"]) == 2
    assert "timestamp" in data

