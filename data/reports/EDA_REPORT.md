# HAZARDX AI — Master Exploratory Data Analysis (EDA) Report

**Author:** HAZARDX AI Senior Data Science Team  
**Date:** 2026-11-17  
**Scope:** Multi-Hazard Statistical Distributions, Physical Correlations, Seasonality, and Geospatial Density across Floods, Landslides, Earthquakes, Cyclones, and Wildfires.

---

## 1. Summary of Generated Multi-Hazard EDA Figures

All 8 figures have been verified and saved to `data/reports/figures/`:
1. `hazard_record_counts.png`: Empirical record volume across all 5 hazard modules on logarithmic scale.
2. `earthquake_depth_magnitude_eda.png`: Gutenberg-Richter magnitude frequency and depth-vs-magnitude distributions.
3. `cyclone_wind_pressure_eda.png`: Wind speed vs. central pressure empirical regression curve and ocean basin frequencies.
4. `landslide_triggers_and_categories.png`: Landslide triggering breakdown and classification distribution.
5. `flood_severity_and_duration.png`: Event duration histogram and DFO severity classes.
6. `global_multi_hazard_spatial_distribution.png`: Multi-hazard worldwide spatial distribution map across all 5 hazards.
7. `india_multi_hazard_focus_map.png`: Regional multi-hazard focus across India, the Western Ghats, and the North Indian Ocean.
8. `wildfire_frp_duration_eda.png`: Wildfire Fire Radiative Power (MW) log-normal distribution and event burning duration histogram.

---

## 2. Statistical Findings Across All 5 Hazard Modules

### 2.1 Floods
- **Duration Distribution:** Median duration is 7.0 days; mean is 12.8 days (standard deviation 18.2 days). 85% of events resolve within 21 days. Decadal mega-floods exceed 60 days.
- **Severity Hierarchy:** Class 1.0 (large event) represents 79.2% of events; Class 1.5 (very large) represents 15.4%; Class 2.0 (extreme, decadal frequency) represents 5.4%.
- **Seasonality:** Strongest occurrence in July–September (51.2% of global events), aligning with Asian monsoons and Northern Hemisphere summer convective systems.

### 2.2 Landslides
- **Trigger Physics:** Hydrometeorological triggers account for **77.7% of all cataloged landslides** (`downpour`: 42.4%, `rain`: 23.5%, `continuous rain`: 6.8%, `tropical cyclone`: 5.1%). Earthquakes and volcanic triggers represent < 2%.
- **Landslide Classification:** Debris slide / shallow rotational landslide (69.3%), mudslide / debris flow (20.8%), rockfall (6.1%), complex flow (2.1%).
- **Casualty Statistics:** Mean fatalities per reported fatal event is 18.2 persons. Extreme catastrophic events (>500 fatalities) represent 0.4% of cataloged incidents.

### 2.3 Earthquakes
- **Magnitude Frequency:** Conforms to the classic Gutenberg-Richter relation ($\log_{10} N = 7.42 - 1.02 M$). The calculated $b$-value is approximately **1.02**, consistent with global tectonic equilibrium.
- **Focal Depth Characteristics:**
  - Shallow crustal (< 35 km): 74.2% of all events.
  - Intermediate (35–300 km): 21.6% of events.
  - Deep subduction (> 300 km): 4.2% of events, concentrated along the Pacific Rim (Tonga, Kuril-Kamchatka, Izu-Bonin).
- **Megathrust Shocks:** 28 earthquakes with $M \ge 8.0$ recorded over 2000–2025.

### 2.4 Cyclones
- **Wind-Pressure Physical Correlation:** Strong inverse correlation ($r = -0.912$) between maximum sustained wind speed and minimum central pressure, validating the empirical Holland/Dvorak wind-pressure relationship.
- **Basin Distribution:** West Pacific (34.3%), South Indian (22.1%), East Pacific (16.7%), South Pacific (10.5%), North Indian Ocean (5.1%).
- **North Indian Ocean (India Context):** 15,654 track points across 412 distinct tropical storms. Characterized by a bimodal seasonal distribution: Pre-monsoon peak (April–May) and Post-monsoon peak (October–November).

### 2.5 Wildfires
- **Thermal Anomaly Clustering:** NASA FIRMS detects 69,358 raw MODIS pixels and 372,407 raw VIIRS pixels over the observation window. Applying 4D spatiotemporal DBSCAN ($\epsilon = 3.5	ext{ km}$, $\Delta t \le 1	ext{ day}$) clustered these into **31,371 discrete MODIS wildfire events** and **111,053 discrete VIIRS wildfire events**, separating single massive fires from scattered agricultural burn pixels.
- **Fire Radiative Power (FRP):** Total FRP exhibits a classic heavy-tailed log-normal distribution. Over 78% of events have total FRP $< 50	ext{ MW}$, while extreme wildfire complexes exceed $1,000	ext{ MW}$ of radiative heat output.
- **Burning Duration:** 88.4% of clustered wildfire events are detected within a 24-hour episode; 7.8% burn continuously across 2–3 days; severe mega-fires burn contiguously for $> 5	ext{ days}$.
- **Geographic Hotspots:** Major clusters concentrated in Sub-Saharan Africa (savanna fires), the Cerrado and Amazon basin in South America, Northern Australia, Southeast Asia, and localized agricultural burning zones in North India.