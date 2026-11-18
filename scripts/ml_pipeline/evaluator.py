"""
HAZARDX AI — Comprehensive Model Evaluator & Curve Generator
Calculates rigorous classification and regression metrics, confusion matrices,
ROC/PR curves, and regression residual diagnostics.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    brier_score_loss, mean_absolute_error, root_mean_squared_error,
    r2_score, median_absolute_error, explained_variance_score,
    roc_curve, precision_recall_curve
)

def evaluate_classification(y_true, y_pred, y_prob=None, is_multiclass=False, num_classes=2):
    """
    Computes complete classification metrics suite.
    """
    metrics = {
        'accuracy': float(accuracy_score(y_true, y_pred)),
    }
    
    if not is_multiclass:
        # Binary classification
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
        specificity = float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0
        sensitivity = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        
        metrics.update({
            'precision': float(precision_score(y_true, y_pred, zero_division=0)),
            'recall': float(recall_score(y_true, y_pred, zero_division=0)),
            'sensitivity': sensitivity,
            'specificity': specificity,
            'f1': float(f1_score(y_true, y_pred, zero_division=0)),
            'f1_macro': float(f1_score(y_true, y_pred, average='macro', zero_division=0)),
            'tn': int(tn),
            'fp': int(fp),
            'fn': int(fn),
            'tp': int(tp)
        })
        
        if y_prob is not None:
            # y_prob is probability of class 1
            try:
                metrics['roc_auc'] = float(roc_auc_score(y_true, y_prob))
            except Exception:
                metrics['roc_auc'] = 0.5
            try:
                metrics['pr_auc'] = float(average_precision_score(y_true, y_prob))
            except Exception:
                metrics['pr_auc'] = float(np.mean(y_true))
            try:
                metrics['brier_score'] = float(brier_score_loss(y_true, y_prob))
            except Exception:
                metrics['brier_score'] = 1.0
    else:
        # Multiclass classification
        cm = confusion_matrix(y_true, y_pred, labels=list(range(num_classes)))
        metrics.update({
            'f1_macro': float(f1_score(y_true, y_pred, average='macro', zero_division=0)),
            'f1_weighted': float(f1_score(y_true, y_pred, average='weighted', zero_division=0)),
            'precision_macro': float(precision_score(y_true, y_pred, average='macro', zero_division=0)),
            'recall_macro': float(recall_score(y_true, y_pred, average='macro', zero_division=0)),
            'confusion_matrix': cm.tolist()
        })
        if y_prob is not None:
            try:
                # OVO or OVR ROC AUC
                metrics['roc_auc'] = float(roc_auc_score(y_true, y_prob, multi_class='ovr', average='macro'))
            except Exception:
                metrics['roc_auc'] = 0.5
                
    return metrics

def evaluate_regression(y_true, y_pred):
    """
    Computes complete regression metrics suite.
    """
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(root_mean_squared_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    med_ae = float(median_absolute_error(y_true, y_pred))
    ev = float(explained_variance_score(y_true, y_pred))
    
    return {
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'median_absolute_error': med_ae,
        'explained_variance': ev
    }

def generate_evaluation_plots(hazard_name, task_name, task_type, y_test, y_pred, y_prob, figures_dir):
    """
    Generates ROC curves, PR curves, Confusion Matrix heatmaps, or Regression Diagnostics.
    """
    os.makedirs(figures_dir, exist_ok=True)
    slug = f"{hazard_name.lower()}_{task_name}"
    
    if task_type == 'binary_classification' and y_prob is not None:
        fig, axs = plt.subplots(1, 3, figsize=(18, 5))
        
        # 1. ROC Curve
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        auc_val = roc_auc_score(y_test, y_prob) if len(np.unique(y_test)) > 1 else 0.5
        axs[0].plot(fpr, tpr, color='#2980b9', lw=2.5, label=f'XGBoost (AUC = {auc_val:.3f})')
        axs[0].plot([0, 1], [0, 1], color='#7f8c8d', linestyle='--', label='Random Chance')
        axs[0].set_title(f'{hazard_name} ({task_name}) — ROC Curve', fontweight='bold')
        axs[0].set_xlabel('False Positive Rate (1 - Specificity)')
        axs[0].set_ylabel('True Positive Rate (Sensitivity / Recall)')
        axs[0].legend(loc='lower right', frameon=True)
        axs[0].grid(True, linestyle='--', alpha=0.4)
        
        # 2. Precision-Recall Curve
        prec, rec, _ = precision_recall_curve(y_test, y_prob)
        pr_auc_val = average_precision_score(y_test, y_prob) if len(np.unique(y_test)) > 1 else float(np.mean(y_test))
        base_rate = float(np.mean(y_test))
        axs[1].plot(rec, prec, color='#e74c3c', lw=2.5, label=f'XGBoost (PR-AUC = {pr_auc_val:.3f})')
        axs[1].axhline(base_rate, color='#7f8c8d', linestyle='--', label=f'Baseline Rate ({base_rate:.3f})')
        axs[1].set_title(f'{hazard_name} ({task_name}) — Precision-Recall Curve', fontweight='bold')
        axs[1].set_xlabel('Recall (Sensitivity)')
        axs[1].set_ylabel('Precision (PPV)')
        axs[1].legend(loc='upper right', frameon=True)
        axs[1].grid(True, linestyle='--', alpha=0.4)
        
        # 3. Confusion Matrix Heatmap
        cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axs[2], cbar=False,
                    xticklabels=['Predicted 0', 'Predicted 1'],
                    yticklabels=['Actual 0', 'Actual 1'])
        axs[2].set_title(f'Test Confusion Matrix (N = {len(y_test)})', fontweight='bold')
        
        plt.tight_layout()
        out_path = os.path.join(figures_dir, f"{slug}_eval_plots.png")
        plt.savefig(out_path, dpi=300)
        plt.close()
        return out_path
        
    elif task_type == 'multiclass_classification':
        fig, ax = plt.subplots(figsize=(6, 5))
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Purples', ax=ax, cbar=False)
        ax.set_title(f'{hazard_name} ({task_name}) — Multiclass Confusion Matrix', fontweight='bold')
        ax.set_xlabel('Predicted Class')
        ax.set_ylabel('Actual Class')
        plt.tight_layout()
        out_path = os.path.join(figures_dir, f"{slug}_confusion_matrix.png")
        plt.savefig(out_path, dpi=300)
        plt.close()
        return out_path
        
    elif task_type == 'regression':
        fig, axs = plt.subplots(1, 2, figsize=(14, 5))
        
        # 1. Actual vs Predicted Scatter
        axs[0].scatter(y_test, y_pred, alpha=0.5, color='#16a085', edgecolor='none')
        min_v = min(np.min(y_test), np.min(y_pred))
        max_v = max(np.max(y_test), np.max(y_pred))
        axs[0].plot([min_v, max_v], [min_v, max_v], color='#e74c3c', linestyle='--', label='1:1 Perfect Prediction')
        axs[0].set_title(f'{hazard_name} ({task_name}) — Actual vs Predicted', fontweight='bold')
        axs[0].set_xlabel('Actual Value')
        axs[0].set_ylabel('Predicted Value')
        axs[0].legend()
        axs[0].grid(True, linestyle='--', alpha=0.4)
        
        # 2. Residual Distribution
        residuals = y_test - y_pred
        sns.histplot(residuals, kde=True, ax=axs[1], color='#8e44ad', bins=30)
        axs[1].axvline(0, color='red', linestyle='--')
        axs[1].set_title(f'Residuals (Actual - Predicted) | Mean: {np.mean(residuals):.2f}', fontweight='bold')
        axs[1].set_xlabel('Residual Error')
        
        plt.tight_layout()
        out_path = os.path.join(figures_dir, f"{slug}_regression_diagnostic.png")
        plt.savefig(out_path, dpi=300)
        plt.close()
        return out_path
        
    return None

