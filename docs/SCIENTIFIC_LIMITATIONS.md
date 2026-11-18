# HAZARDX AI — Scientific Limitations & Epistemic Boundaries
**Document ID:** `HAZARDX-DOCS-LIM-006`  
**Platform Version:** `v1.0.0-PROD`  

---

## 1. Executive Disclosure

Natural hazard intelligence systems must operate with absolute transparency regarding what they can and cannot do. Overstating machine learning capabilities in life-critical disaster early warning endangers lives and damages public trust.

This document articulates the verified physical, computational, observational, and statutory boundaries of HAZARDX AI.

---

## 2. Fundamental Scientific Boundaries

### 2.1 Earthquakes: Non-Deterministic Policy
In strict accordance with the **USGS**, **IASPEI**, and global seismological consensus:
1. HAZARDX AI **does not predict** the date, time, location, or magnitude of future earthquakes.
2. The platform implements **statistical post-mainshock clustering** (aftershock susceptibility within 30 days and 100 km) using empirical Gutenberg-Richter and modified Omori law frameworks.
3. No pseudoscientific precursor signals (animal behavior, planetary alignments, ionospheric fluctuations) are recognized.

### 2.2 Quarantined Regression Models (Negative $R^2$)
Two models were proven to fail generalization on the holdout test set:
- **`earthquakes_aftershock_count`** ($R^2 = -0.0401$)
- **`wildfires_fire_duration`** ($R^2 = -214.75$)

**Diagnostic Cause:** Wildfire duration is governed by human firefighting intervention (containment lines, air tanker drops, municipal response) that does not exist in satellite weather data. Similarly, exact aftershock counts depend on unresolvable fault micro-asperities. Both models are **permanently blocked** from operational decision-making endpoints.

---

## 3. Spatial & Temporal Observational Constraints

1. **Hydrological Resolution:** GloFAS $0.1^\circ$ (~10 km) cannot resolve micro-scale street ponding or localized urban storm drain backups.
2. **Satellite Thermal Revisit:** NASA FIRMS polar orbits (12h revisit) create latency for new ignitions; fire weather indices must bridge the gap between satellite passes.

---

## 4. Statutory Jurisdiction & Authority

> [!CAUTION]
> **No Evacuation Authority:** HAZARDX AI is an advisory decision-support system. It **never** issues mandatory evacuation orders. Statutory authority belongs solely to sovereign government agencies (FEMA, NDMA, local civil protection). Official emergency orders supersede all AI outputs.
