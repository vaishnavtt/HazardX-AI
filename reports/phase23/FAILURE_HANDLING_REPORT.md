# HAZARDX AI — Degraded Failure Mode & Graceful Handling Report (Phase 23)
**Document ID:** `HAZARDX-P23-FHR-005`  
**Evaluation Standard:** Fault Tolerance Under Upstream Failure & Network Partition Scenarios  
**Audit Date:** 2026-11-19  
**Status:** VALIDATED & COMPLIANT  

---

## 1. Executive Summary

Disaster intelligence platforms must operate reliably even when upstream infrastructure fails. In major disaster events, telecommunication lines may be severed, upstream meteorological APIs may experience traffic overloads, or satellite downlink ground stations may experience maintenance delays.

A primary principle of HAZARDX AI is: **Never replace real missing information with synthetic or fabricated data to hide errors.** Instead, the system must gracefully degrade, clearly communicate data provenance and staleness, and preserve all remaining operational capabilities.

---

## 2. Degraded Scenario Stress Testing

| Failure Scenario Tested | System Reaction | User-Facing Behavior | Integrity Assessment |
|---|---|---|---|
| **Single External API Outage (e.g. USGS Down)** | `BaseResilientClient` executes 3 retries with backoff; serves cached observation from SQLite if available. | Earthquake layer shows `CACHED` or `STALE` badge. Other 4 hazard domains continue real-time updates. | **PASS — No Cascading Failure** |
| **Multiple Upstream APIs Down (e.g. Open-Meteo & FIRMS)** | Timeouts trigger gracefully after 8s; database logs failures to `api_logs`. | UI displays warning banner: *"Live satellite feeds delayed. Displaying latest verified telemetry."* | **PASS — Zero Fabricated Data** |
| **Missing Model Binary on Disk** | `ModelRegistry` logs warning on boot; marks missing model as `UNAVAILABLE` in `MODEL_STATUS`. | Specific endpoint returns HTTP 404 with descriptive message; other 11 models operate normally. | **PASS — Independent Isolation** |
| **Database Lock Contention** | SQLite WAL mode permits concurrent reads; 10s busy timeout queues write transactions. | Queries execute without `sqlite3.OperationalError: database is locked`. | **PASS — High Concurrency** |
| **Complete Network Disconnection** | Axios client catches offline error; triggers component error boundary. | `<ErrorState />` renders with informative message: *"Connection lost. Check internet access and retry."* | **PASS — No White-Screen Crash** |

---

## 3. The Anti-Fabrication Invariant Under Degradation

> [!CAUTION]
> **Zero-Fabrication Operational Directive**
> 
> Under no circumstances does HAZARDX AI invent mock sensor readings, fake active fires, or synthetic river discharges when an external API is offline:
> 1. If live data is absent, the system explicitly returns `null` or a cached record with an unambiguous `CACHED_OBSERVATION` provenance stamp.
> 2. The frontend displays the exact time elapsed since the last genuine observation (e.g., `STALE (13.2h)`).
> 3. This transparency guarantees that civil defense analysts are never misled by synthetic "dummy" data during real emergency operations.

---

## 4. Failure Handling Conclusion

The HAZARDX AI platform degrades gracefully, isolates component failures, and maintains absolute transparency during upstream outages.

**Failure Handling Status: VERIFIED & COMPLIANT (PASS)**
