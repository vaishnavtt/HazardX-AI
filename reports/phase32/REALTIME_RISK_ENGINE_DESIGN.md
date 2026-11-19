# Phase 32 — Real-Time Hazard Risk Calculation Engine Design

## Executive Summary

Phase 32 redesigns the real-time hazard risk calculation architecture across all five natural hazard domains (Floods, Landslides, Earthquakes, Cyclones, Wildfires) in HAZARDX AI. Previously, uncalibrated raw machine learning scores (trained on balanced 1:1 case-control datasets) and ungated physical assumptions produced anomalous risk assessments for locations with low natural risk—most notably Wayanad, Kerala (11.6854, 76.1320), where dry, benign conditions generated false "Wildfire: HIGH (60%)" and "Earthquake aftershock: QUIESCENT (18%)" warnings.

The upgraded risk calculation engine enforces:
1. **Mathematical separation between static environmental susceptibility and short-term event probability.**
2. **Strict physical gating mechanisms** that prevent the invocation or interpretation of event models when underlying necessary physical preconditions do not exist.
3. **Bayesian prior odds calibration** transforming balanced classification scores into true empirical occurrence probabilities.
4. **Standardized international index coupling** (such as the Canadian Forest Fire Weather Index for wildfires and Omori-Utsu statistical decay for earthquakes).
5. **Multi-source live data integration** combining numerical weather prediction (Open-Meteo), continental hydrological routing (Copernicus GloFAS), satellite thermal anomaly detection (NASA FIRMS), global active fault catalogs (GEM), and live seismicity feeds (USGS ComCat).

---

## Architectural Workflow

```
   ┌────────────────────────────────────────────────────────┐
   │             Live Coordinate Ingestion                  │
   │               (Latitude, Longitude)                    │
   └───────────────────────────┬────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
 ┌──────────────────────┐             ┌──────────────────────┐
 │ Environmental & Live │             │   Physical Gating    │
 │ Data Ingestion:      │             │   Pre-Condition Check│
 │ - Open-Meteo NWP     │             │ - Quiescent Seismicity│
 │ - Copernicus GloFAS  │             │ - Inland/Basin Storm │
 │ - NASA FIRMS Thermal │             │ - Rain Trigger Check │
 │ - USGS Seismicity    │             └──────────┬───────────┘
 └──────────┬───────────┘                        │
            │                                    │
            ▼                                    ▼
 ┌──────────────────────────────────────────────────────────┐
 │         Domain-Specific Predictive Services:             │
 │                                                          │
 │  1. Flood Service: GloFAS Q-anomaly + NWP + DEM          │
 │  2. Landslide Service: 3-day Antecedent Rain + Slope     │
 │  3. Wildfire Service: Canadian FWI + NASA FIRMS Coupling │
 │  4. Earthquake Service: Omori Decay (Only if M >= 4.0)   │
 │  5. Cyclone Service: Saffir-Simpson (Only if within 800km│
 └──────────────────────────┬───────────────────────────────┘
                            │
                            ▼
 ┌──────────────────────────────────────────────────────────┐
 │     Bayesian Prior Odds & Empirical Calibration          │
 │  P_calibrated = (P_raw * Prior) / [P_raw * Prior + ...]  │
 └──────────────────────────┬───────────────────────────────┘
                            │
                            ▼
 ┌──────────────────────────────────────────────────────────┐
 │       Multi-Horizon Synthesis & Composite Engine         │
 │     (6h, 12h, 24h, 48h, 72h) -> Overall Alert Level      │
 └──────────────────────────────────────────────────────────┘
```

---

## Core Engineering Principles

### 1. Separation of Susceptibility vs. Short-Term Event Probability
- **Susceptibility ($S \in [0, 1]$):** Measures intrinsic geospatial terrain and geologic predisposition (e.g. slope angle, topographic wetness index, fault proximity). Susceptibility does not change day-to-day.
- **Trigger Dynamic ($T(t) \in [0, 1]$):** Measures transient atmospheric or seismic energy injection (e.g. 72h cumulative precipitation, river discharge anomaly ratio, fire weather index, mainshock rupture).
- **Short-Term Probability ($P(\text{Event} \mid S, T)$):** A joint function where $P \to 0$ whenever $T(t) \to 0$, regardless of high baseline susceptibility $S$. In Wayanad, steep terrain confers moderate landslide susceptibility, but zero rain produces an event probability of $< 0.05\%$.

### 2. Physical Gating Pre-Conditions
To prevent pseudo-predictions generated from default or uninitialized values:
- **Earthquake Aftershock:** Gated by `mainshock_mag >= 4.0` within 250 km. If no mainshock occurred, aftershock probability is locked to `0.0%`, status is `QUIESCENT`, alert is `GREEN`.
- **Tropical Cyclone:** Gated by distance to active storm center $\le 800\text{ km}$ and elevation $\le 300\text{ m}$. Inland highland locations automatically resolve to `0.0%` cyclonic wind threat.
- **Wildfire:** Gated by Canadian Forest Fire Weather Index (FWI) danger scale and active thermal anomaly verification via NASA FIRMS satellite observations.

### 3. Clear Target Definition
Every hazard risk calculation explicitly documents:
- **Defined Target:** The exact physical phenomenon evaluated (e.g., "River Inundation & Reach Overflow (24h horizon)", "P(M >= 4.5 Aftershock Sequence | Qualifying Mainshock, 30d/100km)").
- **Confidence / Uncertainty:** Quantitative confidence metric or statistical model attribution.
- **Data Sources & Freshness:** Explicit list of operational data providers (e.g. Copernicus GloFAS, Open-Meteo, USGS, NASA FIRMS).
