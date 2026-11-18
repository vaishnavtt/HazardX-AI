"""
HAZARDX AI — Request Validation & Error Handling Tests
"""

def test_flood_missing_required_field(client, valid_flood_payload):
    bad_payload = valid_flood_payload.copy()
    del bad_payload["river_discharge_m3s"]
    response = client.post("/api/v1/predict/flood", json=bad_payload)
    assert response.status_code == 422
    data = response.json()
    assert data["error_code"] == "VALIDATION_ERROR"
    assert any("river_discharge_m3s" in d["field"] for d in data["details"])

def test_cyclone_out_of_bounds_wind(client, valid_cyclone_payload):
    bad_payload = valid_cyclone_payload.copy()
    bad_payload["current_wind_kt"] = 350.0  # Max limit is 220 kt
    response = client.post("/api/v1/predict/cyclone", json=bad_payload)
    assert response.status_code == 422
    data = response.json()
    assert data["error_code"] == "VALIDATION_ERROR"
    assert any("current_wind_kt" in d["field"] for d in data["details"])

def test_wildfire_invalid_relative_humidity(client, valid_wildfire_payload):
    bad_payload = valid_wildfire_payload.copy()
    bad_payload["relative_humidity_pct"] = 150.0  # Max limit is 100%
    response = client.post("/api/v1/predict/wildfire", json=bad_payload)
    assert response.status_code == 422
    data = response.json()
    assert data["error_code"] == "VALIDATION_ERROR"
    assert any("relative_humidity_pct" in d["field"] for d in data["details"])

def test_earthquake_invalid_slip_type(client, valid_earthquake_payload):
    bad_payload = valid_earthquake_payload.copy()
    bad_payload["nearest_fault_slip_type"] = "Volcanic-Explosion"  # Unsupported category
    response = client.post("/api/v1/predict/earthquake", json=bad_payload)
    assert response.status_code == 422
    data = response.json()
    assert data["error_code"] == "VALIDATION_ERROR"

def test_landslide_invalid_type_string(client, valid_landslide_payload):
    bad_payload = valid_landslide_payload.copy()
    bad_payload["slope_degrees"] = "very_steep"
    response = client.post("/api/v1/predict/landslide", json=bad_payload)
    assert response.status_code == 422
    data = response.json()
    assert data["error_code"] == "VALIDATION_ERROR"

