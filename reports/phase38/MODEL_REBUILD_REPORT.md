# HAZARDX AI — MODEL REBUILD & ARCHITECTURAL REPORT
**Document ID:** `HX-RPT-PH38-02`  
**Phase:** Phase 38 — Model, Data & Risk Engine Improvements  
**Author:** Lead AI/ML & Disaster Risk Systems Architect  
**Date:** November 20, 2026  
**Status:** COMPLETE & SEALED  

---

## 1. Model Registry & Governance Framework

HAZARDX AI enforces strict, audit-verified machine learning governance across all prediction endpoints. Every model deployed within the inference runtime is registered in `ModelRegistry` (`backend/app/services/model_registry.py`) and backed by verified model artifacts, feature order contracts, and validation metadata.

Models demonstrating negative predictive skill, statistical overfit, or uncalibrated variance during Phase 12–37 benchmarking are subjected to **MANDATORY QUARANTINE** and permanently blocked from the operational pipeline.

---

## 2. Complete Model Status Matrix

| Hazard Domain | Model Identifier | Algorithm | Status | Primary Metric | Validation Performance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Floods** | `floods_flood_occurrence` | XGBoost Classifier | **OPERATIONAL** | ROC-AUC | 0.884 |
| **Floods** | `floods_flood_severity` | XGBoost Multi-Class | **OPERATIONAL** | Macro F1 | 0.741 |
| **Landslides** | `landslides_landslide_occurrence` | LightGBM Classifier | **OPERATIONAL** | ROC-AUC | 0.892 |
| **Landslides** | `landslides_landslide_magnitude` | LightGBM Multi-Class | **OPERATIONAL** | Macro F1 | 0.728 |
| **Earthquakes** | `earthquakes_aftershock_hazard` | XGBoost Classifier | **OPERATIONAL** | ROC-AUC | 0.864 |
| **Earthquakes** | `earthquakes_aftershock_count` | Gradient Boosting Regressor | **STRICTLY BLOCKED** | $R^2$ Score | **-0.0401 (QUARANTINED)** |
| **Earthquakes** | `omori_utsu_aftershock_model` | Reasenberg-Jones Analytical | **OPERATIONAL** | Poisson Log-Likelihood | Calibrated Statistical Law |
| **Wildfires** | `wildfires_wildfire_occurrence` | CatBoost Classifier | **OPERATIONAL** | ROC-AUC | 0.879 |
| **Wildfires** | `wildfires_fire_severity_frp` | CatBoost Regressor | **OPERATIONAL** | $R^2$ Score | 0.682 |
| **Wildfires** | `wildfires_fire_duration` | Gradient Boosting Regressor | **STRICTLY BLOCKED** | $R^2$ Score | **-0.0924 (QUARANTINED)** |
| **Cyclones** | `cyclones_rapid_intensification` | XGBoost Classifier | **OPERATIONAL** | ROC-AUC | 0.871 |
| **Cyclones** | `cyclones_intensity_change_24h` | XGBoost Regressor | **OPERATIONAL** | RMSE | 8.42 kt |

---

## 3. Strict Model Quarantine Details

### 3.1 Earthquake Aftershock Count Model (`earthquakes_aftershock_count`)
- **Quarantine Reason:** Severe negative predictive skill ($R^2 = -0.0401$). Predicting exact discrete counts of aftershocks over a 30-day window from point tectonic features violates the stochastic nature of seismic slip distributions.
- **Enforcement:** Quarantined in `model_registry.py`. Invocations return `model_status: "BLOCKED"`, `secondary_metrics: {"aftershock_count": None, "model_count_governance": "BLOCKED"}`.
- **Scientific Replacement:** Operationalized the analytical Omori-Utsu and Reasenberg-Jones formulation (`OmoriAftershockForecaster`), outputting rigorously calibrated Poisson occurrence probabilities $P(N \ge 1)$ across 6h, 12h, 24h, 48h, and 72h horizons.

### 3.2 Wildfire Duration Model (`wildfires_fire_duration`)
- **Quarantine Reason:** Negative predictive skill ($R^2 = -0.0924$). Fire duration is heavily governed by human suppression response times, fire department deployment, and micro-scale fuel breaks that cannot be predicted from 28 km ERA5 grids.
- **Enforcement:** Quarantined in `model_registry.py`. Invocations return `model_status: "BLOCKED"`.
- **Scientific Replacement:** Wildfire severity is quantified using satellite-calibrated Fire Radiative Power (FRP in Megawatts) and Canadian FWI fire danger ratings.

---

## 4. Operational Feature Order Contracts

To guarantee that runtime inference DataFrames match scikit-learn/XGBoost training column alignments with zero permutation errors, column orders are hard-coded in service initializers:

### 4.1 Flood Occurrence Model Schema (14 features)
```python
feature_order = [
    'precip_1d_mm', 'precip_3d_sum_mm', 'precip_7d_sum_mm', 'precip_14d_sum_mm',
    'api_14d_index', 'temp_2m_celsius', 'soil_temp_celsius', 'river_discharge_m3s',
    'river_discharge_7d_mean_m3s', 'river_discharge_ratio_7d', 'elevation_m',
    'slope_degrees', 'topographic_wetness_index', 'distance_to_river_km'
]
```

### 4.2 Landslide Occurrence Model Schema (14 features)
```python
feature_order = [
    'precip_1d_mm', 'precip_3d_sum_mm', 'precip_7d_sum_mm', 'precip_30d_sum_mm',
    'api_30d_index', 'temp_2m_celsius', 'soil_temp_celsius', 'slope_degrees',
    'elevation_m', 'aspect_degrees', 'plan_curvature', 'soil_clay_fraction_pct',
    'distance_to_road_km', 'distance_to_stream_km'
]
```

### 4.3 Wildfire Occurrence Model Schema (10 features)
```python
feature_order = [
    'temp_2m_celsius', 'relative_humidity_pct', 'wind_speed_10m_ms',
    'precip_7d_sum_mm', 'precip_30d_sum_mm', 'soil_temp_celsius',
    'fwi_fire_weather_index', 'slope_degrees', 'elevation_m', 'distance_to_road_km'
]
```

---

## 5. Verification Sign-Off

All operational models pass automated schema validation, TreeSHAP attribution extraction, and JSON serialization. Quarantined models remain completely blocked with clear audit warnings.
