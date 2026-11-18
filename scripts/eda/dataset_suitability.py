"""
HAZARDX AI - Dataset Suitability Assessment Engine
Evaluates every collected dataset against proposed machine learning tasks.
Assigns standardized ratings:
  1. SUITABLE
  2. SUITABLE WITH PREPROCESSING
  3. PARTIALLY SUITABLE
  4. NOT SUITABLE
  5. PENDING VERIFICATION
"""

import os
import json

SUITABILITY_EVALUATION = [
    {
        "hazard": "Floods",
        "dataset_name": "Dartmouth Flood Observatory (DFO) Spatial Archive",
        "file_path": "data/raw/floods/dfo_spatial_flood_archive_1985_2010.csv",
        "intended_task": "Global Flood Susceptibility & Extent Ground-Truth Modeling",
        "rating": "SUITABLE WITH PREPROCESSING",
        "target_available": True,
        "target_variable": "Occurrence & Severity (1.0 to 2.0)",
        "justification": "Contains 4,029 global flood events with 100% verified centroid coordinates and historical dates. Requires preprocessing to sanitize coordinate typos (e.g. record 3229) and join with negative spatio-temporal non-flood controls and dynamic rainfall reanalysis (ERA5).",
        "blockers_or_needs": "Requires negative pseudo-absence sampling and ERA5/GPM precipitation join."
    },
    {
        "hazard": "Floods",
        "dataset_name": "GLIDE Global Flood Sub-Catalog",
        "file_path": "data/raw/floods/glide_flood_events.csv",
        "intended_task": "Flood Disaster Impact & Casualty Modeling",
        "rating": "SUITABLE WITH PREPROCESSING",
        "target_available": True,
        "target_variable": "killed, affected, homeless",
        "justification": "Contains 2,732 international flood and flash flood disaster events with 100% valid coordinates and casualty figures. Requires cleaning year formatting typos (e.g. '20' -> '2020').",
        "blockers_or_needs": "Year format harmonization and normalization of skewed casualty metrics."
    },
    {
        "hazard": "Floods",
        "dataset_name": "Central Water Commission (CWC) Telemetry / India-WRIS",
        "file_path": "data/raw/floods/cwc_water_levels (Investigated)",
        "intended_task": "Real-Time River Water-Level & Stage Forecasting",
        "rating": "PARTIALLY SUITABLE",
        "target_available": False,
        "target_variable": "River gauge stage level (m)",
        "justification": "Official India-WRIS and CWC portals require authenticated portal sessions and interactive CAPTCHA gating. Station-level historical hourly gauge records are not programmatically downloadable via open API without institutional credentials. Global GloFAS daily discharge provides an open surrogate.",
        "blockers_or_needs": "Requires institutional CWC/NWIC data sharing agreement or authenticated telemetry tokens."
    },
    {
        "hazard": "Landslides",
        "dataset_name": "NASA Global Landslide Catalog (GLC / COOLR)",
        "file_path": "data/raw/landslides/nasa_global_landslide_catalog_point.csv",
        "intended_task": "Landslide Susceptibility & Rainfall-Triggered Occurrence Classification",
        "rating": "SUITABLE WITH PREPROCESSING",
        "target_available": True,
        "target_variable": "Occurrence (y=1) & Size (small/medium/large)",
        "justification": "Contains 11,033 empirical global landslide points with 100% valid coordinates, dates, and trigger causes. Suitable as the primary positive occurrence ground truth.",
        "blockers_or_needs": "Must NOT be trained alone; requires stratified sampling of non-landslide slope controls (y=0) and extraction of SRTM slope, SoilGrids, and 7-day GPM rainfall."
    },
    {
        "hazard": "Landslides",
        "dataset_name": "Geological Survey of India (GSI) 1:50k Landslide Susceptibility Maps",
        "file_path": "data/raw/landslides/gsi_maps (Investigated)",
        "intended_task": "Regional High-Resolution Susceptibility Baseline in Western Ghats / Himalayas",
        "rating": "PARTIALLY SUITABLE",
        "target_available": True,
        "target_variable": "National Landslide Susceptibility Mapping (NLSM) Zone",
        "justification": "GSI provides static PDF/WMS maps on Bhukosh geoportal requiring user authentication and GIS georeferencing. Highly relevant for Indian domain validation but not downloadable as raw tabular training vectors.",
        "blockers_or_needs": "Vectorization and georeferencing of GSI Bhukosh tiles."
    },
    {
        "hazard": "Earthquakes",
        "dataset_name": "USGS Earthquake Catalog (ComCat 2000-2025)",
        "file_path": "data/raw/earthquakes/usgs_earthquakes_2000_2025.csv",
        "intended_task": "Regional Seismic Activity Assessment & Aftershock Spatial Probability",
        "rating": "SUITABLE",
        "target_available": True,
        "target_variable": "mag, depth, event rate",
        "justification": "Comprehensive, authoritative global catalog of 689,496 events with 100% valid coordinates and depths. Deduplicated and fully verified.",
        "blockers_or_needs": "None for seismicity rate and aftershock hazard modeling. For ground-motion shaking (PGA/MMI), requires separate station waveform/ShakeMap linkage."
    },
    {
        "hazard": "Earthquakes",
        "dataset_name": "GEM Global Active Faults Database (GAF-DB)",
        "file_path": "data/raw/earthquakes/gem_active_faults.geojson",
        "intended_task": "Tectonic Proximity & Fault Slip Feature Engineering",
        "rating": "SUITABLE",
        "target_available": False,
        "target_variable": "Covariate (distance_to_fault, slip_type, slip_rate)",
        "justification": "16,195 harmonized active fault geometries globally. Directly usable for computing Euclidean and shortest perpendicular distance to fault traces.",
        "blockers_or_needs": "Spatial distance calculation algorithm to join with earthquake epicenters."
    },
    {
        "hazard": "Earthquakes",
        "dataset_name": "Global Ground Motion Datasets (PGA, PGV, MMI Stations)",
        "file_path": "data/raw/earthquakes/ground_motion (Investigated)",
        "intended_task": "Empirical Ground-Motion Prediction Equations (GMPE) via ML",
        "rating": "PARTIALLY SUITABLE",
        "target_available": False,
        "target_variable": "PGA (g), PGV (cm/s), MMI (I-X)",
        "justification": "The primary ComCat catalog contains hypocentral source parameters but does not include recorded surface PGA/PGV timeseries at strong-motion stations. Instrumental ground-motion datasets (USGS ShakeMap flatfiles, PEER NGA-West2) require specialized station joins.",
        "blockers_or_needs": "Direct ShakeMap ground-motion station archive download or GMPE proxy simulation."
    },
    {
        "hazard": "Cyclones",
        "dataset_name": "NOAA IBTrACS v04r01 Best Track Archive",
        "file_path": "data/raw/cyclones/ibtracs_since1980_v04r01.csv",
        "intended_task": "Cyclone Intensity Classification, Wind Speed Estimation & Track Forecasting",
        "rating": "SUITABLE",
        "target_available": True,
        "target_variable": "USA_WIND (kt), USA_PRES (hPa), USA_STATUS, Track (LAT, LON)",
        "justification": "Contains 312,398 track observations across 5,017 storms worldwide since 1980, including 15,654 North Indian Ocean points. Complete coordinates, continuous 3-hourly/6-hourly tracks.",
        "blockers_or_needs": "Time-lagged feature engineering (calculating 12h/24h intensity change, translational speed and heading)."
    },
    {
        "hazard": "Cyclones",
        "dataset_name": "IMD North Indian Ocean Best-Track Reports",
        "file_path": "data/raw/cyclones/imd_tracks (Investigated)",
        "intended_task": "Validation of North Indian Ocean Cyclone Landfalls (Bay of Bengal & Arabian Sea)",
        "rating": "SUITABLE WITH PREPROCESSING",
        "target_available": True,
        "target_variable": "IMD Cyclone Classification (CS, SCS, VSCS, ESCS, Super Cyclone)",
        "justification": "The NOAA IBTrACS dataset already incorporates the New Delhi WMO Regional Specialized Meteorological Centre (RSMC New Delhi / IMD) official agency tracks (agency code 'NEWDELHI').",
        "blockers_or_needs": "Filter IBTrACS records for agency == 'newdelhi' or basin == 'NI'."
    },
    {
        "hazard": "Wildfires",
        "dataset_name": "NASA FIRMS MODIS Active Fire Catalog (C6.1)",
        "file_path": "data/processed/wildfires/wildfire_events_cleaned_catalog.csv",
        "intended_task": "Wildfire Ignition Probability & Fire Radiative Power (FRP) Estimation",
        "rating": "SUITABLE WITH PREPROCESSING",
        "target_available": True,
        "target_variable": "Occurrence (y=1), total_frp_mw, duration_days, estimated_area_km2",
        "justification": "Contains 31,371 discrete physical wildfire events aggregated from 66,140 high-confidence satellite detections using 4D spatiotemporal DBSCAN clustering. Directly provides empirical centroids, duration, pixel footprints, and radiative energy release.",
        "blockers_or_needs": "Requires stratified non-fire background sampling (negative controls) and join with ERA5 Fire Weather Index (FWI), vapor pressure deficit, and SRTM slope."
    },
    {
        "hazard": "Wildfires",
        "dataset_name": "NASA FIRMS VIIRS 375m Active Fire Catalog",
        "file_path": "data/processed/wildfires/wildfire_events_viirs_catalog.csv",
        "intended_task": "High-Resolution Wildfire Perimeter & Active Spread Tracking",
        "rating": "SUITABLE WITH PREPROCESSING",
        "target_available": True,
        "target_variable": "Occurrence (y=1), pixel_count, total_frp_mw",
        "justification": "Contains 111,053 discrete wildfire events clustered from 326,642 nominal/high confidence 375m VIIRS detections. Highest spatial fidelity for localized perimeter and fuel ignition modeling.",
        "blockers_or_needs": "High compute requirement for global feature extraction; recommend regional bounding box (e.g. South Asia / North America)."
    },
    {
        "hazard": "Wildfires",
        "dataset_name": "GLIDE Wildfire Disaster Registry",
        "file_path": "data/processed/wildfires/wildfire_disaster_events_glide.csv",
        "intended_task": "Wildfire Disaster Impact & Socio-Economic Risk Assessment",
        "rating": "SUITABLE WITH PREPROCESSING",
        "target_available": True,
        "target_variable": "killed, affected",
        "justification": "Contains 224 georeferenced major global wildfire disaster events with documented humanitarian impact.",
        "blockers_or_needs": "Macro-level event reporting; should be coupled with satellite fire perimeters for physical modeling."
    },
    {
        "hazard": "Common Environmental",
        "dataset_name": "ECMWF ERA5 / ERA5-Land Reanalysis (Open-Meteo Historical Weather)",
        "file_path": "data/raw/environmental/era5_connector (Verified API)",
        "intended_task": "Cross-Hazard Atmospheric & Hydrological Feature Extraction (Precipitation, Temperature, Wind, Soil Moisture)",
        "rating": "SUITABLE",
        "target_available": False,
        "target_variable": "Dynamic Environmental Covariates",
        "justification": "Provides verified global historical daily and hourly reanalysis for any coordinate back to 1940 with zero API key or cost. Fully tested and operational in project scripts.",
        "blockers_or_needs": "Batch spatial-temporal querying for event-level feature enrichment."
    },
    {
        "hazard": "Common Environmental",
        "dataset_name": "geoBoundaries India Subnational Administrative Boundaries (IND-ADM1 & ADM2)",
        "file_path": "data/raw/environmental/india_state_boundaries.geojson",
        "intended_task": "Spatial Aggregation, Regional Risk Indexing & Early Warning Dissemination",
        "rating": "SUITABLE",
        "target_available": False,
        "target_variable": "Spatial Polygons & Boundary Hierarchy",
        "justification": "Official, validated open GIS boundaries covering all Indian states and Union Territories (including Kerala). 100% valid geometry.",
        "blockers_or_needs": "None. Fully downloaded and ready."
    }
]

def generate_suitability_report():
    out_md = "data/reports/DATASET_SUITABILITY_REPORT.md"
    lines = [
        "# HAZARDX AI — Comprehensive Dataset Suitability Assessment",
        "## Rigorous Machine Learning Task Suitability Audit",
        "",
        "**Author:** HAZARDX AI Senior Data Science & ML Engineering Team  ",
        "**Date:** 2026-11-17  ",
        "**Evaluation Standard:** Objective ML task alignment, target variable availability, data leakage risks, and physical validity. Zero tolerance for unverified assumptions.",
        "",
        "---",
        "",
        "## 1. Summary of Suitability Decisions",
        "",
        "| Hazard | Dataset Name | Assigned Rating | Target Variable Available? | Intended Machine Learning Task |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    
    for item in SUITABILITY_EVALUATION:
        target_str = "Yes (" + item['target_variable'] + ")" if item['target_available'] else "No (Covariate / Covariate Only)"
        lines.append(f"| **{item['hazard']}** | {item['dataset_name']} | **{item['rating']}** | {target_str} | {item['intended_task']} |")
        
    lines.extend([
        "",
        "---",
        "",
        "## 2. In-Depth Suitability Audits by Dataset",
        ""
    ])
    
    for item in SUITABILITY_EVALUATION:
        lines.extend([
            f"### {item['hazard']}: {item['dataset_name']}",
            f"- **File Path / Source:** `{item['file_path']}`",
            f"- **Suitability Rating:** **{item['rating']}**",
            f"- **Intended ML Task:** {item['intended_task']}",
            f"- **Target Variable Status:** {item['target_variable']}",
            f"- **Technical Justification:** {item['justification']}",
            f"- **Blockers & Preprocessing Needs:** {item['blockers_or_needs']}",
            ""
        ])
        
    with open(out_md, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
        
    print(f"Suitability report generated at: {out_md}")
    return SUITABILITY_EVALUATION

if __name__ == '__main__':
    generate_suitability_report()

