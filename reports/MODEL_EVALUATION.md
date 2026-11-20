# HAZARDX AI — Consolidated Model Evaluation & Governance Report
**Document ID:** `HX-RPT-CANON-02`  
**Classification:** Canonical Machine Learning Audit & Model Evaluation  
**Release:** v1.2.0-PROD (Final Release)  
**Authors:** Senior AI/ML Engineer & MLOps Infrastructure Specialist  
**Date:** November 20, 2026  

---

## 1. Executive Summary

This report consolidates the complete evaluation metrics, data provenance, validation methodologies, and governance classifications for all 12 machine learning models developed for HAZARDX AI.

Models are categorized into three operational tiers:
1. **OPERATIONAL (10 Models):** Deployed to live inference endpoints.
2. **EXPERIMENTAL (2 Models):** Deployed with explicit advisory notices.
3. **STRICTLY QUARANTINED (2 Models):** Permanently suppressed from production inference due to negative predictive skill ($R^2 < 0$).

---

## 2. Master Model Evaluation Table

```
======================================================================================================================================
HAZARD DOMAIN    MODEL NAME                      ALGORITHM            TRAINING DATASET        PRIMARY METRIC       OPERATIONAL STATUS
======================================================================================================================================
Floods           floods_flood_occurrence         XGBoost (Isotonic)   Dartmouth Flood (DFO)   ROC-AUC: 0.884       OPERATIONAL
Floods           floods_flood_severity           XGBoost Multi-Class  DFO Historical Floods   Macro F1: 0.753      OPERATIONAL
Landslides       landslides_landslide_occurrence LightGBM (Isotonic)  NASA GLC + Copernicus   ROC-AUC: 0.892       OPERATIONAL
Landslides       landslides_landslide_magnitude  LightGBM Multi-Class NASA GLC Magnitude     Accuracy: 0.622      OPERATIONAL
Earthquakes      earthquakes_aftershock_hazard   XGBoost (Isotonic)   USGS ComCat Seismicity  ROC-AUC: 0.864       OPERATIONAL
Earthquakes      omori_aftershock_analytical     Reasenberg-Jones     Generic USGS Parameters Poisson Likelihood   OPERATIONAL
Earthquakes      earthquakes_max_aftershock_mag  XGBoost Regressor    USGS ComCat Sequences   R2: 0.344 (MAE 1.56) EXPERIMENTAL
Earthquakes      earthquakes_aftershock_count    Gradient Boosting    USGS ComCat Sequences   R2: -0.0401 (FAILED) STRICTLY QUARANTINED
Wildfires        wildfires_wildfire_occurrence   CatBoost (Isotonic)  NASA FIRMS + ERA5 NWP   ROC-AUC: 0.879       OPERATIONAL
Wildfires        wildfires_fire_severity_frp     CatBoost Regressor   NASA FIRMS FRP Series   R2: 0.215 (MAE 1.00) EXPERIMENTAL
Wildfires        wildfires_fire_duration         Gradient Boosting    NASA FIRMS Clustered    R2: -214.75 (FAILED) STRICTLY QUARANTINED
Cyclones         cyclones_rapid_intensification  XGBoost (Sigmoid)    NOAA IBTrACS + NHC      ROC-AUC: 0.871       OPERATIONAL
Cyclones         cyclones_intensity_change_24h   XGBoost Regressor    NOAA IBTrACS 150-yr     R2: 0.443 (MAE 10kt) OPERATIONAL
======================================================================================================================================
```

---

## 3. Strict Quarantine Records & Governance Safeguards

### 3.1 Earthquake Aftershock Count Model (`earthquakes_aftershock_count`)
- **Validation Score:** $R^2 = -0.0401$ (Negative Predictive Skill).
- **Physical Reason for Failure:** Static point features cannot model the complex, chaotic stress transfers that govern discrete aftershock event counts.
- **Enforcement:** Hard-coded in `backend/app/services/model_registry.py` with governance status `BLOCKED`.
- **Operational Replacement:** Analytical Reasenberg-Jones Poisson probability ($P(N \ge 1)$).

### 3.2 Wildfire Duration Model (`wildfires_fire_duration`)
- **Validation Score:** $R^2 = -214.75$ (Extreme Variance Inflation).
- **Physical Reason for Failure:** Fire duration is predominantly governed by human firefighting tactics, bulldozed fuelbreaks, and aerial retardant drops, which are unobservable in synoptic weather rasters.
- **Enforcement:** Hard-coded in `model_registry.py` with governance status `BLOCKED`.
- **Operational Replacement:** Satellite Fire Radiative Power (FRP in Megawatts) and Canadian FWI fire danger rating.

---

## 4. Probability Calibration Benchmarks

Models were evaluated on independent holdout splits before and after Bayesian odds calibration:

| Hazard Domain | Raw Model Score (Brier) | Calibrated Score (Brier) | Expected Calibration Error (ECE) |
| :--- | :--- | :--- | :--- |
| **Floods** | $0.1915$ | **$0.0048$** | $0.0214$ |
| **Landslides** | $0.2341$ | **$0.0021$** | $0.0189$ |
| **Earthquakes** | $0.2787$ | **$0.0012$** | $0.0142$ |
| **Wildfires** | $0.1973$ | **$0.0033$** | $0.0238$ |
| **Cyclones** | $0.1000$ | **$0.0019$** | $0.0195$ |

*Conclusion:* Applying empirical climatological priors drops Brier Scores below $0.005$, ensuring predicted probabilities correspond to true empirical disaster occurrence frequencies.

---

## 5. TreeSHAP Attribution Distributions

Each operational model incorporates on-the-fly local Shapley feature attributions:
- Explanations compute positive margin log-odds deviations in $< 15\text{ ms}$.
- Output provides quantitative feature weights and direction (`RISK_INCREASING` vs `RISK_DECREASING`).
- Precludes false causal interpretations: TreeSHAP measures statistical attribution, not Pearlian causal intervention.
