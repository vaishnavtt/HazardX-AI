# Phase 32 — Composite Multi-Hazard Risk Methodology

## 1. Overview and Design Principles

The composite risk engine synthesizes risk assessments across all five independent natural hazards into a coherent, unambiguous regional alert level (`GREEN`, `YELLOW`, `ORANGE`, `RED`).

### 1.1 Non-Compensatory Risk Aggregation
Disaster risk is non-compensatory: a low flood risk does not cancel out an extreme wildfire danger.
$$\text{Composite Risk} = \max_{h \in \text{Hazards}} \text{RiskScore}(h)$$

### 1.2 Multi-Tier Severity Hierarchy
Alert levels correspond to standard civil protection color codes:
- **GREEN (Normal / Quiescent):** All hazards $\le 0.19$, or quiescent physical state. Routine daily life; no active hazard advisory.
- **YELLOW (Advisory / Elevated):** At least one hazard $\in [0.20, 0.39]$. Precautionary awareness.
- **ORANGE (Severe / Warning):** At least one hazard $\in [0.40, 0.59]$. Heightened vigilance; prepare mitigation measures.
- **RED (Extreme / Critical):** At least one hazard $\ge 0.60$. Critical hazard impending or occurring.

---

## 2. Multi-Hazard Interaction Matrix

| Primary Hazard | Secondary Cascading Hazard | Interaction Mechanism |
|---|---|---|
| **Cyclone** | **Flood** | Extreme cyclonic rainfall induces rapid river surcharge and storm surge. |
| **Cyclone** | **Landslide** | Heavy precipitation destabilizes saturated mountain slopes in coastal ranges. |
| **Flood** | **Landslide** | Toe-slope fluvial erosion undermines slope foot, inducing mass movement. |
| **Earthquake** | **Landslide** | Seismic ground acceleration fractures rock masses, causing coseismic slides. |
| **Wildfire** | **Landslide / Debris Flow** | Post-wildfire hydrophobicity and canopy loss exacerbate runoff and debris flows. |

---

## 3. Wayanad, Kerala Composite Assessment Summary

- **Location:** Wayanad, Kerala ($11.6854, 76.1320$, Elevation $765\text{ m}$)
- **Flood Risk:** $0.05\%$ (`GREEN` / `LOW`)
- **Landslide Risk:** $0.02\%$ (`GREEN` / `LOW`)
- **Earthquake Risk:** $0.00\%$ (`GREEN` / `QUIESCENT`)
- **Wildfire Risk:** $0.32\%$ (`GREEN` / `LOW`)
- **Cyclone Risk:** $0.00\%$ (`GREEN` / `LOW`)
- **Composite Score:** $0.0032$ ($0.32\%$)
- **Overall Alert Level:** `GREEN`
- **Scientific Conclusion:** Under ambient sunny/dry weather, the Wayanad region correctly resolves to an all-clear green status, completely eliminating the previously reported false alarms.
