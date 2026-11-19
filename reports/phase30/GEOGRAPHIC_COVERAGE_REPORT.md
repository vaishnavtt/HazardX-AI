# HAZARDX AI – Phase 30: Geographic Coverage Report

**Date:** November 19, 2026  
**Auditor:** Senior Geospatial Intelligence & Climatology Group  
**Scope:** Spatial Distribution & Regional Generalization Bounds Across All Hazard Models  

---

## 1. Geographic Sample Distribution

| Hazard Domain | Global Latitude Span | Global Longitude Span | Primary Concentration | Subcontinent Representation (India/South Asia) |
| :--- | :--- | :--- | :--- | :--- |
| **Cyclones** | $-45.5^\circ\text{ to }+65.0^\circ$ | $-179.9^\circ\text{ to }+180.0^\circ$ | Western Pacific, North Atlantic, Indian Ocean | **14,210 track points** in North Indian Ocean (Bay of Bengal & Arabian Sea). Excellent coverage. |
| **Earthquakes** | $-77.1^\circ\text{ to }+86.3^\circ$ | $-180.0^\circ\text{ to }+180.0^\circ$ | Circum-Pacific Ring of Fire, Alpine-Himalayan belt | **842 seismic events** along the Himalayan arc, Andaman Sea, and Indo-Burmese wedge. Excellent tectonic coverage. |
| **Floods** | $-38.0^\circ\text{ to }+65.4^\circ$ | $-173.5^\circ\text{ to }+153.2^\circ$ | Global major river basins | **240 out of 600 points (40.0%)** across Indus, Ganges, Brahmaputra, Godavari, and Periyar basins. Good regional representation. |
| **Landslides** | $-45.9^\circ\text{ to }+57.6^\circ$ | $-170.7^\circ\text{ to }+178.4^\circ$ | High-relief orogens (Himalayas, Andes, Alps, Western Ghats) | **246 out of 600 points (41.0%)** located in Indian mountain belts (Uttarakhand, Himachal, Western Ghats / Kerala). Good regional representation. |
| **Wildfires** | $-38.4^\circ\text{ to }+68.6^\circ$ | $-156.7^\circ\text{ to }+150.8^\circ$ | Boreal North America, Western US, Australia | **Only 6 out of 1,200 points (0.5%)** in India. Extreme high-latitude bias ($52.5^\circ\text{N}$ median). **Severe geographic blindspot**. |

---

## 2. Generalization Capacity to Kerala & South Asia

### 2.1 Kerala Regional Dynamics:
- **Geography:** Western Ghats escarpment abruptly descending to coastal plains within $40–70\text{ km}$.
- **Climate:** Tropical monsoon (Köppen *Am*); receives $3,000–5,000\text{ mm}$ annual rainfall, concentrated between June and October.
- **Landslides in Kerala:** Shallow translational debris flows triggered by extreme antecedent rainfall (e.g. Meppadi/Chooralmala landslide in Wayanad, July 30, 2024: $572\text{ mm}$ rain in 48 hours on $34^\circ$ slopes). The landslide model possesses adequate terrain sensitivity, but requires genuine rainfall triggers rather than dry-day predictions.
- **Wildfires in Kerala:** Wildfires in Kerala are confined to dry deciduous forest edges during the peak dry pre-monsoon season (February–April). In November, humid inter-monsoon conditions render wildfire ignition nearly impossible (FWI $< 2.0$, zero active FIRMS detections). The model's failure in Wayanad was directly caused by its high-latitude training distribution.

### 2.2 Global Geographic Transfer Boundaries:
- **Himalayan Corridor:** Well-represented for landslides and earthquakes; high predictive reliability.
- **North America & Mediterranean:** High wildfire accuracy; models reflect semi-arid and chaparral fire ecology.
- **Equatorial Tropics (Amazonia, Congo Basin, Southeast Asia):** Extreme distribution shift for the wildfire model. Must rely on Canadian FWI and FIRMS thermal hotspots.

---

## 3. Geographic Governance Flags

When evaluating locations outside a model's validated geographic domain:
1. If wildfire evaluation is conducted in equatorial/tropical humid biomes without active satellite hotspots:
   - Suppress the uncalibrated ML score.
   - Display: **`LOW FIRE DANGER – TROPICAL HUMID ENVIRONMENT (NO ACTIVE HOTSPOTS)`**.
2. If cyclone evaluation is conducted inland ($> 200\text{ km}$ from coastline) or outside active storm tracks:
   - Suppress the offshore storm model.
   - Display: **`NO CYCLONIC THREAT – INLAND CONTINENTAL REGION`**.
3. If earthquake evaluation is conducted in stable cratonic interiors with zero seismicity:
   - Suppress fictitious mainshock defaults.
   - Display: **`QUIESCENT – STABLE CRATONIC ZONE`**.
