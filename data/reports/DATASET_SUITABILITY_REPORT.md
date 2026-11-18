# HAZARDX AI — Comprehensive Dataset Suitability Assessment
## Rigorous Machine Learning Task Suitability Audit

**Author:** HAZARDX AI Senior Data Science & ML Engineering Team  
**Date:** 2026-11-17  
**Evaluation Standard:** Objective ML task alignment, target variable availability, data leakage risks, and physical validity. Zero tolerance for unverified assumptions.

---

## 1. Summary of Suitability Decisions

| Hazard | Dataset Name | Assigned Rating | Target Variable Available? | Intended Machine Learning Task |
| :--- | :--- | :--- | :--- | :--- |
| **Floods** | Dartmouth Flood Observatory (DFO) Spatial Archive | **SUITABLE WITH PREPROCESSING** | Yes (Occurrence & Severity (1.0 to 2.0)) | Global Flood Susceptibility & Extent Ground-Truth Modeling |
| **Floods** | GLIDE Global Flood Sub-Catalog | **SUITABLE WITH PREPROCESSING** | Yes (killed, affected, homeless) | Flood Disaster Impact & Casualty Modeling |
| **Floods** | Central Water Commission (CWC) Telemetry / India-WRIS | **PARTIALLY SUITABLE** | No (Covariate / Covariate Only) | Real-Time River Water-Level & Stage Forecasting |
| **Landslides** | NASA Global Landslide Catalog (GLC / COOLR) | **SUITABLE WITH PREPROCESSING** | Yes (Occurrence (y=1) & Size (small/medium/large)) | Landslide Susceptibility & Rainfall-Triggered Occurrence Classification |
| **Landslides** | Geological Survey of India (GSI) 1:50k Landslide Susceptibility Maps | **PARTIALLY SUITABLE** | Yes (National Landslide Susceptibility Mapping (NLSM) Zone) | Regional High-Resolution Susceptibility Baseline in Western Ghats / Himalayas |
| **Earthquakes** | USGS Earthquake Catalog (ComCat 2000-2025) | **SUITABLE** | Yes (mag, depth, event rate) | Regional Seismic Activity Assessment & Aftershock Spatial Probability |
| **Earthquakes** | GEM Global Active Faults Database (GAF-DB) | **SUITABLE** | No (Covariate / Covariate Only) | Tectonic Proximity & Fault Slip Feature Engineering |
| **Earthquakes** | Global Ground Motion Datasets (PGA, PGV, MMI Stations) | **PARTIALLY SUITABLE** | No (Covariate / Covariate Only) | Empirical Ground-Motion Prediction Equations (GMPE) via ML |
| **Cyclones** | NOAA IBTrACS v04r01 Best Track Archive | **SUITABLE** | Yes (USA_WIND (kt), USA_PRES (hPa), USA_STATUS, Track (LAT, LON)) | Cyclone Intensity Classification, Wind Speed Estimation & Track Forecasting |
| **Cyclones** | IMD North Indian Ocean Best-Track Reports | **SUITABLE WITH PREPROCESSING** | Yes (IMD Cyclone Classification (CS, SCS, VSCS, ESCS, Super Cyclone)) | Validation of North Indian Ocean Cyclone Landfalls (Bay of Bengal & Arabian Sea) |
| **Wildfires** | NASA FIRMS MODIS Active Fire Catalog (C6.1) | **SUITABLE WITH PREPROCESSING** | Yes (Occurrence (y=1), total_frp_mw, duration_days, estimated_area_km2) | Wildfire Ignition Probability & Fire Radiative Power (FRP) Estimation |
| **Wildfires** | NASA FIRMS VIIRS 375m Active Fire Catalog | **SUITABLE WITH PREPROCESSING** | Yes (Occurrence (y=1), pixel_count, total_frp_mw) | High-Resolution Wildfire Perimeter & Active Spread Tracking |
| **Wildfires** | GLIDE Wildfire Disaster Registry | **SUITABLE WITH PREPROCESSING** | Yes (killed, affected) | Wildfire Disaster Impact & Socio-Economic Risk Assessment |
| **Common Environmental** | ECMWF ERA5 / ERA5-Land Reanalysis (Open-Meteo Historical Weather) | **SUITABLE** | No (Covariate / Covariate Only) | Cross-Hazard Atmospheric & Hydrological Feature Extraction (Precipitation, Temperature, Wind, Soil Moisture) |
| **Common Environmental** | geoBoundaries India Subnational Administrative Boundaries (IND-ADM1 & ADM2) | **SUITABLE** | No (Covariate / Covariate Only) | Spatial Aggregation, Regional Risk Indexing & Early Warning Dissemination |

---

## 2. In-Depth Suitability Audits by Dataset

### Floods: Dartmouth Flood Observatory (DFO) Spatial Archive
- **File Path / Source:** `data/raw/floods/dfo_spatial_flood_archive_1985_2010.csv`
- **Suitability Rating:** **SUITABLE WITH PREPROCESSING**
- **Intended ML Task:** Global Flood Susceptibility & Extent Ground-Truth Modeling
- **Target Variable Status:** Occurrence & Severity (1.0 to 2.0)
- **Technical Justification:** Contains 4,029 global flood events with 100% verified centroid coordinates and historical dates. Requires preprocessing to sanitize coordinate typos (e.g. record 3229) and join with negative spatio-temporal non-flood controls and dynamic rainfall reanalysis (ERA5).
- **Blockers & Preprocessing Needs:** Requires negative pseudo-absence sampling and ERA5/GPM precipitation join.

### Floods: GLIDE Global Flood Sub-Catalog
- **File Path / Source:** `data/raw/floods/glide_flood_events.csv`
- **Suitability Rating:** **SUITABLE WITH PREPROCESSING**
- **Intended ML Task:** Flood Disaster Impact & Casualty Modeling
- **Target Variable Status:** killed, affected, homeless
- **Technical Justification:** Contains 2,732 international flood and flash flood disaster events with 100% valid coordinates and casualty figures. Requires cleaning year formatting typos (e.g. '20' -> '2020').
- **Blockers & Preprocessing Needs:** Year format harmonization and normalization of skewed casualty metrics.

### Floods: Central Water Commission (CWC) Telemetry / India-WRIS
- **File Path / Source:** `data/raw/floods/cwc_water_levels (Investigated)`
- **Suitability Rating:** **PARTIALLY SUITABLE**
- **Intended ML Task:** Real-Time River Water-Level & Stage Forecasting
- **Target Variable Status:** River gauge stage level (m)
- **Technical Justification:** Official India-WRIS and CWC portals require authenticated portal sessions and interactive CAPTCHA gating. Station-level historical hourly gauge records are not programmatically downloadable via open API without institutional credentials. Global GloFAS daily discharge provides an open surrogate.
- **Blockers & Preprocessing Needs:** Requires institutional CWC/NWIC data sharing agreement or authenticated telemetry tokens.

### Landslides: NASA Global Landslide Catalog (GLC / COOLR)
- **File Path / Source:** `data/raw/landslides/nasa_global_landslide_catalog_point.csv`
- **Suitability Rating:** **SUITABLE WITH PREPROCESSING**
- **Intended ML Task:** Landslide Susceptibility & Rainfall-Triggered Occurrence Classification
- **Target Variable Status:** Occurrence (y=1) & Size (small/medium/large)
- **Technical Justification:** Contains 11,033 empirical global landslide points with 100% valid coordinates, dates, and trigger causes. Suitable as the primary positive occurrence ground truth.
- **Blockers & Preprocessing Needs:** Must NOT be trained alone; requires stratified sampling of non-landslide slope controls (y=0) and extraction of SRTM slope, SoilGrids, and 7-day GPM rainfall.

### Landslides: Geological Survey of India (GSI) 1:50k Landslide Susceptibility Maps
- **File Path / Source:** `data/raw/landslides/gsi_maps (Investigated)`
- **Suitability Rating:** **PARTIALLY SUITABLE**
- **Intended ML Task:** Regional High-Resolution Susceptibility Baseline in Western Ghats / Himalayas
- **Target Variable Status:** National Landslide Susceptibility Mapping (NLSM) Zone
- **Technical Justification:** GSI provides static PDF/WMS maps on Bhukosh geoportal requiring user authentication and GIS georeferencing. Highly relevant for Indian domain validation but not downloadable as raw tabular training vectors.
- **Blockers & Preprocessing Needs:** Vectorization and georeferencing of GSI Bhukosh tiles.

### Earthquakes: USGS Earthquake Catalog (ComCat 2000-2025)
- **File Path / Source:** `data/raw/earthquakes/usgs_earthquakes_2000_2025.csv`
- **Suitability Rating:** **SUITABLE**
- **Intended ML Task:** Regional Seismic Activity Assessment & Aftershock Spatial Probability
- **Target Variable Status:** mag, depth, event rate
- **Technical Justification:** Comprehensive, authoritative global catalog of 689,496 events with 100% valid coordinates and depths. Deduplicated and fully verified.
- **Blockers & Preprocessing Needs:** None for seismicity rate and aftershock hazard modeling. For ground-motion shaking (PGA/MMI), requires separate station waveform/ShakeMap linkage.

### Earthquakes: GEM Global Active Faults Database (GAF-DB)
- **File Path / Source:** `data/raw/earthquakes/gem_active_faults.geojson`
- **Suitability Rating:** **SUITABLE**
- **Intended ML Task:** Tectonic Proximity & Fault Slip Feature Engineering
- **Target Variable Status:** Covariate (distance_to_fault, slip_type, slip_rate)
- **Technical Justification:** 16,195 harmonized active fault geometries globally. Directly usable for computing Euclidean and shortest perpendicular distance to fault traces.
- **Blockers & Preprocessing Needs:** Spatial distance calculation algorithm to join with earthquake epicenters.

### Earthquakes: Global Ground Motion Datasets (PGA, PGV, MMI Stations)
- **File Path / Source:** `data/raw/earthquakes/ground_motion (Investigated)`
- **Suitability Rating:** **PARTIALLY SUITABLE**
- **Intended ML Task:** Empirical Ground-Motion Prediction Equations (GMPE) via ML
- **Target Variable Status:** PGA (g), PGV (cm/s), MMI (I-X)
- **Technical Justification:** The primary ComCat catalog contains hypocentral source parameters but does not include recorded surface PGA/PGV timeseries at strong-motion stations. Instrumental ground-motion datasets (USGS ShakeMap flatfiles, PEER NGA-West2) require specialized station joins.
- **Blockers & Preprocessing Needs:** Direct ShakeMap ground-motion station archive download or GMPE proxy simulation.

### Cyclones: NOAA IBTrACS v04r01 Best Track Archive
- **File Path / Source:** `data/raw/cyclones/ibtracs_since1980_v04r01.csv`
- **Suitability Rating:** **SUITABLE**
- **Intended ML Task:** Cyclone Intensity Classification, Wind Speed Estimation & Track Forecasting
- **Target Variable Status:** USA_WIND (kt), USA_PRES (hPa), USA_STATUS, Track (LAT, LON)
- **Technical Justification:** Contains 312,398 track observations across 5,017 storms worldwide since 1980, including 15,654 North Indian Ocean points. Complete coordinates, continuous 3-hourly/6-hourly tracks.
- **Blockers & Preprocessing Needs:** Time-lagged feature engineering (calculating 12h/24h intensity change, translational speed and heading).

### Cyclones: IMD North Indian Ocean Best-Track Reports
- **File Path / Source:** `data/raw/cyclones/imd_tracks (Investigated)`
- **Suitability Rating:** **SUITABLE WITH PREPROCESSING**
- **Intended ML Task:** Validation of North Indian Ocean Cyclone Landfalls (Bay of Bengal & Arabian Sea)
- **Target Variable Status:** IMD Cyclone Classification (CS, SCS, VSCS, ESCS, Super Cyclone)
- **Technical Justification:** The NOAA IBTrACS dataset already incorporates the New Delhi WMO Regional Specialized Meteorological Centre (RSMC New Delhi / IMD) official agency tracks (agency code 'NEWDELHI').
- **Blockers & Preprocessing Needs:** Filter IBTrACS records for agency == 'newdelhi' or basin == 'NI'.

### Wildfires: NASA FIRMS MODIS Active Fire Catalog (C6.1)
- **File Path / Source:** `data/processed/wildfires/wildfire_events_cleaned_catalog.csv`
- **Suitability Rating:** **SUITABLE WITH PREPROCESSING**
- **Intended ML Task:** Wildfire Ignition Probability & Fire Radiative Power (FRP) Estimation
- **Target Variable Status:** Occurrence (y=1), total_frp_mw, duration_days, estimated_area_km2
- **Technical Justification:** Contains 31,371 discrete physical wildfire events aggregated from 66,140 high-confidence satellite detections using 4D spatiotemporal DBSCAN clustering. Directly provides empirical centroids, duration, pixel footprints, and radiative energy release.
- **Blockers & Preprocessing Needs:** Requires stratified non-fire background sampling (negative controls) and join with ERA5 Fire Weather Index (FWI), vapor pressure deficit, and SRTM slope.

### Wildfires: NASA FIRMS VIIRS 375m Active Fire Catalog
- **File Path / Source:** `data/processed/wildfires/wildfire_events_viirs_catalog.csv`
- **Suitability Rating:** **SUITABLE WITH PREPROCESSING**
- **Intended ML Task:** High-Resolution Wildfire Perimeter & Active Spread Tracking
- **Target Variable Status:** Occurrence (y=1), pixel_count, total_frp_mw
- **Technical Justification:** Contains 111,053 discrete wildfire events clustered from 326,642 nominal/high confidence 375m VIIRS detections. Highest spatial fidelity for localized perimeter and fuel ignition modeling.
- **Blockers & Preprocessing Needs:** High compute requirement for global feature extraction; recommend regional bounding box (e.g. South Asia / North America).

### Wildfires: GLIDE Wildfire Disaster Registry
- **File Path / Source:** `data/processed/wildfires/wildfire_disaster_events_glide.csv`
- **Suitability Rating:** **SUITABLE WITH PREPROCESSING**
- **Intended ML Task:** Wildfire Disaster Impact & Socio-Economic Risk Assessment
- **Target Variable Status:** killed, affected
- **Technical Justification:** Contains 224 georeferenced major global wildfire disaster events with documented humanitarian impact.
- **Blockers & Preprocessing Needs:** Macro-level event reporting; should be coupled with satellite fire perimeters for physical modeling.

### Common Environmental: ECMWF ERA5 / ERA5-Land Reanalysis (Open-Meteo Historical Weather)
- **File Path / Source:** `data/raw/environmental/era5_connector (Verified API)`
- **Suitability Rating:** **SUITABLE**
- **Intended ML Task:** Cross-Hazard Atmospheric & Hydrological Feature Extraction (Precipitation, Temperature, Wind, Soil Moisture)
- **Target Variable Status:** Dynamic Environmental Covariates
- **Technical Justification:** Provides verified global historical daily and hourly reanalysis for any coordinate back to 1940 with zero API key or cost. Fully tested and operational in project scripts.
- **Blockers & Preprocessing Needs:** Batch spatial-temporal querying for event-level feature enrichment.

### Common Environmental: geoBoundaries India Subnational Administrative Boundaries (IND-ADM1 & ADM2)
- **File Path / Source:** `data/raw/environmental/india_state_boundaries.geojson`
- **Suitability Rating:** **SUITABLE**
- **Intended ML Task:** Spatial Aggregation, Regional Risk Indexing & Early Warning Dissemination
- **Target Variable Status:** Spatial Polygons & Boundary Hierarchy
- **Technical Justification:** Official, validated open GIS boundaries covering all Indian states and Union Territories (including Kerala). 100% valid geometry.
- **Blockers & Preprocessing Needs:** None. Fully downloaded and ready.
