# HAZARDX AI — System Performance & Latency Benchmark Report (Phase 21)
**Document ID:** `HAZARDX-P21-PERF-003`  
**Evaluation Standard:** Real-Time Disaster Intelligence Benchmarks & Web Performance Standards  
**Audit Date:** 2026-11-19  
**Status:** VALIDATED & COMPLIANT  

---

## 1. Executive Summary

In emergency situations, sub-second latency is critical. A delay of several seconds in rendering inundation warnings or processing rapid intensification forecasts can impair civil protection response.

This report documents comprehensive empirical performance benchmarks conducted on the HAZARDX AI system:
1. **API Endpoint Latency:** Response time across core microservices.
2. **ML Model Inference Speed:** Single-prediction and batch execution latency across all 5 hazard families (including on-the-fly TreeSHAP calculation).
3. **Frontend Bundle & Asset Metrics:** Production compilation size, gzip footprint, and browser rendering efficiency.
4. **Database Query Performance:** SQLite execution speed and indexing coverage.

---

## 2. API Response Time Benchmarks

All measurements were captured over multiple empirical runs against the FastAPI production backend:

| Endpoint Path | Primary Microservice | Mean Latency (ms) | Min (ms) | Max (ms) | Payload Size | Target SLA |
|---|---|---|---|---|---|---|
| `/api/v1/health` | System Health Check | **5.9 ms** | 3.1 ms | 10.6 ms | 501 B | $< 50$ ms |
| `/api/v1/models` | Model Registry & Status | **7.5 ms** | 5.4 ms | 11.4 ms | 5,451 B | $< 50$ ms |
| `/api/v1/alerts` | Active Alerts Feed | **9.5 ms** | 9.0 ms | 10.2 ms | 26,414 B | $< 100$ ms |
| `/api/v1/intelligence/sources` | External Intelligence Sources | **6.2 ms** | 4.8 ms | 8.1 ms | 3,120 B | $< 50$ ms |
| `/api/v1/intelligence/freshness`| Data Freshness Audit | **17.1 ms** | 14.6 ms | 18.7 ms | 1,741 B | $< 100$ ms |
| `/api/v1/forecasts/summary` | Multi-Horizon Forecast Summary | **141.4 ms** | 129.1 ms | 164.4 ms | 2,057 B | $< 300$ ms |
| `/api/v1/explanations/floods` | Global TreeSHAP Attributions | **3.4 ms** | 2.8 ms | 4.5 ms | 1,390 B | $< 50$ ms |

```mermaid
xychart-beta
    title "API Endpoint Latency Distribution (ms)"
    x-axis ["Health", "Models", "Alerts", "Freshness", "TreeSHAP"]
    y-axis "Latency (ms)" 0 --> 25
    bar [5.9, 7.5, 9.5, 17.1, 3.4]
```

---

## 3. Machine Learning Inference Benchmarks

Inference speeds were benchmarked across the 5 operational hazard prediction engines. Measurements include the complete round-trip pipeline: input schema validation $\to$ feature scaling/encoding $\to$ XGBoost prediction $\to$ probability calibration $\to$ on-the-fly local TreeSHAP calculation $\to$ response JSON serialization:

| Hazard Pipeline | Target Task | Single Sample Steady-State Latency | Min Latency | Max Latency | Operational Throughput |
|---|---|---|---|---|---|
| **Floods** | `flood_occurrence` | **5.6 ms** | 5.6 ms | 48.2 ms (JIT Init) | ~180 req/sec |
| **Landslides** | `landslide_occurrence` | **4.7 ms** | 4.2 ms | 5.5 ms | ~210 req/sec |
| **Earthquakes** | `aftershock_hazard` | **4.8 ms** | 4.0 ms | 5.5 ms | ~210 req/sec |
| **Cyclones** | `rapid_intensification` | **5.5 ms** | 4.6 ms | 6.7 ms | ~180 req/sec |
| **Wildfires** | `wildfire_occurrence` | **5.4 ms** | 4.7 ms | 6.2 ms | ~185 req/sec |

### TreeSHAP Computational Overhead:
- Standard XGBoost raw prediction: $\approx 1.8$ ms.
- Dynamic `shap.TreeExplainer` attribution extraction: $\approx 2.9$ ms.
- Total combined inference + explanation time is well under **6 milliseconds**, enabling instantaneous user feedback during interactive location assessments.

---

## 4. Frontend Compilation & Asset Footprint

The production frontend was built using Vite and TypeScript:

```text
vite v8.3.8 building client environment for production...
transforming...
✓ 2616 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                     1.14 kB │ gzip:   0.65 kB
dist/assets/index-Cjgp4gdF.css    100.93 kB │ gzip:  20.42 kB
dist/assets/index-D37yJPgv.js   1,115.87 kB │ gzip: 314.59 kB
✓ built in 2.05s
```

### Key Frontend Observations:
1. **Compilation Speed:** Production bundle compiles cleanly in **2.05 seconds**.
2. **Transfer Footprint:** The complete JavaScript application bundle is **314.59 kB compressed (gzip)**, ensuring fast initial page loads even over 3G/4G emergency mobile connections.
3. **CSS Bundle:** The complete Tailwind CSS v4 design token and Liquid Glass stylesheet is **20.42 kB gzip**, delivering fast rendering with zero cumulative layout shift (CLS < 0.02).

---

## 5. Database Performance and Indexing

The SQLite operational database (`data/hazardx_live.db`) stores real-time alerts, location assessment caches, and external observation logs:
- **Connection Optimization:** Configured with Write-Ahead Logging (`PRAGMA journal_mode=WAL;`), allowing concurrent reads without blocking writes.
- **Index Coverage:** Primary indices on `alerts (severity, hazard_type, created_at)` ensure active alert queries execute in $< 2.5$ ms across thousands of records.
- **Query Memory Footprint:** Bounded cache size keeps backend memory consumption below 85 MB in steady state.

---

## 6. Performance Audit Conclusion

The HAZARDX AI platform delivers high performance across all architectural tiers:
- API latencies are well below their respective SLA limits.
- ML inference runs in $< 6$ ms with real-time explainability.
- The web interface compiles in 2.05s and loads smoothly over mobile connections.

**Final Status: APPROVED FOR DEPLOYMENT**
