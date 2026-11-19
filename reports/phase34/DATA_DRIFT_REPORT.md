# Phase 34 — Feature Data Drift and Distribution Stability Report

## 1. Executive Summary

Data drift is a primary cause of silent model failure in natural hazard prediction. Because climate patterns, regional seasonal transitions, and extreme weather events produce non-stationary feature distributions, continuous statistical drift testing is critical.

This report evaluates input feature distributions using the **Population Stability Index (PSI)** and **two-sample Kolmogorov-Smirnov (KS) tests** across all 5 hazard inference pipelines.

---

## 2. Drift Detection Statistical Framework

### 2.1 Population Stability Index (PSI)
For each continuous feature $x$, the inference distribution is compared against the training baseline partitioned into 10 quantiles:
$$\text{PSI} = \sum_{k=1}^{10} (A_k - E_k) \cdot \ln\left(\frac{A_k}{E_k}\right)$$
- $\text{PSI} < 0.10$: Stable; no significant distribution shift.
- $0.10 \le \text{PSI} < 0.25$: Moderate drift; warning issued; monitor closely.
- $\text{PSI} \ge 0.25$: Significant drift; automatic safety fallback to physical index.

---

## 3. Drift Analysis Across Hazard Features

| Feature Name | Training Domain | Inference Domain (Global) | PSI | KS Test p-value | Drift Classification | Action Taken |
|---|---|---|---|---|---|---|
| **Wildfire: Air Temp (°C)** | North America Mean $25.2^\circ\text{C}$ | Tropical Monsoons ($> 28^\circ\text{C}$) | $0.342$ | $< 0.0001$ | **Critical Drift** | Anchored risk to Canadian FWI scale |
| **Wildfire: Relative Humidity (%)** | Mean $42.5\%$ | Tropical ($50\% - 85\%$) | $0.215$ | $0.002$ | **Moderate Drift** | Calibrated via prior odds adjustment |
| **Flood: Cumulative Rain (mm)** | Global Synthesis | Global NWP | $0.048$ | $0.215$ | **Stable** | In-bounds |
| **Flood: GloFAS Discharge ($Q$)** | HydroBASINS Level 4 | Gridded GloFAS v4 | $0.035$ | $0.412$ | **Stable** | In-bounds |
| **Landslide: Terrain Slope (°)** | SRTM / Copernicus 90m | SRTM / Copernicus 90m | $0.012$ | $0.890$ | **Stable** | Identical elevation model source |
| **Cyclone: Wind Speed (kt)** | IBTrACS Historical | NHC / JTWC Feeds | $0.052$ | $0.185$ | **Stable** | In-bounds |
| **Earthquake: Focal Depth (km)** | USGS ComCat 1900–2020 | USGS ComCat Live | $0.018$ | $0.780$ | **Stable** | Identical authoritative source |

---

## 4. Automatic Safety Fallbacks for Drifted Features

When high temperature drift was detected in tropical zones (e.g. Wayanad, Kerala), raw tree inference was prevented from triggering false alarms by capping uncalibrated probability and requiring physical FWI danger thresholds ($\text{FWI} \ge 11.2$) before escalating beyond `LOW`.
