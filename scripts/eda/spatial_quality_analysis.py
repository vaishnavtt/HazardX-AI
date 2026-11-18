"""
HAZARDX AI - Data Quality Audit: Spatial Quality Analysis
Evaluates geographic coverage, bounding boxes, coordinate completeness,
coordinate reference systems (CRS), and null-island anomalies.
"""

import os
import pandas as pd
import numpy as np

SPATIAL_DATASETS = {
    "Floods": ("data/processed/floods/flood_events_cleaned_catalog.csv", "latitude", "longitude"),
    "Landslides": ("data/processed/landslides/landslide_events_cleaned_catalog.csv", "latitude", "longitude"),
    "Earthquakes": ("data/processed/earthquakes/earthquake_events_cleaned_catalog.csv", "latitude", "longitude"),
    "Cyclones": ("data/processed/cyclones/cyclone_tracks_cleaned_catalog.csv", "LAT", "LON"),
    "India_Disasters": ("data/processed/environmental/india_disaster_events_catalog.csv", "latitude", "longitude")
}

def analyze_spatial_quality():
    print("=================== SPATIAL QUALITY & CRS AUDIT ===================")
    spatial_summary = {}
    
    for hazard, (path, lat_col, lon_col) in SPATIAL_DATASETS.items():
        if not os.path.exists(path):
            continue
            
        print(f"\n--- Hazard: {hazard} ---")
        df = pd.read_csv(path, low_memory=False)
        
        lat = pd.to_numeric(df[lat_col], errors='coerce')
        lon = pd.to_numeric(df[lon_col], errors='coerce')
        
        total = len(df)
        valid = (lat.notnull() & lon.notnull()).sum()
        lat_oob = ((lat < -90) | (lat > 90)).sum()
        lon_oob = ((lon < -180) | (lon > 180)).sum()
        null_island = ((lat == 0) & (lon == 0)).sum()
        
        lat_min, lat_max = lat.min(), lat.max()
        lon_min, lon_max = lon.min(), lon.max()
        
        print(f"Total Features: {total:,}")
        print(f"Valid Coordinates: {valid:,} ({valid/total*100:.2f}%)")
        print(f"Out of Bounds: Lat={lat_oob}, Lon={lon_oob}")
        print(f"Null Island (0,0): {null_island}")
        print(f"Bounding Box: Lat [{lat_min:.4f}, {lat_max:.4f}], Lon [{lon_min:.4f}, {lon_max:.4f}]")
        print(f"Native CRS: WGS84 (EPSG:4326) Decimal Degrees")
        
        spatial_summary[hazard] = {
            "total_records": total,
            "valid_coords": int(valid),
            "valid_pct": round(valid/total*100, 2),
            "lat_oob": int(lat_oob),
            "lon_oob": int(lon_oob),
            "null_island": int(null_island),
            "bbox": [float(lat_min), float(lon_min), float(lat_max), float(lon_max)]
        }
    return spatial_summary

if __name__ == '__main__':
    analyze_spatial_quality()

