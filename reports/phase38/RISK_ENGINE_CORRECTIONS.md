# HAZARDX AI — RISK ENGINE CORRECTIONS & OVERHAUL REPORT
**Document ID:** `HX-RPT-PH38-05`  
**Phase:** Phase 38 — Model, Data & Risk Engine Improvements  
**Author:** Lead Disaster Risk Scientist & Software Systems Engineer  
**Date:** November 20, 2026  
**Status:** COMPLETED & INTEGRATED  

---

## 1. Executive Summary

This report documents the mathematical formulations, algorithmic adjustments, and architectural corrections integrated into the HAZARDX AI risk engine during Phase 38. These modifications eliminate ad-hoc heuristics and replace them with physically based, internationally recognized disaster risk formulations.

---

## 2. Summary of Core Corrections

```
┌───────────────────────────┬───────────────────────────────────┬──────────────────────────────────────┐
│ Hazard Module             │ Pre-Phase 38 Mechanism            │ Phase 38 Overhauled Formulation      │
├───────────────────────────┼───────────────────────────────────┼──────────────────────────────────────┤
│ 1. Wildfire Weather       │ Compressed polynomial proxy       │ Authentic Van Wagner (1987) / EFFIS  │
│                           │ (Ceiling: 12.37)                  │ Canadian FWI System (Scale: 0 - 120) │
├───────────────────────────┼───────────────────────────────────┼──────────────────────────────────────┤
│ 2. Earthquake Aftershock  │ Spatial-blind Omori temporal decay│ Reasenberg-Jones Temporal Decay +    │
│                           │ (Uniform across 250 km)           │ Kagan Wells-Coppersmith Spatial Decay│
├───────────────────────────┼───────────────────────────────────┼──────────────────────────────────────┤
│ 3. Landslide Delay        │ Instantaneous 24h precipitation   │ Coupled Slope-Saturation Hysteresis  │
│                           │ (Zero rain = Zero risk)           │ (Residual pore-water pressure lag)   │
├───────────────────────────┼───────────────────────────────────┼──────────────────────────────────────┤
│ 4. Flood Reach Flow       │ Static topographic depression     │ GloFAS Discharge Ratio Coupling      │
│                           │ (River proximity false alarms)    │ (Q / Q_7d baseline normalization)    │
├───────────────────────────┼───────────────────────────────────┼──────────────────────────────────────┤
│ 5. Cyclone Assessment     │ Hardcoded elevation cutoff        │ Active Storm Proximity Buffer        │
│                           │ (elevation <= 300m blind spot)    │ (D_storm <= 1000 km + NWP Wind Speed)│
└───────────────────────────┴───────────────────────────────────┴──────────────────────────────────────┘
```

---

## 3. Detailed Formulations & Implementations

### 3.1 Wildfire: Canadian Forest Fire Weather Index (FWI)
Implemented in `backend/app/integrations/weather_client.py`:
- Calculates Equilibrium Moisture Content ($\text{EMC}$) from ambient temperature $T$ and relative humidity $H$.
- Computes Fine Fuel Moisture Content ($\text{FFMC}$) with exponential drying rates influenced by wind speed $W$.
- Derives Initial Spread Index ($\text{ISI}$) combining wind propagation $f(W) = e^{0.05039 W}$ and fuel moisture $f(m)$.
- Derives Fire Weather Index ($\text{FWI}$), restoring full dynamic range up to 120.0+.

### 3.2 Earthquake: Spatial-Temporal Omori-Utsu Formulation
Implemented in `backend/app/forecasting/omori_aftershock_model.py`:
- Temporal rate: $\lambda(t) = 10^{a + b(M_m - M_{\text{target}})} (t + c)^{-p}$
- Rupture length scaling: $r_0(M_m) = \max(2.0, 10^{-2.0 + 0.5 M_m})\text{ km}$
- Spatial attenuation kernel:
  $$\rho(r) = \frac{1}{1 + \left(\frac{r}{r_0}\right)^2}$$
- Expected count: $\Lambda(t, \Delta t, r) = \int_t^{t+\Delta t} \lambda(\tau) d\tau \times \rho(r)$
- Poisson probability:
  $$P(N \ge 1) = \begin{cases} 0.0 & \text{if } M_m < 4.0 \text{ or } \Lambda < 10^{-6} \\ 1 - e^{-\Lambda} & \text{otherwise} \end{cases}$$

### 3.3 Landslide: Slope-Saturation Hysteresis
Implemented in `backend/app/services/landslide_service.py`:
- Checks topographic steepness ($\theta \ge 20^\circ$) and antecedent saturation ($P_{7d} \ge 100\text{ mm}$ or $P_{30d} \ge 250\text{ mm}$).
- If saturated steep terrain experiences a 24-hour rainfall lull ($P_{1d} < 5\text{ mm}$), the alert level is maintained at `MODERATE` (`YELLOW`) with clear attribution: *"Antecedent hillslope saturation override active: high cumulative rainfall creates residual landslide hazard despite low 24h precipitation."*
- If terrain is flat ($\theta < 10^\circ$), alert is prevented from escalating to false warnings.

### 3.4 Flood: River Channel Discharge Reconciliation
Implemented in `backend/app/services/flood_service.py`:
- Ingests Copernicus GloFAS river discharge anomaly ratio $\Delta Q = Q / \bar{Q}_{7d}$.
- When $\Delta Q \le 1.25$ and $P_{3d} < 15\text{ mm}$ and $P_{1d} < 5\text{ mm}$, alert is harmonized to `LOW` (`GREEN`), preventing river basin topography alone from triggering false flood alarms during prolonged dry periods.
- When $\Delta Q \ge 2.0$ or $P_{1d} \ge 75\text{ mm}$, risk is elevated to `HIGH` (`ORANGE`).

### 3.5 Cyclone: Active Storm Proximity Gating
Implemented in `backend/app/api/v1/endpoints/geospatial.py` & `spatial_feature_service.py`:
- Replaced the brittle elevation gate (`elevation_m <= 300.0`) with active basin cyclone proximity tracking:
  $$D_{\text{storm}} = \min_{s \in \text{Storms}} \text{GeodeticDistance}((\text{lat}, \text{lon}), (s_{\text{lat}}, s_{\text{lon}}))$$
- If $D_{\text{storm}} \le 1000\text{ km}$, cyclonic intensity and rapid intensification models evaluate the synoptic wind and pressure field.
- If $D_{\text{storm}} > 1000\text{ km}$, assessment returns baseline `LOW` (`GREEN`) with explicit distance reporting (e.g. *"Nearest active cyclonic system is 4200 km away"*).

---

## 4. Verification Sign-Off

All risk engine modifications have been implemented in production backend services and verified with unit and regression tests.
