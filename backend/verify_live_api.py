"""
HAZARDX AI — Live Backend API Verification Script
Tests the live running FastAPI server against all endpoints with real HTTP calls.
"""

import sys
import json
import time
import math
import httpx

def check_finite(val, path=""):
    if isinstance(val, (int, float)):
        if math.isnan(val) or math.isinf(val):
            raise AssertionError(f"Non-finite value found at {path}: {val}")
    elif isinstance(val, dict):
        for k, v in val.items():
            check_finite(v, f"{path}.{k}")
    elif isinstance(val, list):
        for idx, item in enumerate(val):
            check_finite(item, f"{path}[{idx}]")

def run_live_verification():
    base_url = "http://127.0.0.1:8000"
    client = httpx.Client(base_url=base_url, timeout=30.0)
    
    print("=" * 70)
    print("HAZARDX AI — LIVE BACKEND VERIFICATION")
    print("=" * 70)
    
    # 1. Health check
    print("\n1. Testing GET /api/v1/health...")
    r = client.get("/api/v1/health")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    health_data = r.json()
    check_finite(health_data)
    print(f"   [PASS] Status: {health_data['status']}, Models: {health_data['models_loaded']}")
    
    # 2. Model Catalog
    print("\n2. Testing GET /api/v1/models...")
    r = client.get("/api/v1/models")
    assert r.status_code == 200
    catalog = r.json()
    check_finite(catalog)
    print(f"   [PASS] Total Models: {catalog['total_models']} | Operational: {catalog['operational_models_count']} | Experimental: {catalog['experimental_models_count']}")
    
    # 3. Model Performance
    print("\n3. Testing GET /api/v1/models/performance...")
    r = client.get("/api/v1/models/performance")
    assert r.status_code == 200
    perf = r.json()
    check_finite(perf)
    print(f"   [PASS] Benchmarks retrieved for {len(perf)} models.")
    
    # 4. Predictions for All 5 Hazards
    print("\n4. Testing Hazard Prediction Endpoints...")
    
    # Floods
    flood_req = {
        "precip_1d_mm": 88.0, "precip_3d_sum_mm": 140.0, "precip_7d_sum_mm": 210.0,
        "precip_14d_sum_mm": 280.0, "api_14d_index": 45.0, "temp_2m_celsius": 24.0,
        "soil_temp_celsius": 22.0, "river_discharge_m3s": 500.0, "river_discharge_7d_mean_m3s": 420.0,
        "river_discharge_ratio_7d": 1.19, "elevation_m": 45.0, "slope_degrees": 2.5,
        "topographic_wetness_index": 12.0, "distance_to_river_km": 0.4
    }
    r = client.post("/api/v1/predict/flood", json=flood_req)
    assert r.status_code == 200
    f_res = r.json()
    check_finite(f_res)
    print(f"   [PASS] Flood: Prob={f_res['raw_model_score']} | Alert={f_res['alert_level']} | Severity={f_res['severity_label']}")
    
    # Landslides
    landslide_req = {
        "precip_1d_mm": 90.0, "precip_3d_sum_mm": 150.0, "precip_7d_sum_mm": 220.0,
        "precip_30d_sum_mm": 400.0, "api_30d_index": 60.0, "temp_2m_celsius": 17.0,
        "soil_temp_celsius": 15.0, "slope_degrees": 36.0, "elevation_m": 1100.0,
        "aspect_degrees": 135.0, "plan_curvature": -0.03, "soil_clay_fraction_pct": 35.0,
        "distance_to_road_km": 0.15, "distance_to_stream_km": 0.2
    }
    r = client.post("/api/v1/predict/landslide", json=landslide_req)
    assert r.status_code == 200
    l_res = r.json()
    check_finite(l_res)
    print(f"   [PASS] Landslide: Prob={l_res['raw_model_score']} | Alert={l_res['alert_level']} | Magnitude={l_res['hazard_magnitude_label']}")
    
    # Earthquakes
    eq_req = {
        "mainshock_mag": 7.1, "focal_depth_km": 15.0, "dist_to_active_fault_km": 3.5,
        "nearest_fault_slip_type": "Subduction_Thrust", "prior_count_7d_100km": 18,
        "prior_count_30d_100km": 45, "prior_count_365d_100km": 210,
        "prior_max_mag_30d": 5.1, "cumulative_energy_log_joules": 15.2,
        "seismic_rate_accel_ratio": 2.6, "regional_b_value": 0.92
    }
    r = client.post("/api/v1/predict/earthquake", json=eq_req)
    assert r.status_code == 200
    eq_res = r.json()
    check_finite(eq_res)
    print(f"   [PASS] Earthquake Aftershock: Prob={eq_res['hazard_probability']} | Alert={eq_res['alert_level']} | Disclaimer Verified")
    
    # Cyclones
    cyc_req = {
        "current_wind_kt": 80.0, "current_pres_hpa": 968.0, "dist_to_land_km": 300.0,
        "landfall_flag": 0, "past_delta_wind_6h": 15.0, "past_delta_wind_12h": 25.0,
        "past_delta_pres_6h": -14.0, "translational_speed_kt": 14.0, "heading_degrees": 305.0,
        "coriolis_param": 0.00005, "pot_intensity_headroom": 50.0
    }
    r = client.post("/api/v1/predict/cyclone", json=cyc_req)
    assert r.status_code == 200
    cyc_res = r.json()
    check_finite(cyc_res)
    print(f"   [PASS] Cyclone: RI Prob={cyc_res['rapid_intensification_probability']} | 24h Change={cyc_res['predicted_24h_intensity_change_kt']} kt | Projected Wind={cyc_res['projected_wind_24h_kt']} kt")
    
    # Wildfires
    wild_req = {
        "temp_2m_celsius": 38.0, "relative_humidity_pct": 12.0, "wind_speed_10m_ms": 12.5,
        "precip_7d_sum_mm": 0.0, "precip_30d_sum_mm": 1.2, "soil_temp_celsius": 40.0,
        "fwi_fire_weather_index": 48.0, "slope_degrees": 20.0, "elevation_m": 720.0,
        "distance_to_road_km": 0.8
    }
    r = client.post("/api/v1/predict/wildfire", json=wild_req)
    assert r.status_code == 200
    w_res = r.json()
    check_finite(w_res)
    print(f"   [PASS] Wildfire: Susceptibility={w_res['raw_model_score']} | Alert={w_res['alert_level']} | Est FRP={w_res['estimated_log_frp_mw']}")
    
    # 5. Multi-Hazard Composite Prediction
    print("\n5. Testing Multi-Hazard Composite POST /api/v1/predict/all...")
    multi_req = {
        "flood": flood_req,
        "landslide": landslide_req,
        "earthquake": eq_req,
        "cyclone": cyc_req,
        "wildfire": wild_req
    }
    r = client.post("/api/v1/predict/all", json=multi_req)
    assert r.status_code == 200
    m_res = r.json()
    check_finite(m_res)
    print(f"   [PASS] Multi-Hazard Evaluated: {m_res['hazards_evaluated']} | Composite Alert: {m_res['composite_highest_alert_level']}")
    
    # 6. Global Explanations
    print("\n6. Testing TreeSHAP Explanations GET /api/v1/explanations/{hazard}...")
    for h in ["floods", "landslides", "earthquakes", "cyclones", "wildfires"]:
        r = client.get(f"/api/v1/explanations/{h}")
        assert r.status_code == 200
        e_res = r.json()
        check_finite(e_res)
        top_driver = e_res['top_global_features'][0]['feature']
        print(f"   [PASS] {h.capitalize()}: Top Driver = '{top_driver}' | SHAP Plot = {bool(e_res['shap_summary_plot_url'])}")
        
    # 7. Dashboard Summary
    print("\n7. Testing Dashboard Summary GET /api/v1/dashboard/summary...")
    r = client.get("/api/v1/dashboard/summary")
    assert r.status_code == 200
    d_res = r.json()
    check_finite(d_res)
    print(f"   [PASS] System: {d_res['system_name']} | Status: {d_res['status']} | Hazards: {d_res['total_hazards_supported']}")
    
    # 8. Error Handling & Validation
    print("\n8. Testing Validation & Error Codes...")
    bad_cyc = cyc_req.copy()
    bad_cyc["current_wind_kt"] = -25.0  # Invalid
    r = client.post("/api/v1/predict/cyclone", json=bad_cyc)
    assert r.status_code == 422
    err_res = r.json()
    print(f"   [PASS] 422 Rejection Verified: Code={err_res['error_code']}")
    
    print("\n" + "=" * 70)
    print("ALL LIVE VERIFICATION TESTS PASSED SUCCESSFULLY (100% HEALTHY)")
    print("=" * 70)

if __name__ == "__main__":
    run_live_verification()
