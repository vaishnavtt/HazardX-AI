"""
HAZARDX AI - ML Dataset Engineering: Earthquakes Module
Constructs a scientifically valid, model-ready training dataset for Regional
Seismic Activity & Aftershock Hazard Assessment.

Important Scientific Principle:
  Deterministic earthquake prediction (exact time, coordinate, and magnitude)
  is physically impossible and rejected by international seismological consensus.
  This dataset is formulated for statistical regional hazard assessment:
  predicting whether a region experiencing a significant seismic event (M >= 5.0)
  will exhibit elevated aftershock rates or large secondary ruptures within
  the subsequent 30 days.

Features (Available strictly at or before prediction time t0):
  - Current seismic parameters: Magnitude (mag), Focal Depth (depth_km)
  - Tectonic fault proximity: Shortest 3D distance to GEM active fault, Fault slip type
  - Preceding seismicity history within 100 km:
      * 7-day, 30-day, and 365-day earthquake frequency
      * 30-day maximum prior magnitude
      * Log cumulative seismic energy release (Joules)
      * Preceding seismicity rate acceleration ratio
      * Regional Gutenberg-Richter b-value estimate

Targets (Evaluated strictly in subsequent window [t0, t0 + 30 days] within 100 km):
  - elevated_aftershock_hazard: Binary (1 = >=5 aftershocks or secondary M>=5.0, 0 = low/quiescent)
  - aftershock_count_30d: Continuous count of subsequent events
  - max_aftershock_mag_30d: Maximum magnitude in subsequent 30 days

Validation:
  - Walk-forward temporal split: Train (2000-2018), Val (2019-2021), Test (2022-2025)
  - Zero temporal information leakage.
"""

import os
import json
import time
import math
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

PROC_EQ_FILE = 'data/processed/earthquakes/earthquake_events_cleaned_catalog.csv'
GEM_FAULT_FILE = 'data/raw/earthquakes/gem_active_faults.geojson'
MODEL_READY_DIR = 'data/model_ready/earthquakes'
os.makedirs(MODEL_READY_DIR, exist_ok=True)

def load_gem_fault_tree():
    print("[GEM Faults] Loading active faults and building spatial KDTree...")
    t0 = time.time()
    with open(GEM_FAULT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    pts = []
    slip_types = []
    for feat in data.get('features', []):
        st = feat.get('properties', {}).get('slip_type', 'Unknown')
        geom = feat.get('geometry', {})
        coords = geom.get('coordinates', [])
        gtype = geom.get('type')
        if gtype == 'LineString':
            for c in coords:
                pts.append((c[1], c[0]))
                slip_types.append(st)
        elif gtype == 'MultiLineString':
            for line in coords:
                for c in line:
                    pts.append((c[1], c[0]))
                    slip_types.append(st)
                    
    pts = np.array(pts)
    lat_r = np.radians(pts[:, 0])
    lon_r = np.radians(pts[:, 1])
    R = 6371.0
    x = R * np.cos(lat_r) * np.cos(lon_r)
    y = R * np.cos(lat_r) * np.sin(lon_r)
    z = R * np.sin(lat_r)
    
    tree = cKDTree(np.column_stack([x, y, z]))
    print(f"[GEM Faults] Indexed {len(pts):,} fault vertices in {time.time()-t0:.2f}s.")
    return tree, np.array(slip_types)

def build_earthquake_model_ready_dataset(sample_size=10000):
    print("="*70)
    print("TASK 1-4: BUILDING MODEL-READY EARTHQUAKE TRAINING MATRIX")
    print("="*70)
    
    # 1. Load full tectonic catalog (681,902 events)
    print("[Earthquake Catalog] Loading 681,902 verified tectonic earthquakes...")
    t0 = time.time()
    cols = ['event_id', 'time', 'latitude', 'longitude', 'depth', 'mag', 'magType']
    df_all = pd.read_csv(PROC_EQ_FILE, usecols=cols, low_memory=False)
    df_all['time_dt'] = pd.to_datetime(df_all['time'])
    df_all = df_all.sort_values('time_dt').reset_index(drop=True)
    print(f"[Earthquake Catalog] Loaded {len(df_all):,} records in {time.time()-t0:.2f}s.")
    
    # 2. Build 3D spatial KDTree for the full earthquake catalog to rapidly query 100km neighbors
    lat_rad = np.radians(df_all['latitude'].values)
    lon_rad = np.radians(df_all['longitude'].values)
    R = 6371.0
    eq_x = R * np.cos(lat_rad) * np.cos(lon_rad)
    eq_y = R * np.cos(lat_rad) * np.sin(lon_rad)
    eq_z = R * np.sin(lat_rad)
    eq_pts = np.column_stack([eq_x, eq_y, eq_z])
    eq_tree = cKDTree(eq_pts)
    
    # Timestamps in unix epoch seconds for fast temporal filtering
    eq_timestamps = df_all['time_dt'].values.astype('datetime64[s]').astype(np.int64)
    eq_mags = df_all['mag'].values
    
    # 3. Build Fault KDTree
    fault_tree, fault_slip_types = load_gem_fault_tree()
    
    # 4. Filter candidate seismic trigger events (M >= 5.0)
    # Exclude boundary margins (first 365 days and last 30 days) to allow complete feature history and future targets
    min_date = df_all['time_dt'].min() + pd.Timedelta(days=365)
    max_date = df_all['time_dt'].max() - pd.Timedelta(days=30)
    
    candidates = df_all[
        (df_all['mag'] >= 5.0) & 
        (df_all['time_dt'] >= min_date) & 
        (df_all['time_dt'] <= max_date)
    ].copy()
    print(f"[Candidates] Valid trigger events with M >= 5.0 within valid temporal buffer: {len(candidates):,}")
    
    # Stratified / Systematic sample across time to target sample_size
    if len(candidates) > sample_size:
        candidates = candidates.sample(n=sample_size, random_state=42).sort_values('time_dt').reset_index(drop=True)
    print(f"[Sampling] Evaluating {len(candidates):,} candidate seismic sequence anchors...")
    
    # 5. Extract Features & Future Targets
    t1 = time.time()
    rows = []
    
    # Query fault distances for all candidates at once
    cand_lat_r = np.radians(candidates['latitude'].values)
    cand_lon_r = np.radians(candidates['longitude'].values)
    cand_x = R * np.cos(cand_lat_r) * np.cos(cand_lon_r)
    cand_y = R * np.cos(cand_lat_r) * np.sin(cand_lon_r)
    cand_z = R * np.sin(cand_lat_r)
    cand_pts = np.column_stack([cand_x, cand_y, cand_z])
    
    fault_dists, fault_indices = fault_tree.query(cand_pts, k=1)
    
    # Chord distance corresponding to 100 km radius
    r_100km = 2 * R * np.sin(100.0 / (2 * R))
    
    sec_7d = 7 * 86400
    sec_30d = 30 * 86400
    sec_365d = 365 * 86400
    
    for i in range(len(candidates)):
        c_row = candidates.iloc[i]
        c_t = eq_timestamps[c_row.name]
        c_pt = cand_pts[i]
        
        # Spatial neighbors within 100 km
        nb_indices = eq_tree.query_ball_point(c_pt, r=r_100km)
        nb_indices = np.array(nb_indices)
        nb_times = eq_timestamps[nb_indices]
        nb_mags = eq_mags[nb_indices]
        
        # Prior Seismicity (t < c_t)
        prior_mask = (nb_times < c_t)
        prior_times = nb_times[prior_mask]
        prior_mags = nb_mags[prior_mask]
        
        # Prior 7 days
        mask_7d = (prior_times >= c_t - sec_7d)
        prior_count_7d = int(mask_7d.sum())
        
        # Prior 30 days
        mask_30d = (prior_times >= c_t - sec_30d)
        prior_count_30d = int(mask_30d.sum())
        prior_mags_30d = prior_mags[mask_30d]
        prior_max_mag_30d = float(prior_mags_30d.max()) if len(prior_mags_30d) > 0 else 0.0
        
        # Prior 365 days
        mask_365d = (prior_times >= c_t - sec_365d)
        prior_count_365d = int(mask_365d.sum())
        
        # Cumulative seismic energy release in prior 30 days: E = 10^(4.8 + 1.5 * M)
        if len(prior_mags_30d) > 0:
            energies = 10.0 ** (4.8 + 1.5 * prior_mags_30d)
            cum_energy_log = float(np.log10(np.sum(energies) + 1.0))
        else:
            cum_energy_log = 0.0
            
        # Regional b-value estimate (Aki 1965 formula: b = log10(e) / (mean(M) - M_min))
        if len(prior_mags) >= 10:
            m_min = 2.5
            valid_m = prior_mags[prior_mags >= m_min]
            if len(valid_m) >= 5:
                mean_m = float(np.mean(valid_m))
                b_val = round(float(np.log10(np.e) / max(0.1, mean_m - m_min)), 3)
            else:
                b_val = 1.0
        else:
            b_val = 1.0
            
        # Rate acceleration ratio: (N_7d / 7) / ((N_30d + 1) / 30)
        rate_7d = prior_count_7d / 7.0
        rate_30d = (prior_count_30d + 1.0) / 30.0
        accel_ratio = round(rate_7d / rate_30d, 2)
        
        # Future Target Window: [c_t + 1, c_t + 30 days] within 100 km
        future_mask = (nb_times > c_t) & (nb_times <= c_t + sec_30d)
        future_mags = nb_mags[future_mask]
        aftershock_count_30d = int(len(future_mags))
        max_aftershock_mag_30d = round(float(future_mags.max()), 2) if aftershock_count_30d > 0 else 0.0
        
        # Binary hazard target: 1 if >= 5 aftershocks OR any aftershock with M >= 5.0
        elevated_hazard = 1 if (aftershock_count_30d >= 5 or max_aftershock_mag_30d >= 5.0) else 0
        
        # Split assignment (Chronological)
        yr = c_row['time_dt'].year
        if yr <= 2018:
            split_label = 'train'
        elif yr <= 2021:
            split_label = 'val'
        else:
            split_label = 'test'
            
        rows.append({
            'event_id': c_row['event_id'],
            'timestamp': str(c_row['time']),
            'latitude': round(float(c_row['latitude']), 4),
            'longitude': round(float(c_row['longitude']), 4),
            # Current Source Features
            'mainshock_mag': round(float(c_row['mag']), 2),
            'focal_depth_km': round(float(c_row['depth']), 2),
            # Tectonic Fault Features (GEM)
            'dist_to_active_fault_km': round(float(fault_dists[i]), 2),
            'nearest_fault_slip_type': fault_slip_types[fault_indices[i]],
            # Prior Seismicity Features (strictly antecedent)
            'prior_count_7d_100km': prior_count_7d,
            'prior_count_30d_100km': prior_count_30d,
            'prior_count_365d_100km': prior_count_365d,
            'prior_max_mag_30d': round(prior_max_mag_30d, 2),
            'cumulative_energy_log_joules': round(cum_energy_log, 2),
            'seismic_rate_accel_ratio': accel_ratio,
            'regional_b_value': b_val,
            # Future Target Variables (strictly subsequent 30d)
            'elevated_aftershock_hazard': elevated_hazard,
            'aftershock_count_30d': aftershock_count_30d,
            'max_aftershock_mag_30d': max_aftershock_mag_30d,
            # Split
            'split': split_label
        })
        
        if (i + 1) % 2500 == 0 or (i + 1) == len(candidates):
            print(f"  Processed {i+1:,} / {len(candidates):,} seismic anchors ({time.time()-t1:.1f}s)...")
            
    df_out = pd.DataFrame(rows)
    out_file = os.path.join(MODEL_READY_DIR, 'earthquake_model_ready.csv')
    df_out.to_csv(out_file, index=False)
    print(f"\n[OUTPUT] Saved model-ready earthquake dataset: {out_file}")
    print(f"  - Total records: {len(df_out):,}")
    print(f"  - Elevated hazard cases (y=1): {(df_out['elevated_aftershock_hazard'] == 1).sum():,}")
    print(f"  - Quiescent cases (y=0): {(df_out['elevated_aftershock_hazard'] == 0).sum():,}")
    print(f"  - Input feature count: 11 engineered features")
    print(f"  - Split distribution: {df_out['split'].value_counts().to_dict()}")
    print(f"  - Missing values: {df_out.isnull().sum().sum()}")
    
    meta = {
        "hazard": "Earthquakes",
        "task": "Regional Seismic Activity & Aftershock Hazard Assessment",
        "dataset_file": out_file,
        "record_count": len(df_out),
        "feature_count": 11,
        "input_features": [
            "mainshock_mag", "focal_depth_km", "dist_to_active_fault_km", "nearest_fault_slip_type",
            "prior_count_7d_100km", "prior_count_30d_100km", "prior_count_365d_100km",
            "prior_max_mag_30d", "cumulative_energy_log_joules", "seismic_rate_accel_ratio", "regional_b_value"
        ],
        "target_variables": {
            "elevated_aftershock_hazard": "Binary indicator (1 = >=5 aftershocks or secondary M>=5.0 within 30 days and 100km; 0 = low)",
            "aftershock_count_30d": "Continuous count of subsequent earthquakes in 30 days",
            "max_aftershock_mag_30d": "Maximum magnitude of aftershock in subsequent 30 days"
        },
        "validation_strategy": "Chronological Walk-Forward Split: train (2000-2018), val (2019-2021), test (2022-2025)",
        "scientific_limitation": "Explicitly restricts ML task to statistical aftershock rate and regional seismic hazard. Deterministic exact earthquake prediction is physically impossible.",
        "class_balance": {
            "elevated_hazard_count": int((df_out['elevated_aftershock_hazard'] == 1).sum()),
            "quiescent_count": int((df_out['elevated_aftershock_hazard'] == 0).sum()),
            "positive_ratio": round(float((df_out['elevated_aftershock_hazard'] == 1).mean()), 3)
        }
    }
    with open(os.path.join(MODEL_READY_DIR, 'earthquake_features_metadata.json'), 'w') as f:
        json.dump(meta, f, indent=2)

if __name__ == '__main__':
    build_earthquake_model_ready_dataset(sample_size=10000)
