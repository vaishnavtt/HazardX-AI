"""
HAZARDX AI — Master ML Training Orchestrator
Executes training, validation tuning, test evaluation, explainability, and artifact persistence
for all five natural hazard prediction modules.
"""

import os
import time
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

from .config import HAZARD_CONFIGS, SHAP_DIR, FIGURES_DIR, RANDOM_STATE
from .data_loader import load_hazard_dataset
from .models import train_and_tune_model
from .evaluator import evaluate_classification, evaluate_regression, generate_evaluation_plots
from .explainability import explain_model_with_shap

def json_serializer(obj):
    """Encodes numpy data types and non-standard objects to JSON-serializable primitives."""
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return str(obj)

def run_hazard_training_pipeline(hazard_filter=None, n_jobs=4):
    """
    Executes end-to-end model training, validation optimization, test evaluation,
    SHAP explainability, and artifact serialization across all hazards.
    """
    start_total_time = time.time()
    all_task_results = []
    
    print("\n" + "="*80)
    print("HAZARDX AI — MASTER XGBOOST MACHINE LEARNING PIPELINE")
    print("="*80)
    
    for h_key, h_cfg in HAZARD_CONFIGS.items():
        if hazard_filter and h_key != hazard_filter:
            continue
            
        print(f"\n>>> PROCESSING HAZARD MODULE: {h_cfg['name'].upper()} <<<")
        print(f"Dataset path: {h_cfg['dataset_path']}")
        
        # 1. Load dataset & partitions
        data_bundle = load_hazard_dataset(h_key, h_cfg)
        X_train = data_bundle['X_train']
        X_val = data_bundle['X_val']
        X_test = data_bundle['X_test']
        features = data_bundle['features']
        
        print(f"Features ({len(features)}): {features}")
        print(f"Partition shapes: Train {X_train.shape}, Val {X_val.shape}, Test {X_test.shape}")
        
        # 2. Iterate through prediction tasks
        for task_name, task_cfg in h_cfg['tasks'].items():
            task_type = task_cfg['type']
            print(f"\n--- Training Task: {task_name.upper()} ({task_type}) ---")
            print(f"Target: {task_cfg['target']} | Description: {task_cfg['description']}")
            
            y_train = data_bundle['target_data'][task_name]['y_train']
            y_val = data_bundle['target_data'][task_name]['y_val']
            y_test = data_bundle['target_data'][task_name]['y_test']
            
            t_start = time.time()
            
            # 3. Train Baseline, Initial XGBoost, and Tune on Validation
            tune_results = train_and_tune_model(
                task_name, task_cfg, X_train, y_train, X_val, y_val,
                random_state=RANDOM_STATE, n_jobs=n_jobs
            )
            
            best_model = tune_results['best_model']
            best_params = tune_results['best_params']
            baseline_model = tune_results['baseline_model']
            initial_model = tune_results['initial_model']
            
            # 4. Evaluate Once on the Untouched Test Set
            if task_type in ['binary_classification', 'multiclass_classification']:
                # Baseline Test
                base_test_pred = baseline_model.predict(X_test)
                base_test_prob = baseline_model.predict_proba(X_test)
                if task_type == 'binary_classification':
                    base_test_metrics = evaluate_classification(y_test, base_test_pred, base_test_prob[:, 1])
                else:
                    base_test_metrics = evaluate_classification(y_test, base_test_pred, base_test_prob, is_multiclass=True, num_classes=task_cfg.get('num_class'))
                    
                # Initial XGBoost Test
                init_test_pred = initial_model.predict(X_test)
                init_test_prob = initial_model.predict_proba(X_test)
                if task_type == 'binary_classification':
                    init_test_metrics = evaluate_classification(y_test, init_test_pred, init_test_prob[:, 1])
                else:
                    init_test_metrics = evaluate_classification(y_test, init_test_pred, init_test_prob, is_multiclass=True, num_classes=task_cfg.get('num_class'))
                    
                # Best Tuned XGBoost Test
                test_pred = best_model.predict(X_test)
                test_prob = best_model.predict_proba(X_test)
                if task_type == 'binary_classification':
                    test_prob_primary = test_prob[:, 1]
                    test_metrics = evaluate_classification(y_test, test_pred, test_prob_primary)
                else:
                    test_prob_primary = test_prob
                    test_metrics = evaluate_classification(y_test, test_pred, test_prob, is_multiclass=True, num_classes=task_cfg.get('num_class'))
            else:
                # Regression Test
                base_test_pred = baseline_model.predict(X_test)
                base_test_metrics = evaluate_regression(y_test, base_test_pred)
                
                init_test_pred = initial_model.predict(X_test)
                init_test_metrics = evaluate_regression(y_test, init_test_pred)
                
                test_pred = best_model.predict(X_test)
                test_prob_primary = None
                test_metrics = evaluate_regression(y_test, test_pred)
                
            elapsed = time.time() - t_start
            print(f"Task completed in {elapsed:.2f}s.")
            print(f"Validation Metric ({task_cfg.get('metric_primary', 'score')}): {tune_results['best_val_metrics'].get(task_cfg.get('metric_primary', 'score')):.4f}")
            if task_type == 'binary_classification':
                print(f"Test PR-AUC: {test_metrics['pr_auc']:.4f} | ROC-AUC: {test_metrics['roc_auc']:.4f} | F1: {test_metrics['f1']:.4f} | Acc: {test_metrics['accuracy']:.4f}")
            elif task_type == 'multiclass_classification':
                print(f"Test Macro-F1: {test_metrics['f1_macro']:.4f} | Weighted-F1: {test_metrics['f1_weighted']:.4f} | Acc: {test_metrics['accuracy']:.4f}")
            else:
                print(f"Test RMSE: {test_metrics['rmse']:.4f} | MAE: {test_metrics['mae']:.4f} | R2: {test_metrics['r2']:.4f}")
                
            # 5. Generate Evaluation Plots
            eval_plot_path = generate_evaluation_plots(
                h_cfg['name'], task_name, task_type, y_test, test_pred, test_prob_primary, FIGURES_DIR
            )
            
            # 6. Generate SHAP Explanations
            print("Computing SHAP explanations...")
            shap_results = explain_model_with_shap(
                best_model, X_train, X_test, y_test, h_cfg['name'], task_name, task_type, SHAP_DIR
            )
            
            # 7. Serialize Models & Metadata
            model_slug = f"{h_key}_{task_name}_xgboost"
            joblib_path = os.path.join(h_cfg['model_dir'], f"{model_slug}.joblib")
            json_path = os.path.join(h_cfg['model_dir'], f"{model_slug}.json")
            meta_path = os.path.join(h_cfg['model_dir'], f"{model_slug}_metadata.json")
            
            joblib.dump(best_model, joblib_path)
            try:
                best_model.save_model(json_path)
            except Exception as e:
                print(f"  [Notice] Native JSON model save skipped: {e}")
                
            task_metadata = {
                'hazard': h_key,
                'hazard_name': h_cfg['name'],
                'task_name': task_name,
                'task_type': task_type,
                'target_column': task_cfg['target'],
                'description': task_cfg['description'],
                'features': features,
                'feature_count': len(features),
                'train_samples': len(X_train),
                'val_samples': len(X_val),
                'test_samples': len(X_test),
                'best_hyperparameters': best_params,
                'validation_metrics': tune_results['best_val_metrics'],
                'initial_validation_metrics': tune_results['initial_val_metrics'],
                'baseline_validation_metrics': tune_results['baseline_val_metrics'],
                'unweighted_validation_metrics': tune_results['unweighted_val_metrics'],
                'test_metrics': test_metrics,
                'initial_test_metrics': init_test_metrics,
                'baseline_test_metrics': base_test_metrics,
                'top_features_shap': shap_results['top_features'],
                'artifact_joblib': os.path.abspath(joblib_path),
                'artifact_json': os.path.abspath(json_path) if os.path.exists(json_path) else None,
                'eval_plot': os.path.abspath(eval_plot_path) if eval_plot_path else None,
                'shap_summary_plot': os.path.abspath(shap_results['summary_plot']) if shap_results['summary_plot'] else None,
                'shap_bar_plot': os.path.abspath(shap_results['bar_plot']) if shap_results['bar_plot'] else None,
                'version': '1.0.0',
                'training_timestamp': datetime.utcnow().isoformat()
            }
            
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(task_metadata, f, indent=2, default=json_serializer)
                
            all_task_results.append(task_metadata)
            print(f"Artifacts saved to {h_cfg['model_dir']}")

    total_pipeline_time = time.time() - start_total_time
    print("\n" + "="*80)
    print(f"ALL {len(all_task_results)} HAZARD MODELS SUCCESSFULLY TRAINED IN {total_pipeline_time:.2f}s")
    print("="*80)
    
    return all_task_results
