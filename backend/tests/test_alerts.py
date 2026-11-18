"""
HAZARDX AI — Phase 8 Intelligent Early Warning & Alert Management Tests
Verifies alert rules, classification, deduplication, state lifecycle,
audit logging, notifications, and background monitoring endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.alerts.alert_rules import alert_rules
from backend.app.alerts.alert_deduplication import alert_deduplicator
from backend.app.alerts.alert_classifier import alert_classifier
from backend.app.alerts.alert_manager import alert_manager
from backend.app.alerts.notification_service import notification_service

def test_alert_rules_evaluation():
    """Verifies that physical thresholds accurately map to four alert severity tiers."""
    # 1. Flood: Anomaly ratio >= 2.5 should yield RED
    sev, conf, metric = alert_rules.evaluate_flood(anomaly_ratio=2.8, precip_1d_mm=40.0, discharge_m3s=500.0)
    assert sev == "RED"
    assert conf >= 0.85

    # Flood: Moderate anomaly ratio 1.5 should yield YELLOW
    sev, conf, metric = alert_rules.evaluate_flood(anomaly_ratio=1.5, precip_1d_mm=10.0, discharge_m3s=150.0)
    assert sev == "YELLOW"

    # 2. Landslide: High slope + heavy rain should yield RED
    sev, conf, metric = alert_rules.evaluate_landslide(slope_degrees=32.0, precip_1d_mm=95.0, precip_30d_mm=250.0)
    assert sev == "RED"

    # 3. Earthquake: Mainshock M >= 6.5 should yield RED aftershock advisory
    sev, conf, metric = alert_rules.evaluate_earthquake(magnitude=6.8, depth_km=10.0, dist_fault_km=12.0)
    assert sev == "RED"

    # 4. Cyclone: Category 4 wind (130 kt) should yield RED
    sev, conf, metric = alert_rules.evaluate_cyclone(intensity_kt=130.0, min_pres_hpa=925.0)
    assert sev == "RED"

    # 5. Wildfire: High FRP + severe fire weather index should yield RED
    sev, conf, metric = alert_rules.evaluate_wildfire(frp_mw=85.0, brightness_k=365.0, fwi=45.0)
    assert sev == "RED"

def test_alert_deduplication_and_escalation():
    """Verifies spatial-temporal clustering and severity escalation logic."""
    hazard = "floods"
    lat, lon = 29.95, -90.07

    key1 = alert_deduplicator.generate_dedup_key(hazard, lat, lon)
    # Coordinate slightly offset within the same 0.25 deg cell (~25km)
    key2 = alert_deduplicator.generate_dedup_key(hazard, lat + 0.05, lon - 0.05)
    assert key1 == key2

    # Verify escalation logic
    assert alert_deduplicator.should_escalate("YELLOW", "RED") is True
    assert alert_deduplicator.should_escalate("ORANGE", "RED") is True
    assert alert_deduplicator.should_escalate("RED", "ORANGE") is False
    assert alert_deduplicator.should_escalate("RED", "RED") is False

def test_alert_crud_and_lifecycle(client: TestClient):
    """Verifies end-to-end alert creation, retrieval, acknowledgement, and resolution."""
    # 1. Create a test alert via classifier & manager
    payload = alert_classifier.classify_flood(
        lat=37.77,
        lon=-122.42,
        location_name="San Francisco Bay Drainage Reach",
        discharge_m3s=420.0,
        anomaly_ratio=2.6,
        precip_1d_mm=85.0,
        model_score=0.78
    )

    alert_item, is_new = alert_manager.create_or_update_alert(payload)
    assert alert_item.alert_id is not None
    assert alert_item.severity == "RED"
    assert alert_item.status == "ACTIVE"

    # 2. Retrieve via GET /api/v1/alerts/{alert_id}
    resp = client.get(f"/api/v1/alerts/{alert_item.alert_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["alert_id"] == alert_item.alert_id
    assert data["hazard_type"] == "floods"
    assert "Discharge Anomaly" in data["description"] or "discharge anomaly" in data["description"]

    # 3. Acknowledge alert via POST /api/v1/alerts/{alert_id}/acknowledge
    ack_resp = client.post(
        f"/api/v1/alerts/{alert_item.alert_id}/acknowledge",
        json={"acknowledged_by": "Test Analyst", "notes": "Dispatched field team"}
    )
    assert ack_resp.status_code == 200
    ack_data = ack_resp.json()
    assert ack_data["status"] == "ACKNOWLEDGED"
    assert ack_data["acknowledged_by"] == "Test Analyst"

    # 4. Resolve alert via POST /api/v1/alerts/{alert_id}/resolve
    res_resp = client.post(
        f"/api/v1/alerts/{alert_item.alert_id}/resolve",
        json={"resolved_by": "Incident Commander", "resolution_notes": "Waters receded below alert threshold"}
    )
    assert res_resp.status_code == 200
    res_data = res_resp.json()
    assert res_data["status"] == "RESOLVED"
    assert res_data["resolution_notes"] == "Waters receded below alert threshold"

def test_alert_listing_and_filtering(client: TestClient):
    """Verifies paginated alert listing with hazard and severity filters."""
    # Create test alerts for different hazards
    eq_payload = alert_classifier.classify_earthquake(
        lat=35.68,
        lon=139.69,
        location_name="Tokyo Kanto Basin",
        magnitude=5.8,
        depth_km=15.0,
        dist_fault_km=18.0
    )
    alert_manager.create_or_update_alert(eq_payload)

    # Query with hazard filter
    resp = client.get("/api/v1/alerts?hazard_type=earthquakes&page=1&page_size=10")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    assert all(a["hazard_type"] == "earthquakes" for a in data["items"])

    # Query with severity filter
    resp_sev = client.get("/api/v1/alerts?severity=ORANGE")
    assert resp_sev.status_code == 200
    data_sev = resp_sev.json()
    assert all(a["severity"] == "ORANGE" for a in data_sev["items"])

def test_alert_summary_endpoint(client: TestClient):
    """Verifies the alert summary and operational metric counts."""
    resp = client.get("/api/v1/alerts/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_active" in data
    assert "total_severe_red" in data
    assert "by_hazard" in data
    assert "recent_alerts" in data
    assert "floods" in data["by_hazard"]
    assert "earthquakes" in data["by_hazard"]

def test_alert_history_audit_trail(client: TestClient):
    """Verifies that alert state changes are recorded in the audit trail."""
    resp = client.get("/api/v1/alerts/history?limit=10")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    if len(data) > 0:
        entry = data[0]
        assert "alert_id" in entry
        assert "action_type" in entry
        assert "timestamp" in entry

def test_alert_monitor_status_and_trigger(client: TestClient):
    """Verifies the background alert monitor status and manual cycle trigger."""
    # Check status
    stat_resp = client.get("/api/v1/alerts/monitor/status")
    assert stat_resp.status_code == 200
    stat_data = stat_resp.json()
    assert "is_running" in stat_data
    assert "interval_seconds" in stat_data

    # Manual trigger
    trig_resp = client.post("/api/v1/alerts/monitor/trigger")
    assert trig_resp.status_code == 200
    trig_data = trig_resp.json()
    assert "success" in trig_data
    assert trig_data["success"] is True

def test_notification_service_fallback():
    """Verifies that notification service falls back safely without raising errors when unconfigured."""
    dummy_alert = alert_classifier.classify_flood(
        lat=30.0, lon=-90.0, location_name="Test Basin", discharge_m3s=500.0, anomaly_ratio=3.0
    )
    alert_item, _ = alert_manager.create_or_update_alert(dummy_alert)
    
    # Run notification asynchronously (should report NOT_CONFIGURED or SENT)
    import asyncio
    result = asyncio.run(notification_service.notify_alert(alert_item))
    assert result["status"] in ["NOT_CONFIGURED", "SENT", "SUPPRESSED_DEDUP"]

