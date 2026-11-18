"""
HAZARDX AI — Common Pydantic Schemas & Shared Types
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class FeatureAttribution(BaseModel):
    feature: str = Field(..., description="Name of the physical/environmental covariate")
    importance_score: float = Field(..., description="SHAP attribution or relative importance weight")
    direction: str = Field(..., description="'RISK_INCREASING' or 'RISK_DECREASING'")
    description: str = Field(..., description="Physical interpretation of the feature contribution")

class ModelPerformanceSummary(BaseModel):
    hazard: str
    task_name: str
    task_type: str
    target_column: str
    algorithm: str = "XGBoost"
    operational_status: str
    primary_metric_name: str
    primary_test_score: float
    secondary_metric_name: str
    secondary_test_score: float
    top_important_features: str
    version: str = "1.0.0"

class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    service: str = "HAZARDX AI Early Warning Backend"
    models_loaded: int
    operational_models: List[str]
    experimental_models: List[str]
    timestamp: str

