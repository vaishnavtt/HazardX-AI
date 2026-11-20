# Phase 37 — Earthquake Hazard Validation & Seismological Audit

## 1. Audit of the 250 km Radius and Mw 4.0 Threshold

In `forecast_service.py` (lines 508–522):
- The service queried earthquakes with $M \ge 3.5$ up to $250\text{ km}$ away.
- It filtered for mainshocks with $M_w \ge 4.0$.
- In `spatial_feature_service.py` (lines 135–145), the radius checked was $100\text{ km}$.

### 1.1 Seismological Flaw: Absence of Spatial Distance Decay
According to empirical rupture physics (Wells & Coppersmith, 1994; Kagan, 2002; Felzer & Brodsky, 2006):
- An $M_w 4.0$ earthquake has an average rupture length of $L \approx 0.6\text{ km}$ to $1.2\text{ km}$.
- An $M_w 5.0$ earthquake has an average rupture length of $L \approx 3.0\text{ km}$ to $4.5\text{ km}$.
- Aftershocks are concentrated within $1 - 2$ rupture lengths of the mainshock fault plane. Beyond $30\text{ km}$ for an M4–M5 event, aftershock spatial density drops by over three orders of magnitude.

**Critical Finding:** `OmoriAftershockForecaster` in `omori_aftershock_model.py` implements pure temporal Omori-Utsu decay:
$$\Lambda(\Delta t) = \int_t^{t+\Delta t} \frac{10^{a + b(M_m - M_{\text{target}})}}{(t + c)^p} dt$$
It does **not** include a spatial attenuation kernel $\rho(r)$. As a consequence, if an $M_w 4.5$ mainshock occurs $240\text{ km}$ away from a city, the platform calculates the same $18\%$ aftershock probability for that city as if the epicenter were directly beneath city hall!

Applying sequence-wide Poisson probabilities uniformly across a $250\text{ km}$ circle without spatial distance weighting ($\propto r^{-\gamma}$) is physically indefensible.

---

## 2. Omori-Utsu vs. Reasenberg-Jones Implementation

- The implementation in `omori_aftershock_model.py` correctly adopts the Reasenberg & Jones (1989, 1994) formula with parameters $a = -1.67$, $b = 1.00$, $p = 1.05$, $c = 0.05\text{ days}$.
- However, line 51 clamped the probability to:
  `prob = max(0.0001, min(0.9999, prob))`
  This prevented the model from ever returning a true $0.0000$ when no qualifying events occurred, requiring downstream services to manually override the output to 0.0.

---

## 3. Separation of Earthquake Hazard Dimensions

The platform must explicitly present three distinct seismological layers:
1. **Regional Baseline Seismic Hazard (Long-Term Susceptibility):**
   - Driven by GEM (Global Earthquake Model) active fault distance, fault slip rate, tectonic regime, and historical seismicity rate ($a$ and $b$ values).
   - This baseline hazard does NOT become zero merely because no earthquake happened this week.
2. **Recent Regional Seismicity (Observational):**
   - 7-day, 30-day, and 365-day earthquake counts within $100\text{ km}$ from USGS ComCat.
3. **Conditional Aftershock Probability (Short-Term Event):**
   - Evaluated *only* when an $M_w \ge 4.5$ mainshock has ruptured within the physically justifiable rupture zone ($R \le 20\text{ km}$ for M4.5, $R \le 50\text{ km}$ for M6.0, $R \le 100\text{ km}$ for M7.0+).
   - Distance attenuation kernel must scale aftershock probability with distance from the epicenter.
