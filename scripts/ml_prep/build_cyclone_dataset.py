"""
HAZARDX AI - ML Dataset Engineering: Cyclones Module
Constructs a scientifically valid, model-ready training dataset for 24-Hour
Tropical Cyclone Intensity Change (Delta V_24h) & Rapid Intensification (RI) Prediction.

Features (Available strictly at or before observation time t0):
  - Current Intensity: Maximum sustained wind (current_wind_kt), Minimum pressure (current_pres_hpa)
  - Current Position: Latitude, Longitude, Ocean Basin, Distance to Land (dist2land_km), Landfall flag
  - Past Intensity Trends:
      * 6-hour wind change (past_delta_wind_6h)
      * 12-hour wind change (past_delta_wind_12h)
      * 6-hour pressure change (past_delta_pres_6h)
  - Track Kinematics:
      * Translational speed (translational_speed_kt)
      * Track heading / Azimuth (heading_degrees)
  - Dynamic / Environmental Proxies:
      * Coriolis parameter (coriolis_param)
      * Potential intensity headroom (pot_intensity_headroom)

Targets (Evaluated strictly at t0 + 24 hours):
  - delta_wind_24h: Continuous 24-hour intensity change (knots)
  - rapid_intensification: Binary indicator (1 if Delta V_24h >= 30 kt; 0 otherwise)
  - future_wind_24h: Continuous sustained wind speed at t0 + 24h

Validation:
  - Storm-level Grouped Temporal Validation:
      * Train: Storm seasons <= 2017
      * Validation: Storm seasons 2018-2021
      * Test: Storm seasons 2022-2027
  - Strict grouping on Storm ID (SID): All observations of any given storm
    belong exclusively to a single split, completely eliminating track autocorrelation leakage.
"""

import os
import json
import time
import math
import numpy as np
import pandas as pd

PROC_CYC_FILE = 'data/processed/cyclones/cyclone_tracks_cleaned_catalog.csv'
MODEL_READY_DIR = 'data/model_ready/cyclones'
os.makedirs(MODEL_READY_DIR, exist_ok=True)

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp = np.radians(lat2 - lat1)
    dl = np.radians(lon2 - lon1)
    a = np.sin(dp / 2.0)**2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2.0)**2
    return 2.0 * R * np.arcsin(np.sqrt(np.clip(a, 0.0, 1.0)))

def calculate_heading(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dl = np.radians(lon2 - lon1)
    x = np.sin(dl) * np.cos(p2)
    y = np.cos(p1) * np.sin(p2) - np.sin(p1) * np.cos(p2) * np.cos(dl)
    initial_bearing = np.degrees(np.arctan2(x, y))
    return (initial_bearing + 360.0) % 360.0

def build_cyclone_model_ready_dataset():
    print("="*70)
    print("TASK 1-4: BUILDING MODEL-READY CYCLONE TRAINING MATRIX")
    print("="*70)
    
    t0 = time.time()
    print("[IBTrACS Catalog] Loading cleaned cyclone track observations...")
    df = pd.read_csv(PROC_CYC_FILE, low_memory=False)
    print(f"[IBTrACS Catalog] Loaded {len(df):,} track observations across {df['SID'].nunique():,} storms.")
    
    # Sort chronologically by storm and time
    df['time_dt'] = pd.to_datetime(df['ISO_TIME'])
    df = df.sort_values(['SID', 'time_dt']).reset_index(drop=True)
    
    # Clean numeric types
    df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
    df['LON'] = pd.to_numeric(df['LON'], errors='coerce')
    df['USA_WIND'] = pd.to_numeric(df['USA_WIND'], errors='coerce')
    df['USA_PRES'] = pd.to_numeric(df['USA_PRES'], errors='coerce')
    df['DIST2LAND'] = pd.to_numeric(df['DIST2LAND'], errors='coerce').fillna(500.0)
    df['LANDFALL'] = pd.to_numeric(df['LANDFALL'], errors='coerce').fillna(0).astype(int)
    
    # If USA_PRES is missing, impute using empirical Dvorak wind-pressure relation:
    # P_c ~ 1012 - (V / 1.45)^1.2
    v_clean = df['USA_WIND'].fillna(35.0)
    pres_est = 1014.0 - 0.75 * v_clean - 0.002 * (v_clean ** 2)
    df['USA_PRES'] = df['USA_PRES'].fillna(pres_est)
    
    print("[Feature Engineering] Computing track kinematics & past intensity trends...")
    # Group by Storm ID (SID)
    grp = df.groupby('SID')
    
    # Past 6h (shift 2 steps on 3-hourly data) and Past 12h (shift 4 steps)
    df['past_lat_6h'] = grp['LAT'].shift(2)
    df['past_lon_6h'] = grp['LON'].shift(2)
    df['past_time_6h'] = grp['time_dt'].shift(2)
    df['past_wind_6h'] = grp['USA_WIND'].shift(2)
    df['past_wind_12h'] = grp['USA_WIND'].shift(4)
    df['past_pres_6h'] = grp['USA_PRES'].shift(2)
    
    # Forward 24-hour target (shift -8 steps on 3-hourly data)
    df['future_wind_24h'] = grp['USA_WIND'].shift(-8)
    df['future_time_24h'] = grp['time_dt'].shift(-8)
    
    # Verify exact 24-hour time delta (21 to 27 hours)
    df['delta_hours_future'] = (df['future_time_24h'] - df['time_dt']).dt.total_seconds() / 3600.0
    
    # Filter valid pairs
    valid_mask = (
        df['USA_WIND'].notnull() & 
        df['future_wind_24h'].notnull() &
        (df['delta_hours_future'] >= 21.0) & 
        (df['delta_hours_future'] <= 27.0)
    )
    df_valid = df[valid_mask].copy()
    print(f"[Pairs] Valid 24-hour forecast instances: {len(df_valid):,} track points")
    
    # Calculate Past Intensity Trends
    df_valid['past_delta_wind_6h'] = (df_valid['USA_WIND'] - df_valid['past_wind_6h']).fillna(0.0)
    df_valid['past_delta_wind_12h'] = (df_valid['USA_WIND'] - df_valid['past_wind_12h']).fillna(0.0)
    df_valid['past_delta_pres_6h'] = (df_valid['USA_PRES'] - df_valid['past_pres_6h']).fillna(0.0)
    
    # Calculate Translational Velocity & Heading
    p_lat = df_valid['past_lat_6h'].fillna(df_valid['LAT'])
    p_lon = df_valid['past_lon_6h'].fillna(df_valid['LON'])
    step_dist_km = haversine_km(p_lat, p_lon, df_valid['LAT'], df_valid['LON'])
    df_valid['translational_speed_kt'] = np.round((step_dist_km / 6.0) * 0.539957, 1)  # km/h to knots
    df_valid['translational_speed_kt'] = np.clip(df_valid['translational_speed_kt'], 0.0, 50.0)
    
    df_valid['heading_degrees'] = np.round(calculate_heading(p_lat, p_lon, df_valid['LAT'], df_valid['LON']), 1)
    
    # Coriolis parameter: f = 2 * Omega * sin(lat)
    omega = 7.2921e-5
    df_valid['coriolis_param'] = np.round(2.0 * omega * np.sin(np.radians(df_valid['LAT'])), 7)
    
    # Potential Intensity Headroom: MPI ~ 170 kt - V_0
    df_valid['pot_intensity_headroom'] = np.round(np.maximum(0.0, 165.0 - df_valid['USA_WIND']), 1)
    
    # Compute Target Variables
    df_valid['delta_wind_24h'] = np.round(df_valid['future_wind_24h'] - df_valid['USA_WIND'], 1)
    df_valid['rapid_intensification'] = np.where(df_valid['delta_wind_24h'] >= 30.0, 1, 0)
    
    # Assign Grouped Temporal Split on Storm ID (SID) & SEASON
    df_valid['SEASON'] = pd.to_numeric(df_valid['SEASON'], errors='coerce').fillna(2000).astype(int)
    
    df_valid['split'] = 'train'
    df_valid.loc[df_valid['SEASON'] >= 2018, 'split'] = 'val'
    df_valid.loc[df_valid['SEASON'] >= 2022, 'split'] = 'test'
    
    # Clean and reorder columns
    cols = [
        'SID', 'NAME', 'SEASON', 'BASIN', 'ISO_TIME', 'LAT', 'LON',
        # Input Features (Strictly antecedent & current)
        'USA_WIND', 'USA_PRES', 'DIST2LAND', 'LANDFALL',
        'past_delta_wind_6h', 'past_delta_wind_12h', 'past_delta_pres_6h',
        'translational_speed_kt', 'heading_degrees', 'coriolis_param', 'pot_intensity_headroom',
        # Target Variables (Strictly +24 hours)
        'delta_wind_24h', 'rapid_intensification', 'future_wind_24h',
        # Grouped Split
        'split'
    ]
    df_out = df_valid[cols].copy()
    df_out = df_out.rename(columns={
        'USA_WIND': 'current_wind_kt',
        'USA_PRES': 'current_pres_hpa',
        'DIST2LAND': 'dist_to_land_km',
        'LANDFALL': 'landfall_flag',
        'LAT': 'latitude',
        'LON': 'longitude',
        'ISO_TIME': 'timestamp',
        'BASIN': 'ocean_basin'
    })
    
    out_file = os.path.join(MODEL_READY_DIR, 'cyclone_model_ready.csv')
    df_out.to_csv(out_file, index=False)
    print(f"\n[OUTPUT] Saved model-ready cyclone dataset: {out_file}")
    print(f"  - Total records: {len(df_out):,}")
    print(f"  - Unique storms represented: {df_out['SID'].nunique():,}")
    print(f"  - Rapid Intensification cases (RI=1): {(df_out['rapid_intensification'] == 1).sum():,} ({float(df_out['rapid_intensification'].mean())*100:.2f}%)")
    print(f"  - Input feature count: 11 engineered kinematic/intensity features")
    print(f"  - Split distribution: {df_out['split'].value_counts().to_dict()}")
    print(f"  - Storm count per split: {df_out.groupby('split')['SID'].nunique().to_dict()}")
    print(f"  - Missing values: {df_out.isnull().sum().sum()}")
    
    meta = {
        "hazard": "Cyclones",
        "task": "24-Hour Tropical Cyclone Intensity Change & Rapid Intensification (RI) Prediction",
        "dataset_file": out_file,
        "record_count": len(df_out),
        "storm_count": int(df_out['SID'].nunique()),
        "feature_count": 11,
        "input_features": [
            "current_wind_kt", "current_pres_hpa", "dist_to_land_km", "landfall_flag",
            "past_delta_wind_6h", "past_delta_wind_12h", "past_delta_pres_6h",
            "translational_speed_kt", "heading_degrees", "coriolis_param", "pot_intensity_headroom"
        ],
        "target_variables": {
            "delta_wind_24h": "Continuous 24-hour wind speed change (knots)",
            "rapid_intensification": "Binary indicator (1 = Delta V >= 30 kt in 24 hours, 0 = non-RI)",
            "future_wind_24h": "Continuous sustained wind speed at t0 + 24 hours (knots)"
        },
        "validation_strategy": "Storm-Level Grouped Chronological Split: train (<=2017), val (2018-2021), test (>=2022). All observations of any given storm belong exclusively to a single split.",
        "class_balance": {
            "rapid_intensification_count": int((df_out['rapid_intensification'] == 1).sum()),
            "non_ri_count": int((df_out['rapid_intensification'] == 0).sum()),
            "ri_percentage": round(float(df_out['rapid_intensification'].mean()) * 100, 2)
        }
    }
    with open(os.path.join(MODEL_READY_DIR, 'cyclone_features_metadata.json'), 'w') as f:
        json.dump(meta, f, indent=2)

if __name__ == '__main__':
    build_cyclone_model_ready_dataset()

