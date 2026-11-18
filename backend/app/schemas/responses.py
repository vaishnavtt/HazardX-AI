"""
HAZARDX AI — Management & Summary Responses
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from .common import ModelPerformanceSummary

class ModelCatalogItem(BaseModel):
    hazard: str
    task_name: str
    task_type: str
    target_column: str
    operational_status: str
    primary_metric_name: str
    primary_test_score: float
    model_version: str
    artifact_path: str
    description: str

class ModelCatalogResponse(BaseModel):
    total_models: int
    operational_models_count: int
    experimental_models_count: int
    models: List[ModelCatalogItem]

class HazardExplanationResponse(BaseModel):
    hazard_name: str
    task_name: str
    method: str = "TreeSHAP (Tree Explainer)"
    top_global_features: List[Dict[str, Any]]
    physical_interpretation: str
    shap_summary_plot_url: Optional[str]
    shap_bar_plot_url: Optional[str]

class DashboardSummaryResponse(BaseModel):
    system_name: str = "HAZARDX AI Multi-Hazard Intelligence Platform"
    status: str = "ONLINE"
    total_hazards_supported: int = 5
    total_models_available: int = 12
    operational_models_count: int
    experimental_models_count: int
    hazard_overview: Dict[str, Dict[str, Any]]

