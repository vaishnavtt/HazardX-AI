"""
HAZARDX AI — Dataset Loader & Feature Split Extractor
Loads model-ready CSVs, performs strict partition separation, encodes categoricals without leakage,
and guarantees that test splits remain untouched.
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
import joblib

def load_hazard_dataset(hazard_key, config):
    """
    Loads dataset for a specific hazard, validates schema, encodes categorical variables
    strictly on the training partition, and returns train, val, and test splits.
    """
    path = config['dataset_path']
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset for {hazard_key} not found at {path}")
    
    df = pd.read_csv(path)
    features = list(config['features'])
    cat_features = list(config['categorical_features'])
    
    # Verify no target or identifier leakage into features
    disallowed_cols = {'event_id', 'SID', 'NAME', 'SEASON', 'timestamp', 'split', 'sample_type'}
    for feat in features:
        if feat in disallowed_cols:
            raise ValueError(f"CRITICAL LEAKAGE: Metadata column '{feat}' found in feature list for {hazard_key}!")
        if feat not in df.columns:
            raise KeyError(f"Feature '{feat}' missing from {path}")
    
    # Split partitions
    train_mask = df['split'] == 'train'
    val_mask = df['split'] == 'val'
    test_mask = df['split'] == 'test'
    
    if not (train_mask.any() and val_mask.any() and test_mask.any()):
        raise ValueError(f"Incomplete split assignments in {path}. Splits found: {df['split'].unique()}")
    
    # Extract feature matrices
    X_train = df.loc[train_mask, features].copy()
    X_val = df.loc[val_mask, features].copy()
    X_test = df.loc[test_mask, features].copy()
    
    # Handle categorical variables (e.g., nearest_fault_slip_type in earthquakes)
    encoder = None
    if cat_features:
        encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
        # Fit strictly on train! Never fit on val or test!
        X_train[cat_features] = encoder.fit_transform(X_train[cat_features].astype(str))
        X_val[cat_features] = encoder.transform(X_val[cat_features].astype(str))
        X_test[cat_features] = encoder.transform(X_test[cat_features].astype(str))
        
        # Save encoder artifact
        enc_path = os.path.join(config['model_dir'], f"{hazard_key}_categorical_encoder.joblib")
        joblib.dump(encoder, enc_path)
    
    # Ensure all dtypes are numeric float64 / int64
    X_train = X_train.astype(np.float64)
    X_val = X_val.astype(np.float64)
    X_test = X_test.astype(np.float64)
    
    # Extract target series for each task
    target_data = {}
    for task_name, task_cfg in config['tasks'].items():
        t_col = task_cfg['target']
        if t_col not in df.columns:
            raise KeyError(f"Target variable '{t_col}' missing from {path}")
            
        y_train = df.loc[train_mask, t_col].copy()
        y_val = df.loc[val_mask, t_col].copy()
        y_test = df.loc[test_mask, t_col].copy()
        
        if task_cfg['type'] in ['binary_classification', 'multiclass_classification']:
            y_train = y_train.astype(int)
            y_val = y_val.astype(int)
            y_test = y_test.astype(int)
        else:
            y_train = y_train.astype(float)
            y_val = y_val.astype(float)
            y_test = y_test.astype(float)
            
        target_data[task_name] = {
            'y_train': y_train,
            'y_val': y_val,
            'y_test': y_test
        }
    
    return {
        'hazard': hazard_key,
        'features': features,
        'X_train': X_train,
        'X_val': X_val,
        'X_test': X_test,
        'target_data': target_data,
        'raw_df': df,
        'encoder': encoder
    }

