# HAZARDX AI — Cross-Dataset Integration & Spatial Compatibility Report

**Author:** HAZARDX AI Geospatial & Machine Learning Integration Team  
**Date:** 2026-11-17  
**Objective:** Establish mathematically and physically defensible integration pipelines for all 5 natural hazards.

---

## 1. Spatial & Temporal Harmonization Framework

| Integration Dimension | Standard Adopted | Compatibility Across Hazards | Validation Status |
|:---|:---|:---|:---|
| **Coordinate Reference System (CRS)** | WGS84 Decimal Degrees (`EPSG:4326`) | 100% unified across Floods, Landslides, Earthquakes, Cyclones, Wildfires, and Faults | Verified |
| **Temporal Standard** | ISO 8601 (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SSZ`) UTC | Unified across all historical event catalogues | Verified |
| **Grid Alignment Strategy** | Bilinear interpolation & Nearest-Neighbor on regular 0.05° / 0.1° grids | Reanalysis (ERA5, GPM, GloFAS) easily sampled at event points | Verified |

---

## 2. Hazard-Specific Integration Pipelines

### 2.1 Flood Module Integration
- **Anchor Dataset:** `data/processed/floods/flood_events_cleaned_catalog.csv` (6,761 historical flood footprints).
- **Physical Integration Strategy:**
  1. For each flood point $(x_i, y_i)$ and onset date $t_i$, sample antecedent cumulative precipitation $P_{1d}, P_{3d}, P_{7d}, P_{14d}$ from ECMWF ERA5 / GPM.
  2. Query daily upstream river discharge $Q(t)$ from GloFAS reanalysis.
  3. Extract static topographic covariates from NASA SRTM DEM (Elevation, Slope, Topographic Wetness Index $TWI = \ln(a / 	an eta)$, and Height Above Nearest Drainage [HAND]).
  4. Spatial join with OpenStreetMap / HydroSHEDS distance to river channels.
- **Negative Control Sampling Protocol:** Generate spatio-temporal controls ($y=0$) outside historical flood zones during equivalent seasonal windows.

### 2.2 Landslide Module Integration
- **Anchor Dataset:** `data/processed/landslides/landslide_events_cleaned_catalog.csv` (11,216 historical events).
- **Physical Integration Strategy:**
  1. Topographic overlay: Extract slope, aspect, planform/profile curvature from NASA SRTM 30m.
  2. Geotechnical overlay: Sample soil clay, sand, silt fractions, and depth-to-bedrock from ISRIC SoilGrids.
  3. Dynamic hydrometeorology: Join 24h peak rainfall and 7-day antecedent rainfall from ERA5/GPM, plus rootzone soil moisture from SMAP/ERA5-Land.
  4. Anthropogenic distance overlay: Calculate Euclidean distance to nearest road cuts (OpenStreetMap) and river drainage channels (HydroSHEDS).
- **Negative Control Sampling Protocol:** Stratified sampling across diverse terrain slopes (including stable slopes and steep forested slopes during dry/untriggered periods).

### 2.3 Earthquake Module Integration
- **Anchor Dataset:** `data/processed/earthquakes/earthquake_events_cleaned_catalog.csv` (681,902 pure tectonic earthquakes).
- **Physical Integration Strategy:**
  1. Fault Proximity Join: Compute shortest 2D/3D Euclidean distance to nearest fault trace in `data/raw/earthquakes/gem_active_faults.geojson` (16,195 active faults).
  2. Attach nearest fault kinematics (slip type: normal, reverse, strike-slip) and slip rate (mm/yr).
  3. Site Geology Overlay: Extract time-averaged shear-wave velocity $V_{S30}$ from USGS Global $V_{S30}$ Mosaic (Heath et al. 2020) and SRTM slope proxy.
  4. Spatio-Temporal Seismicity Metrics: Calculate rolling 30-day and 365-day event counts within 50 km and regional Gutenberg-Richter $b$-value.

### 2.4 Cyclone Module Integration
- **Anchor Dataset:** `data/processed/cyclones/cyclone_tracks_cleaned_catalog.csv` (312,398 track points) & `cyclone_tracks_north_indian_ocean.csv` (15,654 track points).
- **Physical Integration Strategy:**
  1. Compute track kinematics: Translational velocity $ec{v}_{trans}$, forward heading $	heta$, and 12h/24h intensity change $\Delta V_{wind}$, $\Delta P_{pres}$.
  2. Join oceanic thermal conditions: Daily Sea Surface Temperature (SST) and Ocean Heat Content (OHC) along storm track.
  3. Atmospheric environment join: Vertical wind shear (200 hPa – 850 hPa) and mid-tropospheric relative humidity from ERA5.

### 2.5 Wildfire Module Integration
- **Anchor Dataset:** `data/processed/wildfires/wildfire_events_cleaned_catalog.csv` (31,371 discrete events derived via 4D DBSCAN clustering of NASA FIRMS MODIS active fire detections) and `wildfire_disaster_events_glide.csv` (224 disaster records).
- **Physical Integration Strategy:**
  1. Atmospheric fire weather overlay: Sample 2m air temperature, relative humidity, and 10m wind speed from ERA5 reanalysis.
  2. Fire Weather Index (FWI) extraction: Join Canadian Forest Fire Weather Index system components (FFMC, DMC, DC, ISI, BUI, FWI) from Copernicus CEMS / ERA5.
  3. Fuel moisture proxy: Query topsoil volumetric soil water (0–7 cm depth) from ERA5-Land.
  4. Topographic slope acceleration: Extract slope in degrees from NASA SRTM 30m DEM (wildfires spread rapidly uphill due to convective pre-heating).
  5. Fuel load & vegetation curing: Extract NDVI from MODIS (MOD13A2) or Sentinel-2 to capture live fuel curing.
  6. Human ignition accessibility: Compute Euclidean distance to primary and secondary roads from OpenStreetMap.
- **Negative Control Sampling Protocol:** Spatiotemporally matched non-fire background locations sampled across identical biomes, vegetation types, and seasons without thermal anomalies.