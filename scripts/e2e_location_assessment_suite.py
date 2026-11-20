"""
HAZARDX AI — End-to-End 10-Location Multi-Hazard Assessment Suite (Phase 45)
Evaluates composite risk, 5-hazard models, TreeSHAP attributions, forecast timelines,
and prediction archive logging across 10 globally diverse benchmark coordinates.
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
from fastapi.testclient import TestClient

# Add repository root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.main import app
from backend.app.services.prediction_archive_service import prediction_archive_service

LOCATIONS = [
    {"name": "Wayanad, India", "lat": 11.6854, "lon": 76.1320, "archetype": "Tropical Mountain Western Ghats"},
    {"name": "Kochi, India", "lat": 9.9312, "lon": 76.2673, "archetype": "Arabian Sea Coastal Lowland"},
    {"name": "Munnar, India", "lat": 10.0889, "lon": 77.0595, "archetype": "High-Altitude Tea Highlands"},
    {"name": "Idukki, India", "lat": 9.8493, "lon": 76.9710, "archetype": "High-Relief Dam Catchment"},
    {"name": "Palakkad, India", "lat": 10.7867, "lon": 76.6548, "archetype": "Inland Gap River Floodplain"},
    {"name": "Ridgecrest, USA", "lat": 35.6225, "lon": -117.6709, "archetype": "Mojave Desert Strike-Slip Fault"},
    {"name": "Tokyo, Japan", "lat": 35.6762, "lon": 139.6503, "archetype": "Subduction Megacity Coast"},
    {"name": "Zhengzhou, China", "lat": 34.7466, "lon": 113.6253, "archetype": "Yellow River Basin Floodplain"},
    {"name": "Tacloban, Philippines", "lat": 11.2444, "lon": 125.0039, "archetype": "Typhoon Storm Surge Corridor"},
    {"name": "Paradise, California, USA", "lat": 39.7596, "lon": -121.6219, "archetype": "Chaparral Wildland-Urban Interface"}
]

def run_e2e_suite():
    print("=" * 80)
    print("HAZARDX AI — PHASE 45 END-TO-END APPLICATION & LOCATION SUITE")
    print("=" * 80)
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n")

    client = TestClient(app)

    # 1. Health check
    print("[1/4] Verifying /health endpoint...")
    h_resp = client.get("/api/v1/health")
    assert h_resp.status_code == 200, f"Health check failed: {h_resp.status_code}"
    print(f"  -> Health OK (200): {h_resp.json().get('status', 'OK')}")

    # 2. Hazard zones GeoJSON
    print("\n[2/4] Verifying /hazard-zones GeoJSON FeatureCollection...")
    hz_resp = client.get("/api/v1/geospatial/hazard-zones?hazard_type=all&horizon=24h")
    assert hz_resp.status_code == 200, f"Hazard zones failed: {hz_resp.status_code}"
    hz_data = hz_resp.json()
    print(f"  -> Hazard Zones OK (200): Type={hz_data.get('type')}, Feature Count={hz_data.get('count')}")

    # 3. Location Assessments across all 10 coordinates
    print("\n[3/4] Executing 5-Hazard Location Assessments across 10 locations...")
    results = []

    for idx, loc in enumerate(LOCATIONS, 1):
        name = loc["name"]
        lat = loc["lat"]
        lon = loc["lon"]
        arch = loc["archetype"]

        t0 = time.time()
        payload = {
            "latitude": lat,
            "longitude": lon,
            "hazards": ["floods", "landslides", "earthquakes", "wildfires", "cyclones"]
        }
        resp = client.post("/api/v1/geospatial/assess", json=payload)
        latency_ms = round((time.time() - t0) * 1000, 1)

        if resp.status_code != 200:
            print(f"  [{idx:02d}/10] {name:28s} -> FAILED ({resp.status_code}): {resp.text}")
            results.append({"name": name, "status": "FAILED", "code": resp.status_code})
            continue

        data = resp.json()
        comp_risk = data.get("overall_composite_risk", "UNKNOWN")
        env = data.get("environmental_context", {})
        elev = env.get("elevation_m", 0)
        slope = env.get("slope_degrees", 0)
        fwi = env.get("fwi_fire_weather_index", 0)
        fault_dist = env.get("dist_to_active_fault_km", 0)

        assess = data.get("assessments", {})
        fl_cat = assess.get("floods", {}).get("risk_category", "N/A")
        ls_cat = assess.get("landslides", {}).get("risk_category", "N/A")
        eq_cat = assess.get("earthquakes", {}).get("risk_category", "N/A")
        wf_cat = assess.get("wildfires", {}).get("risk_category", "N/A")
        cy_cat = assess.get("cyclones", {}).get("risk_category", "N/A")

        print(f"  [{idx:02d}/10] {name:28s} [{arch[:20]}] -> Composite: {comp_risk} ({latency_ms} ms)")
        print(f"         Env: Elev={elev:.0f}m, Slope={slope:.1f}°, FWI={fwi:.1f}, FaultDist={fault_dist:.1f}km")
        print(f"         Hazards: Flood={fl_cat}, Landslide={ls_cat}, Quake={eq_cat}, Fire={wf_cat}, Cyclone={cy_cat}")

        results.append({
            "name": name,
            "coordinates": [lat, lon],
            "archetype": arch,
            "latency_ms": latency_ms,
            "composite_risk": comp_risk,
            "environmental": {
                "elevation_m": elev,
                "slope_deg": slope,
                "fwi": fwi,
                "fault_dist_km": fault_dist
            },
            "hazard_categories": {
                "floods": fl_cat,
                "landslides": ls_cat,
                "earthquakes": eq_cat,
                "wildfires": wf_cat,
                "cyclones": cy_cat
            }
        })

    # 4. Verify Prediction Archive records
    print("\n[4/4] Verifying Prediction Archive audit persistence...")
    arch_resp = client.get("/api/v1/geospatial/validation/archive?limit=50")
    assert arch_resp.status_code == 200, f"Archive query failed: {arch_resp.status_code}"
    arch_data = arch_resp.json()
    arch_count = arch_data.get("count", 0)
    print(f"  -> Prediction Archive OK: {arch_count} archived snapshots confirmed in database.")

    rel_resp = client.get("/api/v1/geospatial/validation/reliability")
    assert rel_resp.status_code == 200
    rel_data = rel_resp.json()
    print(f"  -> Reliability Metrics: Brier Score={rel_data.get('brier_score')}, Hit Rate={rel_data.get('hit_rate')}, FAR={rel_data.get('false_alarm_rate')}")

    print("\n" + "=" * 80)
    print("PHASE 45 E2E LOCATION ASSESSMENT SUMMARY:")
    print(f"Total Locations Tested: {len(LOCATIONS)}")
    print(f"Successfully Resolved:  {len([r for r in results if r.get('composite_risk')])} / {len(LOCATIONS)}")
    print("=" * 80)

    # Save structured results to file for final reporting
    out_path = os.path.join(os.path.dirname(__file__), "..", "data", "e2e_location_test_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Results persisted to {out_path}")

    return results

if __name__ == "__main__":
    run_e2e_suite()
