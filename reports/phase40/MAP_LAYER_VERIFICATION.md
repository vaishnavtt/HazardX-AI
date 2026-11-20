# HAZARDX AI — MAP LAYER & GEOSPATIAL AUDIT REPORT
**Document ID:** `HX-RPT-PH40-05`  
**Phase:** Phase 40 — Application, Security, Map & Performance Audit  
**Author:** Senior GIS & Geospatial Visualization Engineer  
**Date:** November 20, 2026  
**Status:** VERIFIED & COMPLIANT  

---

## 1. Executive Summary

This report documents the verification of the interactive geospatial visualization layer, GeoJSON vector layers, raster map styling, and coordinate projection systems within HAZARDX AI.

---

## 2. Geospatial Layer Specifications

The interactive map (`/map`) renders multi-hazard layers via MapLibre GL and Leaflet, styled with distinct hazard color palettes adhering to international early-warning conventions:

| Hazard Domain | Primary Color | Hex Code | Vector Geometry | Data Attribution / Sources |
| :--- | :--- | :--- | :--- | :--- |
| **Floods** | Hydro Blue | `#3B82F6` | Polygons / Inundation Zones | Copernicus GloFAS / HydroSHEDS |
| **Landslides** | Terrestrial Amber | `#F59E0B` | Contours / High-Slope Corridors | NASA GLC / Copernicus DEM 90m |
| **Earthquakes** | Tectonic Red | `#EF4444` | Polylines (Faults) & Point Epicenters | USGS ComCat / GEM Global Faults |
| **Wildfires** | Flame Orange | `#F97316` | Heatmaps & Hotspot Points | NASA FIRMS / EFFIS Fire Danger |
| **Cyclones** | Storm Violet | `#8B5CF6` | Cone Corridors & Track Trajectories | NOAA NHC / IBTrACS / IMD RSMC |

---

## 3. Map Layer Features Verified

1. **WGS 84 (EPSG:4326) Projection:** All GeoJSON coordinates conform strictly to longitude/latitude ordering without inversion errors.
2. **Dynamic Zoom Filtering:** Point clustering automatically adjusts from macro-synoptic scale (Zoom 2) down to neighborhood hazard zones (Zoom 14).
3. **Interactive Popups & Tooltips:** Clicking any hazard zone or event marker displays:
   - Hazard name and current alert level badge.
   - Primary physical metric (e.g., FWI index, river discharge ratio, Richter magnitude).
   - Timestamp and data provenance.
   - Actionable protective guidance.
4. **Layer Toggle Controls:** Users can independently toggle each of the 5 hazard layers and switch between Forecast Risk Zones, Live Observations, and Historical Benchmarks.

---

## 4. Certification Sign-Off

The geospatial map visualization layer functions smoothly, adheres to GIS standards, and presents geographically meaningful, scientifically accurate risk zones.
