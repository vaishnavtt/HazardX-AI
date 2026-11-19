# HAZARDX AI – Phase 29: Live Feature Mapping Audit

**Date:** November 19, 2026  
**Auditor:** AI/ML & Data Engineering Group  
**Scope:** Training Schema vs. Live Inference Feature Mapping for all 12 Machine Learning Models  

---

## 1. Feature Mapping Comparative Matrix

| Hazard & Task | Training Features (from JSON Metadata) | Live Inferred Features (`spatial_feature_service.py`) | Units & Scaling | Alignment Status | Identified Mismatches & Defects |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Wildfires:** `wildfire_occurrence` | `temp_2m_celsius`<br>`relative_humidity_pct`<br>`wind_speed_10m_ms`<br>`precip_7d_sum_mm`<br>`precip_30d_sum_mm`<br>`soil_temp_celsius`<br>`fwi_fire_weather_index`<br>`slope_degrees`<br>`elevation_m`<br>`distance_to_road_km` | Identical 10 feature names in matching order | °C<br>%<br>m/s<br>mm<br>mm<br>°C<br>FWI index<br>deg<br>m<br>km | **CRITICAL MISMATCH** | **Formula Divergence:** Training computed FWI proxy using simple linear deficit $(T + \Delta RH) \cdot W \cdot R \cdot 0.15$ (range 0–100, median 6.0), whereas live inference computed McArthur exponential FWI (yielding 0.7 for Wayanad). The model learned split points on the training distribution that do not match the live formula. |
| **Earthquakes:** `aftershock_hazard` | `mainshock_mag`<br>`focal_depth_km`<br>`dist_to_active_fault_km`<br>`nearest_fault_slip_type`<br>`prior_count_7d_100km`<br>`prior_count_30d_100km`<br>`prior_count_365d_100km`<br>`prior_max_mag_30d`<br>`cumulative_energy_log_joules`<br>`seismic_rate_accel_ratio`<br>`regional_b_value` | Identical 11 feature names in matching order | Mw<br>km<br>km<br>Categorical<br>Integer count<br>Integer count<br>Integer count<br>Mw<br>log10(J)<br>Ratio<br>Scalar | **CRITICAL DEFECT** | **Arbitrary Feature Substitution:** When no earthquake occurs (count=0), live feature builder defaulted `mainshock_mag = 6.0`, `prior_max_m = 3.2`, and `cum_energy = 9.5`, inventing a non-existent major earthquake. |
| **Cyclones:** `rapid_intensification` | `current_wind_kt`<br>`current_pres_hpa`<br>`dist_to_land_km`<br>`landfall_flag`<br>`past_delta_wind_6h`<br>`past_delta_wind_12h`<br>`past_delta_pres_6h`<br>`translational_speed_kt`<br>`heading_degrees`<br>`coriolis_param`<br>`pot_intensity_headroom` | Identical 11 feature names in matching order | kt<br>hPa<br>km<br>Binary (0/1)<br>kt<br>kt<br>hPa<br>kt<br>deg<br>rad/s<br>kt | **CRITICAL DEFECT** | **Geographic Invalidity:** When evaluating inland mountain locations (e.g. Wayanad), builder supplied dummy values: `current_wind_kt = 45.0`, `dist_to_land_km = 85.0`, forcing the cyclone model to run where no cyclone physically exists. |
| **Floods:** `flood_occurrence` | `precip_1d_mm`<br>`precip_3d_sum_mm`<br>`precip_7d_sum_mm`<br>`precip_14d_sum_mm`<br>`api_14d_index`<br>`temp_2m_celsius`<br>`soil_temp_celsius`<br>`river_discharge_m3s`<br>`river_discharge_7d_mean_m3s`<br>`river_discharge_ratio_7d`<br>`elevation_m`<br>`slope_degrees`<br>`topographic_wetness_index`<br>`distance_to_river_km` | Identical 14 feature names in matching order | mm<br>mm<br>mm<br>mm<br>API index<br>°C<br>°C<br>m³/s<br>m³/s<br>Ratio<br>m<br>deg<br>Scalar<br>km | **PARTIAL MISMATCH** | **Rainfall Interpolation:** Cumulative precipitation ($p_3, p_7, p_{14}$) in `spatial_feature_service.py` was derived using synthetic multipliers ($p_1 \times 1.5$, $p_1 \times 1.8$) when ERA5 reanalysis was slow to respond, distorting multi-day hydrologic accumulation. |
| **Landslides:** `landslide_occurrence` | `precip_1d_mm`<br>`precip_3d_sum_mm`<br>`precip_7d_sum_mm`<br>`precip_30d_sum_mm`<br>`api_30d_index`<br>`temp_2m_celsius`<br>`soil_temp_celsius`<br>`slope_degrees`<br>`elevation_m`<br>`aspect_degrees`<br>`plan_curvature`<br>`soil_clay_fraction_pct`<br>`distance_to_road_km`<br>`distance_to_stream_km` | Identical 14 feature names in matching order | mm<br>mm<br>mm<br>mm<br>API index<br>°C<br>°C<br>deg<br>m<br>deg<br>Scalar<br>%<br>km<br>km | **PARTIAL MISMATCH** | **Static Soil & Road Proxies:** Static default values (`soil_clay_fraction_pct = 28.5`, `distance_to_road_km = 0.45`) used uniformly globally instead of utilizing genuine local geotechnical survey data or open infrastructure maps. |

---

## 2. In-Depth Root Cause: Feature Formula Divergence in Wildfires

### Training Feature Generation (`build_wildfire_dataset.py`):
```python
def compute_fwi_proxy(temp_c, rh_pct, wind_ms, rain_mm):
    t_factor = max(0.0, (temp_c - 10.0) * 0.8)
    rh_deficit = max(0.0, (100.0 - rh_pct) * 0.4)
    w_factor = max(1.0, wind_ms * 1.5)
    r_factor = max(0.1, 1.0 / (1.0 + rain_mm * 0.2))
    raw_fwi = (t_factor + rh_deficit) * w_factor * r_factor * 0.15
    return round(float(np.clip(raw_fwi, 0.0, 100.0)), 2)
```

### Live Feature Generation (`weather_features.py`):
```python
def _calculate_fire_weather_index(self, temp_c, rh_pct, wind_ms, precip_7d, precip_30d):
    rain_deficit = max(0.0, 100.0 - precip_30d)
    drought_factor = min(10.0, max(1.0, 1.0 + (rain_deficit / 12.0) - (precip_7d / 15.0)))
    wind_kmh = wind_ms * 3.6
    ln_df = math.log(max(1.0, drought_factor))
    exponent = -0.450 + (0.987 * ln_df) - (0.0345 * rh_pct) + (0.0338 * temp_c) + (0.0234 * wind_kmh)
    fwi = 2.0 * math.exp(max(-3.0, min(4.0, exponent)))
    return max(0.5, min(100.0, fwi))
```

### Numerical Impact:
For Wayanad ($T = 26.5^\circ\text{C}, RH = 49\%, W = 2.5\text{ m/s}, \text{Precip}_{30d} = 120\text{ mm}$):
- `weather_features.py` yielded: **$0.70$**
- `build_wildfire_dataset.py` would yield: **$18.33$**
- **Discrepancy:** A factor of $26\times$! The model was trained expecting FWI scores on a scale where moderate fire weather is $15–30$. When fed $0.7$, the feature fell outside the learned distribution, while the raw temperature ($26.5^\circ\text{C}$) dominated the decision trees.

---

## 3. Mandatory Engineering Corrections

1. **Standardize Fire Weather Index:** Unify on the standard, scientifically validated Canadian Forest Fire Weather Index (FFMC, DMC, DC, ISI, BUI, FWI) across both dataset preparation and real-time inference.
2. **Strict Gating for Conditional Phenomena:**
   - Earthquakes: Check USGS radial query within $100\text{ km}$ over past 30 days. If $\max(M) < 4.0$, bypass aftershock inference entirely, assign probability $= 0.000$, and set risk to `QUIESCENT`.
   - Cyclones: Check distance to nearest active storm from NOAA/IMD. If distance $> 800\text{ km}$ or location is non-coastal inland, bypass cyclone model, assign risk $= \text{NONE}$.
3. **True Antecedent Precipitation Retrieval:** Eliminate heuristic multipliers ($p_1 \times 1.5$). Always query Open-Meteo multi-day historical precipitation records ($1\text{d}, 3\text{d}, 7\text{d}, 14\text{d}, 30\text{d}$) with fallback to climatological monthly normals.
