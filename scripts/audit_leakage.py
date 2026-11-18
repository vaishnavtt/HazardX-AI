import os
import pandas as pd
import numpy as np

events = [
    ('floods', 'Henan', '2021-07-20', 34.75, 113.63),
    ('floods', 'Katrina', '2005-08-29', 29.95, -90.07),
    ('landslides', 'Wayanad', '2024-07-30', 11.53, 76.22),
    ('landslides', 'Oso', '2014-03-22', 48.28, -121.84),
    ('earthquakes', 'Gorkha', '2015-04-25', 28.15, 84.71),
    ('earthquakes', 'Kumamoto', '2016-04-15', 32.75, 130.76),
    ('cyclones', 'Haiyan', '2013-11-08', 11.0, 125.0),
    ('cyclones', 'Amphan', '2020-05-20', 21.7, 88.3),
    ('wildfires', 'Camp Fire', '2018-11-08', 39.81, -121.44),
    ('wildfires', 'Black Summer', '2019-12-31', -35.3, 150.1)
]

paths = {
    'floods': 'data/model_ready/floods/flood_model_ready.csv',
    'landslides': 'data/model_ready/landslides/landslide_model_ready.csv',
    'earthquakes': 'data/model_ready/earthquakes/earthquake_model_ready.csv',
    'cyclones': 'data/model_ready/cyclones/cyclone_model_ready.csv',
    'wildfires': 'data/model_ready/wildfires/wildfire_model_ready.csv'
}

print("=== CHECKING FOR TRAIN/TEST CONTAMINATION IN 10 HISTORICAL DISASTER EVENTS ===")
for hazard, name, dt, lat, lon in events:
    csv_path = paths[hazard]
    df = pd.read_csv(csv_path)
    
    lat_cols = [c for c in df.columns if 'lat' in c.lower()]
    lon_cols = [c for c in df.columns if 'lon' in c.lower()]
    time_cols = [c for c in df.columns if any(k in c.lower() for k in ['time', 'date'])]
    
    lat_col = lat_cols[0] if lat_cols else None
    lon_col = lon_cols[0] if lon_cols else None
    time_col = time_cols[0] if time_cols else None
    
    nearby = df[(abs(df[lat_col] - lat) < 1.0) & (abs(df[lon_col] - lon) < 1.0)] if (lat_col and lon_col) else pd.DataFrame()
    
    print(f"\nHazard: {hazard:11s} | Event: {name:15s} | Target Date: {dt}")
    print(f"  Coordinates: ({lat:.2f}, {lon:.2f})")
    print(f"  Nearby spatially (+/- 1.0 deg): {len(nearby)} records")
    if len(nearby) > 0 and time_col:
        # Check temporal match
        nearby_time = nearby[nearby[time_col].astype(str).str.contains(dt[:7])]
        print(f"  Exact month temporal match ({dt[:7]}): {len(nearby_time)} records")
        if len(nearby_time) > 0:
            print("  Matched record splits:", nearby_time['split'].value_counts().to_dict())
            for idx, r in nearby_time.iterrows():
                print(f"    -> Record {idx}: Date={r.get(time_col)} | Split={r.get('split')}")
        else:
            print("  No temporal match in dataset for that month/year.")
    elif len(nearby) == 0:
        print("  Event location is NOT present in the dataset.")
