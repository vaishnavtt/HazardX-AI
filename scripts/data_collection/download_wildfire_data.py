"""
HAZARDX AI - Data Collection Module: Wildfires
Ingests official global wildfire and active fire datasets:
  1. NASA FIRMS (Fire Information for Resource Management System) - MODIS C6.1
  2. NASA FIRMS - VIIRS 375m (NOAA-20 / J1)
  3. Asian Disaster Reduction Center (ADRC) / UN OCHA (GLIDE Wildfires)
"""

import os
import requests
import pandas as pd

RAW_WILD_DIR = 'data/raw/wildfires'
PROC_WILD_DIR = 'data/processed/wildfires'
os.makedirs(RAW_WILD_DIR, exist_ok=True)
os.makedirs(PROC_WILD_DIR, exist_ok=True)

MODIS_URL = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_Global_7d.csv'
VIIRS_URL = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_Global_7d.csv'
GLIDE_RAW = 'data/raw/floods/glide_events_global.csv'

def download_firms_modis():
    out_path = os.path.join(RAW_WILD_DIR, 'modis_active_fire_global_7d.csv')
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
        print(f"[NASA FIRMS MODIS] Already exists at {out_path} ({os.path.getsize(out_path)/1024/1024:.2f} MB)")
        return
    print(f"[NASA FIRMS MODIS] Downloading open active fire data from {MODIS_URL}...")
    r = requests.get(MODIS_URL, timeout=60)
    with open(out_path, 'wb') as f:
        f.write(r.content)
    print(f"[NASA FIRMS MODIS] Saved to {out_path} ({os.path.getsize(out_path)/1024/1024:.2f} MB)")

def download_firms_viirs():
    out_path = os.path.join(RAW_WILD_DIR, 'viirs_active_fire_global_7d.csv')
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
        print(f"[NASA FIRMS VIIRS] Already exists at {out_path} ({os.path.getsize(out_path)/1024/1024:.2f} MB)")
        return
    print(f"[NASA FIRMS VIIRS] Downloading open active fire data from {VIIRS_URL}...")
    r = requests.get(VIIRS_URL, timeout=120)
    with open(out_path, 'wb') as f:
        f.write(r.content)
    print(f"[NASA FIRMS VIIRS] Saved to {out_path} ({os.path.getsize(out_path)/1024/1024:.2f} MB)")

def extract_glide_wildfires():
    if not os.path.exists(GLIDE_RAW):
        print("GLIDE raw master not found.")
        return
    df = pd.read_csv(GLIDE_RAW, low_memory=False)
    df_wf = df[df['event'] == 'WF'].copy()
    out_path = os.path.join(RAW_WILD_DIR, 'glide_wildfire_disaster_events.csv')
    df_wf.to_csv(out_path, index=False)
    print(f"[GLIDE Wildfires] Extracted {len(df_wf)} disaster records to {out_path}")

if __name__ == '__main__':
    download_firms_modis()
    download_firms_viirs()
    extract_glide_wildfires()
    print("Wildfire raw collection complete.")

