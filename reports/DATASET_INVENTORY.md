# HAZARDX AI — Complete Project & Data Inventory
## Multi-Hazard Intelligence & Early Warning System Repository Audit

**Author:** HAZARDX AI Data Engineering & Geospatial Science Team  
**Audit Date:** 2026-11-17  
**Verification Standard:** 100% empirical file verification on disk. Zero fabricated records.

---

## 1. Master Repository Inventory (All 5 Hazards & Common Layers)

| # | Hazard Module | Dataset Name | File Path | Format | File Size | Record / Feature Count | Attribute Count | Geographic Bounds | Temporal Coverage | Role & Status |
|---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | **Floods** | DFO Spatial Flood Archive | `data/raw/floods/dfo_spatial_flood_archive_1985_2010.csv` | CSV | 1.05 MB | 4,029 events | 35 | Lat [-45.7°, 66.8°], Lon [-173.5°, 179.7°] | 1985-01-01 to 2010-08-11 | Raw Historical Ground Truth (Complete) |
| 2 | **Floods** | DFO Master Tabular Records | `data/raw/floods/dfo_flood_records_1985_2024.csv` | CSV | 428.9 KB | 5,503 events | 12 | Global (411 countries/regions) | 1985-01-01 to 2024-01-09 | Historical Validation Catalog (Complete) |
| 3 | **Floods** | DFO Shapefile Layer | `data/raw/floods/dfo_shapefile/wlf_nhr_fl_dfomasterlist_20190418.shp` | SHP/DBF | 15.7 MB | 4,029 polygons/pts | 35 | Global | 1985–2010 | Geospatial Vector Polygons (Complete) |
| 4 | **Floods** | GLIDE Flood Sub-Catalog | `data/raw/floods/glide_flood_events.csv` | CSV | 1.22 MB | 2,732 events | 24 | Lat [-50.2°, 66.8°], Lon [-172.1°, 179.8°] | 1972-06-09 to 2026-10-29 | Disaster Impact Ground Truth (Complete) |
| 5 | **Floods** | Cleaned Flood Catalog | `data/processed/floods/flood_events_cleaned_catalog.csv` | CSV | 1.07 MB | 6,761 events | 15 | Global (99.99% valid coords) | 1972-06-09 to 2026-10-29 | Standardized Training Catalog (Complete) |
| 6 | **Floods** | Cross-Source Duplicates Audit | `data/processed/floods/flood_cross_source_duplicates.csv` | CSV | 14.2 KB | 88 pairs | 10 | Global | 1990–2010 | Deduplication Audit Table (Complete) |
| 7 | **Landslides** | NASA Global Landslide Catalog | `data/raw/landslides/nasa_global_landslide_catalog_point.csv` | CSV | 8.48 MB | 11,033 events | 31 | Lat [-46.8°, 72.6°], Lon [-179.98°, 179.99°] | 1988-11-07 to 2017-09-28 | Primary Occurrence Ground Truth (Complete) |
| 8 | **Landslides** | NASA GLC Shapefile Layer | `data/raw/landslides/nasa_shapefile/global_landslide_catalog_NASA.shp` | SHP/DBF | 66.4 MB | 11,033 points | 31 | Global | 1988–2017 | Spatial GIS Vector Layer (Complete) |
| 9 | **Landslides** | GLIDE Landslide Sub-Catalog | `data/raw/landslides/glide_landslide_events.csv` | CSV | 74.4 KB | 183 events | 24 | Lat [-45.3°, 48.3°], Lon [-121.9°, 152.9°] | 1912-05-23 to 2026-07-17 | Disaster Impact Inventory (Complete) |
| 10 | **Landslides** | Cleaned Landslide Catalog | `data/processed/landslides/landslide_events_cleaned_catalog.csv` | CSV | 1.78 MB | 11,216 events | 15 | Global (100% valid coords & dates) | 1912-05-23 to 2026-07-17 | Standardized Training Catalog (Complete) |
| 11 | **Landslides** | Cross-Source Duplicates Audit | `data/processed/landslides/landslide_cross_source_duplicates.csv` | CSV | 19.8 KB | 115 pairs | 10 | Global | 1993–2017 | Deduplication Audit Table (Complete) |
| 12 | **Earthquakes** | USGS ComCat Historical Catalog | `data/raw/earthquakes/usgs_earthquakes_2000_2025.csv` | CSV | 120.55 MB | 689,496 events | 22 | Lat [-84.4°, 87.4°], Lon [-180.0°, 180.0°] | 2000-01-01 to 2025-12-31 | Primary Global Seismicity Archive (Complete) |
| 13 | **Earthquakes** | Monthly Partitioned Archive | `data/raw/earthquakes/monthly/` (312 CSVs) | CSVs | ~120 MB | 689,496 events | 22 | Global | 2000–2025 (Month-by-month) | Partitioned Acquisition Cache (Complete) |
| 14 | **Earthquakes** | GEM Global Active Faults | `data/raw/earthquakes/gem_active_faults.geojson` | GeoJSON | 12.30 MB | 16,195 faults | 10 | Global Active Fault Systems | Quaternary active faults | Tectonic Covariate Layer (Complete) |
| 15 | **Earthquakes** | GLIDE Earthquake Disasters | `data/raw/earthquakes/glide_earthquake_events.csv` | CSV | 205.8 KB | 649 events | 24 | Lat [-46.3°, 60.5°], Lon [-179.8°, 179.8°] | 1906–2026 | Disaster Casualty Ground Truth (Complete) |
| 16 | **Earthquakes** | Cleaned Tectonic Catalog | `data/processed/earthquakes/earthquake_events_cleaned_catalog.csv` | CSV | 104.38 MB | 681,902 events | 19 | Global (100% valid coords, depths, mag) | 2000-01-01 to 2025-12-31 | Pure Tectonic Earthquake Matrix (Complete) |
| 17 | **Cyclones** | NOAA IBTrACS v04r01 Archive | `data/raw/cyclones/ibtracs_since1980_v04r01.csv` | CSV | 138.64 MB | 312,398 track pts | 174 | Lat [-68.8°, 69.5°], Lon [-180.0°, 180.0°] | 1980 to 2027 (5,017 storms) | Primary Global Best-Track Archive (Complete) |
| 18 | **Cyclones** | GLIDE Cyclone Sub-Catalog | `data/raw/cyclones/glide_cyclone_events.csv` | CSV | 1.15 MB | 1,165 events | 24 | Global Coastal Zones | 1970–2026 | Cyclone Disaster Impact Records (Complete) |
| 19 | **Cyclones** | Cleaned Global Track Catalog | `data/processed/cyclones/cyclone_tracks_cleaned_catalog.csv` | CSV | 49.12 MB | 312,398 track pts | 18 | Global Ocean Basins | 1980–2027 | Normalized Storm Track Database (Complete) |
| 20 | **Cyclones** | North Indian Ocean Cyclone Tracks | `data/processed/cyclones/cyclone_tracks_north_indian_ocean.csv` | CSV | 2.45 MB | 15,654 track pts | 18 | Bay of Bengal & Arabian Sea (India) | 1980–2027 (412 storms) | Regional India Cyclone Early Warning (Complete) |
| 21 | **Wildfires** | NASA FIRMS MODIS Active Fire (7d) | `data/raw/wildfires/modis_active_fire_global_7d.csv` | CSV | 5.09 MB | 69,358 pixels | 13 | Global (MODIS 1km pixels) | 7-day rolling satellite observations | Raw Instantaneous Thermal Detections (Complete) |
| 22 | **Wildfires** | NASA FIRMS VIIRS Active Fire (7d) | `data/raw/wildfires/viirs_active_fire_global_7d.csv` | CSV | 29.49 MB | 372,407 pixels | 13 | Global (VIIRS 375m pixels) | 7-day rolling satellite observations | High-Resolution Thermal Detections (Complete) |
| 23 | **Wildfires** | GLIDE Wildfire Disasters | `data/raw/wildfires/glide_wildfire_disaster_events.csv` | CSV | 100.2 KB | 224 events | 24 | Global Fire Zones | 1982–2026 | Historical Wildfire Disasters (Complete) |
| 24 | **Wildfires** | Clustered Wildfire Events Catalog | `data/processed/wildfires/wildfire_events_cleaned_catalog.csv` | CSV | 3.25 MB | 31,371 events | 14 | Global Terrestrial Coverage | 2026 | DBSCAN Aggregated Wildfire Events (Complete) |
| 25 | **Wildfires** | VIIRS Clustered Events Catalog | `data/processed/wildfires/wildfire_events_viirs_catalog.csv` | CSV | 11.82 MB | 111,053 events | 14 | Global Terrestrial Coverage | 2026 | High-Res Clustered Fire Events (Complete) |
| 26 | **Wildfires** | GLIDE Processed Disasters | `data/processed/wildfires/wildfire_disaster_events_glide.csv` | CSV | 98.4 KB | 224 events | 24 | Global | 1982–2026 | Georeferenced Disaster Events (Complete) |
| 27 | **Common** | India State Boundaries | `data/raw/environmental/india_state_boundaries.geojson` | GeoJSON | 4.87 MB | 36 States/UTs | 11 | Lat [6.7°, 37.1°], Lon [68.1°, 97.4°] | 2020 boundary baseline | Official Subnational GIS Boundaries (Complete) |
| 28 | **Common** | India GLIDE Disaster Catalog | `data/raw/environmental/india_glide_disaster_events.geojson` | GeoJSON | 2.66 MB | 292 disasters | 24 | India & Adjacent Seas | 1970–2026 | National Multi-Hazard Historical Events (Complete) |
| 29 | **Common** | India Disasters Tabular | `data/processed/environmental/india_disaster_events_catalog.csv` | CSV | 2.53 MB | 292 disasters | 26 | India | 1970–2026 | Standardized Event Records (Complete) |
| 30 | **Common** | Kerala Disasters Subset | `data/processed/environmental/kerala_disaster_events.csv` | CSV | 18.5 KB | 13 disasters | 26 | Kerala, India | 2001–2024 | Focused State Multi-Hazard Baseline (Complete) |
| 31 | **Common** | Full GLIDE Master Archive | `data/raw/floods/glide_events_global.csv` | CSV | 3.75 MB | 9,142 disasters | 24 | Global | 1906–2026 | Multi-Hazard International Master Registry (Complete) |