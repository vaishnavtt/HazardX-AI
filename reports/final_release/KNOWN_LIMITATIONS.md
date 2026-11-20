# HAZARDX AI — KNOWN SCIENTIFIC & TECHNICAL LIMITATIONS
**Document ID:** `HX-RPT-REL-05`  
**Phase:** Phase 47 — Final Scientific and Product Verification  
**Author:** Multidisciplinary Senior Engineering Team  
**Date:** November 20, 2026  
**Status:** PUBLIC DISCLOSURE & BOUNDARIES  

---

## 1. Executive Notice

HAZARDX AI is an advanced, automated decision-support platform designed to synthesize multi-hazard intelligence, forecast hazard trajectories, and evaluate environmental risk probabilities. 

**IT IS NOT A STATUTORY CIVIL DEFENSE EVACUATION AUTHORITY.**  
Sovereign civil protection agencies (e.g. NDMA, USGS, NOAA, JMA, PAGASA) hold exclusive statutory authority to issue binding public warnings and evacuation mandates.

---

## 2. Fundamental Scientific Boundaries

### 2.1 Deterministic Earthquake Prediction is Scientifically Impossible
- **Scientific Fact:** Earthquake nucleation involves unobservable microscopic fault friction and chaotic stress transfer. No methodology exists in modern geophysics to deterministically forecast the exact time, location, and magnitude of an impending earthquake.
- **System Policy:** HAZARDX AI strictly adheres to USGS policy. Models **only** evaluate statistical post-mainshock secondary aftershock decay (Omori-Utsu / Reasenberg-Jones) conditional on an observed seismic event ($M_w \ge 4.0$). Any attempt to use HAZARDX AI for deterministic prediction is explicitly warned against in all API responses.

### 2.2 Permanent Quarantine of Low-Performing Models
Two regression models developed during earlier development phases exhibited negative predictive skill on holdout sets and are **strictly quarantined**:
1. `earthquakes_aftershock_count` ($R^2 = -0.0401$): Discrete count estimation from static point features violates stochastic spatial point-process dynamics. Quarantined in favor of analytical Poisson probabilities.
2. `wildfires_fire_duration` ($R^2 = -214.75$): Active fire duration is heavily dictated by human firefighting suppression tactics, micro-fuelbreaks, and aircraft retardant drops which are unobservable in synoptic weather grids. Quarantined in favor of satellite Fire Radiative Power (FRP).

### 2.3 Spatial Resolution Limits & Micro-Scale Blind Spots
- **GloFAS Hydro Routing (0.05° / ~5 km):** Accurately models major river reach inundations. It **cannot** model hyper-local urban street pluvial ponding caused by clogged municipal storm drains.
- **Copernicus DEM (90m):** Represents regional macro-topography. Localized road embankment cuts, highway retaining walls, or localized construction excavations may exhibit micro-slopes steeper than the 90m raster average.
- **ERA5 NWP Reanalysis (0.1° / ~10 km):** Synoptic weather grids may smooth localized orographic cloudburst peaks (e.g., micro-burst convective thunderstorms).

### 2.4 Case-Control Training Distribution vs Real-World Base Rates
Machine learning models trained on 1:1 case-control historical disaster datasets output raw scores reflecting balanced samples. While HAZARDX AI applies Bayesian log-odds adjustments ($\text{logit}(p) = \text{logit}(p_{\text{model}}) + \ln(\pi / (1-\pi))$) with empirical climatological priors ($\pi = 0.001 - 0.005$), rare black-swan compound disasters may still deviate from historical statistical distributions.

---

## 3. Technical & Operational Boundaries

1. **Third-Party API Outages:** If upstream scientific providers (USGS, Open-Meteo, GloFAS) suffer network downtime, the system falls back to regional climatological baselines. The system explicitly tags outputs with `data_provenance: "FALLBACK"` and includes warning notices.
2. **Satellite Orbital Delays:** NASA FIRMS satellite thermal passes occur 2 to 4 times daily per constellation (MODIS / VIIRS). Thermal hotspots represent recent satellite observations (3-hour latency), not zero-second telemetry.

---

## 4. Sign-Off

These limitations represent transparent scientific boundaries. Documenting them clearly preserves the integrity of HAZARDX AI as an honest, defensible research prototype and decision-support system.
