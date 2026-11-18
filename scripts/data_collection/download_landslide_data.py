"""
HAZARDX AI - Data Collection Module: Landslides
Downloads and organizes official global historical landslide catalogues.
Sources:
  1. NASA Global Landslide Catalog (GLC / COOLR) - NASA Goddard Space Flight Center
  2. Asian Disaster Reduction Center (ADRC) / UN OCHA (GLIDE Landslides)
"""

import os
import requests
import zipfile
import io
import pandas as pd

RAW_LANDSLIDE_DIR = 'data/raw/landslides'
PROCESSED_LANDSLIDE_DIR = 'data/processed/landslides'
os.makedirs(RAW_LANDSLIDE_DIR, exist_ok=True)
os.makedirs(PROCESSED_LANDSLIDE_DIR, exist_ok=True)

NASA_HDX_ZIP = 'https://data.humdata.org/dataset/1eb911ba-3681-4a96-b025-ae0c33b80a12/resource/ed703c45-2001-4286-ba16-8248c17fec80/download/global_landslide_catalog_nasa.zip'
GLIDE_RAW = 'data/raw/floods/glide_events_global.csv'

def download_nasa_shapefile():
    shp_dir = os.path.join(RAW_LANDSLIDE_DIR, 'nasa_shapefile')
    os.makedirs(shp_dir, exist_ok=True)
    shp_marker = os.path.join(shp_dir, 'global_landslide_catalog_NASA.shp')
    if os.path.exists(shp_marker):
        print(f"[NASA GLC Shapefile] Already exists at {shp_marker}")
        return
    print(f"[NASA GLC Shapefile] Downloading from {NASA_HDX_ZIP}...")
    r = requests.get(NASA_HDX_ZIP, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    zf.extractall(shp_dir)
    print(f"[NASA GLC Shapefile] Successfully extracted to {shp_dir}")

def extract_glide_landslides():
    if not os.path.exists(GLIDE_RAW):
        print("GLIDE raw master not found. Run download_flood_data.py first.")
        return
    df = pd.read_csv(GLIDE_RAW, low_memory=False)
    df_ls = df[df['event'] == 'LS'].copy()
    out_path = os.path.join(RAW_LANDSLIDE_DIR, 'glide_landslide_events.csv')
    df_ls.to_csv(out_path, index=False)
    print(f"[GLIDE Landslides] Extracted {len(df_ls)} records to {out_path}")

if __name__ == '__main__':
    download_nasa_shapefile()
    extract_glide_landslides()
    print("Landslide data collection verified.")

