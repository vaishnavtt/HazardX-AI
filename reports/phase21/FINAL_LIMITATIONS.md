# HAZARDX AI — Platform Scientific Limitations & Operational Boundaries (Phase 21)
**Document ID:** `HAZARDX-P21-LIM-005`  
**Scientific Ethics Standard:** Responsible AI for Natural Disasters & WMO Disaster Risk Governance  
**Audit Date:** 2026-11-19  
**Status:** PUBLIC DISCLOSURE & MANDATORY GOVERNANCE  

---

## 1. Executive Summary

Scientific integrity in disaster intelligence requires transparent acknowledgment of model boundaries, observational limits, and epistemic uncertainties. Overstating machine learning capabilities during natural hazards can endanger lives and degrade public trust in emergency communications.

This document outlines the **known physical, observational, computational, and jurisdictional boundaries** of the HAZARDX AI platform.

---

## 2. Quarantined Regression Models (Negative $R^2$)

During rigorous empirical auditing on the holdout test set ($N = 23,561$), two models exhibited negative out-of-sample coefficients of determination:
- **`earthquakes_aftershock_count`:** $R^2 = -0.0401$
- **`wildfires_fire_duration`:** $R^2 = -214.75$

### Physical Diagnostic Rationale:
1. **Unmodeled Human Suppression Dynamics:** Wildfire duration is fundamentally governed by human suppression actions (aerial retardant drops, bulldozed containment lines, initial attack dispatch speed) and fine-scale firefighter tactics that do not exist within satellite environmental datasets. Predicting duration purely from pre-ignition weather produces massive variance ($R^2 < 0$).
2. **Stress Heterogeneity in Seismic Rupture:** Omori-Utsu aftershock sequences are sensitive to micro-scale geometric asperities, fluid pore pressures at 15–30 km depths, and static Coulomb stress transfer details unresolvable by regional catalog features.
3. **Quarantine Invariant:** Both models are **permanently blocked** from operational early warning endpoints (`/api/v1/predict/` and `/api/v1/alerts/`). They remain registered in `/api/v1/models` strictly for academic auditing and transparent governance tracking.

---

## 3. Earthquake Non-Predictability & USGS Compliance

> [!CAUTION]
> **Strict Non-Deterministic Seismic Governance**
> 
> In absolute alignment with the United States Geological Survey (USGS), IASPEI, and the international seismological consensus:
> 1. HAZARDX AI **DOES NOT PREDICT** the date, time, location, or magnitude of future earthquakes.
> 2. No deterministic precursor claims (e.g., thermal anomalies, animal behavior, planetary alignment, ionospheric fluctuations) are recognized or implemented.
> 3. The seismic engine models **post-mainshock statistical clustering** (aftershock susceptibility within 30 days and 100 km) using empirical Gutenberg-Richter and modified Omori law frameworks.

---

## 4. Geospatial Resolution & Micro-Topography Constraints

| Hazard Domain | Underlying Numerical Feed | Spatial Resolution | Operational Limitation |
|---|---|---|---|
| **Floods** | Copernicus GloFAS | $0.1^\circ \times 0.1^\circ$ (~10 km) | Cannot resolve street-level pluvial flash ponding or urban storm sewer backups smaller than basin cell. |
| **Landslides** | NASA GLC & SRTM DEM | $30 \text{ m}$ DEM / $0.1^\circ$ Weather | Deep-seated bedrock failures and roadside excavation cuts require local geotechnical borehole data. |
| **Cyclones** | NOAA NHC / IBTrACS | Storm Center Fix (~5–10 km) | Eyewall mesovortices and localized microburst tornadoes within outer rainbands cannot be individually tracked. |
| **Wildfires** | NASA FIRMS VIIRS | $375 \text{ m}$ pixel footprint | Smoldering ground fires under dense forest canopies may escape satellite radiative thermal detection. |

---

## 5. Temporal Latency and External Stream Dependencies

1. **Satellite Orbit Latency:** NASA FIRMS relies on polar-orbiting satellites (Suomi-NPP, NOAA-20, NOAA-21) providing ~12-hour orbital revisits. Fires ignited between overpasses are tracked primarily through Fire Weather Index (FWI) proxy forecasts until the next thermal pass.
2. **External API Outages:** If global services (USGS, Open-Meteo, GloFAS) encounter network degradation or upstream server maintenance, HAZARDX AI engages exponential backoff and cached baselines. Real-time updates depend on internet connectivity to these open data providers.
3. **Data Freshness Classification:** Users must monitor the `data_freshness` metadata badge (`FRESH`, `RECENT`, `DELAYED`, `STALE`). Advisories marked `STALE` (>12 hours old) must not be relied upon for fast-moving flash floods or rapid fire spread.

---

## 6. Statutory Jurisdiction and Non-Statutory Authority

HAZARDX AI is an artificial intelligence decision-support platform designed to aid researchers, municipal civil defense planners, and emergency analysts.

- **No Evacuation Authority:** HAZARDX AI **never** issues mandatory evacuation orders. Statutory legal authority to order evacuations rests solely with sovereign and municipal civil protection bodies (e.g., FEMA, NDMA, regional prefectures, police, and civil defense agencies).
- **Subordination Clause:** In all operational scenarios, official alerts, sirens, and instructions from national meteorological services (e.g., NWS, IMD, JMA, PAGASA) and local authorities **supersede all HAZARDX AI outputs**.

---

## 7. Limitations Summary

By maintaining transparent scientific boundaries, HAZARDX AI ensures that emergency managers utilize the platform with clear awareness of its strengths and constraints.

**Governance Document: PUBLISHED & ACTIVE**
