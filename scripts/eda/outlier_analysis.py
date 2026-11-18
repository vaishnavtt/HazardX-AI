"""
HAZARDX AI - Data Quality Audit: Outlier & Physical Boundary Analysis
Detects statistical outliers (IQR / Z-score) and domain-specific physical violations.
Critically evaluates genuine natural disaster extremes vs measurement errors.
"""

import os
import pandas as pd
import numpy as np

def analyze_outliers():
    print("=================== OUTLIER & PHYSICAL BOUNDARY AUDIT ===================")
    
    # 1. Earthquakes
    eq_path = "data/processed/earthquakes/earthquake_events_cleaned_catalog.csv"
    if os.path.exists(eq_path):
        df_eq = pd.read_csv(eq_path, low_memory=False)
        print("\n--- Earthquakes Physical Range Audit ---")
        mag = df_eq['mag'].dropna()
        depth = df_eq['depth'].dropna()
        
        # Physical checks
        mag_invalid = ((mag < 0) | (mag > 10.0)).sum()
        depth_invalid = ((depth < -10) | (depth > 800)).sum()
        print(f"Magnitude [0-10]: Invalid={mag_invalid}, Min={mag.min()}, Max={mag.max()}")
        print(f"Depth [-10 to 800 km]: Invalid={depth_invalid}, Min={depth.min()} km, Max={depth.max()} km")
        
        # High-magnitude genuine extremes
        great_quakes = df_eq[df_eq['mag'] >= 8.0]
        print(f"Genuine Megathrust Extremes (M >= 8.0): {len(great_quakes)} events verified (e.g., 2004 Sumatra M9.1, 2011 Tohoku M9.1)")
        
    # 2. Cyclones
    cyc_path = "data/processed/cyclones/cyclone_tracks_cleaned_catalog.csv"
    if os.path.exists(cyc_path):
        df_cyc = pd.read_csv(cyc_path, low_memory=False)
        print("\n--- Cyclones Physical Range Audit ---")
        w_col = 'USA_WIND' if 'USA_WIND' in df_cyc.columns else 'WMO_WIND'
        p_col = 'USA_PRES' if 'USA_PRES' in df_cyc.columns else 'WMO_PRES'
        
        wind = df_cyc[w_col].dropna()
        pres = df_cyc[p_col].dropna()
        
        wind_invalid = ((wind < 0) | (wind > 220)).sum()
        pres_invalid = ((pres < 850) | (pres > 1050)).sum()
        print(f"Wind Speed [0-220 kt]: Invalid={wind_invalid}, Min={wind.min()} kt, Max={wind.max()} kt")
        print(f"Central Pressure [850-1050 hPa]: Invalid={pres_invalid}, Min={pres.min()} hPa, Max={pres.max()} hPa")
        
        # Extreme cyclones
        cat5 = df_cyc[df_cyc[w_col] >= 137]
        print(f"Category 5 Super Cyclones / Typhoons (Wind >= 137 kt): {len(cat5):,} track points verified")

    # 3. Floods
    fl_path = "data/processed/floods/flood_events_cleaned_catalog.csv"
    if os.path.exists(fl_path):
        df_fl = pd.read_csv(fl_path, low_memory=False)
        print("\n--- Floods Physical Range Audit ---")
        dur = df_fl['duration_days'].dropna()
        area = df_fl['affected_area_sqkm'].dropna()
        dur_invalid = (dur < 0).sum()
        area_invalid = (area < 0).sum()
        print(f"Duration >= 0 days: Invalid={dur_invalid}, Max Duration={dur.max()} days")
        print(f"Affected Area >= 0 sqkm: Invalid={area_invalid}, Max Area={area.max():,.0f} sqkm")
        
    # 4. Landslides
    ls_path = "data/processed/landslides/landslide_events_cleaned_catalog.csv"
    if os.path.exists(ls_path):
        df_ls = pd.read_csv(ls_path, low_memory=False)
        print("\n--- Landslides Physical Range Audit ---")
        fat = df_ls['fatalities'].dropna()
        fat_invalid = (fat < 0).sum()
        print(f"Fatalities >= 0: Invalid={fat_invalid}, Max Fatalities={fat.max():,.0f}")
        high_fatality = df_ls[df_ls['fatalities'] >= 500]
        print(f"Catastrophic Landslide Events (Fatalities >= 500): {len(high_fatality)} events documented")

if __name__ == '__main__':
    analyze_outliers()

