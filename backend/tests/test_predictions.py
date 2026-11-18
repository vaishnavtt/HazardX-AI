"""
HAZARDX AI — Per-Hazard Prediction Endpoint Tests
"""

def test_flood_prediction(client, valid_flood_payload):
    response = client.post("/api/v1/predict/flood", json=valid_flood_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["hazard_name"] == "Floods"
    assert "flood_occurrence_predicted" in data
    assert 0.0 <= data["raw_model_score"] <= 1.0
    assert 0.0 <= data["calibrated_susceptibility_score"] <= 1.0
    assert data["risk_category"] in ["LOW", "MODERATE", "HIGH", "SEVERE_CRITICAL"]
    assert data["alert_level"] in ["GREEN", "YELLOW", "ORANGE", "RED"]
    assert len(data["important_contributing_features"]) > 0
    assert data["input_validation_status"] == "VALID"
    assert len(data["limitations_and_warnings"]) > 0

def test_landslide_prediction(client, valid_landslide_payload):
    response = client.post("/api/v1/predict/landslide", json=valid_landslide_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["hazard_name"] == "Landslides"
    assert "landslide_occurrence_predicted" in data
    assert 0.0 <= data["raw_model_score"] <= 1.0
    assert 0.0 <= data["calibrated_susceptibility_score"] <= 1.0
    assert data["risk_category"] in ["LOW", "MODERATE", "HIGH", "SEVERE_CRITICAL"]
    assert data["alert_level"] in ["GREEN", "YELLOW", "ORANGE", "RED"]
    assert len(data["important_contributing_features"]) > 0
    assert data["input_validation_status"] == "VALID"

def test_earthquake_prediction(client, valid_earthquake_payload):
    response = client.post("/api/v1/predict/earthquake", json=valid_earthquake_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["hazard_name"] == "Earthquakes"
    assert "elevated_aftershock_hazard_predicted" in data
    assert 0.0 <= data["hazard_probability"] <= 1.0
    assert data["alert_level"] in ["GREEN", "YELLOW", "RED"]
    assert "NOT an exact earthquake prediction" in data["disclaimer"]
    assert len(data["important_contributing_features"]) > 0
    # Operational governance verification: count model blocked
    assert data["estimated_aftershock_count"] is None
    assert any("UNAVAILABLE FOR OPERATIONAL USE" in w or "BLOCKED" in w for w in data["limitations_and_warnings"])

def test_cyclone_prediction(client, valid_cyclone_payload):
    response = client.post("/api/v1/predict/cyclone", json=valid_cyclone_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["hazard_name"] == "Cyclones"
    assert "rapid_intensification_predicted" in data
    assert 0.0 <= data["rapid_intensification_probability"] <= 1.0
    assert isinstance(data["predicted_24h_intensity_change_kt"], (int, float))
    assert data["projected_wind_24h_kt"] >= 10.0
    assert data["risk_category"] in ["LOW_RI_RISK", "MODERATE_RI_POTENTIAL", "RAPID_INTENSIFICATION_ALERT"]
    assert data["alert_level"] in ["GREEN", "YELLOW", "RED"]
    assert len(data["important_contributing_features"]) > 0

def test_wildfire_prediction(client, valid_wildfire_payload):
    response = client.post("/api/v1/predict/wildfire", json=valid_wildfire_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["hazard_name"] == "Wildfires"
    assert "wildfire_susceptibility_predicted" in data
    assert 0.0 <= data["raw_model_score"] <= 1.0
    assert 0.0 <= data["calibrated_susceptibility_score"] <= 1.0
    assert data["risk_category"] in ["LOW", "MODERATE", "HIGH", "SEVERE_CRITICAL"]
    assert data["alert_level"] in ["GREEN", "YELLOW", "ORANGE", "RED"]
    assert len(data["important_contributing_features"]) > 0
    # Operational governance verification: duration blocked
    assert data["estimated_duration_days"] is None
    assert any("BLOCKED" in w for w in data["limitations_and_warnings"])
