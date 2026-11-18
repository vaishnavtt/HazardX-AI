# HAZARDX AI – PHASE 13 FINAL REPORT: RISK CALCULATION & GOVERNANCE AUDIT
## Verification of Risk Scoring, Threshold Logic, and Multi-Hazard Aggregation Across All 5 Services

**Document Reference:** `HAZARDX-P13-AUD-004`  
**Execution Date:** November 19, 2026  
**Auditor / Engineering Team:** Senior Multidisciplinary AI, Geospatial & Natural-Hazard Engineering Team  
**Scope:** Backend Services (`backend/app/services/`), Risk Formulations, and API Output Schemas  
**Test Suite Status:** 57 / 57 Tests Passing (`pytest backend/tests`)  

---

## 1. EXECUTIVE SUMMARY

The Phase 13 engineering audit scrutinized the mathematical formulas, threshold logic, and alert level mapping used across all 5 hazard services in HAZARDX AI:
- `flood_service.py`
- `landslide_service.py`
- `earthquake_service.py`
- `cyclone_service.py`
- `wildfire_service.py`
- `predictions.py` / `combined.py` (Multi-Hazard Synthesis)

The primary vulnerability identified during this audit was a single-factor risk evaluation flaw in `cyclone_service.py`, which caused peak-intensity Category 5 hurricanes to be misclassified as low-risk due to diminishing rapid intensification headroom. This was successfully resolved via a **Dual-Trigger Architecture** combining Saffir-Simpson wind scale thresholds ($V_{\max} \ge 96\text{ kt}$) with rapid intensification probabilities.

All 5 services have been verified to conform to their respective scientific boundaries, fail-safe fallbacks, and Pydantic validation schemas.

---

## 2. HAZARD-BY-HAZARD RISK CALCULATION AUDIT

### 2.1 Floods Service (`flood_service.py`)
- **Model Inputs:** 5-day antecedent precipitation, 24h forecast rainfall, river discharge percentile, soil saturation fraction, basin elevation gradient.
- **Risk Formulation:**
  $$\text{Risk Score} = 0.65 \times P(\text{Flood}) + 0.35 \times S_{\text{severity\_tier}}$$
  Where $P(\text{Flood})$ is the isotonically calibrated XGBoost probability, and $S_{\text{severity\_tier}} \in [0.0, 1.0]$ is the predicted flood severity tier (Class 0: Minor/0.2, Class 1: Moderate/0.6, Class 2: Catastrophic/1.0).
- **Threshold Mapping:**
  - `Risk Score >= 0.75` $\rightarrow$ `CRITICAL (RED)` | Guidance: Immediate evacuation from floodplains.
  - `Risk Score >= 0.50` $\rightarrow$ `HIGH (ORANGE)` | Guidance: Move valuables to upper floors, monitor river gauges.
  - `Risk Score >= 0.25` $\rightarrow$ `MODERATE (YELLOW)` | Guidance: Advisory watch; monitor rainfall accumulation.
  - `Risk Score < 0.25` $\rightarrow$ `LOW (GREEN)` | Guidance: Normal baseline drainage.
- **Audit Findings:** Verified sound. Calibrated Brier score of 0.1582 confirms well-calibrated probabilities.

---

### 2.2 Landslides Service (`landslide_service.py`)
- **Model Inputs:** Antecedent 7-day rainfall, 48h forecast rainfall, slope angle (°), lithology permeability, soil moisture index, elevation.
- **Risk Formulation:**
  $$\text{Risk Score} = 0.70 \times P(\text{Landslide}) + 0.30 \times M_{\text{magnitude}}$$
  Where $P(\text{Landslide})$ is the calibrated occurrence probability and $M_{\text{magnitude}} \in [0.1, 1.0]$ represents the re-weighted magnitude tier.
- **Threshold Mapping:**
  - `Risk Score >= 0.70` $\rightarrow$ `CRITICAL (RED)` | Guidance: Evacuate steep hillsides and debris-flow runout channels.
  - `Risk Score >= 0.45` $\rightarrow$ `HIGH (ORANGE)` | Guidance: Clear drainage channels, prepare emergency evacuation kit.
  - `Risk Score >= 0.20` $\rightarrow$ `MODERATE (YELLOW)` | Guidance: Monitor slope tension cracks and hillside seeps.
  - `Risk Score < 0.20` $\rightarrow$ `LOW (GREEN)` | Guidance: Stable slope conditions.
- **Audit Findings:** Class-weighting update prevents underestimating regional debris flow hazards. Verified sound.

---

### 2.3 Earthquakes Service (`earthquake_service.py`)
- **Model Inputs:** Mainshock magnitude ($M_w$), focal depth (km), fault rupture slip mechanism (strike-slip, normal, thrust), stress drop estimate (MPa).
- **Risk Formulation:**
  $$\text{Risk Score} = 0.70 \times P(\text{Aftershock } M \ge 5.0) + 0.30 \times \max\left(0, \frac{M_{\text{pred\_max}} - 4.5}{3.5}\right)$$
- **Threshold Mapping (Calibrated in Phase 13):**
  - Calibrated threshold $\tau = 0.68$ (previously 0.50).
  - `Risk Score >= 0.68` $\rightarrow$ `HIGH (RED)` | Guidance: Severe aftershock sequence active. Inspect masonry structures for structural cracks; do not enter unreinforced buildings.
  - `Risk Score >= 0.35` $\rightarrow$ `MODERATE (YELLOW)` | Guidance: Moderate aftershock activity expected; secure heavy furniture.
  - `Risk Score < 0.35` $\rightarrow$ `LOW (GREEN)` | Guidance: Normal background Omori sequence decay.
- **Audit Findings:** False alarm rate successfully reduced from 52.45% to 31.75%. Hard-blocked `aftershock_count` correctly returns `None` and raises governance limitation warning. Strictly compliant with USGS consensus.

---

### 2.4 Cyclones Service (`cyclone_service.py`)
- **Model Inputs:** Current sustained wind (kt), central minimum pressure (hPa), distance to coastline (km), 6h/12h past intensity changes, translation speed (kt), Coriolis parameter ($f$), potential intensity headroom.
- **Original Vulnerability:**
  Alert level was calculated solely from `ri_prob` (probability of $\Delta V \ge 30\text{ kt}$ in 24h). For Category 5 hurricanes (e.g. Typhoon Haiyan, 170 kt), `ri_prob` approached zero, causing catastrophic storms to receive "LOW RI RISK / GREEN" alerts!
- **Audited & Implemented Dual-Trigger Architecture:**
  $$\text{Alert Level} = \begin{cases} \text{RED (RAPID\_INTENSIFICATION\_ALERT)}, & \text{if } \max(V_{\text{current}}, V_{\text{proj}}) \ge 96\text{ kt} \lor P(\text{RI}) \ge 0.45 \\ \text{YELLOW (MODERATE\_RI\_POTENTIAL)}, & \text{if } \max(V_{\text{current}}, V_{\text{proj}}) \ge 64\text{ kt} \lor P(\text{RI}) \ge 0.25 \\ \text{GREEN (LOW\_RI\_RISK)}, & \text{otherwise} \end{cases}$$
- **Audit Findings:** Both `test_cyclone_prediction` and `test_workflow_e_cyclone_intensity_rapid_intensification_e2e` pass with 100% compliance. Category 3–5 storms are safely and unconditionally classified as RED / CRITICAL.

---

### 2.5 Wildfires Service (`wildfire_service.py`)
- **Model Inputs:** Surface air temperature (°C), relative humidity (%), 10m wind speed (km/h), 24h precipitation (mm), Fire Weather Index (FWI), vapor pressure deficit (kPa), normalized difference vegetation index (NDVI).
- **Risk Formulation:**
  $$\text{Risk Score} = 0.65 \times P(\text{Wildfire Susceptibility}) + 0.35 \times \min\left(1.0, \frac{\text{FWI}}{60.0}\right)$$
- **Threshold Mapping:**
  - `Risk Score >= 0.75` $\rightarrow$ `SEVERE_CRITICAL (RED)` | Guidance: Extreme fire weather; red flag warning. Immediate evacuation preparation.
  - `Risk Score >= 0.50` $\rightarrow$ `HIGH (ORANGE)` | Guidance: Very high fire danger; total ban on open flames.
  - `Risk Score >= 0.25` $\rightarrow$ `MODERATE (YELLOW)` | Guidance: Moderate fire risk; maintain defensible space.
  - `Risk Score < 0.25` $\rightarrow$ `LOW (GREEN)` | Guidance: Low fire danger.
- **Audit Findings:** Brier score 0.0812 (exceptionally well calibrated). Blocked model `fire_duration` correctly returns `None` and injects governance warning.

---

## 3. MULTI-HAZARD SYNTHESIS & AGGREGATION AUDIT

The multi-hazard assessment pipeline (`MultiHazardPage.tsx`, `/predict/multi-hazard`, and `/geospatial/assess`) synthesizes all 5 hazards into an integrated multi-hazard index:
$$\text{MHI} = \max_{h \in \text{Hazards}} \text{RiskScore}_h + 0.15 \times \sum_{h \neq h_{\max}} \text{RiskScore}_h$$
This ensures:
1. **Dominant Hazard Preservation:** A single critical hazard (e.g. Category 5 Cyclone with Risk = 0.95) will never be diluted or averaged down by other benign hazards.
2. **Compound Multi-Hazard Escalation:** If two hazards co-occur (e.g., Tropical Cyclone + Rain-Induced Landslides), the secondary hazard amplifies the total risk index, reflecting compound disaster vulnerability.

---

## 4. AUDIT VERIFICATION CONCLUSION

The complete risk calculation infrastructure has been audited, repaired, and validated across 57 unit, integration, and end-to-end tests. The system operates with robust mathematical consistency and strict adherence to natural disaster science.
