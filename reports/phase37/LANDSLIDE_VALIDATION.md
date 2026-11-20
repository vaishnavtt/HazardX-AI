# Phase 37 — Landslide Hazard Validation & Geotechnical Audit

## 1. Audit of the 24-Hour Rainfall Assumption

In Phase 32, the following logic was applied to suppress false alarms on dry days:
When forecast rainfall was zero ($P_{24h} = 0.0\text{ mm}$), the calibrated occurrence probability was reported as $< 0.1\%$ ($0.02\%$), and alert level was set to `GREEN`.

### 1.1 Empirical Verification Test
To audit this assumption, an empirical experiment was executed with the operational `landslide_service.predict()`:
- **Terrain Slope:** $32^\circ$ (steep, failure-prone mountain face)
- **Soil Clay Fraction:** $35\%$
- **Antecedent 30-day Rain:** $450.0\text{ mm}$ (monsoon deluge)
- **Antecedent 7-day Rain:** $150.0\text{ mm}$
- **Current 24h Rain:** $0.0\text{ mm}$ (temporary rain lull)

**Result:**
- `Raw Score:` $0.2225$
- `Calibrated Probability:` **$0.000573$ ($0.05\%$)**
- `Risk Category:` **`LOW`**
- `Alert Level:` **`GREEN`**

### 1.2 Geotechnical Flaw
In hillslope hydrology and soil mechanics (Terzaghi's effective stress principle: $\sigma' = \sigma - u$):
- Rainfall-triggered landslides do **not** occur instantaneously with rainfall arrival, nor do they cease the moment rain stops.
- Infiltrating water percolates through unsaturated topsoil to build positive pore-water pressure ($u$) along slip planes. In deep-seated colluvial soils, pore-water pressure peaks can lag precipitation peaks by **24 to 72 hours**.
- If a mountain region receives $450\text{ mm}$ of rain over 3 days, followed by a sunny morning, the slope is at its maximum saturation and instability.
- Labeling such a slope as `0.05% (GREEN)` merely because the rain stopped in the last 24 hours is a critical failure that could lead to unheralded slope collapse.

---

## 2. Multi-Timeframe Rainfall and Soil Moisture Integration

A defensible landslide model must evaluate three interacting physical drivers:
1. **Short-Term Intensity ($I_{24h}, I_{72h}$):** Triggers rapid shallow translational slides and debris flows.
2. **Antecedent Saturation ($\text{API}_{30}, \theta_{\text{soil}}$):** Pre-conditions soil moisture and elevates the water table.
3. **Topographic Susceptibility (Slope, Curvature, TWI):** Determines gravitational shear stress ($\tau = \gamma h \sin \beta \cos \beta$).

**Mandated Correction:**
The landslide risk engine must prevent alert de-escalation to `GREEN` whenever antecedent soil moisture ($\theta_{\text{soil}} \ge 0.38\text{ m}^3/\text{m}^3$) or antecedent precipitation ($\text{API}_{30} \ge 150\text{ mm}$) remains critically elevated on slopes $> 20^\circ$.
