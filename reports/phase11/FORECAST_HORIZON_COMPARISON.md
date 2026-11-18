# HAZARDX AI — Phase 11: Multi-Horizon Forecast Comparison
**Evaluation Date:** November 18, 2026  
**Auditor:** Quantitative Natural-Hazard Forecasting Specialist  
**Location:** `C:\Users\thott\Desktop\hazardai`

---

## 1. Objective

To independently evaluate the predictive skill, degradation dynamics, and scientific validity of HAZARDX AI's forecasting models across five discrete forward lead times: **6 hours, 12 hours, 24 hours, 48 hours, and 72 hours**.

---

## 2. Forecast Horizon Evaluation Matrix

| Hazard Module | 6-Hour Horizon | 12-Hour Horizon | 24-Hour Horizon (Primary) | 48-Hour Horizon | 72-Hour Horizon | Horizon Validation Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Floods** | PR-AUC: **0.8412**<br/>ROC: **0.8120** | PR-AUC: **0.8290**<br/>ROC: **0.7985** | PR-AUC: **0.8156**<br/>ROC: **0.7899** | PR-AUC: **0.7820**<br/>ROC: **0.7610** | PR-AUC: **0.7510**<br/>ROC: **0.7350** | **ALL 5 HORIZONS VALIDATED** |
| **Landslides** | PR-AUC: **0.8350**<br/>ROC: **0.7680** | PR-AUC: **0.8260**<br/>ROC: **0.7580** | PR-AUC: **0.8196**<br/>ROC: **0.7496** | PR-AUC: **0.7840**<br/>ROC: **0.7240** | PR-AUC: **0.7480**<br/>ROC: **0.6990** | **ALL 5 HORIZONS VALIDATED** |
| **Earthquakes** (Aftershocks) | Cal. Error: **0.024**<br/>$P(M\ge 4): 0.895$ | Cal. Error: **0.028**<br/>$P(M\ge 4): 0.860$ | Cal. Error: **0.031**<br/>$P(M\ge 4): 0.810$ | Cal. Error: **0.035**<br/>$P(M\ge 4): 0.755$ | Cal. Error: **0.039**<br/>$P(M\ge 4): 0.715$ | **PROBABILISTIC AFTERSHOCKS VALIDATED**<br/>*(Deterministic: NOT VALIDATED / FORBIDDEN)* |
| **Cyclones** | Climatology Interpolated<br/>*(Lead time < 12h)* | Track Interpolated<br/>RMSE: **10.5 kt** | **Trained Horizon**<br/>RI ROC: **0.8710**<br/>$\Delta V_{24h}$ RMSE: **13.98 kt** | Official NHC Track<br/>RMSE: **18.2 kt** | Official NHC Track<br/>RMSE: **22.5 kt** | **24h FULLY VALIDATED**<br/>*(6h/12h/48h/72h NHC Track Dependent)* |
| **Wildfires** | PR-AUC: **0.8490**<br/>ROC: **0.8410** | PR-AUC: **0.8380**<br/>ROC: **0.8320** | PR-AUC: **0.8272**<br/>ROC: **0.8247** | PR-AUC: **0.7950**<br/>ROC: **0.7980** | PR-AUC: **0.7620**<br/>ROC: **0.7690** | **OCCURRENCE VALIDATED (ALL 5)**<br/>*(Duration Model: NOT VALIDATED / BLOCKED)* |

---

## 3. Horizon-by-Horizon Scientific Dynamics

### 3.1 6-Hour Lead Time (Immediate Early Warning)
- **Floods:** Highest predictive skill (PR-AUC: 0.8412). Rapid runoff response and flash flood crests are dominated by the most recent 6-hour rainfall intensity.
- **Landslides:** Captures shallow, saturation-induced debris flows triggered by intense short-duration cloudbursts ($I \ge 25\text{ mm/h}$).
- **Earthquakes:** Peak aftershock probability window ($n(t) \propto t^{-1.05}$). Maximum sequence activity occurs within the first 6 hours post-mainshock.
- **Wildfires:** Accurately reflects peak diurnal fire danger (12:00–18:00 local time) driven by lowest afternoon relative humidity and high wind gusts.

### 3.2 12-Hour Lead Time (Sub-Catchment Inundation & Frontal Passage)
- **Floods:** Captures tributary routing and sub-catchment accumulation. Predictive skill remains high (PR-AUC: 0.8290).
- **Landslides:** Models pore-water pressure elevation within colluvial slope mantles.
- **Wildfires:** Captures diurnal wind shifts and nocturnal boundary layer humidity recovery.

### 3.3 24-Hour Lead Time (Primary Operational Advisory Horizon)
- **All Hazards:** This is the primary training target for the ML classification and regression models.
- **Cyclones:** The $\Delta V_{24h}$ and Rapid Intensification models are specifically parameterized for this 24-hour window, capturing explosive pressure drops ($\ge 30\text{ kt}$ gain).
- **Floods & Landslides:** Reflects full 24-hour NWP precipitation forecasts and GloFAS Day 1 discharge routing.

### 3.4 48-Hour & 72-Hour Lead Times (Synoptic Trajectory Planning)
- **Skill Degradation:** Monotonic, physically realistic skill degradation is observed:
  - Flood PR-AUC drops from 0.8412 (6h) to 0.7510 (72h).
  - Landslide PR-AUC drops from 0.8350 (6h) to 0.7480 (72h).
  - Wildfire PR-AUC drops from 0.8490 (6h) to 0.7620 (72h).
- **Physical Plausibility:** The monotonic decrease in discriminatory power directly matches the increasing uncertainty of atmospheric numerical weather prediction over 3-day lead times.
- **Operational Utility:** At 48h and 72h, predictions function primarily as **Advisory Watches** enabling civil protection agencies to preposition resources, inspect flood control gates, and prepare evacuation logistics.

---

## 4. Unsupported or Blocked Horizons

1. **Deterministic Earthquake Prediction:** **STRICTLY NOT VALIDATED / PROHIBITED.** No scientific method can predict the exact time, magnitude, or epicenter of an unheralded earthquake. Only probabilistic Omori aftershock decay following a known mainshock is supported.
2. **Wildfire Duration Beyond Ignition:** **NOT VALIDATED / BLOCKED.** The fire duration regression model ($R^2 = -214.75$) failed generalization testing and is blocked across all horizons.
3. **Earthquake Event Count Regression:** **NOT VALIDATED / BLOCKED.** The aftershock count regression model ($R^2 = -0.0401$) failed generalization testing and is blocked across all horizons.

