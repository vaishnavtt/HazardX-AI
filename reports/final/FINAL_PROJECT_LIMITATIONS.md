# HAZARDX AI – FINAL SCIENTIFIC & TECHNICAL LIMITATIONS DISCLOSURE

**Document ID:** `HX-DOC-LIMITATIONS-2026-FINAL`  
**Evaluation Scope:** Transparent Boundary Disclosure, Safety Governance, and Operational Realities  
**Date of Audit:** November 2026  
**Auditor:** Senior Disaster Risk Scientist & AI Systems Architect  
**Classification:** Public Safety & Ethics Disclosure  

---

## 1. Executive Summary

In adherence to the United Nations Office for Disaster Risk Reduction (UNDRR) Sendai Framework and international meteorological ethics standards, this document establishes the explicit scientific, computational, and operational boundaries of **HAZARDX AI**.

Early warning systems must remain honest about their limits to prevent both false alarms and unwarranted complacency. HAZARDX AI is designed strictly as an automated decision-support system and does not replace official civil protection agencies.

---

## 2. Scientific & Methodological Boundaries

### 2.1 Non-Predictive Earthquake Policy
- **Absolute Boundary:** HAZARDX AI **does not** predict the exact time, epicenter, or magnitude of future earthquakes.
- **Scientific Rationale:** In accordance with USGS, IASPEI, and consensus geophysics, deterministic earthquake prediction is currently scientifically impossible due to non-linear chaotic friction dynamics along tectonic faults.
- **Operational Scope:** Seismic features within the platform strictly report recorded physical shocks and statistical aftershock probabilities using the empirical Omori-Utsu power law decay ($p=1.05$) following a recognized mainshock.

### 2.2 Quarantined Regression Models
- **Earthquake Aftershock Count:** The tabular regression model for aftershock count exhibited negative holdout generalization ($R^2 = -0.0401$) due to heavy-tailed swarm distributions. It is permanently quarantined and replaced with empirical Omori rate estimation.
- **Wildfire Burn Duration:** Fire duration is heavily modulated by human firefighting actions, fuel breaks, and micro-scale wind shifts ($R^2 = -214.75$). It is quarantined and replaced with meteorological fire weather index (FWI) windows.

### 2.3 Spatial and Temporal Resolution Limits
- **Numerical Weather Prediction (NWP):** Open-Meteo forecasts operate at an approximate $0.1^\circ \times 0.1^\circ$ (~11 km) grid resolution. Local micro-climatic rain squalls or convective cloudbursts below this resolution may be smoothed over.
- **Hydrological Routing:** Copernicus GloFAS river discharge models represent major river networks and basins; ultra-local storm sewer urban drainage backups require local municipal hydrodynamic sensor integration.
- **Topography:** Digital Elevation Models (DEM) operate at 30-meter pixel resolution, sufficient for regional slope stability but not sub-meter structural retaining wall analysis.

---

## 3. Operational Infrastructure Realities

### 3.1 Email Notification Mock Mode
- **Current State:** The email dispatch service operates in `LOCAL_MOCK_MODE` because no external SMTP server credentials (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`) are configured in the local development `.env` environment.
- **Operational Reality:** Alert dispatches are logged to the backend console and database audit trail, but actual outbound emails are not transmitted over the public internet until an enterprise SMTP server or SendGrid/Postmark API key is provisioned.

### 3.2 External Rate Limiting & Offline Resilience
- **API Limits:** Free public tiers of upstream APIs (Photon OSM, Open-Meteo, USGS) have burst request limits. HAZARDX AI mitigates this through 5-to-15 minute in-memory caching.
- **Network Outages:** If the host computer loses internet connectivity, the system automatically switches to deterministic climatological synthetic baselines. Alerts during this state carry the explicit tag `provenance: CALIBRATED_FALLBACK`.

---

## 4. Statutory Legal Notice

> **IMPORTANT DISCLAIMER FOR EMERGENCY OPERATORS AND CITIZENS:**  
> HAZARDX AI is an automated machine learning and numerical modeling advisory decision-support platform. It **never supersedes** statutory emergency warnings, evacuation orders, or directives issued by local civil protection authorities, national meteorological services, or emergency management agencies. Always follow instructions from authorized first responders during active crises.
