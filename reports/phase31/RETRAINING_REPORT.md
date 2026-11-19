# HAZARDX AI – Phase 31: Retraining & Model Architecture Update Report

**Date:** November 19, 2026  
**Auditor:** Senior MLOps & Model Governance Group  
**Scope:** Model Configuration, Retraining Verification, and Physical Architecture Transition  

---

## 1. Artifact Preservation & Versioning

In strict compliance with Global Requirements 17 & 18:
- All original model artifacts in `models/` (`floods_flood_occurrence_xgboost.json`, `landslides_landslide_occurrence_xgboost.json`, `earthquakes_aftershock_hazard_xgboost.json`, `cyclones_rapid_intensification_xgboost.json`, `wildfires_wildfire_occurrence_xgboost.json`, etc.) are preserved without deletion.
- Model metadata files in `models/` are preserved with complete historical training records.
- Quarantined models (`earthquakes_aftershock_count_xgboost` and `wildfires_fire_duration_xgboost`) remain strictly blocked in `backend/app/config.py`.

---

## 2. Architecture Upgrade: Physical-Gated Hybrid Intelligence

Rather than relying on unconstrained tree-based black-box regressors that hallucinate risk outside their narrow training domains, the HAZARDX AI architecture is upgraded to an **Enterprise Physical-Gated Hybrid Intelligence Architecture**:

```text
               [Target Geographic Coordinate (lat, lon)]
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
 [USGS Seismicity Gate]   [IMD/NOAA Cyclone Gate]   [NASA FIRMS & FWI Engine]
  - Radial query (100km)   - Regional storm query    - Radial thermal hotspots (50km)
  - Qualifying M >= 4.0?   - Storm in range (<800km)?- Canadian Forest FWI standard
         │                        │                        │
  ┌──────┴──────┐          ┌──────┴──────┐          ┌──────┴──────┐
  ▼             ▼          ▼             ▼          ▼             ▼
[YES]          [NO]      [YES]          [NO]      [HOTSPOTS]    [0 HOTSPOTS]
  │             │          │             │          │             │
Omori-Utsu   QUIESCENT   Run RI        NO THREAT  Extreme Fire  Evaluate FWI
Decay Model  (P = 0.0%)  Model         (P = 0.0%) Threat Alert  Weather Danger
```

---

## 3. Retraining & Configuration Parameters

1. **Fire Weather Index (FWI) Harmonization:**
   - Unified standard Van Wagner / McArthur formulation implemented in `backend/app/geospatial/weather_features.py`.
   - Continuous inputs: Temperature, Relative Humidity, 10m Wind Speed, 30-day Precipitation Deficit.
2. **Radial Satellite Fire Hotspot Scanner:**
   - Implemented in `backend/app/integrations/nasa_firms_client.py`.
   - Circular radius: $50\text{ km}$, minimum confidence threshold: $50\%$.
3. **Radial Seismicity Pre-Condition Filter:**
   - Implemented in `backend/app/integrations/usgs_client.py` and `spatial_feature_service.py`.
   - Gating threshold: $\max(M) \ge 4.0$ within past 30 days within $100\text{ km}$.
4. **Marine Cyclone Distance Filter:**
   - Implemented in `backend/app/geospatial/spatial_feature_service.py`.
   - Proximity limit: $800\text{ km}$, elevation ceiling: $300\text{ m}$.
