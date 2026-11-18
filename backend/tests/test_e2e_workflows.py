"""
HAZARDX AI — Complete End-to-End System Validation Suite (Workflows A - F)
==========================================================================
Verifies full operational workflows across all five natural hazards:
  - Workflow A: Earthquake (USGS ingest -> aftershock hazard ML -> alert generation -> acknowledgement)
  - Workflow B: Wildfire (FIRMS ingest -> fire weather susceptibility ML -> alert escalation -> resolution)
  - Workflow C: Flood (Hydrological discharge -> flood occurrence ML -> alert deduplication & clustering)
  - Workflow D: Landslide (Slope & rainfall -> geotechnical susceptibility ML -> advisory guidance)
  - Workflow E: Cyclone (Storm track -> intensity & rapid intensification ML -> hurricane warning)
  - Workflow F: Multi-Hazard Integration (/geospatial/assess multi-hazard synthesis & composite alert)
"""

import time
import pytest
from fastapi.testclient import TestClient
from backend.app.alerts.alert_classifier import alert_classifier
from backend.app.alerts.alert_manager import alert_manager

def test_workflow_a_earthquake_aftershock_e2e(client: TestClient, valid_earthquake_payload):
    """
    Workflow A: Ingests USGS earthquake feed, evaluates regional aftershock hazard,
    generates decision-support alert, and executes acknowledgement lifecycle.
    """
    # 1. Ingest / inspect live USGS earthquake feed
    live_res = client.get("/api/v1/live/earthquakes?min_magnitude=3.0&limit=5")
    assert live_res.status_code == 200
    live_data = live_res.json()
    assert live_data["hazard_type"] == "earthquakes"
    assert "USGS" in live_data["source_attribution"]

    # 2. Evaluate Regional Aftershock Hazard via ML
    # Note: Strictly regional aftershock hazard assessment, NOT exact earthquake prediction.
    eq_payload = dict(valid_earthquake_payload)
    pred_res = client.post("/api/v1/predict/earthquake", json=eq_payload)
    assert pred_res.status_code == 200
    pred = pred_res.json()
    assert pred["hazard_name"] == "Earthquakes"
    assert "hazard_probability" in pred
    assert pred["alert_level"] in ["GREEN", "YELLOW", "RED"]
    assert "NOT an exact earthquake prediction" in pred["disclaimer"]
    # Operational governance verification: count model blocked
    assert pred["estimated_aftershock_count"] is None

    # 3. Create Alert via Alert Classifier & Manager
    import time
    alert_dict = alert_classifier.classify_earthquake(
        lat=35.0,
        lon=-118.0,
        location_name="Southern California Fault Zone",
        magnitude=eq_payload["mainshock_mag"],
        depth_km=eq_payload["focal_depth_km"],
        dist_fault_km=eq_payload["dist_to_active_fault_km"],
        aftershock_prob=pred["hazard_probability"]
    )
    alert_dict["dedup_key"] = f"eq_test_a_{time.time()}"
    alert_item, is_new = alert_manager.create_or_update_alert(alert_dict)
    alert_id = alert_item.alert_id
    assert alert_id.startswith("alt_")
    assert alert_item.status == "ACTIVE"

    # 4. Verify Alert Retrieval via API
    get_res = client.get(f"/api/v1/alerts/{alert_id}")
    assert get_res.status_code == 200
    assert get_res.json()["alert_id"] == alert_id

    # 5. Acknowledge Alert (Duty Officer Action)
    ack_res = client.post(
        f"/api/v1/alerts/{alert_id}/acknowledge",
        json={"acknowledged_by": "Senior Seismologist Chen", "notes": "USGS shake-map and fault stress verified."}
    )
    assert ack_res.status_code == 200
    acked = ack_res.json()
    assert acked["status"] == "ACKNOWLEDGED"
    assert acked["acknowledged_by"] == "Senior Seismologist Chen"

    # 6. Audit Trail Verification
    history_res = client.get(f"/api/v1/alerts/history?alert_id={alert_id}")
    assert history_res.status_code == 200
    history = history_res.json()
    assert len(history) >= 2  # GENERATED/CREATED and ACKNOWLEDGED actions
    assert any("ACKNOWLEDGE" in h["action_type"] for h in history)


def test_workflow_b_wildfire_susceptibility_e2e(client: TestClient, valid_wildfire_payload):
    """
    Workflow B: Ingests NASA FIRMS active fire detections, evaluates wildfire ignition
    and spread susceptibility under extreme fire weather, and resolves the incident.
    """
    # 1. Ingest / check live NASA FIRMS active fires
    wf_live = client.get("/api/v1/live/wildfires?limit=5")
    assert wf_live.status_code == 200
    wf_data = wf_live.json()
    assert wf_data["hazard_type"] == "wildfires"
    assert "NASA FIRMS" in wf_data["source_attribution"]

    # 2. Predict Wildfire Susceptibility with Extreme Fire Weather
    wf_payload = dict(valid_wildfire_payload)
    wf_payload["temp_2m_celsius"] = 39.0
    wf_payload["relative_humidity_pct"] = 10.0
    wf_payload["wind_speed_10m_ms"] = 15.0
    wf_payload["fwi_fire_weather_index"] = 48.0

    wf_res = client.post("/api/v1/predict/wildfire", json=wf_payload)
    assert wf_res.status_code == 200
    wf_pred = wf_res.json()
    assert wf_pred["hazard_name"] == "Wildfires"
    assert wf_pred["wildfire_susceptibility_predicted"] is True
    assert wf_pred["risk_category"] in ["HIGH", "SEVERE_CRITICAL", "MODERATE"]
    assert wf_pred["alert_level"] in ["ORANGE", "RED"]
    # Operational governance verification: duration blocked
    assert wf_pred["estimated_duration_days"] is None

    # 3. Create Alert via Alert Classifier & Manager
    alert_dict = alert_classifier.classify_wildfire(
        lat=39.75,
        lon=-121.58,
        location_name="Sierra Nevada Foothills",
        frp_mw=95.0,
        brightness_k=365.0,
        fwi=wf_payload["fwi_fire_weather_index"],
        wind_ms=wf_payload["wind_speed_10m_ms"],
        model_score=wf_pred["calibrated_susceptibility_score"]
    )
    alert_dict["dedup_key"] = f"wf_test_b_{time.time()}"
    alert_item, is_new = alert_manager.create_or_update_alert(alert_dict)
    alert_id = alert_item.alert_id

    # 4. Resolve Alert via API
    res_res = client.post(
        f"/api/v1/alerts/{alert_id}/resolve",
        json={"resolved_by": "Incident Commander Alvarez", "resolution_notes": "Front passed, humidity increased to 65%."}
    )
    assert res_res.status_code == 200
    resolved = res_res.json()
    assert resolved["status"] == "RESOLVED"
    assert resolved["resolved_by"] == "Incident Commander Alvarez"


def test_workflow_c_flood_deduplication_e2e(client: TestClient, valid_flood_payload):
    """
    Workflow C: Ingests GloFAS hydrological streamflow, evaluates flood occurrence ML,
    and validates spatial-temporal deduplication and escalation.
    """
    # 1. Query GloFAS flood discharge feed
    flood_live = client.get("/api/v1/live/floods?lat=29.95&lon=-90.07&location_name=Mississippi%20River")
    assert flood_live.status_code == 200
    assert "current_discharge_m3s" in flood_live.json()

    # 2. Evaluate Flood Model for Monsoon High-Discharge Basin
    flood_payload = dict(valid_flood_payload)
    flood_payload["precip_1d_mm"] = 125.0
    flood_payload["precip_3d_sum_mm"] = 240.0
    flood_payload["river_discharge_m3s"] = 1200.0

    flood_res = client.post("/api/v1/predict/flood", json=flood_payload)
    assert flood_res.status_code == 200
    flood_pred = flood_res.json()
    assert flood_pred["hazard_name"] == "Floods"
    assert flood_pred["flood_occurrence_predicted"] is True
    assert flood_pred["alert_level"] in ["ORANGE", "RED"]

    # 3. Create Initial Alert (YELLOW / ORANGE)
    import time
    dedup_shared_key = f"flood_test_c_{time.time()}"
    base_lat = 25.0
    base_lon = 85.0

    alert_dict_1 = alert_classifier.classify_flood(
        lat=base_lat,
        lon=base_lon,
        location_name="Assam River Basin",
        discharge_m3s=850.0,
        anomaly_ratio=1.6,
        precip_1d_mm=55.0,
        model_score=0.65
    )
    alert_dict_1["dedup_key"] = dedup_shared_key
    alert_item_1, is_new_1 = alert_manager.create_or_update_alert(alert_dict_1)
    assert is_new_1 is True
    alert_1_id = alert_item_1.alert_id

    # 4. Ingest Escalated Severe Observation in Same 0.25 deg Grid Cell (< 12 hours)
    alert_dict_2 = alert_classifier.classify_flood(
        lat=base_lat + 0.03,  # ~3 km shift within same 0.25 deg cell
        lon=base_lon + 0.03,
        location_name="Assam River Basin - Downstream",
        discharge_m3s=1450.0,
        anomaly_ratio=3.2,
        precip_1d_mm=135.0,
        model_score=0.92
    )
    alert_dict_2["dedup_key"] = dedup_shared_key
    alert_item_2, is_new_2 = alert_manager.create_or_update_alert(alert_dict_2)
    
    # Must deduplicate to the same alert_id and escalate severity to RED
    assert is_new_2 is False
    assert alert_item_2.alert_id == alert_1_id
    assert alert_item_2.severity == "RED"


def test_workflow_d_landslide_susceptibility_e2e(client: TestClient, valid_landslide_payload):
    """
    Workflow D: Ingests NASA GLC landslide inventory, assesses geotechnical slope
    stability under heavy antecedent monsoon rains, and validates SHAP feature attribution.
    """
    # 1. Query live/recent landslides feed
    ls_live = client.get("/api/v1/live/landslides?limit=5")
    assert ls_live.status_code == 200
    assert ls_live.json()["hazard_type"] == "landslides"

    # 2. Evaluate Landslide ML
    ls_payload = dict(valid_landslide_payload)
    ls_payload["precip_1d_mm"] = 110.0
    ls_payload["precip_3d_sum_mm"] = 195.0
    ls_payload["slope_degrees"] = 42.0

    ls_res = client.post("/api/v1/predict/landslide", json=ls_payload)
    assert ls_res.status_code == 200
    ls_pred = ls_res.json()
    assert ls_pred["hazard_name"] == "Landslides"
    assert ls_pred["landslide_occurrence_predicted"] is True
    assert ls_pred["alert_level"] in ["ORANGE", "RED"]
    assert len(ls_pred["important_contributing_features"]) >= 3


def test_workflow_e_cyclone_intensity_rapid_intensification_e2e(client: TestClient, valid_cyclone_payload):
    """
    Workflow E: Evaluates tropical cyclone intensity and rapid intensification (RI)
    under high sea surface temperature and low vertical wind shear.
    """
    # 1. Query live cyclone tracking feed
    cyc_live = client.get("/api/v1/live/cyclones?active_only=false")
    assert cyc_live.status_code == 200
    assert cyc_live.json()["hazard_type"] == "cyclones"

    # 2. Evaluate Cyclone Dual Models (Intensity + Rapid Intensification)
    cyc_payload = dict(valid_cyclone_payload)
    cyc_payload["current_wind_kt"] = 105.0
    cyc_payload["current_pres_hpa"] = 948.0
    cyc_payload["pot_intensity_headroom"] = 55.0

    cyc_res = client.post("/api/v1/predict/cyclone", json=cyc_payload)
    assert cyc_res.status_code == 200
    cyc_pred = cyc_res.json()
    assert cyc_pred["hazard_name"] == "Cyclones"
    assert cyc_pred["alert_level"] in ["GREEN", "YELLOW", "RED"]
    assert "rapid_intensification_predicted" in cyc_pred
    assert "projected_wind_24h_kt" in cyc_pred

    # 3. Create Cyclone Alert
    alert_dict = alert_classifier.classify_cyclone(
        lat=19.5,
        lon=87.2,
        storm_name="Cyclone Biparjoy",
        intensity_kt=cyc_payload["current_wind_kt"],
        min_pres_hpa=cyc_payload["current_pres_hpa"],
        ri_prob=cyc_pred["rapid_intensification_probability"],
        delta_v_24h=cyc_pred["predicted_24h_intensity_change_kt"]
    )
    alert_item, is_new = alert_manager.create_or_update_alert(alert_dict)
    assert alert_item.alert_id.startswith("alt_")
    assert alert_item.hazard_type == "cyclones"


def test_workflow_f_multihazard_geospatial_synthesis_e2e(client: TestClient):
    """
    Workflow F: Evaluates composite multi-hazard risk assessment via /geospatial/assess
    for a high-risk geographic location, verifies independent models, and inspects alert metrics.
    """
    # 1. Evaluate Multi-Hazard Geospatial Assessment for San Francisco / Pacific Rim
    lat, lon = 37.7749, -122.4194
    assess_res = client.post("/api/v1/geospatial/assess", json={
        "latitude": lat,
        "longitude": lon,
        "hazards": ["floods", "landslides", "earthquakes", "wildfires", "cyclones"]
    })
    assert assess_res.status_code == 200
    assess_data = assess_res.json()
    assert assess_data["latitude"] == pytest.approx(lat, rel=1e-2)
    assert assess_data["longitude"] == pytest.approx(lon, rel=1e-2)
    assert "assessments" in assess_data
    assert len(assess_data["assessments"]) == 5
    assert assess_data["overall_composite_risk"] in ["GREEN", "YELLOW", "ORANGE", "RED"]

    # 2. Verify summary metrics reflect system state
    sum_res = client.get("/api/v1/alerts/summary")
    assert sum_res.status_code == 200
    summary = sum_res.json()
    assert "total_active" in summary
    assert "by_hazard" in summary
    assert "authentic scientific" in summary["data_policy"].lower()
