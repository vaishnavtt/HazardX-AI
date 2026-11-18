"""
HAZARDX AI — Model Explainability & Dashboard Endpoint Tests
"""

def test_explanations_all_hazards(client):
    hazards = ["floods", "landslides", "earthquakes", "cyclones", "wildfires"]
    for h in hazards:
        response = client.get(f"/api/v1/explanations/{h}")
        assert response.status_code == 200
        data = response.json()
        assert data["hazard_name"].lower() == h
        assert len(data["top_global_features"]) > 0
        assert len(data["physical_interpretation"]) > 0
        assert data["method"] == "TreeSHAP (Tree Explainer)"
        # Check that top features have physical interpretations
        for item in data["top_global_features"]:
            assert "feature" in item
            assert "mean_abs_shap" in item
            assert "physical_role" in item

def test_explanations_invalid_hazard(client):
    response = client.get("/api/v1/explanations/tornado")
    assert response.status_code == 404
    data = response.json()
    assert data["error_code"] == "HTTP_404"
    assert "not recognized" in data["message"]

def test_dashboard_summary(client):
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ONLINE"
    assert data["total_hazards_supported"] == 5
    assert data["total_models_available"] == 12
    assert data["operational_models_count"] == 8
    assert data["experimental_models_count"] == 2
    assert len(data["hazard_overview"]) == 5

