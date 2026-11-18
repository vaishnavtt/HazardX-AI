"""
HAZARDX AI — Model Catalog & Performance Endpoints
"""

import os
import json
from typing import List
from fastapi import APIRouter
from backend.app.schemas.responses import ModelCatalogResponse, ModelCatalogItem
from backend.app.schemas.common import ModelPerformanceSummary
from backend.app.services.model_registry import registry
from backend.app.config import settings

router = APIRouter()

@router.get("/models", response_model=ModelCatalogResponse, tags=["Model Governance"])
def get_model_catalog() -> ModelCatalogResponse:
    """
    Returns the comprehensive catalog of all 12 trained hazard models with their
    operational status, primary performance metrics, and governance boundaries.
    """
    items: List[ModelCatalogItem] = []
    operational_cnt = 0
    experimental_cnt = 0
    
    # Read dashboard json for consistent cross-reference
    dash_path = os.path.join(settings.MODELS_DIR, "model_comparison_dashboard.json")
    dash_records = {}
    if os.path.exists(dash_path):
        with open(dash_path, "r", encoding="utf-8") as f:
            for r in json.load(f):
                h_key = r["hazard"].lower()
                task_key = r["prediction_target"]
                dash_records[f"{h_key}_{task_key}"] = r

    for key, meta in registry.metadata.items():
        hazard = meta.get("hazard", key.split("_")[0])
        task_name = meta.get("task_name", "_".join(key.split("_")[1:]))
        status = settings.MODEL_STATUS.get(key, "OPERATIONAL")
        
        if status == "OPERATIONAL":
            operational_cnt += 1
        elif status == "EXPERIMENTAL":
            experimental_cnt += 1
            
        dash_row = dash_records.get(key, {})
        primary_metric = dash_row.get("primary_metric_name", "Test Score")
        primary_score = float(dash_row.get("primary_test_score", 0.0))
        
        items.append(ModelCatalogItem(
            hazard=hazard.capitalize(),
            task_name=task_name,
            task_type=meta.get("task_type", "unknown"),
            target_column=meta.get("target_column", "target"),
            operational_status=status,
            primary_metric_name=primary_metric,
            primary_test_score=primary_score,
            model_version=meta.get("version", "1.0.0"),
            artifact_path=meta.get("artifact_joblib", ""),
            description=meta.get("description", "")
        ))
        
    return ModelCatalogResponse(
        total_models=len(items),
        operational_models_count=operational_cnt,
        experimental_models_count=experimental_cnt,
        models=items
    )

@router.get("/models/performance", response_model=List[ModelPerformanceSummary], tags=["Model Governance"])
def get_model_performance() -> List[ModelPerformanceSummary]:
    """
    Returns empirical test set performance benchmarks for all trained models.
    """
    summaries: List[ModelPerformanceSummary] = []
    dash_path = os.path.join(settings.MODELS_DIR, "model_comparison_dashboard.json")
    if os.path.exists(dash_path):
        with open(dash_path, "r", encoding="utf-8") as f:
            records = json.load(f)
            for r in records:
                h_key = r["hazard"].lower()
                task_key = r["prediction_target"]
                key = f"{h_key}_{task_key}"
                status = settings.MODEL_STATUS.get(key, "OPERATIONAL")
                
                summaries.append(ModelPerformanceSummary(
                    hazard=r["hazard"],
                    task_name=r["prediction_target"],
                    task_type=r["task_type"],
                    target_column=r["target_column"],
                    algorithm=r.get("algorithm", "XGBoost"),
                    operational_status=status,
                    primary_metric_name=r.get("primary_metric_name", "Primary Metric"),
                    primary_test_score=float(r.get("primary_test_score", 0.0)),
                    secondary_metric_name=r.get("secondary_metric_name", "Secondary Metric"),
                    secondary_test_score=float(r.get("secondary_test_score", 0.0)),
                    top_important_features=r.get("top_important_features", ""),
                    version=r.get("model_version", "1.0.0")
                ))
    return summaries


@router.get("/models/phase13-validation", tags=["Model Governance"])
def get_phase13_validation():
    """
    Returns the complete Phase 13 retrospective validation data:
    - Dataset and model inventory
    - Holdout test evaluation results with confusion matrices & baseline comparisons
    - Retrospective timeline advance warning experiments for 10 landmark disasters
    - Model improvement and calibration findings
    """
    reports_dir = settings.REPORTS_DIR
    def load_json(filename):
        path = os.path.join(reports_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    return {
        "inventory": load_json("phase13_model_and_dataset_inventory.json"),
        "evaluation": load_json("phase13_model_evaluation_results.json"),
        "retrospective": load_json("phase13_retrospective_experiments.json"),
        "improvements": load_json("phase13_model_improvements_summary.json"),
    }

