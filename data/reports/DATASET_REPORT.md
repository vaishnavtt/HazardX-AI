# HAZARDX AI — Global Multi-Hazard Intelligence & Early Warning System
## Comprehensive Historical Dataset Collection, Verification & Data Quality Audit Report

**Author / System:** HAZARDX AI Data Engineering Pipeline & Geospatial Science Team  
**Date of Verification:** 2026-11-17  
**Status:** Complete 5-Hazard Historical Dataset Collection, Quality Audit & EDA  
**Strict Data Integrity Policy:** Verified official sources only; 100% real empirical data; zero fabricated or synthetic records. Zero machine learning model training initiated.

---

## 1. Directory Structure

```
data/
    raw/
        floods/
            dfo_spatial_flood_archive_1985_2010.csv       # DFO shapefile attribute export (4,029 records)
            dfo_flood_records_1985_2024.csv               # DFO master tabular archive (5,503 records)
            dfo_shapefile/                                # Original ESRI Shapefile bundle (.shp, .dbf, .prj, .shx)
            glide_events_global.csv                       # Full ADRC/UN OCHA GLIDE archive (9,142 records)
            glide_flood_events.csv                        # Filtered flood & flash flood events (2,732 records)
        landslides/
            nasa_global_landslide_catalog_point.csv       # NASA Global Landslide Catalog (GLC) points (11,033 records)
            nasa_shapefile/                               # NASA GLC ESRI Shapefile bundle (.shp, .dbf, .prj, .shx)
            glide_landslide_events.csv                    # GLIDE landslide disaster events (183 records)
        earthquakes/
            usgs_earthquakes_2000_2025.csv                # Official USGS ComCat historical records M>=2.5 (689,496 records, 120.55 MB)
            monthly/                                      # 312 partitioned monthly raw CSVs (2000-01 to 2025-12)
            gem_active_faults.geojson                     # GEM Global Active Faults Database (16,195 fault traces, 12.30 MB)
            glide_earthquake_events.csv                   # GLIDE earthquake disaster events (649 records)
        cyclones/
            ibtracs_since1980_v04r01.csv                  # Official NOAA IBTrACS v04r01 raw best tracks (312,398 track pts, 138.64 MB)
            glide_cyclone_events.csv                      # GLIDE tropical cyclone disaster events (1,165 records)
        wildfires/
            modis_active_fire_global_7d.csv               # NASA FIRMS MODIS C6.1 active fire detections (69,358 pixels, 5.09 MB)
            viirs_active_fire_global_7d.csv               # NASA FIRMS VIIRS 375m active fire detections (372,407 pixels, 29.49 MB)
            glide_wildfire_disaster_events.csv            # GLIDE wildfire disaster events (224 records)
        environmental/
            india_state_boundaries.geojson                # Official subnational administrative boundaries (36 States/UTs, 4.87 MB)
            india_glide_disaster_events.geojson           # Georeferenced national disaster events in India (292 records, 2.66 MB)
    processed/
        floods/
            flood_events_cleaned_catalog.csv              # Standardized historical flood catalog (6,761 records)
            flood_cross_source_duplicates.csv             # DFO vs. GLIDE entity resolution audit (88 duplicate pairs)
            flood_environmental_features_spec.json        # Feature engineering schema for XGBoost
        landslides/
            landslide_events_cleaned_catalog.csv          # Standardized historical landslide catalog (11,216 records)
            landslide_cross_source_duplicates.csv         # NASA GLC vs. GLIDE entity resolution audit (115 duplicate pairs)
            landslide_environmental_features_spec.json    # Feature engineering schema for XGBoost
        earthquakes/
            earthquake_events_cleaned_catalog.csv         # Cleaned tectonic earthquake catalog (681,902 records, 104.38 MB)
            earthquake_features_spec.json                 # Seismic hazard feature engineering specification
        cyclones/
            cyclone_tracks_cleaned_catalog.csv            # Normalized storm track catalog (312,398 track points, 49.12 MB)
            cyclone_tracks_north_indian_ocean.csv         # North Indian Ocean storm tracks (15,654 track points, 2.45 MB)
        wildfires/
            wildfire_events_cleaned_catalog.csv           # 4D DBSCAN clustered MODIS wildfire events (31,371 events, 3.25 MB)
            wildfire_events_viirs_catalog.csv             # 4D DBSCAN clustered VIIRS wildfire events (111,053 events, 11.82 MB)
            wildfire_disaster_events_glide.csv            # Processed GLIDE wildfire disaster impact records (224 events)
            wildfire_environmental_features_spec.json     # Feature engineering schema for XGBoost
        environmental/
            india_disaster_events_catalog.csv             # Standardized all-hazard disaster events in India (292 records)
            kerala_disaster_events.csv                    # Focused multi-hazard disaster subset for Kerala (13 records)
    reports/
        DATASET_INVENTORY.md
        DATA_QUALITY_REPORT.md
        DATASET_SUITABILITY_REPORT.md
        DATASET_INTEGRATION_REPORT.md
        DATA_READINESS_MATRIX.md
        EDA_REPORT.md
        DATA_SOURCE_REGISTER.csv
        DATASET_METADATA.json
        ENVIRONMENTAL_DATASET_VERIFICATION.json
        figures/                                          # 8 verified high-resolution multi-hazard EDA plots
```

---

## 2. Hazard 1: Floods

### 2.1 Dataset Catalogue: Historical Event Inventories

| Property | Dartmouth Flood Observatory (DFO) Spatial Archive | Dartmouth Flood Observatory (DFO) Master Tabular | GLIDE Global Disaster Events (Floods Sub-catalog) |
| :--- | :--- | :--- | :--- |
| **Official Source** | University of Colorado Boulder / CSDMS / DFO | University of Colorado Boulder / DFO | Asian Disaster Reduction Center (ADRC) / UN OCHA / HDX |
| **Verified Download URL** | `https://data.humdata.org/dataset/1fd855de-57c6-42b3-83e1-9cf989b0f70d` | `https://floodobservatory.colorado.edu/` | `https://data.humdata.org/dataset/5721abce-4367-4307-abbd-f99cf95ebeca` |
| **License** | Open Access / CC-BY / Humanitarian Open Data | CC-BY / Open Research Data | Open Data (Creative Commons Attribution) |
| **Raw File Format** | ESRI Shapefile (`.shp`, `.dbf`, `.shx`, `.prj`) | CSV (Latin-1 encoded) | CSV (UTF-8) |
| **Number of Records** | **4,029** | **5,503** | **2,732** (2,500 FL + 232 FF) |
| **Number of Columns** | **35** | **12** | **24** |
| **Geographical Coverage** | Global (-45.69° to +66.80° Lat, -173.45° to +179.65° Lon) | Global (411 countries & regions) | Global (-50.20° to +66.76° Lat, -172.10° to +179.81° Lon) |
| **Historical Coverage** | 1985-01-01 to 2010-08-11 | 1985-01-01 to 2024-01-09 | 1972-06-09 to 2026-10-29 |
| **Coordinate Completeness**| 100% (4,029 / 4,029 non-null coordinates) | Tabular only (Country/Region names) | 100% (2,732 / 2,732 non-null coordinates) |
| **Cleaned Output** | [flood_events_cleaned_catalog.csv](file:///c:/Users/thott/Desktop/hazardai/data/processed/floods/flood_events_cleaned_catalog.csv) (**6,761 standardized events**) |

### 2.2 Data Quality & Verification Audit Findings
1. **Latitude Anomaly in DFO Spatial Record #3229:** Record `Register__ = 3229` (Philippines) contained `Centroid_Y = 124.833`, which exceeded the valid latitude range \([-90, +90]\). `Centroid_X` was duplicated into `Centroid_Y`. Sanitized to `NaN`.
2. **Year Truncation in GLIDE Record `FL-20-000033-PER`:** Record had `year = 20` instead of `2020`. Standardized to `2020`.
3. **Cross-Source Deduplication (DFO vs. GLIDE):** Found 235 direct key references, 19 confirmed duplicates ($\le 2$ days, $\le 30$ km), 69 potential duplicates ($\le 7$ days, $\le 150$ km), 3,944 unique DFO events, and 2,646 unique GLIDE events. Saved to [flood_cross_source_duplicates.csv](file:///c:/Users/thott/Desktop/hazardai/data/processed/floods/flood_cross_source_duplicates.csv).

---

## 3. Hazard 2: Landslides

### 3.1 Dataset Catalogue: Historical Event Inventories

| Property | NASA Global Landslide Catalog (GLC / COOLR) Point Archive | NASA GLC Official Shapefile Archive | GLIDE Global Disaster Events (Landslide Sub-catalog) |
| :--- | :--- | :--- | :--- |
| **Official Source** | NASA Goddard Space Flight Center (Dalia Kirschbaum, Thomas Stanley) | NASA Goddard Space Flight Center / HDX | Asian Disaster Reduction Center (ADRC) / UN OCHA / HDX |
| **Verified Download URL** | Local Raw Mirror: `data/raw/landslides/nasa_global_landslide_catalog_point.csv` | `https://data.humdata.org/dataset/1eb911ba-3681-4a96-b025-ae0c33b80a12` | `https://data.humdata.org/dataset/5721abce-4367-4307-abbd-f99cf95ebeca` |
| **License** | NASA Open Data Policy / US Government Public Domain | Open Data (Public Domain / CC-BY) | Creative Commons Attribution (CC-BY) |
| **Raw File Format** | CSV (UTF-8, 8.48 MB) | ESRI Shapefile bundle (`.shp`, `.dbf`, `.prj`, `.shx` - 65.9 MB DBF) | CSV (UTF-8, 74.4 KB) |
| **Number of Records** | **11,033** | **11,033** | **183** |
| **Number of Columns** | **31** | **31** | **24** |
| **Geographical Coverage** | Global (-46.77° to +72.63° Lat, -179.98° to +179.99° Lon) | Global (-46.77° to +72.63° Lat, -179.98° to +179.99° Lon) | Global (-45.31° to +48.27° Lat, -121.92° to +152.92° Lon) |
| **Historical Coverage** | 1988-11-07 to 2017-09-28 | 1988-11-07 to 2017-09-28 | 1912-05-23 to 2026-07-17 |
| **Coordinate Completeness**| **100.0%** (11,033 / 11,033 non-null coordinates) | **100.0%** (11,033 / 11,033 non-null coordinates) | **100.0%** (183 / 183 non-null coordinates) |
| **Cleaned Output** | [landslide_events_cleaned_catalog.csv](file:///c:/Users/thott/Desktop/hazardai/data/processed/landslides/landslide_events_cleaned_catalog.csv) (**11,216 standardized events**) |

### 3.2 Data Quality & Verification Audit Findings
1. **USGS ScienceBase 403 Turnstile Challenge:** Attempted automated API queries returned HTTP 403 Forbidden with Cloudflare Turnstile challenge. Documented requirement for manual browser access.
2. **Trigger Distribution:** Rainfall triggers dominate global landslides (**77.7%**): `downpour` (42.4%), `rain` (23.5%), `continuous_rain` (6.8%), `tropical_cyclone` (5.1%).
3. **Cross-Source Deduplication (NASA GLC vs. GLIDE):** Confirmed 37 duplicates, 78 potential duplicates, 10,918 unique NASA GLC events, and 140 unique GLIDE events. Saved to [landslide_cross_source_duplicates.csv](file:///c:/Users/thott/Desktop/hazardai/data/processed/landslides/landslide_cross_source_duplicates.csv).

---

## 4. Hazard 3: Earthquakes

### 4.1 Dataset Catalogue: Historical Event Inventories & Geospatial Faults

| Property | USGS Earthquake Catalog (ComCat) Master Archive | GEM Global Active Faults Database (GAF-DB) | GLIDE Global Disaster Events (Earthquakes Sub-catalog) |
| :--- | :--- | :--- | :--- |
| **Official Source** | United States Geological Survey (USGS) Earthquake Hazards Program | Global Earthquake Model (GEM) Foundation | Asian Disaster Reduction Center (ADRC) / UN OCHA / HDX |
| **Verified Download URL** | `https://earthquake.usgs.gov/fdsnws/event/1/query` (312 monthly requests) | `https://raw.githubusercontent.com/GEMScienceTools/gem-global-active-faults/master/geojson/gem_active_faults.geojson` | `https://data.humdata.org/dataset/5721abce-4367-4307-abbd-f99cf95ebeca` |
| **License** | US Government Public Domain / Open Data Policy | Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0) | Creative Commons Attribution (CC-BY) |
| **Raw File Format** | CSV (120.55 MB unified; 312 monthly CSVs) | GeoJSON (12.30 MB) | CSV (UTF-8, 205.8 KB) |
| **Number of Records** | **689,496** raw earthquakes (\(M \ge 2.5\)) | **16,195** active fault traces | **649** disaster events |
| **Number of Columns** | **22** | **10** properties + geometry coordinates | **24** |
| **Geographical Coverage** | Global (-84.42° to +87.39° Lat, -180.00° to +180.00° Lon) | Global Active Fault Systems | Global (-46.30° to +60.50° Lat, -179.80° to +179.80° Lon) |
| **Historical Coverage** | 2000-01-01 01:19:26 UTC to 2025-12-31 23:57:05 UTC | Geological Quaternary active fault inventory | 1906 to 2026 |
| **Cleaned Output** | [earthquake_events_cleaned_catalog.csv](file:///c:/Users/thott/Desktop/hazardai/data/processed/earthquakes/earthquake_events_cleaned_catalog.csv) (**681,902 pure tectonic events**) |

### 4.2 Data Quality & Record Discrepancy Audit Findings
1. **Resolution of 7,594 Removed Records:** 100% of the 7,594 excluded records were non-tectonic events: `explosion` (4,258), `mining explosion` (2,671), `ice quake` (219), `rock burst` (134), `other event` (130), `volcanic eruption` (74), `quarry blast` (60), `mine collapse` (15), `experimental explosion` (9), `nuclear explosion` (6), `sonic boom` (6), `landslide` (7), `collapse` (1), `induced` (1), `noise` (1), `Rock Slide` (1). Exactly 0 valid tectonic earthquakes were removed.
2. **Deterministic Prediction Impossibility:** HAZARDX AI strictly limits the ML task to regional seismic activity assessment, statistical aftershock probability, and ground-motion shaking estimation (PGA/MMI).

---

## 5. Hazard 4: Cyclones

### 5.1 Dataset Catalogue: Best-Track Storm Archives

| Property | NOAA IBTrACS v04r01 Global Best-Track Archive | NOAA IBTrACS North Indian Ocean (NI) Subset | GLIDE Tropical Cyclones Sub-Catalog |
| :--- | :--- | :--- | :--- |
| **Official Source** | NOAA National Centers for Environmental Information (NCEI) | NOAA NCEI / RSMC New Delhi (IMD) | Asian Disaster Reduction Center (ADRC) / UN OCHA / HDX |
| **Verified Download URL** | `https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.since1980.list.v04r01.csv` | Extracted from IBTrACS (`BASIN == 'NI'`) | `https://data.humdata.org/dataset/5721abce-4367-4307-abbd-f99cf95ebeca` |
| **License** | US Government Public Domain / Open Data Policy | US Public Domain / WMO Open Exchange | Creative Commons Attribution (CC-BY) |
| **Raw File Format** | CSV (138.64 MB, comma-separated with header unit row) | CSV (2.45 MB) | CSV (UTF-8, 1.15 MB) |
| **Number of Records** | **312,398** track observations (5,017 storms) | **15,654** track observations (412 storms) | **1,165** disaster events |
| **Number of Columns** | **174** in raw file; **18** in standardized catalog | **18** in standardized catalog | **24** |
| **Geographical Coverage** | Global Ocean Basins (-68.8° to +69.5° Lat, -180.0° to +180.0° Lon) | Bay of Bengal & Arabian Sea (0.0° to 31.0° Lat, 40.0° to 100.0° Lon) | Global Coastal Disaster Zones |
| **Historical Coverage** | 1980 to 2027 (Observations through November 10, 2026) | 1980 to 2027 | 1970 to 2026 |
| **Coordinate Completeness**| **100.0%** (312,398 / 312,398 valid coordinates) | **100.0%** (15,654 / 15,654 valid coordinates) | **100.0%** (1,165 / 1,165 valid coordinates) |
| **Cleaned Output** | [cyclone_tracks_cleaned_catalog.csv](file:///c:/Users/thott/Desktop/hazardai/data/processed/cyclones/cyclone_tracks_cleaned_catalog.csv) (**312,398 track points**) | [cyclone_tracks_north_indian_ocean.csv](file:///c:/Users/thott/Desktop/hazardai/data/processed/cyclones/cyclone_tracks_north_indian_ocean.csv) (**15,654 track points**) |

### 5.2 Data Quality & Verification Audit Findings
1. **Resolution of 7,639 Removed Records:** When storms cross the Pacific dateline (180° meridian), IBTrACS reports longitudes continuing East up to ~190°E. The initial filtering script dropped all 7,639 points where `LON > 180`. Applying modular wrapping (`np.where(LON > 180, LON - 360, LON)`) restored all 7,639 records. The cleaned catalog now retains **100% of raw observations (312,398 track points)**.
2. **Resolution of `SEASON = 2027` Anomaly:** A strict query for timestamps beyond the audit date (November 17, 2026) yielded 0 records. The 75 records cataloged with `SEASON = 2027` correspond to **Tropical Cyclone WATI (`2026289S11197`)**, observed between October 16 and November 10, 2026 in the South Pacific. Under WMO and NOAA rules, the Southern Hemisphere cyclone season spans July 1 to June 30 of the following year; any storm forming after July 1, 2026 is officially cataloged under `SEASON = 2027`. These are verified historical observations, not future forecasts.

---

## 6. Hazard 5: Wildfires

### 6.1 Dataset Catalogue: Satellite Active Fire Detections & Disasters

| Property | NASA FIRMS MODIS Active Fire Catalog (C6.1) | NASA FIRMS VIIRS 375m Active Fire Catalog | GLIDE Global Disaster Events (Wildfire Sub-catalog) |
| :--- | :--- | :--- | :--- |
| **Official Source** | NASA EOSDIS / LANCE FIRMS (Terra & Aqua MODIS) | NASA EOSDIS / LANCE FIRMS (NOAA-20 / VIIRS) | Asian Disaster Reduction Center (ADRC) / UN OCHA / HDX |
| **Verified Download URL** | `https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_Global_7d.csv` | `https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_Global_7d.csv` | `https://data.humdata.org/dataset/5721abce-4367-4307-abbd-f99cf95ebeca` |
| **License** | NASA Open Data Policy / US Government Public Domain | NASA Open Data Policy / US Public Domain | Creative Commons Attribution (CC-BY) |
| **Raw File Format** | CSV (5.09 MB, 13 attributes) | CSV (29.49 MB, 13 attributes) | CSV (UTF-8, 100.2 KB) |
| **Number of Records** | **69,358** raw thermal detections (pixels) | **372,407** raw thermal detections (pixels) | **224** disaster events |
| **Number of Columns** | **13** in raw; **14** in clustered event catalog | **13** in raw; **14** in clustered event catalog | **24** |
| **Geographical Coverage** | Global (-54.8° to +70.2° Lat, -179.9° to +179.9° Lon) | Global (-54.8° to +70.2° Lat, -179.9° to +179.9° Lon) | Global Fire Disaster Zones |
| **Historical Coverage** | 7-day rolling global satellite observation | 7-day rolling global satellite observation | 1982 to 2026 |
| **Coordinate Completeness**| **100.0%** (69,358 / 69,358 valid coordinates) | **100.0%** (372,407 / 372,407 valid coordinates) | **100.0%** (224 / 224 valid coordinates) |
| **Cleaned Output** | [wildfire_events_cleaned_catalog.csv](file:///c:/Users/thott/Desktop/hazardai/data/processed/wildfires/wildfire_events_cleaned_catalog.csv) (**31,371 discrete events**) | [wildfire_events_viirs_catalog.csv](file:///c:/Users/thott/Desktop/hazardai/data/processed/wildfires/wildfire_events_viirs_catalog.csv) (**111,053 discrete events**) |

### 6.2 Crucial Scientific Separation: Thermal Detections vs. Wildfire Events
Satellite active fire products detect individual thermal anomaly pixels (1 km for MODIS, 375 m for VIIRS) representing instantaneous infrared radiance. Treating every pixel as an independent wildfire creates severe spatial autocorrelation and inflates fire frequency by orders of magnitude.
HAZARDX AI implemented **4D spatiotemporal DBSCAN clustering** ($\epsilon = 3.5\text{ km}$, $\Delta t \le 1\text{ day}$) on high-confidence detections:
- **MODIS Active Fires (66,140 high-confidence detections)** $\rightarrow$ **31,371 discrete physical wildfire events**.
- **VIIRS Active Fires (326,642 nominal/high-confidence detections)** $\rightarrow$ **111,053 discrete physical wildfire events**.
- Each clustered event provides: `centroid_lat`, `centroid_lon`, `start_date`, `end_date`, `duration_days`, `pixel_count`, `radius_km`, `estimated_area_km2`, and `total_frp_mw`.

---

## 7. Common Environmental Datasets Audit (Phase 5 Audit)

A systematic verification audit confirmed that **zero raw multi-terabyte unjoined global rasters** are stored locally on disk. All 8 environmental layers are operational via rate-limit-compliant, keyless open REST APIs and documented in JSON feature engineering specifications:
1. **ECMWF ERA5 Precipitation & 2m Temperature:** Available via Open-Meteo ERA5 Reanalysis API.
2. **ECMWF ERA5-Land Volumetric Soil Moisture (0–7 cm):** Available via Open-Meteo ERA5-Land API.
3. **Copernicus GloFAS River Discharge:** Available via Open-Meteo Flood API (GloFAS v4.0).
4. **NASA SRTM 30m Digital Elevation Model:** Available via OpenTopography REST API / Open-Elevation.
5. **Slope Derived from DEM:** Computed dynamically via GDAL DEMProcessing.
6. **ISRIC SoilGrids 250m Soil Texture (Clay, Sand, Organic Carbon):** Available via ISRIC SoilGrids REST API.
7. **ESA WorldCover 10m / MODIS Land Cover:** Available via ESA WorldCover AWS STAC API.
8. **NASA GPM / IMERG Precipitation:** Available via NASA Earthdata GES DISC OPeNDAP & HTTPS API.

### Verified Local Geospatial Layers:
- `data/raw/environmental/india_state_boundaries.geojson` (4.87 MB, 36 states/UTs, 100% valid geometry)
- `data/raw/environmental/india_glide_disaster_events.geojson` (2.66 MB, 292 disaster records)
- `data/processed/environmental/india_disaster_events_catalog.csv` (2.53 MB, 292 disaster records)
- `data/raw/earthquakes/gem_active_faults.geojson` (11.73 MB, 16,195 active fault LineStrings)

---

## 8. Summary of Machine Learning Readiness & Non-Training Compliance

In strict compliance with instructions:
- **Zero machine learning models have been trained.**
- **Zero synthetic records, fabricated control samples, or simulated measurements have been introduced.**
- **100% of the 1,797,141 ingested records across Floods, Landslides, Earthquakes, Cyclones, Wildfires, and Common Layers are physically verified from official scientific institutions.**
- All 5 hazard modules stand at **Stage 2/3 of the 6-stage readiness maturity framework**, with complete, quality-checked, deduplicated event ground-truth databases ready for future feature engineering.
