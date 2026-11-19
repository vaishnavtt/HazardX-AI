# Phase 32 — Earthquake Risk Calculation Methodology

## 1. Scientific Governance & Objective Notice

> [!IMPORTANT]
> **Deterministic Earthquake Prediction:** Predicting the exact time, location, and magnitude of future earthquakes is scientifically impossible with current physical knowledge and is strictly prohibited in HAZARDX AI.
> 
> The HAZARDX AI earthquake module provides **probabilistic aftershock decay forecasting** based on empirical seismological physical laws (Omori-Utsu and Reasenberg-Jones) following an observed mainshock, combined with static GEM active fault distance metrics.
> 
> Quarantined models (specifically `aftershock_count` regression with negative test $R^2 = -0.0401$) remain strictly suppressed.

---

## 2. Methodology & Physical Gating

### 2.1 USGS Live Seismicity Ingestion
The system connects via FDSNWS to the USGS Comprehensive Earthquake Catalog (ComCat):
- Queries all events with $M \ge 3.5$ occurring within $250\text{ km}$ of the target coordinate over the past 30 days.
- Retrieves hypocentral depth, event timestamp, and moment magnitude ($M_w$).

### 2.2 Physical Gating Logic
An aftershock sequence physically requires a preceding mainshock:
1. If no earthquake with $M_w \ge 4.0$ occurred within $250\text{ km}$:
   - **Status:** `QUIESCENT`
   - **Hazard Probability:** `0.00%`
   - **Expected M4+ Aftershock Count:** `0.00`
   - **Alert Level:** `GREEN`
   - **Guidance:** "No qualifying seismic mainshock (M >= 4.0) observed within 250 km. Tectonically quiescent background state."
2. If a qualifying mainshock ($M_w \ge 4.0$) occurred:
   - Evaluate Modified Omori-Utsu aftershock decay rate:
     $$\lambda(t) = \frac{K}{(t + c)^p}$$
     where standard regional decay parameters are $p = 1.05$, $c = 0.05\text{ days}$.
   - Estimate non-homogeneous Poisson probability of aftershock with $M \ge M_{\text{target}}$ over horizon $\Delta t$:
     $$P(N \ge 1) = 1 - \exp\left(-\int_{t_1}^{t_2} \lambda(t) \cdot 10^{-b(M_{\text{target}} - M_{\text{main}})} dt\right)$$

---

## 3. Wayanad, Kerala Validation

In Wayanad, Kerala ($11.6854, 76.1320$):
- **Nearest Active Fault:** $1410.1\text{ km}$ away (GEM catalog).
- **Recent Seismicity ($M \ge 3.5$ within 250 km):** `0 events detected`.
- **Pre-Fix Bug:** Previously, the system defaulted `mainshock_mag = 4.5` and injected synthetic shaking, displaying "QUIESCENT – 18%".
- **Post-Fix Output:**
  - `mainshock_mag = 0.0`
  - `hazard_score = 0.0`
  - `prob_m4_plus = 0.0%`
  - `alert_level = GREEN`
  - `risk_category = QUIESCENT`
