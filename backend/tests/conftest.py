"""
HAZARDX AI — Pytest Fixtures & Shared Test Configuration
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def valid_flood_payload():
    return {
        "precip_1d_mm": 85.5,
        "precip_3d_sum_mm": 145.0,
        "precip_7d_sum_mm": 210.0,
        "precip_14d_sum_mm": 290.0,
        "api_14d_index": 42.5,
        "temp_2m_celsius": 22.0,
        "soil_temp_celsius": 20.5,
        "river_discharge_m3s": 450.0,
        "river_discharge_7d_mean_m3s": 380.0,
        "river_discharge_ratio_7d": 1.18,
        "elevation_m": 35.0,
        "slope_degrees": 2.1,
        "topographic_wetness_index": 11.2,
        "distance_to_river_km": 0.35
    }

@pytest.fixture
def valid_landslide_payload():
    return {
        "precip_1d_mm": 95.0,
        "precip_3d_sum_mm": 160.0,
        "precip_7d_sum_mm": 240.0,
        "precip_30d_sum_mm": 420.0,
        "api_30d_index": 65.0,
        "temp_2m_celsius": 18.0,
        "soil_temp_celsius": 16.5,
        "slope_degrees": 34.5,
        "elevation_m": 1200.0,
        "aspect_degrees": 145.0,
        "plan_curvature": -0.04,
        "soil_clay_fraction_pct": 38.5,
        "distance_to_road_km": 0.12,
        "distance_to_stream_km": 0.25
    }

@pytest.fixture
def valid_earthquake_payload():
    return {
        "mainshock_mag": 6.8,
        "focal_depth_km": 12.0,
        "dist_to_active_fault_km": 4.2,
        "nearest_fault_slip_type": "Strike-Slip",
        "prior_count_7d_100km": 14,
        "prior_count_30d_100km": 38,
        "prior_count_365d_100km": 180,
        "prior_max_mag_30d": 4.5,
        "cumulative_energy_log_joules": 14.8,
        "seismic_rate_accel_ratio": 2.4,
        "regional_b_value": 0.95
    }

@pytest.fixture
def valid_cyclone_payload():
    return {
        "current_wind_kt": 75.0,
        "current_pres_hpa": 972.0,
        "dist_to_land_km": 240.0,
        "landfall_flag": 0,
        "past_delta_wind_6h": 15.0,
        "past_delta_wind_12h": 25.0,
        "past_delta_pres_6h": -12.0,
        "translational_speed_kt": 12.0,
        "heading_degrees": 290.0,
        "coriolis_param": 0.000045,
        "pot_intensity_headroom": 45.0
    }

@pytest.fixture
def valid_wildfire_payload():
    return {
        "temp_2m_celsius": 36.5,
        "relative_humidity_pct": 14.0,
        "wind_speed_10m_ms": 11.5,
        "precip_7d_sum_mm": 0.0,
        "precip_30d_sum_mm": 2.5,
        "soil_temp_celsius": 38.0,
        "fwi_fire_weather_index": 42.0,
        "slope_degrees": 18.0,
        "elevation_m": 650.0,
        "distance_to_road_km": 1.2
    }

