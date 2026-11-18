# HAZARDX AI — Frequently Asked Questions (FAQ)
**Document ID:** `HAZARDX-DOCS-FAQ-010`  
**Platform Version:** `v1.0.0-PROD`  

---

### Q1: What natural hazards does HAZARDX AI cover?
**Answer:** HAZARDX AI covers five primary disaster domains:
1. **Floods:** Pluvial flash flooding and fluvial river overbank inundation.
2. **Landslides:** Rainfall-triggered slope failures and debris flows.
3. **Earthquakes:** Statistical post-mainshock secondary aftershock hazard clustering.
4. **Tropical Cyclones:** Rapid intensification (RI) and 24-hour wind intensity changes.
5. **Wildfires:** Weather-driven ignition susceptibility and thermal anomaly tracking.

---

### Q2: Does HAZARDX AI predict earthquakes in advance?
**Answer:** **No.** In strict compliance with the USGS, IASPEI, and international seismological consensus, HAZARDX AI **does not** claim to predict the exact date, time, location, or magnitude of future earthquakes. The seismic model evaluates **post-mainshock aftershock hazard** (the statistical probability of elevated secondary clustering following an observed mainshock) using Gutenberg-Richter and modified Omori law frameworks.

---

### Q3: Do I need paid API keys to run HAZARDX AI?
**Answer:** **No.** All seven external scientific integrations (USGS, Open-Meteo, Copernicus GloFAS, NOAA NHC, IMD RSMC, NASA GLC, NASA FIRMS open feeds) operate out-of-the-box using public endpoints with zero required subscription fees.

---

### Q4: Does the system require a GPU?
**Answer:** **No.** All 12 XGBoost gradient-boosted models, Scikit-learn calibrations, and TreeSHAP polynomial explainers run natively on standard x86-64 or ARM64 CPUs. Steady-state model inference executes in under **6 milliseconds** on a standard dual-core laptop.

---

### Q5: Can HAZARDX AI operate during network outages?
**Answer:** **Yes.** When internet connectivity drops, HAZARDX AI activates its local SQLite cache (`CACHED_OBSERVATION`) and offline baselines, displaying clear data freshness badges rather than crashing.

---

### Q6: Can HAZARDX AI issue mandatory evacuation orders?
**Answer:** **No.** HAZARDX AI is an artificial intelligence decision-support platform. Statutory authority to order civil evacuations rests exclusively with sovereign government civil protection bodies (e.g., FEMA, NDMA, regional prefectures, civil defense). In any conflict, official government instructions supersede AI guidance.
