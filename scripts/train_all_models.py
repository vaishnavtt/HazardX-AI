"""
HAZARDX AI — Master Machine Learning Pipeline Entry Point
Executes training, optimization, evaluation, explainability, and artifact persistence
across all five natural hazard prediction modules, compiling dashboard comparison records.
"""

import os
import sys
import json
import argparse
import pandas as pd

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.ml_pipeline.config import MODELS_DIR, REPORTS_DIR
from scripts.ml_pipeline.trainer import run_hazard_training_pipeline, json_serializer

def compile_dashboard_artifacts(all_results):
    """
    Compiles structured JSON and CSV datasets for the HAZARDX AI Dashboard.
    """
    dashboard_records = []
    
    for r in all_results:
        # Extract top features as readable string
        top_feats = [f['feature'] for f in r.get('top_features_shap', [])]
        
        # Primary test metric
        if r['task_type'] == 'binary_classification':
            primary_score = r['test_metrics']['pr_auc']
            metric_label = 'PR-AUC'
            secondary_score = r['test_metrics']['roc_auc']
            secondary_label = 'ROC-AUC'
        elif r['task_type'] == 'multiclass_classification':
            primary_score = r['test_metrics']['f1_macro']
            metric_label = 'Macro-F1'
            secondary_score = r['test_metrics']['accuracy']
            secondary_label = 'Accuracy'
        else:
            primary_score = r['test_metrics']['rmse']
            metric_label = 'RMSE'
            secondary_score = r['test_metrics']['r2']
            secondary_label = 'R2'
            
        rec = {
            'hazard': r['hazard_name'],
            'prediction_target': r['task_name'],
            'target_column': r['target_column'],
            'task_type': r['task_type'],
            'algorithm': 'XGBoost',
            'train_sample_count': r['train_samples'],
            'val_sample_count': r['val_samples'],
            'test_sample_count': r['test_samples'],
            'primary_metric_name': metric_label,
            'primary_test_score': round(primary_score, 4),
            'secondary_metric_name': secondary_label,
            'secondary_test_score': round(secondary_score, 4),
            'top_important_features': ", ".join(top_feats),
            'best_hyperparameters': json.dumps(r['best_hyperparameters'], default=json_serializer),
            'model_version': r['version'],
            'training_timestamp': r['training_timestamp'],
            'joblib_path': r['artifact_joblib'],
            'eval_plot_path': r['eval_plot'],
            'shap_plot_path': r['shap_summary_plot']
        }
        dashboard_records.append(rec)
        
    df_dash = pd.DataFrame(dashboard_records)
    
    # Save in models/ and reports/model_evaluation/
    dash_json_p1 = os.path.join(MODELS_DIR, 'model_comparison_dashboard.json')
    dash_csv_p1 = os.path.join(MODELS_DIR, 'model_comparison_dashboard.csv')
    dash_json_p2 = os.path.join(REPORTS_DIR, 'model_comparison_dashboard.json')
    dash_csv_p2 = os.path.join(REPORTS_DIR, 'model_comparison_dashboard.csv')
    
    with open(dash_json_p1, 'w', encoding='utf-8') as f:
        json.dump(dashboard_records, f, indent=2, default=json_serializer)
    with open(dash_json_p2, 'w', encoding='utf-8') as f:
        json.dump(dashboard_records, f, indent=2, default=json_serializer)
        
    df_dash.to_csv(dash_csv_p1, index=False)
    df_dash.to_csv(dash_csv_p2, index=False)
    
    print(f"\n[DASHBOARD] Compiled dashboard metrics saved to:")
    print(f"  - {dash_json_p1}")
    print(f"  - {dash_csv_p1}")

def main():
    parser = argparse.ArgumentParser(description="HAZARDX AI Master ML Model Training Pipeline")
    parser.add_argument("--hazard", type=str, default=None, choices=['floods', 'landslides', 'earthquakes', 'cyclones', 'wildfires'],
                        help="Filter execution to a specific hazard module (default: all)")
    parser.add_argument("--n_jobs", type=int, default=4, help="Number of CPU cores for XGBoost training")
    args = parser.parse_args()
    
    results = run_hazard_training_pipeline(hazard_filter=args.hazard, n_jobs=args.n_jobs)
    compile_dashboard_artifacts(results)
    print("\n[SUCCESS] Master model training pipeline executed completely.")

if __name__ == '__main__':
    main()
