"""
HAZARDX AI — Phase 7 Advanced Geospatial Risk Assessment Tests
Verifies dynamic environmental feature synthesis, Copernicus DEM 5-point stencil,
GEM active fault indexing, and SHAP-explained multi-hazard location assessment.
"""

import pytest
from fastapi.testclient import TestClient

def test_location_profile_endpoint(client: TestClient):
    """Verifies that the location profile endpoint extracts authentic environmental variables."""
    # Test San Francisco coordinates
    lat, lon = 37.7749, -122.4194
    response = client.get(f"/api/v1/geospatial/location/{lat}/{lon}")
    assert response.status_code == 200
    data = response.json()
    assert "environmental_context" in data
    assert "nearest_fault" in data
    assert "terrain" in data
    assert "weather" in data
    assert "hydrology" in data

    env = data["environmental_context"]
    assert "elevation_m" in env
    assert "slope_degrees" in env
    assert "topographic_wetness_index" in env
    assert "dist_to_active_fault_km" in env
    assert env["dist_to_active_fault_km"] < 100.0  # San Francisco is near the San Andreas fault
    assert env["nearest_fault_slip_type"] in ["Dextral", "Strike-Slip", "Unknown"]
    assert "temp_2m_celsius" in env
    assert "fwi_fire_weather_index" in env

def test_geospatial_assess_endpoint_full(client: TestClient):
    """Verifies end-to-end multi-hazard risk assessment across all five hazards."""
    payload = {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "hazards": ["floods", "landslides", "earthquakes", "wildfires", "cyclones"]
    }
    response = client.post("/api/v1/geospatial/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["latitude"] == pytest.approx(37.7749, rel=1e-2)
    assert data["longitude"] == pytest.approx(-122.4194, rel=1e-2)
    assert data["feature_completeness_pct"] == 100.0
    assert data["overall_composite_risk"] in ["GREEN", "YELLOW", "ORANGE", "RED"]
    assert "overall_summary" in data
    assert "environmental_context" in data

    assessments = data["assessments"]
    assert "floods" in assessments
    assert "landslides" in assessments
    assert "earthquakes" in assessments
    assert "wildfires" in assessments
    assert "cyclones" in assessments

    # Inspect earthquake aftershock assessment result
    eq = assessments["earthquakes"]
    assert eq["hazard"] == "earthquakes"
    assert "aftershock" in eq["model_name"]
    assert 0.0 <= eq["probability"] <= 1.0
    assert eq["alert_level"] in ["GREEN", "YELLOW", "ORANGE", "RED"]
    assert isinstance(eq["risk_category"], str)
    assert len(eq["top_features"]) > 0  # SHAP attributions present

    # Inspect flood assessment result
    fl = assessments["floods"]
    assert fl["hazard"] == "floods"
    assert 0.0 <= fl["probability"] <= 1.0
    assert len(fl["top_features"]) > 0

def test_geospatial_assess_scenario_overrides(client: TestClient):
    """Verifies that scenario overrides (e.g. simulated major earthquake or deluge) are applied."""
    payload = {
        "latitude": 34.0522,
        "longitude": -118.2437, # Los Angeles
        "hazards": ["earthquakes", "floods"],
        "scenario_params": {
            "mainshock_mag": 7.8,
            "focal_depth_km": 5.0,
            "precip_1d_mm": 180.0
        }
    }
    response = client.post("/api/v1/geospatial/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assessments = data["assessments"]
    assert "earthquakes" in assessments
    assert "floods" in assessments
    # Extreme scenario should elevate hazard probabilities
    assert assessments["earthquakes"]["probability"] > 0.30

def test_geospatial_validation_errors(client: TestClient):
    """Verifies proper validation error codes on invalid coordinates."""
    response = client.post("/api/v1/geospatial/assess", json={"latitude": 120.0, "longitude": 0.0})
    assert response.status_code == 422

def test_geospatial_hazard_zones_all(client: TestClient):
    """
    Verifies that the /hazard-zones endpoint returns a valid GeoJSON FeatureCollection
    containing all 5 hazards with their mandatory scientific colors and valid properties.
    """
    response = client.get("/api/v1/geospatial/hazard-zones")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert "features" in data
    assert len(data["features"]) >= 5

    # Check that all 5 hazard types and mandatory colors are represented
    hazard_types = {f["properties"]["hazard_type"] for f in data["features"]}
    expected_hazards = {"floods", "landslides", "earthquakes", "cyclones", "wildfires"}
    assert expected_hazards.issubset(hazard_types)

    color_map = {
        "floods": "#2196F3",
        "landslides": "#FF9800",
        "earthquakes": "#9C27B0",
        "cyclones": "#00BCD4",
        "wildfires": "#F44336"
    }

    valid_severities = {"LOW", "MODERATE", "HIGH", "VERY HIGH", "VERY_HIGH", "EXTREME"}
    valid_layers = {"FORECAST_RISK_ZONE", "LIVE_OBSERVATION", "HISTORICAL_BENCHMARK", "MODEL_ASSESSMENT"}

    for f in data["features"]:
        props = f["properties"]
        hz = props["hazard_type"]
        assert props["color"] == color_map[hz]
        assert props["severity"] in valid_severities
        assert props["layer_type"] in valid_layers
        assert "risk_score" in props
        assert "data_provenance" in props
        assert f["geometry"]["type"] in ["Polygon", "Point", "LineString"]

def test_geospatial_hazard_zones_filtered(client: TestClient):
    """Verifies filtering by hazard_type and layer_type."""
    # Filter by hazard_type
    resp_flood = client.get("/api/v1/geospatial/hazard-zones?hazard_type=floods")
    assert resp_flood.status_code == 200
    data_flood = resp_flood.json()
    assert all(f["properties"]["hazard_type"] == "floods" for f in data_flood["features"])
    assert all(f["properties"]["color"] == "#2196F3" for f in data_flood["features"])

    # Filter by layer_type
    resp_layer = client.get("/api/v1/geospatial/hazard-zones?layer_type=FORECAST_RISK_ZONE")
    assert resp_layer.status_code == 200
    data_layer = resp_layer.json()
    assert all(f["properties"]["layer_type"] == "FORECAST_RISK_ZONE" for f in data_layer["features"])

