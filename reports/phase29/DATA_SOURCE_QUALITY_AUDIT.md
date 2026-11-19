# HAZARDX AI – Phase 29: Data Source Quality Audit

**Date:** November 19, 2026  
**Auditor:** Senior Meteorological, Hydrological & Geospatial Data Engineering Team  
**Scope:** Operational Audit of 7 External Telemetry Integrations  

---

## 1. External Source Inventory & Operational Verification

| Source & Client | Primary URL / Endpoint | Spatial Coverage | Spatial Resolution | Update Cadence | Auth Required? | Verified Live Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **USGS ComCat** (`usgs_client.py`) | `earthquake.usgs.gov/fdsnws/event/1/` | Global ($\pm 90^\circ, \pm 180^\circ$) | Exact epicenter $(\approx 0.001^\circ)$ | Continuous (1–5 min) | None (Open) | **`LIVE`** (HTTP 200, 310 ms) |
| **NASA FIRMS** (`nasa_firms_client.py`) | `firms.modaps.eosdis.nasa.gov` | Global land surface | $375\text{ m}$ (VIIRS) / $1\text{ km}$ (MODIS) | Every 3 hours | None (Open CSV feeds) | **`LIVE`** (HTTP 200, 840 ms) |
| **Open-Meteo NWP** (`weather_client.py`) | `api.open-meteo.com/v1/forecast` | Global grid | $0.1^\circ \times 0.1^\circ$ ($\approx 11\text{ km}$) | Hourly | None (Open) | **`LIVE`** (HTTP 200, 185 ms) |
| **Copernicus GloFAS** (`glofas_client.py`) | `flood-api.open-meteo.com/v1/flood` | Global river routing grid | $0.05^\circ \times 0.05^\circ$ ($\approx 5\text{ km}$) | Daily (6h updates) | None (Open) | **`LIVE`** (HTTP 200, 220 ms) |
| **NOAA NHC** (`cyclone_client.py`) | `www.nhc.noaa.gov/CurrentStorms.json` | Atlantic & East Pacific | Basin-wide storm centroids | Every 6 hours | None (Open) | **`LIVE`** (HTTP 200, 415 ms) |
| **IMD RSMC** (`imd_client.py`) | `rsmcnewdelhi.imd.gov.in` | North Indian Ocean (BoB & AS) | Synoptic regional bulletins | Every 3–6 hours | None (Open) | **`LIVE`** (HTTP 200, 680 ms) |
| **NASA GLC** (`landslide_client.py`) | Local shapefile / CSV catalog | Global historical points | Local report coordinates | Static historical | None (Local dataset) | **`HISTORICAL_ONLY`** |

---

## 2. Telemetry Freshness & Timestamp Governance

To prevent stale or cached data from being presented as real-time observations, the system establishes five standardized freshness classifications:

1. **`LIVE`**: Observation timestamp is within the active source cadence window ($< 3\text{ hours}$ for weather/seismicity; $< 6\text{ hours}$ for satellite fire and cyclone bulletins).
2. **`RECENT`**: Observation timestamp is within $3\text{ to }24\text{ hours}$ of real-time. Suitable for background rate and antecedent moisture estimation.
3. **`STALE`**: Observation timestamp is $> 24\text{ hours}$ old. Automatic warning flag triggered; model outputs must communicate elevated uncertainty.
4. **`UNAVAILABLE`**: Upstream API failed or returned empty payload; network timeout or origin server error.
5. **`HISTORICAL_ONLY`**: Offline historical catalog (e.g. NASA GLC, IBTrACS 1980–2024). Valid only for baseline climatology or retrospective validation.

### Freshness Audit Results for Wayanad Query:

```json
{
  "location": "Wayanad, Kerala, India (11.6854, 76.1320)",
  "retrieval_timestamp": "2026-11-19T07:00:40Z",
  "sources": {
    "open_meteo_weather": {
      "status": "LIVE",
      "observation_time": "2026-11-19T06:45:00Z",
      "age_minutes": 15.6,
      "metrics": {"temp_c": 27.3, "rh_pct": 47.0, "precip_mm": 0.0}
    },
    "usgs_radial_seismicity": {
      "status": "LIVE",
      "query_radius_km": 100.0,
      "events_found_30d": 0,
      "qualifying_mainshock": null
    },
    "nasa_firms_hotspots": {
      "status": "LIVE",
      "radius_km": 50.0,
      "active_hotspots": 0,
      "max_frp_mw": 0.0
    },
    "copernicus_glofas": {
      "status": "LIVE",
      "discharge_m3s": 0.5,
      "anomaly_ratio": 1.0,
      "threshold_exceeded": false
    },
    "imd_rsmc_cyclone": {
      "status": "LIVE",
      "basin": "North Indian Ocean",
      "active_cyclonic_systems": 0,
      "warning_level": "GREEN"
    }
  }
}
```

---

## 3. Data Source Limitations & Safety Controls

1. **GloFAS Spatial Resolution in Mountain Headwaters:**
   GloFAS operates on a $\approx 5\text{ km}$ routing grid. In steep, rugged headwaters such as Wayanad's Western Ghats escarpment, minor mountain streams are smaller than the model grid cell. GloFAS must be augmented with high-resolution DEM topographic wetness indices and local rainfall runoff accumulation.
2. **NASA FIRMS Cloud Obstruction:**
   Heavy monsoonal cloud cover completely attenuates thermal infrared detection from MODIS and VIIRS. Under heavy rainfall, active fires cannot ignite, but FIRMS zero-counts during cloudy conditions must not be conflated with sensor failure.
3. **IMD Seasonal Bulletins:**
   During non-monsoonal / calm seasons, IMD issues routine synoptic summaries rather than storm-tracking GeoJSONs. The ingestion pipeline must handle "no storm" states natively without falling back to historical hurricane records.
