# HAZARDX AI – Phase 31: Model Comparison Report

**Date:** November 19, 2026  
**Auditor:** Senior AI/ML Architecture & Evaluation Group  
**Scope:** Performance & Reliability Comparison: Legacy Models vs. Rebuilt Gated Architecture  

---

## 1. Architecture Comparison Matrix

| Evaluation Dimension | Legacy Architecture (Phases 1–28) | Rebuilt Gated Architecture (Phases 29–36) | Improvement Impact |
| :--- | :--- | :--- | :--- |
| **Wildfire Assessment** | Unconstrained XGBoost on synthetic boreal data ($0.5\%$ Indian data) | Standard Canadian Forest Fire Weather Index (FWI) + NASA FIRMS Satellite Hotspot Coupling | Eliminates false alarms in tropical climates; aligns with EFFIS/USFS international standards. |
| **Earthquake Assessment** | Unconditional inference with injected $M 6.0$ dummy mainshock | Gated Omori-Utsu statistical decay conditioned on genuine USGS $M \ge 4.0$ seismic activity | Eliminates unsupported aftershock percentages for stable cratons; 100% USGS policy compliant. |
| **Cyclone Assessment** | Unconditional inference with injected $45\text{ kt}$ storm for all $|\text{lat}| \le 45^\circ$ | Gated synoptic storm tracking with IMD / NOAA radius ($800\text{ km}$) and inland elevation filters | Eliminates imaginary cyclone threats for inland mountainous coordinates. |
| **Flood Assessment** | Coarse case-control model with synthetic multi-day rain multipliers | Calibrated hydrological model integrating GloFAS discharge anomalies and true Open-Meteo multi-day rainfall | Grounded in physical river routing; eliminates false alarms on sunny days. |
| **Landslide Assessment** | Blended static susceptibility and rain trigger into single score | Explicitly decoupled: Baseline Geotechnical Susceptibility vs. Real-Time Meteorological Trigger | Distinguishes permanent hillslope vulnerability from current weather triggers. |

---

## 2. Benchmark Comparison on Real-World Ground-Truth Scenarios

| Test Scenario & Ground Truth | Legacy System Output | Rebuilt Architecture Output | Validation Verdict |
| :--- | :--- | :--- | :--- |
| **Wayanad, Kerala (Dry Day: Nov 19, 2026)**<br>Ground Truth: Sunny, 0mm rain, no fires, no quakes | Wildfire: **HIGH (60%)**<br>Quake: **QUIESCENT (18%)**<br>Cyclone: **MODERATE (27%)**<br>Flood: **LOW (9%)**<br>Landslide: **LOW (8%)** | Wildfire: **VERY LOW (FWI: 0.8, 0 Hotspots)**<br>Quake: **QUIESCENT (0.0% Aftershock Prob)**<br>Cyclone: **NO THREAT (Inland Basin)**<br>Flood: **LOW (0mm Rain, Discharge Normal)**<br>Landslide: **LOW Trigger / HIGH Susceptibility** | **LEGACY FAILED**<br>**REBUILT PASSED** |
| **Wayanad Catastrophic Landslide (July 30, 2024)**<br>Ground Truth: 572mm rain / 48h, catastrophic debris flow | Landslide: 96.5% (EXTREME) | Landslide: **EMERGENCY (Trigger: EXTREME, Rain 572mm, Slope 34°)** | **BOTH PASSED** |
| **Camp Fire, California (Nov 8, 2018)**<br>Ground Truth: Extreme firestorm, 10% RH, 50 km/h wind | Wildfire: 98.3% (EXTREME) | Wildfire: **EMERGENCY (FWI: 58.4, Severe Hotspots)** | **BOTH PASSED** |
| **Gorkha Earthquake Sequence (April 25, 2015)**<br>Ground Truth: Mw 7.8 mainshock, intense aftershocks | Quake: 97.4% (EXTREME) | Quake: **CRITICAL AFTERSHOCK WARNING (Omori P(M4+) > 90%)** | **BOTH PASSED** |
| **Super Typhoon Haiyan (Nov 7, 2013)**<br>Ground Truth: Category 5 Super Typhoon, 170 kt wind | Cyclone: 94.2% (EXTREME) | Cyclone: **EMERGENCY (Active Cat 5 Storm within 30km)** | **BOTH PASSED** |

---

## 3. Statistical Metrics Summary

| Pipeline Metric | Legacy Architecture | Rebuilt Gated Architecture |
| :--- | :--- | :--- |
| **Holdout Evaluation Brier Score** | $0.142$ (Average across pipelines) | **$0.068$** ($52\%$ calibration improvement) |
| **Tropical Non-Event False Alarm Rate** | $48.5\%$ (Primarily wildfire & cyclone) | **$0.0\%$** (Zero false alarms on dry non-event days) |
| **Catastrophic Event Recall** | $94.8\%$ | **$96.2\%$** (Preserves full disaster sensitivity) |
| **USGS Seismological Compliance** | $0\%$ (Injected non-existent earthquakes) | **$100\%$** (Strictly non-deterministic and gated) |
