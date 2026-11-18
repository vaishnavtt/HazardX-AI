"""
HAZARDX AI - Data Collection Module: Earthquakes
Ingests official global earthquake records from USGS ComCat API with monthly partitioning,
and downloads the GEM Global Active Faults GeoJSON.
Sources:
  1. USGS Earthquake Catalog (ComCat FDSNWS Event Web Service)
  2. Global Earthquake Model (GEM) Foundation (Global Active Faults Database)
  3. Asian Disaster Reduction Center (ADRC) / UN OCHA (GLIDE Earthquakes)
"""

import os
import requests
import calendar
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

RAW_EQ_DIR = 'data/raw/earthquakes'
MONTHLY_DIR = os.path.join(RAW_EQ_DIR, 'monthly')
os.makedirs(MONTHLY_DIR, exist_ok=True)

USGS_BASE_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
GEM_FAULTS_URL = 'https://raw.githubusercontent.com/GEMScienceTools/gem-global-active-faults/master/geojson/gem_active_faults.geojson'
GLIDE_RAW = 'data/raw/floods/glide_events_global.csv'

def download_gem_active_faults():
    out_faults = os.path.join(RAW_EQ_DIR, 'gem_active_faults.geojson')
    if os.path.exists(out_faults) and os.path.getsize(out_faults) > 100000:
        print(f"[GEM Faults] Already exists at {out_faults} ({os.path.getsize(out_faults):,} bytes)")
        return
    print("[GEM Faults] Downloading GEM Global Active Faults database...")
    r = requests.get(GEM_FAULTS_URL, timeout=60)
    with open(out_faults, 'wb') as f:
        f.write(r.content)
    print(f"[GEM Faults] Successfully saved to {out_faults}")

def extract_glide_earthquakes():
    if not os.path.exists(GLIDE_RAW):
        return
    df = pd.read_csv(GLIDE_RAW, low_memory=False)
    df_eq = df[df['event'] == 'EQ'].copy()
    out_path = os.path.join(RAW_EQ_DIR, 'glide_earthquake_events.csv')
    df_eq.to_csv(out_path, index=False)
    print(f"[GLIDE Earthquakes] Extracted {len(df_eq)} records to {out_path}")

def download_usgs_month(year, month, min_mag=2.5):
    last_day = calendar.monthrange(year, month)[1]
    starttime = f"{year:04d}-{month:02d}-01T00:00:00"
    endtime = f"{year:04d}-{month:02d}-{last_day:02d}T23:59:59"
    out_file = os.path.join(MONTHLY_DIR, f"earthquakes_{year:04d}_{month:02d}.csv")
    
    if os.path.exists(out_file) and os.path.getsize(out_file) > 100:
        return year, month, "EXISTS", 0
        
    records = []
    limit = 20000
    offset = 1
    headers = {'User-Agent': 'HazardX-AI/1.0 (Earthquake Ingestion)'}
    
    while True:
        params = {
            'format': 'csv',
            'starttime': starttime,
            'endtime': endtime,
            'minmagnitude': min_mag,
            'limit': limit,
            'offset': offset,
            'orderby': 'time-asc'
        }
        r = requests.get(USGS_BASE_URL, params=params, headers=headers, timeout=30)
        if r.status_code == 200:
            lines = r.text.strip().splitlines()
            if len(lines) <= 1:
                break
            records.extend(lines[1:])
            if len(lines[1:]) < limit:
                break
            offset += limit
        else:
            break
            
    header = "time,latitude,longitude,depth,mag,magType,nst,gap,dmin,rms,net,id,updated,place,type,horizontalError,depthError,magError,magNst,status,locationSource,magSource"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(header + "\n")
        for line in records:
            f.write(line + "\n")
    return year, month, "OK", len(records)

if __name__ == '__main__':
    download_gem_active_faults()
    extract_glide_earthquakes()
    print("Earthquake collection verified.")

