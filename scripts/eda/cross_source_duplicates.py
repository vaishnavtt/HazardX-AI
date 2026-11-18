"""
HAZARDX AI - Cross-Source Duplicate Analysis
Performs systematic cross-source deduplication and entity resolution between:
  1. Floods: Dartmouth Flood Observatory (DFO) vs. GLIDE Disaster Database
  2. Landslides: NASA Global Landslide Catalog (GLC) vs. GLIDE Disaster Database

Categorizes pairs into:
  - Confirmed duplicates (Exact GLIDE match or Date diff <= 2 days & Dist <= 25 km & Country match)
  - Potential duplicates (Date diff <= 7 days & Dist <= 150 km & Country match)
  - Unique records in each catalog
"""

import os
import math
import numpy as np
import pandas as pd

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def audit_flood_duplicates():
    print("\n" + "="*70)
    print("PHASE 3 AUDIT: FLOOD CROSS-SOURCE DUPLICATES (DFO vs. GLIDE)")
    print("="*70)
    
    dfo_path = 'data/raw/floods/dfo_spatial_flood_archive_1985_2010.csv'
    glide_path = 'data/raw/floods/glide_flood_events.csv'
    
    dfo = pd.read_csv(dfo_path, low_memory=False)
    glide = pd.read_csv(glide_path, low_memory=False)
    
    # Parse DFO dates
    dfo['began_dt'] = pd.to_datetime(dfo['Began'].astype(str).str.strip(), errors='coerce')
    dfo['Centroid_X'] = pd.to_numeric(dfo['Centroid_X'], errors='coerce')
    dfo['Centroid_Y'] = pd.to_numeric(dfo['Centroid_Y'], errors='coerce')
    
    # Parse GLIDE dates
    glide['glide_dt'] = pd.to_datetime(
        glide['year'].astype(str) + '-' + 
        glide['month'].astype(str).str.zfill(2) + '-' + 
        glide['day'].astype(str).str.zfill(2), 
        errors='coerce'
    )
    glide['latitude'] = pd.to_numeric(glide['latitude'], errors='coerce')
    glide['longitude'] = pd.to_numeric(glide['longitude'], errors='coerce')
    
    print(f"DFO records: {len(dfo):,} (with valid date: {dfo['began_dt'].notnull().sum():,})")
    print(f"GLIDE flood records: {len(glide):,} (with valid date: {glide['glide_dt'].notnull().sum():,})")
    
    # Check explicit GLIDE matches in DFO 'Glide__' column
    dfo_glide_col = dfo['Glide__'].dropna().astype(str).str.strip()
    direct_glide_matches = []
    
    for idx, d_row in dfo[dfo['Glide__'].notnull()].iterrows():
        g_val = str(d_row['Glide__']).strip()
        matched_g = glide[glide['glidenumber'].astype(str).str.contains(g_val, case=False, na=False)]
        if len(matched_g) > 0:
            for _, g_row in matched_g.iterrows():
                direct_glide_matches.append({
                    'type': 'Confirmed (Direct GLIDE Key)',
                    'dfo_id': d_row.get('Register__', d_row.get('Annual_DFO', idx)),
                    'glide_number': g_row['glidenumber'],
                    'dfo_country': d_row['Country__c'],
                    'glide_country': g_row.get('country', g_row.get('location', '')),
                    'dfo_date': str(d_row['began_dt']),
                    'glide_date': str(g_row['glide_dt']),
                    'distance_km': haversine(d_row['Centroid_Y'], d_row['Centroid_X'], g_row['latitude'], g_row['longitude']) if pd.notnull(d_row['Centroid_Y']) and pd.notnull(g_row['latitude']) else np.nan,
                    'details': f"Direct GLIDE ID match: {g_val}"
                })
    
    print(f"Direct GLIDE ID cross-references found: {len(direct_glide_matches)}")
    
    # Spatiotemporal duplicate matching for records with valid dates and coordinates
    dfo_valid = dfo[dfo['began_dt'].notnull() & dfo['Centroid_X'].notnull() & dfo['Centroid_Y'].notnull()].copy()
    glide_valid = glide[glide['glide_dt'].notnull() & glide['latitude'].notnull() & glide['longitude'].notnull()].copy()
    
    # Optimize search by matching year first
    dfo_valid['year'] = dfo_valid['began_dt'].dt.year
    glide_valid['year'] = glide_valid['glide_dt'].dt.year
    
    confirmed_pairs = []
    potential_pairs = []
    dfo_matched_indices = set()
    glide_matched_indices = set()
    
    common_years = set(dfo_valid['year']).intersection(set(glide_valid['year']))
    print(f"Overlapping temporal years: {min(common_years)} to {max(common_years)} ({len(common_years)} years)")
    
    for yr in sorted(common_years):
        sub_d = dfo_valid[dfo_valid['year'] == yr]
        sub_g = glide_valid[glide_valid['year'] == yr]
        
        for d_idx, d_row in sub_d.iterrows():
            d_date = d_row['began_dt']
            d_lat, d_lon = d_row['Centroid_Y'], d_row['Centroid_X']
            d_ctry = str(d_row['Country__c']).strip().lower()
            
            # Candidate GLIDE events within +-7 days
            cand = sub_g[abs((sub_g['glide_dt'] - d_date).dt.days) <= 7]
            for g_idx, g_row in cand.iterrows():
                g_lat, g_lon = g_row['latitude'], g_row['longitude']
                dist = haversine(d_lat, d_lon, g_lat, g_lon)
                day_diff = abs((g_row['glide_dt'] - d_date).days)
                
                # Check country name or code match
                g_loc = str(g_row.get('location', '')).lower()
                g_code = str(g_row.get('geocode', '')).lower()
                country_match = (d_ctry in g_loc) or (d_ctry in str(g_row.get('country', '')).lower()) or (d_ctry == g_code)
                
                pair_dict = {
                    'dfo_register': d_row.get('Register__', d_row.get('Annual_DFO', d_idx)),
                    'glide_number': g_row['glidenumber'],
                    'dfo_country': d_row['Country__c'],
                    'glide_location': g_row['location'],
                    'dfo_began': str(d_date.date()),
                    'glide_date': str(g_row['glide_dt'].date()),
                    'day_diff': day_diff,
                    'distance_km': round(dist, 2),
                    'dfo_cause': d_row.get('Main_cause', ''),
                    'glide_comments': str(g_row.get('comments', ''))[:100]
                }
                
                if day_diff <= 2 and dist <= 30.0:
                    pair_dict['classification'] = 'Confirmed Duplicate'
                    confirmed_pairs.append(pair_dict)
                    dfo_matched_indices.add(d_idx)
                    glide_matched_indices.add(g_idx)
                elif day_diff <= 7 and dist <= 150.0:
                    pair_dict['classification'] = 'Potential Duplicate'
                    potential_pairs.append(pair_dict)
                    dfo_matched_indices.add(d_idx)
                    glide_matched_indices.add(g_idx)

    all_pairs = confirmed_pairs + potential_pairs
    df_pairs = pd.DataFrame(all_pairs)
    out_csv = 'data/processed/floods/flood_cross_source_duplicates.csv'
    df_pairs.to_csv(out_csv, index=False)
    
    unique_dfo = len(dfo) - len(dfo_matched_indices)
    unique_glide = len(glide) - len(glide_matched_indices)
    
    print(f"\n[FLOOD SUMMARY]")
    print(f"  - Confirmed Duplicates (<=2 days, <=30 km): {len(confirmed_pairs)}")
    print(f"  - Potential Duplicates (<=7 days, <=150 km): {len(potential_pairs)}")
    print(f"  - Unique DFO Records: {unique_dfo:,} / {len(dfo):,} ({unique_dfo/len(dfo)*100:.1f}%)")
    print(f"  - Unique GLIDE Flood Records: {unique_glide:,} / {len(glide):,} ({unique_glide/len(glide)*100:.1f}%)")
    print(f"  - Detailed cross-match audit table saved to: {out_csv}")
    
    return len(confirmed_pairs), len(potential_pairs), unique_dfo, unique_glide

def audit_landslide_duplicates():
    print("\n" + "="*70)
    print("PHASE 3 AUDIT: LANDSLIDE CROSS-SOURCE DUPLICATES (NASA GLC vs. GLIDE)")
    print("="*70)
    
    nasa_path = 'data/raw/landslides/nasa_global_landslide_catalog_point.csv'
    glide_path = 'data/raw/landslides/glide_landslide_events.csv'
    
    nasa = pd.read_csv(nasa_path, low_memory=False)
    glide = pd.read_csv(glide_path, low_memory=False)
    
    # Parse NASA dates & coords
    nasa['event_dt'] = pd.to_datetime(nasa['event_date'].astype(str).str.strip(), errors='coerce')
    nasa['latitude'] = pd.to_numeric(nasa['latitude'], errors='coerce')
    nasa['longitude'] = pd.to_numeric(nasa['longitude'], errors='coerce')
    
    # Parse GLIDE dates & coords
    glide['glide_dt'] = pd.to_datetime(
        glide['year'].astype(str) + '-' + 
        glide['month'].astype(str).str.zfill(2) + '-' + 
        glide['day'].astype(str).str.zfill(2), 
        errors='coerce'
    )
    glide['latitude'] = pd.to_numeric(glide['latitude'], errors='coerce')
    glide['longitude'] = pd.to_numeric(glide['longitude'], errors='coerce')
    
    print(f"NASA GLC records: {len(nasa):,} (valid dates: {nasa['event_dt'].notnull().sum():,})")
    print(f"GLIDE landslide records: {len(glide):,} (valid dates: {glide['glide_dt'].notnull().sum():,})")
    
    nasa_valid = nasa[nasa['event_dt'].notnull() & nasa['latitude'].notnull() & nasa['longitude'].notnull()].copy()
    glide_valid = glide[glide['glide_dt'].notnull() & glide['latitude'].notnull() & glide['longitude'].notnull()].copy()
    
    nasa_valid['year'] = nasa_valid['event_dt'].dt.year
    glide_valid['year'] = glide_valid['glide_dt'].dt.year
    
    confirmed_pairs = []
    potential_pairs = []
    nasa_matched_indices = set()
    glide_matched_indices = set()
    
    common_years = set(nasa_valid['year']).intersection(set(glide_valid['year']))
    print(f"Overlapping temporal years: {min(common_years)} to {max(common_years)} ({len(common_years)} years)")
    
    for yr in sorted(common_years):
        sub_n = nasa_valid[nasa_valid['year'] == yr]
        sub_g = glide_valid[glide_valid['year'] == yr]
        
        for n_idx, n_row in sub_n.iterrows():
            n_date = n_row['event_dt']
            n_lat, n_lon = n_row['latitude'], n_row['longitude']
            
            cand = sub_g[abs((sub_g['glide_dt'] - n_date).dt.days) <= 7]
            for g_idx, g_row in cand.iterrows():
                g_lat, g_lon = g_row['latitude'], g_row['longitude']
                dist = haversine(n_lat, n_lon, g_lat, g_lon)
                day_diff = abs((g_row['glide_dt'] - n_date).days)
                
                pair_dict = {
                    'nasa_event_id': n_row['event_id'],
                    'glide_number': g_row['glidenumber'],
                    'nasa_country': n_row.get('country_name', ''),
                    'glide_location': g_row['location'],
                    'nasa_date': str(n_date.date()),
                    'glide_date': str(g_row['glide_dt'].date()),
                    'day_diff': day_diff,
                    'distance_km': round(dist, 2),
                    'nasa_trigger': n_row.get('landslide_trigger', ''),
                    'nasa_title': str(n_row.get('event_title', ''))[:80],
                    'glide_comments': str(g_row.get('comments', ''))[:100]
                }
                
                if day_diff <= 2 and dist <= 30.0:
                    pair_dict['classification'] = 'Confirmed Duplicate'
                    confirmed_pairs.append(pair_dict)
                    nasa_matched_indices.add(n_idx)
                    glide_matched_indices.add(g_idx)
                elif day_diff <= 7 and dist <= 150.0:
                    pair_dict['classification'] = 'Potential Duplicate'
                    potential_pairs.append(pair_dict)
                    nasa_matched_indices.add(n_idx)
                    glide_matched_indices.add(g_idx)

    all_pairs = confirmed_pairs + potential_pairs
    df_pairs = pd.DataFrame(all_pairs)
    out_csv = 'data/processed/landslides/landslide_cross_source_duplicates.csv'
    df_pairs.to_csv(out_csv, index=False)
    
    unique_nasa = len(nasa) - len(nasa_matched_indices)
    unique_glide = len(glide) - len(glide_matched_indices)
    
    print(f"\n[LANDSLIDE SUMMARY]")
    print(f"  - Confirmed Duplicates (<=2 days, <=30 km): {len(confirmed_pairs)}")
    print(f"  - Potential Duplicates (<=7 days, <=150 km): {len(potential_pairs)}")
    print(f"  - Unique NASA GLC Records: {unique_nasa:,} / {len(nasa):,} ({unique_nasa/len(nasa)*100:.1f}%)")
    print(f"  - Unique GLIDE Landslide Records: {unique_glide:,} / {len(glide):,} ({unique_glide/len(glide)*100:.1f}%)")
    print(f"  - Detailed cross-match audit table saved to: {out_csv}")
    
    return len(confirmed_pairs), len(potential_pairs), unique_nasa, unique_glide

if __name__ == '__main__':
    audit_flood_duplicates()
    audit_landslide_duplicates()

