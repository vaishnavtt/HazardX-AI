"""
HAZARDX AI - Wildfire Data Processing and Clustering Module
Processes raw NASA FIRMS active fire satellite detections (MODIS and VIIRS)
and aggregates them into discrete physical wildfire event records using
spatiotemporal DBSCAN clustering.

Separates:
  1. Satellite Active Fire Detections (instantaneous thermal anomalies / pixels)
  2. Aggregated Wildfire Events (spatiotemporally contiguous wildfire burning episodes)
  3. Historical Wildfire Disaster Impact Records (GLIDE disaster registry)
"""

import os
import math
import json
import time
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

RAW_WILD_DIR = 'data/raw/wildfires'
PROC_WILD_DIR = 'data/processed/wildfires'
os.makedirs(PROC_WILD_DIR, exist_ok=True)

def haversine_np(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2.0)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2.0)**2
    return 2 * R * np.arcsin(np.sqrt(a))

def cluster_active_fires_dbscan(df, sensor_name='MODIS', eps_km=3.5, time_scale_km=5.0):
    """
    Groups individual thermal anomaly pixels into contiguous wildfire events
    using 4D spatiotemporal DBSCAN (3D Cartesian coordinates + temporal scale dimension).
    """
    t0 = time.time()
    print(f"[{sensor_name}] Spatiotemporal DBSCAN clustering of {len(df):,} pixels...")
    
    # Coordinates in 3D Cartesian space
    lat_rad = np.radians(df['latitude'].values)
    lon_rad = np.radians(df['longitude'].values)
    R = 6371.0
    x = R * np.cos(lat_rad) * np.cos(lon_rad)
    y = R * np.cos(lat_rad) * np.sin(lon_rad)
    z = R * np.sin(lat_rad)
    
    # Temporal dimension: day offset scaled so 1 day separation = time_scale_km
    dates = pd.to_datetime(df['acq_date'])
    min_date = dates.min()
    day_offsets = (dates - min_date).dt.total_seconds() / 86400.0
    t_scaled = day_offsets.values * time_scale_km
    
    features_4d = np.column_stack([x, y, z, t_scaled])
    
    # DBSCAN clustering
    db = DBSCAN(eps=eps_km, min_samples=1, metric='euclidean', n_jobs=-1)
    labels = db.fit_predict(features_4d)
    
    df['cluster_label'] = labels
    n_clusters = len(set(labels))
    print(f"[{sensor_name}] Formed {n_clusters:,} discrete wildfire event clusters in {time.time()-t0:.2f}s.")
    
    # Vectorized / GroupBy aggregation for speed
    grouped = df.groupby('cluster_label')
    agg_df = grouped.agg(
        centroid_lat=('latitude', 'mean'),
        centroid_lon=('longitude', 'mean'),
        start_date=('acq_date', 'min'),
        end_date=('acq_date', 'max'),
        pixel_count=('latitude', 'count'),
        total_frp_mw=('frp', 'sum'),
        mean_frp_mw=('frp', 'mean'),
        max_frp_mw=('frp', 'max'),
        min_lat=('latitude', 'min'),
        max_lat=('latitude', 'max'),
        min_lon=('longitude', 'min'),
        max_lon=('longitude', 'max')
    ).reset_index()
    
    # Calculate duration and approximate radius / area
    start_dt = pd.to_datetime(agg_df['start_date'])
    end_dt = pd.to_datetime(agg_df['end_date'])
    agg_df['duration_days'] = (end_dt - start_dt).dt.days + 1
    
    # Approximate radius from bounding box
    d_lat = haversine_np(agg_df['min_lat'], agg_df['centroid_lon'], agg_df['max_lat'], agg_df['centroid_lon'])
    d_lon = haversine_np(agg_df['centroid_lat'], agg_df['min_lon'], agg_df['centroid_lat'], agg_df['max_lon'])
    agg_df['radius_km'] = np.round(np.maximum(d_lat, d_lon) / 2.0, 2)
    agg_df['radius_km'] = np.where(agg_df['radius_km'] < 0.5, 0.5, agg_df['radius_km'])
    agg_df['estimated_area_km2'] = np.round(np.pi * (agg_df['radius_km'] ** 2), 2)
    
    # Format columns
    agg_df['centroid_lat'] = agg_df['centroid_lat'].round(5)
    agg_df['centroid_lon'] = agg_df['centroid_lon'].round(5)
    agg_df['total_frp_mw'] = agg_df['total_frp_mw'].round(2)
    agg_df['mean_frp_mw'] = agg_df['mean_frp_mw'].round(2)
    agg_df['max_frp_mw'] = agg_df['max_frp_mw'].round(2)
    
    prefix = 'WF_MODIS' if 'MODIS' in sensor_name else 'WF_VIIRS'
    agg_df['event_id'] = [f"{prefix}_{i:06d}" for i in range(1, len(agg_df) + 1)]
    agg_df['sensor_source'] = sensor_name
    agg_df['is_multi_pixel'] = np.where(agg_df['pixel_count'] > 1, 1, 0)
    
    cols = [
        'event_id', 'sensor_source', 'start_date', 'end_date', 'duration_days',
        'centroid_lat', 'centroid_lon', 'pixel_count', 'is_multi_pixel',
        'radius_km', 'estimated_area_km2', 'total_frp_mw', 'mean_frp_mw', 'max_frp_mw'
    ]
    return agg_df[cols]

def process_all_wildfires():
    print("="*70)
    print("HAZARD 5: WILDFIRE DATA CLEANING, DBSCAN CLUSTERING & VERIFICATION")
    print("="*70)
    
    # 1. MODIS Active Fire
    modis_raw = os.path.join(RAW_WILD_DIR, 'modis_active_fire_global_7d.csv')
    df_m = pd.read_csv(modis_raw)
    df_m['latitude'] = pd.to_numeric(df_m['latitude'], errors='coerce')
    df_m['longitude'] = pd.to_numeric(df_m['longitude'], errors='coerce')
    df_m['frp'] = pd.to_numeric(df_m['frp'], errors='coerce').fillna(0.0)
    df_m['confidence'] = pd.to_numeric(df_m['confidence'], errors='coerce').fillna(50)
    
    df_m_clean = df_m[
        df_m['latitude'].notnull() & df_m['longitude'].notnull() &
        (df_m['latitude'] >= -90) & (df_m['latitude'] <= 90) &
        (df_m['longitude'] >= -180) & (df_m['longitude'] <= 180) &
        (df_m['confidence'] >= 30)
    ].copy()
    
    df_modis_events = cluster_active_fires_dbscan(df_m_clean, sensor_name='MODIS_C6_1', eps_km=3.5)
    modis_out = os.path.join(PROC_WILD_DIR, 'wildfire_events_cleaned_catalog.csv')
    df_modis_events.to_csv(modis_out, index=False)
    print(f"[MODIS Events Catalog] Saved {len(df_modis_events):,} discrete events to {modis_out}")
    
    # 2. VIIRS Active Fire
    viirs_raw = os.path.join(RAW_WILD_DIR, 'viirs_active_fire_global_7d.csv')
    df_v = pd.read_csv(viirs_raw)
    df_v['latitude'] = pd.to_numeric(df_v['latitude'], errors='coerce')
    df_v['longitude'] = pd.to_numeric(df_v['longitude'], errors='coerce')
    df_v['frp'] = pd.to_numeric(df_v['frp'], errors='coerce').fillna(0.0)
    
    # VIIRS confidence: 'low', 'nominal', 'high'
    df_v_clean = df_v[
        df_v['latitude'].notnull() & df_v['longitude'].notnull() &
        (df_v['latitude'] >= -90) & (df_v['latitude'] <= 90) &
        (df_v['longitude'] >= -180) & (df_v['longitude'] <= 180) &
        (df_v['confidence'].astype(str).str.lower() != 'low')
    ].copy()
    
    df_viirs_events = cluster_active_fires_dbscan(df_v_clean, sensor_name='VIIRS_375m', eps_km=3.0)
    viirs_out = os.path.join(PROC_WILD_DIR, 'wildfire_events_viirs_catalog.csv')
    df_viirs_events.to_csv(viirs_out, index=False)
    print(f"[VIIRS Events Catalog] Saved {len(df_viirs_events):,} discrete events to {viirs_out}")
    
    # 3. GLIDE Wildfire Disasters
    glide_raw = os.path.join(RAW_WILD_DIR, 'glide_wildfire_disaster_events.csv')
    df_g = pd.read_csv(glide_raw)
    df_g['latitude'] = pd.to_numeric(df_g['latitude'], errors='coerce')
    df_g['longitude'] = pd.to_numeric(df_g['longitude'], errors='coerce')
    df_g['killed'] = pd.to_numeric(df_g['killed'], errors='coerce').fillna(0)
    df_g['affected'] = pd.to_numeric(df_g['affected'], errors='coerce').fillna(0)
    
    df_g_clean = df_g[
        df_g['latitude'].notnull() & df_g['longitude'].notnull() &
        (df_g['latitude'] >= -90) & (df_g['latitude'] <= 90) &
        (df_g['longitude'] >= -180) & (df_g['longitude'] <= 180)
    ].copy()
    glide_out = os.path.join(PROC_WILD_DIR, 'wildfire_disaster_events_glide.csv')
    df_g_clean.to_csv(glide_out, index=False)
    print(f"[GLIDE Disasters] Saved {len(df_g_clean):,} disaster events to {glide_out}")
    
    # 4. Feature Specification for Wildfire XGBoost
    feature_spec = {
        "hazard": "Wildfires",
        "task": "Wildfire Ignition Probability & Spread Susceptibility Assessment",
        "model_architecture": "XGBoost Classifier / Regressor",
        "target_variables": {
            "wildfire_occurrence": "Binary indicator (1 = verified wildfire event, 0 = non-fire background sample)",
            "fire_radiative_power_mw": "Continuous peak FRP (fire intensity and severity)",
            "fire_duration_days": "Duration of active burning episode",
            "burned_area_class": "Categorical severity class (Low, Medium, High, Extreme)"
        },
        "environmental_features_required": [
            {
                "feature": "2m_temperature_celsius",
                "source": "ERA5 Reanalysis (ECMWF)",
                "temporal_resolution": "Daily / Hourly",
                "spatial_resolution": "0.25° (~31 km)",
                "description": "Ambient surface air temperature at 2 meters elevation"
            },
            {
                "feature": "relative_humidity_pct",
                "source": "ERA5 Reanalysis (ECMWF)",
                "temporal_resolution": "Daily / Hourly",
                "spatial_resolution": "0.25° (~31 km)",
                "description": "Surface relative humidity; critical threshold < 20% indicates extreme fire danger"
            },
            {
                "feature": "10m_wind_speed_ms",
                "source": "ERA5 Reanalysis (ECMWF)",
                "temporal_resolution": "Daily / Hourly",
                "spatial_resolution": "0.25° (~31 km)",
                "description": "Wind velocity at 10 meters; drives rate of fire spread and spotting"
            },
            {
                "feature": "fwi_fire_weather_index",
                "source": "Copernicus CEMS / ERA5 Fire Weather",
                "temporal_resolution": "Daily",
                "spatial_resolution": "0.25° (~31 km)",
                "description": "Canadian Forest Fire Weather Index (FFMC, DMC, DC, ISI, BUI, FWI)"
            },
            {
                "feature": "volumetric_soil_water_layer1",
                "source": "ERA5-Land",
                "temporal_resolution": "Daily",
                "spatial_resolution": "0.1° (~9 km)",
                "description": "Topsoil moisture (0-7 cm depth); proxy for fine fuel moisture"
            },
            {
                "feature": "precipitation_accumulated_7d_mm",
                "source": "NASA GPM / IMERG or ERA5",
                "temporal_resolution": "Daily aggregate",
                "spatial_resolution": "0.1° (~10 km)",
                "description": "7-day cumulative rainfall prior to observation date"
            },
            {
                "feature": "ndvi_vegetation_greenness",
                "source": "MODIS (MOD13A2) or Sentinel-2",
                "temporal_resolution": "16-day composite",
                "spatial_resolution": "250m to 1km",
                "description": "Normalized Difference Vegetation Index; proxy for live fuel load and curing status"
            },
            {
                "feature": "terrain_slope_degrees",
                "source": "SRTM 30m DEM (NASA / USGS)",
                "temporal_resolution": "Static",
                "spatial_resolution": "30m / 1 arc-second",
                "description": "Topographical slope; fires burn significantly faster uphill due to preheating"
            },
            {
                "feature": "land_cover_fuel_type",
                "source": "ESA WorldCover / MODIS MCD12Q1",
                "temporal_resolution": "Annual static",
                "spatial_resolution": "10m to 500m",
                "description": "Vegetation classification (forest, shrubland, grassland, cropland, wetland, barren)"
            },
            {
                "feature": "distance_to_roads_km",
                "source": "OpenStreetMap (OSM)",
                "temporal_resolution": "Static",
                "spatial_resolution": "Vector",
                "description": "Human accessibility proxy; >80% of global wildfires are human-ignited near infrastructure"
            }
        ],
        "training_strategy": {
            "positive_samples": "Verified discrete wildfire event centroids with documented burning duration and FRP",
            "negative_samples": "Spatiotemporally matched non-fire background locations sampled across same climate zones and seasons",
            "cross_validation": "Spatial Block or Temporal K-Fold Cross-Validation to prevent spatial autocorrelation leakage",
            "evaluation_metrics": ["AUC-ROC", "PR-AUC", "F1-Score", "Brier Score", "Confusion Matrix"]
        }
    }
    
    spec_path = os.path.join(PROC_WILD_DIR, 'wildfire_environmental_features_spec.json')
    with open(spec_path, 'w') as f:
        json.dump(feature_spec, f, indent=2)
    print(f"[Feature Spec] Saved Wildfire ML feature specification to {spec_path}")

if __name__ == '__main__':
    process_all_wildfires()
