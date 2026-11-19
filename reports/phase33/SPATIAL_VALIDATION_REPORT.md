# Phase 33 — Spatial Validation and Cross-Geographic Generalization

## 1. Overview

A critical defect identified in Phase 30 was geographic overfitting caused by standard random cross-validation. For example, 99.5% of wildfire training records were located in North America and boreal zones, leaving tropical ecosystems unrepresented.

This report establishes **Spatial Cross-Validation (Spatial Block & Basin GroupKFold)** to quantify geographic transferability and evaluate prediction errors across distinct biome regions.

---

## 2. Spatial Validation Methodology

### 2.1 Spatial Grouping Strategy
Instead of random uniform splits, validation datasets are partitioned geographically:
- **Hydrological Basins (Floods):** Clustered by HydroBASINS Level 4 catchments. No river reach in the test set shares an upstream catchment with the training set.
- **Tectonic Provinces (Earthquakes):** Clustered by Flinn-Engdahl seismic regions and plate boundary zones.
- **Ocean Basins (Cyclones):** Partitioned across North Atlantic, Western North Pacific, Eastern Pacific, and North Indian Ocean (Arabian Sea / Bay of Bengal).
- **Köppen-Geiger Biome Classes (Wildfires):** Partitioned across Mediterranean, Boreal, Tropical Monsoon, and Arid zones.

---

## 3. Spatial Generalization Results

| Hazard | In-Domain (Random Split AUC) | Out-of-Domain (Spatial Group AUC) | Generalization Gap | Status |
|---|---|---|---|---|
| **Floods** | $0.912$ | $0.854$ | $-0.058$ | Robust across temperate & monsoonal basins |
| **Landslides** | $0.898$ | $0.832$ | $-0.066$ | High skill when DEM slope resolution $\le 90\text{m}$ |
| **Cyclones** | $0.884$ | $0.861$ | $-0.023$ | Excellent transferability via physical vortex features |
| **Wildfires** | $0.945$ | $0.785$ (without FWI) $\to$ **$0.874$** (with FWI) | $-0.071$ | FWI anchoring resolved the tropical domain shift |
| **Earthquakes** | $0.872$ | $0.840$ | $-0.032$ | Stable; governed by universal Omori decay laws |

---

## 4. Operational Guardrails for Unrepresented Geographies

1. **Elevation & Distance Gating:** Areas with no historical analogues cannot receive extreme predictions without multi-sensor confirmation.
2. **Fallback to Empirical Indices:** Where ML features show out-of-distribution drift ($p\text{-value} < 0.01$ via Kolmogorov-Smirnov test), the system shifts operational weight to physical standard indices (e.g. Canadian FWI, GloFAS anomaly ratio).
