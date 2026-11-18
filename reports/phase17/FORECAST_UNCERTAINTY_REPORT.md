# HAZARDX AI – PHASE 17 REPORT: FORECAST UNCERTAINTY QUANTIFICATION
## Prediction Intervals, Calibration Bands, Data Completeness & Uncertainty Reporting

**Document Reference:** `HAZARDX-P17-UNC-004`  
**Execution Date:** November 19, 2026  
**Auditor / Engineering Team:** Senior Disaster Risk Scientist & Statistical Modeler  
**Core Methodology:** Residual Distribution Analysis & Uncertainty Bounds  

---

## 1. THE IMPERATIVE OF UNCERTAINTY COMMUNICATION

Deterministic single-point predictions (e.g., *"Wind speed will increase by exactly 18.2 knots"* or *"Flood probability is exactly 84.1%"*) present a dangerous illusion of certainty in complex natural systems.

In accordance with Phase 17 requirements, HAZARDX AI quantifies and communicates three dimensions of uncertainty:
1. **Model Parameter & Residual Uncertainty:** Prediction intervals based on empirical test set error distributions.
2. **Probability Calibration Uncertainty:** Calibrated confidence bands mapping model confidence to real-world frequencies.
3. **Data Completeness Uncertainty:** Telemetry coverage penalties when local sensors or NWP grids are degraded.

---

## 2. PREDICTION INTERVALS FOR REGRESSION PIPELINES

For continuous regression forecasts, prediction intervals are computed using the empirical holdout residual standard errors ($\sigma_{\text{residual}}$) derived in Phase 15:

### 2.1 Tropical Cyclone 24h Intensity Change
- **Model:** `cyclones_intensity_change_24h`
- **Mean Absolute Error (MAE):** $10.03\text{ knots}$ | **Root Mean Squared Error (RMSE):** $13.99\text{ knots}$
- **Residual Distribution:** Zero-mean Gaussian ($\mu = 0.08\text{ kt}, \sigma = 13.98\text{ kt}$).
- **Operational Prediction Interval (90% Confidence):**
  $$\hat{V}_{24\text{h}} = V_{\text{current}} + \Delta \hat{V} \quad \pm \quad 1.645 \times 13.99\text{ kt} \quad \approx \quad \Delta \hat{V} \pm 23.0\text{ knots}$$
- **UI Communication:** The forecast center displays the median projection with an explicit $\pm 14\text{ kt}$ expected error cone, expanding to $\pm 24\text{ kt}$ at 48h.

### 2.2 Maximum Expected Aftershock Magnitude (Mw)
- **Model:** `earthquakes_max_aftershock_mag` (Experimental)
- **RMSE:** $1.94\text{ magnitude units}$ | **Median Absolute Error:** $1.28\text{ Mw}$
- **Operational Prediction Interval:**
  $$\hat{M}_{\text{max\_aftershock}} \pm 1.5\text{ Mw}$$
- **Governance Constraint:** Because the uncertainty interval ($\pm 1.5\text{ Mw}$) spans three full orders of seismic energy release, this model is labeled **EXPERIMENTAL / ADVISORY ONLY** and is strictly prohibited from triggering standalone sirens.

---

## 3. PROBABILITY CALIBRATION BANDS & CONFIDENCE FLAGS

For classification pipelines, raw probabilities are mapped through isotonic and sigmoid calibration curves to provide genuine empirical confidence:

```
[Raw Probability: 0.82] 
          |
          v
[Isotonic Calibration Curve (Phase 15)] 
          |
          v
[Calibrated Empirical Frequency: 0.78 +/- 0.06]
          |
          v
[UI Display: "HIGH RISK: 78% Observed Frequency in Similar Historical Settings"]
```

### Confidence Level Flagging:
- **HIGH CONFIDENCE (Flag: Green):** All required inputs present; observation age $< 1\text{ hour}$; forecast horizon $\le 24\text{ hours}$.
- **MODERATE CONFIDENCE (Flag: Amber):** Forecast horizon between 24h and 48h; or secondary input (e.g. soil moisture) estimated via ERA5 reanalysis stencil.
- **LOW CONFIDENCE / HIGH UNCERTAINTY (Flag: Red/Orange):** Forecast horizon $> 48\text{ hours}$; or critical upstream sensor (e.g. river gauge) reporting stale telemetry ($> 6\text{ hours}$).

---

## 4. DATA COMPLETENESS PENALTIES

When assessing a remote location where physical sensors are sparse:
- If a river discharge station is $> 50\text{ km}$ away, the flood service injects an explicit uncertainty disclaimer:
  > *"River-level observations are currently unavailable for this catchment. This assessment is derived from satellite precipitation forecasts and has elevated spatial uncertainty."*
- If seismic fault slip mechanism is unmapped, the earthquake service defaults to conservative strike-slip geometry with an expanded uncertainty margin.

---

## 5. UNCERTAINTY REPORT CONCLUSION

HAZARDX AI sets a high standard for scientific integrity by replacing point predictions with calibrated prediction intervals, confidence ratings, and transparent data completeness warnings.
