# HAZARDX AI — Complete Machine Learning Model Documentation
**Document ID:** `HAZARDX-DOCS-MDL-001`  
**Platform Version:** `v1.2.0-PROD`  
**Status:** Certified & Governed  

---

## 1. Machine Learning Architecture Overview

HAZARDX AI operationalizes a multidisciplinary machine learning framework consisting of 12 specialized models across five catastrophic natural hazard domains: Floods, Landslides, Earthquakes, Wildfires, and Tropical Cyclones.

All models adhere to strict governance rules:
- **Operational Models (10):** Validated on independent holdout sets, calibrated with Bayesian priors (Isotonic / Sigmoid), and coupled to live observational data feeds.
- **Quarantined Models (2):** Permanently blocked from production API endpoints due to unacceptable variance or negative out-of-sample predictive skill ($R^2 < 0$).

```
                      [Global Environmental Feeds]
            (USGS, Open-Meteo, GloFAS, FIRMS, NOAA, Copernicus DEM)
                                   │
                                   ▼
                   [Spatial Feature Synthesis Service]
                                   │
         ┌─────────────┬───────────┼───────────┬─────────────┐
         ▼             ▼           ▼           ▼             ▼
      Floods      Landslides  Earthquakes  Wildfires     Cyclones
      (XGBoost)   (LightGBM)  (Omori/XGB)  (CatBoost)    (XGBoost)
         │             │           │           │             │
         └─────────────┴───────────┼───────────┴─────────────┘
                                   ▼
                   [Bayesian Odds Prior Calibration]
                                   │
                                   ▼
                   [TreeSHAP Attribution Explainer]
                                   │
                                   ▼
                   [Prospective Prediction Archive]
```

---

## 2. Model Governance & Operational Inventory

```
========================================================================================================================
HAZARD DOMAIN    MODEL IDENTIFIER                 ALGORITHM            TARGET VARIABLE           METRIC     STATUS
========================================================================================================================
Floods           floods_flood_occurrence         XGBoost (Isotonic)   Reach Inundation (0/1)    AUC: 0.884 OPERATIONAL
Floods           floods_flood_severity           XGBoost Multi-Class  Flood Magnitude (0, 1, 2) F1: 0.753  OPERATIONAL
Landslides       landslides_landslide_occurrence LightGBM (Isotonic)  Slope Failure (0/1)       AUC: 0.892 OPERATIONAL
Landslides       landslides_landslide_magnitude  LightGBM Multi-Class Impact Class (0, 1, 2)    Acc: 0.622 OPERATIONAL
Earthquakes      earthquakes_aftershock_hazard   XGBoost (Isotonic)   Aftershock Sequence (0/1) AUC: 0.864 OPERATIONAL
Earthquakes      omori_aftershock_analytical     Reasenberg-Jones     P(N >= 1) Poisson Decay   Poisson LL OPERATIONAL
Earthquakes      earthquakes_max_aftershock_mag  XGBoost Regressor    Estimated Max Aftershock  R2: 0.344  EXPERIMENTAL
Earthquakes      earthquakes_aftershock_count    Gradient Boosting    Discrete Aftershock Count R2: -0.040 QUARANTINED
Wildfires        wildfires_wildfire_occurrence   CatBoost (Isotonic)  Ignition / Spread (0/1)   AUC: 0.879 OPERATIONAL
Wildfires        wildfires_fire_severity_frp     CatBoost Regressor   Log FRP (MW) Intensity    R2: 0.215  EXPERIMENTAL
Wildfires        wildfires_fire_duration         Gradient Boosting    Active Duration (Days)    R2: -214.7 QUARANTINED
Cyclones         cyclones_rapid_intensification  XGBoost (Sigmoid)    Delta V >= 30 kt / 24h    AUC: 0.871 OPERATIONAL
Cyclones         cyclones_intensity_change_24h   XGBoost Regressor    24h Intensity Delta (kt)  R2: 0.443  OPERATIONAL
========================================================================================================================
```

---

## 3. Quarantined Models & Formal Blocking Policy

### 3.1 Earthquake Aftershock Count Regressor (`earthquakes_aftershock_count`)
- **Reported Metric:** $R^2 = -0.0401$ (Negative Predictive Skill).
- **Physical Reason:** Static point tectonic features cannot resolve the stochastic micro-asperity interactions that govern discrete aftershock event counts.
- **Enforcement:** Permanently suppressed in `ModelRegistry` (`backend/app/services/model_registry.py`).
- **Operational Replacement:** Analytical Reasenberg-Jones / Omori-Utsu Poisson occurrence probability ($P(N \ge 1)$).

### 3.2 Wildfire Duration Regressor (`wildfires_fire_duration`)
- **Reported Metric:** $R^2 = -214.75$ (Extreme Variance Inflation).
- **Physical Reason:** Fire duration is predominantly governed by human firefighting suppression tactics, micro-fuelbreaks, and air tanker deployments, which are unobservable in synoptic weather grids.
- **Enforcement:** Permanently blocked in `ModelRegistry`.
- **Operational Replacement:** Satellite Fire Radiative Power (FRP in Megawatts) and Canadian FWI fire danger rating.

---

## 4. Feature Order Schemas & Reflection Invariants

Every operational model strictly enforces DataFrame column alignments matching its training metadata:

### 4.1 Flood Occurrence (14 Features)
```python
feature_order = [
    'precip_1d_mm', 'precip_3d_sum_mm', 'precip_7d_sum_mm', 'precip_14d_sum_mm',
    'api_14d_index', 'temp_2m_celsius', 'soil_temp_celsius', 'river_discharge_m3s',
    'river_discharge_7d_mean_m3s', 'river_discharge_ratio_7d', 'elevation_m',
    'slope_degrees', 'topographic_wetness_index', 'distance_to_river_km'
]
```

### 4.2 Landslide Occurrence (14 Features)
```python
feature_order = [
    'precip_1d_mm', 'precip_3d_sum_mm', 'precip_7d_sum_mm', 'precip_30d_sum_mm',
    'api_30d_index', 'temp_2m_celsius', 'soil_temp_celsius', 'slope_degrees',
    'elevation_m', 'aspect_degrees', 'plan_curvature', 'soil_clay_fraction_pct',
    'distance_to_road_km', 'distance_to_stream_km'
]
```

### 4.3 Wildfire Occurrence (10 Features)
```python
feature_order = [
    'temp_2m_celsius', 'relative_humidity_pct', 'wind_speed_10m_ms',
    'precip_7d_sum_mm', 'precip_30d_sum_mm', 'soil_temp_celsius',
    'fwi_fire_weather_index', 'slope_degrees', 'elevation_m', 'distance_to_road_km'
]
```

### 4.4 Cyclone Rapid Intensification (11 Features)
```python
feature_order = [
    'current_wind_kt', 'current_pres_hpa', 'dist_to_land_km', 'landfall_flag',
    'past_delta_wind_6h', 'past_delta_wind_12h', 'past_delta_pres_6h',
    'translational_speed_kt', 'heading_degrees', 'coriolis_param',
    'pot_intensity_headroom'
]
```

---

## 5. Explainable AI: Real-Time TreeSHAP Attribution

To provide transparent decision support, each inference service dynamically calculates TreeSHAP values for the top 5 contributing features using `shap.TreeExplainer`:
- Measures positive margin log-odds deviation from baseline expected value $E[f(x)]$.
- Generates human-readable physical interpretations (e.g. *"Acute 24h rainfall causing flash runoff"*).
- Precludes false causal assumptions: TreeSHAP provides associative attribution, not Pearlian causal DAG intervention.
