# Phase 32 — Cyclone Risk Calculation Methodology

## 1. Overview and Target Definition

- **Defined Physical Target:** Tropical cyclone 24-hour rapid intensification ($\Delta V \ge 30\text{ kt}$ in 24 hours) and maritime-to-coastal wind threat ($P(\text{RI} \mid \text{Vortex Dynamics, Thermodynamic Potential})$).
- **Primary Data Sources:**
  - NOAA National Hurricane Center (NHC) active tropical cyclone feeds.
  - Joint Typhoon Warning Center (JTWC) and India Meteorological Department (IMD) operational bulletins.
  - IBTrACS global historical benchmark database.
  - Calibrated XGBoost Rapid Intensification Classifier (ROC-AUC 0.871).

---

## 2. Physical Gating & Spatial Validity

### 2.1 Geographic & Topographic Constraints
Tropical cyclones are warm-core, low-pressure maritime atmospheric vortices driven by latent heat release over sea surface temperatures $> 26.5^\circ\text{C}$. They decay rapidly upon moving inland:
- **Maritime Proximity Gate:** The system evaluates distance from the target coordinate to the nearest active cyclone center ($D_{\text{storm}}$). If $D_{\text{storm}} > 800\text{ km}$, cyclonic threat is zero.
- **Inland Highland Gate:** Coordinates with surface elevation $> 300\text{ m}$ (such as Wayanad at 765m) and distance to coast $> 50\text{ km}$ cannot sustain tropical cyclone vortex wind dynamics.
- **Pre-Fix Bug:** Previously, if no storm was active, the system pulled the first global storm (or fabricated a 35 kt storm with 85 km distance to land), reporting false cyclone threats for mountainous regions.

### 2.2 Saffir-Simpson Intensity Mapping
When an active storm is within the $800\text{ km}$ threat envelope:
- Cat 5 ($V \ge 137\text{ kt}$): Score $0.95$ (`EXTREME`)
- Cat 4 ($V \ge 113\text{ kt}$): Score $0.85$ (`VERY HIGH`)
- Cat 3 ($V \ge 96\text{ kt}$): Score $0.70$ (`HIGH`)
- Cat 1–2 ($V \ge 64\text{ kt}$): Score $0.50$ (`MODERATE`)
- Tropical Storm ($V \ge 34\text{ kt}$): Score $0.30$ (`LOW`)
- Tropical Depression / Quiescent: Score $0.00$ (`LOW`)

---

## 3. Wayanad, Kerala Validation

In Wayanad, Kerala ($11.6854, 76.1320$):
- **Elevation:** $765\text{ m}$ (inland highland plateau).
- **Active Cyclones within 800 km:** `0`.
- **Pre-Fix Output:** Assumed $35\text{ kt}$ disturbance, risk score $0.15$.
- **Post-Fix Output:**
  - `current_wind_kt = 0.0`
  - `rapid_intensification_prob_24h = 0.0%`
  - `hazard_score = 0.0`
  - `alert_level = GREEN`
  - `risk_category = LOW`
  - `guidance = "Inland continental/mountain location outside maritime tropical cyclone genesis and landfall zones."`
