"""
HAZARDX AI — Model Explainability Suite with TreeSHAP
Generates global beeswarm summary plots, bar plots, feature importance rankings,
and individual waterfall prediction explanations for representative test instances.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap

def explain_model_with_shap(model, X_train, X_test, y_test, hazard_name, task_name, task_type, shap_dir):
    """
    Computes TreeSHAP values and outputs comprehensive explainability plots.
    """
    os.makedirs(shap_dir, exist_ok=True)
    slug = f"{hazard_name.lower()}_{task_name}"
    
    # Subsample test set for TreeExplainer if N > 1000 for lightning speed and stability
    if len(X_test) > 1000:
        np.random.seed(42)
        sample_idx = np.random.choice(len(X_test), size=1000, replace=False)
        X_sample = X_test.iloc[sample_idx].copy()
        y_sample = y_test.iloc[sample_idx].copy() if y_test is not None else None
    else:
        X_sample = X_test.copy()
        y_sample = y_test.copy() if y_test is not None else None
        
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer(X_sample)
        
        # Handle multiclass or single-output
        # For multiclass, shap_values.values has shape (N, features, num_classes)
        # Select class 1 or largest active class for visualization
        is_multi = len(shap_values.values.shape) == 3
        if is_multi:
            # Focus on active hazard severity (e.g. class 1)
            vals_for_plot = shap_values[:, :, 1]
            raw_shap = explainer.shap_values(X_sample)
            if isinstance(raw_shap, list) and len(raw_shap) > 1:
                plot_raw = raw_shap[1]
            else:
                plot_raw = raw_shap[:, :, 1] if len(raw_shap.shape) == 3 else raw_shap
        else:
            vals_for_plot = shap_values
            plot_raw = explainer.shap_values(X_sample)
            
        # 1. SHAP Beeswarm Summary Plot
        plt.figure(figsize=(10, 6))
        shap.summary_plot(plot_raw, X_sample, show=False)
        plt.title(f'{hazard_name} ({task_name}) — SHAP Summary (Beeswarm)', fontsize=12, fontweight='bold', pad=15)
        plt.tight_layout()
        p_summary = os.path.join(shap_dir, f"{slug}_shap_summary.png")
        plt.savefig(p_summary, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. SHAP Bar Plot (Global Mean Absolute SHAP Importance)
        plt.figure(figsize=(10, 6))
        shap.summary_plot(plot_raw, X_sample, plot_type='bar', show=False, color='#2980b9')
        plt.title(f'{hazard_name} ({task_name}) — Mean Absolute SHAP Importance', fontsize=12, fontweight='bold', pad=15)
        plt.tight_layout()
        p_bar = os.path.join(shap_dir, f"{slug}_shap_bar.png")
        plt.savefig(p_bar, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. XGBoost Native Feature Importance (Gain)
        plt.figure(figsize=(10, 6))
        importances = model.feature_importances_
        feature_names = X_test.columns.tolist()
        sorted_idx = np.argsort(importances)[::-1]
        
        plt.barh(np.arange(len(feature_names)), importances[sorted_idx][::-1], color='#e67e22')
        plt.yticks(np.arange(len(feature_names)), [feature_names[i] for i in sorted_idx][::-1], fontweight='bold')
        plt.xlabel('XGBoost Relative Gain Importance', fontweight='bold')
        plt.title(f'{hazard_name} ({task_name}) — Native Feature Gain Importance', fontsize=12, fontweight='bold')
        plt.grid(axis='x', linestyle='--', alpha=0.4)
        plt.tight_layout()
        p_gain = os.path.join(shap_dir, f"{slug}_native_importance.png")
        plt.savefig(p_gain, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Individual Case Waterfall Explanations (High Hazard vs Low Hazard)
        p_waterfall = None
        try:
            plt.figure(figsize=(10, 6))
            # Pick a sample with high predicted probability/value
            if task_type == 'binary_classification':
                preds = model.predict_proba(X_sample)[:, 1]
                rep_idx = int(np.argmax(preds))
            elif task_type == 'regression':
                preds = model.predict(X_sample)
                rep_idx = int(np.argmax(preds))
            else:
                rep_idx = 0
                
            shap.plots.waterfall(vals_for_plot[rep_idx], show=False)
            plt.title(f'{hazard_name} ({task_name}) — Representative Case Explanation', fontsize=12, fontweight='bold', pad=15)
            plt.tight_layout()
            p_waterfall = os.path.join(shap_dir, f"{slug}_case_waterfall.png")
            plt.savefig(p_waterfall, dpi=300, bbox_inches='tight')
            plt.close()
        except Exception as e:
            # Fallback if waterfall plot layout triggers formatting issue
            print(f"  [Notice] Waterfall plot skipped for {slug}: {e}")
            plt.close()
            
        # Top 5 influential features from SHAP
        if hasattr(plot_raw, 'shape'):
            mean_abs_shap = np.mean(np.abs(plot_raw), axis=0)
            top5_indices = np.argsort(mean_abs_shap)[::-1][:5]
            top_features = [
                {'feature': feature_names[i], 'mean_abs_shap': float(mean_abs_shap[i])}
                for i in top5_indices
            ]
        else:
            top_features = []
            
        return {
            'summary_plot': p_summary,
            'bar_plot': p_bar,
            'gain_plot': p_gain,
            'waterfall_plot': p_waterfall,
            'top_features': top_features
        }
        
    except Exception as e:
        print(f"  [Warning] SHAP explanation failed for {slug}: {e}")
        return {
            'summary_plot': None,
            'bar_plot': None,
            'gain_plot': None,
            'waterfall_plot': None,
            'top_features': []
        }

