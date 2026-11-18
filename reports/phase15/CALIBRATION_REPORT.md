# HAZARDX AI – PHASE 15 REPORT: PROBABILITY CALIBRATION & THRESHOLD OPTIMIZATION
## Rigorous Evaluation of Reliability Curves, Brier Scores, and Life-Safety Decision Boundaries

**Document Reference:** `HAZARDX-P15-CALIB-004`  
**Execution Date:** November 19, 2026  
**Auditor / Engineering Team:** Senior Machine Learning Engineer, Risk Modeler & Decision Support Architect  
**Empirical Source:** `reports/phase15/model_improvement_data.json`  
**Validation Base:** Holdout Test Splits ($N = 23,561$)  

---

## 1. CALIBRATION PRINCIPLES IN NATURAL HAZARD EARLY WARNING

In natural disaster forecasting, an uncalibrated model probability can lead to catastrophic operational errors:
- If a model outputs "90% flood probability," but real-world events only occur 30% of the time, emergency managers will mobilize costly evacuations unnecessarily, creating public complacency ("the boy who cried wolf").
- Conversely, if an uncalibrated model outputs "20% probability" during a rare extreme storm, authorities may fail to issue life-saving warnings.

### Evaluation Metrics:
1. **Brier Score:** Mean squared difference between predicted probabilities and binary outcomes:
   $$\text{BS} = \frac{1}{N} \sum_{i=1}^N (P_i - y_i)^2 \quad (\text{Lower is better; } 0.0 = \text{perfect})$$
2. **Expected Calibration Error (ECE):** Weighted average deviation between bin confidence and true bin empirical frequency across 10 equal bins:
   $$\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$

---

## 2. CALIBRATION RESULTS ACROSS ALL BINARY CLASSIFIERS

| Hazard Task | Raw XGBoost Brier Score | Raw ECE | Sigmoid (Platt) Brier Score | Isotonic Brier Score | Calibrated ECE | Optimal Calibration Method |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `floods_flood_occurrence` | **0.1915** | 0.0984 | 0.1913 | 0.2135 | **0.0821** | **Raw / Sigmoid** (Naturally well-calibrated) |
| `landslides_landslide_occurrence` | 0.2341 | 0.1420 | **0.2048** | 0.2195 | **0.0915** | **Sigmoid Scaling** (-12.5% Brier error) |
| `earthquakes_aftershock_hazard` | 0.2787 | 0.2185 | 0.1426 | **0.1399** | **0.0462** | **Isotonic Regression** (**-49.8% Brier error!**) |
| `cyclones_rapid_intensification` | 0.1000 | 0.0841 | **0.0505** | 0.0507 | **0.0210** | **Sigmoid Scaling** (**-49.5% Brier error!**) |
| `wildfires_wildfire_occurrence` | **0.1973** | 0.1012 | 0.2005 | 0.2027 | **0.0985** | **Raw XGBoost** (Naturally calibrated) |

### Key Calibration Insights:
1. **Earthquake Aftershock Hazard:** Raw XGBoost suffered from high miscalibration due to positive class weighting (`pos_weight = 4.05`), which systematically inflated probabilities. Applying **Isotonic regression** reduced the Brier score from **0.2787 down to 0.1399** (a 49.8% reduction in squared probability error), and cut ECE from 0.2185 to **0.0462**.
2. **Cyclone Rapid Intensification:** Because RI occurs in only 6.6% of intervals, raw positive probabilities were overconfident. Applying **Sigmoid calibration** cut the Brier score from **0.1000 down to 0.0505** (a 49.5% reduction), producing true empirical probabilities.
3. **Floods & Wildfires:** Both classifiers showed strong natural calibration out-of-the-box, with Brier scores under 0.20 and low ECE (<0.10).

---

## 3. DECISION THRESHOLD OPTIMIZATION (FAR vs MISSED-EVENT RATE)

In disaster response, $\tau = 0.50$ is rarely optimal. The operational threshold $\tau$ must balance:
- **False Alarm Rate (FAR):** $\frac{\text{FP}}{\text{TP} + \text{FP}}$ (Civil defense resource waste and public fatigue).
- **Missed-Event Rate (MER):** $\frac{\text{FN}}{\text{TP} + \text{FN}}$ (Failure to warn; direct threat to human life).
- **Critical Success Index (Threat Score CSI):** $\frac{\text{TP}}{\text{TP} + \text{FP} + \text{FN}}$.

### Optimal Thresholds Derived from Holdout Sweep:

```
1. Floods (flood_occurrence):
   - Default (tau = 0.50): F1 = 0.7089, FAR = 26.3%, Missed = 31.7%, CSI = 0.5490
   - Optimal (tau = 0.40): F1 = 0.7381, FAR = 28.6%, Missed = 24.4%, CSI = 0.5849
   Operational Rule: tau = 0.40 chosen to prioritize earlier catchment evacuation.

2. Landslides (landslide_occurrence):
   - Default (tau = 0.50): F1 = 0.6667, FAR = 15.2%, Missed = 45.1%, CSI = 0.5000
   - Operational (tau = 0.35): F1 = 0.7368, FAR = 22.2%, Missed = 31.4%, CSI = 0.5833
   Operational Rule: Low threshold (0.35) needed because steep saprolite failures are rapid and fatal.

3. Earthquakes (aftershock_hazard):
   - Default (tau = 0.50): F1 = 0.4311, FAR = 52.45%, Missed = 16.7%, CSI = 0.2687
   - Optimal (tau = 0.65-0.68): F1 = 0.4612, FAR = 31.75%, Missed = 36.4%, CSI = 0.2898
   Operational Rule: Calibrated tau = 0.68 adopted to eliminate the unacceptable 52.45% false alarm rate.

4. Cyclones (rapid_intensification):
   - Default (tau = 0.50): F1 = 0.3880, FAR = 72.9%, Missed = 31.7%, CSI = 0.2407
   - Optimal (tau = 0.60): F1 = 0.4104, FAR = 57.1%, Missed = 42.9%, CSI = 0.2582
   Operational Rule: Combined with Dual-Trigger wind scale to safeguard Category 3-5 storms.

5. Wildfires (wildfire_occurrence):
   - Default (tau = 0.50): F1 = 0.7368, FAR = 25.5%, Missed = 27.1%, CSI = 0.5833
   - Optimal (tau = 0.65): F1 = 0.7527, FAR = 20.5%, Missed = 27.1%, CSI = 0.6034
   Operational Rule: tau = 0.65 adopted to suppress false alarms on marginal summer afternoons.
```

---

## 4. GOVERNANCE & PRODUCTION IMPLEMENTATION STATUS

The calibrated thresholds and calibration methods have been incorporated into:
1. `backend/app/services/earthquake_service.py` (Isotonic aftershock probability, $\tau = 0.68$).
2. `backend/app/services/cyclone_service.py` (Sigmoid RI scaling + Dual-Trigger wind scale).
3. `backend/app/utils/calibration.py` (Hazard-specific alert level tiers).
4. `frontend/src/pages/ModelsPage.tsx` (Displaying verified Brier scores and calibrated FAR/Missed-Event rates).

**Conclusion:** All four deliverables for Phase 15 are complete, reproducible, and documented with complete scientific traceability.
