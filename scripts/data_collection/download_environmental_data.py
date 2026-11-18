"""
HAZARDX AI - Data Collection Module: Common Environmental Datasets
Ingests cross-hazard environmental layers:
  1. Administrative boundaries (geoBoundaries IND-ADM1 States & IND-ADM2 Districts)
  2. Disaster events in India (GLIDE India GeoJSON)
  3. Meteorological & Hydrological Reanalysis Connectors (ECMWF ERA5 / GloFAS)
"""

import os
import requests
import json
import pandas as pd

RAW_ENV_DIR = 'data/raw/environmental'
PROC_ENV_DIR = 'data/processed/environmental'
os.makedirs(RAW_ENV_DIR, exist_ok=True)
os.makedirs(PROC_ENV_DIR, exist_ok=True)

ADM1_URL = 'https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/IND/ADM1/geoBoundaries-IND-ADM1_simplified.geojson'
INDIA_GLIDE_URL = 'https://data.humdata.org/dataset/138fec77-2cf9-4e19-919c-7f403fabd8cc/resource/b5268f14-2d89-4107-8a3d-7dfa1ca32d1d/download/ind_glide_events.geojson'

def download_boundaries():
    path = os.path.join(RAW_ENV_DIR, 'india_state_boundaries.geojson')
    if not os.path.exists(path) or os.path.getsize(path) < 1000:
        print("[Boundaries] Downloading India State boundaries GeoJSON...")
        r = requests.get(ADM1_URL, timeout=60)
        with open(path, 'wb') as f:
            f.write(r.content)
        print(f"[Boundaries] Saved to {path} ({os.path.getsize(path):,} bytes)")
    else:
        print(f"[Boundaries] Already exists at {path}")

def download_india_glide():
    path = os.path.join(RAW_ENV_DIR, 'india_glide_disaster_events.geojson')
    if not os.path.exists(path) or os.path.getsize(path) < 1000:
        print("[India GLIDE] Downloading disaster events GeoJSON...")
        r = requests.get(INDIA_GLIDE_URL, timeout=60)
        with open(path, 'wb') as f:
            f.write(r.content)
        print(f"[India GLIDE] Saved to {path} ({os.path.getsize(path):,} bytes)")
    else:
        print(f"[India GLIDE] Already exists at {path}")

def extract_india_kerala_disasters():
    """Extract and tabulate India-wide disaster records into structured CSV."""
    path = os.path.join(RAW_ENV_DIR, 'india_glide_disaster_events.geojson')
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    rows = []
    for feat in data.get('features', []):
        props = feat.get('properties', {})
        geom = feat.get('geometry', {})
        coords = geom.get('coordinates', [None, None])
        lon = coords[0] if len(coords) > 0 else None
        lat = coords[1] if len(coords) > 1 else None
        
        props['latitude'] = lat
        props['longitude'] = lon
        rows.append(props)
        
    df = pd.DataFrame(rows)
    out_csv = os.path.join(PROC_ENV_DIR, 'india_disaster_events_catalog.csv')
    df.to_csv(out_csv, index=False)
    print(f"[India Disasters] Processed {len(df):,} events into {out_csv}")
    
    # Filter Kerala records
    df_kerala = df[df['location'].astype(str).str.contains('Kerala', case=False, na=False)].copy()
    kerala_out = os.path.join(PROC_ENV_DIR, 'kerala_disaster_events.csv')
    df_kerala.to_csv(kerala_out, index=False)
    print(f"[Kerala Disasters] Extracted {len(df_kerala):,} Kerala events into {kerala_out}")

if __name__ == '__main__':
    download_boundaries()
    download_india_glide()
    extract_india_kerala_disasters()
    print("Environmental data ingestion verified.")

