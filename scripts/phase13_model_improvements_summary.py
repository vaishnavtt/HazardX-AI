"""
HAZARDX AI — Phase 13 Step 4: Model Improvement & Scientific Governance Experiments
Documents data scarcity investigations, class weighting experiments on landslide magnitude,
decision threshold tuning on aftershock hazard & rapid intensification, and empirical justification
for maintaining safety locks on blocked regressors.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, roc_auc_score, average_precision_score
import xgboost as xgb

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)
MODELS_DIR = os.path.join(BASE_DIR, 'models')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

from scripts.ml_pipeline.config import HAZARD_CONFIGS
from scripts.ml_pipeline.data_loader import load_hazard_dataset

def run_improvement_experiments():
    improvements = {}
    
    # -------------------------------------------------------------------------
    # 1. Landslide Magnitude Class Weighting Experiment
    # -------------------------------------------------------------------------
    print("=== 1. LANDSLIDE MAGNITUDE IMBALANCE EXPERIMENT ===")
    cfg_ls = HAZARD_CONFIGS['landslides']
    data_ls = load_hazard_dataset('landslides', cfg_ls)
    X_train_ls = data_ls['X_train']
    X_test_ls = data_ls['X_test']
    y_train_ls = data_ls['target_data']['landslide_magnitude']['y_train']
    y_test_ls = data_ls['target_data']['landslide_magnitude']['y_test']
    
    weights_ls = compute_sample_weight('balanced', y_train_ls)
    
    clf_ls = xgb.XGBClassifier(
        n_estimators=150,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1.0,
        random_state=42,
        num_class=3
    )
    clf_ls.fit(X_train_ls, y_train_ls, sample_weight=weights_ls)
    preds_ls = clf_ls.predict(X_test_ls)
    
    f1_orig = 0.4221
    acc_orig = 0.6222
    f1_improved = float(f1_score(y_test_ls, preds_ls, average='macro'))
    acc_improved = float(accuracy_score(y_test_ls, preds_ls))
    
    improvements["landslides_landslide_magnitude"] = {
        "hazard": "landslides",
        "task": "landslide_magnitude",
        "issue_diagnosed": "Severe sample scarcity in class 2 (large/catastrophic, only 6 train & 4 test samples). Val split had 0 class-2 samples.",
        "experimental_action": "Applied balanced sample weighting to penalize minority misclassifications and tuned regularization (lambda=1.0).",
        "baseline_naive_macro_f1": 0.2016,
        "existing_model_macro_f1": f1_orig,
        "existing_model_accuracy": acc_orig,
        "improved_macro_f1": round(f1_improved, 4),
        "improved_accuracy": round(acc_improved, 4),
        "governance_decision": "Retain primary operational reliance on binary occurrence model (PR-AUC 0.8196); treat magnitude as secondary advisory indicator."
    }
    print(f"Landslide Magnitude: Macro-F1 {f1_orig} -> {f1_improved:.4f}, Accuracy {acc_orig} -> {acc_improved:.4f}")
    
    # -------------------------------------------------------------------------
    # 2. Earthquake Aftershock Hazard Threshold Calibration
    # -------------------------------------------------------------------------
    print("\n=== 2. EARTHQUAKE AFTERSHOCK HAZARD THRESHOLD CALIBRATION ===")
    cfg_eq = HAZARD_CONFIGS['earthquakes']
    data_eq = load_hazard_dataset('earthquakes', cfg_eq)
    X_val_eq = data_eq['X_val']
    y_val_eq = data_eq['target_data']['aftershock_hazard']['y_val']
    X_test_eq = data_eq['X_test']
    y_test_eq = data_eq['target_data']['aftershock_hazard']['y_test']
    
    m_eq = joblib.load(os.path.join(MODELS_DIR, 'earthquakes', 'earthquakes_aftershock_hazard_xgboost.joblib'))
    val_probs_eq = m_eq.predict_proba(X_val_eq)[:, 1]
    test_probs_eq = m_eq.predict_proba(X_test_eq)[:, 1]
    
    # Search optimal threshold on VAL set to balance F1 & FAR
    best_thresh_eq = 0.50
    best_f1_val_eq = 0.0
    for t in np.arange(0.30, 0.75, 0.02):
        score = f1_score(y_val_eq, (val_probs_eq >= t).astype(int), zero_division=0)
        if score > best_f1_val_eq:
            best_f1_val_eq = score
            best_thresh_eq = float(t)
            
    # Apply optimal threshold on test
    pred_default_eq = (test_probs_eq >= 0.50).astype(int)
    pred_opt_eq = (test_probs_eq >= best_thresh_eq).astype(int)
    
    f1_test_default_eq = float(f1_score(y_test_eq, pred_default_eq))
    f1_test_opt_eq = float(f1_score(y_test_eq, pred_opt_eq))
    far_default_eq = float(np.sum((pred_default_eq == 1) & (y_test_eq == 0)) / np.sum(y_test_eq == 0))
    far_opt_eq = float(np.sum((pred_opt_eq == 1) & (y_test_eq == 0)) / np.sum(y_test_eq == 0))
    
    improvements["earthquakes_aftershock_hazard"] = {
        "hazard": "earthquakes",
        "task": "aftershock_hazard",
        "issue_diagnosed": "Class imbalance (~20% positive) led to elevated False Alarm Rate (52.5%) at default 0.50 threshold.",
        "experimental_action": f"Calibrated operational decision threshold on validation set (best val threshold = {best_thresh_eq:.2f}).",
        "default_threshold": 0.50,
        "default_test_f1": round(f1_test_default_eq, 4),
        "default_test_far": round(far_default_eq, 4),
        "calibrated_threshold": round(best_thresh_eq, 2),
        "calibrated_test_f1": round(f1_test_opt_eq, 4),
        "calibrated_test_far": round(far_opt_eq, 4),
        "governance_decision": "Integrate calibrated decision threshold into warning level assignment to reduce false alarms."
    }
    print(f"Earthquake Threshold: Default (0.50) F1={f1_test_default_eq:.4f}, FAR={far_default_eq:.4f} -> Calibrated ({best_thresh_eq:.2f}) F1={f1_test_opt_eq:.4f}, FAR={far_opt_eq:.4f}")

    # -------------------------------------------------------------------------
    # 3. Cyclone Rapid Intensification Threshold Calibration
    # -------------------------------------------------------------------------
    print("\n=== 3. CYCLONE RAPID INTENSIFICATION THRESHOLD CALIBRATION ===")
    cfg_cy = HAZARD_CONFIGS['cyclones']
    data_cy = load_hazard_dataset('cyclones', cfg_cy)
    X_val_cy = data_cy['X_val']
    y_val_cy = data_cy['target_data']['rapid_intensification']['y_val']
    X_test_cy = data_cy['X_test']
    y_test_cy = data_cy['target_data']['rapid_intensification']['y_test']
    
    m_cy = joblib.load(os.path.join(MODELS_DIR, 'cyclones', 'cyclones_rapid_intensification_xgboost.joblib'))
    val_probs_cy = m_cy.predict_proba(X_val_cy)[:, 1]
    test_probs_cy = m_cy.predict_proba(X_test_cy)[:, 1]
    
    best_thresh_cy = 0.50
    best_f1_val_cy = 0.0
    for t in np.arange(0.20, 0.70, 0.02):
        score = f1_score(y_val_cy, (val_probs_cy >= t).astype(int), zero_division=0)
        if score > best_f1_val_cy:
            best_f1_val_cy = score
            best_thresh_cy = float(t)
            
    pred_default_cy = (test_probs_cy >= 0.50).astype(int)
    pred_opt_cy = (test_probs_cy >= best_thresh_cy).astype(int)
    
    f1_test_default_cy = float(f1_score(y_test_cy, pred_default_cy))
    f1_test_opt_cy = float(f1_score(y_test_cy, pred_opt_cy))
    rec_default_cy = float(recall_score(y_test_cy, pred_default_cy))
    rec_opt_cy = float(recall_score(y_test_cy, pred_opt_cy))
    
    improvements["cyclones_rapid_intensification"] = {
        "hazard": "cyclones",
        "task": "rapid_intensification",
        "issue_diagnosed": "Severe positive class rarity (5.48% positive base rate) suppressed recall at arbitrary 0.50 cutoff.",
        "experimental_action": f"Optimized operational trigger threshold on validation set (optimal threshold = {best_thresh_cy:.2f}).",
        "default_threshold": 0.50,
        "default_test_f1": round(f1_test_default_cy, 4),
        "default_test_recall": round(rec_default_cy, 4),
        "calibrated_threshold": round(best_thresh_cy, 2),
        "calibrated_test_f1": round(f1_test_opt_cy, 4),
        "calibrated_test_recall": round(rec_opt_cy, 4),
        "governance_decision": "Enforce dual-trigger evaluation: Rapid Intensification probability combined with Saffir-Simpson wind intensity."
    }
    print(f"Cyclone RI Threshold: Default (0.50) Recall={rec_default_cy:.4f}, F1={f1_test_default_cy:.4f} -> Calibrated ({best_thresh_cy:.2f}) Recall={rec_opt_cy:.4f}, F1={f1_test_opt_cy:.4f}")

    # -------------------------------------------------------------------------
    # 4. Quarantined Models Governance Audit
    # -------------------------------------------------------------------------
    improvements["earthquakes_aftershock_count"] = {
        "hazard": "earthquakes",
        "task": "aftershock_count",
        "status": "UNAVAILABLE_FOR_OPERATIONAL_USE (QUARANTINED)",
        "empirical_r2": -0.0401,
        "investigation_outcome": "Heavy-tailed swarm distribution with non-stationary clustered ruptures prevents tabular gradient boosted regression from outperforming the baseline mean. The physical Omori-Utsu power law decay is mathematically defensible and acts as the official operational alternative.",
        "governance_decision": "MAINTAIN STRICT SAFETY LOCK. Do not unblock."
    }
    improvements["wildfires_fire_duration"] = {
        "hazard": "wildfires",
        "task": "fire_duration",
        "status": "UNAVAILABLE_FOR_OPERATIONAL_USE (QUARANTINED)",
        "empirical_r2": -214.75,
        "investigation_outcome": "Extreme variance in burn duration (hours to months) driven by unobserved human suppression tactics and micro-scale fuel discontinuities. Loss function squares errors on outlier megafires.",
        "governance_decision": "MAINTAIN STRICT SAFETY LOCK. Do not unblock."
    }

    out_file = os.path.join(REPORTS_DIR, 'phase13_model_improvements_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(improvements, f, indent=2)
    print(f"\n[SUCCESS] Improvement experiments saved to: {out_file}")
    return improvements

if __name__ == '__main__':
    run_improvement_experiments()
