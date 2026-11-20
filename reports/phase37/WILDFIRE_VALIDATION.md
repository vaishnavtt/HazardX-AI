# Phase 37 — Wildfire Hazard Validation & FWI Implementation Audit

## 1. Audit of the Fire Weather Index (FWI) Implementation

In `backend/app/integrations/weather_client.py` (lines 321–330), the FWI is computed as:
```python
def _calc_horizon_fwi(self, temp_c: float, rh_pct: float, wind_ms: float, cum_precip_mm: float) -> float:
    wind_kmh = wind_ms * 3.6
    precip_discount = max(0.2, 1.0 - (cum_precip_mm / 10.0))
    exponent = -0.450 - (0.0345 * rh_pct) + (0.0338 * temp_c) + (0.0234 * wind_kmh)
    raw_fwi = 2.0 * math.exp(max(-3.0, min(4.0, exponent))) * precip_discount
    return max(0.5, min(100.0, raw_fwi))
```

### 1.1 Mathematical & Physical Discrepancy
The Canadian Forest Fire Weather Index (FWI) System (Van Wagner, 1987) consists of six interconnected components:
1. **Fine Fuel Moisture Code (FFMC):** Represents moisture of litter and fine fuels.
2. **Duff Moisture Code (DMC):** Represents moisture of loosely compacted decomposing organic layers.
3. **Drought Code (DC):** Represents deep, compact organic layers and seasonal drought.
4. **Initial Spread Index (ISI):** Combines wind speed and FFMC to model rate of fire spread.
5. **Buildup Index (BUI):** Combines DMC and DC to represent total fuel available.
6. **Fire Weather Index (FWI):** Combines ISI and BUI to represent fire intensity.

The equation implemented in `weather_client.py` is a single-step exponential proxy inspired by McArthur formulas, but it is **not** the Canadian FWI system.

### 1.2 Numerical Range Mismatch
Testing this proxy under extreme wildfire conditions:
- **Diablo / Santa Ana Windstorm ($T = 38^\circ\text{C}$, $\text{RH} = 8\%$, $\text{Wind} = 15\text{ m/s}$ / $54\text{ km/h}$, $P = 0\text{ mm}$):**
  $$\text{exponent} = -0.450 - (0.0345 \times 8) + (0.0338 \times 38) + (0.0234 \times 54) = +1.8218$$
  $$\text{raw\_fwi} = 2.0 \times e^{1.8218} = 12.37$$

In `wildfire_service.py`, the risk categorization thresholds were set to:
- $\text{FWI} < 5.2$: `LOW`
- $5.2 \le \text{FWI} < 11.2$: `MODERATE`
- $11.2 \le \text{FWI} < 21.3$: `HIGH`
- $21.3 \le \text{FWI} < 38.0$: `VERY HIGH`
- $\text{FWI} \ge 38.0$: `SEVERE_CRITICAL`

**Critical Finding:** Under a catastrophic California firestorm with hurricane-force desert winds and 8% humidity, the proxy formula generates a value of only **$12.37$**, which categorizes the hazard as merely `HIGH` ($11.2 - 21.3$) rather than `SEVERE_CRITICAL` ($\ge 38.0$). The proxy scale is compressed by a factor of $\approx 3.5\times$ relative to the standard Canadian FWI scale.

---

## 2. Active Fire Detections vs. Ignition Potential

In Phase 32, radial querying of NASA FIRMS satellite thermal anomalies was introduced:
`active_fires = await nasa_firms_client.get_active_fires_near(lat, lon, radius_km=50.0)`

### 2.1 The Conceptual Conflation
- **NASA FIRMS detects thermal radiative emissions from fires ALREADY IGNITED.**
- **Wildfire early warning systems model the probability of FUTURE IGNITION and SPREAD.**

Treating the absence of active satellite detections as proof that a region has low fire risk is scientifically invalid: every devastating wildfire started at a moment when NASA FIRMS detected 0 active fires in that county. Satellite observations verify current fire existence, but cannot replace fuel dryness and ignition potential.

---

## 3. Separation of Wildfire Hazard Dimensions

To achieve scientific defensibility, HAZARDX AI must explicitly separate:
1. **Fire Weather Danger (Atmospheric):** Continuous fuel drying capacity driven by temperature, vapor pressure deficit (VPD), relative humidity, and wind.
2. **Fuel & Vegetation Susceptibility (Terrestrial):** Fuel bed presence, canopy type, dead fuel moisture, and cure state. A desert rock plateau or urban center cannot sustain forest crown fires regardless of high temperature.
3. **Active Fire Incident Status (Observational):** Real-time NASA FIRMS VIIRS/MODIS thermal anomalies indicating active combustion.
4. **Ignition Probability (Predictive):** Joint likelihood of human/lightning spark interacting with receptive fine fuel.
