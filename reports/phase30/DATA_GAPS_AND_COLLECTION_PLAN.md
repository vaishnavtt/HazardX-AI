# HAZARDX AI – Phase 30: Data Gaps and Collection Plan

**Date:** November 19, 2026  
**Auditor:** Data Acquisition & MLOps Infrastructure Team  
**Scope:** Actionable Data Collection Roadmap & Gap Remediation  

---

## 1. Identified Data Gaps

| Hazard Domain | Primary Data Gap | Technical Impact | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **Wildfires** | Severe absence of tropical/monsoonal fire and non-fire samples ($0.5\%$ Indian data). | Model falsely labels ambient tropical temperatures ($26–30^\circ\text{C}$) as extreme fire danger. | Augment dataset with 2,000 authentic tropical fire detections from NASA FIRMS VIIRS (South Asia, Indochina, Brazil) paired with genuine ERA5 reanalysis weather. |
| **Wildfires** | Live point assessment does not query localized FIRMS satellite hotspots. | Predictions rely entirely on weather heuristics without verifying whether fires are actually burning. | Integrate localized circular radial query in `nasa_firms_client.py` ($50\text{ km}$ radius). |
| **Earthquakes** | Lack of explicit seismic hazard zone mapping for stable continental cratons. | System default injected an $M 6.0$ event for quiet regions. | Integrate USGS Global Dynamic Fault Catalog and GSHAP Global Seismic Hazard Map to classify cratonic baselines. |
| **Cyclones** | Lack of geographic proximity gating for inland locations. | Evaluated mountain coordinates as having offshore tropical cyclones. | Implement topological spatial clipping: if distance to coastline $> 150\text{ km}$, bypass cyclone intensification modeling. |
| **Floods & Landslides** | Static soil clay and road distance heuristics used globally. | Local geotechnical variations are flattened to constants ($28.5\%$ clay, $0.45\text{ km}$ to road). | Ingest OpenStreetMap highways and ISRIC SoilGrids 250m clay fractions for exact point coordinates. |

---

## 2. Authoritative Data Acquisition Sources

1. **NASA FIRMS Archive:**
   - Source: NASA Earthdata EOSDIS.
   - License: Open access / Public domain (US Government work).
   - Elements: 10-year global VIIRS 375m active fire detections (2014–2024), brightness temperature, FRP (MW), and acquisition confidence.
2. **Copernicus Climate Change Service (C3S) ERA5-Land:**
   - Source: ECMWF Climate Data Store.
   - License: Open access (Copernicus License).
   - Elements: 2m temperature, 2m dewpoint, 10m wind speed, surface pressure, total precipitation, volumetric soil water (layers 1–4).
3. **Open-Meteo Historical & Forecast APIs:**
   - Source: Open-Meteo.com.
   - License: Non-commercial open access / Attribution (CC-BY 4.0).
   - Elements: Multi-day hourly weather archives, ECMWF IFS 0.1° and GFS 0.25° NWP forecasts.

---

## 3. Data Collection & Preprocessing Pipeline

```text
[NASA FIRMS Global Fire Archive] + [Copernicus GloFAS Historical]
                         │
                         ▼
             [Harmonized Spatial Indexing]
       (Match exact lat, lon, and event timestamp)
                         │
                         ▼
        [Authentic ERA5-Land Environmental Pull]
   (Retrieve true antecedent rain, humidity, soil moisture)
                         │
                         ▼
            [Standardized Canadian FWI Engine]
     (Compute true FFMC, DMC, DC, ISI, BUI, and FWI)
                         │
                         ▼
       [Balanced Multi-Biome Training Matrix]
 (Include Boreal, Temperate, Mediterranean, and Tropical)
```

---

## 4. Compliance and Redistribution Rules

- No copyrighted, proprietary, or subscription-locked datasets may be bundled in the repository.
- Raw multi-gigabyte external archives must be downloaded on demand using reproducible python scripts in `scripts/data_collection/`.
- Training matrices in `data/model_ready/` must remain below GitHub's 50 MB threshold per file.
