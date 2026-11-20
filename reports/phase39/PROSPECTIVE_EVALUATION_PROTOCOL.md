# HAZARDX AI — PROSPECTIVE EVALUATION PROTOCOL
**Document ID:** `HX-RPT-PH39-02`  
**Phase:** Phase 39 — Prospective Validation, Archival & Live Monitoring  
**Author:** Disaster Risk Scientist & Empirical Evaluation Lead  
**Date:** November 20, 2026  
**Status:** BENCHMARKED & STANDARDIZED  

---

## 1. Scientific Protocol Definition

Prospective validation requires evaluating model predictions against real-world events that occur strictly *after* the prediction timestamp has been logged and sealed.

This protocol eliminates:
1. **Hindsight Bias:** Optimizing hyperparameters or thresholds knowing where disasters occurred.
2. **Temporal Data Leakage:** Inadvertently including post-event observations in feature calculation.
3. **Selective Reporting:** Cherry-picking test cases that yield favorable numbers.

---

## 2. Event Verification Ground-Truth Criteria

| Hazard Domain | Verification Target Event ($Y = 1$) | Official Verification Source | Verification Window ($\Delta t$) | Spatial Tolerance ($\Delta r$) |
| :--- | :--- | :--- | :--- | :--- |
| **Earthquakes** | Magnitude $M \ge 4.5$ seismic event | USGS ComCat / FDSNWS | 24 to 72 hours | Epicentral distance $\le 50\text{ km}$ |
| **Wildfires** | Active thermal anomaly with FRP $\ge 20\text{ MW}$ | NASA FIRMS VIIRS/MODIS Hotspots | 24 hours | Radial distance $\le 15\text{ km}$ |
| **Floods** | River discharge exceeding bankfull stage or GloFAS ratio $\ge 2.0$ | Copernicus GloFAS / CEMS Flood | 24 to 48 hours | Reach buffer $\le 10\text{ km}$ |
| **Landslides** | Slope destabilization / debris flow | Geological Survey of India / USGS / NASA GLC | 24 to 72 hours | Hillslope buffer $\le 5\text{ km}$ |
| **Cyclones** | 24h rapid intensification ($\Delta V \ge 30\text{ kt}$) | NOAA NHC / JTWC / IMD Best Track | 24 hours | Storm eye radius $\le 150\text{ km}$ |

---

## 3. Contingency Classification Matrix

For any archived prediction with decision threshold $\tau = 0.50$ (or alert level `ORANGE` / `RED`):

$$\begin{array}{c|c|c}
 & \textbf{Event Observed } (Y=1) & \textbf{No Event Observed } (Y=0) \\
\hline
\textbf{Alert Issued } (\hat{Y}=1) & \text{Hit } (H) & \text{False Alarm } (FA) \\
\hline
\textbf{No Alert } (\hat{Y}=0) & \text{Miss } (M) & \text{Correct Rejection } (CR)
\end{array}$$

### Standard Derived Metrics:
- **Probability of Detection (Hit Rate):** $\text{POD} = \frac{H}{H + M}$
- **False Alarm Ratio (FAR):** $\text{FAR} = \frac{FA}{H + FA}$
- **False Alarm Rate (Probability of False Detection):** $\text{POFD} = \frac{FA}{CR + FA}$
- **Critical Success Index (Threat Score):** $\text{CSI} = \frac{H}{H + FA + M}$
- **Brier Score:** $\text{BS} = \frac{1}{N} \sum_{i=1}^N (p_i - o_i)^2$

---

## 4. Operational Execution

The automated verification pipeline runs continuously in the background, auditing pending predictions against live global sensor networks and publishing updated reliability metrics to the admin dashboard and API endpoints.
