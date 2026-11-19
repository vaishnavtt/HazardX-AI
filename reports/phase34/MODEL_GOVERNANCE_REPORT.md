# Phase 34 — Model Governance, Safety Standards and Quarantine Policy

## 1. Executive Summary & Governance Mandate

Natural hazard predictions directly impact human safety, evacuation logistics, and civil emergency response. Delivering unvalidated or statistically invalid models can lead to either tragic loss of life (false negative) or catastrophic loss of public trust and economic disruption (false alarm).

The HAZARDX AI Model Governance Framework enforces strict operational criteria for all machine learning models before they can be promoted to production.

---

## 2. Operational Model Qualification Gates

To achieve `OPERATIONAL` status in the model registry, every pipeline must pass four mandatory gates:
1. **Gate 1 (Scientific Grounding):** The physical target must be strictly defined and bounded. Deterministic earthquake prediction is strictly prohibited.
2. **Gate 2 (Generalization Quality):** Test set coefficient of determination $R^2 \ge 0.15$ (for regression) or ROC-AUC $\ge 0.75$ (for classification) under spatial block cross-validation. Models with negative test $R^2$ are disqualified.
3. **Gate 3 (Calibration Verification):** Expected Calibration Error (ECE) $\le 0.05$ across test deciles.
4. **Gate 4 (Physical Gating Compliance):** The model must be wrapped in deterministic domain pre-condition gates (e.g., zero rain $\implies$ low flood risk; no storm within 800 km $\implies$ zero cyclone threat).

---

## 3. Quarantined & Blocked Models

Two models in the HAZARDX AI registry failed to satisfy governance standards and are **strictly quarantined from operational inference**:

### 3.1 Earthquake Aftershock Count Model (`earthquakes_aftershock_count`)
- **Status:** `BLOCKED` / `QUARANTINED`
- **Failure Metric:** Test $R^2 = -0.0401$.
- **Root Cause:** Aftershock sequence counts exhibit heavy-tailed Pareto dispersion with extreme spatial clustering. Linear and gradient boosted regressors fitted to small regional samples failed to generalize and performed worse than predicting the sample mean.
- **Enforcement:** The model is suppressed. Secondary predictions return `None`, accompanied by an explicit governance notice: `"Aftershock count regression model is STRICTLY BLOCKED (R² = -0.0401; suppressed)."`.

### 3.2 Wildfire Duration Model (`wildfires_fire_duration`)
- **Status:** `BLOCKED` / `QUARANTINED`
- **Failure Metric:** Test $R^2 = -214.75$.
- **Root Cause:** Wildfire duration is primarily determined by human suppression efforts (firefighter deployment, air tanker drops, backburning) and shifting synoptic weather fronts over weeks, features absent from satellite snapshot telemetry.
- **Enforcement:** Model inference is strictly suppressed. Outputs return `None` with an advisory flag in all API responses.

---

## 4. Operational Model Inventory Summary

| Model Identifier | Domain | Target | Algorithm | Status | Version |
|---|---|---|---|---|---|
| `floods_flood_occurrence` | Floods | Fluvial River Inundation | Calibrated XGBoost | `OPERATIONAL` | v1.0.0 |
| `floods_flood_severity` | Floods | Severity Classification (1–3) | Calibrated XGBoost | `OPERATIONAL` | v1.0.0 |
| `landslides_landslide_occurrence` | Landslides | Rainfall Slope Failure | Calibrated XGBoost | `OPERATIONAL` | v1.0.0 |
| `landslides_hazard_magnitude` | Landslides | Mass Movement Scale | Calibrated XGBoost | `OPERATIONAL` | v1.0.0 |
| `wildfires_wildfire_occurrence` | Wildfires | Ignition Susceptibility | Calibrated XGBoost + FWI | `OPERATIONAL` | v1.0.0 |
| `wildfires_frp_intensity` | Wildfires | Log Fire Radiative Power | Random Forest | `EXPERIMENTAL` | v1.0.0 |
| `wildfires_fire_duration` | Wildfires | Fire Duration (Days) | Gradient Boosted Regressor | **`BLOCKED`** | v1.0.0 |
| `earthquakes_aftershock_hazard` | Earthquakes | Omori Aftershock Sequence | Omori-Utsu Formulation | `OPERATIONAL` | v1.0.0 |
| `earthquakes_aftershock_count` | Earthquakes | Expected Aftershock Count | Poisson / XGBoost | **`BLOCKED`** | v1.0.0 |
| `cyclones_rapid_intensification` | Cyclones | $\Delta V \ge 30\text{ kt}$ in 24h | Calibrated XGBoost | `OPERATIONAL` | v1.0.0 |
| `cyclones_intensity_change` | Cyclones | 24h Intensity Delta (kt) | Gradient Boosted Regressor | `OPERATIONAL` | v1.0.0 |
