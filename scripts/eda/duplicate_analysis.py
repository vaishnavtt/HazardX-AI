"""
HAZARDX AI - Data Quality Audit: Duplicate Records Analysis
Checks exact row duplicates, primary key collisions, duplicate coordinates/timestamps,
and validates deduplication rules.
"""

import os
import pandas as pd

DATASETS = {
    "Floods_Cleaned": ("data/processed/floods/flood_events_cleaned_catalog.csv", "event_id"),
    "Landslides_Cleaned": ("data/processed/landslides/landslide_events_cleaned_catalog.csv", "event_id"),
    "Earthquakes_Cleaned": ("data/processed/earthquakes/earthquake_events_cleaned_catalog.csv", "event_id"),
    "Cyclones_Cleaned": ("data/processed/cyclones/cyclone_tracks_cleaned_catalog.csv", None),
    "India_Disasters": ("data/processed/environmental/india_disaster_events_catalog.csv", "glidenumber")
}

def analyze_duplicates():
    results = {}
    print("=================== DUPLICATE RECORDS QUALITY AUDIT ===================")
    for name, (path, id_col) in DATASETS.items():
        if not os.path.exists(path):
            continue
            
        print(f"\n--- Dataset: {name} ---")
        df = pd.read_csv(path, low_memory=False)
        
        # 1. Exact row duplicates
        exact_dups = df.duplicated().sum()
        print(f"Exact Duplicate Rows: {exact_dups:,} ({exact_dups/len(df)*100:.2f}%)")
        
        # 2. Key duplicates
        key_dups = 0
        if id_col and id_col in df.columns:
            key_dups = df.duplicated(subset=[id_col]).sum()
            print(f"Primary Key ({id_col}) Duplicates: {key_dups:,}")
            
        # 3. Spatial-Temporal duplicates
        st_dups = 0
        time_cols = [c for c in ['start_date', 'time', 'ISO_TIME', 'event_date'] if c in df.columns]
        coord_cols = [c for c in ['latitude', 'LAT'] if c in df.columns]
        lon_cols = [c for c in ['longitude', 'LON'] if c in df.columns]
        
        if time_cols and coord_cols and lon_cols:
            tc, lc, lnc = time_cols[0], coord_cols[0], lon_cols[0]
            st_dups = df.duplicated(subset=[tc, lc, lnc]).sum()
            print(f"Exact Spatio-Temporal Duplicates ({tc}, {lc}, {lnc}): {st_dups:,}")
            
        results[name] = {
            "total_rows": len(df),
            "exact_duplicates": int(exact_dups),
            "key_duplicates": int(key_dups),
            "spatio_temporal_duplicates": int(st_dups)
        }
    return results

if __name__ == '__main__':
    analyze_duplicates()

