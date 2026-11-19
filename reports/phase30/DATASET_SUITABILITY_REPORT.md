# HAZARDX AI – Phase 30: Dataset Suitability Report

**Date:** November 19, 2026  
**Auditor:** Disaster Risk Scientist & AI/ML Validation Group  
**Scope:** Scientific & Operational Suitability Analysis of All 5 Hazard Pipelines  

---

## 1. Hazard-by-Hazard Suitability Assessment

### 1.1 Tropical Cyclones
- **Target Phenomenon:** Rapid Intensification ($\Delta V \ge 30\text{ kt} / 24\text{h}$) and 24-hour wind change ($\Delta V$).
- **Data Source:** NOAA IBTrACS v04r01 (1980–2024 global best-track catalog).
- **Physical Representation:** Authentic synoptic track observations recorded at 6-hour intervals with authentic central pressure, sustained winds, translational speed, and distance to land.
- **Suitability:** **HIGHLY SUITABLE** for active tropical storms.
- **Operational Boundary:** Must be executed *only* when an active tropical disturbance or storm is detected within the relevant oceanic basin. Applying the model to an inland coordinate with dummy storm values is physically invalid.

### 1.2 Earthquakes
- **Target Phenomenon:** Elevated conditional aftershock hazard following a mainshock ($M \ge 4.5$).
- **Data Source:** USGS Comprehensive Earthquake Catalog (ComCat).
- **Physical Representation:** Authentic seismic events with focal depth, fault distance, and empirical aftershock sequences.
- **Suitability:** **HIGHLY SUITABLE** for post-mainshock conditional hazard assessment.
- **Operational Boundary:** In strict compliance with USGS scientific policy, deterministic mainshock prediction is impossible. The dataset models conditional aftershock rate decay $\lambda(t) = K / (t + c)^p$. If no qualifying mainshock has occurred in the region, the operational state must be strictly reported as `QUIESCENT` (zero aftershock probability).

### 1.3 Floods
- **Target Phenomenon:** River reach inundation occurrence and stage severity.
- **Data Source:** Dartmouth Flood Observatory (DFO) and GloFAS hydrological simulations.
- **Physical Representation:** Identifies historical river reach inundation boundaries.
- **Suitability:** **MODERATE / CONDITIONAL**.
- **Operational Boundary:** Highly capable of identifying excessive runoff and discharge anomalies when integrated with GloFAS. However, coarse basin discharge ($5\text{ km}$) cannot be extrapolated to street-level urban flash floods without local storm drainage models.

### 1.4 Landslides
- **Target Phenomenon:** Rainfall-triggered hillslope failure and failure magnitude.
- **Data Source:** NASA Global Landslide Catalog (GLC) points and Copernicus 30m DEM.
- **Physical Representation:** Authentic landslide failure scars.
- **Suitability:** **MODERATE / CONDITIONAL**.
- **Operational Boundary:** Terrain features (slope, aspect, curvature, TWI) represent permanent **geographic susceptibility**, whereas rainfall ($p_1, p_3, p_{30}$) represents the **transient trigger**. The model is suitable only when both components are explicitly separated in the risk calculation.

### 1.5 Wildfires
- **Target Phenomenon:** Surface fire ignition susceptibility and Fire Radiative Power (FRP).
- **Data Source:** NASA FIRMS satellite active fire detections (VIIRS/MODIS).
- **Physical Representation:** Satellite-detected thermal anomalies.
- **Suitability:** **UNSUITABLE IN CURRENT FORM** for tropical / monsoonal zones without physical FWI and FIRMS gating.
- **Operational Boundary:** The model cannot be used as an unconstrained global temperature regressor. Wildfire assessment must be governed primarily by the Canadian Forest Fire Weather Index (FWI) danger scale and real-time NASA FIRMS thermal anomaly detection within a localized radius ($50\text{ km}$).

---

## 2. Suitability Decision Matrix

| Hazard Domain | Operational Deployment Mode | Required Physical Pre-Condition |
| :--- | :--- | :--- |
| **Cyclones** | Gated Event Forecast | Active storm tracked within $800\text{ km}$ of coastal marine coordinate. |
| **Earthquakes** | Gated Aftershock Assessment | Qualifying mainshock ($M \ge 4.0$) observed within $100\text{ km}$ in past 30 days. |
| **Floods** | Hybrid Hydrological Model | Evaluates GloFAS discharge ratio + NWP rainfall infiltration against return periods. |
| **Landslides** | Decoupled Susceptibility & Trigger | High slope susceptibility ($> 20^\circ$) coupled with real-time antecedent rainfall saturation. |
| **Wildfires** | Multi-Factor Physical & Hotspot Engine | Canadian FWI rating combined with NASA FIRMS satellite hotspot detection within $50\text{ km}$. |
