# HAZARDX AI – PHASE 14 AUDIT: DATA LEAKAGE AUDIT
## Comprehensive Investigation of Temporal, Target, Geographic, and Train-Set Contamination

**Document Reference:** `HAZARDX-P14-LEAK-002`  
**Audit Date:** November 19, 2026  
**Auditor:** Senior AI Quality, Geospatial Intelligence & Data Forensic Team  
**Evaluation Scope:** 5 Model-Ready Datasets and 10 Retrospective Landmark Disaster Timelines  
**Script Executed:** `scripts/audit_leakage.py`  

---

## 1. EXECUTIVE SUMMARY & CRITICAL FINDINGS

A rigorous scientific audit of the data pipelines and retrospective testing scripts was performed to identify any form of data leakage.

### Key Audit Findings:
1. **Train/Test Contamination in Historical Disasters:**
   - **Gorkha Earthquake (Nepal 2015):** Record 5907 (`2015-04-25T06:11:25.950Z`) was found in the `train` split of `earthquake_model_ready.csv`.
   - **Super Typhoon Haiyan (Yolanda 2013):** Records 159291 and 159292 (`2013-11-07 21:00:00` and `2013-11-08 00:00:00`) were found in the `train` split of `cyclone_model_ready.csv`.
   - **Remaining 8 Disasters:** No train/test contamination found. Wayanad (2024), Oso (2014), Kumamoto (2016), Amphan (2020), Camp Fire (2018), Black Summer (2019–2020), Henan (2021), and Katrina (2005) were completely absent from their respective training sets.
2. **Reconstructed Reanalysis Scenarios vs Blind Operational Forecasts:**
   - In `scripts/phase13_retrospective_testing.py`, the environmental feature profiles at -72h, -48h, -24h, -12h, and -6h were manually reconstructed from post-event meteorological reanalysis and surface station data.
   - In an operational setting at -72h, meteorologists rely on **Numerical Weather Prediction (NWP) forecasts** which inherently contain spatial and quantitative precipitation uncertainty. Using observed reanalysis values represents an ideal case (perfect weather forecast assumption).
   - **Scientific Classification:** These experiments are formally classified as **RECONSTRUCTED HISTORICAL VALIDATION SCENARIOS** and must be distinguished from blind real-time operational forecasts.
3. **Internal Dataset Partitioning (No Feature-Target Leakage):**
   - In `data/model_ready/`, all metadata columns (`event_id`, `SID`, `NAME`, `SEASON`, `timestamp`, `split`, `sample_type`) are strictly excluded from feature matrices.
   - Categorical encoders (`OrdinalEncoder`) are fitted strictly on the `train` partition and merely applied to `val` and `test`, preventing data snooping.

---

## 2. AUDIT OF THE 10 LANDMARK DISASTER EXPERIMENTS

Every historical disaster event evaluated in Phase 13 was cross-checked against its underlying dataset for spatial, temporal, and split contamination.

| Hazard | Event Name | Target Disaster Date | Dataset Latitude / Longitude | Spatially Nearby Records ($<1^\circ$) | Temporal Match in Dataset? | Dataset Split Assignment | Leakage Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Floods** | **Henan Deluge** | 2021-07-20 | 34.75°N, 113.63°E | 0 records | None (Dataset ends 2026 synthetic / non-Henan) | None | **CLEAN (Out-of-sample)** |
| **Floods** | **Hurricane Katrina Surge** | 2005-08-29 | 29.95°N, -90.07°W | 0 records | None | None | **CLEAN (Out-of-sample)** |
| **Landslides** | **Wayanad Debris Flow** | 2024-07-30 | 11.53°N, 76.22°E | 4 records | None (Catalog ends August 2017) | None | **CLEAN (Out-of-sample)** |
| **Landslides** | **Oso Landslide** | 2014-03-22 | 48.28°N, -121.84°W | 8 records | None (Different months in PNW) | None | **CLEAN (Out-of-sample)** |
| **Earthquakes** | **Gorkha Mw 7.8** | 2015-04-25 | 28.15°N, 84.71°E | 2 records | **1 record (2015-04-25)** | **`train` (Record 5907)** | **CONTAMINATED (In-Sample)** |
| **Earthquakes** | **Kumamoto Mw 7.0** | 2016-04-15 | 32.75°N, 130.76°E | 3 records | None (Different seismic events) | None | **CLEAN (Out-of-sample)** |
| **Cyclones** | **Typhoon Haiyan** | 2013-11-08 | 11.00°N, 125.00°E | 201 records | **2 records (2013-11-07/08)** | **`train` (Records 159291/92)** | **CONTAMINATED (In-Sample)** |
| **Cyclones** | **Super Cyclone Amphan**| 2020-05-20 | 21.70°N, 88.30°E | 26 records | None | None | **CLEAN (Out-of-sample)** |
| **Wildfires** | **Camp Fire** | 2018-11-08 | 39.81°N, -121.44°W | 0 records | None | None | **CLEAN (Out-of-sample)** |
| **Wildfires** | **Black Summer** | 2019-12-31 | -35.30°S, 150.10°E | 4 records | None | None | **CLEAN (Out-of-sample)** |

---

## 3. IN-DEPTH ANALYSIS OF CONTAMINATED EVENTS

### 3.1 Gorkha Earthquake (Nepal 2015)
- **Finding:** The Mw 7.8 Gorkha mainshock was ingested into the global USGS earthquake catalog training split as record 5907.
- **Scientific Impact:** When the earthquake service predicted aftershock hazard probability for Gorkha at 94.6%, the XGBoost model had already seen the Gorkha mainshock during training!
- **Scientific Remediation:**
  - The Gorkha retrospective experiment cannot be cited as a "blind holdout test."
  - It must be formally labeled as an **IN-SAMPLE HISTORICAL RECONSTRUCTION**.
  - Conversely, the **Kumamoto 2016 Mw 7.0 sequence** was completely absent from the training partition and serves as the true **out-of-sample** seismic validation.

### 3.2 Super Typhoon Haiyan (Philippines 2013)
- **Finding:** Super Typhoon Haiyan is one of the most prominent storms in the IBTrACS global tropical cyclone database (1980–2026). Records 159291 and 159292 represent Haiyan's 6-hourly track points and were assigned to the `train` partition.
- **Scientific Impact:** The model's evaluation of Haiyan at -72h and -48h had exposure to Haiyan's historical storm track in training.
- **Scientific Remediation:**
  - Haiyan must be labeled as an **IN-SAMPLE HISTORICAL CASE STUDY**.
  - **Super Cyclone Amphan (2020)** in the Bay of Bengal had no track points in the training set and serves as the primary **out-of-sample** cyclone validation case study.

---

## 4. FEATURE PROVENANCE & OPERATIONAL LEAD-TIME REALISM

### 4.1 What Was Used vs What Is Available Operationally
In a real-world operational early-warning deployment:
- **At -72 hours:** The true 72h accumulated rainfall is unknown. Forecasters must rely on numerical weather prediction models (e.g., GFS, ECMWF, Open-Meteo). NWP models have forecast errors (spatial displacement of storm tracks, over/under-estimation of convective cell rain rates).
- **In Retrospective Reconstructions:** Features such as `precip_3d_sum_mm` and `river_discharge_m3s` were reconstructed using observed historical station data. This evaluates **model response under known antecedent conditions** (a sensitivity test), rather than an end-to-end NWP+ML coupled forecast.

### 4.2 Time-Zone & Timestamp Verification
All timestamps in `scripts/phase13_retrospective_testing.py` were verified against UTC:
- **Henan:** `2021-07-20T16:00:00Z` corresponds to July 21 00:00 CST (Zhengzhou local time), coinciding with the peak evening deluge.
- **Katrina:** `2005-08-29T11:00:00Z` corresponds to 06:00 CDT, precisely when Katrina made landfall in Plaquemines Parish.
- **Wayanad:** `2024-07-30T02:00:00Z` corresponds to 07:30 IST, following the early morning debris slides (02:00–04:00 IST).
- No incorrect time-zone offsets were detected.

---

## 5. LEAKAGE AUDIT CONCLUSION & GOVERNANCE DIRECTIVES

1. **Re-classification of Retrospective Experiments:**
   - 8 Events are verified **Out-of-Sample Reconstructed Historical Scenarios**.
   - 2 Events (Gorkha and Haiyan) are designated **In-Sample Historical Case Studies**.
2. **User Communication Rule:**
   - All frontend cards and documentation must clearly state: *"Historical scenarios evaluated using reconstructed environmental conditions. Forecast skill in live operations depends on underlying Numerical Weather Prediction (NWP) accuracy."*
3. **No Target Leakage in ML Pipeline:**
   - Feature matrices are completely clean of targets, IDs, and future indicators. Partition separation is strictly enforced in `data_loader.py`.
