# HAZARDX AI – Phase 29: Complete Prediction Pipeline Audit

**Date:** November 19, 2026  
**Auditor:** Senior Multi-Disciplinary Engineering & Disaster Risk Intelligence Team  
**Scope:** Full end-to-end tracing from external APIs to frontend presentation  
**Benchmark Target:** Wayanad, Kerala, India (11.6854° N, 76.1320° E)  

---

## 1. Executive Summary

An exhaustive audit of the HAZARDX AI prediction and risk assessment pipeline was conducted to investigate critical anomalies where displayed risk categories contradicted physical environmental conditions.

The investigation traced the entire data flow across nine distinct stages:
$$\text{External Data Source} \longrightarrow \text{Ingestion} \longrightarrow \text{Validation} \longrightarrow \text{Feature Engineering} \longrightarrow \text{Model Input} \longrightarrow \text{Inference} \longrightarrow \text{Calibration} \longrightarrow \text{Risk Calculation} \longrightarrow \text{Frontend Display}$$

### Key Findings:
1. **Wildfire False Alarm (60% / HIGH):** The wildfire occurrence model was trained on synthetic data where positive fire events were drawn with temperature $\sim \mathcal{N}(32.5, 5.0)$ and negative non-events with temperature $\sim \mathcal{N}(18.0, 6.0)$. When queried for tropical Wayanad (26.5°C), the model interpreted ambient tropical warmth as fire ignition evidence ($+2.08$ SHAP log-odds). Furthermore, `wildfire_service.py` assigned risk category based on raw uncalibrated model score ($0.61$), completely ignoring the Canadian Fire Weather Index ($0.7$ = LOW danger) and Bayesian calibrated prior ($0.003$ = $0.3\%$).
2. **Unsupported Earthquake Aftershock (18%):** Wayanad lies $1,410\text{ km}$ from the nearest active fault with zero seismic events within $100\text{ km}$. However, `spatial_feature_service.py` and `forecast_service.py` defaulted missing mainshocks to $M 6.0$ / $M 4.5$ at $10\text{ km}$ depth, generating an artificial $18\%$ aftershock probability.
3. **Dummy Cyclone Evaluation (27%):** `geospatial.py` evaluated any location with $|\text{lat}| \le 45^\circ$ as having an active $45\text{ kt}$ tropical storm $85\text{ km}$ offshore, generating false cyclone intensification threats for inland mountain regions.
4. **Susceptibility vs. Short-Term Event Triggering:** For floods ($9\%$) and landslides ($8\%$), the models evaluated 1:1 case-control models under dry weather ($0\text{ mm}$ rain). The frontend presented these baseline scores as "Estimated Threat Scores" without distinguishing baseline geotechnical susceptibility from real-time meteorological triggering.

---

## 2. Stage-by-Stage Pipeline Trace

| Stage | Subsystem | Implementation File | Verified Behavior & Identified Flaw |
| :--- | :--- | :--- | :--- |
| **1. Data Source** | Open-Meteo, USGS, GloFAS, FIRMS, IMD | `backend/app/integrations/` | External APIs successfully return live meteorological readings (26.5°C, 49% RH, 0mm rain). USGS returns empty list for 100km radius. |
| **2. Ingestion** | Ingestion & Cache Managers | `backend/app/ingestion/` | Correctly caches API responses with appropriate TTLs. |
| **3. Validation** | Schema Validators | `backend/app/schemas/` | Pydantic models validate data types, but lack physical plausibility gating (e.g. allowing non-existent earthquakes). |
| **4. Feature Engineering** | Spatial Feature Service | `backend/app/geospatial/spatial_feature_service.py` | **CRITICAL DEFECT:** Silently substitutes missing seismic events with dummy $M 6.0$ mainshock; substitutes missing cyclone with $45\text{ kt}$ storm; computes FWI using McArthur formula whereas training used an entirely different formula. |
| **5. Model Input** | Feature DataFrames | `backend/app/services/*_service.py` | Features formatted into Pandas DataFrames matching training feature order, but values fall outside valid physical model scope. |
| **6. Inference** | XGBoost Classifiers & Regressors | `models/` | Predicts high raw probabilities due to feature dominance of ambient temperature in wildfire model. |
| **7. Calibration** | Bayesian Prior Calibration | `backend/app/utils/calibration.py` | Computes calibrated probabilities (e.g., $0.003$ for wildfire), but downstream services discard them in favor of raw scores. |
| **8. Risk Calculation** | Categorization Engine | `backend/app/utils/calibration.py` | Categorizes risk using `raw_prob` rather than `calibrated_prob` or physical domain indices (FWI). |
| **9. Display** | React UI Cards | `LocationAssessmentPage.tsx` | Formats raw score directly as `((hData.probability || 0.1) * 100).toFixed(0)%`, presenting uncalibrated model scores as real-world threat percentages. |

---

## 3. Detailed Audit of the 7 Data Integrations

1. **USGS ComCat (`usgs_client.py`):**
   - *Data:* Real-time global seismic feeds ($M \ge 2.5$) and radial point queries.
   - *Status:* Working. Returns 0 events for Wayanad within 100 km.
   - *Defect in usage:* Service assumed $M 6.0$ default instead of setting aftershock hazard to strictly 0.0% / QUIESCENT.
2. **NASA FIRMS (`nasa_firms_client.py`):**
   - *Data:* Global active fire thermal anomalies (MODIS C6.1 and VIIRS 375m).
   - *Status:* Working for global list, but lacked localized radial query for location assessment.
3. **Open-Meteo NWP & ERA5 (`weather_client.py`):**
   - *Data:* Real-time temperature, humidity, wind, surface pressure, and 30-day precipitation history.
   - *Status:* Fully operational. Accurately delivered Wayanad conditions (26.5°C, 49% RH, 0 mm rain).
4. **Copernicus GloFAS (`glofas_client.py`):**
   - *Data:* Gridded river discharge reanalysis and 7-day forecast.
   - *Status:* Working. Accurately returned low discharge ratio ($1.0\times$ normal).
5. **NOAA NHC (`cyclone_client.py`):**
   - *Data:* Active tropical cyclones from NHC.
   - *Defect in usage:* Falls back to historical IBTrACS storms and assigns them to queried inland coordinates regardless of geographic basin or distance.
6. **IMD RSMC New Delhi (`imd_client.py`):**
   - *Data:* Official North Indian Ocean cyclonic bulletins.
   - *Status:* Successfully reports "NO_ACTIVE_CYCLONIC_DISTURBANCE".
   - *Defect in usage:* Location assessment failed to check IMD basin status before running cyclone model.
7. **NASA Global Landslide Catalog (`landslide_client.py`):**
   - *Data:* Historical landslide catalog points and regional corridors.
   - *Status:* Historical points provide geographic susceptibility baseline, not short-term trigger.

---

## 4. Remediation Directives

1. **Eliminate Dummy Defaults:** Completely remove hardcoded $M 6.0$ earthquakes and $45\text{ kt}$ cyclones from `spatial_feature_service.py`. If no triggering phenomenon is present, output zero event probability and assign `QUIESCENT` / `NO_ACTIVE_THREAT`.
2. **Align Fire Weather Index (FWI) Formulation:** Rebuild wildfire risk evaluation to adhere strictly to the Canadian FWI system and ground-truth NASA FIRMS satellite hotspots.
3. **Calibrated Probabilities Only:** Transition all risk categorization and frontend displays from raw model scores to validated calibrated probabilities and physical domain metrics.
4. **Decouple Susceptibility from Real-Time Triggers:** Distinguish long-term environmental susceptibility (terrain slope, historical landslide prevalence) from short-term meteorological triggers (current rainfall, soil saturation).
