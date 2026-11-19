# HAZARDX AI – Phase 30: Dataset Exploratory Data Analysis Report

**Date:** November 19, 2026  
**Auditor:** Senior Data Science & Exploratory Analytics Group  
**Scope:** In-Depth Statistical Distribution & Feature Covariance Analysis Across 5 Datasets  

---

## 1. Feature Distribution Summary

### 1.1 Cyclone Dataset (`cyclone_model_ready.csv`, $N = 220,484$)
- `current_wind_kt`: Mean $44.8\text{ kt}$, Median $40.0\text{ kt}$, IQR $[30.0, 55.0]$, Max $185.0\text{ kt}$ (Category 5 Super Typhoons).
- `current_pres_hpa`: Mean $993.4\text{ hPa}$, Min $870.0\text{ hPa}$ (Typhoon Tip), Max $1024.0\text{ hPa}$.
- `delta_wind_24h`: Mean $+0.42\text{ kt}$, Std $16.8\text{ kt}$, Min $-105\text{ kt}$, Max $+115\text{ kt}$.
- `rapid_intensification` ($\ge +30\text{ kt} / 24\text{h}$): $5.8\%$ positive prevalence ($12,788$ instances), realistically representing severe meteorological intensification infrequency.

### 1.2 Earthquake Dataset (`earthquake_model_ready.csv`, $N = 10,000$)
- `mainshock_mag`: Mean $5.41\text{ Mw}$, Median $5.20\text{ Mw}$, Min $4.0\text{ Mw}$, Max $9.1\text{ Mw}$ (2011 Tohoku).
- `focal_depth_km`: Mean $34.2\text{ km}$, Median $15.0\text{ km}$, Max $680.0\text{ km}$ (Deep subduction slab events).
- `dist_to_active_fault_km`: Mean $48.6\text{ km}$, Median $18.4\text{ km}$, Max $850.0\text{ km}$.
- `elevated_aftershock_hazard`: $42.1\%$ positive (defined as $P(M \ge 4.5 \text{ within } 30\text{d}) \ge 0.50$).

### 1.3 Flood Dataset (`flood_model_ready.csv`, $N = 600$)
- `precip_1d_mm`: Flood events: Mean $59.4\text{ mm}$, Range $[25.0, 95.0\text{ mm}]$. Non-floods: Mean $1.9\text{ mm}$, Range $[0.0, 4.0\text{ mm}]$.
- `precip_7d_sum_mm`: Flood events: Mean $238.1\text{ mm}$. Non-floods: Mean $6.8\text{ mm}$.
- `river_discharge_ratio_7d`: Flood events: Mean $2.14\times$ normal baseline. Non-floods: Mean $0.98\times$ baseline.
- **EDA Insight:** Sharp artificial separation between positive and negative classes due to synthetic sampling thresholds. Intermediate borderline storm events ($15–25\text{ mm}$ rain with high saturation) are underrepresented.

### 1.4 Landslide Dataset (`landslide_model_ready.csv`, $N = 600$)
- `precip_1d_mm`: Slide events: Mean $98.6\text{ mm}$, Range $[45.0, 160.0\text{ mm}]$. Non-slides: Mean $1.4\text{ mm}$, Range $[0.0, 3.0\text{ mm}]$.
- `precip_30d_sum_mm`: Slide events: Mean $412.5\text{ mm}$. Non-slides: Mean $11.2\text{ mm}$.
- `slope_degrees`: Slide events: Mean $28.4^\circ$, Range $[18.0^\circ, 52.0^\circ]$. Non-slides: Mean $8.2^\circ$.
- **EDA Insight:** Slope gradient and 30-day antecedent rain are strong discriminating predictors, but non-event controls lack steep slopes under moderate rain.

### 1.5 Wildfire Dataset (`wildfire_model_ready.csv`, $N = 1,200$)
- `temp_2m_celsius`: Fires: Mean $32.4^\circ\text{C}$, Std $4.8^\circ\text{C}$. Non-fires: Mean $18.1^\circ\text{C}$, Std $5.9^\circ\text{C}$.
- `relative_humidity_pct`: Fires: Mean $18.7\%$, Std $5.8\%$. Non-fires: Mean $64.8\%$, Std $14.2\%$.
- `wind_speed_10m_ms`: Fires: Mean $5.8\text{ m/s}$. Non-fires: Mean $3.2\text{ m/s}$.
- `fwi_fire_weather_index`: Fires: Mean $16.4$. Non-fires: Mean $3.2$.
- **EDA Insight:** Ambient temperature exhibits artificial Pearson correlation of $r = +0.78$ with `wildfire_occurred` because non-fire controls were generated at cold temperatures ($18^\circ\text{C}$). This synthetic artifact created the Wayanad false alarm.

---

## 2. Multicollinearity & Correlation Highlights

| Dataset | High Covariance Pairs ($|r| > 0.80$) | Physical Implication & Treatment |
| :--- | :--- | :--- |
| **Floods** | `precip_3d_sum_mm` $\leftrightarrow$ `precip_7d_sum_mm` ($r = 0.91$) | Strong temporal auto-correlation in rainfall accumulation. L2 regularization (`reg_lambda = 1.0`) prevents tree weight explosion. |
| **Landslides** | `precip_7d_sum_mm` $\leftrightarrow$ `precip_30d_sum_mm` ($r = 0.88$) | Antecedent saturation is naturally cumulative. Preserved to distinguish short burst vs sustained saturation. |
| **Wildfires** | `temp_2m_celsius` $\leftrightarrow$ `soil_temp_celsius` ($r = 0.96$) | Near-perfect collinearity. Soil temperature adds negligible unique information beyond surface air temperature. |
| **Cyclones** | `current_wind_kt` $\leftrightarrow$ `current_pres_hpa` ($r = -0.89$) | Classical wind-pressure relationship (Dvorak empirical law). Essential physical constraint. |

---

## 3. EDA Remediation Directives

1. **Decouple Fire Risk from Absolute Temperature:** Temperature alone must never dictate wildfire risk. Wildfire potential must be governed by atmospheric moisture deficit (VPD, RH $< 30\%$), wind speed ($> 5\text{ m/s}$), fuel moisture deficit (Canadian FWI), and verified satellite thermal anomalies (NASA FIRMS).
2. **Re-anchor Case-Control Baselines:** Incorporate realistic baseline priors into all classification outputs to prevent $0\text{ mm}$ rain conditions from displaying $10\%$ threat scores.
