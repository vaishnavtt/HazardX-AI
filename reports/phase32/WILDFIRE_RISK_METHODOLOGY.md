# Phase 32 — Wildfire Risk Calculation Methodology

## 1. Overview and Target Definition

- **Defined Physical Target:** Daily wildfire ignition susceptibility and propagation danger within a 24-hour horizon ($P(\text{Ignition} \mid \text{Atmospheric Moisture, Fuel Dryness, Wind})$).
- **Primary Data Sources:**
  - Canadian Forest Fire Weather Index (FWI) System (standard international physical benchmark).
  - NASA FIRMS (Fire Information for Resource Management System) Near Real-Time MODIS/VIIRS Active Fire Thermal Hotspot Detections.
  - Open-Meteo High-Resolution Global NWP (temperature, relative humidity, 10m wind speed, cumulative rain).
  - Quarantined Models: Fire duration model remains strictly blocked ($R^2 = -214.75$).

---

## 2. Root Cause Analysis & Resolution of Wayanad False Alarm

### 2.1 The Wayanad 60% Wildfire Anomaly
In Wayanad, Kerala ($11.6854, 76.1320$), ambient weather showed $T = 26.5^\circ\text{C}$, $\text{RH} = 49\%$, $\text{FWI} = 0.7$, and zero active fires. Yet HAZARDX AI reported:
`Wildfire: HIGH – 60%`

### 2.2 Root Causes
1. **Synthetic Training Data Shift:** The training script `build_wildfire_dataset.py` sampled fire temperatures from $\mathcal{N}(32.5, 5.0)$ and non-fire from $\mathcal{N}(18.0, 6.0)$. Only 3 out of 600 non-fire samples had $T > 28^\circ\text{C}$. The XGBoost trees learned that any temperature $> 25^\circ\text{C}$ strongly implied a wildfire (+2.08 SHAP value).
2. **Ignored Physics:** The Canadian FWI was computed as $0.7$ (which belongs to the lowest danger category), but the service completely bypassed the FWI danger rating and displayed the raw uncalibrated ML score.
3. **Absence of Ground Truth Active Fire Verification:** NASA FIRMS satellite observations were not radially checked around the target coordinate.

### 2.3 The Solution Architecture
1. **Standard Canadian Forest FWI Danger Scale Integration:**
   - $\text{FWI} < 5.2$: **LOW (GREEN)**. Fine fuel moisture is high; ignition probability $< 0.5\%$.
   - $5.2 \le \text{FWI} < 11.2$: **MODERATE (YELLOW)**. Normal precautions.
   - $11.2 \le \text{FWI} < 21.3$: **HIGH (ORANGE)**. Dry fine fuels; rapid spread possible.
   - $21.3 \le \text{FWI} < 38.0$: **VERY HIGH (ORANGE)**. Extreme dryness.
   - $\text{FWI} \ge 38.0$: **EXTREME (RED)**. Critical fire spread conditions.
2. **Radial NASA FIRMS Integration:**
   `nasa_firms_client.get_active_fires_near(lat, lon, radius_km=50.0)` queries satellite thermal anomalies within 50 km to verify whether an actual wildfire is burning.
3. **Empirical Prior Calibration:**
   Calibrates the 1:1 training score down to the empirical tropical wildfire daily base rate ($\pi_{\text{prior}} \approx 0.003$).

---

## 3. Wayanad, Kerala Post-Fix Validation

In Wayanad, Kerala ($11.6854, 76.1320$):
- **Temperature:** $27.9^\circ\text{C}$
- **Relative Humidity:** $41\%$
- **Fire Weather Index:** $1.0$ (Danger rating: `LOW`)
- **NASA FIRMS Active Fires (50 km):** `0 detected`
- **Pre-Fix Output:** `HIGH – 60%`
- **Post-Fix Output:**
  - `hazard_score = 0.0032` ($0.32\%$)
  - `alert_level = GREEN`
  - `risk_category = LOW`
  - `guidance = "Low fire weather danger (FWI 1.0). Humid or moderate atmospheric conditions inhibit wildfire ignition and spread."`
