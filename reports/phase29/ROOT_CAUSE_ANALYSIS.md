# HAZARDX AI – Phase 29: Root Cause Analysis Report

**Date:** November 19, 2026  
**Auditor:** Senior Multi-Disciplinary Engineering & QA Team  
**Scope:** Formal Taxonomy & Root Cause Classification of Prediction Pipeline Defects  

---

## 1. Formal Root Cause Taxonomy & Defect Mapping

Every identified issue in the HAZARDX AI prediction and location assessment pipeline has been classified into the required standard categories:

### 1. `FEATURE_MAPPING_ERROR` [CRITICAL]
- **Issue 1A (Formula Divergence in FWI):** The wildfire dataset preparation script (`build_wildfire_dataset.py`) computed an empirical FWI proxy $(T + \Delta RH) \cdot W \cdot R \cdot 0.15$ with range $0–100$ and median $6.0$. Conversely, live inference (`weather_features.py`) computed the McArthur exponential FWI equation. The model evaluated tree split thresholds calibrated on a completely different numerical scale.
- **Issue 1B (Precipitation Window Multipliers):** Live multi-day precipitation ($3\text{d}, 7\text{d}, 14\text{d}$) was approximated via heuristic multipliers ($p_1 \times 1.5$, $p_1 \times 1.8$) instead of extracting actual accumulated multi-day totals from ERA5 reanalysis.

### 2. `RISK_LOGIC_ERROR` [CRITICAL]
- **Issue 2A (Arbitrary Seismic Feature Substitution):** In `spatial_feature_service.py`, when a radial USGS seismicity query returned 0 events within $100\text{ km}$, the code defaulted `mainshock_mag = 6.0` and `depth = 10.0 km`. This injected a non-existent $M 6.0$ major earthquake into the aftershock model.
- **Issue 2B (Fictitious Cyclone Injection):** In `geospatial.py`, any location with $|\text{lat}| \le 45^\circ$ was subjected to cyclone evaluation with dummy parameters (`current_wind_kt = 45.0`, `dist_to_land_km = 85.0`), even for inland mountain valleys thousands of kilometers from tropical cyclones.
- **Issue 2C (Raw Score Categorization):** Downstream service layers (`wildfire_service.py`, `geospatial.py`) categorized alert levels and risk tiers using `raw_prob` from 1:1 case-control models rather than the calibrated real-world probabilities or established physical danger indices.

### 3. `MODEL_QUALITY_ERROR` & `GEOGRAPHIC_TRANSFER_ERROR` [HIGH]
- **Issue 3A (Synthetic Training Weather Distributions):** In `build_wildfire_dataset.py`, weather features for fire events were generated from $\mathcal{N}(32.5, 5.0)$ and non-events from $\mathcal{N}(18.0, 6.0)$. The model learned a severe positive temperature bias ($+2.08$ SHAP log-odds). When queried for tropical regions (like Wayanad at $26.5^\circ\text{C}$), the ambient warmth alone pushed the model score into elevated risk ($56\%–61\%$), regardless of humidity ($47\%$) or precipitation ($118\text{ mm}$).
- **Issue 3B (Lack of Tropical Fire Training Data):** Training fires were predominantly sampled from high-latitude North American boreal forests (median latitude $52.5^\circ\text{N}$, median temperature $11.95^\circ\text{C}$), causing failure when transferring to tropical monsoonal ecosystems.

### 4. `MODEL_CALIBRATION_ERROR` [HIGH]
- **Issue 4A (Uncalibrated Presentation):** Although `adjust_case_control_probability()` was implemented to adjust for climatological base rates ($0.002$), the calibrated probability ($0.0025$) was discarded, and the raw case-control score ($0.558$) was passed directly to the frontend display.
- **Issue 4B (Lack of Empirical Isotonic / Platt Calibration):** The models relied solely on synthetic testing splits without empirical reliability diagram calibration or Platt scaling against observed real-world base rates.

### 5. `FRONTEND_DISPLAY_ERROR` [MEDIUM]
- **Issue 5A (Misleading "Threat Score" Labeling):** In `LocationAssessmentPage.tsx`, raw model scores were rendered as:
  ```tsx
  Estimated Threat Score: {((hData.probability || 0.1) * 100).toFixed(0)}%
  ```
  This misled users into interpreting raw XGBoost classification scores as real-world probabilities of a disaster occurring today.
- **Issue 5B (Hardcoded Metadata):** The frontend hardcoded strings such as `Horizon: 24h` and `Driven primarily by...` without dynamic binding to model horizon validations.

### 6. `FORECAST_ERROR` [MEDIUM]
- **Issue 6A (Conflation of Susceptibility and Event Forecast):** The system failed to distinguish between **long-term geographic susceptibility** (e.g. Wayanad's steep mountain slopes with high historical landslide risk) and **short-term triggering forecast** (dry weather today with zero rainfall infiltration).

---

## 2. Root Cause Summary Matrix

| Defect Identifier | Root Cause Category | Severity | Primary Remediating Phase |
| :--- | :--- | :--- | :--- |
| **Wayanad Wildfire 60% False Alarm** | `MODEL_QUALITY_ERROR` / `FEATURE_MAPPING_ERROR` / `RISK_LOGIC_ERROR` | CRITICAL | Phase 31 & Phase 32 |
| **Wayanad Earthquake 18% Aftershock** | `RISK_LOGIC_ERROR` | CRITICAL | Phase 32 |
| **Inland Mountain Cyclone Threat (27%)**| `RISK_LOGIC_ERROR` / `GEOGRAPHIC_TRANSFER_ERROR` | CRITICAL | Phase 32 |
| **FWI Calculation Mismatch** | `FEATURE_MAPPING_ERROR` | HIGH | Phase 30 & Phase 32 |
| **Disregard of Calibrated Probability** | `MODEL_CALIBRATION_ERROR` | HIGH | Phase 33 |
| **Synthetic Weather Distributions** | `MODEL_QUALITY_ERROR` | HIGH | Phase 30 & Phase 31 |
| **Misleading Frontend Percentages** | `FRONTEND_DISPLAY_ERROR` | MEDIUM | Phase 36 |
| **Susceptibility vs Event Confusion** | `FORECAST_ERROR` | HIGH | Phase 32 |

---

## 3. Engineering Action Plan for Phases 30–36

1. **Phase 30 (Dataset Quality & Suitability):** Audit all 5 hazard datasets, replace synthetic distributions with authentic physical/meteorological observations, and resolve geographic distribution shifts.
2. **Phase 31 (Model Rebuild & Improvement):** Retrain models with standardized features, eliminate temperature-overfitting in wildfires, test alternative algorithms (XGBoost with constrained monotonicity, Random Forest baselines), and establish strict model promotion gates.
3. **Phase 32 (Real-Time Risk Calculation Engine):** Redesign `spatial_feature_service.py` and `forecast_service.py`. Enforce physical preconditions:
   - *Seismic:* No qualifying mainshock $\to$ Aftershock probability $= 0.0\%$, status `QUIESCENT`.
   - *Cyclone:* No active storm within danger radius $\to$ Threat $= \text{NONE}$.
   - *Wildfire:* Incorporate NASA FIRMS active fire detection + Canadian FWI danger rating.
   - *Landslide/Flood:* Explicitly separate terrain susceptibility from short-term rainfall triggering.
4. **Phase 33 (Calibration & Validation):** Apply Platt scaling / isotonic regression, evaluate Brier scores and reliability curves, and validate multi-horizon skill decay across 6h, 12h, 24h, 48h, 72h.
5. **Phase 34 (Monitoring & Governance):** Implement live input drift detection and automatic safety gates for missing or out-of-bounds telemetry.
6. **Phase 35 (Real-World & Wayanad Validation):** Replay historical disasters and test non-event conditions across Wayanad, Kerala locations, and global test sites.
7. **Phase 36 (Frontend & Verification):** Modernize UI hazard cards to display verified risk factors, calibrated probabilities, and explicit scientific limitations.
