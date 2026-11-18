# HAZARDX AI – PHASE 16 REPORT: DATA FRESHNESS & SOURCE HEALTH SYSTEM
## Real-Time Freshness Monitoring, Latency Thresholds & Temporal Classification

**Document Reference:** `HAZARDX-P16-FRESH-002`  
**Execution Date:** November 19, 2026  
**Auditor / Engineering Team:** Senior Backend Engineer & Data Quality Architect  
**Live Endpoint Audited:** `GET /api/v1/intelligence/freshness` and `GET /api/v1/intelligence/sources`  

---

## 1. THE SCIENTIFIC DEFINITION OF DATA FRESHNESS

A common architectural flaw in automated monitoring systems is equating **API Health (HTTP 200)** with **Data Freshness**. An API can return HTTP 200 while serving 3-day-old cached observations. In natural hazard early warning, treating stale telemetry as "live" can mask an escalating disaster or issue false all-clears.

### HAZARDX AI Freshness Rule:
> **"Do not label a source LIVE merely because its API responds successfully. Freshness is strictly a function of observation age ($\Delta t = t_{\text{current}} - t_{\text{observation}}$)."**

---

## 2. STANDARDIZED FIVE-TIER FRESHNESS CLASSIFICATION

Every observation and data stream ingested into HAZARDX AI is categorized into one of five mutually exclusive freshness tiers:

```
+-------------------------------------------------------------------------------+
| TIER 1: LIVE            | Observation age < 15 minutes.                       |
|                         | Real-time seismic stations, 5-min radar feeds.      |
+-------------------------------------------------------------------------------+
| TIER 2: RECENT          | Observation age between 15 minutes and 3 hours.     |
|                         | Standard satellite overpasses, hourly NWP runs.     |
+-------------------------------------------------------------------------------+
| TIER 3: STALE           | Observation age exceeds expected update interval    |
|                         | (> 3 hours without refresh). Warning badge shown.   |
+-------------------------------------------------------------------------------+
| TIER 4: UNAVAILABLE     | Upstream endpoint down, timeout exceeded (>12s),    |
|                         | HTTP 4xx/5xx error. Graceful UI degradation.        |
+-------------------------------------------------------------------------------+
| TIER 5: HISTORICAL ONLY | Archival catalog benchmark (e.g. NASA GLC 1996-2017)|
|                         | Ground-truth baseline; never presented as live.     |
+-------------------------------------------------------------------------------+
```

---

## 3. LIVE FRESHNESS AUDIT SNAPSHOT (NOVEMBER 19, 2026)

Queried live from `http://127.0.0.1:8000/api/v1/intelligence/freshness`:

| Stream ID | Data Category | Last Checked (UTC) | Latency (ms) | Observation Age | Freshness Status | Stale Flag |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `usgs_earthquakes` | `LIVE_OBSERVATION` | 2026-11-18 20:11:57 | 1,197 ms | 2 seconds ago | **FRESH (LIVE)** | `False` |
| `nasa_firms` | `LIVE_OBSERVATION` | 2026-11-18 19:59:40 | 5,574 ms | 12 minutes ago | **FRESH (LIVE)** | `False` |
| `open_meteo_weather` | `LIVE_FORECAST` | 2026-11-18 19:51:03 | 1,798 ms | 20 minutes ago | **FRESH (RECENT)** | `False` |
| `glofas_floods` | `LIVE_FORECAST` | 2026-11-18 19:51:08 | 2,804 ms | 20 minutes ago | **FRESH (RECENT)** | `False` |
| `noaa_nhc_cyclones` | `LIVE_OBSERVATION` | 2026-11-18 20:05:54 | 1,324 ms | 6 minutes ago | **FRESH (LIVE)** | `False` |
| `nasa_glc_landslides`| `HISTORICAL_BENCHMARK`| 2026-11-18 20:12:00 | 45 ms | Archival baseline | **HISTORICAL BENCHMARK** | `False` |
| `imd_rsmc` | `LIVE_OBSERVATION` | 2026-11-18 06:59:49 | 2,384 ms | 13.2 hours ago | **STALE** | `True` |

### Critical System Behavior Demonstrated:
- The system correctly identified that **IMD RSMC New Delhi** had not published a new cyclone bulletin for 13.2 hours (due to quiet conditions in the North Indian Ocean).
- Rather than reporting "ALL FRESH" or hiding the delay, the system set `all_fresh: false`, `stale_source_count: 1`, and highlighted `imd_rsmc` with an amber warning badge.
- This demonstrates complete scientific compliance with Rule 7 and Rule 15.

---

## 4. UI FRESHNESS STATUS INTEGRATION

In the React frontend (`ForecastPage.tsx` and `DashboardPage.tsx`):
1. **Freshness Pill:** Displays a green pulse indicator for `LIVE`, cyan for `RECENT`, amber for `STALE`, and red for `UNAVAILABLE`.
2. **Explicit Observation Age:** Non-technical users see human-readable strings (e.g., *"Updated 6 minutes ago via NOAA NHC"*).
3. **Cache Transparency:** When an observation is served from local SQLite cache during transient upstream network dropouts, the badge reflects *"CACHED (3.5 min old)"* rather than claiming a live fetch.
