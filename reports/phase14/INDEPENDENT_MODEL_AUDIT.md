# HAZARDX AI – PHASE 14 AUDIT: INDEPENDENT MODEL AUDIT
## Comprehensive Traceability, Split Verification & Empirical Benchmark Matrix for All 12 Models

**Document Reference:** `HAZARDX-P14-AUDIT-001`  
**Audit Date:** November 19, 2026  
**Auditor:** Senior Multidisciplinary AI & Disaster Risk Audit Team  
**Evaluation Scope:** 12 Trained XGBoost Models across Floods, Landslides, Earthquakes, Cyclones, Wildfires  
**Source Code Reference:** `scripts/ml_pipeline/`, `backend/app/services/`, `models/`  
**Dataset Directory:** `data/model_ready/`  

---

## 1. AUDIT METHODOLOGY & SCOPE

This independent audit inspected the complete machine learning lifecycle for all 12 models in HAZARDX AI:
1. **Model Artifacts:** Inspecting `.joblib` binary serializations and `.json` native XGBoost model dumps in `models/`.
2. **Metadata Files:** Cross-referencing `*_metadata.json` for hyperparameters, feature order, and loss objectives.
3. **Dataset Splits:** Verifying partition assignments (`train`, `val`, `test`), temporal date ranges, and sample counts in `data/model_ready/`.
4. **Evaluation Scripts:** Inspecting `scripts/ml_pipeline/evaluator.py` and `scripts/phase13_evaluate_models.py`.
5. **Metric Discrepancies:** Reconciling previously reported metrics in Phase 13 text vs actual empirical measurements stored in `reports/phase13_model_evaluation_results.json` and `models/model_comparison_dashboard.json`.

---

## 2. DISCREPANCY RECONCILIATION: TEST SAMPLE COUNTS

### 2.1 The Issue Discovered
Earlier narrative reports (e.g. `PHASE13_HAZARD_WISE_RESULTS.md`) cited an aggregate holdout count of **2,298 samples** with arbitrary subset sizes (e.g., Floods $N=256$, Cyclones $N=899$, Landslides $N=270$).

### 2.2 Actual Empirical Ground Truth
Our direct inspection of the 5 model-ready datasets in `data/model_ready/*.csv` and the automated execution of `scripts/phase13_evaluate_models.py` proves the actual partition breakdown:

| Hazard Dataset | File Path | Total Rows | Train Split | Validation Split | Test Split ($N_{\text{test}}$) | Temporal Span |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Floods** | `data/model_ready/floods/flood_model_ready.csv` | 600 | 486 (81.0%) | 33 (5.5%) | **81 (13.5%)** | 1996-09-02 to 2026-10-10 |
| **Landslides** | `data/model_ready/landslides/landslide_model_ready.csv` | 600 | 366 (61.0%) | 144 (24.0%) | **90 (15.0%)** | 1996-06-29 to 2017-08-21 |
| **Earthquakes** | `data/model_ready/earthquakes/earthquake_model_ready.csv` | 10,000 | 7,255 (72.6%) | 1,207 (12.1%) | **1,538 (15.4%)** | 2000-12-31 to 2025-11-30 |
| **Cyclones** | `data/model_ready/cyclones/cyclone_model_ready.csv` | 220,484 | 177,798 (80.6%) | 20,930 (9.5%) | **21,756 (9.9%)** | 1980-01-01 to 2026-11-11 |
| **Wildfires** | `data/model_ready/wildfires/wildfire_model_ready.csv` | 1,200 | 930 (77.5%) | 174 (14.5%) | **96 (8.0%)** | 1990-01-18 to 2026-08-14 |
| **TOTAL** | — | **232,884** | **186,835** | **22,488** | **23,561** | — |

**Verdict:** The actual verified holdout evaluation suite evaluates **23,561 test samples**, not 2,298. The numbers in `models/model_comparison_dashboard.json` and `reports/phase13_model_evaluation_results.json` reflect this full 23,561-sample test suite.

---

## 3. TRACEABLE AUDIT RECORD FOR ALL 12 MODELS

### Model 1: `floods_flood_occurrence`
- **Target Variable:** `flood_occurred` (Binary: 1 = Inundation event, 0 = Non-flood control)
- **Task Type:** Binary Classification
- **Dataset:** `data/model_ready/floods/flood_model_ready.csv` (v1.0.0, 600 rows)
- **Partitions:** Train = 486, Val = 33, Test = 81
- **Features Used (14):** `precip_1d_mm`, `precip_3d_sum_mm`, `precip_7d_sum_mm`, `precip_14d_sum_mm`, `api_14d_index`, `temp_2m_celsius`, `soil_temp_celsius`, `river_discharge_m3s`, `river_discharge_7d_mean_m3s`, `river_discharge_ratio_7d`, `elevation_m`, `slope_degrees`, `topographic_wetness_index`, `distance_to_river_km`
- **Artifact Path:** `models/floods/floods_flood_occurrence_xgboost.joblib` (246 KB)
- **Native JSON:** `models/floods/floods_flood_occurrence_xgboost.json` (184 KB)
- **Actual Measured Test Metrics ($N=81$):**
  - **PR-AUC:** `0.8156` (Naive baseline: `0.5062`, Physical baseline: `0.6420`)
  - **ROC-AUC:** `0.7899` | **F1-Score:** `0.7089` | **Accuracy:** `0.7160`
  - **Brier Score:** `0.1915` | **Confusion Matrix:** TN=30, FP=10, FN=13, TP=28
  - **FAR:** `26.32%` | **Missed-Event Rate:** `31.71%` | **CSI (Threat Score):** `0.5490`
- **Operational Status:** **OPERATIONAL** (Beats baselines with substantial margin).

### Model 2: `floods_flood_severity`
- **Target Variable:** `severity_class` (Multiclass: 0 = None, 1 = Large, 2 = Extreme/Decadal)
- **Task Type:** Multi-class Classification
- **Dataset:** `data/model_ready/floods/flood_model_ready.csv`
- **Partitions:** Train = 486, Val = 33, Test = 81
- **Features Used (14):** Same 14 hydrological & terrain features as Model 1.
- **Artifact Path:** `models/floods/floods_flood_severity_xgboost.joblib` (1.07 MB)
- **Actual Measured Test Metrics ($N=81$):**
  - **Accuracy:** `75.31%` (Naive baseline: `49.38%`)
  - **Macro F1:** `0.7527` | **Weighted F1:** `0.7526`
  - **Confusion Matrix:**
    $$\begin{pmatrix} 32 & 8 & 0 \\ 12 & 29 & 0 \\ 0 & 0 & 0 \end{pmatrix}$$
- **Operational Status:** **OPERATIONAL** (Note: Severe class 2 has zero test instances; model correctly discriminates Class 0 vs Class 1).

### Model 3: `landslides_landslide_occurrence`
- **Target Variable:** `landslide_occurred` (Binary: 1 = Slope failure, 0 = Stable terrain)
- **Task Type:** Binary Classification
- **Dataset:** `data/model_ready/landslides/landslide_model_ready.csv` (v1.0.0, 600 rows)
- **Partitions:** Train = 366, Val = 144, Test = 90
- **Features Used (14):** `precip_1d_mm`, `precip_3d_sum_mm`, `precip_7d_sum_mm`, `precip_30d_sum_mm`, `api_30d_index`, `temp_2m_celsius`, `soil_temp_celsius`, `slope_degrees`, `elevation_m`, `aspect_degrees`, `plan_curvature`, `soil_clay_fraction_pct`, `distance_to_road_km`, `distance_to_stream_km`
- **Artifact Path:** `models/landslides/landslides_landslide_occurrence_xgboost.joblib` (443 KB)
- **Actual Measured Test Metrics ($N=90$):**
  - **PR-AUC:** `0.8196` (Naive baseline: `0.5667`, Physical baseline: `0.6720`)
  - **ROC-AUC:** `0.7496` | **F1-Score:** `0.6667` | **Accuracy:** `0.6889`
  - **Brier Score:** `0.2341` | **Confusion Matrix:** TN=34, FP=5, FN=23, TP=28
  - **FAR:** `15.15%` | **Missed-Event Rate:** `45.10%` | **CSI:** `0.5000`
- **Operational Status:** **OPERATIONAL** (High precision of 84.8%, low false alarms).

### Model 4: `landslides_landslide_magnitude`
- **Target Variable:** `hazard_magnitude_class` (Multiclass: 0 = None, 1 = Small/Medium, 2 = Large/Catastrophic)
- **Task Type:** Multi-class Classification
- **Dataset:** `data/model_ready/landslides/landslide_model_ready.csv`
- **Partitions:** Train = 366, Val = 144, Test = 90
- **Features Used (14):** Same 14 geomorphic & precipitation features.
- **Artifact Path:** `models/landslides/landslides_landslide_magnitude_xgboost.joblib` (269 KB)
- **Actual Measured Test Metrics ($N=90$):**
  - **Accuracy:** `62.22%` (Unweighted) $\rightarrow$ `64.44%` (Class-weighted)
  - **Macro F1:** `0.4221` (Unweighted) $\rightarrow$ `0.4362` (Class-weighted)
  - **Confusion Matrix:**
    $$\begin{pmatrix} 32 & 7 & 0 \\ 23 & 24 & 0 \\ 1 & 3 & 0 \end{pmatrix}$$
- **Operational Status:** **OPERATIONAL** (Minority class 2 has severe data sparsity; 4 total instances in test split).

### Model 5: `earthquakes_aftershock_hazard`
- **Target Variable:** `elevated_aftershock_hazard` (Binary: $\ge 5$ aftershocks or secondary $M \ge 5.0$ in 30d/100km)
- **Task Type:** Binary Classification
- **Dataset:** `data/model_ready/earthquakes/earthquake_model_ready.csv` (10,000 rows)
- **Partitions:** Train = 7,255, Val = 1,207, Test = 1,538
- **Features Used (11):** `mainshock_mag`, `focal_depth_km`, `dist_to_active_fault_km`, `nearest_fault_slip_type` (encoded via OrdinalEncoder), `prior_count_7d_100km`, `prior_count_30d_100km`, `prior_count_365d_100km`, `prior_max_mag_30d`, `cumulative_energy_log_joules`, `seismic_rate_accel_ratio`, `regional_b_value`
- **Artifact Path:** `models/earthquakes/earthquakes_aftershock_hazard_xgboost.joblib` (350 KB)
- **Actual Measured Test Metrics ($N=1,538$):**
  - **PR-AUC:** `0.4658` (Naive baseline: `0.2055`)
  - **ROC-AUC:** `0.7400` | **Recall:** `0.8323` | **F1-Score:** `0.4311` (Default $\tau=0.50$) $\rightarrow$ `0.4493` (Calibrated $\tau=0.68$)
  - **Brier Score:** `0.2787` | **Confusion Matrix ($\tau=0.50$):** TN=581, FP=641, FN=53, TP=263
- **Operational Status:** **OPERATIONAL** (Threshold calibrated to $\tau=0.68$ to cut FAR).

### Model 6: `earthquakes_aftershock_count`
- **Target Variable:** `aftershock_count_30d` (Continuous count)
- **Task Type:** Regression
- **Dataset:** `data/model_ready/earthquakes/earthquake_model_ready.csv`
- **Partitions:** Train = 7,255, Val = 1,207, Test = 1,538
- **Artifact Path:** `models/earthquakes/earthquakes_aftershock_count_xgboost.joblib` (396 KB)
- **Actual Measured Test Metrics ($N=1,538$):**
  - **MAE:** `1.4851` | **RMSE:** `2.4599`
  - **$R^2$ Score:** **`-0.0401`** (FAIL: Worse than sample mean baseline $R^2 = 0.00$)
  - **Explained Variance:** `0.0177`
- **Operational Status:** **BLOCKED / QUARANTINED** (Permanently restricted from operational alerting).

### Model 7: `earthquakes_max_aftershock_mag`
- **Target Variable:** `max_aftershock_mag_30d` (Continuous Mw)
- **Task Type:** Regression
- **Dataset:** `data/model_ready/earthquakes/earthquake_model_ready.csv`
- **Partitions:** Train = 7,255, Val = 1,207, Test = 1,538
- **Artifact Path:** `models/earthquakes/earthquakes_max_aftershock_mag_xgboost.joblib` (120 KB)
- **Actual Measured Test Metrics ($N=1,538$):**
  - **MAE:** `1.5612` | **RMSE:** `1.9449`
  - **$R^2$ Score:** **`0.3439`** (Beats baseline $R^2 = 0.00$)
  - **Explained Variance:** `0.3519`
- **Operational Status:** **EXPERIMENTAL** (Advisory guidance for researchers; excluded from sirens).

### Model 8: `cyclones_rapid_intensification`
- **Target Variable:** `rapid_intensification` (Binary: $\Delta V \ge 30\text{ kt}$ in 24 hours)
- **Task Type:** Binary Classification
- **Dataset:** `data/model_ready/cyclones/cyclone_model_ready.csv` (220,484 rows)
- **Partitions:** Train = 177,798, Val = 20,930, Test = 21,756
- **Features Used (11):** `current_wind_kt`, `current_pres_hpa`, `dist_to_land_km`, `landfall_flag`, `past_delta_wind_6h`, `past_delta_wind_12h`, `past_delta_pres_6h`, `translational_speed_kt`, `heading_degrees`, `coriolis_param`, `pot_intensity_headroom`
- **Artifact Path:** `models/cyclones/cyclones_rapid_intensification_xgboost.joblib` (406 KB)
- **Actual Measured Test Metrics ($N=21,756$):**
  - **PR-AUC:** `0.3543` (Naive baseline: `0.0662`, Extreme class imbalance 6.6% positive rate)
  - **ROC-AUC:** `0.8710` | **Recall:** `0.6833` | **F1-Score:** `0.3880`
  - **Brier Score:** `0.1000` | **Confusion Matrix:** TN=17,668, FP=2,648, FN=456, TP=984
- **Operational Status:** **OPERATIONAL** (Integrated with Dual-Trigger wind scale).

### Model 9: `cyclones_intensity_change_24h`
- **Target Variable:** `delta_wind_24h` (Continuous wind change in knots)
- **Task Type:** Regression
- **Dataset:** `data/model_ready/cyclones/cyclone_model_ready.csv`
- **Partitions:** Train = 177,798, Val = 20,930, Test = 21,756
- **Artifact Path:** `models/cyclones/cyclones_intensity_change_24h_xgboost.joblib` (1.07 MB)
- **Actual Measured Test Metrics ($N=21,756$):**
  - **MAE:** `10.0337 knots` | **RMSE:** `13.9854 knots`
  - **$R^2$ Score:** **`0.4426`** (Strong generalization on 21,756 holdout samples)
  - **Explained Variance:** `0.4442` | **Median Absolute Error:** `7.03 knots`
- **Operational Status:** **OPERATIONAL** (Primary numerical wind intensity engine).

### Model 10: `wildfires_wildfire_occurrence`
- **Target Variable:** `wildfire_occurred` (Binary: 1 = Active fire detection, 0 = Non-fire control)
- **Task Type:** Binary Classification
- **Dataset:** `data/model_ready/wildfires/wildfire_model_ready.csv` (1,200 rows)
- **Partitions:** Train = 930, Val = 174, Test = 96
- **Features Used (10):** `temp_2m_celsius`, `relative_humidity_pct`, `wind_speed_10m_ms`, `precip_7d_sum_mm`, `precip_30d_sum_mm`, `soil_temp_celsius`, `fwi_fire_weather_index`, `slope_degrees`, `elevation_m`, `distance_to_road_km`
- **Artifact Path:** `models/wildfires/wildfires_wildfire_occurrence_xgboost.joblib` (545 KB)
- **Actual Measured Test Metrics ($N=96$):**
  - **PR-AUC:** `0.8272` (Naive baseline: `0.5000`)
  - **ROC-AUC:** `0.8247` | **F1-Score:** `0.7368` | **Accuracy:** `0.7396`
  - **Brier Score:** `0.1973` | **Confusion Matrix:** TN=36, FP=12, FN=13, TP=35
  - **FAR:** `25.53%` | **Missed-Event Rate:** `27.08%` | **CSI:** `0.5833`
- **Operational Status:** **OPERATIONAL** (Strong meteorological fire susceptibility skill).

### Model 11: `wildfires_frp_intensity`
- **Target Variable:** `log_total_frp_mw` (Continuous log10 Fire Radiative Power)
- **Task Type:** Regression
- **Dataset:** `data/model_ready/wildfires/wildfire_model_ready.csv`
- **Partitions:** Train = 930, Val = 174, Test = 96
- **Artifact Path:** `models/wildfires/wildfires_frp_intensity_xgboost.joblib` (468 KB)
- **Actual Measured Test Metrics ($N=96$):**
  - **MAE:** `1.0008` | **RMSE:** `1.3717`
  - **$R^2$ Score:** **`0.2154`** (Beats baseline $R^2 = 0.00$)
  - **Explained Variance:** `0.2154`
- **Operational Status:** **EXPERIMENTAL** (Advisory guidance for fire intensity; not standalone).

### Model 12: `wildfires_fire_duration`
- **Target Variable:** `fire_duration_days` (Continuous days)
- **Task Type:** Regression
- **Dataset:** `data/model_ready/wildfires/wildfire_model_ready.csv`
- **Partitions:** Train = 930, Val = 174, Test = 96
- **Artifact Path:** `models/wildfires/wildfires_fire_duration_xgboost.joblib` (118 KB)
- **Actual Measured Test Metrics ($N=96$):**
  - **MAE:** `4.5318 days` | **RMSE:** `7.3442 days`
  - **$R^2$ Score:** **`-214.75`** (CATASTROPHIC FAILURE)
  - **Explained Variance:** `-143.63`
- **Operational Status:** **BLOCKED / QUARANTINED** (Permanently hard-blocked).

---

## 4. SUMMARY AUDIT TABLE & GOVERNANCE COMPLIANCE

| Tier | Model Key | Verified Primary Metric | Primary Score | Status in Backend | Passed Independent Audit? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Operational** | `floods_flood_occurrence` | PR-AUC | 0.8156 | Active in `flood_service.py` | **YES** |
| **Operational** | `floods_flood_severity` | Macro F1 | 0.7527 | Active in `flood_service.py` | **YES** |
| **Operational** | `landslides_landslide_occurrence` | PR-AUC | 0.8196 | Active in `landslide_service.py` | **YES** |
| **Operational** | `landslides_landslide_magnitude` | Macro F1 | 0.4221 | Active in `landslide_service.py` | **YES** (Class-weighted) |
| **Operational** | `earthquakes_aftershock_hazard` | PR-AUC | 0.4658 | Active in `earthquake_service.py` | **YES** ($\tau=0.68$) |
| **Operational** | `cyclones_rapid_intensification` | PR-AUC | 0.3543 | Active in `cyclone_service.py` | **YES** (Dual-Trigger) |
| **Operational** | `cyclones_intensity_change_24h` | RMSE | 13.9854 kt ($R^2=0.44$) | Active in `cyclone_service.py` | **YES** |
| **Operational** | `wildfires_wildfire_occurrence` | PR-AUC | 0.8272 | Active in `wildfire_service.py` | **YES** |
| **Experimental** | `earthquakes_max_aftershock_mag` | RMSE | 1.9449 Mw ($R^2=0.34$) | Advisory only | **YES** |
| **Experimental** | `wildfires_frp_intensity` | RMSE | 1.3717 ($R^2=0.22$) | Advisory only | **YES** |
| **Blocked** | `earthquakes_aftershock_count` | $R^2$ | -0.0401 | Hard-blocked; returns None | **YES (Enforced)** |
| **Blocked** | `wildfires_fire_duration` | $R^2$ | -214.75 | Hard-blocked; returns None | **YES (Enforced)** |

**Audit Conclusion:** The 12 models have been completely audited and verified against disk artifacts and true holdout test partitions ($N=23,561$). All discrepancies between prior prose narratives and empirical records are fully reconciled.
