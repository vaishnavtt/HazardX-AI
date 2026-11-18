"""
HAZARDX AI — Phase 10 Multi-Hazard Forecasting & Early Warning Automated Tests
Verifies multi-horizon forecast endpoints (6h, 12h, 24h, 48h, 72h), Omori-Utsu aftershock decay,
model governance preservation, and location-specific predictive risk profiling.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.forecasting.omori_aftershock_model import omori_model
from backend.app.alerts.alert_classifier import alert_classifier

def test_forecast_summary_endpoint(client: TestClient):
    """
    Verifies that GET /api/v1/forecasts/summary returns forecast cards for all 5 hazards.
    """
    res = client.get("/api/v1/forecasts/summary")
    assert res.status_code == 200
    cards = res.json()
    assert isinstance(cards, list)
    assert len(cards) == 5

    hazards_present = {c["hazard_type"] for c in cards}
    assert hazards_present == {"floods", "landslides", "wildfires", "earthquakes", "cyclones"}

    for c in cards:
        assert "forecast_risk" in c
        assert c["forecast_risk"] in ["LOW", "MODERATE", "HIGH", "VERY HIGH", "EXTREME"]
        assert c["forecast_horizon"] in ["6h", "12h", "24h", "48h", "72h"]
        assert "trend" in c
        assert "primary_data_source" in c
        assert "data_provenance" in c

def test_forecast_timeline_endpoint(client: TestClient):
    """
    Verifies that GET /api/v1/forecasts/timeline returns 6h, 12h, 24h, 48h, 72h horizons for Floods.
    """
    res = client.get("/api/v1/forecasts/timeline?hazard=floods&lat=29.95&lon=-90.07")
    assert res.status_code == 200
    timeline = res.json()
    assert timeline["hazard_type"] == "floods"
    assert "horizons" in timeline
    assert set(timeline["horizons"].keys()) == {"6h", "12h", "24h", "48h", "72h"}

    h24 = timeline["horizons"]["24h"]
    assert h24["risk_category"] in ["LOW", "MODERATE", "HIGH", "VERY HIGH", "EXTREME"]
    assert "primary_metric_value" in h24
    assert "primary_metric_label" in h24
    assert timeline["overall_trend"] in ["RISING", "FALLING", "STABLE", "PEAKING"]
    assert "disclaimer" in timeline

def test_location_forecast_assessment(client: TestClient):
    """
    Verifies that POST /api/v1/forecasts/assess-location produces multi-hazard forecast synthesis.
    """
    payload = {
        "latitude": 30.3165,
        "longitude": 78.0322,
        "location_name": "Uttarakhand Himalayan Basin",
        "hazards": ["floods", "landslides", "wildfires", "earthquakes"],
        "selected_horizon": "24h"
    }
    res = client.post("/api/v1/forecasts/assess-location", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["location_name"] == "Uttarakhand Himalayan Basin"
    assert "composite_risk_category" in data
    assert "hazard_forecasts" in data
    assert "landslides" in data["hazard_forecasts"]
    assert "floods" in data["hazard_forecasts"]
    assert "disclaimer" in data

    # Verify duration and aftershock count models remain blocked
    wf_fc = data["hazard_forecasts"]["wildfires"]
    assert wf_fc["secondary_metrics"].get("duration_days") is None
    assert wf_fc["secondary_metrics"].get("model_duration_governance") == "BLOCKED"

    eq_fc = data["hazard_forecasts"]["earthquakes"]
    assert eq_fc["secondary_metrics"].get("aftershock_count") is None
    assert eq_fc["secondary_metrics"].get("model_count_governance") == "BLOCKED"

def test_omori_aftershock_statistical_decay():
    """
    Verifies that Omori-Utsu statistical decay calculates Poisson probabilities correctly
    and strictly enforces non-predictability disclaimers.
    """
    res = omori_model.forecast_horizons(mainshock_mag=7.0, elapsed_hours=4.0)
    assert "6h" in res
    assert "24h" in res
    assert "72h" in res

    # Probability of M4+ aftershock should be positive and bounded <= 1.0
    p6 = res["6h"]["prob_m4_plus"]
    p24 = res["24h"]["prob_m4_plus"]
    assert 0.0 < p6 <= 1.0
    assert 0.0 < p24 <= 1.0
    assert "NOT an exact earthquake prediction" in res["6h"]["disclaimer"]

def test_forecast_evaluations_endpoint(client: TestClient):
    """
    Verifies that GET /api/v1/forecasts/evaluations returns validated metrics and governance statuses.
    """
    res = client.get("/api/v1/forecasts/evaluations")
    assert res.status_code == 200
    data = res.json()
    assert "forecast_registry" in data
    assert "governance_status" in data
    assert "earthquakes_aftershock_count" in data["governance_status"]
    assert "BLOCKED" in data["governance_status"]["earthquakes_aftershock_count"]
