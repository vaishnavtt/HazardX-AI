# HAZARDX AI — Complete REST API Reference Manual
**Document ID:** `HAZARDX-DOCS-API-004`  
**Base URL:** `http://127.0.0.1:8000/api/v1`  
**OpenAPI Specification:** Available at `/openapi.json` and interactive Swagger UI at `/docs`  

---

## 1. System Health & Metadata Endpoints

### 1.1 Service Health Check
- **`GET /api/v1/health`**
- **Description:** Verifies database connectivity, active worker uptime, and model registry loading.
- **Example Response:**
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-11-19T02:00:00Z",
    "version": "1.0.0",
    "total_models": 12,
    "database_connected": true,
    "active_alerts_count": 22
  }
  ```

### 1.2 Model Registry Catalog
- **`GET /api/v1/models`**
- **Description:** Returns operational disposition, algorithms, and primary holdout metrics for all 12 models.

---

## 2. Machine Learning Prediction Endpoints

### 2.1 Flood Susceptibility & Occurrence
- **`POST /api/v1/predict/floods`**
- **Example Request:**
  ```json
  {
    "precip_1d_mm": 120.5,
    "precip_3d_sum_mm": 210.0,
    "precip_7d_sum_mm": 320.0,
    "precip_14d_sum_mm": 450.0,
    "api_14d_index": 85.0,
    "river_discharge_m3s": 1250.0,
    "elevation_m": 45.0,
    "slope_degrees": 2.5,
    "topographic_wetness_index": 11.2,
    "distance_to_river_km": 0.8,
    "soil_temp_celsius": 18.5,
    "temp_2m_celsius": 24.0
  }
  ```
- **Example Response:**
  ```json
  {
    "hazard": "Floods",
    "predictions": {
      "flood_occurrence_probability": 0.842,
      "severity_class": "EXTREME"
    },
    "attributions": [
      {
        "feature": "precip_1d_mm",
        "importance_score": 0.5335,
        "direction": "RISK_INCREASING",
        "description": "Acute 24-hour rainfall intensity causing flash runoff."
      }
    ],
    "disclaimer": "HAZARDX AI Decision Support Advisory — Does not constitute a mandatory evacuation order."
  }
  ```

### 2.2 Landslide Occurrence & Runout
- **`POST /api/v1/predict/landslides`**

### 2.3 Earthquake Aftershock Clustering
- **`POST /api/v1/predict/earthquakes`**

### 2.4 Tropical Cyclone Rapid Intensification
- **`POST /api/v1/predict/cyclones`**

### 2.5 Wildfire Ignition Susceptibility
- **`POST /api/v1/predict/wildfires`**

---

## 3. Early Warning & Multi-Horizon Forecasting

### 3.1 Active Early Warning Alerts
- **`GET /api/v1/alerts`**
- **Query Parameters:** `hazard` (optional), `severity` (optional), `status` (default: `ACTIVE`)

### 3.2 Multi-Horizon Forecast Projections
- **`GET /api/v1/forecasts/summary`**
- **Description:** Returns summary forecast cards with lead times across 6h, 12h, 24h, 48h, and 72h.

### 3.3 Geospatial Multi-Hazard Assessment
- **`POST /api/v1/geospatial/assess`**
- **Request:** `{"lat": 35.6762, "lon": 139.6503, "location_name": "Tokyo, Japan"}`
- **Response:** Composite 5-hazard risk scores, 5-axis radar chart coordinates, and localized precautionary advice.
