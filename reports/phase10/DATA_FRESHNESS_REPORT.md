# HAZARDX AI — Real-Time Data Freshness & Ingestion Telemetry Report
**Phase 10: Multi-Hazard Forecasting & Live Data Integration**
**Date:** November 18, 2026
**System Status:** OPERATIONAL

---

## 1. Executive Summary

This report establishes the data freshness policies, latency benchmarks, and cache expiration standards across all real-time atmospheric, hydrological, geotechnical, and oceanic data feeds powering the **HAZARDX AI Multi-Hazard Forecasting Platform**.

To ensure scientific defensibility, every incoming data observation is assigned a deterministic **Freshness State** (`FRESH`, `ACCEPTABLE`, `STALE`, `UNAVAILABLE`) and an explicit **Data Provenance Tag** (`LIVE_OBSERVATION`, `LIVE_FORECAST`, `CACHED_OBSERVATION`, `CACHED_FORECAST`, `HISTORICAL_BENCHMARK`, `MODEL_INFERENCE`).

---

## 2. Ingestion & Freshness Matrix by Authoritative Source

| Source Identifier | Authoritative Agency | Data Type & Physical Coverage | Expected Update Cadence | `FRESH` Threshold | `ACCEPTABLE` Threshold | `STALE` Threshold | Fallback Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `usgs_earthquakes` | USGS Earthquake Hazards Program | Global seismicity (M2.5+), hypocenters, focal depths | Real-time / 5 min | $\le 15$ min | $\le 1$ hour | $> 2$ hours | SQLite ComCat cache |
| `nasa_firms` | NASA FIRMS (MODIS C6.1 / VIIRS) | Global thermal hotspots, FRP (MW), brightness (K) | 1 to 3 hours | $\le 2$ hours | $\le 6$ hours | $> 12$ hours | SQLite active fire cache |
| `open_meteo_weather` | Open-Meteo Global NWP (ECMWF / GFS) | 96h hourly NWP: rain, temp, wind, soil moisture, FWI | 1 hour | $\le 3$ hours | $\le 6$ hours | $> 12$ hours | SQLite gridded cache |
| `glofas_floods` | Copernicus / GloFAS Hydrology | 7-day river discharge ($m^3/s$), 7d running mean | 6 to 12 hours | $\le 12$ hours | $\le 24$ hours | $> 48$ hours | Persistent basin reach cache |
| `noaa_nhc_cyclones` | NOAA NHC & IBTrACS | Active tropical systems, sustained wind, pressure | 3 to 6 hours | $\le 6$ hours | $\le 12$ hours | $> 24$ hours | IBTrACS historical benchmark |
| `nasa_glc_landslides`| NASA Goddard Space Flight Center | Global Landslide Catalog (GLC) susceptibility | Historical | Catalog (N/A) | Catalog (N/A) | Catalog (N/A) | NASA GLC Inventory |
| `imd_cyclones` | India Meteorological Dept (RSMC New Delhi) | North Indian Ocean cyclone bulletins, track & cone | 3 to 6 hours | $\le 6$ hours | $\le 12$ hours | $> 24$ hours | Regional RSMC cache |

---

## 3. Freshness State Machine

```
  Observation Ingested
         │
         ▼
   Age <= Threshold_Fresh ?  ─── YES ───► [ FRESH ] (Live streaming operations)
         │
        NO
         ▼
   Age <= Threshold_Stale ?  ─── YES ───► [ ACCEPTABLE ] (Recent valid context)
         │
        NO
         ▼
   Network Connection OK?    ─── YES ───► [ STALE ] (Trigger background refresh)
         │
        NO
         ▼
  [ UNAVAILABLE ] (Engage persistent SQLite benchmark fallback + issue provenance alert)
```

---

## 4. Background Ingestion Scheduler Telemetry

- **Engine:** `backend/app/ingestion/scheduler.py`
- **Cadence:** Configurable periodic polling loop (Default: 300 seconds / 5 minutes).
- **Concurrency Protection:** `asyncio.Lock()` prevents overlapping cycles during network latency spikes.
- **Circuit Breakers:** Exponential backoff with jitter on HTTP 429/5xx responses; max retry count = 3.
- **Physical Boundary Validation:** Managed by `data_validator.py` (e.g. Rejecting wind > 250 kt, relative humidity < 0% or > 100%, negative rainfall).

---

## 5. Provenance Labeling & Operational Transparency

1. **Active Earthquakes:** Labeled `LIVE_OBSERVATION` when timestamp $< 60$ minutes; aftershock trajectories are labeled `MODEL_INFERENCE` (Omori-Utsu statistical decay).
2. **Wildfire Detections:** Labeled `LIVE_OBSERVATION` from FIRMS; strictly disclosed as **existing thermal anomalies**, while 24h–72h forward ignition susceptibility is labeled `LIVE_FORECAST`.
3. **Flood Forecasting:** River discharge projections derived from GloFAS simulations labeled `LIVE_FORECAST` with the explicit note that they reflect gridded hydrological models, not in-situ stage gauges.
4. **Cyclone Forecasting:** When active storms are present in NOAA NHC / IMD bulletins, labeled `LIVE_FORECAST`; during calm off-season basins, benchmark historical systems (e.g., Cyclone Biparjoy, Hurricane Ian) are clearly tagged `HISTORICAL_BENCHMARK`.

---

**Approved by:**
HAZARDX AI Chief Data Engineer & Operational Science Lead

