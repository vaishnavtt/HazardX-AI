# Phase 36 — Wayanad Regression Test and Invariant Report

## 1. Objective

To prevent future engineering regressions, this report codifies five **Mathematical Invariants** that must hold for Wayanad, Kerala ($11.6854^\circ\text{N}, 76.1320^\circ\text{E}$) under ambient dry/typical weather.

---

## 2. Invariant Definitions & Test Assertions

### Invariant 1: Quiescent Earthquake Precondition
$$\text{If } \max_{e \in \text{USGS}(250\text{km})} M_w(e) < 4.0 \implies P(\text{Aftershock}) = 0.00 \land \text{RiskCategory} = \text{"QUIESCENT"}$$
- **Verification:** Fault distance is $1410.1\text{ km}$; 0 events detected.
- **Status:** **PASS** ($P = 0.00\%$, `GREEN`).

### Invariant 2: Canadian FWI Danger Anchoring
$$\text{If } \text{FWI} < 5.2 \land N_{\text{FIRMS}}(50\text{km}) = 0 \implies \text{RiskCategory} = \text{"LOW"} \land P(\text{Wildfire}) \le 0.01$$
- **Verification:** Current $\text{FWI} = 1.0$; 0 FIRMS hotspots detected.
- **Status:** **PASS** ($P = 0.32\%$, `GREEN`).

### Invariant 3: Inland Highland Cyclone Gate
$$\text{If } \text{Elevation} > 300\text{ m} \land D_{\text{cyclone}} > 800\text{ km} \implies P(\text{Cyclone}) = 0.00 \land V_{\text{wind}} = 0\text{ kt}$$
- **Verification:** Elevation is $765\text{ m}$; 0 active storms within 800 km.
- **Status:** **PASS** ($P = 0.00\%$, `GREEN`).

### Invariant 4: Dry Weather Flood & Landslide Decoupling
$$\text{If } P_{24h} = 0.0\text{ mm} \land Q_{\text{ratio}} \le 1.1 \implies P(\text{Flood}) < 0.01 \land P(\text{Landslide}) < 0.01$$
- **Verification:** $P_{24h} = 0.0\text{ mm}$; GloFAS $Q_{\text{ratio}} = 0.92$.
- **Status:** **PASS** ($P_{\text{flood}} = 0.05\%$, $P_{\text{landslide}} = 0.02\%$).

### Invariant 5: Composite Alert Integrity
$$\text{Composite Alert Level} = \max_{h} \text{Alert}(h) = \text{GREEN}$$
- **Verification:** All 5 individual hazards resolve to `GREEN`.
- **Status:** **PASS** (Composite Alert = `GREEN`).

---

## 3. Automated Regression Guard

These invariants are codified directly into the automated CI test pipeline in `backend/tests/test_geospatial.py` and `backend/tests/test_forecasts.py`. Any code modification that causes Wayanad to regress to false high risk will fail the build immediately.
