"""
HAZARDX AI - Master Exploratory Data Analysis & Quality Reporting Pipeline
Generates all multi-hazard EDA figures across all 5 hazard modules:
  1. Floods (DFO & GLIDE)
  2. Landslides (NASA GLC & GLIDE)
  3. Earthquakes (USGS ComCat M>=2.5)
  4. Cyclones (NOAA IBTrACS & GLIDE)
  5. Wildfires (NASA FIRMS MODIS/VIIRS & GLIDE)
"""

import os
import json
import calendar
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

FIG_DIR = 'data/reports/figures'
REP_DIR = 'data/reports'
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(REP_DIR, exist_ok=True)

PATHS = {
    'floods': 'data/processed/floods/flood_events_cleaned_catalog.csv',
    'landslides': 'data/processed/landslides/landslide_events_cleaned_catalog.csv',
    'earthquakes': 'data/processed/earthquakes/earthquake_events_cleaned_catalog.csv',
    'cyclones': 'data/processed/cyclones/cyclone_tracks_cleaned_catalog.csv',
    'cyclones_nio': 'data/processed/cyclones/cyclone_tracks_north_indian_ocean.csv',
    'wildfires': 'data/processed/wildfires/wildfire_events_cleaned_catalog.csv',
    'wildfires_viirs': 'data/processed/wildfires/wildfire_events_viirs_catalog.csv',
    'wildfires_glide': 'data/processed/wildfires/wildfire_disaster_events_glide.csv',
    'india_disasters': 'data/processed/environmental/india_disaster_events_catalog.csv',
    'gem_faults': 'data/raw/earthquakes/gem_active_faults.geojson',
    'india_bounds': 'data/raw/environmental/india_state_boundaries.geojson'
}

def load_data():
    print("Loading processed datasets for 5-hazard EDA...")
    df_flood = pd.read_csv(PATHS['floods'], low_memory=False)
    df_ls = pd.read_csv(PATHS['landslides'], low_memory=False)
    df_eq = pd.read_csv(PATHS['earthquakes'], usecols=['time', 'latitude', 'longitude', 'depth', 'mag', 'magType'], low_memory=False)
    df_cyc = pd.read_csv(PATHS['cyclones'], usecols=['SID', 'SEASON', 'BASIN', 'ISO_TIME', 'LAT', 'LON', 'USA_WIND', 'USA_PRES', 'DIST2LAND'], low_memory=False)
    df_cyc_nio = pd.read_csv(PATHS['cyclones_nio'], low_memory=False)
    df_wf = pd.read_csv(PATHS['wildfires'], low_memory=False)
    df_ind = pd.read_csv(PATHS['india_disasters'], low_memory=False)
    return df_flood, df_ls, df_eq, df_cyc, df_cyc_nio, df_wf, df_ind

def generate_eda_figures(df_flood, df_ls, df_eq, df_cyc, df_cyc_nio, df_wf, df_ind):
    print("Generating comprehensive EDA figures for all 5 hazards...")
    sns.set_theme(style="whitegrid", font_scale=1.1)
    
    # FIG 1: Hazard Record Count Comparison (All 5 Hazards)
    fig, ax = plt.subplots(figsize=(12, 6))
    hazards = [
        'Floods\n(Events)', 
        'Landslides\n(Events)', 
        'Earthquakes\n(M>=2.5 Events)', 
        'Cyclones\n(Track Points)', 
        'Wildfires\n(MODIS Events)',
        'North Indian Ocean\nCyclones (Tracks)'
    ]
    counts = [len(df_flood), len(df_ls), len(df_eq), len(df_cyc), len(df_wf), len(df_cyc_nio)]
    colors = ['#1f77b4', '#8c564b', '#d62728', '#2ca02c', '#e65100', '#ff7f0e']
    bars = ax.bar(hazards, counts, color=colors, edgecolor='black', alpha=0.85)
    ax.set_yscale('log')
    ax.set_title("HAZARDX AI: Verified Empirical Records Across All 5 Hazards (Log Scale)", fontsize=14, weight='bold')
    ax.set_ylabel("Total Number of Records (Logarithmic)")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:,}", xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=10, weight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'hazard_record_counts.png'), dpi=200)
    plt.close()

    # FIG 2: Earthquakes Depth vs Magnitude & Distribution
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    eq_sample = df_eq.sample(n=min(30000, len(df_eq)), random_state=42)
    sns.histplot(df_eq['mag'].dropna(), bins=35, kde=True, ax=ax1, color='#d62728')
    ax1.set_title("Earthquake Magnitude Distribution (M >= 2.5)", weight='bold')
    ax1.set_xlabel("Magnitude (M)")
    ax1.set_ylabel("Frequency Count")
    
    scatter = ax2.scatter(eq_sample['mag'], eq_sample['depth'], c=eq_sample['depth'], cmap='viridis_r', alpha=0.4, s=12)
    ax2.set_yscale('log')
    ax2.invert_yaxis()
    ax2.set_title("Earthquake Focal Depth vs Magnitude (Sampled n=30k)", weight='bold')
    ax2.set_xlabel("Magnitude (M)")
    ax2.set_ylabel("Hypocentral Depth (km, Log Scale)")
    plt.colorbar(scatter, ax=ax2, label="Depth (km)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'earthquake_depth_magnitude_eda.png'), dpi=200)
    plt.close()

    # FIG 3: Cyclone Wind Speed vs Central Pressure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    valid_cyc = df_cyc[(df_cyc['USA_WIND'] > 0) & (df_cyc['USA_PRES'] > 850) & (df_cyc['USA_PRES'] < 1040)].copy()
    cyc_sample = valid_cyc.sample(n=min(25000, len(valid_cyc)), random_state=42)
    
    sns.regplot(data=cyc_sample, x='USA_WIND', y='USA_PRES', ax=ax1, color='#2ca02c',
                scatter_kws={'alpha': 0.25, 's': 10}, line_kws={'color': 'darkgreen', 'linewidth': 2})
    ax1.set_title("Cyclone Wind Speed vs Minimum Central Pressure\n(Dvorak Empirical Physical Law)", weight='bold')
    ax1.set_xlabel("Maximum Sustained Wind Speed (knots)")
    ax1.set_ylabel("Central Pressure (hPa)")
    
    basin_counts = df_cyc['BASIN'].value_counts()
    basin_labels = {'WP': 'West Pacific', 'SI': 'South Indian', 'EP': 'East Pacific', 'SP': 'South Pacific', 'NI': 'North Indian Ocean\n(India)', 'SA': 'South Atlantic'}
    b_names = [basin_labels.get(k, k) for k in basin_counts.index]
    ax2.bar(b_names, basin_counts.values, color='#17becf', edgecolor='black')
    ax2.set_title("Global Tropical Cyclone Track Frequency by Ocean Basin", weight='bold')
    ax2.set_ylabel("Track Points")
    ax2.tick_params(axis='x', rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'cyclone_wind_pressure_eda.png'), dpi=200)
    plt.close()

    # FIG 4: Landslide Triggers & Categories
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    trig = df_ls['trigger'].value_counts().head(6)
    ax1.barh(trig.index, trig.values, color='#8c564b', edgecolor='black')
    ax1.set_title("Landslide Triggering Mechanisms (NASA GLC)", weight='bold')
    ax1.set_xlabel("Number of Events")
    ax1.invert_yaxis()
    
    cat = df_ls['landslide_category'].value_counts().head(5)
    ax2.pie(cat.values, labels=cat.index, autopct='%1.1f%%', colors=['#bcbd22', '#ffbb78', '#98df8a', '#c5b0d5', '#ff9896'], startangle=140)
    ax2.set_title("Landslide Classification Breakdown", weight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'landslide_triggers_and_categories.png'), dpi=200)
    plt.close()

    # FIG 5: Flood Duration & Severity
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    valid_dur = df_flood['duration_days'].dropna()
    valid_dur = valid_dur[(valid_dur > 0) & (valid_dur <= 60)]
    sns.histplot(valid_dur, bins=30, kde=True, ax=ax1, color='#1f77b4')
    ax1.set_title("Flood Event Duration Distribution (Days <= 60)", weight='bold')
    ax1.set_xlabel("Duration (Days)")
    ax1.set_ylabel("Event Count")
    
    sev_df = df_flood[df_flood['severity'].isin([1.0, 1.5, 2.0])]
    sev = sev_df['severity'].value_counts().sort_index()
    sev_labels = [f"Class {k}\n({'Large' if k==1.0 else 'Very Large' if k==1.5 else 'Extreme/Decadal'})" for k in sev.index]
    ax2.bar(sev_labels, sev.values, color=['#aec7e8', '#1f77b4', '#08519c'], edgecolor='black')
    ax2.set_title("DFO Flood Severity Class Distribution", weight='bold')
    ax2.set_ylabel("Event Count")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'flood_severity_and_duration.png'), dpi=200)
    plt.close()

    # FIG 6: Global Multi-Hazard Spatial Distribution Map (All 5 Hazards)
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_facecolor('#f0f8ff')
    ax.scatter(df_eq.sample(15000, random_state=42)['longitude'], df_eq.sample(15000, random_state=42)['latitude'],
               color='#d62728', s=2, alpha=0.25, label='Earthquakes (USGS ComCat M>=2.5)')
    ax.scatter(df_cyc.sample(15000, random_state=42)['LON'], df_cyc.sample(15000, random_state=42)['LAT'],
               color='#2ca02c', s=2, alpha=0.3, label='Cyclones (NOAA IBTrACS)')
    ax.scatter(df_flood['longitude'], df_flood['latitude'],
               color='#1f77b4', s=6, alpha=0.6, label='Floods (DFO & GLIDE)')
    ax.scatter(df_ls['longitude'], df_ls['latitude'],
               color='#8c564b', s=5, alpha=0.6, label='Landslides (NASA GLC)')
    ax.scatter(df_wf.sample(min(10000, len(df_wf)), random_state=42)['centroid_lon'], 
               df_wf.sample(min(10000, len(df_wf)), random_state=42)['centroid_lat'],
               color='#e65100', s=4, alpha=0.5, label='Wildfires (NASA FIRMS Clustered Events)')
    
    ax.set_xlim(-180, 180)
    ax.set_ylim(-85, 85)
    ax.set_title("HAZARDX AI: Global Multi-Hazard Empirical Spatial Coverage\n(Floods, Landslides, Earthquakes, Cyclones, Wildfires)", fontsize=15, weight='bold')
    ax.set_xlabel("Longitude (WGS84 Degrees)")
    ax.set_ylabel("Latitude (WGS84 Degrees)")
    ax.legend(loc='lower left', markerscale=5, frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'global_multi_hazard_spatial_distribution.png'), dpi=200)
    plt.close()

    # FIG 7: India Multi-Hazard Focus Map (All 5 Hazards)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_facecolor('#fdfbf7')
    ind_bbox = (df_eq['latitude'] >= 6) & (df_eq['latitude'] <= 38) & (df_eq['longitude'] >= 68) & (df_eq['longitude'] <= 98)
    ind_eq = df_eq[ind_bbox]
    ind_cyc_bbox = (df_cyc_nio['LAT'] >= 5) & (df_cyc_nio['LAT'] <= 30) & (df_cyc_nio['LON'] >= 55) & (df_cyc_nio['LON'] <= 100)
    ind_cyc = df_cyc_nio[ind_cyc_bbox]
    ind_fl = df_flood[(df_flood['latitude'] >= 6) & (df_flood['latitude'] <= 38) & (df_flood['longitude'] >= 68) & (df_flood['longitude'] <= 98)]
    ind_ls = df_ls[(df_ls['latitude'] >= 6) & (df_ls['latitude'] <= 38) & (df_ls['longitude'] >= 68) & (df_ls['longitude'] <= 98)]
    ind_wf = df_wf[(df_wf['centroid_lat'] >= 6) & (df_wf['centroid_lat'] <= 38) & (df_wf['centroid_lon'] >= 68) & (df_wf['centroid_lon'] <= 98)]
    
    ax.scatter(ind_eq['longitude'], ind_eq['latitude'], color='#d62728', s=6, alpha=0.35, label=f'Earthquakes ({len(ind_eq):,} events)')
    ax.scatter(ind_cyc['LON'], ind_cyc['LAT'], color='#2ca02c', s=4, alpha=0.3, label=f'North Indian Ocean Cyclones ({len(ind_cyc):,} tracks)')
    ax.scatter(ind_fl['longitude'], ind_fl['latitude'], color='#1f77b4', s=14, alpha=0.7, label=f'Floods ({len(ind_fl):,} events)')
    ax.scatter(ind_ls['longitude'], ind_ls['latitude'], color='#8c564b', s=12, alpha=0.7, label=f'Landslides ({len(ind_ls):,} events)')
    ax.scatter(ind_wf['centroid_lon'], ind_wf['centroid_lat'], color='#e65100', s=8, alpha=0.6, label=f'Wildfires ({len(ind_wf):,} events)')
    
    ax.set_xlim(65, 100)
    ax.set_ylim(5, 38)
    ax.set_title("HAZARDX AI: India & South Asia 5-Hazard Spatial Architecture", fontsize=13, weight='bold')
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.legend(loc='upper right', markerscale=3, frameon=True, facecolor='white')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'india_multi_hazard_focus_map.png'), dpi=200)
    plt.close()

    # FIG 8: Wildfire Fire Radiative Power (FRP) & Event Duration
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    valid_frp = df_wf[df_wf['total_frp_mw'] > 0]['total_frp_mw']
    sns.histplot(valid_frp, bins=40, kde=True, ax=ax1, color='#e65100', log_scale=True)
    ax1.set_title("Wildfire Total Fire Radiative Power (MW, Log Scale)", weight='bold')
    ax1.set_xlabel("Total FRP (Megawatts, MW)")
    ax1.set_ylabel("Event Count")
    
    dur_counts = df_wf['duration_days'].value_counts().sort_index().head(7)
    ax2.bar([f"{d} Day{'s' if d>1 else ''}" for d in dur_counts.index], dur_counts.values, color='#bf360c', edgecolor='black')
    ax2.set_title("Wildfire Event Episode Duration (Days)", weight='bold')
    ax2.set_ylabel("Number of Clustered Events")
    for idx, v in enumerate(dur_counts.values):
        ax2.annotate(f"{v:,}", xy=(idx, v), xytext=(0, 3), textcoords="offset points", ha='center', fontsize=9, weight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'wildfire_frp_duration_eda.png'), dpi=200)
    plt.close()
    
    print("All 8 multi-hazard EDA figures successfully generated.")

if __name__ == '__main__':
    df_flood, df_ls, df_eq, df_cyc, df_cyc_nio, df_wf, df_ind = load_data()
    generate_eda_figures(df_flood, df_ls, df_eq, df_cyc, df_cyc_nio, df_wf, df_ind)
