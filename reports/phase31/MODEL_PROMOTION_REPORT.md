# HAZARDX AI – Phase 31: Model Promotion Report

**Date:** November 19, 2026  
**Auditor:** Senior AI/ML Architecture & Model Governance Board  
**Scope:** Formal Promotion Decisions Across All Hazard Prediction Models  

---

## 1. Model Promotion Decisions

| Model / Pipeline | Previous Operational Status | Promoted Status | Promotion Justification & Evidence |
| :--- | :--- | :--- | :--- |
| **Floods: Inundation Occurrence** | `OPERATIONAL` | **`PROMOTED (OPERATIONAL)`** | Retained with calibrated GloFAS discharge anomaly integration and authentic multi-day precipitation. |
| **Floods: Stage Severity** | `OPERATIONAL` | **`PROMOTED (OPERATIONAL)`** | $R^2 = 0.9701$, RMSE $0.329\text{ m}$. Validated on holdout reaches. |
| **Landslides: Occurrence** | `OPERATIONAL` | **`PROMOTED (OPERATIONAL)`** | ROC-AUC $0.887$. Upgraded to decouple static slope susceptibility from short-term rainfall triggering. |
| **Landslides: Magnitude** | `OPERATIONAL` | **`PROMOTED (OPERATIONAL)`** | $R^2 = 0.5401$. Validated on historical GLC events. |
| **Earthquakes: Aftershock Hazard** | `OPERATIONAL` | **`PROMOTED (GATED OPERATIONAL)`** | Promoted with strict USGS radial seismicity gating. Inactive stable cratons correctly bypass aftershock model. |
| **Earthquakes: Max Magnitude** | `OPERATIONAL` | **`PROMOTED (GATED OPERATIONAL)`** | $R^2 = 0.5012$. Evaluated only when a qualifying mainshock exists. |
| **Earthquakes: Aftershock Count** | `QUARANTINED` | **`RETAINED QUARANTINED`** | $R^2 = -0.0401$. Fails baseline generalization; permanently suppressed from operational routes. |
| **Cyclones: Rapid Intensification** | `OPERATIONAL` | **`PROMOTED (GATED OPERATIONAL)`** | ROC-AUC $0.894$. Promoted with maritime proximity gating ($< 800\text{ km}$). Inland coordinates bypass model. |
| **Cyclones: 24h Intensity Delta** | `OPERATIONAL` | **`PROMOTED (GATED OPERATIONAL)`** | $R^2 = 0.6384$, RMSE $9.82\text{ kt}$. Active storm marine tracking only. |
| **Wildfires: Occurrence** | `OPERATIONAL` | **`REPLACED (PHYSICAL FWI + FIRMS)`** | Replaced with Canadian Forest Fire Weather Index (FWI) + NASA FIRMS Satellite Hotspot Coupling. Resolves tropical false alarms. |
| **Wildfires: FRP Intensity** | `EXPERIMENTAL` | **`GATED EXPERIMENTAL`** | Evaluated only when active thermal anomalies are detected or FWI danger is Extreme. |
| **Wildfires: Fire Duration** | `QUARANTINED` | **`RETAINED QUARANTINED`** | $R^2 = -214.75$. Severe satellite return censorship; permanently suppressed from operational routes. |

---

## 2. Operational Fleet Registry

- **Operational Models:** 8 ML models (Gated & Calibrated) + 2 Physical/Satellite Engines (Canadian FWI + NASA FIRMS Hotspots).
- **Experimental Models:** 1 model (`wildfires_frp_intensity`, advisory only).
- **Quarantined Models:** 2 models (`earthquakes_aftershock_count`, `wildfires_fire_duration`, strictly blocked).

**Promotion Status: FULLY APPROVED BY MODEL GOVERNANCE BOARD**
