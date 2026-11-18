"""
HAZARDX AI — Phase 6 Real-Time Disaster Intelligence Integration Tests
Verifies live and recent data endpoints, scientific feed ingestion,
SQLite event persistence, and API health telemetry.
"""

import pytest
from fastapi.testclient import TestClient

def test_live_status_endpoint(client: TestClient):
    """Verifies that the live telemetry status endpoint reports all 6 scientific data sources."""
    response = client.get("/api/v1/live/status")
    assert response.status_code == 200
    data = response.json()
    assert data["system_status"] in ["OPERATIONAL", "DEGRADED"]
    assert "sources" in data
    assert len(data["sources"]) >= 6
    assert "Authentic Scientific APIs" in data["data_policy"]
    
    source_ids = [s["source_id"] for s in data["sources"]]
    assert "usgs_earthquakes" in source_ids
    assert "nasa_firms" in source_ids
    assert "open_meteo_weather" in source_ids
    assert "glofas_floods" in source_ids
    assert "noaa_nhc_cyclones" in source_ids
    assert "nasa_glc_landslides" in source_ids

def test_live_earthquakes_endpoint(client: TestClient):
    """Verifies real-time USGS earthquake feed ingestion."""
    response = client.get("/api/v1/live/earthquakes?min_magnitude=2.5&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["hazard_type"] == "earthquakes"
    assert "USGS" in data["source_attribution"]
    assert isinstance(data["data"], list)
    if len(data["data"]) > 0:
        event = data["data"][0]
        assert "magnitude" in event
        assert event["magnitude"] >= 2.5
        assert "latitude" in event
        assert "longitude" in event
        assert "depth_km" in event
        assert event["data_freshness"] in ["LIVE", "RECENT"]

def test_live_wildfires_endpoint(client: TestClient):
    """Verifies real-time NASA FIRMS active fire detection feed."""
    response = client.get("/api/v1/live/wildfires?min_confidence=nominal&limit=15")
    assert response.status_code == 200
    data = response.json()
    assert data["hazard_type"] == "wildfires"
    assert "NASA FIRMS" in data["source_attribution"]
    assert isinstance(data["data"], list)
    if len(data["data"]) > 0:
        event = data["data"][0]
        assert "brightness_kelvin" in event
        assert "frp_mw" in event
        assert "satellite" in event

def test_live_cyclones_endpoint(client: TestClient):
    """Verifies active tropical cyclone advisories and recent NOAA IBTrACS data."""
    response = client.get("/api/v1/live/cyclones?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["hazard_type"] == "cyclones"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    storm = data["data"][0]
    assert "intensity_kt" in storm
    assert "basin" in storm
    assert "name" in storm
    assert storm["data_freshness"] in ["LIVE", "RECENT"]

def test_live_floods_endpoint(client: TestClient):
    """Verifies Copernicus GloFAS river discharge endpoint."""
    # Test on Mississippi River delta reach
    response = client.get("/api/v1/live/floods?lat=29.95&lon=-90.07&location_name=Mississippi%20River")
    assert response.status_code == 200
    data = response.json()
    assert "current_discharge_m3s" in data
    assert "mean_discharge_7d_m3s" in data
    assert "discharge_anomaly_ratio" in data
    assert data["latitude"] == pytest.approx(29.95, rel=1e-2)
    assert data["longitude"] == pytest.approx(-90.07, rel=1e-2)
    assert "Copernicus GloFAS" in data["source"]

def test_live_landslides_endpoint(client: TestClient):
    """Verifies real-time landslide monitoring corridors and hydrometeorological triggers."""
    response = client.get("/api/v1/live/landslides?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["hazard_type"] == "landslides"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    obs = data["data"][0]
    assert "slope_degrees" in obs
    assert "precip_1d_mm" in obs
    assert "elevated_moisture_hazard" in obs

def test_live_weather_endpoint(client: TestClient):
    """Verifies real-time Open-Meteo atmospheric telemetry."""
    response = client.get("/api/v1/live/weather?lat=37.7749&lon=-122.4194")
    assert response.status_code == 200
    data = response.json()
    assert "temperature_2m_c" in data
    assert "relative_humidity_pct" in data
    assert "surface_pressure_hpa" in data
    assert "wind_speed_10m_ms" in data
    assert data["latitude"] == pytest.approx(37.7749, rel=1e-2)

def test_unified_events_endpoint(client: TestClient):
    """Verifies aggregated multi-hazard event query."""
    response = client.get("/api/v1/live/events?limit=25")
    assert response.status_code == 200
    data = response.json()
    assert "total_records" in data
    assert "records_returned" in data
    assert isinstance(data["data"], list)

