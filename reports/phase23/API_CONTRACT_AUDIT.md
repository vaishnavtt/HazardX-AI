# HAZARDX AI — API Contract & Endpoint Verification Audit (Phase 23)
**Document ID:** `HAZARDX-P23-ACA-002`  
**Evaluation Standard:** OpenAPI 3.1 & REST API Architectural Consistency  
**Audit Date:** 2026-11-19  
**Status:** ALL CONTRACTS VERIFIED & COMPLIANT  

---

## 1. Executive Summary

A disaster intelligence platform serves diverse consumers: interactive web dashboards, emergency command center consoles, automated message queues, and external civic partners. Strict adherence to API contracts, deterministic HTTP status codes, and predictable JSON schemas is vital to prevent frontend crashes or downstream integration failures.

This audit evaluates the complete REST API interface of HAZARDX AI (`/api/v1/`).

---

## 2. API Endpoint Verification Matrix

| Endpoint Route | Method | Expected HTTP | Validated Status | Request Payload DTO | Response Model DTO | Audit Finding |
|---|---|---|---|---|---|---|
| `/` | `GET` | 200 OK | **200 OK** | None | `RootResponse` | Root metadata & service health status |
| `/api/v1/health` | `GET` | 200 OK | **200 OK** | None | `HealthResponse` | Verifies database connectivity and model count |
| `/api/v1/models` | `GET` | 200 OK | **200 OK** | None | `ModelRegistryListResponse` | Full catalog of 12 models with operational statuses |
| `/api/v1/models/{hazard}/{task}` | `GET` | 200 OK / 404 | **200 OK** | Path parameters | `ModelDetailResponse` | Metadata, hyperparameters, and holdout scores |
| `/api/v1/predict/floods` | `POST` | 200 OK / 422 | **200 OK** | `FloodPredictionRequest` | `FloodPredictionResponse` | Bounded physical features, calibrated risk, TreeSHAP |
| `/api/v1/predict/landslides` | `POST` | 200 OK / 422 | **200 OK** | `LandslidePredictionRequest` | `LandslidePredictionResponse`| Topography, slope, antecedent rain, TreeSHAP |
| `/api/v1/predict/earthquakes` | `POST` | 200 OK / 422 | **200 OK** | `EarthquakePredictionRequest`| `EarthquakePredictionResponse`| Mainshock magnitude, fault distance, aftershock prob |
| `/api/v1/predict/cyclones` | `POST` | 200 OK / 422 | **200 OK** | `CyclonePredictionRequest` | `CyclonePredictionResponse` | Wind momentum, pressure drop, RI probability |
| `/api/v1/predict/wildfires` | `POST` | 200 OK / 422 | **200 OK** | `WildfirePredictionRequest` | `WildfirePredictionResponse` | FWI, RH, wind speed, occurrence probability |
| `/api/v1/explanations/{hazard}` | `GET` | 200 OK / 404 | **200 OK** | Query `task` | `HazardExplanationResponse` | Global TreeSHAP feature attributions and plot paths |
| `/api/v1/alerts` | `GET` | 200 OK | **200 OK** | Query filters | `AlertListResponse` | Active alerts with severity badges and guidance |
| `/api/v1/alerts/{id}/acknowledge`| `POST`| 200 OK / 404 | **200 OK** | JSON body | `AlertActionResponse` | Analyst acknowledgment transition |
| `/api/v1/alerts/{id}/resolve` | `POST` | 200 OK / 404 | **200 OK** | JSON body | `AlertActionResponse` | Alert resolution lifecycle transition |
| `/api/v1/intelligence/sources` | `GET` | 200 OK | **200 OK** | None | `SourcesResponse` | Telemetry provider metadata across 7 streams |
| `/api/v1/intelligence/freshness`| `GET` | 200 OK | **200 OK** | None | `DataFreshnessReport` | Real-time observation latency audit |
| `/api/v1/forecasts/summary` | `GET` | 200 OK | **200 OK** | None | `List[ForecastSummaryCard]` | Multi-hazard predictive outlook cards |
| `/api/v1/forecasts/timeline` | `GET` | 200 OK / 422 | **200 OK** | Query `hazard, lat, lon` | `HazardForecastTimeline` | Multi-horizon risk projections (6h to 72h) |
| `/api/v1/geospatial/assess` | `POST` | 200 OK / 422 | **200 OK** | `GeospatialAssessmentRequest`| `GeospatialAssessmentResponse`| Composite 5-hazard assessment and radar metrics |

---

## 3. Standardized Error Contract

All error responses across the platform conform to the unified error schema:

```json
{
  "status": "error",
  "error_code": "STRING_IDENTIFIER",
  "message": "Human-readable diagnostic summary.",
  "details": "Field-specific validation errors or sanitized diagnostic details."
}
```

### Verified HTTP Status Codes:
- **`200 OK`**: Successful query, inference, or lifecycle action.
- **`404 NOT FOUND`**: Unrecognized hazard domain, missing model task, or non-existent alert ID.
- **`422 UNPROCESSABLE CONTENT`**: Out-of-bounds physical variables (e.g. relative humidity $> 100\%$, latitude $> 90^\circ$).
- **`500 INTERNAL SERVER ERROR`**: Sanitized error envelope preventing raw traceback leaks.

---

## 4. Audit Conclusion

The HAZARDX AI API contract is uniform, strictly typed via Pydantic v2 schemas, and fully aligned with OpenAPI specifications.

**API Contract Status: AUDIT PASSED (100%)**
