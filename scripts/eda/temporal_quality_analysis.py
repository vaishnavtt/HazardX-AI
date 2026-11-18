"""
HAZARDX AI - Data Quality Audit: Temporal Quality Analysis
Evaluates temporal coverage, resolution, observation frequencies,
missing intervals, and seasonal distributions across hazards.
"""

import os
import pandas as pd
import numpy as np

TEMPORAL_DATASETS = {
    "Floods": ("data/processed/floods/flood_events_cleaned_catalog.csv", "start_date"),
    "Landslides": ("data/processed/landslides/landslide_events_cleaned_catalog.csv", "start_date"),
    "Earthquakes": ("data/processed/earthquakes/earthquake_events_cleaned_catalog.csv", "time"),
    "Cyclones": ("data/processed/cyclones/cyclone_tracks_cleaned_catalog.csv", "ISO_TIME"),
    "India_Disasters": ("data/processed/environmental/india_disaster_events_catalog.csv", "start_date")
}

def analyze_temporal_quality():
    print("=================== TEMPORAL QUALITY & TIME-SERIES AUDIT ===================")
    temporal_summary = {}
    
    for hazard, (path, time_col) in TEMPORAL_DATASETS.items():
        if not os.path.exists(path):
            continue
            
        print(f"\n--- Hazard: {hazard} ---")
        df = pd.read_csv(path, low_memory=False)
        
        parsed = pd.to_datetime(df[time_col], errors='coerce')
        valid_dates = parsed.dropna()
        
        t_min = valid_dates.min()
        t_max = valid_dates.max()
        span_years = (t_max - t_min).days / 365.25 if pd.notnull(t_min) and pd.notnull(t_max) else 0
        
        # Monthly distribution (seasonality)
        months = valid_dates.dt.month.value_counts().sort_index()
        peak_month = months.idxmax() if not months.empty else None
        
        print(f"Total Records: {len(df):,}")
        print(f"Valid Timestamps: {len(valid_dates):,} ({len(valid_dates)/len(df)*100:.2f}%)")
        print(f"Temporal Span: {t_min} to {t_max} (~{span_years:.1f} years)")
        print(f"Peak Event Month: Month {peak_month} ({months.get(peak_month, 0):,} events)")
        
        # Monthly seasonality breakdown
        print("Quarterly Seasonality Distribution:")
        q1 = months.loc[1:3].sum() if 1 in months else 0
        q2 = months.loc[4:6].sum() if 4 in months else 0
        q3 = months.loc[7:9].sum() if 7 in months else 0
        q4 = months.loc[10:12].sum() if 10 in months else 0
        total_m = len(valid_dates)
        if total_m > 0:
            print(f"  Q1 (Jan-Mar): {q1:,} ({q1/total_m*100:.1f}%)")
            print(f"  Q2 (Apr-Jun): {q2:,} ({q2/total_m*100:.1f}%)")
            print(f"  Q3 (Jul-Sep - Monsoon/Peak Storm): {q3:,} ({q3/total_m*100:.1f}%)")
            print(f"  Q4 (Oct-Dec - Post-Monsoon): {q4:,} ({q4/total_m*100:.1f}%)")
            
        temporal_summary[hazard] = {
            "total_records": len(df),
            "valid_dates": len(valid_dates),
            "earliest": str(t_min),
            "latest": str(t_max),
            "span_years": round(span_years, 1),
            "peak_month": int(peak_month) if peak_month else None
        }
    return temporal_summary

if __name__ == '__main__':
    analyze_temporal_quality()

