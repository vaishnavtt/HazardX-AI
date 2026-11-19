# Phase 32 — Flood Risk Calculation Methodology

## 1. Overview and Target Definition

- **Defined Physical Target:** Daily fluvial river reach overflow and surface inundation probability within a 24-hour horizon ($P(\text{Flood} \mid \text{Hydrology, Meteorology, Topography})$).
- **Primary Numerical Models:**
  - Copernicus GloFAS (Global Flood Awareness System) Continental Hydrological Routing Model (via Open-Meteo Flood API).
  - Open-Meteo High-Resolution Global Numerical Weather Prediction (ECMWF IFS / GFS).
  - Copernicus DEM 90m Topographic Wetness Index (TWI).
  - Calibrated XGBoost Fluvial Flood Occurrence Model.

---

## 2. Mathematical Formulation

### 2.1 Feature Inputs
The model consumes real-time environmental context:
- $Q(t)$: Forecast river discharge ($\text{m}^3/\text{s}$).
- $Q_{\text{ratio}} = \frac{Q(t)}{\bar{Q}_{7d}}$: Ratio of forecast discharge to 7-day climatological mean.
- $P_{1d}, P_{3d}, P_{7d}, P_{14d}$: Cumulative precipitation across 1, 3, 7, and 14 days.
- $\text{API}_{14}$: 14-day Antecedent Precipitation Index:
  $$\text{API}_{14} = 0.85 \cdot P_{1d} + 0.15 \cdot P_{14d}$$
- $\text{TWI}$: Topographic Wetness Index ($\ln(a / \tan \beta)$).
- $D_{\text{river}}$: 3D Euclidean distance to the nearest mapped hydrological drainage channel (km).

### 2.2 Bayesian Prior Calibration
The XGBoost classifier was trained on a balanced 1:1 case-control dataset ($\pi_{\text{train}} = 0.50$). The empirical annual flood probability for an arbitrary terrestrial coordinate is approximately $\pi_{\text{prior}} \approx 0.005$ (1.8 days/year).

Applying odds-ratio Bayesian inversion:
$$\text{Odds}_{\text{calibrated}} = \left(\frac{P_{\text{raw}}}{1 - P_{\text{raw}}}\right) \cdot \left(\frac{\pi_{\text{prior}}}{1 - \pi_{\text{prior}}}\right) \cdot \left(\frac{1 - \pi_{\text{train}}}{\pi_{\text{train}}}\right)$$
$$P_{\text{calibrated}} = \frac{\text{Odds}_{\text{calibrated}}}{1 + \text{Odds}_{\text{calibrated}}}$$

### 2.3 Physical Hydrological Overrides
- **Dry Season Constraint:** When $P_{3d} < 5.0\text{ mm}$ and $Q_{\text{ratio}} \le 1.1$, $P_{\text{calibrated}}$ is bounded strictly below $0.001$ ($0.1\%$).
- **Extreme Flow Trigger:** When $Q_{\text{ratio}} \ge 3.5$ or $P_{24h} \ge 150.0\text{ mm}$, alert level escalates directly to `ORANGE` or `RED`.

---

## 3. Wayanad, Kerala Validation

Under prevailing dry weather ($P_{24h} = 0.0\text{ mm}$, GloFAS $Q = 0.4\text{ m}^3/\text{s}$, $Q_{\text{ratio}} = 0.92$):
- Raw model score: $0.092$
- **Calibrated event probability:** $0.0005$ ($0.05\%$)
- **Alert Level:** `GREEN`
- **Risk Category:** `LOW`
- **Output:** "Normal baseline conditions; no immediate hazard advisory."
