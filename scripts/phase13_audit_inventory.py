"""
HAZARDX AI — Phase 13 Step 1: Complete Model & Dataset Inventory Audit
Extracts full metadata, schemas, temporal splits, geographic ranges, class distributions,
data hygiene, and operational governance across all 12 models and 5 datasets.
"""

import os
import sys
import json
import numpy as np
import pandas as pd

# Set paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

DATA_DIR = os.path.join(BASE_DIR, 'data', 'model_ready')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

from scripts.ml_pipeline.config import HAZARD_CONFIGS

def audit_datasets_and_models():
    inventory = {
        "datasets": {},
        "models": []
    }
    
    # 1. Dataset Audit
    print("=== AUDITING 5 MODEL-READY DATASETS ===")
    for hazard_key, cfg in HAZARD_CONFIGS.items():
        csv_path = cfg['dataset_path']
        df = pd.read_csv(csv_path)
        
        # Hygiene checks
        missing_count = int(df.isna().sum().sum())
        dup_count = int(df.duplicated().sum())
        
        # Coordinates check
        lat_col = 'latitude' if 'latitude' in df.columns else None
        lon_col = 'longitude' if 'longitude' in df.columns else None
        coord_valid = False
        lat_range = None
        lon_range = None
        if lat_col and lon_col:
            valid_lat = df[lat_col].between(-90, 90).all()
            valid_lon = df[lon_col].between(-180, 180).all()
            coord_valid = bool(valid_lat and valid_lon)
            lat_range = [float(df[lat_col].min()), float(df[lat_col].max())]
            lon_range = [float(df[lon_col].min()), float(df[lon_col].max())]
            
        # Time / Temporal checks
        time_col = 'timestamp' if 'timestamp' in df.columns else None
        time_min = None
        time_max = None
        if time_col:
            df['parsed_time'] = pd.to_datetime(df[time_col], errors='coerce')
            time_min = str(df['parsed_time'].min())
            time_max = str(df['parsed_time'].max())
            
        # Splits check
        splits = df['split'].value_counts().to_dict() if 'split' in df.columns else {}
        split_periods = {}
        if time_col and 'split' in df.columns:
            for s in ['train', 'val', 'test']:
                s_df = df[df['split'] == s]
                if not s_df.empty:
                    split_periods[s] = {
                        "count": len(s_df),
                        "start": str(s_df['parsed_time'].min()),
                        "end": str(s_df['parsed_time'].max())
                    }
                    
        # Feature columns
        feature_cols = cfg['features']
        missing_feats = [f for f in feature_cols if f not in df.columns]
        
        dataset_meta = {
            "hazard": hazard_key,
            "file_name": os.path.basename(csv_path),
            "total_rows": len(df),
            "total_cols": len(df.columns),
            "missing_values": missing_count,
            "duplicate_records": dup_count,
            "coord_valid": coord_valid,
            "latitude_range": lat_range,
            "longitude_range": lon_range,
            "temporal_span": [time_min, time_max] if time_min else None,
            "splits": splits,
            "split_periods": split_periods,
            "feature_count": len(feature_cols),
            "features": feature_cols,
            "categorical_features": cfg.get('categorical_features', []),
            "missing_features": missing_feats
        }
        inventory["datasets"][hazard_key] = dataset_meta
        print(f"[{hazard_key.upper()}] Rows: {len(df)}, Missing: {missing_count}, Dups: {dup_count}, Splits: {splits}")
        
    # 2. Model Audit
    print("\n=== AUDITING 12 MACHINE LEARNING MODELS ===")
    with open(os.path.join(MODELS_DIR, 'model_comparison_dashboard.json'), 'r') as f:
        dashboard = json.load(f)
        
    for entry in dashboard:
        hazard_name = entry['hazard'].lower()
        task_name = entry['prediction_target']
        target_col = entry['target_column']
        task_type = entry['task_type']
        
        # Load corresponding metadata json
        meta_file = f"{hazard_name}_{task_name}_xgboost_metadata.json"
        meta_path = os.path.join(MODELS_DIR, hazard_name, meta_file)
        model_meta = {}
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as mf:
                model_meta = json.load(mf)
                
        # Check operational status from config
        sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, 'backend')))
        from backend.app.config import settings
        status_key = f"{hazard_name}_{task_name}"
        op_status = settings.MODEL_STATUS.get(status_key, "UNKNOWN")
        
        # Class distribution in dataset
        ds = inventory["datasets"].get(hazard_name)
        class_dist = None
        if ds and task_type in ['binary_classification', 'multiclass_classification']:
            raw_csv = os.path.join(DATA_DIR, hazard_name, ds["file_name"])
            raw_df = pd.read_csv(raw_csv)
            if target_col in raw_df.columns:
                class_dist = raw_df[target_col].value_counts().to_dict()
                
        # Split periods from dataset
        split_periods = ds.get("split_periods", {}) if ds else {}
        
        # Determine known limitations
        limitations = []
        if op_status == "UNAVAILABLE_FOR_OPERATIONAL_USE":
            limitations.append("Blocked from operational inference due to non-generalizing holdout R2 (<0)")
        elif op_status == "EXPERIMENTAL":
            limitations.append("Experimental advisory tier only; not certified for critical life-safety warnings")
        if task_type == 'binary_classification' and class_dist:
            min_c = min(class_dist.values())
            max_c = max(class_dist.values())
            if max_c / min_c > 3.0:
                limitations.append(f"Significant class imbalance ({max_c}:{min_c}); requires threshold tuning and PR-AUC focus")
        if hazard_name == 'earthquakes':
            limitations.append("Strict non-predictive governance: regional aftershock sequence estimation only (no deterministic prediction)")
            
        model_record = {
            "hazard": hazard_name,
            "task_name": task_name,
            "target_variable": target_col,
            "task_type": task_type,
            "algorithm": entry.get('algorithm', 'XGBoost'),
            "training_dataset": ds["file_name"] if ds else None,
            "training_period": split_periods.get("train", {}).get("start", "") + " to " + split_periods.get("train", {}).get("end", "") if "train" in split_periods else "Walk-forward / Grouped",
            "validation_period": split_periods.get("val", {}).get("start", "") + " to " + split_periods.get("val", {}).get("end", "") if "val" in split_periods else "Walk-forward / Grouped",
            "test_period": split_periods.get("test", {}).get("start", "") + " to " + split_periods.get("test", {}).get("end", "") if "test" in split_periods else "Walk-forward / Grouped",
            "train_samples": entry.get('train_sample_count'),
            "val_samples": entry.get('val_sample_count'),
            "test_samples": entry.get('test_sample_count'),
            "input_features": model_meta.get('features', []),
            "feature_count": len(model_meta.get('features', [])),
            "primary_metric": entry.get('primary_metric_name'),
            "primary_test_score": entry.get('primary_test_score'),
            "secondary_metric": entry.get('secondary_metric_name'),
            "secondary_test_score": entry.get('secondary_test_score'),
            "operational_status": op_status,
            "class_distribution": class_dist,
            "known_limitations": limitations
        }
        inventory["models"].append(model_record)
        print(f"Model: {hazard_name}_{task_name} | Status: {op_status} | Primary: {entry.get('primary_metric_name')}={entry.get('primary_test_score')}")

    out_path = os.path.join(REPORTS_DIR, 'phase13_model_and_dataset_inventory.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=2)
    print(f"\n[SUCCESS] Inventory compiled and saved to {out_path}")
    return inventory

if __name__ == '__main__':
    audit_datasets_and_models()
