# Phase 37 — Root Cause Summary & Engineering Correction Roadmap

## 1. Executive Summary

This document consolidates the findings of Phase 37, detailing the root causes behind the scientific flaws identified across all five hazard pipelines, and establishes the concrete engineering action plan for Phase 38.

---

## 2. Matrix of Audited Flaws and Root Causes

| Hazard | Identified Defect | Root Cause in Code / Architecture | Engineering Correction (Phase 38) |
|---|---|---|---|
| **Wildfire** | Scale misalignment; FWI proxy cannot reach extreme levels ($12.37$ max under catastrophic firestorm); absence of FIRMS fire hotspots treated as 0% ignition risk; fuel bed/vegetation unmodeled. | Simplified single-step exponential proxy in `weather_client.py` does not match the 6-component Canadian FWI scale. `wildfire_service.py` conflates active fire satellite observation with future ignition hazard. | Implement standardized Canadian FWI components or calibrated multi-factor fire weather index with correct dynamic range ($0 - 100+$); decouple active thermal detection from ignition danger; incorporate fuel presence indicator. |
| **Earthquake** | Aftershock probability applied uniformly across 250 km radius without spatial distance decay; an M4.2 at 220 km away produced same aftershock probability as epicenter. | `omori_aftershock_model.py` implements pure temporal Omori decay without spatial distance attenuation kernel $\rho(r)$. Clamping to 0.0001 prevented exact zero probabilities. | Incorporate Wells & Coppersmith rupture scaling and spatial distance decay ($\propto (r + d)^{-\gamma}$) so aftershock hazard drops off realistically with distance from the mainshock epicenter. |
| **Landslide** | Zero rain in immediate 24h collapsed landslide probability to $0.05\%$ (`GREEN`) on a steep $32^\circ$ slope with $450\text{ mm}$ antecedent rain and high saturation. | `landslide_service.py` heavily weights immediate 1-day rain during balanced training, ignoring geotechnical pore-water pressure lag in deep mountain soils. | Redesign landslide trigger logic: require both low immediate rain AND safe antecedent saturation ($\theta_{\text{soil}} < 0.35\text{ m}^3/\text{m}^3$, $\text{API}_{30} < 100\text{ mm}$) before downgrading steep terrain to `GREEN`. |
| **Cyclone** | Hardcoded `elevation_m <= 300.0` filter silenced cyclone evaluations for all terrain $> 300\text{ m}$, ignoring severe orographic precipitation and mountain gales. | Ad-hoc elevation check in `backend/app/api/v1/endpoints/geospatial.py` added to silence Wayanad. | Remove the 300m hard filter entirely. Evaluate cyclone threats based on storm track distance, intensity, wind radii, and local NWP forecast wind gusts over realistic terrain. |
| **Flood** | Alert level assigned based on uncalibrated `raw_prob` while displayed score used `calibrated_prob`, causing `ORANGE` alert with $1.06\%$ probability in Palakkad. | `flood_service.py` called `categorize_hazard_risk("floods", raw_prob)` instead of calibrated score or physical discharge return period. | Harmonize alert categorization with calibrated probability and GloFAS discharge anomaly ratios ($Q / \bar{Q}_{7d}$). |
| **Validation** | Claimed $0.3\%$ false alarm rate was derived from theoretical calculation without live API benchmark dataset. | In Phase 35, no real 1,000-point coordinate benchmark was saved or executed against live APIs. | Withdraw flawed claim; build genuine versioned 50-coordinate live benchmark dataset and reproducible evaluation script. |

---

## 3. Engineering Roadmap for Phase 38

1. **Fix Cyclone Service & Endpoints:** Remove the 300m elevation hard restriction; implement real storm proximity and NWP wind field coupling.
2. **Fix Earthquake Omori Model:** Implement spatial distance decay kernel $\rho(r)$ centered on the mainshock epicenter.
3. **Fix Landslide Service:** Prevent alert suppression when antecedent soil saturation is high on steep slopes.
4. **Fix Wildfire Service & FWI:** Calibrate the fire weather index scale to span full standard danger ranges ($0 - 60+$) and decouple active FIRMS detection from ignition potential.
5. **Harmonize Flood & Landslide Alert Categorization:** Ensure alert levels (`GREEN`, `YELLOW`, `ORANGE`, `RED`) strictly correspond to calibrated event probabilities and physical flow anomalies.
6. **Build Reproducible Benchmark Suite:** Create real benchmark manifests and validation scripts.
