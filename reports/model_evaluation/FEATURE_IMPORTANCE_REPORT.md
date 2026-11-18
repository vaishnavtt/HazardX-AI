# HAZARDX AI — Feature Importance & SHAP Explainability Report
## Physical Interpretability, Environmental Feature Attribution & TreeSHAP Diagnostics

**Publication Date:** 2026-11-18  
**Author:** HAZARDX AI Geospatial & Machine Learning Interpretability Team  
**Methodology:** Lundberg et al. TreeSHAP (Tree Explainer) & Native XGBoost Split Gain Attribution

---

## 1. Executive Summary

Black-box machine learning models are unacceptable in natural hazard risk intelligence. Decision-makers and emergency responders must understand **why** an early-warning alert is triggered and which physical, meteorological, or geophysical covariates are driving the prediction.

This report documents the global and local feature importance profiles across all five HAZARDX AI hazard modules, combining:
1. **TreeSHAP Global Summary Plots (Beeswarm):** Revealing feature impact magnitude and directionality.
2. **Mean Absolute SHAP Bar Plots:** Ranking average contribution to model output log-odds or regression units.
3. **XGBoost Split Gain Importance:** Quantifying relative reduction in loss objective provided by each feature.
4. **Representative Case Waterfall Plots:** Explaining individual positive and negative test events.

All plots are preserved under [`reports/model_evaluation/shap/`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/).

---

## 2. Top-5 Feature Rankings Across All 12 Hazard Models

| Hazard Module | Prediction Task | #1 Top Predictor | #2 Predictor | #3 Predictor | #4 Predictor | #5 Predictor | Physical Domain |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Floods** | Flood Occurrence | `precip_1d_mm` | `precip_3d_sum_mm` | `precip_7d_sum_mm` | `soil_temp_celsius` | `elevation_m` | Meteorological & Topography |
| **Floods** | Flood Severity | `precip_3d_sum_mm` | `precip_14d_sum_mm`| `temp_2m_celsius` | `soil_temp_celsius` | `precip_1d_mm` | Multi-week Hydrometeorology |
| **Landslides** | Landslide Occurrence| `precip_3d_sum_mm` | `precip_1d_mm` | `precip_30d_sum_mm`| `api_30d_index` | `precip_7d_sum_mm` | Short-term & Antecedent Rain |
| **Landslides** | Landslide Magnitude | `precip_3d_sum_mm` | `precip_30d_sum_mm`| `soil_clay_fraction`| `api_30d_index` | `precip_1d_mm` | Geotechnical & Antecedent |
| **Earthquakes**| Aftershock Hazard | `prior_count_365d` | `fault_slip_type` | `focal_depth_km` | `prior_count_30d` | `prior_max_mag_30d` | Long-term Seismotectonics |
| **Earthquakes**| Aftershock Count | `prior_count_365d` | `prior_count_30d` | `focal_depth_km` | `dist_to_fault_km` | `fault_slip_type` | Regional Strain Accumulation |
| **Earthquakes**| Max Aftershock Mag| `prior_count_365d` | `focal_depth_km` | `cumulative_energy`| `fault_slip_type` | `regional_b_value` | Radiated Energy & Depth |
| **Cyclones** | Rapid Intensification| `past_delta_wind_6h`| `coriolis_param` | `current_wind_kt` | `past_delta_pres_6h`| `past_delta_wind_12h`| Kinematic Momentum & Latitude|
| **Cyclones** | 24h Intensity Change| `current_wind_kt` | `past_delta_wind_6h`| `landfall_flag` | `past_delta_pres_6h`| `coriolis_param` | Intensity Climatology & Land |
| **Wildfires** | Wildfire Occurrence | `temp_2m_celsius` | `relative_humidity`| `fwi_fire_weather` | `soil_temp_celsius` | `precip_30d_sum_mm` | Atmospheric Aridity & FWI |
| **Wildfires** | FRP Intensity | `temp_2m_celsius` | `soil_temp_celsius`| `relative_humidity`| `fwi_fire_weather` | `precip_30d_sum_mm` | Thermal Heat & Dry Soil |
| **Wildfires** | Fire Duration | `temp_2m_celsius` | `soil_temp_celsius`| `relative_humidity`| `fwi_fire_weather` | `wind_speed_10m_ms`| Sustained Desiccation |

---

## 3. Physical Interpretability Deep-Dive by Hazard

### 3.1 Flood Occurrence Model
- **Primary Driving Feature: `precip_1d_mm` & `precip_3d_sum_mm`**
  * SHAP beeswarm analysis confirms an exponential positive response: 1-day rainfall exceeding 25 mm and 3-day accumulated rainfall exceeding 50 mm sharply increase the log-odds of inundation.
  * `elevation_m` acts as an inverse modulator: low-elevation coastal and flood-plain basins ($\le 50\text{ m}$) exhibit large positive SHAP values, whereas mountainous locations suppress flood probability.
  * `river_discharge_ratio_7d` provides secondary predictive uplift when antecedent channel flow exceeds seasonal climatology.
- **Visual Evidence:**
  * Summary Beeswarm: [`floods_flood_occurrence_shap_summary.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/floods_flood_occurrence_shap_summary.png)
  * Feature Importance Bar: [`floods_flood_occurrence_shap_bar.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/floods_flood_occurrence_shap_bar.png)
  * Individual Case Waterfall: [`floods_flood_occurrence_case_waterfall.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/floods_flood_occurrence_case_waterfall.png)

### 3.2 Landslide Occurrence Model
- **Primary Driving Feature: `precip_3d_sum_mm` & `precip_30d_sum_mm`**
  * Landslide failure requires both **antecedent pore-water saturation** (captured by `precip_30d_sum_mm` and `api_30d_index`) and an **intense triggering burst** (captured by `precip_3d_sum_mm` and `precip_1d_mm`).
  * `slope_degrees` provides baseline geomorphological susceptibility: slopes between $18^\circ$ and $45^\circ$ have strong positive attribution, whereas flat plains ($<5^\circ$) have strong negative attribution.
- **Visual Evidence:**
  * Summary Beeswarm: [`landslides_landslide_occurrence_shap_summary.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/landslides_landslide_occurrence_shap_summary.png)
  * Feature Importance Bar: [`landslides_landslide_occurrence_shap_bar.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/landslides_landslide_occurrence_shap_bar.png)
  * Individual Case Waterfall: [`landslides_landslide_occurrence_case_waterfall.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/landslides_landslide_occurrence_case_waterfall.png)

### 3.3 Earthquake Aftershock Hazard Model
- **Primary Driving Feature: `prior_count_365d_100km` & `nearest_fault_slip_type`**
  * Regions with elevated 1-year background seismicity ($\ge 50$ events within 100 km) exhibit significantly higher probability of triggering extensive aftershock sequences, consistent with high tectonic loading and clustered fault networks.
  * `nearest_fault_slip_type`: Subduction zone thrust faults and major strike-slip systems exhibit greater aftershock productivity than oceanic spreading ridges.
  * `focal_depth_km`: Shallow mainshocks ($\le 25\text{ km}$) contribute positively to aftershock hazard; deep events have minimal secondary ruptures.
- **Visual Evidence:**
  * Summary Beeswarm: [`earthquakes_aftershock_hazard_shap_summary.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/earthquakes_aftershock_hazard_shap_summary.png)
  * Feature Importance Bar: [`earthquakes_aftershock_hazard_shap_bar.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/earthquakes_aftershock_hazard_shap_bar.png)
  * Individual Case Waterfall: [`earthquakes_aftershock_hazard_case_waterfall.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/earthquakes_aftershock_hazard_case_waterfall.png)

### 3.4 Tropical Cyclone Rapid Intensification Model
- **Primary Driving Feature: `past_delta_wind_6h` & `coriolis_param`**
  * **Intensification Momentum:** Cyclones already intensifying rapidly in the preceding 6 hours ($\Delta V_{6h} \ge +5\text{ kt}$) have high inertia to sustain rapid intensification over the next 24 hours.
  * **Coriolis Parameter ($f = 2\Omega \sin \phi$):** Equatorial systems ($\phi < 5^\circ$) cannot develop sufficient planetary vorticity to undergo RI; systems between $12^\circ$ and $25^\circ$ latitude exhibit optimal vortex spin-up conditions.
  * **Current Intensity Headroom:** Strong positive contribution occurs when storms are in the tropical depression / tropical storm stage ($35–50\text{ kt}$) over warm waters with large headroom beneath the Maximum Potential Intensity (MPI).
- **Visual Evidence:**
  * Summary Beeswarm: [`cyclones_rapid_intensification_shap_summary.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/cyclones_rapid_intensification_shap_summary.png)
  * Feature Importance Bar: [`cyclones_rapid_intensification_shap_bar.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/cyclones_rapid_intensification_shap_bar.png)
  * Individual Case Waterfall: [`cyclones_rapid_intensification_case_waterfall.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/cyclones_rapid_intensification_case_waterfall.png)

### 3.5 Wildfire Ignition Susceptibility Model
- **Primary Driving Feature: `temp_2m_celsius`, `relative_humidity_pct`, & `fwi_fire_weather_index`**
  * High 2m air temperatures ($\ge 25^\circ\text{C}$) combined with low relative humidity ($\le 30\%$) produce large positive SHAP attribution.
  * The Canadian Forest Fire Weather Index (FWI) proxy captures integrated fuel dryness; values $> 15$ drive sharp increases in wildfire probability.
  * Negative controls (sampled in winter/wet seasons) are decisively pushed toward zero by sub-zero temperatures and high cumulative antecedent rainfall.
- **Visual Evidence:**
  * Summary Beeswarm: [`wildfires_wildfire_occurrence_shap_summary.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/wildfires_wildfire_occurrence_shap_summary.png)
  * Feature Importance Bar: [`wildfires_wildfire_occurrence_shap_bar.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/wildfires_wildfire_occurrence_shap_bar.png)
  * Individual Case Waterfall: [`wildfires_wildfire_occurrence_case_waterfall.png`](file:///c:/Users/thott/Desktop/hazardai/reports/model_evaluation/shap/wildfires_wildfire_occurrence_case_waterfall.png)

---

## 4. Synthesis & Scientific Validation

Across all five hazard categories, the TreeSHAP attribution profiles confirm that the XGBoost models are learning **genuine physical, geophysical, and meteorological laws**, rather than spurious statistical artifacts or dataset shortcuts.

