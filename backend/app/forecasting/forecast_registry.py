"""
HAZARDX AI — Forecasting Model Registry & Capability Directory
Defines operational metadata, validated forecast horizons, and governance policies
for all hazard forecasting pipelines.
"""

from typing import Dict, Any, List

FORECAST_REGISTRY = {
    "floods": {
        "pipeline_name": "Floods Multi-Horizon Hydrological Forecasting",
        "primary_model": "floods_flood_occurrence_xgboost",
        "secondary_model": "floods_flood_severity_xgboost",
        "supported_horizons": ["6h", "12h", "24h", "48h", "72h"],
        "governance_status": "OPERATIONAL",
        "data_feed": "Copernicus GloFAS & Open-Meteo Weather Forecast",
        "validated_metrics": {
            "test_pr_auc": 0.8156,
            "test_roc_auc": 0.7899,
            "test_brier_score": 0.1412
        },
        "scientific_basis": "Gridded LISFLOOD river discharge routing coupled with cumulative rainfall infiltration and Bayesian prior calibration."
    },
    "landslides": {
        "pipeline_name": "Landslides Precipitation-Infiltration Slope Forecaster",
        "primary_model": "landslides_landslide_occurrence_xgboost",
        "secondary_model": "landslides_landslide_magnitude_xgboost",
        "supported_horizons": ["6h", "12h", "24h", "48h", "72h"],
        "governance_status": "OPERATIONAL",
        "data_feed": "Open-Meteo High-Resolution Precipitation & Copernicus DEM",
        "validated_metrics": {
            "test_pr_auc": 0.8196,
            "test_roc_auc": 0.7496,
            "test_brier_score": 0.1583
        },
        "scientific_basis": "Empirical rainfall intensity-duration thresholds (Caine/Guzzetti) combined with geotechnical slope saturation and XGBoost susceptibility."
    },
    "wildfires": {
        "pipeline_name": "Wildfires Fire Weather & Ignition Danger Forecaster",
        "primary_model": "wildfires_wildfire_occurrence_xgboost",
        "secondary_model": "wildfires_frp_intensity_xgboost",
        "blocked_model": "wildfires_fire_duration_xgboost",
        "supported_horizons": ["6h", "12h", "24h", "48h", "72h"],
        "governance_status": "OPERATIONAL (Duration Model BLOCKED)",
        "data_feed": "Open-Meteo Atmospheric Forecast & NASA FIRMS Validation",
        "validated_metrics": {
            "occurrence_pr_auc": 0.8272,
            "occurrence_roc_auc": 0.8247,
            "duration_r2_blocked": -214.75
        },
        "scientific_basis": "Canadian/McArthur Fire Weather Index (FWI) combined with weather extreme forecasts (temperature, humidity deficit, wind gusts)."
    },
    "earthquakes": {
        "pipeline_name": "Earthquake Regional Aftershock Statistical Forecaster",
        "primary_model": "earthquakes_aftershock_hazard_xgboost",
        "statistical_model": "Omori-Utsu / Reasenberg-Jones Temporal Decay",
        "blocked_model": "earthquakes_aftershock_count_xgboost",
        "supported_horizons": ["6h", "12h", "24h", "48h", "72h"],
        "governance_status": "OPERATIONAL (Regional Aftershocks Only; Count Model BLOCKED)",
        "data_feed": "USGS ComCat Real-Time Feed",
        "validated_metrics": {
            "aftershock_hazard_pr_auc": 0.4658,
            "aftershock_hazard_roc_auc": 0.7400,
            "aftershock_count_r2_blocked": -0.0401
        },
        "scientific_basis": "Strictly probabilistic aftershock clustering following a verified mainshock. Deterministic earthquake prediction is scientifically impossible."
    },
    "cyclones": {
        "pipeline_name": "Tropical Cyclone 24h RI & Intensity Trajectory Forecaster",
        "primary_model": "cyclones_rapid_intensification_xgboost",
        "secondary_model": "cyclones_intensity_change_24h_xgboost",
        "supported_horizons": ["6h", "12h", "24h", "48h", "72h"],
        "governance_status": "OPERATIONAL",
        "data_feed": "NOAA National Hurricane Center & NOAA IBTrACS",
        "validated_metrics": {
            "ri_roc_auc": 0.8710,
            "ri_pr_auc": 0.3543,
            "intensity_change_rmse_kt": 13.9854,
            "intensity_change_r2": 0.4426
        },
        "scientific_basis": "Statistical-dynamical intensification prediction using SST, vertical wind shear, inner-core pressure, and storm speed."
    }
}

