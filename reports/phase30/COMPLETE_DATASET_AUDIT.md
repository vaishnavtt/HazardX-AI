# HAZARDX AI – Phase 30: Complete Dataset Audit

**Date:** November 19, 2026  
**Auditor:** Senior AI/ML & Disaster Data Engineering Group  
**Scope:** Comprehensive Audit of all 5 Model-Ready Training Datasets in `data/model_ready/`  

---

## 1. Dataset Inventory & Statistical Profile

| Hazard Domain | Dataset File | Records | Features | Missing Values | Duplicates | Train / Val / Test Split | Class Balance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cyclones** | `cyclone_model_ready.csv` | **220,484** | 22 | 0 (0.0%) | 0 (0.0%) | 177,798 / 20,930 / **21,756** | 5.8% RI Positive (12,788) / 94.2% Negative (207,696) |
| **Earthquakes** | `earthquake_model_ready.csv` | **10,000** | 19 | 0 (0.0%) | 0 (0.0%) | 7,255 / 1,207 / **1,538** | 42.1% Elevated Hazard (4,210) / 57.9% Quiescent (5,790) |
| **Floods** | `flood_model_ready.csv` | **600** | 22 | 0 (0.0%) | 0 (0.0%) | 486 / 33 / **81** | 50.0% Floods (300) / 50.0% Non-Flood Controls (300) |
| **Landslides** | `landslide_model_ready.csv` | **600** | 22 | 0 (0.0%) | 0 (0.0%) | 366 / 144 / **90** | 50.0% Landslides (300) / 50.0% Non-Slide Controls (300) |
| **Wildfires** | `wildfire_model_ready.csv` | **1,200** | 19 | 0 (0.0%) | 0 (0.0%) | 930 / 174 / **96** | 50.0% Fire Events (600) / 50.0% Non-Fire Controls (600) |

---

## 2. In-Depth Quality Audit Findings

### 2.1 The Case-Control Pre-Conditioning Issue
Floods, Landslides, and Wildfires were structured as **1:1 case-control datasets** (50% positive events, 50% negative controls).
- **Consequence:** Tree-based classifiers trained on balanced 1:1 data output raw probabilities centered near $0.50$ across their feature spaces. On a completely dry day with zero rainfall and zero trigger ($p_1 = 0\text{ mm}$), the tree leafs output $\approx 0.08–0.10$ ($8\%–10\%$).
- **Flaw:** Without Bayesian recalibration to actual environmental priors ($\sim 0.001–0.005$), these baseline scores ($8\%–10\%$) were mistakenly displayed as today's "Estimated Threat Score", confusing users into believing there is an active 10% disaster risk on a clear sunny day.

### 2.2 Synthetic Atmospheric Sampling in Dataset Preparation
In `build_wildfire_dataset.py`, `build_flood_dataset.py`, and `build_landslide_dataset.py`:
- Atmospheric weather variables were generated via parameterized random sampling rather than true ERA5 atmospheric extraction:
  - Wildfires: Fire temperature drawn from $\mathcal{N}(32.5, 5.0)$, non-fire from $\mathcal{N}(18.0, 6.0)$.
  - Floods: Flood 1d rain drawn from $\mathcal{U}(25, 95)$, non-flood from $\mathcal{U}(0, 4)$.
  - Landslides: Slide 1d rain drawn from $\mathcal{U}(45, 160)$, non-slide from $\mathcal{U}(0, 3)$.
- **Consequence:** The wildfire model learned that temperature $> 22^\circ\text{C}$ is a primary indicator of fire ignition, rendering it incapable of recognizing tropical monsoonal regions where temperatures are permanently $25–30^\circ\text{C}$ without fire risk.

### 2.3 Regional Distribution Deficits
- **Wildfire Dataset:** Only **6 out of 1,200 samples (0.5%)** are located in the Indian subcontinent. Median latitude is $52.5^\circ\text{N}$ (Boreal North America).
- **Landslides & Floods:** Good Indian subcontinent presence ($\approx 40\%$), but heavily reliant on high-rainfall triggers.

---

## 3. Dataset Suitability Assessment

| Hazard Pipeline | Suitable for Real-Time Operational Inference? | Assessment & Directives |
| :--- | :--- | :--- |
| **Cyclones** | **YES** | Authoritative NOAA IBTrACS dataset (220,484 genuine synoptic records). Suitable for RI and intensity delta modeling, provided input storms are physically verified within synoptic range. |
| **Earthquakes** | **YES (Conditionally)** | Authentic USGS ComCat catalog (10,000 real earthquakes). Valid for aftershock hazard assessment *only* when a real mainshock has occurred. Inappropriate for unconditioned location assessment. |
| **Floods** | **PARTIAL** | Authentic Dartmouth Flood Observatory event locations, but synthetic weather features require physical calibration and true GloFAS discharge integration. |
| **Landslides** | **PARTIAL** | Authentic NASA GLC landslide points, but synthetic non-event controls require physical slope-saturation decoupling. |
| **Wildfires** | **UNSUITABLE AS CONSTRUCTED** | Highly synthetic weather features + extreme boreal geographic bias. Must be replaced with authentic Canadian Forest Fire Weather Index (FWI) calculations and NASA FIRMS thermal anomaly detection. |
