# HAZARDX AI — DATA DRIFT & MODEL MONITORING REPORT
**Document ID:** `HX-RPT-PH39-04`  
**Phase:** Phase 39 — Prospective Validation, Archival & Live Monitoring  
**Author:** Lead MLOps Engineer & Disaster Risk Scientist  
**Date:** November 20, 2026  
**Status:** OPERATIONAL & MONITORED  

---

## 1. Overview of Drift Vulnerabilities in Multi-Hazard Intelligence

Multi-hazard early warning models face two primary sources of performance degradation over time:
1. **Covariate Shift (Data Drift):** Climate change trends shift input distributions (e.g., higher average temperatures, longer summer droughts, more intense cloudbursts).
2. **Concept Drift:** The relationship between environmental features and disaster consequences changes due to human infrastructure (e.g., new retaining walls, flood barrier construction, land use zoning).

This report outlines the drift detection framework embedded in HAZARDX AI.

---

## 2. Statistical Drift Detection Methodology

### 2.1 Population Stability Index (PSI)
For continuous features (e.g., FWI, river discharge, slope, 7d rainfall), PSI evaluates distribution divergence between the baseline training distribution $P(x)$ and rolling 30-day inference batches $Q(x)$:

$$\text{PSI} = \sum_{k=1}^K \left(Q_k - P_k\right) \times \ln\left(\frac{Q_k}{P_k}\right)$$

- $\text{PSI} < 0.10$: Minimal drift; model is stable.
- $0.10 \le \text{PSI} < 0.25$: Moderate drift; warning logged; investigation recommended.
- $\text{PSI} \ge 0.25$: Significant drift; triggers automated retraining pipeline alert.

### 2.2 Wasserstein Distance (Earth Mover's Distance)
Used for physical variables with natural geometric scales (temperature, wind speed, precipitation):
$$W_1(P, Q) = \int_{-\infty}^{\infty} |F_P(x) - F_Q(x)| dx$$

---

## 3. Continuous Calibration Monitoring

The prediction archive tracks rolling 90-day Brier Score trends:
$$BS_{\text{rolling}} = \frac{1}{N} \sum_{i=1}^N (p_i - o_i)^2$$

If $BS_{\text{rolling}}$ exceeds $0.15$ for any hazard domain, the system raises an administrative alert indicating calibration deterioration and recalibrates the climatological prior $\pi$.

---

## 4. Monitoring Dashboard Endpoints

Drift and reliability statistics are exposed in real-time via:
- `GET /api/v1/geospatial/validation/archive`
- `GET /api/v1/geospatial/validation/reliability`

---

## 5. Sign-Off

The data drift and model monitoring framework is active and protecting all operational ML pipelines against silent performance degradation.
