# Phase 32 — Landslide Risk Calculation Methodology

## 1. Overview and Target Definition

- **Defined Physical Target:** Rainfall-induced shallow hillslope failure or debris flow occurrence within a 24-hour window ($P(\text{Landslide} \mid \text{Terrain, Antecedent Moisture, Trigger Rain})$).
- **Primary Data Sources:**
  - Copernicus DEM (90m global digital elevation model) terrain slope, aspect, and plan curvature.
  - Open-Meteo High-Resolution Multi-Hour NWP precipitation and topsoil volumetric water content ($\text{m}^3/\text{m}^3$).
  - NASA Global Landslide Catalog (GLC) historical inventory baseline.
  - Calibrated XGBoost Hillslope Susceptibility Model.

---

## 2. Mathematical Separation: Susceptibility vs. Trigger

### 2.1 Static Geomorphic Susceptibility ($S_{\text{geo}}$)
Topographic slope is the fundamental resisting/driving stress determinant:
- Slopes $< 10^\circ$: Planar lowlands; gravity-induced shear failure is geophysically negligible ($S_{\text{geo}} \to 0$).
- Slopes $10^\circ - 25^\circ$: Moderate rolling hills; requires saturated pore pressure or high rainfall intensities.
- Slopes $> 25^\circ$: Steep mountainous escarpments (e.g. Western Ghats); high intrinsic geomorphic susceptibility.

### 2.2 Dynamic Hydrological Trigger ($T_{\text{hydro}}$)
Rainfall infiltration reduces effective normal stress ($\sigma' = \sigma - u$) across the potential slip surface.
- $\text{API}_{30} = 0.90 \cdot P_{1d} + 0.10 \cdot P_{30d}$
- Soil Volumetric Moisture: $\theta_{\text{soil}} \in [0.10, 0.45]\text{ m}^3/\text{m}^3$

### 2.3 Physical Gating and Joint Probability
A landslide cannot initiate without either a seismic shock ($PGA > 0.15\text{g}$) or a hydrological infiltration trigger.
$$\text{If } P_{72h} < 10.0\text{ mm} \implies P(\text{Landslide Trigger} \mid \text{Dry Day}) < 0.0005$$

Applying Bayesian prior odds calibration on the balanced 1:1 training dataset with terrestrial background prior $\pi_{\text{prior}} \approx 0.002$:
$$P_{\text{calibrated}} = \frac{P_{\text{raw}} \cdot \pi_{\text{prior}}}{P_{\text{raw}} \cdot \pi_{\text{prior}} + (1 - P_{\text{raw}}) \cdot (1 - \pi_{\text{prior}})}$$

---

## 3. Wayanad, Kerala Validation

In Wayanad, Kerala ($11.6854, 76.1320$):
- **Terrain Slope:** $5.9^\circ$ (gentle valley bench, below critical $25^\circ$ failure threshold).
- **Current Rainfall:** $0.0\text{ mm}$ (dry atmospheric conditions).
- **Raw ML Model Score:** $0.081$ (reflecting baseline tropical soil taxonomy).
- **Calibrated Event Probability:** $0.0002$ ($0.02\%$).
- **Alert Level:** `GREEN` / `LOW`.
- **Contrast with Disaster Conditions (July 30, 2024):**
  - When $P_{48h} = 572\text{ mm}$ and slope $> 30^\circ$, calibrated probability jumps to $> 0.92$, triggering `RED` / `EXTREME` alert.
