"""
HAZARDX AI — Model Factory & Hyperparameter Optimization Engine
Constructs baselines, initial XGBoost models, and executes validation-based hyperparameter tuning.
"""

import numpy as np
import xgboost as xgb
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from .evaluator import evaluate_classification, evaluate_regression

def build_baseline_model(task_type, random_state=42):
    """
    Builds appropriate non-trivial baseline model for each task type.
    """
    if task_type == 'binary_classification':
        # Prioritize stratified/frequency dummy as naive reference
        return DummyClassifier(strategy='prior', random_state=random_state)
    elif task_type == 'multiclass_classification':
        return DummyClassifier(strategy='prior', random_state=random_state)
    elif task_type == 'regression':
        return DummyRegressor(strategy='mean')
    else:
        raise ValueError(f"Unknown task type: {task_type}")

def train_and_tune_model(task_name, task_cfg, X_train, y_train, X_val, y_val, random_state=42, n_jobs=4):
    """
    Trains baseline, initial XGBoost, and performs validation-based hyperparameter optimization.
    """
    task_type = task_cfg['type']
    pos_weight = task_cfg.get('pos_weight', 1.0)
    num_class = task_cfg.get('num_class', None)
    
    # -------------------------------------------------------------
    # 1. Train and evaluate Baseline Model
    # -------------------------------------------------------------
    baseline = build_baseline_model(task_type, random_state=random_state)
    baseline.fit(X_train, y_train)
    
    if task_type in ['binary_classification', 'multiclass_classification']:
        base_val_pred = baseline.predict(X_val)
        base_val_prob = baseline.predict_proba(X_val)
        if task_type == 'binary_classification':
            base_val_metrics = evaluate_classification(y_val, base_val_pred, base_val_prob[:, 1])
        else:
            base_val_metrics = evaluate_classification(y_val, base_val_pred, base_val_prob, is_multiclass=True, num_classes=num_class)
    else:
        base_val_pred = baseline.predict(X_val)
        base_val_metrics = evaluate_regression(y_val, base_val_pred)

    # -------------------------------------------------------------
    # 2. Train Initial XGBoost Model (Default baseline configuration)
    # -------------------------------------------------------------
    if task_type == 'binary_classification':
        init_xgb = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            scale_pos_weight=pos_weight,
            random_state=random_state,
            n_jobs=n_jobs,
            eval_metric='logloss'
        )
    elif task_type == 'multiclass_classification':
        init_xgb = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            objective='multi:softprob',
            num_class=num_class,
            random_state=random_state,
            n_jobs=n_jobs,
            eval_metric='mlogloss'
        )
    else: # regression
        init_xgb = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=random_state,
            n_jobs=n_jobs,
            eval_metric='rmse'
        )
        
    init_xgb.fit(X_train, y_train)
    
    if task_type == 'binary_classification':
        init_val_pred = init_xgb.predict(X_val)
        init_val_prob = init_xgb.predict_proba(X_val)[:, 1]
        init_val_metrics = evaluate_classification(y_val, init_val_pred, init_val_prob)
    elif task_type == 'multiclass_classification':
        init_val_pred = init_xgb.predict(X_val)
        init_val_prob = init_xgb.predict_proba(X_val)
        init_val_metrics = evaluate_classification(y_val, init_val_pred, init_val_prob, is_multiclass=True, num_classes=num_class)
    else:
        init_val_pred = init_xgb.predict(X_val)
        init_val_metrics = evaluate_regression(y_val, init_val_pred)

    # -------------------------------------------------------------
    # 3. Class Imbalance Investigation (for Earthquakes & Cyclones)
    # -------------------------------------------------------------
    unweighted_comparison = None
    if task_name in ['aftershock_hazard', 'rapid_intensification']:
        unweighted_xgb = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            scale_pos_weight=1.0, # Unweighted reference
            random_state=random_state,
            n_jobs=n_jobs,
            eval_metric='logloss'
        )
        unweighted_xgb.fit(X_train, y_train)
        unw_val_pred = unweighted_xgb.predict(X_val)
        unw_val_prob = unweighted_xgb.predict_proba(X_val)[:, 1]
        unweighted_comparison = evaluate_classification(y_val, unw_val_pred, unw_val_prob)

    # -------------------------------------------------------------
    # 4. Hyperparameter Search Space
    # -------------------------------------------------------------
    # Sizing search appropriately based on dataset scale
    is_large = len(X_train) > 50000
    n_iter = 6 if is_large else 14
    
    param_grid = {
        'n_estimators': [100, 150, 200, 250, 300] if not is_large else [150, 250],
        'max_depth': [3, 4, 5, 6, 7] if not is_large else [4, 6],
        'learning_rate': [0.02, 0.05, 0.08, 0.1, 0.15] if not is_large else [0.05, 0.1],
        'subsample': [0.7, 0.8, 0.9, 1.0],
        'colsample_bytree': [0.7, 0.8, 0.9, 1.0],
        'min_child_weight': [1, 3, 5, 7],
        'reg_lambda': [0.1, 1.0, 5.0, 10.0],
        'gamma': [0.0, 0.1, 0.2, 0.5]
    }
    
    if task_name == 'aftershock_hazard':
        param_grid['scale_pos_weight'] = [1.0, 3.0, 4.05, 5.5]
    elif task_name == 'rapid_intensification':
        param_grid['scale_pos_weight'] = [1.0, 10.0, 17.25, 22.0]
    else:
        param_grid['scale_pos_weight'] = [pos_weight]
        
    rng = np.random.RandomState(random_state)
    best_score = -float('inf')
    best_params = None
    best_model = init_xgb
    best_val_metrics = init_val_metrics
    search_records = []
    
    primary_metric = task_cfg.get('metric_primary', 'pr_auc')
    
    for i in range(n_iter):
        candidate_params = {
            k: rng.choice(v) for k, v in param_grid.items()
        }
        
        try:
            if task_type == 'binary_classification':
                model = xgb.XGBClassifier(
                    **candidate_params,
                    random_state=random_state,
                    n_jobs=n_jobs,
                    eval_metric='logloss'
                )
                model.fit(X_train, y_train)
                val_pred = model.predict(X_val)
                val_prob = model.predict_proba(X_val)[:, 1]
                val_metrics = evaluate_classification(y_val, val_pred, val_prob)
                score = val_metrics[primary_metric]
                
            elif task_type == 'multiclass_classification':
                model = xgb.XGBClassifier(
                    **candidate_params,
                    objective='multi:softprob',
                    num_class=num_class,
                    random_state=random_state,
                    n_jobs=n_jobs,
                    eval_metric='mlogloss'
                )
                model.fit(X_train, y_train)
                val_pred = model.predict(X_val)
                val_prob = model.predict_proba(X_val)
                val_metrics = evaluate_classification(y_val, val_pred, val_prob, is_multiclass=True, num_classes=num_class)
                score = val_metrics[primary_metric]
                
            else: # regression
                # Remove scale_pos_weight for regressor
                reg_params = {k: v for k, v in candidate_params.items() if k != 'scale_pos_weight'}
                model = xgb.XGBRegressor(
                    **reg_params,
                    random_state=random_state,
                    n_jobs=n_jobs,
                    eval_metric='rmse'
                )
                model.fit(X_train, y_train)
                val_pred = model.predict(X_val)
                val_metrics = evaluate_regression(y_val, val_pred)
                # Primary metric is RMSE -> higher is better when negated
                score = -val_metrics['rmse']
                
            search_records.append({
                'iteration': i + 1,
                'params': candidate_params,
                'val_score': score,
                'val_metrics': val_metrics
            })
            
            if score > best_score:
                best_score = score
                best_params = candidate_params
                best_model = model
                best_val_metrics = val_metrics
                
        except Exception as e:
            print(f"  [Warning] Iteration {i+1} failed: {e}")
            continue

    # Fallback to initial if search did not improve or failed
    if best_params is None:
        best_params = init_xgb.get_params()
        best_model = init_xgb
        best_val_metrics = init_val_metrics

    return {
        'baseline_model': baseline,
        'baseline_val_metrics': base_val_metrics,
        'initial_model': init_xgb,
        'initial_val_metrics': init_val_metrics,
        'unweighted_val_metrics': unweighted_comparison,
        'best_model': best_model,
        'best_params': best_params,
        'best_val_metrics': best_val_metrics,
        'search_records': search_records
    }

