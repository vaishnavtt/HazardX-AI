"""
HAZARDX AI — Executive Dashboard Summary Endpoint
"""

import os
import json
from typing import Dict, Any
from fastapi import APIRouter
from backend.app.schemas.responses import DashboardSummaryResponse
from backend.app.services.model_registry import registry
from backend.app.config import settings

router = APIRouter()

@router.get("/dashboard/summary", response_model=DashboardSummaryResponse, tags=["Dashboard"])
def get_dashboard_summary() -> DashboardSummaryResponse:
    """
    Returns an executive-level summary of the entire HAZARDX AI intelligence system,
    including model operational counts, per-hazard benchmark metrics, and system status.
    """
    operational_cnt = 0
    experimental_cnt = 0
    for key in registry.models.keys():
        s = settings.MODEL_STATUS.get(key, "OPERATIONAL")
        if s == "OPERATIONAL":
            operational_cnt += 1
        elif s == "EXPERIMENTAL":
            experimental_cnt += 1

    # Load dashboard table
    dash_path = os.path.join(settings.MODELS_DIR, "model_comparison_dashboard.json")
    dash_records = []
    if os.path.exists(dash_path):
        with open(dash_path, "r", encoding="utf-8") as f:
            dash_records = json.load(f)

    hazard_overview: Dict[str, Dict[str, Any]] = {
        "Floods": {
            "supported_tasks": ["flood_occurrence", "flood_severity"],
            "primary_task": "flood_occurrence",
            "primary_metric": "PR-AUC: 0.8156 | ROC-AUC: 0.7899",
            "operational_status": "OPERATIONAL",
            "key_drivers": ["1d/3d/7d precipitation", "soil temperature", "elevation", "river discharge"]
        },
        "Landslides": {
            "supported_tasks": ["landslide_occurrence", "landslide_magnitude"],
            "primary_task": "landslide_occurrence",
            "primary_metric": "PR-AUC: 0.8407 | ROC-AUC: 0.8471",
            "operational_status": "OPERATIONAL",
            "key_drivers": ["slope angle", "30d antecedent precipitation", "elevation", "clay fraction"]
        },
        "Earthquakes": {
            "supported_tasks": ["aftershock_hazard", "max_aftershock_mag", "aftershock_count"],
            "primary_task": "aftershock_hazard (M>=5.0)",
            "primary_metric": "PR-AUC: 0.8464 | ROC-AUC: 0.8038",
            "operational_status": "OPERATIONAL (Regression tasks experimental / blocked)",
            "key_drivers": ["prior 365d count", "mainshock magnitude", "focal depth", "fault distance"],
            "disclaimer": "Evaluates statistical aftershock hazard; NOT an earthquake prediction."
        },
        "Cyclones": {
            "supported_tasks": ["rapid_intensification", "intensity_change_24h"],
            "primary_task": "rapid_intensification (+30kt/24h)",
            "primary_metric": "PR-AUC: 0.3543 (vs 0.0662 baseline) | Intensity R^2: 0.4426",
            "operational_status": "OPERATIONAL",
            "key_drivers": ["past delta wind 6h", "translational speed", "coriolis param", "pressure drop"]
        },
        "Wildfires": {
            "supported_tasks": ["wildfire_occurrence", "frp_intensity", "fire_duration"],
            "primary_task": "wildfire_occurrence",
            "primary_metric": "PR-AUC: 0.8272 | ROC-AUC: 0.8247",
            "operational_status": "OPERATIONAL (Duration blocked; FRP experimental)",
            "key_drivers": ["relative humidity", "Fire Weather Index", "air temperature", "wind speed"]
        }
    }

    return DashboardSummaryResponse(
        system_name="HAZARDX AI Multi-Hazard Intelligence Platform",
        status="ONLINE",
        total_hazards_supported=5,
        total_models_available=len(registry.models),
        operational_models_count=operational_cnt,
        experimental_models_count=experimental_cnt,
        hazard_overview=hazard_overview
    )
