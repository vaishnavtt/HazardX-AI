# Phase 37 — Tropical Cyclone Hazard Validation & Elevation Gate Audit

## 1. Audit of the 300m Elevation Restriction

In `backend/app/api/v1/endpoints/geospatial.py` (lines 164–165):
```python
if abs(lat) <= 45.0 and env_context.elevation_m <= 300.0:
    # evaluate cyclone model
else:
    # return probability = 0.0, alert_level = "GREEN", guidance = "Inland continental/mountain location..."
```

### 1.1 Meteorological & Historical Flaw
Tropical cyclones are synoptic-scale atmospheric vortices spanning $500\text{ km}$ to $1,000\text{ km}$ in diameter. While their core warm-water thermodynamic engine weakens over land due to frictional dissipation and loss of latent heat flux, their impacts extend far inland and into high-altitude topography:

1. **Orographic Precipitation Amplification:**
   When tropical cyclone outer rainbands encounter coastal mountain barriers, forced orographic uplift intensifies rainfall rates by $200\% - 400\%$.
   - *Hurricane Helene (September 2024):* Devastated mountain communities in western North Carolina at elevations of $600\text{ m} - 1,500\text{ m}$ (Asheville elev. $650\text{ m}$), generating decadal floods.
   - *Super Typhoon Morakot (August 2009):* Dumped $2,777\text{ mm}$ of rain at Mount Ali, Taiwan (elevation $2,200\text{ m}$), burying villages in debris flows.
   - *Cyclone Ockhi (December 2017):* Generated gale-force gusts and heavy downpours across the Western Ghats mountain ranges of Kerala at elevations $> 1,000\text{ m}$.
2. **Terrain-Amplified Wind Speeds:**
   Wind speeds over mountain ridges and windward gaps frequently accelerate due to the Venturi effect, producing gusts significantly higher than sea-level measurements.

**Critical Finding:** Hardcoding `elevation_m <= 300.0` as an automatic zero-risk gate creates an unacceptable blind spot. Any mountain community at $301\text{ m}$ elevation within $50\text{ km}$ of a landfalling Category 4 cyclone was assigned a `0.0%` cyclone threat level and a `GREEN` alert by `geospatial.py`.

---

## 2. Active Storm Proximity vs. Fixed Elevation Cutoff

The proper physical determinant of tropical cyclone wind and rain hazard is:
1. **Distance to Vortex Center ($D_{\text{storm}}$):** Evaluated against the storm's actual wind radii (R34, R50, R64 knots).
2. **Current & Projected Intensity ($V_{\text{max}}$):** From official RSMC/NHC/IMD advisories.
3. **Local NWP Forecast Wind Gusts:** High-resolution numerical weather prediction (e.g. Open-Meteo ECMWF/GFS) already models surface winds over realistic topography, incorporating terrain elevation friction.

**Mandated Correction:**
The 300m elevation hard restriction must be **completely removed**. The cyclone service must evaluate whether any active tropical depression or cyclone exists within $800\text{ km}$, and combine track proximity with local NWP wind forecasts.
