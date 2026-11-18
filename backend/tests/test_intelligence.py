"""
HAZARDX AI — External Intelligence Telemetry & Ingestion Automated Tests
Verifies source registry, health checks, freshness policies, and scheduler controls.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

def test_intelligence_sources_endpoint(client: TestClient):
    """
    Verifies that GET /api/v1/intelligence/sources returns authoritative data connectors.
    """
    res = client.get("/api/v1/intelligence/sources")
    assert res.status_code == 200
    sources = res.json()
    assert isinstance(sources, list)
    assert len(sources) >= 6

    ids = {s["source_id"] for s in sources}
    assert "usgs_earthquakes" in ids
    assert "open_meteo_weather" in ids
    assert "glofas_floods" in ids
    assert "nasa_firms" in ids
    assert "noaa_nhc_cyclones" in ids

    for s in sources:
        assert "health_status" in s
        assert "freshness_status" in s
        assert "data_category" in s
        assert "update_frequency" in s

def test_intelligence_health_endpoint(client: TestClient):
    """
    Verifies that GET /api/v1/intelligence/health provides latency and health metrics.
    """
    res = client.get("/api/v1/intelligence/health")
    assert res.status_code == 200
    health = res.json()
    assert "overall_status" in health
    assert health["overall_status"] in ["HEALTHY", "DEGRADED", "UNAVAILABLE"]
    assert "total_sources" in health
    assert "active_cache_entries" in health
    assert "sources" in health

def test_intelligence_freshness_endpoint(client: TestClient):
    """
    Verifies that GET /api/v1/intelligence/freshness analyzes observation age.
    """
    res = client.get("/api/v1/intelligence/freshness")
    assert res.status_code == 200
    data = res.json()
    assert "all_fresh" in data
    assert "sources" in data
    for s in data["sources"]:
        assert "freshness_status" in s
        assert s["freshness_status"] in ["FRESH", "ACCEPTABLE", "STALE", "UNAVAILABLE", "UNKNOWN"]
        assert "age_human" in s

def test_ingestion_status_endpoint(client: TestClient):
    """
    Verifies that GET /api/v1/ingestion/status returns scheduler configuration.
    """
    res = client.get("/api/v1/ingestion/status")
    assert res.status_code == 200
    data = res.json()
    assert "is_running" in data
    assert "interval_sec" in data
