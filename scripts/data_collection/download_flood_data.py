"""
HAZARDX AI - Data Collection Module: Floods
Downloads and organizes official global historical flood event datasets and environmental river discharge.
Sources:
  1. Dartmouth Flood Observatory (DFO) - University of Colorado Boulder / CSDMS
  2. Asian Disaster Reduction Center (ADRC) / UN OCHA (GLIDE Floods)
  3. Copernicus GloFAS / Open-Meteo Flood API (River Discharge Reanalysis)
"""

import os
import requests
import zipfile
import io
import pandas as pd

RAW_FLOOD_DIR = 'data/raw/floods'
PROCESSED_FLOOD_DIR = 'data/processed/floods'
os.makedirs(RAW_FLOOD_DIR, exist_ok=True)
os.makedirs(PROCESSED_FLOOD_DIR, exist_ok=True)

DFO_SHP_URL = 'https://data.humdata.org/dataset/1fd855de-57c6-42b3-83e1-9cf989b0f70d/resource/984cc240-b2b7-4266-9f61-5715a9e10ff5/download/wlf_nhr_fl_dfomasterlist_20190418.zip'
GLIDE_URL = 'https://data.humdata.org/dataset/5721abce-4367-4307-abbd-f99cf95ebeca/resource/2b0e6ef0-7006-4d99-bf01-04a7ad14fd12/download/glide_events_global.csv'

def download_dfo_shapefile():
    shp_dir = os.path.join(RAW_FLOOD_DIR, 'dfo_shapefile')
    os.makedirs(shp_dir, exist_ok=True)
    shp_marker = os.path.join(shp_dir, 'wlf_nhr_fl_dfomasterlist_20190418.shp')
    if os.path.exists(shp_marker):
        print(f"[DFO Shapefile] Already exists at {shp_marker}")
        return
    print(f"[DFO Shapefile] Downloading from {DFO_SHP_URL}...")
    r = requests.get(DFO_SHP_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    zf.extractall(shp_dir)
    print(f"[DFO Shapefile] Successfully extracted to {shp_dir}")

def download_glide_floods():
    glide_raw = os.path.join(RAW_FLOOD_DIR, 'glide_events_global.csv')
    if not os.path.exists(glide_raw):
        print(f"[GLIDE] Downloading full archive from {GLIDE_URL}...")
        r = requests.get(GLIDE_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
        with open(glide_raw, 'wb') as f:
            f.write(r.content)
    df = pd.read_csv(glide_raw, low_memory=False)
    df_flood = df[df['event'].isin(['FL', 'FF'])].copy()
    out_flood = os.path.join(RAW_FLOOD_DIR, 'glide_flood_events.csv')
    df_flood.to_csv(out_flood, index=False)
    print(f"[GLIDE Floods] Saved {len(df_flood)} flood events to {out_flood}")

def fetch_glofas_sample(lat, lon, start_date, end_date):
    """Query Copernicus GloFAS river discharge reanalysis via Open-Meteo Flood API."""
    url = f"https://flood-api.open-meteo.com/v1/flood?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=river_discharge"
    r = requests.get(url, timeout=15)
    if r.status_code == 200:
        return r.json()
    return None

if __name__ == '__main__':
    download_dfo_shapefile()
    download_glide_floods()
    print("Flood data collection verified.")

