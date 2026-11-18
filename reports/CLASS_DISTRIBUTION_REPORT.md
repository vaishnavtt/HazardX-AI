# HAZARDX AI — Class Distribution & Split-Level Balance Audit
## Statistical Representation, Sample Sizing, and Imbalance Handling Across All 5 Hazards

**Audit Execution Date:** 2026-11-18  
**Auditing Authority:** HAZARDX AI Machine Learning Engineering Team

---

## 1. Overall Class Distribution Summary

Following Phase 2 dataset remediation, all five model-ready datasets have been verified for class balance and empirical integrity:

| Hazard Module | Positive Class ($y=1$) | Negative / Quiescent ($y=0$) | Total Records | Positive % | Negative % | Effective Ratio ($N_{neg} : N_{pos}$) | Natural Hazard Phenotype |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Floods** | **300** | **300** | **600** | **50.0%** | **50.0%** | **1.0 : 1** | Balanced Case-Control (Paired temporal offset) |
| **Landslides** | **300** | **300** | **600** | **50.0%** | **50.0%** | **1.0 : 1** | Balanced Case-Control (Paired seasonal offset) |
| **Earthquakes** | **1,979** | **8,021** | **10,000** | **19.79%** | **80.21%** | **4.05 : 1** | Moderately Imbalanced (Physical earthquake clustering) |
| **Cyclones** | **12,076** | **208,408** | **220,484** | **5.48%** | **94.52%** | **17.26 : 1** | Severely Imbalanced (Climatological extreme) |
| **Wildfires** | **600** | **600** | **1,200** | **50.0%** | **50.0%** | **1.0 : 1** | Balanced Case-Control (Paired 180d seasonal offset) |

![Class Distributions Across 5 Hazards](file:///c:/Users/thott/Desktop/hazardai/reports/figures/audit_class_distributions_5_hazards.png)

---

## 2. Split-Level Class Distribution (Train, Validation, Test)

To prevent data leakage, evaluate generalization, and ensure stable performance metrics, class representation was audited independently within each split partition across physical files.

### 2.1 Floods Split Breakdown
- **Path:** [`flood_model_ready.csv`](file:///c:/Users/thott/Desktop/hazardai/data/model_ready/floods/flood_model_ready.csv)
- **Split Strategy:** Chronological walk-forward.

| Split Partition | Total Records | Share of Matrix | Positive Count | Negative Count | Positive % | Negative % | Date Coverage |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **TRAIN** | 486 | 81.0% | 242 | 244 | 49.79% | 50.21% | 1996-09-02 to 2016-12-18 |
| **VAL** | 33 | 5.5% | 17 | 16 | 51.52% | 48.48% | 2017-01-05 to 2020-12-11 |
| **TEST** | 81 | 13.5% | 41 | 40 | 50.62% | 49.38% | 2021-01-26 to 2026-10-10 |

### 2.2 Landslides Split Breakdown
- **Path:** [`landslide_model_ready.csv`](file:///c:/Users/thott/Desktop/hazardai/data/model_ready/landslides/landslide_model_ready.csv)
- **Split Strategy:** Chronological walk-forward.

| Split Partition | Total Records | Share of Matrix | Positive Count | Negative Count | Positive % | Negative % | Date Coverage |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **TRAIN** | 366 | 61.0% | 179 | 187 | 48.91% | 51.09% | 1996-06-29 to 2013-12-25 |
| **VAL** | 144 | 24.0% | 70 | 74 | 48.61% | 51.39% | 2014-01-05 to 2015-12-23 |
| **TEST** | 90 | 15.0% | 51 | 39 | 56.67% | 43.33% | 2016-01-14 to 2017-08-21 |

### 2.3 Earthquakes Split Breakdown
- **Path:** [`earthquake_model_ready.csv`](file:///c:/Users/thott/Desktop/hazardai/data/model_ready/earthquakes/earthquake_model_ready.csv)
- **Split Strategy:** Chronological walk-forward.

| Split Partition | Total Records | Share of Matrix | Positive Count | Negative Count | Positive % | Negative % | Date Coverage |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **TRAIN** | 7,255 | 72.55% | 1,444 | 5,811 | 19.90% | 80.10% | 2000-12-31 to 2018-12-31 |
| **VAL** | 1,207 | 12.07% | 219 | 988 | 18.14% | 81.86% | 2019-01-01 to 2021-12-31 |
| **TEST** | 1,538 | 15.38% | 316 | 1,222 | 20.55% | 79.45% | 2022-01-01 to 2025-11-30 |

### 2.4 Cyclones Split Breakdown
- **Path:** [`cyclone_model_ready.csv`](file:///c:/Users/thott/Desktop/hazardai/data/model_ready/cyclones/cyclone_model_ready.csv)
- **Split Strategy:** Storm-level grouped partition ($N_{\text{leaking storms}} = 0$).

| Split Partition | Total Records | Share of Matrix | Positive Count | Negative Count | Positive % | Negative % | Date Coverage |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **TRAIN** | 177,798 | 80.64% | 9,386 | 168,412 | 5.28% | 94.72% | 1980-01-01 to 2017-12-25 |
| **VAL** | 20,930 | 9.49% | 1,250 | 19,680 | 5.97% | 94.03% | 2017-11-28 to 2021-12-20 |
| **TEST** | 21,756 | 9.87% | 1,440 | 20,316 | 6.62% | 93.38% | 2021-11-19 to 2026-11-11 |

### 2.5 Wildfires Split Breakdown
- **Path:** [`wildfire_model_ready.csv`](file:///c:/Users/thott/Desktop/hazardai/data/model_ready/wildfires/wildfire_model_ready.csv)
- **Split Strategy:** Multi-decadal spatial block partition (Americas, EMEA, APAC).

| Split Partition | Total Records | Share of Matrix | Positive Count | Negative Count | Positive % | Negative % | Date Coverage |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **TRAIN** | 930 | 77.50% | 465 | 465 | 50.00% | 50.00% | 1990-01-18 to 2026-08-08 |
| **VAL** | 174 | 14.50% | 87 | 87 | 50.00% | 50.00% | 1997-04-05 to 2026-08-14 |
| **TEST** | 96 | 8.00% | 48 | 48 | 50.00% | 50.00% | 1997-03-19 to 2026-07-16 |

![Split Level Class Distributions](file:///c:/Users/thott/Desktop/hazardai/reports/figures/audit_split_class_distributions.png)

---

## 3. XGBoost Hyperparameter Implications & Recommendations

1. **Floods, Landslides, Wildfires ($1.0 : 1$ Ratio):**
   - Direct standard binary cross-entropy loss (`scale_pos_weight = 1.0`).
   - Standard probability calibration thresholds ($p = 0.50$).
2. **Earthquakes ($4.05 : 1$ Ratio):**
   - Moderate imbalance: Recommended `scale_pos_weight = 4.05` to equalize gradient updates.
   - Evaluation metrics: Emphasize PR-AUC and F1-score rather than raw accuracy.
3. **Cyclones ($17.26 : 1$ Ratio):**
   - Severe imbalance: Recommended `scale_pos_weight = 17.26` or focal loss.
   - Primary metric: Precision-Recall Area Under Curve (PR-AUC), Brier Skill Score (BSS), and F2-score to penalize missed rapid intensification events.
