# HAZARDX AI — FINAL SCIENTIFIC LIMITATIONS & ETHICAL NOTICE

**Author:** Science Advisory & AI Ethics Committee  
**Date:** March 2026  
**Document Classification:** Final Project Milestone Deliverable  
**Repository Location:** `C:\Users\thott\Desktop\hazardai`  

---

## 1. Executive Summary

Scientific integrity and transparency require an explicit enumeration of the assumptions, data constraints, and physical boundaries governing **HAZARDX AI**. 

This document details the known limitations across all five hazard modules to prevent misinterpretation and ensure responsible emergency decision-support.

---

## 2. Hazard-Specific Scientific Boundaries

### 2.1 Earthquakes: Strict No-Prediction Policy
- **Boundary:** Under modern seismological physics (IASPEI & USGS guidelines), earthquakes **cannot be predicted** with deterministic time, epicenter, and magnitude.
- **System Capability:** The system exclusively evaluates *probabilistic aftershock clustering risk* following a verified physical mainshock within an adaptive spatial-temporal window ($100\text{ km}$, $30\text{ days}$) using the modified Omori-Utsu power law.
- **Guardrail:** Any deterministic prediction claim is strictly barred by system governance.

### 2.2 Tropical Cyclones: Basin Seasonality & Fallback Tracks
- **Boundary:** During off-season calm periods in the North Atlantic or Eastern Pacific, NOAA NHC reports zero active systems (`{"activeStorms": []}`).
- **System Capability:** The system activates verified historical reference benchmark tracks (e.g. Hurricane Katrina) alongside live IMD RSMC North Indian Ocean bulletins.
- **Uncertainty:** Cyclone track cones represent the 67% historical confidence envelope; deviations outside the cone are physically possible due to steering flow anomalies.

### 2.3 Floods: Ungauged Streams & Urban Micro-Drainage
- **Boundary:** Copernicus GloFAS models continental river reaches down to $0.1^\circ$ resolution. Hyper-local urban flash floods caused by localized storm-drain clogging cannot be resolved at continental scales.
- **System Capability:** Inundation risk is synthesized from 1d/3d accumulated precipitation, soil moisture saturation, and GloFAS river discharge.

### 2.4 Landslides: Geotechnical Micro-Stratigraphy
- **Boundary:** Regional Copernicus DEM slope analysis ($30\text{m}$ resolution) captures macroscopic relief, but cannot measure subterranean shear plane friction angles or localized fractured bedrock joints.
- **System Capability:** Evaluates empirical hillslope failure susceptibility derived from slope angle, antecedent 30-day precipitation infiltration, and NASA Global Landslide Catalog proximity.

### 2.5 Wildfires: Satellite Overpass Cadence
- **Boundary:** NASA FIRMS VIIRS and MODIS polar-orbiting satellites refresh active thermal hotspots at 3 to 6-hour overpass intervals. Rapidly expanding spot fires ignited between satellite passes may have latency before detection.
- **System Capability:** Bridges satellite latency using forward-looking Canadian Fire Weather Index (FWI) calculations based on hourly temperature, relative humidity, wind velocity, and drought indices.

---

## 3. Operational & Communication Boundaries

### 3.1 Decision Support vs. Statutory Evacuation Directives
- **Statutory Notice:** HAZARDX AI is an automated decision-support and risk-awareness tool. It does **not** issue legally binding civil protection directives or evacuation orders.
- **Operator Guidance:** Citizens and emergency managers must always follow statutory instructions issued by local emergency services, national meteorological agencies, and civil defense authorities.

### 3.2 Notification Delivery Mode
- **SMTP Notification:** When an external SMTP mail server is not configured in environment variables, the system operates in a **local mock notification mode**. Audit trails record all generated alerts without raising false delivery errors.

### 3.3 Forecast Horizon Limits
- **Predictive Horizon:** Operational predictive skill is verified up to 72 hours. Predictions attempted beyond 72 hours are subject to extreme atmospheric chaos and are suppressed to maintain defensibility.
