"""
HAZARDX AI — Frontend & Backend Integration Verification Script
Tests that the Vite frontend web server and FastAPI backend communicate properly.
"""

import sys
import httpx

def verify():
    print("=" * 70)
    print("HAZARDX AI — FRONTEND & BACKEND INTEGRATION TEST SUITE")
    print("=" * 70)
    
    frontend_url = "http://localhost:5173"
    backend_url = "http://127.0.0.1:8000/api/v1"
    
    # 1. Test Frontend Root
    print("\n1. Testing Frontend HTTP Service (http://localhost:5173)...")
    try:
        r = httpx.get(frontend_url, timeout=5.0)
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        assert '<div id="root"></div>' in r.text, "Root element missing from HTML"
        assert 'HAZARDX AI' in r.text, "Title missing from HTML"
        print(f"   [PASS] Frontend serving index.html ({len(r.text)} bytes)")
    except Exception as e:
        print(f"   [FAIL] Could not connect to frontend: {e}")
        sys.exit(1)
        
    # 2. Test Backend Health Connection from Frontend Perspective
    print("\n2. Testing Backend Health (/api/v1/health)...")
    try:
        r = httpx.get(f"{backend_url}/health", timeout=5.0)
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "healthy"
        assert data["models_loaded"] == 12
        print(f"   [PASS] Backend reports {data['models_loaded']} models loaded, status: {data['status']}")
    except Exception as e:
        print(f"   [FAIL] Backend health check failed: {e}")
        sys.exit(1)

    # 3. Test Model Catalog & Performance
    print("\n3. Testing Model Catalog & Governance (/api/v1/models)...")
    r = httpx.get(f"{backend_url}/models", timeout=5.0)
    assert r.status_code == 200
    catalog = r.json()
    assert catalog["total_models"] == 12
    assert catalog["operational_models_count"] == 8
    print(f"   [PASS] 12 models in catalog (8 Operational, 2 Experimental, 2 Blocked)")

    # 4. Test Flood Module Integration
    print("\n4. Testing Flood Module POST /predict/flood...")
    flood_payload = {
        "precip_1d_mm": 88.5, "precip_3d_sum_mm": 145.0, "precip_7d_sum_mm": 215.0,
        "precip_14d_sum_mm": 290.0, "api_14d_index": 45.2, "temp_2m_celsius": 24.0,
        "soil_temp_celsius": 22.5, "river_discharge_m3s": 520.0, "river_discharge_7d_mean_m3s": 430.0,
        "river_discharge_ratio_7d": 1.21, "elevation_m": 42.0, "slope_degrees": 2.2,
        "topographic_wetness_index": 12.1, "distance_to_river_km": 0.35
    }
    r = httpx.post(f"{backend_url}/predict/flood", json=flood_payload, timeout=5.0)
    assert r.status_code == 200
    f_res = r.json()
    assert "raw_model_score" in f_res
    assert len(f_res["important_contributing_features"]) > 0
    print(f"   [PASS] Flood prediction verified: Prob={f_res['raw_model_score']} | Alert={f_res['alert_level']} | TreeSHAP={len(f_res['important_contributing_features'])} drivers")

    # 5. Test Landslide Module Integration
    print("\n5. Testing Landslide Module POST /predict/landslide...")
    landslide_payload = {
        "precip_1d_mm": 95.0, "precip_3d_sum_mm": 165.0, "precip_7d_sum_mm": 245.0,
        "precip_30d_sum_mm": 430.0, "api_30d_index": 68.0, "temp_2m_celsius": 18.0,
        "soil_temp_celsius": 16.5, "slope_degrees": 36.5, "elevation_m": 1250.0,
        "aspect_degrees": 140.0, "plan_curvature": -0.045, "soil_clay_fraction_pct": 38.0,
        "distance_to_road_km": 0.12, "distance_to_stream_km": 0.22
    }
    r = httpx.post(f"{backend_url}/predict/landslide", json=landslide_payload, timeout=5.0)
    assert r.status_code == 200
    l_res = r.json()
    assert "hazard_magnitude_label" in l_res
    print(f"   [PASS] Landslide prediction verified: Prob={l_res['raw_model_score']} | Alert={l_res['alert_level']} | Magnitude={l_res['hazard_magnitude_label']}")

    # 6. Test Earthquake Module Integration & Disclaimers
    print("\n6. Testing Earthquake Module POST /predict/earthquake...")
    eq_payload = {
        "mainshock_mag": 7.0, "focal_depth_km": 10.0, "dist_to_active_fault_km": 1.5,
        "nearest_fault_slip_type": "Strike-Slip", "prior_count_7d_100km": 22,
        "prior_count_30d_100km": 55, "prior_count_365d_100km": 240,
        "prior_max_mag_30d": 6.2, "cumulative_energy_log_joules": 15.1,
        "seismic_rate_accel_ratio": 2.8, "regional_b_value": 0.88
    }
    r = httpx.post(f"{backend_url}/predict/earthquake", json=eq_payload, timeout=5.0)
    assert r.status_code == 200
    eq_res = r.json()
    assert "NOT an exact earthquake prediction" in eq_res["disclaimer"]
    assert eq_res["estimated_aftershock_count"] is None
    print(f"   [PASS] Earthquake aftershock hazard verified: Prob={eq_res['hazard_probability']} | Disclaimer Enforced | Count Blocked")

    # 7. Test Cyclone Module Integration
    print("\n7. Testing Cyclone Module POST /predict/cyclone...")
    cyc_payload = {
        "current_wind_kt": 80.0, "current_pres_hpa": 968.0, "dist_to_land_km": 280.0,
        "landfall_flag": 0, "past_delta_wind_6h": 15.0, "past_delta_wind_12h": 25.0,
        "past_delta_pres_6h": -14.0, "translational_speed_kt": 14.0, "heading_degrees": 310.0,
        "coriolis_param": 0.000065, "pot_intensity_headroom": 55.0
    }
    r = httpx.post(f"{backend_url}/predict/cyclone", json=cyc_payload, timeout=5.0)
    assert r.status_code == 200
    cyc_res = r.json()
    assert "rapid_intensification_probability" in cyc_res
    print(f"   [PASS] Cyclone forecast verified: RI Prob={cyc_res['rapid_intensification_probability']} | Wind Delta={cyc_res['predicted_24h_intensity_change_kt']} kt")

    # 8. Test Wildfire Module Integration
    print("\n8. Testing Wildfire Module POST /predict/wildfire...")
    wild_payload = {
        "temp_2m_celsius": 38.0, "relative_humidity_pct": 9.5, "wind_speed_10m_ms": 14.0,
        "precip_7d_sum_mm": 0.0, "precip_30d_sum_mm": 1.0, "soil_temp_celsius": 40.0,
        "fwi_fire_weather_index": 54.0, "slope_degrees": 22.0, "elevation_m": 680.0,
        "distance_to_road_km": 0.7
    }
    r = httpx.post(f"{backend_url}/predict/wildfire", json=wild_payload, timeout=5.0)
    assert r.status_code == 200
    w_res = r.json()
    assert w_res["estimated_duration_days"] is None
    print(f"   [PASS] Wildfire assessment verified: Susceptibility={w_res['raw_model_score']} | Alert={w_res['alert_level']} | Duration Blocked")

    # 9. Test Unified Multi-Hazard Assessment
    print("\n9. Testing Multi-Hazard Composite POST /predict/all...")
    multi_payload = {
        "flood": flood_payload,
        "landslide": landslide_payload,
        "cyclone": cyc_payload
    }
    r = httpx.post(f"{backend_url}/predict/all", json=multi_payload, timeout=5.0)
    assert r.status_code == 200
    m_res = r.json()
    assert m_res["composite_highest_alert_level"] in ["GREEN", "YELLOW", "ORANGE", "RED"]
    print(f"   [PASS] Multi-hazard composite verified: Composite Alert={m_res['composite_highest_alert_level']} | Evaluated: {m_res['hazards_evaluated']}")

    print("\n" + "=" * 70)
    print("ALL FRONTEND & BACKEND INTEGRATION CHECKS PASSED (100% HEALTHY)")
    print("=" * 70)

if __name__ == "__main__":
    verify()

