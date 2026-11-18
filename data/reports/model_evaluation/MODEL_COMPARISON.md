# HAZARDX AI — Model Architecture, Baseline & Optimization Comparison
## Detailed Empirical Analysis of Baseline Models, Hyperparameter Tuning & Loss Weighting

**Publication Date:** 2026-11-18  
**Author:** HAZARDX AI Machine Learning & Quantitative Hazard Research Team

---

## 1. Executive Summary

This report provides a comparative analysis of model progression across three development tiers for all 12 hazard prediction tasks:
1. **Tier 1: Baseline Models** (Naive statistical priors / Dummy classifiers / Mean regressors)
2. **Tier 2: Default Initial XGBoost** (Standard hyperparameter configuration)
3. **Tier 3: Optimized Tuned XGBoost** (Validation-guided randomized hyperparameter search)

Additionally, it provides an empirical investigation into **Class Imbalance Loss Weighting** and **Case-Control Base-Rate Calibration**.

---

## 2. Master Progression Table: Baseline vs. Initial vs. Tuned Models

### 2.1 Classification Tasks (Validation & Test Sets)

| Hazard | Task | Baseline Val PR-AUC | Initial Val PR-AUC | Tuned Val PR-AUC | Baseline Test PR-AUC | Initial Test PR-AUC | **Tuned Test PR-AUC** | Baseline Test ROC-AUC | **Tuned Test ROC-AUC** |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Floods** | Flood Occurrence | 0.5152 | 0.8844 | **0.9351** | 0.5062 | 0.7896 | **0.8156** | 0.5000 | **0.7899** |
| **Floods** | Severity (Macro-F1)| 0.3400 | 0.4912 | **0.5284** | 0.3306 | 0.4878 | **0.7527** | N/A | N/A |
| **Landslides** | Landslide Occurrence| 0.4861 | 0.8250 | **0.8484** | 0.5667 | 0.8101 | **0.8196** | 0.5000 | **0.7496** |
| **Landslides** | Magnitude (Macro-F1)| 0.3288 | 0.4352 | **0.4501** | 0.2016 | 0.4462 | **0.4221** | N/A | N/A |
| **Earthquakes**| Aftershock Hazard | 0.1814 | 0.4150 | **0.4658** | 0.2055 | 0.4547 | **0.4658** | 0.5000 | **0.7400** |
| **Cyclones** | Rapid Intensification| 0.0597 | 0.3771 | **0.3838** | 0.0662 | 0.3548 | **0.3543** | 0.5000 | **0.8710** |
| **Wildfires** | Wildfire Occurrence | 0.5000 | 0.8145 | **0.8305** | 0.5000 | 0.8038 | **0.8272** | 0.5000 | **0.8247** |

### 2.2 Regression Tasks (Validation & Test Sets)

| Hazard | Task | Baseline Val RMSE | Initial Val RMSE | Tuned Val RMSE | Baseline Test RMSE | Initial Test RMSE | **Tuned Test RMSE** | Baseline Test $R^2$ | **Tuned Test $R^2$** |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Earthquakes**| Aftershock Count | 8.7976 | 7.2300 | **7.5776** | 2.4176 | 2.4774 | **2.4599** | -0.0046 | -0.0401 |
| **Earthquakes**| Max Aftershock Mag| 2.3715 | 1.9888 | **1.9670** | 2.4182 | 1.9476 | **1.9449** | -0.0143 | **0.3439** |
| **Cyclones** | 24h Intensity Change| 18.6189 | 13.2702| **13.1383** | 18.7332 | 14.1225| **13.9854** | -0.0001 | **0.4426** |
| **Wildfires** | FRP Intensity | 1.4050 | 1.3967 | **1.3467** | 1.5527 | 1.4772 | **1.3717** | -0.0055 | **0.2154** |
| **Wildfires** | Fire Duration | 3.4277 | 19.2861| **6.6894** | 3.2739 | 10.3381| **7.3442** | -41.8734 | -214.75 |

---

## 3. Class Imbalance Investigation: Loss-Weighting vs. Unweighted Models

In natural hazard early warning systems, missing an extreme event (False Negative) has catastrophic humanitarian consequences, whereas a False Alarm (False Positive) can be managed with phased alert protocols.

We conducted an empirical investigation comparing unweighted XGBoost (`scale_pos_weight = 1.0`) against loss-weighted XGBoost on the validation partitions:

### 3.1 Tropical Cyclone Rapid Intensification ($1 : 17.25$ Natural Prevalence)
- **Unweighted Model (`scale_pos_weight = 1.0`):**
  * Validation Recall: **7.84%** (Misses **92.16%** of all rapid intensification events!).
  * Validation Precision: 62.03%.
  * Validation F1-Score: 0.1392.
  * Validation PR-AUC: 0.3715.
- **Initial Loss-Weighted Model (`scale_pos_weight = 17.25`):**
  * Validation Recall: **83.36%** (Captures **83.36%** of all rapid intensification events!).
  * Validation Precision: 21.54%.
  * Validation F1-Score: 0.3423 ($+145\%$ improvement).
  * Validation PR-AUC: 0.3771.
- **Tuned Model (`scale_pos_weight = 10.0`, depth 4, colsample 0.9):**
  * Validation Recall: **72.16%**.
  * Validation Precision: **26.99%**.
  * Validation F1-Score: **0.3929** ($+182\%$ improvement over unweighted).
  * Validation PR-AUC: **0.3838**.
- **Conclusion:** Standard unweighted loss functions produce dangerously quiescent models that fail in operational warning. Setting `scale_pos_weight` between 10.0 and 17.25 dramatically elevates early-warning sensitivity without degrading overall ROC-AUC (0.8710).

### 3.2 Earthquake Aftershock Hazard ($1 : 4.05$ Natural Prevalence)
- **Unweighted Model (`scale_pos_weight = 1.0`):**
  * Validation Recall: **38.36%** (Misses 61.64% of hazardous aftershock sequences).
  * Validation Precision: 48.55%.
  * Validation F1-Score: 0.4286.
- **Tuned Loss-Weighted Model (`scale_pos_weight = 4.05`):**
  * Validation Recall: **84.47%** ($+120\%$ boost in hazard sequence detection).
  * Validation Precision: 27.65%.
  * Validation F1-Score: 0.4167.
  * Validation PR-AUC: **0.4658** ($+5.4\%$ over unweighted).
- **Conclusion:** Loss weighting aligns the decision boundary with real-world public safety priorities, ensuring that 84.5% of aftershock hazard zones receive advance advisory notices.

---

## 4. Case-Control Sampling Analysis (Floods, Landslides, Wildfires)

The model-ready datasets for Floods, Landslides, and Wildfires were structured as **balanced case-control matrices ($1 : 1$ positive-to-negative ratio)**.

### Calibration & Base-Rate Correction
1. **The Base-Rate Fallacy:** In a $1:1$ case-control dataset, an uncalibrated model predicting $P(Y=1) = 0.50$ does **not** imply that a given coordinate has a 50% chance of experiencing a flood on any given day. The true climatological base rate $\pi = P(Y=1)$ in the real world is substantially smaller ($\sim 10^{-3}$ to $10^{-4}$).
2. **Prior Odds Correction Formula:**
   To translate model scores into real-world posterior probabilities in production deployment, the logistic link function must be adjusted by the sampling ratio:
   $$\text{logit}(P_{\text{real}}) = \text{logit}(P_{\text{model}}) + \ln\left(\frac{\pi}{1 - \pi}\right) - \ln\left(\frac{0.5}{0.5}\right)$$
   $$\text{logit}(P_{\text{real}}) = \text{logit}(P_{\text{model}}) + \ln\left(\frac{\pi}{1 - \pi}\right)$$
3. **Operational Recommendation:** In HAZARDX AI, these models should be utilized primarily as **Hazard Susceptibility Index (HSI)** estimators (ranging from 0 to 100) or thresholded into advisory alert tiers (Green: $<0.30$, Yellow: $0.30–0.60$, Red: $>0.60$) rather than raw daily event probability forecasts.

---

## 5. Best Hyperparameter Configurations

All optimal hyperparameter vectors discovered during validation tuning are summarized below:

| Hazard Module | Prediction Task | `n_estimators` | `max_depth` | `learning_rate` | `subsample` | `colsample_bytree` | `min_child_weight` | `reg_lambda` | `gamma` | `scale_pos_weight` |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Floods** | Flood Occurrence | 100 | 7 | 0.02 | 0.7 | 0.9 | 1 | 0.1 | 0.0 | 1.0 |
| **Floods** | Severity Class | 150 | 4 | 0.02 | 0.9 | 0.9 | 1 | 5.0 | 0.2 | 1.0 |
| **Landslides** | Landslide Occurrence | 100 | 5 | 0.05 | 0.7 | 0.8 | 1 | 0.1 | 0.0 | 1.0 |
| **Landslides** | Magnitude Class | 250 | 3 | 0.05 | 0.7 | 1.0 | 1 | 0.1 | 0.1 | 1.0 |
| **Earthquakes**| Aftershock Hazard | 100 | 3 | 0.05 | 0.9 | 1.0 | 3 | 0.1 | 0.0 | 4.05 |
| **Earthquakes**| Aftershock Count | 200 | 6 | 0.02 | 0.7 | 0.7 | 1 | 10.0 | 0.1 | N/A |
| **Earthquakes**| Max Aftershock Mag| 250 | 4 | 0.05 | 0.9 | 0.7 | 3 | 1.0 | 0.0 | N/A |
| **Cyclones** | Rapid Intensification| 150 | 4 | 0.05 | 0.7 | 0.9 | 3 | 1.0 | 0.1 | 10.0 |
| **Cyclones** | 24h Intensity Change| 250 | 6 | 0.05 | 0.8 | 0.9 | 5 | 1.0 | 0.0 | N/A |
| **Wildfires** | Wildfire Occurrence | 250 | 4 | 0.02 | 0.7 | 0.8 | 1 | 1.0 | 0.0 | 1.0 |
| **Wildfires** | FRP Intensity | 100 | 4 | 0.05 | 1.0 | 0.8 | 7 | 5.0 | 0.2 | N/A |
| **Wildfires** | Fire Duration | 200 | 3 | 0.02 | 0.8 | 0.8 | 1 | 5.0 | 0.0 | N/A |
