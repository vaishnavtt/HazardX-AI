"""
HAZARDX AI — Combined Multi-Hazard Prediction Tests
"""

def test_multi_hazard_all_five(client, valid_flood_payload, valid_landslide_payload,
                                valid_earthquake_payload, valid_cyclone_payload, valid_wildfire_payload):
    request_data = {
        "flood": valid_flood_payload,
        "landslide": valid_landslide_payload,
        "earthquake": valid_earthquake_payload,
        "cyclone": valid_cyclone_payload,
        "wildfire": valid_wildfire_payload
    }
    response = client.post("/api/v1/predict/all", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data["hazards_evaluated"]) == 5
    assert data["composite_highest_alert_level"] in ["GREEN", "YELLOW", "ORANGE", "RED"]
    assert "flood" in data["results"]
    assert "landslide" in data["results"]
    assert "earthquake" in data["results"]
    assert "cyclone" in data["results"]
    assert "wildfire" in data["results"]

def test_multi_hazard_partial_two(client, valid_flood_payload, valid_landslide_payload):
    request_data = {
        "flood": valid_flood_payload,
        "landslide": valid_landslide_payload
    }
    response = client.post("/api/v1/predict/all", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data["hazards_evaluated"]) == 2
    assert "floods" in data["hazards_evaluated"]
    assert "landslides" in data["hazards_evaluated"]
    assert "flood" in data["results"]
    assert "landslide" in data["results"]
    assert "earthquake" not in data["results"]

def test_multi_hazard_empty_payload(client):
    response = client.post("/api/v1/predict/all", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error_code"] == "HTTP_400"
    assert "At least one hazard feature set must be provided" in data["message"]

