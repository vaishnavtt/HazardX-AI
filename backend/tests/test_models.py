"""
HAZARDX AI — Model Catalog & Governance Tests
"""

def test_model_catalog(client):
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert data["total_models"] == 12
    assert data["operational_models_count"] == 8
    assert data["experimental_models_count"] == 2
    assert len(data["models"]) == 12
    
    # Check that each item has required governance fields
    for item in data["models"]:
        assert item["operational_status"] in ["OPERATIONAL", "EXPERIMENTAL", "UNAVAILABLE_FOR_OPERATIONAL_USE"]
        assert item["hazard"] in ["Floods", "Landslides", "Earthquakes", "Cyclones", "Wildfires"]
        assert item["model_version"] == "1.0.0"

def test_model_performance(client):
    response = client.get("/api/v1/models/performance")
    assert response.status_code == 200
    summaries = response.json()
    assert len(summaries) == 12
    
    # Check presence of all hazards
    hazards_found = set(s["hazard"] for s in summaries)
    assert {"Floods", "Landslides", "Earthquakes", "Cyclones", "Wildfires"}.issubset(hazards_found)
    
    # Verify cyclone rapid intensification metric
    ri_summary = next(s for s in summaries if s["task_name"] == "rapid_intensification")
    assert ri_summary["primary_metric_name"] == "PR-AUC"
    assert ri_summary["primary_test_score"] > 0.30
    assert ri_summary["operational_status"] == "OPERATIONAL"

    # Verify blocked models
    eq_count = next(s for s in summaries if s["task_name"] == "aftershock_count")
    assert eq_count["operational_status"] == "UNAVAILABLE_FOR_OPERATIONAL_USE"

    fire_dur = next(s for s in summaries if s["task_name"] == "fire_duration")
    assert fire_dur["operational_status"] == "UNAVAILABLE_FOR_OPERATIONAL_USE"

