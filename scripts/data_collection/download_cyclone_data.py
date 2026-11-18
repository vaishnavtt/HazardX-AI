"""
HAZARDX AI - Data Collection Module: Cyclones
Ingests and organizes NOAA IBTrACS best-track data and GLIDE tropical cyclones.
Sources:
  1. NOAA National Centers for Environmental Information (NCEI) - IBTrACS v04r01
  2. Asian Disaster Reduction Center (ADRC) / UN OCHA (GLIDE Cyclones)
"""

import os
import shutil
import pandas as pd
import numpy as np

RAW_CYCLONE_DIR = 'data/raw/cyclones'
PROC_CYCLONE_DIR = 'data/processed/cyclones'
os.makedirs(RAW_CYCLONE_DIR, exist_ok=True)
os.makedirs(PROC_CYCLONE_DIR, exist_ok=True)

IBTRACS_OFFICIAL_URL = 'https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.since1980.list.v04r01.csv'
EXISTING_RAW = 'data/raw/cyclone/ibtracs.since1980.list.v04r01.csv'
TARGET_RAW = os.path.join(RAW_CYCLONE_DIR, 'ibtracs_since1980_v04r01.csv')
GLIDE_RAW = 'data/raw/floods/glide_events_global.csv'

def organize_raw_ibtracs():
    if not os.path.exists(TARGET_RAW) and os.path.exists(EXISTING_RAW):
        shutil.copyfile(EXISTING_RAW, TARGET_RAW)
        print(f"[IBTrACS] Copied existing raw file to {TARGET_RAW}")
    elif os.path.exists(TARGET_RAW):
        print(f"[IBTrACS] Verified target raw file: {TARGET_RAW} ({os.path.getsize(TARGET_RAW)/1024/1024:.2f} MB)")

def extract_glide_cyclones():
    if not os.path.exists(GLIDE_RAW):
        return
    df = pd.read_csv(GLIDE_RAW, low_memory=False)
    df_tc = df[df['event'] == 'TC'].copy()
    out_path = os.path.join(RAW_CYCLONE_DIR, 'glide_cyclone_events.csv')
    df_tc.to_csv(out_path, index=False)
    print(f"[GLIDE Cyclones] Extracted {len(df_tc)} records to {out_path}")

def process_cyclone_tracks():
    print("[IBTrACS] Cleaning and structuring cyclone track observations...")
    df = pd.read_csv(TARGET_RAW, skiprows=[1], low_memory=False)
    
    # Core tracking columns
    cols = [
        'SID', 'SEASON', 'NUMBER', 'BASIN', 'SUBBASIN', 'NAME', 'ISO_TIME', 
        'NATURE', 'LAT', 'LON', 'WMO_WIND', 'WMO_PRES', 'USA_STATUS', 
        'USA_WIND', 'USA_PRES', 'TRACK_TYPE', 'DIST2LAND', 'LANDFALL'
    ]
    df_sub = df[cols].copy()
    
    # Clean numeric types
    df_sub['LAT'] = pd.to_numeric(df_sub['LAT'], errors='coerce')
    df_sub['LON'] = pd.to_numeric(df_sub['LON'], errors='coerce')
    df_sub['WMO_WIND'] = pd.to_numeric(df_sub['WMO_WIND'], errors='coerce')
    df_sub['WMO_PRES'] = pd.to_numeric(df_sub['WMO_PRES'], errors='coerce')
    df_sub['USA_WIND'] = pd.to_numeric(df_sub['USA_WIND'], errors='coerce')
    df_sub['USA_PRES'] = pd.to_numeric(df_sub['USA_PRES'], errors='coerce')
    df_sub['DIST2LAND'] = pd.to_numeric(df_sub['DIST2LAND'], errors='coerce')
    
    # Normalize longitude from (180, 360] to [-180, 180] to handle Pacific dateline crossings
    # IBTrACS documents longitudes crossing 180° East up to ~190°
    df_sub['LON'] = np.where(df_sub['LON'] > 180, df_sub['LON'] - 360, df_sub['LON'])
    df_sub['LON'] = np.where(df_sub['LON'] < -180, df_sub['LON'] + 360, df_sub['LON'])
    
    # Filter valid coordinates
    df_clean = df_sub[
        df_sub['LAT'].notnull() & 
        df_sub['LON'].notnull() &
        (df_sub['LAT'] >= -90) & (df_sub['LAT'] <= 90) &
        (df_sub['LON'] >= -180) & (df_sub['LON'] <= 180)
    ].copy()
    
    cleaned_out = os.path.join(PROC_CYCLONE_DIR, 'cyclone_tracks_cleaned_catalog.csv')
    df_clean.to_csv(cleaned_out, index=False)
    print(f"[Cleaned Tracks] Saved {len(df_clean):,} track points to {cleaned_out}")
    
    # Also extract North Indian Ocean subset for focused Indian regional early warning
    df_nio = df_clean[df_clean['BASIN'] == 'NI'].copy()
    nio_out = os.path.join(PROC_CYCLONE_DIR, 'cyclone_tracks_north_indian_ocean.csv')
    df_nio.to_csv(nio_out, index=False)
    print(f"[NIO Tracks] Saved {len(df_nio):,} North Indian Ocean track points to {nio_out}")

if __name__ == '__main__':
    organize_raw_ibtracs()
    extract_glide_cyclones()
    process_cyclone_tracks()
    print("Cyclone data processing verified.")

