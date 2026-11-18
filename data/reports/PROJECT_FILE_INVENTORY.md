# HAZARDX AI — Master Project File Inventory & Classification
## Recursive File Audit, Dependency Mapping, and Lifecycle Status

**Total Files Indexed:** 456  
**Total Workspace Footprint:** 864.01 MB  
**Audit Timestamp:** 2026-11-17

---

## 1. Classification Summary

| Category | File Count | Description |
| :--- | :---: | :--- |
| **ESSENTIAL** | **375** | Core production datasets (raw, processed, model-ready), master catalogs, and primary figures. |
| **ACTIVE** | **34** | Active feature engineering, data collection, audit scripts, and canonical reports. |
| **HISTORICAL** | **36** | Completed EDA modules, duplicate data reports, and superseded single-hazard prototype scripts. |
| **REDUNDANT** | **10** | Obsolete loose files in the root directory that have newer canonical versions in `reports/`. |
| **TEMPORARY** | **1** | Compiled Python bytecode (`__pycache__`) and intermediate runtime artifacts. |
| **UNKNOWN** | **0** | Files whose lifecycle state cannot be verified. |

---

## 2. Cleanup Candidates (Safe for Archiving)

The following files have been verified as either redundant root duplicates or obsolete prototypes without active references:

| File Path | Size (KB) | Category | Justification | Destination |
| :--- | :---: | :---: | :--- | :--- |
| `scripts/audit_and_process_earthquakes.py` | 4.77 | HISTORICAL | Early single-hazard prototype script superseded by modular subdirectories. | `_archive/scripts/audit_and_process_earthquakes.py` |
| `scripts/audit_landslides.py` | 3.19 | HISTORICAL | Early single-hazard prototype script superseded by modular subdirectories. | `_archive/scripts/audit_landslides.py` |
| `scripts/download_all_earthquakes.py` | 5.33 | HISTORICAL | Early single-hazard prototype script superseded by modular subdirectories. | `_archive/scripts/download_all_earthquakes.py` |
| `scripts/download_earthquakes.py` | 3.37 | HISTORICAL | Early single-hazard prototype script superseded by modular subdirectories. | `_archive/scripts/download_earthquakes.py` |
| `scripts/process_floods.py` | 3.96 | HISTORICAL | Early single-hazard prototype script superseded by modular subdirectories. | `_archive/scripts/process_floods.py` |
| `scripts/process_landslides.py` | 3.8 | HISTORICAL | Early single-hazard prototype script superseded by modular subdirectories. | `_archive/scripts/process_landslides.py` |
| `DATASET_INTEGRATION_REPORT.md` | 4.07 | REDUNDANT | Outdated duplicate of canonical report located in reports/. | `_archive/DATASET_INTEGRATION_REPORT.md` |
| `DATASET_INVENTORY.md` | 5.9 | REDUNDANT | Outdated duplicate of canonical report located in reports/. | `_archive/DATASET_INVENTORY.md` |
| `DATASET_METADATA.json` | 2.37 | REDUNDANT | Outdated duplicate of canonical report located in reports/. | `_archive/DATASET_METADATA.json` |
| `DATASET_REPORT.md` | 18.09 | REDUNDANT | Outdated duplicate of canonical report located in reports/. | `_archive/DATASET_REPORT.md` |
| `DATASET_SUITABILITY_REPORT.md` | 11.46 | REDUNDANT | Outdated duplicate of canonical report located in reports/. | `_archive/DATASET_SUITABILITY_REPORT.md` |
| `DATA_COLLECTION_REPORT.md` | 2.79 | REDUNDANT | Outdated duplicate of canonical report located in reports/. | `_archive/DATA_COLLECTION_REPORT.md` |
| `DATA_QUALITY_REPORT.md` | 3.69 | REDUNDANT | Outdated duplicate of canonical report located in reports/. | `_archive/DATA_QUALITY_REPORT.md` |
| `DATA_READINESS_MATRIX.md` | 5.09 | REDUNDANT | Outdated duplicate of canonical report located in reports/. | `_archive/DATA_READINESS_MATRIX.md` |
| `DATA_SOURCE_REGISTER.csv` | 2.5 | REDUNDANT | Outdated duplicate of canonical report located in reports/. | `_archive/DATA_SOURCE_REGISTER.csv` |
| `EDA_REPORT.md` | 3.43 | REDUNDANT | Outdated duplicate of canonical report located in reports/. | `_archive/EDA_REPORT.md` |
| `scripts/__pycache__/download_earthquakes.cpython-311.pyc` | 4.6 | TEMPORARY | Compiled Python bytecode cache. | `_archive/scripts/__pycache__/download_earthquakes.cpython-311.pyc` |

---

## 3. Complete File Inventory

| File Path | Size (KB) | Category | Actively Used | Contains Data | Purpose | References |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| `data/raw/environmental/extracted/flood_era5_cache.json` | 0.0 | ACTIVE | YES | YES | Cached API extraction responses from ERA5 / GloFAS. | 0 |
| `data/raw/environmental/extracted/flood_glofas_cache.json` | 205.03 | ACTIVE | YES | YES | Cached API extraction responses from ERA5 / GloFAS. | 0 |
| `data/raw/environmental/extracted/landslide_era5_cache.json` | 0.0 | ACTIVE | YES | YES | Cached API extraction responses from ERA5 / GloFAS. | 0 |
| `reports/DATASET_INTEGRATION_REPORT.md` | 5.34 | ACTIVE | YES | NO | Canonical project documentation and data governance report. | 2 |
| `reports/DATASET_INVENTORY.md` | 7.98 | ACTIVE | YES | NO | Canonical project documentation and data governance report. | 2 |
| `reports/DATASET_METADATA.json` | 3.61 | ACTIVE | YES | NO | Canonical project documentation and data governance report. | 2 |
| `reports/DATASET_REPORT.md` | 21.1 | ACTIVE | YES | NO | Canonical project documentation and data governance report. | 0 |
| `reports/DATASET_SUITABILITY_REPORT.md` | 14.25 | ACTIVE | YES | NO | Canonical project documentation and data governance report. | 2 |
| `reports/DATA_COLLECTION_REPORT.md` | 2.79 | ACTIVE | YES | NO | Canonical project documentation and data governance report. | 0 |
| `reports/DATA_QUALITY_REPORT.md` | 10.28 | ACTIVE | YES | NO | Canonical project documentation and data governance report. | 2 |
| `reports/DATA_READINESS_MATRIX.md` | 6.11 | ACTIVE | YES | NO | Canonical project documentation and data governance report. | 2 |
| `reports/DATA_SOURCE_REGISTER.csv` | 3.11 | ACTIVE | YES | NO | Canonical project documentation and data governance report. | 2 |
| `reports/EDA_REPORT.md` | 4.75 | ACTIVE | YES | NO | Canonical project documentation and data governance report. | 2 |
| `reports/ENVIRONMENTAL_DATASET_VERIFICATION.json` | 8.78 | ACTIVE | YES | NO | Canonical project documentation and data governance report. | 2 |
| `reports/ML_TRAINING_READINESS_REPORT.md` | 11.89 | ACTIVE | YES | NO | Canonical project documentation and data governance report. | 0 |
| `reports/audit/INDEPENDENT_AUDIT_METRICS.json` | 29.04 | ACTIVE | YES | YES | Audit metrics and validation verification output. | 0 |
| `scripts/audit/generate_project_inventory.py` | 8.03 | ACTIVE | YES | NO | Active independent dataset and project structure audit script. | 0 |
| `scripts/audit/run_independent_dataset_audit.py` | 17.36 | ACTIVE | YES | NO | Active independent dataset and project structure audit script. | 0 |
| `scripts/audit/verify_environmental_datasets.py` | 10.05 | ACTIVE | YES | NO | Active independent dataset and project structure audit script. | 0 |
| `scripts/data_collection/download_cyclone_data.py` | 3.91 | ACTIVE | YES | NO | Active official API downloader and raw processor. | 0 |
| `scripts/data_collection/download_earthquake_data.py` | 3.49 | ACTIVE | YES | NO | Active official API downloader and raw processor. | 0 |
| `scripts/data_collection/download_environmental_data.py` | 3.27 | ACTIVE | YES | NO | Active official API downloader and raw processor. | 0 |
| `scripts/data_collection/download_flood_data.py` | 2.73 | ACTIVE | YES | NO | Active official API downloader and raw processor. | 1 |
| `scripts/data_collection/download_landslide_data.py` | 1.97 | ACTIVE | YES | NO | Active official API downloader and raw processor. | 0 |
| `scripts/data_collection/download_wildfire_data.py` | 2.53 | ACTIVE | YES | NO | Active official API downloader and raw processor. | 0 |
| `scripts/data_collection/process_wildfire_data.py` | 12.55 | ACTIVE | YES | NO | Active official API downloader and raw processor. | 0 |
| `scripts/ml_prep/__pycache__/validate_all_datasets.cpython-311.pyc` | 13.37 | ACTIVE | YES | NO | Active ML dataset engineering, validation, or report compilation script. | 0 |
| `scripts/ml_prep/build_cyclone_dataset.py` | 9.86 | ACTIVE | YES | NO | Active ML dataset engineering, validation, or report compilation script. | 0 |
| `scripts/ml_prep/build_earthquake_dataset.py` | 12.81 | ACTIVE | YES | NO | Active ML dataset engineering, validation, or report compilation script. | 0 |
| `scripts/ml_prep/build_flood_dataset.py` | 15.64 | ACTIVE | YES | NO | Active ML dataset engineering, validation, or report compilation script. | 0 |
| `scripts/ml_prep/build_landslide_dataset.py` | 14.06 | ACTIVE | YES | NO | Active ML dataset engineering, validation, or report compilation script. | 0 |
| `scripts/ml_prep/build_wildfire_dataset.py` | 11.11 | ACTIVE | YES | NO | Active ML dataset engineering, validation, or report compilation script. | 0 |
| `scripts/ml_prep/generate_readiness_report.py` | 16.49 | ACTIVE | YES | NO | Active ML dataset engineering, validation, or report compilation script. | 0 |
| `scripts/ml_prep/validate_all_datasets.py` | 11.82 | ACTIVE | YES | NO | Active ML dataset engineering, validation, or report compilation script. | 1 |
| `data/model_ready/cyclones/cyclone_features_metadata.json` | 1.16 | ESSENTIAL | YES | YES | Final model-ready training matrix or feature schema metadata. | 0 |
| `data/model_ready/cyclones/cyclone_model_ready.csv` | 30136.18 | ESSENTIAL | YES | YES | Final model-ready training matrix or feature schema metadata. | 1 |
| `data/model_ready/earthquakes/earthquake_features_metadata.json` | 1.31 | ESSENTIAL | YES | YES | Final model-ready training matrix or feature schema metadata. | 0 |
| `data/model_ready/earthquakes/earthquake_model_ready.csv` | 1176.7 | ESSENTIAL | YES | YES | Final model-ready training matrix or feature schema metadata. | 1 |
| `data/model_ready/floods/flood_features_metadata.json` | 1.11 | ESSENTIAL | YES | YES | Final model-ready training matrix or feature schema metadata. | 0 |
| `data/model_ready/floods/flood_model_ready.csv` | 87.41 | ESSENTIAL | YES | YES | Final model-ready training matrix or feature schema metadata. | 1 |
| `data/model_ready/landslides/landslide_features_metadata.json` | 1.13 | ESSENTIAL | YES | YES | Final model-ready training matrix or feature schema metadata. | 0 |
| `data/model_ready/landslides/landslide_model_ready.csv` | 86.59 | ESSENTIAL | YES | YES | Final model-ready training matrix or feature schema metadata. | 1 |
| `data/model_ready/wildfires/wildfire_features_metadata.json` | 1.12 | ESSENTIAL | YES | YES | Final model-ready training matrix or feature schema metadata. | 0 |
| `data/model_ready/wildfires/wildfire_model_ready.csv` | 296.05 | ESSENTIAL | YES | YES | Final model-ready training matrix or feature schema metadata. | 1 |
| `data/processed/cyclones/cyclone_tracks_cleaned_catalog.csv` | 30397.17 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/processed/cyclones/cyclone_tracks_north_indian_ocean.csv` | 1486.38 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/processed/earthquakes/earthquake_events_cleaned_catalog.csv` | 106882.08 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 1 |
| `data/processed/earthquakes/earthquake_features_spec.json` | 4.84 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/processed/environmental/india_disaster_events_catalog.csv` | 2592.65 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/processed/environmental/kerala_disaster_events.csv` | 4.57 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/processed/floods/flood_cross_source_duplicates.csv` | 19.02 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/processed/floods/flood_environmental_features_spec.json` | 3.21 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/processed/floods/flood_events_cleaned_catalog.csv` | 1041.64 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 1 |
| `data/processed/landslides/landslide_cross_source_duplicates.csv` | 26.57 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/processed/landslides/landslide_environmental_features_spec.json` | 4.87 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/processed/landslides/landslide_events_cleaned_catalog.csv` | 1742.71 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 1 |
| `data/processed/wildfires/wildfire_disaster_events_glide.csv` | 71.09 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/processed/wildfires/wildfire_environmental_features_spec.json` | 3.97 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/processed/wildfires/wildfire_events_cleaned_catalog.csv` | 3079.03 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/processed/wildfires/wildfire_events_viirs_catalog.csv` | 10718.47 | ESSENTIAL | YES | YES | Quality-checked, deduplicated hazard catalog required for ML preparation. | 0 |
| `data/raw/cyclone/ibtracs.since1980.list.v04r01.csv` | 141963.76 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/cyclones/glide_cyclone_events.csv` | 521.42 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/cyclones/ibtracs_since1980_v04r01.csv` | 141963.76 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/earthquakes/gem_active_faults.geojson` | 12014.46 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/earthquakes/glide_earthquake_events.csv` | 200.99 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2000_01.csv` | 212.33 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2000_02.csv` | 192.03 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2000_03.csv` | 228.22 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2000_04.csv` | 242.99 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2000_05.csv` | 265.17 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2000_06.csv` | 260.75 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2000_07.csv` | 291.51 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2000_08.csv` | 266.23 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2000_09.csv` | 218.73 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2000_10.csv` | 230.59 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2000_11.csv` | 322.7 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2000_12.csv` | 259.28 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2001_01.csv` | 280.65 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2001_02.csv` | 266.27 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2001_03.csv` | 261.58 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2001_04.csv` | 311.05 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2001_05.csv` | 255.89 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2001_06.csv` | 294.08 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2001_07.csv` | 303.42 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2001_08.csv` | 278.19 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2001_09.csv` | 257.28 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2001_10.csv` | 289.79 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2001_11.csv` | 272.17 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2001_12.csv` | 294.76 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2002_01.csv` | 300.38 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2002_02.csv` | 276.31 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2002_03.csv` | 316.25 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2002_04.csv` | 285.19 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2002_05.csv` | 270.51 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2002_06.csv` | 288.48 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2002_07.csv` | 265.13 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2002_08.csv` | 272.95 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2002_09.csv` | 337.11 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2002_10.csv` | 314.82 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2002_11.csv` | 586.44 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2002_12.csv` | 332.05 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2003_01.csv` | 298.52 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2003_02.csv` | 288.45 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2003_03.csv` | 372.9 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2003_04.csv` | 325.07 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2003_05.csv` | 338.89 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2003_06.csv` | 363.96 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2003_07.csv` | 326.53 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2003_08.csv` | 330.67 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2003_09.csv` | 318.71 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2003_10.csv` | 319.55 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2003_11.csv` | 346.87 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2003_12.csv` | 433.83 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2004_01.csv` | 356.6 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2004_02.csv` | 371.45 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2004_03.csv` | 359.32 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2004_04.csv` | 326.75 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2004_05.csv` | 386.67 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2004_06.csv` | 335.87 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2004_07.csv` | 329.03 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2004_08.csv` | 368.86 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2004_09.csv` | 444.34 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2004_10.csv` | 459.07 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2004_11.csv` | 416.25 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2004_12.csv` | 484.76 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2005_01.csv` | 541.67 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2005_02.csv` | 355.21 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2005_03.csv` | 483.46 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2005_04.csv` | 502.21 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2005_05.csv` | 432.15 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2005_06.csv` | 431.65 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2005_07.csv` | 406.14 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2005_08.csv` | 386.8 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2005_09.csv` | 407.56 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2005_10.csv` | 490.14 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2005_11.csv` | 374.3 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2005_12.csv` | 389.08 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2006_01.csv` | 373.11 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2006_02.csv` | 361.76 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2006_03.csv` | 451.0 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2006_04.csv` | 469.55 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2006_05.csv` | 479.44 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2006_06.csv` | 572.42 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2006_07.csv` | 486.49 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2006_08.csv` | 443.67 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2006_09.csv` | 389.75 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2006_10.csv` | 424.33 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2006_11.csv` | 526.6 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2006_12.csv` | 408.32 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2007_01.csv` | 452.7 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2007_02.csv` | 329.56 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2007_03.csv` | 407.49 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2007_04.csv` | 528.59 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2007_05.csv` | 399.44 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2007_06.csv` | 388.62 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2007_07.csv` | 437.34 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2007_08.csv` | 513.61 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2007_09.csv` | 443.84 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2007_10.csv` | 443.26 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2007_11.csv` | 364.9 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2007_12.csv` | 427.97 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2008_01.csv` | 390.61 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2008_02.csv` | 496.79 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2008_03.csv` | 477.53 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2008_04.csv` | 477.57 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2008_05.csv` | 557.65 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2008_06.csv` | 516.93 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2008_07.csv` | 473.45 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2008_08.csv` | 504.2 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2008_09.csv` | 354.42 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2008_10.csv` | 448.94 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2008_11.csv` | 399.28 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2008_12.csv` | 386.28 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2009_01.csv` | 271.68 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2009_02.csv` | 223.16 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2009_03.csv` | 218.78 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2009_04.csv` | 212.54 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2009_05.csv` | 197.31 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2009_06.csv` | 204.69 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2009_07.csv` | 205.37 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2009_08.csv` | 233.69 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2009_09.csv` | 196.78 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2009_10.csv` | 289.39 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2009_11.csv` | 198.04 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2009_12.csv` | 187.94 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2010_01.csv` | 246.7 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2010_02.csv` | 284.66 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2010_03.csv` | 354.96 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2010_04.csv` | 699.12 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2010_05.csv` | 309.52 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2010_06.csv` | 285.66 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2010_07.csv` | 538.58 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2010_08.csv` | 343.23 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2010_09.csv` | 283.27 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2010_10.csv` | 282.72 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2010_11.csv` | 294.08 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2010_12.csv` | 381.77 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2011_01.csv` | 300.25 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2011_02.csv` | 250.84 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2011_03.csv` | 713.83 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2011_04.csv` | 352.98 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2011_05.csv` | 321.85 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2011_06.csv` | 288.2 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2011_07.csv` | 341.02 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2011_08.csv` | 296.96 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2011_09.csv` | 272.57 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2011_10.csv` | 262.85 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2011_11.csv` | 277.99 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2011_12.csv` | 232.63 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2012_01.csv` | 250.77 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2012_02.csv` | 267.41 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2012_03.csv` | 270.9 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2012_04.csv` | 324.79 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2012_05.csv` | 260.24 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2012_06.csv` | 236.45 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2012_07.csv` | 241.15 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2012_08.csv` | 321.93 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2012_09.csv` | 376.65 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2012_10.csv` | 291.34 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2012_11.csv` | 272.33 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2012_12.csv` | 260.59 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2013_01.csv` | 296.18 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2013_02.csv` | 332.47 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2013_03.csv` | 235.53 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2013_04.csv` | 273.29 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2013_05.csv` | 307.22 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2013_06.csv` | 249.42 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2013_07.csv` | 267.95 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2013_08.csv` | 296.32 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2013_09.csv` | 302.51 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2013_10.csv` | 297.18 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2013_11.csv` | 361.81 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2013_12.csv` | 331.94 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2014_01.csv` | 427.68 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2014_02.csv` | 320.92 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2014_03.csv` | 414.91 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2014_04.csv` | 510.94 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2014_05.csv` | 405.74 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2014_06.csv` | 501.24 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2014_07.csv` | 425.81 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2014_08.csv` | 390.12 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2014_09.csv` | 375.62 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2014_10.csv` | 427.22 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2014_11.csv` | 476.9 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2014_12.csv` | 386.22 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2015_01.csv` | 394.85 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2015_02.csv` | 346.94 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2015_03.csv` | 375.36 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2015_04.csv` | 356.36 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2015_05.csv` | 436.99 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2015_06.csv` | 346.97 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2015_07.csv` | 460.45 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2015_08.csv` | 408.9 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2015_09.csv` | 530.83 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2015_10.csv` | 381.92 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2015_11.csv` | 415.68 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2015_12.csv` | 368.19 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2016_01.csv` | 408.3 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2016_02.csv` | 358.49 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2016_03.csv` | 337.14 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2016_04.csv` | 422.03 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2016_05.csv` | 353.52 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2016_06.csv` | 354.7 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2016_07.csv` | 342.67 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2016_08.csv` | 378.0 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2016_09.csv` | 417.73 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2016_10.csv` | 325.95 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2016_11.csv` | 390.58 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2016_12.csv` | 426.13 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2017_01.csv` | 327.7 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2017_02.csv` | 255.54 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2017_03.csv` | 304.0 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2017_04.csv` | 345.13 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2017_05.csv` | 507.44 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2017_06.csv` | 307.75 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2017_07.csv` | 365.46 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2017_08.csv` | 312.75 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2017_09.csv` | 456.06 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2017_10.csv` | 288.78 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2017_11.csv` | 341.37 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2017_12.csv` | 301.29 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2018_01.csv` | 525.51 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2018_02.csv` | 486.71 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2018_03.csv` | 438.0 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2018_04.csv` | 380.15 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2018_05.csv` | 616.9 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2018_06.csv` | 1334.19 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2018_07.csv` | 1480.74 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2018_08.csv` | 668.54 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2018_09.csv` | 429.52 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2018_10.csv` | 419.49 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2018_11.csv` | 387.88 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2018_12.csv` | 494.66 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2019_01.csv` | 381.67 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2019_02.csv` | 343.73 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2019_03.csv` | 373.59 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2019_04.csv` | 358.63 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2019_05.csv` | 325.84 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2019_06.csv` | 345.37 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2019_07.csv` | 809.0 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2019_08.csv` | 321.96 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2019_09.csv` | 393.46 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2019_10.csv` | 384.54 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2019_11.csv` | 374.86 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2019_12.csv` | 431.73 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2020_01.csv` | 778.71 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2020_02.csv` | 426.8 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2020_03.csv` | 420.9 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2020_04.csv` | 496.26 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2020_05.csv` | 585.93 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2020_06.csv` | 462.11 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2020_07.csv` | 488.36 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2020_08.csv` | 410.2 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2020_09.csv` | 369.97 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2020_10.csv` | 568.86 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2020_11.csv` | 412.91 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2020_12.csv` | 432.62 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2021_01.csv` | 445.1 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2021_02.csv` | 422.8 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2021_03.csv` | 526.8 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2021_04.csv` | 375.58 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2021_05.csv` | 369.05 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2021_06.csv` | 396.97 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2021_07.csv` | 471.85 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2021_08.csv` | 609.91 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2021_09.csv` | 406.17 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2021_10.csv` | 374.16 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2021_11.csv` | 374.61 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2021_12.csv` | 453.57 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2022_01.csv` | 458.61 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2022_02.csv` | 385.03 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2022_03.csv` | 443.96 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2022_04.csv` | 396.04 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2022_05.csv` | 374.72 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2022_06.csv` | 386.19 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2022_07.csv` | 424.21 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2022_08.csv` | 437.41 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2022_09.csv` | 445.22 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2022_10.csv` | 400.23 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2022_11.csv` | 417.77 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2022_12.csv` | 396.71 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2023_01.csv` | 431.69 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2023_02.csv` | 428.99 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2023_03.csv` | 421.6 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2023_04.csv` | 391.8 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2023_05.csv` | 445.9 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2023_06.csv` | 398.09 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2023_07.csv` | 394.83 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2023_08.csv` | 386.9 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2023_09.csv` | 374.46 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2023_10.csv` | 429.33 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2023_11.csv` | 419.35 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2023_12.csv` | 566.51 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2024_01.csv` | 420.02 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2024_02.csv` | 409.45 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2024_03.csv` | 358.27 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2024_04.csv` | 425.47 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2024_05.csv` | 403.94 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2024_06.csv` | 375.0 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2024_07.csv` | 387.96 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2024_08.csv` | 378.64 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2024_09.csv` | 341.45 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2024_10.csv` | 385.95 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2024_11.csv` | 345.59 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2024_12.csv` | 487.98 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2025_01.csv` | 418.95 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2025_02.csv` | 405.63 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2025_03.csv` | 417.42 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2025_04.csv` | 401.25 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2025_05.csv` | 378.39 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2025_06.csv` | 376.75 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2025_07.csv` | 791.77 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2025_08.csv` | 582.82 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2025_09.csv` | 441.57 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2025_10.csv` | 379.61 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2025_11.csv` | 371.21 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/monthly/earthquakes_2025_12.csv` | 536.13 | ESSENTIAL | NO | YES | Raw USGS ComCat monthly earthquake partition (2000-2025). | 0 |
| `data/raw/earthquakes/usgs_earthquakes_2000_2025.csv` | 123447.08 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/environmental/india_glide_disaster_events.geojson` | 2727.34 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/environmental/india_state_boundaries.geojson` | 4984.13 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/flood/Global_Flood_Records.csv` | 418.81 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/floods/dfo_flood_records_1985_2024.csv` | 418.81 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/floods/dfo_shapefile/wlf_nhr_fl_dfomasterlist_20190418.cpg` | 0.0 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/floods/dfo_shapefile/wlf_nhr_fl_dfomasterlist_20190418.dbf` | 15192.5 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/floods/dfo_shapefile/wlf_nhr_fl_dfomasterlist_20190418.prj` | 0.14 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/floods/dfo_shapefile/wlf_nhr_fl_dfomasterlist_20190418.sbn` | 36.76 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/floods/dfo_shapefile/wlf_nhr_fl_dfomasterlist_20190418.sbx` | 1.29 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/floods/dfo_shapefile/wlf_nhr_fl_dfomasterlist_20190418.shp` | 110.27 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/floods/dfo_shapefile/wlf_nhr_fl_dfomasterlist_20190418.shx` | 31.57 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/floods/dfo_spatial_flood_archive_1985_2010.csv` | 1021.24 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/floods/glide_events_global.csv` | 3663.73 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/floods/glide_flood_events.csv` | 1192.89 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/landslide/Global_Landslide_Catalog_Export_rows.csv` | 8280.97 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/landslides/glide_landslide_events.csv` | 72.68 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/landslides/nasa_global_landslide_catalog_point.csv` | 8280.97 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/landslides/nasa_shapefile/global_landslide_catalog_NASA.dbf` | 64421.22 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/landslides/nasa_shapefile/global_landslide_catalog_NASA.prj` | 0.14 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/landslides/nasa_shapefile/global_landslide_catalog_NASA.shp` | 301.78 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/landslides/nasa_shapefile/global_landslide_catalog_NASA.shx` | 86.29 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/wildfires/glide_wildfire_disaster_events.csv` | 71.09 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/wildfires/modis_active_fire_global_7d.csv` | 5211.8 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `data/raw/wildfires/viirs_active_fire_global_7d.csv` | 30196.2 | ESSENTIAL | YES | YES | Authoritative raw hazard observation catalog or shapefile from official source. | 0 |
| `reports/figures/audit_class_distributions_5_hazards.png` | 172.89 | ESSENTIAL | YES | YES | Publication-quality visual figure illustrating data distributions. | 0 |
| `reports/figures/audit_cyclone_feature_distributions.png` | 688.52 | ESSENTIAL | YES | YES | Publication-quality visual figure illustrating data distributions. | 0 |
| `reports/figures/audit_earthquake_feature_distributions.png` | 272.35 | ESSENTIAL | YES | YES | Publication-quality visual figure illustrating data distributions. | 0 |
| `reports/figures/audit_flood_feature_distributions.png` | 274.82 | ESSENTIAL | YES | YES | Publication-quality visual figure illustrating data distributions. | 0 |
| `reports/figures/audit_landslide_feature_distributions.png` | 245.69 | ESSENTIAL | YES | YES | Publication-quality visual figure illustrating data distributions. | 0 |
| `reports/figures/audit_split_class_distributions.png` | 213.64 | ESSENTIAL | YES | YES | Publication-quality visual figure illustrating data distributions. | 0 |
| `reports/figures/audit_wildfire_feature_distributions.png` | 286.92 | ESSENTIAL | YES | YES | Publication-quality visual figure illustrating data distributions. | 0 |
| `data/reports/DATASET_INTEGRATION_REPORT.md` | 5.34 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 2 |
| `data/reports/DATASET_INVENTORY.md` | 7.98 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 2 |
| `data/reports/DATASET_METADATA.json` | 3.61 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 2 |
| `data/reports/DATASET_REPORT.md` | 21.1 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 0 |
| `data/reports/DATASET_SUITABILITY_REPORT.md` | 14.25 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 2 |
| `data/reports/DATA_COLLECTION_REPORT.md` | 2.79 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 0 |
| `data/reports/DATA_QUALITY_REPORT.md` | 10.28 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 2 |
| `data/reports/DATA_READINESS_MATRIX.md` | 6.11 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 2 |
| `data/reports/DATA_SOURCE_REGISTER.csv` | 3.11 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 2 |
| `data/reports/EDA_REPORT.md` | 4.75 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 2 |
| `data/reports/ENVIRONMENTAL_DATASET_VERIFICATION.json` | 8.78 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 2 |
| `data/reports/ML_TRAINING_READINESS_REPORT.md` | 11.89 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 0 |
| `data/reports/figures/cyclone_wind_pressure_eda.png` | 389.46 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 0 |
| `data/reports/figures/earthquake_depth_magnitude_eda.png` | 497.75 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 0 |
| `data/reports/figures/flood_severity_and_duration.png` | 113.1 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 0 |
| `data/reports/figures/global_multi_hazard_spatial_distribution.png` | 1707.25 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 0 |
| `data/reports/figures/hazard_record_counts.png` | 97.33 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 0 |
| `data/reports/figures/india_multi_hazard_focus_map.png` | 1738.82 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 0 |
| `data/reports/figures/landslide_triggers_and_categories.png` | 144.58 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 0 |
| `data/reports/figures/wildfire_frp_duration_eda.png` | 133.46 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 0 |
| `data/reports/validation/MODEL_READY_VALIDATION_RESULTS.json` | 2.97 | HISTORICAL | NO | NO | Mirror copy of reports within data directory. | 0 |
| `scripts/audit_and_process_earthquakes.py` | 4.77 | HISTORICAL | NO | NO | Early single-hazard prototype script superseded by modular subdirectories. | 0 |
| `scripts/audit_landslides.py` | 3.19 | HISTORICAL | NO | NO | Early single-hazard prototype script superseded by modular subdirectories. | 0 |
| `scripts/download_all_earthquakes.py` | 5.33 | HISTORICAL | NO | NO | Early single-hazard prototype script superseded by modular subdirectories. | 0 |
| `scripts/download_earthquakes.py` | 3.37 | HISTORICAL | NO | NO | Early single-hazard prototype script superseded by modular subdirectories. | 0 |
| `scripts/eda/cross_source_duplicates.py` | 12.3 | HISTORICAL | NO | NO | Comprehensive exploratory data analysis and duplicate inspection module. | 0 |
| `scripts/eda/dataset_suitability.py` | 13.82 | HISTORICAL | NO | NO | Comprehensive exploratory data analysis and duplicate inspection module. | 0 |
| `scripts/eda/duplicate_analysis.py` | 2.34 | HISTORICAL | NO | NO | Comprehensive exploratory data analysis and duplicate inspection module. | 0 |
| `scripts/eda/generate_master_reports.py` | 45.37 | HISTORICAL | NO | NO | Comprehensive exploratory data analysis and duplicate inspection module. | 0 |
| `scripts/eda/missing_value_analysis.py` | 2.57 | HISTORICAL | NO | NO | Comprehensive exploratory data analysis and duplicate inspection module. | 0 |
| `scripts/eda/outlier_analysis.py` | 3.5 | HISTORICAL | NO | NO | Comprehensive exploratory data analysis and duplicate inspection module. | 0 |
| `scripts/eda/run_full_eda.py` | 12.51 | HISTORICAL | NO | NO | Comprehensive exploratory data analysis and duplicate inspection module. | 0 |
| `scripts/eda/spatial_quality_analysis.py` | 2.48 | HISTORICAL | NO | NO | Comprehensive exploratory data analysis and duplicate inspection module. | 0 |
| `scripts/eda/temporal_quality_analysis.py` | 2.98 | HISTORICAL | NO | NO | Comprehensive exploratory data analysis and duplicate inspection module. | 0 |
| `scripts/process_floods.py` | 3.96 | HISTORICAL | NO | NO | Early single-hazard prototype script superseded by modular subdirectories. | 0 |
| `scripts/process_landslides.py` | 3.8 | HISTORICAL | NO | NO | Early single-hazard prototype script superseded by modular subdirectories. | 0 |
| `DATASET_INTEGRATION_REPORT.md` | 4.07 | REDUNDANT | NO | NO | Outdated duplicate of canonical report located in reports/. | 2 |
| `DATASET_INVENTORY.md` | 5.9 | REDUNDANT | NO | NO | Outdated duplicate of canonical report located in reports/. | 2 |
| `DATASET_METADATA.json` | 2.37 | REDUNDANT | NO | NO | Outdated duplicate of canonical report located in reports/. | 2 |
| `DATASET_REPORT.md` | 18.09 | REDUNDANT | NO | NO | Outdated duplicate of canonical report located in reports/. | 0 |
| `DATASET_SUITABILITY_REPORT.md` | 11.46 | REDUNDANT | NO | NO | Outdated duplicate of canonical report located in reports/. | 2 |
| `DATA_COLLECTION_REPORT.md` | 2.79 | REDUNDANT | NO | NO | Outdated duplicate of canonical report located in reports/. | 0 |
| `DATA_QUALITY_REPORT.md` | 3.69 | REDUNDANT | NO | NO | Outdated duplicate of canonical report located in reports/. | 2 |
| `DATA_READINESS_MATRIX.md` | 5.09 | REDUNDANT | NO | NO | Outdated duplicate of canonical report located in reports/. | 2 |
| `DATA_SOURCE_REGISTER.csv` | 2.5 | REDUNDANT | NO | NO | Outdated duplicate of canonical report located in reports/. | 2 |
| `EDA_REPORT.md` | 3.43 | REDUNDANT | NO | NO | Outdated duplicate of canonical report located in reports/. | 2 |
| `scripts/__pycache__/download_earthquakes.cpython-311.pyc` | 4.6 | TEMPORARY | NO | NO | Compiled Python bytecode cache. | 0 |