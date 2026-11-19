# HAZARDX AI – Phase 29: Prediction Trace Report

**Date:** November 19, 2026  
**Auditor:** Senior AI/ML & Disaster Intelligence Engineering Team  
**Subject:** End-to-End Diagnostic Trace of Location Risk Assessment  
**Test Location:** Wayanad, Kerala, India (11.6854° N, 76.1320° E)  

---

## 1. Raw External Telemetry Captured

| Telemetry Element | Capturing Client | Measured Real-Time Value | Status |
| :--- | :--- | :--- | :--- |
| **2m Ambient Temperature** | Open-Meteo Global NWP | **27.3°C** | `LIVE` |
| **Relative Humidity** | Open-Meteo Global NWP | **47.0%** | `LIVE` |
| **10m Surface Wind Speed** | Open-Meteo Global NWP | **2.6 m/s** (9.4 km/h) | `LIVE` |
| **Surface Pressure** | Open-Meteo Global NWP | **928.4 hPa** | `LIVE` |
| **Current 1h / 24h Precipitation** | Open-Meteo Global NWP | **0.0 mm** | `LIVE` |
| **Antecedent 30-Day Precipitation**| Open-Meteo ERA5 / NWP | **118.4 mm** | `LIVE` |
| **River Discharge & Anomaly** | Copernicus GloFAS | **0.50 m³/s** ($1.0\times$ normal) | `LIVE` |
| **Regional Seismicity (100km / 30d)**| USGS ComCat API | **0 events** (Max M: 0.0) | `LIVE` |
| **Nearest Mapped Active Fault** | Global Fault Database | **1,410.1 km** (Indian Ocean) | `HISTORICAL` |
| **Active Satellite Fire Hotspots** | NASA FIRMS VIIRS/MODIS | **0 detections within 50 km** | `LIVE` |
| **North Indian Ocean Cyclones** | IMD RSMC New Delhi | **0 active depressions/storms** | `LIVE` |
| **Topography (Copernicus DEM)** | 30m Global DEM | Elevation: **765 m**, Slope: **5.9°** | `STATIC` |

---

## 2. Model Feature Ingestion & Prediction Trace

```
══════════════════════════════════════════════════════════════════════════════════════════════════════
                               WAYANAD PIPELINE EXECUTION TRACE
══════════════════════════════════════════════════════════════════════════════════════════════════════
 1. FLOODS:
    - Input Features  : precip_1d=0.0mm, precip_7d=0.0mm, Q=0.5m³/s, Q_ratio=1.0, slope=5.9°, TWI=7.2
    - Raw Model Score : 0.0907 (9.1%)
    - Calibrated Score: 0.0005 (0.05%)
    - Classification  : Category: LOW | Alert: GREEN
    - Diagnosis       : Dry weather; model correctly reflects absence of flood trigger.

 2. LANDSLIDES:
    - Input Features  : precip_1d=0.0mm, precip_30d=118.4mm, slope=5.9°, clay=28.5%
    - Raw Model Score : 0.1041 (10.4%)
    - Calibrated Score: 0.0002 (0.02%)
    - Classification  : Category: LOW | Alert: GREEN
    - Diagnosis       : Dry weather; model correctly reflects lack of meteorological trigger today.
                        (Note: Historical Chooralmala debris flow occurred on July 30, 2024 under 572mm rain).

 3. EARTHQUAKES:
    - Injected Dummy  : mainshock_mag=6.0, focal_depth=10.0km, prior_count_30d=0, dist_to_fault=1410km
    - Raw Model Score : 0.1769 (17.7%)
    - Calibrated Score: 0.1769 (17.7%)
    - Classification  : Category: QUIESCENT | Alert: GREEN
    - Defect Detected : System injected non-existent M6.0 mainshock and computed 18% aftershock rate!
                        Correct behavior: 0 events -> Aftershock probability = 0.0% / QUIESCENT.

 4. WILDFIRES:
    - Input Features  : temp=27.3°C, RH=47%, wind=2.6m/s, rain_30d=118.4mm, FWI=0.8
    - Raw Model Score : 0.5582 (55.8% ~ 60%)
    - Calibrated Score: 0.0025 (0.25%)
    - Classification  : Category: MODERATE (Previously HIGH) | Alert: YELLOW (Previously ORANGE)
    - Defect Detected : Raw score dominated by ambient tropical temp (+2.08 SHAP); system passed raw
                        uncalibrated score to categorizer, ignoring FWI=0.8 and calibrated prob 0.25%.

 5. CYCLONES:
    - Injected Dummy  : current_wind=45.0kt, current_pres=996hPa, dist_to_land=85km
    - Raw Model Score : 0.2744 (27.4%)
    - Calibrated Score: 0.2744 (27.4%)
    - Classification  : Category: MODERATE_RI_POTENTIAL | Alert: YELLOW
    - Defect Detected : Injected fictitious 45kt storm into an inland mountain valley in Kerala!
                        Correct behavior: No active storm in BoB/AS -> Cyclone threat = NONE.
══════════════════════════════════════════════════════════════════════════════════════════════════════
```

---

## 3. Discrepancy Reconciliation Summary

| Hazard | Previously Displayed Output | Actual Physical Telemetry | Source of Discrepancy |
| :--- | :--- | :--- | :--- |
| **Wildfire** | `HIGH – 60%` | $T = 27.3^\circ\text{C}$, $\text{RH} = 47\%$, $\text{FWI} = 0.8$, 0 active FIRMS fires | Synthetic training distribution shift + raw uncalibrated score categorization |
| **Earthquake** | `QUIESCENT – 18%` | 0 earthquakes within $100\text{ km}$, nearest fault $1,410\text{ km}$ | Dummy $M 6.0$ default injected into aftershock decay formula |
| **Cyclone** | `MODERATE – 27%` | Inland mountain valley, 0 active storms in North Indian Ocean | Dummy $45\text{ kt}$ storm injected for all locations $|\text{lat}| \le 45^\circ$ |
| **Flood** | `LOW – 9%` | $0\text{ mm}$ rain, normal river discharge ($0.5\text{ m}^3/\text{s}$) | Baseline 1:1 case-control raw probability under zero rainfall |
| **Landslide** | `LOW – 8%` | $0\text{ mm}$ rain, dry conditions today | Baseline 1:1 case-control raw probability under zero rainfall |

**Conclusion:** The reported inconsistencies are 100% reproducible and traced directly to feature injection fallbacks, uncalibrated scoring, and synthetic training distribution shifts.
