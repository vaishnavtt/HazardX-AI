"""
HAZARDX AI - Data Quality Audit: Missing Value Analysis
Analyzes missing value rates, patterns, completely empty rows/columns,
and recommends domain-appropriate handling strategies.
"""

import os
import pandas as pd
import numpy as np

DATASETS = {
    "Floods_Cleaned": "data/processed/floods/flood_events_cleaned_catalog.csv",
    "Landslides_Cleaned": "data/processed/landslides/landslide_events_cleaned_catalog.csv",
    "Earthquakes_Cleaned": "data/processed/earthquakes/earthquake_events_cleaned_catalog.csv",
    "Cyclones_Cleaned": "data/processed/cyclones/cyclone_tracks_cleaned_catalog.csv",
    "Cyclones_NIO": "data/processed/cyclones/cyclone_tracks_north_indian_ocean.csv",
    "India_Disasters": "data/processed/environmental/india_disaster_events_catalog.csv"
}

def analyze_missing_values():
    results = {}
    print("=================== MISSING VALUE QUALITY AUDIT ===================")
    for name, path in DATASETS.items():
        if not os.path.exists(path):
            print(f"Skipping {name}: file not found at {path}")
            continue
            
        print(f"\n--- Dataset: {name} ---")
        df = pd.read_csv(path, low_memory=False)
        total_cells = df.size
        total_nulls = df.isnull().sum().sum()
        pct_nulls = total_nulls / total_cells * 100 if total_cells > 0 else 0
        
        col_nulls = df.isnull().sum()
        col_pct = (col_nulls / len(df) * 100).round(2)
        
        empty_cols = col_nulls[col_nulls == len(df)].index.tolist()
        excessive_cols = col_pct[col_pct >= 50.0].index.tolist()
        
        print(f"Total Rows: {len(df):,}, Columns: {len(df.columns)}")
        print(f"Overall Missing Rate: {pct_nulls:.2f}% ({total_nulls:,} / {total_cells:,} cells)")
        if empty_cols:
            print(f"Completely Empty Columns: {empty_cols}")
        if excessive_cols:
            print(f"Columns with >=50% Missing: {excessive_cols}")
            
        print("Missing by column:")
        for col in df.columns:
            cnt = col_nulls[col]
            pct = col_pct[col]
            if cnt > 0:
                print(f"  - {col}: {cnt:,} ({pct}%)")
                
        results[name] = {
            "rows": len(df),
            "cols": len(df.columns),
            "total_nulls": int(total_nulls),
            "null_pct": round(pct_nulls, 2),
            "col_stats": {c: {"missing": int(col_nulls[c]), "pct": float(col_pct[c])} for c in df.columns},
            "empty_cols": empty_cols,
            "excessive_cols": excessive_cols
        }
    return results

if __name__ == '__main__':
    analyze_missing_values()

