# HAZARDX AI – FINAL USER & OPERATING GUIDE

**Document ID:** `HX-DOC-OPS-2026-FINAL`  
**System:** HAZARDX AI – Global Multi-Hazard Intelligence and Early Warning System  
**Audience:** Disaster Management Operators, First Responders, Researchers, and Everyday Users  
**Date:** November 2026  
**Status:** Approved for Local and Operational Use  

---

## 1. Welcome to HAZARDX AI

**HAZARDX AI** is a global multi-hazard intelligence and early warning decision-support system. It continuously analyzes real-time weather models, satellite observations, seismic feeds, and river basin sensors to forecast natural hazard risks across five domains:
- 🌊 **Floods** (River overflow, intense cloudburst rain, and inundation)
- ⛰️ **Landslides** (Steep slope failure, rain-saturated soil mudflows)
- ⚡ **Earthquakes** (Recorded seismic shocks and statistical aftershock decay probability)
- 🌀 **Cyclones** (Tropical storm tracks, wind swaths, and rapid intensification)
- 🔥 **Wildfires** (Satellite thermal hotspots, low humidity, and dry fuel conditions)

The platform is wrapped in a clean, Apple-inspired **Light Liquid Glass** user interface designed for maximum readability and ease of use.

---

## 2. Quick-Start Instructions (One-Click Launch)

You do **not** need to type complex terminal commands or edit code files to use HAZARDX AI.

### Starting the Application
1. Open the project folder: `C:\Users\thott\Desktop\hazardai`.
2. Double-click **`START_HAZARDX.bat`**.
3. A launcher window will automatically:
   - Check your Python and Node.js environments.
   - Start the FastAPI backend server on `http://127.0.0.1:8000`.
   - Start the React frontend on `http://localhost:5173`.
   - Automatically open your default web browser to the application dashboard.

### Stopping the Application
1. Double-click **`STOP_HAZARDX.bat`**.
2. All background server processes on ports 8000 and 5173 will be cleanly terminated.

---

## 3. Manual Startup (For Developers)

If you prefer to start services individually using separate terminal windows:

### Terminal 1: Backend
```powershell
cd C:\Users\thott\Desktop\hazardai
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Documentation (Swagger UI): `http://127.0.0.1:8000/docs`
- Health Endpoint: `http://127.0.0.1:8000/api/v1/health`

### Terminal 2: Frontend
```powershell
cd C:\Users\thott\Desktop\hazardai\frontend
npm run dev
```
- Web Application: `http://localhost:5173`

---

## 4. Platform Navigation Guide

| Page | Navigation Route | Primary Features |
|:---|:---|:---|
| **Dashboard** | `/` | Overview of global system health, high-priority active alerts, quick search bar, and one-click shortcuts to each hazard module. |
| **Global Hazard Map** | `/map` | Interactive world map featuring OpenStreetMap tiles, layer toggles for all 5 hazards, basemap switcher (Standard, Light, Terrain), and clickable inspection drawer. |
| **Forecast Center** | `/forecasts` | Predictive projections spanning **6h, 12h, Tomorrow (24h), Next 2 Days, and Next 3 Days**, with interactive risk trajectory graphs and live telemetry source monitors. |
| **Check My Location** | `/check-location` | Global city search and coordinate risk assessment engine. Evaluates composite risk across all five hazard vectors for any location on Earth. |
| **Active Alerts** | `/alerts` | Operational incident management feed with severity filtering (*Critical Red, High Orange, Moderate Yellow*), physical telemetry factors, and officer resolution workflows. |
| **Past Events** | `/past-events` | Ground-truth historical benchmark disaster archive (Wayanad 2024, Henan 2021, Katrina 2005, Haiyan 2013, Gorkha 2015). |
| **About & Ethics** | `/about` | Explains system mechanics, official hazard colors, severity standards, and statutory non-predictive earthquake policies. |

---

## 5. How to Use Global City Search & Autocomplete

On both the **Dashboard** and the **Check My Location** page, you will find the Global Location Search bar:

1. **Search by City Name:** Type any city or region worldwide (e.g., `Wayanad`, `Kochi`, `London`, `Tokyo`, `New York`, `Sydney`).
2. **Instant Suggestions:** Autocomplete options will appear automatically within 250 milliseconds.
3. **Keyboard Navigation:** Use `ArrowDown` and `ArrowUp` on your keyboard to navigate suggestions, then press `Enter` to select.
4. **Search by Coordinates:** You can also paste exact geographic coordinates (e.g. `29.95, -90.07`).
5. **Recent Searches:** Your 5 most recent searches are remembered in your browser for one-click access.

---

## 6. Understanding the Five Official Hazard Colors

HAZARDX AI uses five consistent colors worldwide so you can instantly recognize each hazard without reading small text:

- 🌊 **Blue (`#2196F3`):** Floods
- ⛰️ **Orange (`#FF9800`):** Landslides
- ⚡ **Purple (`#9C27B0`):** Earthquakes
- 🌀 **Cyan (`#00BCD4`):** Cyclones
- 🔥 **Red (`#F44336`):** Wildfires

### Risk Severity Tiers
Severity is communicated through geometric opacity and borders rather than changing the hazard color:
- **LOW:** Mild background conditions (20% opacity).
- **MODERATE:** Elevated physical readings (40% opacity).
- **HIGH:** Significant hazard development (60% opacity).
- **CRITICAL / EXTREME:** Severe life-safety threat (75%+ opacity with pulsing rings).

---

## 7. Troubleshooting Common Questions

### 1. The map is not loading tiles or showing an error
- HAZARDX AI uses OpenStreetMap standard tiles (`tile.openstreetmap.org`) which do not require any API keys.
- If you have no internet access, the map will use cached tiles or fallback seamlessly.
- You can switch between **Standard**, **Light**, and **Terrain** using the basemap selector in the top-right of the map.

### 2. Port already in use error (Port 8000 or 5173)
- If you see an error indicating port 8000 or 5173 is already in use, run **`STOP_HAZARDX.bat`** once to clear orphaned processes, then re-run **`START_HAZARDX.bat`**.

### 3. Are earthquake predictions guaranteed?
- **No.** HAZARDX AI strictly follows international USGS scientific consensus: **exact earthquake time and location cannot be predicted**. The platform displays recorded physical seismic events and models statistical aftershock decay probability following an event.
