# HAZARDX AI — PROBABILITY CALIBRATION & ALERT HARMONIZATION REPORT
**Document ID:** `HX-RPT-PH38-06`  
**Phase:** Phase 38 — Model, Data & Risk Engine Improvements  
**Author:** Statistical Risk Analyst & Machine Learning Scientist  
**Date:** November 20, 2026  
**Status:** VALIDATED & APPROVED  

---

## 1. Executive Summary

Supervised classification models trained on balanced case-control disaster datasets (e.g. 50% disaster / 50% non-disaster) output raw probabilities that reflect the balanced sample distribution rather than true real-world climatological occurrence rates.

This report documents the Bayesian odds-ratio calibration applied across HAZARDX AI and the harmonization of discrete alert levels (`GREEN`, `YELLOW`, `ORANGE`, `RED`) with calibrated probabilities and physical indices.

---

## 2. Bayesian Prior Odds Adjustment

To convert raw model predicted probabilities $p_{\text{model}}$ into calibrated daily occurrence probabilities $p_{\text{calibrated}}$, Bayes' rule is applied:

$$\text{logit}(p_{\text{calibrated}}) = \text{logit}(p_{\text{model}}) + \ln\left(\frac{\pi}{1 - \pi}\right)$$

Where $\pi$ represents the empirical daily climatological prior for the hazard type:

| Hazard Domain | Daily Climatological Prior ($\pi$) | Justification / Source |
| :--- | :--- | :--- |
| **Floods** | $0.005$ (~1.8 flood events per 365 days in vulnerable reaches) | Dartmouth Flood Observatory / GloFAS Climatology |
| **Landslides** | $0.002$ (~0.7 slope failures per 365 days in hilly terrain) | NASA Global Landslide Catalog (GLC) |
| **Wildfires** | $0.003$ (~1.1 fire ignition days per year in vegetated biomes) | EFFIS / MODIS Global Fire Atlas |
| **Earthquakes** | $0.001$ (~0.36 significant M4.5+ events per year within 100km) | USGS ComCat 50-year Seismicity Catalog |
| **Cyclones** | $0.001$ (~0.36 tropical storms passing within 500km annually) | NOAA IBTrACS 150-year Global Trajectories |

Implementation in `backend/app/utils/calibration.py`:
```python
def adjust_case_control_probability(p_model: float, real_world_prior: float) -> float:
    p_clamped = max(1e-6, min(1.0 - 1e-6, p_model))
    pi_clamped = max(1e-6, min(1.0 - 1e-6, real_world_prior))
    logit_model = math.log(p_clamped / (1.0 - p_clamped))
    logit_prior = math.log(pi_clamped / (1.0 - pi_clamped))
    logit_calibrated = logit_model + logit_prior
    return float(round(1.0 / (1.0 + math.exp(-logit_calibrated)), 6))
```

---

## 3. Alert Level Categorization Matrix

Alert categories are harmonized between calibrated susceptibility scores and physical warning thresholds:

```
┌──────────────┬─────────────┬───────────────────┬────────────────────────────────────────────────────────┐
│ Alert Level  │ Badge Color │ Score Range       │ Operational Action Guidance                            │
├──────────────┼─────────────┼───────────────────┼────────────────────────────────────────────────────────┤
│ GREEN        │ #10B981     │ Score < 0.30      │ Normal baseline conditions; routine monitoring.        │
│ YELLOW       │ #FBBF24     │ 0.30 <= Score < 0.60 Elevated susceptibility; maintain structural vigilance. │
│ ORANGE       │ #F97316     │ 0.60 <= Score < 0.80 High hazard danger; prepare mitigation barriers.        │
│ RED          │ #EF4444     │ Score >= 0.80     │ Severe/Critical hazard imminent; initiate evacuations. │
└──────────────┴─────────────┴───────────────────┴────────────────────────────────────────────────────────┘
```

---

## 4. Calibration Curve Verification

Comparing raw model scores vs calibrated probabilities across standard operational checkpoints:

```
Raw Model Score (Case-Control)  │  Calibrated Flood Prob (π=0.005)  │  Calibrated Landslide Prob (π=0.002)
────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────
0.10                            │  0.00056                          │  0.00022
0.30                            │  0.00215                          │  0.00086
0.50 (Decision Threshold)       │  0.00500                          │  0.00200
0.70                            │  0.01160                          │  0.00465
0.90                            │  0.04327                          │  0.01768
0.99                            │  0.33221                          │  0.16529
0.999                           │  0.83403                          │  0.66644
```

*Key Takeaway:* Even when raw model susceptibility indicates elevated environmental propensity ($p_{\text{raw}} = 0.50$), the daily calibrated likelihood of a catastrophic inundation or slope failure is accurately anchored to the true climatological baseline prior ($0.2\% - 0.5\%$), avoiding sensationalist over-prediction while maintaining relative risk ranking.
