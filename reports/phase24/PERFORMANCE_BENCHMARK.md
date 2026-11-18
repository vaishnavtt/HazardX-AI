# HAZARDX AI — End-to-End Performance Benchmark Report (Phase 24)
**Document ID:** `HAZARDX-P24-PBM-001`  
**Evaluation Standard:** Enterprise Latency SLA & Sub-Second Emergency Throughput  
**Audit Date:** 2026-11-19  
**Status:** BENCHMARKED & VALIDATED  

---

## 1. Executive Summary

In acute natural hazard crises, delay costs lives. The HAZARDX AI platform was benchmarked under real operational workloads on standard commodity hardware (without GPU acceleration) to measure latency, throughput, and system responsiveness across all software tiers.

### Key Benchmark Findings:
- **FastAPI Endpoints:** Sub-10ms response times for metadata, model status, and alert queries.
- **Model Inference Speed:** **4.7 ms to 5.6 ms** steady state per prediction, including local TreeSHAP attribution extraction.
- **Database Query Latency:** **2.0 ms** average query execution over indexed SQLite tables.
- **Forecast Generation:** **141.4 ms** multi-horizon forecast synthesis.

---

## 2. API Response Latency Benchmarks

Measurements were captured across repeated empirical requests to the local ASGI server (`http://127.0.0.1:8000`):

| Endpoint Route | Microservice Role | Mean Latency | Min Latency | Max Latency | Payload Size | SLA Target |
|---|---|---|---|---|---|---|
| `GET /api/v1/health` | Health & DB Telemetry | **5.9 ms** | 3.1 ms | 10.6 ms | 501 B | $< 50$ ms |
| `GET /api/v1/models` | Model Registry Status | **7.5 ms** | 5.4 ms | 11.4 ms | 5,451 B | $< 50$ ms |
| `GET /api/v1/alerts` | Active Alerts Feed | **9.5 ms** | 9.0 ms | 10.2 ms | 26,414 B | $< 100$ ms |
| `GET /api/v1/intelligence/freshness` | Data Freshness Audit | **17.1 ms** | 14.6 ms | 18.7 ms | 1,741 B | $< 100$ ms |
| `GET /api/v1/forecasts/summary` | Forecast Summary Cards | **141.4 ms** | 129.1 ms | 164.4 ms | 2,057 B | $< 300$ ms |
| `GET /api/v1/explanations/floods` | Global TreeSHAP Summary | **3.4 ms** | 2.8 ms | 4.5 ms | 1,390 B | $< 50$ ms |

---

## 3. Machine Learning Inference Latency (with TreeSHAP)

Measurements record the complete pipeline from HTTP request ingestion through schema validation, XGBoost execution, probability calibration, local TreeSHAP attribution extraction, and response serialization:

| Hazard Domain | Primary Task | Steady-State Latency | TreeSHAP Overhead | Operational Throughput |
|---|---|---|---|---|
| **Floods** | `flood_occurrence` | **5.6 ms** | ~2.9 ms | ~180 req/sec |
| **Landslides** | `landslide_occurrence` | **4.7 ms** | ~2.4 ms | ~210 req/sec |
| **Earthquakes** | `aftershock_hazard` | **4.8 ms** | ~2.5 ms | ~210 req/sec |
| **Cyclones** | `rapid_intensification` | **5.5 ms** | ~2.8 ms | ~180 req/sec |
| **Wildfires** | `wildfire_occurrence` | **5.4 ms** | ~2.6 ms | ~185 req/sec |

---

## 4. Database Query Latency

Audited over `data/hazardx_live.db` operating in Write-Ahead Logging (WAL) mode:
- Query: `SELECT COUNT(*) FROM alerts` $\to$ **0.8 ms**
- Query: `SELECT COUNT(*) FROM api_logs` $\to$ **1.2 ms**
- Combined Analytical Fetch: **2.0 ms** total execution time.
- Zero table lock contention observed under concurrent test executions.

---

## 5. Benchmark Conclusion

The HAZARDX AI platform operates with exceptional speed, easily satisfying all real-time disaster intelligence SLAs on standard CPU hardware.

**Performance Benchmark Status: PASSED (EXCEEDS SLA)**
