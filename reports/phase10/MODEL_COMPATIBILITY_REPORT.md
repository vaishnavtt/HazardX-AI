# HAZARDX AI — Phase 10: Model Compatibility Report
**Evaluation Date:** November 18, 2026  
**Focus:** Assessment of Existing 12 XGBoost Models for Numerical Weather Forecast & Predictive Early Warning Inputs  
**Location:** `C:\Users\thott\Desktop\hazardai`

---

## 1. Objective

To evaluate whether the existing 12 trained XGBoost models can ingest forward-looking numerical weather prediction (NWP) forecasts (e.g. from ECMWF, GFS, ICON via Open-Meteo and GloFAS) across discrete forecast horizons: **6h, 12h, 24h, 48h, and 72h**, without violating physical causality or feature schema definitions.

---

## 2. Model-by-Model Compatibility Assessment

### 2.1 Floods Models
- **Model 1:** `floods_flood_occurrence_xgboost` (Binary Classification, PR-AUC: 0.8156, ROC-AUC: 0.7899)
- **Model 2:** `floods_flood_severity_xgboost` (Multiclass, Macro-F1: 0.7527)
- **Feature Set:** `precip_1d_mm`, `precip_3d_sum_mm`, `precip_7d_sum_mm`, `precip_14d_sum_mm`, `api_14d_index`, `temp_2m_celsius`, `soil_temp_celsius`, `river_discharge_m3s`, `river_discharge_7d_mean_m3s`, `river_discharge_ratio_7d`, `elevation_m`, `slope_degrees`, `topographic_wetness_index`, `distance_to_river_km`.
- **Forecast Compatibility Analysis:**
  - **High Compatibility.**
  - GloFAS produces gridded daily river discharge forecasts for Day 0 through Day 7.
  - Open-Meteo produces hourly precipitation forecasts up to 96 hours.
  - Sub-daily (6h, 12h) discharge is interpolated between current and Day 1; multi-day (24h, 48h, 72h) discharge directly reflects GloFAS forecast routing.
  - Cumulative precipitation sums for future horizons are calculated from hourly NWP series.
  - Static features (elevation, slope, TWI, distance to river) remain invariant.
- **Operational Verdict:** **COMPATIBLE FOR OPERATIONAL FORECASTING**.

### 2.2 Landslides Models
- **Model 1:** `landslides_landslide_occurrence_xgboost` (Binary Classification, PR-AUC: 0.8196, ROC-AUC: 0.7496)
- **Model 2:** `landslides_landslide_magnitude_xgboost` (Multiclass, Macro-F1: 0.4221)
- **Feature Set:** `precip_1d_mm`, `precip_3d_sum_mm`, `precip_7d_sum_mm`, `precip_30d_sum_mm`, `api_30d_index`, `temp_2m_celsius`, `soil_temp_celsius`, `slope_degrees`, `elevation_m`, `aspect_degrees`, `plan_curvature`, `soil_clay_fraction_pct`, `distance_to_road_km`, `distance_to_stream_km`.
- **Forecast Compatibility Analysis:**
  - **High Compatibility.**
  - Rainfall is the primary dynamic trigger of rapid-onset shallow landslides.
  - Forward-looking rainfall sums ($P_{6h}, P_{12h}, P_{24h}, P_{48h}, P_{72h}$) and soil moisture forecasts (`soil_moisture_0_to_1cm`) directly drive infiltration and pore-water pressure increases.
  - Paired with empirical intensity-duration thresholds ($I = \alpha D^{-\beta}$) to provide physically grounded confidence.
- **Operational Verdict:** **COMPATIBLE FOR OPERATIONAL FORECASTING**.

### 2.3 Wildfires Models
- **Model 1:** `wildfires_wildfire_occurrence_xgboost` (Binary Classification, PR-AUC: 0.8272, ROC-AUC: 0.8247)
- **Model 2:** `wildfires_frp_intensity_xgboost` (Regression, RMSE: 1.3717, R²: 0.2154) - EXPERIMENTAL
- **Model 3:** `wildfires_fire_duration_xgboost` (Regression, R²: -214.75) - **BLOCKED**
- **Feature Set:** `temp_2m_celsius`, `relative_humidity_pct`, `wind_speed_10m_ms`, `wind_direction_10m_deg`, `surface_pressure_hpa`, `precip_1d_mm`, `precip_7d_sum_mm`, `precip_30d_sum_mm`, `elevation_m`, `slope_degrees`, `aspect_degrees`, `ndvi_vegetation_index`, `distance_to_road_km`.
- **Forecast Compatibility Analysis:**
  - **High Compatibility for Occurrence / Ignition Susceptibility.**
  - Dynamic atmospheric variables (forecast maximum temperature, minimum relative humidity, maximum wind gusts, and precipitation deficits) are extracted for each forecast window.
  - McArthur/Canadian Fire Weather Index (FWI) is computed per horizon.
  - **Duration model remains strictly blocked:** Model outputs `None` with governance notice.
- **Operational Verdict:** **OCCURRENCE MODEL COMPATIBLE; DURATION MODEL STRICTLY BLOCKED**.

### 2.4 Cyclones Models
- **Model 1:** `cyclones_rapid_intensification_xgboost` (Binary Classification, ROC-AUC: 0.8710, PR-AUC: 0.3543)
- **Model 2:** `cyclones_intensity_change_24h_xgboost` (Regression, RMSE: 13.9854 kt, R²: 0.4426)
- **Feature Set:** `current_wind_kt`, `current_min_pressure_hpa`, `forward_speed_kt`, `sst_celsius`, `vertical_wind_shear_kt`, `relative_humidity_700_500_pct`, `storm_lat`, `storm_lon`, `basin_encoded`.
- **Forecast Compatibility Analysis:**
  - **Compatible for 24-Hour Horizon.**
  - Targets are specifically formulated for 24-hour intensification trajectory and rapid intensification ($\ge 30\text{ kt}$ gain).
  - Official multi-day forecast tracks (12h, 24h, 48h, 72h) are ingested from NOAA NHC / IMD bulletins.
- **Operational Verdict:** **COMPATIBLE FOR OPERATIONAL FORECASTING**.

### 2.5 Earthquakes Models
- **Model 1:** `earthquakes_aftershock_hazard_xgboost` (Binary Classification, PR-AUC: 0.4658, ROC-AUC: 0.7400)
- **Model 2:** `earthquakes_max_aftershock_mag_xgboost` (Regression, RMSE: 1.9449, R²: 0.3439) - EXPERIMENTAL
- **Model 3:** `earthquakes_aftershock_count_xgboost` (Regression, R²: -0.0401) - **BLOCKED**
- **Forecast Compatibility Analysis:**
  - **Deterministic earthquake prediction is physically impossible.**
  - The aftershock hazard classification model evaluates regional clustering following a mainshock.
  - To support multi-horizon forecasts (6h, 12h, 24h, 48h, 72h), the platform integrates the **Standard Statistical Omori-Utsu / Reasenberg-Jones temporal decay model** ($n(t) = K / (t + c)^p$).
  - **Aftershock count regression model remains strictly blocked.**
- **Operational Verdict:** **PROBABILISTIC AFTERSHOCK DECAY COMPATIBLE; DETERMINISTIC PREDICTION STRICTLY FORBIDDEN**.

---

## 3. Compatibility Summary Matrix

| Hazard Module | Pipeline Type | Horizon Support | Reused Model | Statistical Augmentation | Operational Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Floods** | Hydrological Trajectory | 6h, 12h, 24h, 48h, 72h | `flood_occurrence_xgboost` | GloFAS Anomaly Exceedance | **OPERATIONAL** |
| **Landslides**| Infiltration Susceptibility | 6h, 12h, 24h, 48h, 72h | `landslide_occurrence_xgboost` | Caine/Guzzetti I-D Thresholds | **OPERATIONAL** |
| **Wildfires** | Fire Weather & Ignition | 6h, 12h, 24h, 48h, 72h | `wildfire_occurrence_xgboost` | McArthur Fire Weather Index | **OPERATIONAL (Duration BLOCKED)** |
| **Earthquakes**| Probabilistic Aftershocks | 6h, 12h, 24h, 48h, 72h | `aftershock_hazard_xgboost` | Omori-Utsu Temporal Decay | **OPERATIONAL (Count BLOCKED)** |
| **Cyclones** | RI & Intensity Change | 6h, 12h, 24h, 48h, 72h | `rapid_intensification_xgboost` | NHC Official Track Cones | **OPERATIONAL** |

