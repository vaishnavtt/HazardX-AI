# HAZARDX AI – Phase 31: Model Root Cause Report

**Date:** November 19, 2026  
**Auditor:** Senior AI/ML Architecture & Model Governance Group  
**Scope:** Model-by-Model Root Cause Diagnosis Across 12 Machine Learning Models  

---

## 1. Hazard-by-Hazard Model Diagnosis

### 1.1 Wildfire Occurrence Classifier (`wildfires_wildfire_occurrence_xgboost`)
- **Observed Failure:** Outputs $60\%$ probability (`HIGH` risk) for Wayanad at $26.5^\circ\text{C}$ and $47\%$ RH under wet antecedent conditions ($118\text{ mm}$ rain, $\text{FWI} = 0.8$).
- **Diagnosis:**
  - *Data Deficit:* Only $6$ of $1,200$ training samples ($0.5\%$) were in South Asia. $95\%$ of samples were from high-latitude boreal North America ($52.5^\circ\text{N}$ median).
  - *Synthetic Weather Artifact:* Non-fire controls were generated at cold temperatures ($\sim 18^\circ\text{C}$), while fires were generated at warm temperatures ($\sim 32.5^\circ\text{C}$). Only $3$ of $600$ non-fire samples had temperatures $> 28^\circ\text{C}$.
  - *Feature Dominance:* Tree splits assigned $+2.08$ SHAP log-odds to ambient temperature. The model treats normal tropical warmth as evidence of wildfire ignition.
  - *Formula Divergence:* The training pipeline used an empirical proxy for FWI, while live inference used an exponential McArthur formula, causing live FWI ($0.7$) to be treated as out-of-distribution noise.
- **Root Cause Classification:** `MODEL_QUALITY_ERROR` + `GEOGRAPHIC_TRANSFER_ERROR` + `FEATURE_MAPPING_ERROR`.

### 1.2 Earthquake Aftershock Hazard Classifier (`earthquakes_aftershock_hazard_xgboost`)
- **Observed Failure:** Outputs $18\%$ probability for Wayanad despite 0 earthquakes within $100\text{ km}$ and nearest active fault at $1,410\text{ km}$.
- **Diagnosis:**
  - *Arbitrary Substitution:* `spatial_feature_service.py` defaulted missing mainshocks to $M 6.0$ at $10\text{ km}$ depth with $9.5\log_{10}(\text{Joules})$ cumulative energy when 0 events were detected.
  - *Conceptual Error:* Model was evaluated where no qualifying trigger existed. Under USGS guidelines, aftershock models must only execute conditionally upon observed mainshocks.
- **Root Cause Classification:** `RISK_LOGIC_ERROR`.

### 1.3 Tropical Cyclone Rapid Intensification Classifier (`cyclones_rapid_intensification_xgboost`)
- **Observed Failure:** Outputs $27\%$ rapid intensification probability for inland mountain valleys in Kerala.
- **Diagnosis:**
  - *Unconditional Execution:* Model was executed unconditionally for all coordinates with $|\text{lat}| \le 45^\circ$, injecting a fictitious $45\text{ kt}$ storm $85\text{ km}$ offshore.
- **Root Cause Classification:** `RISK_LOGIC_ERROR` + `GEOGRAPHIC_TRANSFER_ERROR`.

### 1.4 Flood Occurrence Classifier (`floods_flood_occurrence_xgboost`)
- **Diagnosis:**
  - Model performs well when supplied with authentic multi-day precipitation and GloFAS discharge anomalies.
  - However, because it was trained on 1:1 balanced data, its zero-rainfall base output is $\approx 0.09$ ($9\%$). Without calibration, this was rendered as a $9\%$ threat score.
- **Root Cause Classification:** `MODEL_CALIBRATION_ERROR`.

### 1.5 Landslide Occurrence Classifier (`landslides_landslide_occurrence_xgboost`)
- **Diagnosis:**
  - Accurately captures high terrain slope gradients ($> 20^\circ$).
  - However, the system failed to distinguish static terrain susceptibility from short-term meteorological triggering.
- **Root Cause Classification:** `FORECAST_ERROR`.

---

## 2. Model Governance Decision

1. **Quarantine Retention:** `earthquakes_aftershock_count` ($R^2 = -0.0401$) and `wildfires_fire_duration` ($R^2 = -214.75$) remain permanently blocked.
2. **Wildfire Occurrence Architecture Pivot:** The unconstrained black-box XGBoost wildfire model cannot be relied upon in tropical humid zones. Wildfire danger must be governed by the standard Canadian FWI rating and localized NASA FIRMS satellite thermal anomaly detection.
3. **Seismic & Cyclone Gating:** Aftershock hazard and cyclone intensification must be conditionally gated by real-world physical events.
