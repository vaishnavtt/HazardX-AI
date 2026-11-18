# HAZARDX AI — Phase 11: Interactive Map Defect Analysis
**Component:** `frontend/src/components/map/GlobalHazardMap.tsx` & `frontend/src/pages/MapPage.tsx`  
**Date:** November 18, 2026  
**Auditor:** Senior Frontend Architect & GIS Engineering Specialist  
**System Location:** `C:\Users\thott\Desktop\hazardai`

---

## 1. Executive Summary

An in-depth technical inspection of the existing interactive map implementation identified multiple critical defects that prevented the map from operating as a reliable, production-grade GIS platform.

The defects ranged from **React component lifecycle and DOM sizing failures** to **complete omission of geographic polygon geometries, non-standard color palettes, and blank initial render states**.

---

## 2. Root Cause Defect Breakdown

### Defect 1: Missing Geographic Polygons & Hazard Zones
- **Observation:** `GlobalHazardMap.tsx` only initialized `L.marker` instances.
- **Root Cause:** The code contained zero logic for GeoJSON feature layers, polygons, multi-polygons, or corridor lines.
- **Impact:** Users could only see points on the map. Flood river basins, landslide slope failure corridors, earthquake fault zones, cyclone track cones, and wildfire danger areas could not be visually represented geographically.

### Defect 2: Non-Standard Hazard Color Scheme
- **Observation:** The map used arbitrary colors (`#0ea5e9`, `#f59e0b`, `#a855f7`, `#14b8a6`, `#f97316`).
- **Root Cause:** Hardcoded hex values did not adhere to the mandated hazard color specification.
- **Remediation Required:**
  - **Floods:** Blue (`#2196F3`)
  - **Landslides:** Orange (`#FF9800`)
  - **Earthquakes:** Purple (`#9C27B0`)
  - **Cyclones:** Cyan (`#00BCD4`)
  - **Wildfires:** Red (`#F44336`)

### Defect 3: Conflation of Hazard Type with Risk Severity
- **Observation:** Markers were colored only by hazard type without visual distinction of risk level.
- **Root Cause:** Missing separate visual encoding for risk categories (`LOW`, `MODERATE`, `HIGH`, `VERY HIGH`, `EXTREME`).
- **Remediation Required:**
  - Base color represents Hazard Category.
  - Severity represented via opacity, border stroke width, and pulsing ring:
    - *Low:* 20% opacity fill, 1px border.
    - *Moderate:* 40% opacity fill, 1.5px border.
    - *High:* 60% opacity fill, 2px border.
    - *Very High:* 75% opacity fill, 2.5px border.
    - *Extreme:* 90% opacity fill, 3px border with animated pulsing glow.

### Defect 4: Leaflet Container Sizing & Resize Invalidation Failure
- **Observation:** On certain screen sizes or when the sidebar collapsed/expanded, tiles appeared misaligned, gray, or only rendered in the top-left corner.
- **Root Cause:** Leaflet calculates tile grids based on the DOM container's pixel dimensions during initialization. If the flex container has not completed CSS layout, Leaflet computes 0 or incomplete dimensions. No `ResizeObserver` or window resize listener was attached to call `map.invalidateSize()`.
- **Remediation Required:** Attach a `ResizeObserver` to the map container to trigger `map.invalidateSize()` whenever parent layout shifts.

### Defect 5: React StrictMode Double-Mount / Container Initialization Crash
- **Observation:** During development or fast route transitions, Leaflet threw `Error: Map container is already initialized`.
- **Root Cause:** React 18/19 StrictMode mounts, unmounts, and remounts components. While `map.remove()` was called, the container DOM element still retained Leaflet's internal `_leaflet_id` property, causing subsequent `L.map()` calls to fail.
- **Remediation Required:** In the cleanup function, call `map.remove()` and explicitly delete `(container as any)._leaflet_id`.

### Defect 6: Blank Initial Render State
- **Observation:** When navigating to `/map`, the map appeared empty.
- **Root Cause:** `feedMode` was hardcoded to default to `'ALERTS'`. If the database had no active alerts at that moment, `alertEvents` was empty, resulting in zero plotted markers.
- **Remediation Required:** Default to a comprehensive multi-hazard view combining forecast risk zones and authentic live observations, ensuring immediate visual feedback.

### Defect 7: Coordinate Swapping Risk (GeoJSON vs Leaflet)
- **Observation:** Standard GeoJSON uses `[longitude, latitude]`, whereas Leaflet uses `[latitude, longitude]`.
- **Root Cause:** Inconsistent coordinate ordering can render polygons in the wrong hemisphere or ocean.
- **Remediation Required:** Strict GeoJSON standard parsing using Leaflet's native `L.geoJSON` layer with coordinate validation.

---

## 3. Repair Roadmap

1. **Backend:** Implement `GET /api/v1/geospatial/hazard-zones` returning authenticated GeoJSON FeatureCollections for all five hazard zones (Floods, Landslides, Earthquakes, Cyclones, Wildfires) linked to real-time risk evaluations.
2. **Frontend Map Architecture:**
   - Overhaul `GlobalHazardMap.tsx` with full GeoJSON polygon layers, point marker layers, and line layers.
   - Enforce the 5 mandatory hazard colors and 5 severity visual tiers.
   - Implement layer control switches: Hazard Toggles, Layer Category Toggles (`LIVE_OBSERVATIONS`, `FORECAST_RISK_ZONES`, `HISTORICAL_BENCHMARKS`, `MODEL_ASSESSMENTS`), and Severity Filters.
   - Implement robust Leaflet lifecycle with `ResizeObserver` and StrictMode cleanup.
   - Rich interactive click popup displaying hazard, location, coordinates, risk score, valid until, data source, provenance, and contributing factors.
   - Click-to-assess tool enabling dynamic 72h point evaluation.
3. **Browser Testing:** Launch backend and frontend, and run DevTools browser automation to visually verify map rendering, zoom/pan, layer toggles, and popup clicks.

