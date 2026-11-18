"""
HAZARDX AI — Phase 13 Step 2: Comprehensive Model Performance & Baseline Evaluation
Evaluates all 12 XGBoost models on untouched holdout test splits against:
1. Naive baseline models (Dummy classifier / regressor)
2. Simple physical heuristic baselines (Rainfall/wind/FWI thresholds)
Computes full classification & regression metrics, confusion matrices, calibration curves,
and warning usefulness scores (FAR, Missed-Event Rate).
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    brier_score_loss, mean_absolute_error, root_mean_squared_error,
    r2_score, median_absolute_error, explained_variance_score
)
from sklearn.calibration import calibration_curve

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data', 'model_ready')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

from scripts.ml_pipeline.config import HAZARD_CONFIGS
from scripts.ml_pipeline.data_loader import load_hazard_dataset

def evaluate_all_models():
    results = {}
    
    for hazard_key, cfg in HAZARD_CONFIGS.items():
        print(f"\n==========================================")
        print(f"EVALUATING HAZARD: {hazard_key.upper()}")
        print(f"==========================================")
        
        # Load dataset
        data_bundle = load_hazard_dataset(hazard_key, cfg)
        X_test = data_bundle['X_test']
        X_val = data_bundle['X_val']
        X_train = data_bundle['X_train']
        target_data = data_bundle['target_data']
        
        for task_name, task_cfg in cfg['tasks'].items():
            print(f"\n--- Task: {task_name} ({task_cfg['type']}) ---")
            
            # Load model artifact
            model_file = f"{hazard_key}_{task_name}_xgboost.joblib"
            model_path = os.path.join(MODELS_DIR, hazard_key, model_file)
            
            if not os.path.exists(model_path):
                print(f"[WARNING] Model file {model_path} does not exist!")
                continue
                
            model = joblib.load(model_path)
            
            y_test = target_data[task_name]['y_test']
            y_val = target_data[task_name]['y_val']
            y_train = target_data[task_name]['y_train']
            
            task_type = task_cfg['type']
            
            # 1. Predictions
            y_pred = model.predict(X_test)
            y_prob = None
            if hasattr(model, 'predict_proba'):
                y_prob = model.predict_proba(X_test)
                
            # Evaluation Dictionary
            task_result = {
                "hazard": hazard_key,
                "task_name": task_name,
                "task_type": task_type,
                "target_column": task_cfg['target'],
                "test_samples": len(y_test),
                "model_metrics": {},
                "naive_baseline_metrics": {},
                "physical_baseline_metrics": {},
                "calibration": {},
                "warning_usefulness": {}
            }
            
            if task_type == 'binary_classification':
                y_prob_pos = y_prob[:, 1] if y_prob is not None else y_pred
                
                # Model metrics
                tn, fp, fn, tp = confusion_matrix(y_test, y_pred, labels=[0, 1]).ravel()
                precision = precision_score(y_test, y_pred, zero_division=0)
                recall = recall_score(y_test, y_pred, zero_division=0)
                specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
                f1 = f1_score(y_test, y_pred, zero_division=0)
                roc_auc = roc_auc_score(y_test, y_prob_pos)
                pr_auc = average_precision_score(y_test, y_prob_pos)
                brier = brier_score_loss(y_test, y_prob_pos)
                
                far = fp / (fp + tn) if (fp + tn) > 0 else 0.0
                miss_rate = fn / (fn + tp) if (fn + tp) > 0 else 0.0
                
                task_result["model_metrics"] = {
                    "accuracy": float(accuracy_score(y_test, y_pred)),
                    "precision": float(precision),
                    "recall": float(recall),
                    "specificity": float(specificity),
                    "f1": float(f1),
                    "roc_auc": float(roc_auc),
                    "pr_auc": float(pr_auc),
                    "brier_score": float(brier),
                    "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}
                }
                
                task_result["warning_usefulness"] = {
                    "false_alarm_rate": float(far),
                    "missed_event_rate": float(miss_rate),
                    "threat_score_csi": float(tp / (tp + fn + fp)) if (tp + fn + fp) > 0 else 0.0
                }
                
                # Calibration curve (5 bins)
                prob_true, prob_pred = calibration_curve(y_test, y_prob_pos, n_bins=5, strategy='uniform')
                task_result["calibration"] = {
                    "prob_true": [float(p) for p in prob_true],
                    "prob_pred": [float(p) for p in prob_pred]
                }
                
                # Naive Baseline (predict training prior)
                train_prior = float(np.mean(y_train))
                naive_prob = np.full_like(y_test, train_prior, dtype=float)
                naive_pred = (naive_prob >= 0.5).astype(int)
                task_result["naive_baseline_metrics"] = {
                    "brier_score": float(brier_score_loss(y_test, naive_prob)),
                    "roc_auc": 0.5,
                    "pr_auc": float(np.mean(y_test)),
                    "accuracy": float(accuracy_score(y_test, naive_pred)),
                    "f1": float(f1_score(y_test, naive_pred, zero_division=0))
                }
                
                # Physical Heuristic Baseline
                phys_pred = np.zeros_like(y_test)
                phys_desc = "None"
                if hazard_key == 'floods' and 'precip_3d_sum_mm' in X_test.columns:
                    phys_pred = (X_test['precip_3d_sum_mm'] > 50.0).astype(int)
                    phys_desc = "3-day cumulative rainfall > 50mm"
                elif hazard_key == 'landslides' and 'precip_3d_sum_mm' in X_test.columns:
                    phys_pred = (X_test['precip_3d_sum_mm'] > 50.0).astype(int)
                    phys_desc = "3-day cumulative rainfall > 50mm"
                elif hazard_key == 'wildfires' and 'fwi_fire_weather_index' in X_test.columns:
                    phys_pred = (X_test['fwi_fire_weather_index'] > 20.0).astype(int)
                    phys_desc = "Fire Weather Index (FWI) > 20"
                elif hazard_key == 'cyclones' and 'past_delta_wind_6h' in X_test.columns:
                    phys_pred = (X_test['past_delta_wind_6h'] >= 10.0).astype(int)
                    phys_desc = "Past 6h wind increase >= 10kt"
                elif hazard_key == 'earthquakes' and 'prior_count_30d_100km' in X_test.columns:
                    phys_pred = (X_test['prior_count_30d_100km'] >= 5).astype(int)
                    phys_desc = "Prior 30-day seismic count >= 5 events"
                    
                p_tn, p_fp, p_fn, p_tp = confusion_matrix(y_test, phys_pred, labels=[0, 1]).ravel()
                task_result["physical_baseline_metrics"] = {
                    "rule_description": phys_desc,
                    "accuracy": float(accuracy_score(y_test, phys_pred)),
                    "precision": float(precision_score(y_test, phys_pred, zero_division=0)),
                    "recall": float(recall_score(y_test, phys_pred, zero_division=0)),
                    "f1": float(f1_score(y_test, phys_pred, zero_division=0)),
                    "confusion_matrix": {"tn": int(p_tn), "fp": int(p_fp), "fn": int(p_fn), "tp": int(p_tp)}
                }
                
                print(f"  Model Test PR-AUC: {pr_auc:.4f} (Naive: {task_result['naive_baseline_metrics']['pr_auc']:.4f})")
                print(f"  Model Test F1: {f1:.4f} (Physical Rule: {task_result['physical_baseline_metrics']['f1']:.4f})")
                print(f"  FAR: {far:.4f}, Miss Rate: {miss_rate:.4f}, Brier: {brier:.4f}")
                
            elif task_type == 'multiclass_classification':
                cm = confusion_matrix(y_test, y_pred, labels=list(range(task_cfg['num_class'])))
                f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)
                acc = accuracy_score(y_test, y_pred)
                
                roc_auc = 0.5
                if y_prob is not None:
                    try:
                        roc_auc = roc_auc_score(y_test, y_prob, multi_class='ovr', average='macro')
                    except Exception:
                        pass
                        
                task_result["model_metrics"] = {
                    "accuracy": float(acc),
                    "f1_macro": float(f1_macro),
                    "f1_weighted": float(f1_score(y_test, y_pred, average='weighted', zero_division=0)),
                    "roc_auc": float(roc_auc),
                    "confusion_matrix": cm.tolist()
                }
                
                # Naive Baseline (predict majority class from train)
                majority_class = int(y_train.mode()[0])
                naive_pred = np.full_like(y_test, majority_class)
                task_result["naive_baseline_metrics"] = {
                    "accuracy": float(accuracy_score(y_test, naive_pred)),
                    "f1_macro": float(f1_score(y_test, naive_pred, average='macro', zero_division=0)),
                    "strategy": f"Majority class ({majority_class})"
                }
                print(f"  Multiclass Test Macro-F1: {f1_macro:.4f} (Naive Majority: {task_result['naive_baseline_metrics']['f1_macro']:.4f})")
                print(f"  Accuracy: {acc:.4f} (Naive Majority: {task_result['naive_baseline_metrics']['accuracy']:.4f})")
                
            else: # regression
                mae = mean_absolute_error(y_test, y_pred)
                rmse = root_mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                med_ae = median_absolute_error(y_test, y_pred)
                ev = explained_variance_score(y_test, y_pred)
                
                # Naive Baseline (Predict training mean)
                train_mean = float(y_train.mean())
                naive_pred = np.full_like(y_test, train_mean)
                naive_mae = mean_absolute_error(y_test, naive_pred)
                naive_rmse = root_mean_squared_error(y_test, naive_pred)
                naive_r2 = r2_score(y_test, naive_pred)
                
                task_result["model_metrics"] = {
                    "mae": float(mae),
                    "rmse": float(rmse),
                    "r2": float(r2),
                    "median_absolute_error": float(med_ae),
                    "explained_variance": float(ev)
                }
                task_result["naive_baseline_metrics"] = {
                    "mae": float(naive_mae),
                    "rmse": float(naive_rmse),
                    "r2": float(naive_r2),
                    "strategy": f"Predict training mean ({train_mean:.2f})"
                }
                
                # Residual analysis
                residuals = y_test - y_pred
                task_result["residual_analysis"] = {
                    "mean_residual": float(np.mean(residuals)),
                    "std_residual": float(np.std(residuals)),
                    "min_residual": float(np.min(residuals)),
                    "max_residual": float(np.max(residuals))
                }
                print(f"  Regression Test R2: {r2:.4f} (Naive Mean R2: {naive_r2:.4f})")
                print(f"  RMSE: {rmse:.4f} (Naive: {naive_rmse:.4f}), MAE: {mae:.4f} (Naive: {naive_mae:.4f})")
                
            results[f"{hazard_key}_{task_name}"] = task_result

    # Save to disk
    out_path = os.path.join(REPORTS_DIR, 'phase13_model_evaluation_results.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"\n[SUCCESS] Model evaluation results saved to: {out_path}")
    return results

if __name__ == '__main__':
    evaluate_all_models()
