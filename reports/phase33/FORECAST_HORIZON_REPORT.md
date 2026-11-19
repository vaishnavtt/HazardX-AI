# Phase 33 — Forecast Horizon Optimization and Lead-Time Dynamics

## 1. Overview

Each forecast horizon serves distinct emergency management and civil defense operational objectives:

```
   Tactical Operations             Operational Preparation           Strategic Readiness
 ┌──────────────────────┐         ┌────────────────────────┐       ┌───────────────────────┐
 │       6h / 12h       │         │          24h           │       │       48h / 72h       │
 │ - Flash flood egress │  ───►   │ - Levee deployment     │  ──►  │ - Emergency staging   │
 │ - Immediate sheltering│        │ - Pre-emptive warning  │       │ - Civil defense alert │
 │ - Fire crew dispatch │         │ - Shelter activation   │       │ - Regional stockpiles │
 └──────────────────────┘         └────────────────────────┘       └───────────────────────┘
```

---

## 2. Lead-Time Uncertainty Characterization

### 2.1 Atmospheric vs. Earth Surface Variance
- **Atmospheric Hazards (Cyclones, Wildfires, Inundation):** Forecast entropy expands non-linearly after 36 hours due to chaos in Eulerian NWP integrations. At 72h, uncertainty bounds on precipitation accumulation typically reach $\pm 35\%$.
- **Geomorphic Hazards (Landslides):** Hysteresis in soil pore-water pressure delays slope failure, meaning the 12h–24h horizon is often more predictive than the 6h horizon for deep-seated slides.
- **Seismic Hazard (Aftershocks):** Aftershock frequency is highest immediately following the mainshock ($t < 6\text{h}$) and decays as $1/t$. Uncertainty is smallest at short horizons and broadens over 72h due to secondary branching.

---

## 3. Recommended Operational Thresholds by Horizon

| Horizon | Flood Trigger ($Q_{\text{ratio}}$) | Landslide Trigger ($P_{\text{cum}}$) | Wildfire Trigger (FWI) | Cyclone Warning ($V_{\text{sustained}}$) |
|---|---|---|---|---|
| **6 Hours** | $\ge 1.8\text{x}$ normal | $\ge 40\text{ mm}$ | $\ge 25.0$ | $\ge 45\text{ kt}$ within $100\text{ km}$ |
| **12 Hours** | $\ge 2.2\text{x}$ normal | $\ge 70\text{ mm}$ | $\ge 21.3$ | $\ge 50\text{ kt}$ within $250\text{ km}$ |
| **24 Hours** | $\ge 2.5\text{x}$ normal | $\ge 100\text{ mm}$ | $\ge 18.0$ | $\ge 64\text{ kt}$ within $400\text{ km}$ |
| **48 Hours** | $\ge 3.0\text{x}$ normal | $\ge 160\text{ mm}$ | $\ge 15.0$ | $\ge 75\text{ kt}$ within $600\text{ km}$ |
| **72 Hours** | $\ge 3.5\text{x}$ normal | $\ge 220\text{ mm}$ | $\ge 12.0$ | $\ge 85\text{ kt}$ within $800\text{ km}$ |
