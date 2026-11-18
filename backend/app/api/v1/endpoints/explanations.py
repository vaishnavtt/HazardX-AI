"""
HAZARDX AI — Global Explainability & SHAP Insights Endpoint
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.schemas.responses import HazardExplanationResponse
from backend.app.services.model_registry import registry
from backend.app.services.explanation_service import PHYSICAL_INTERPRETATIONS
from backend.app.utils.logging_config import get_logger

logger = get_logger("explanations_api")
router = APIRouter()

PRIMARY_TASKS = {
    "floods": "flood_occurrence",
    "flood": "flood_occurrence",
    "landslides": "landslide_occurrence",
    "landslide": "landslide_occurrence",
    "earthquakes": "aftershock_hazard",
    "earthquake": "aftershock_hazard",
    "cyclones": "rapid_intensification",
    "cyclone": "rapid_intensification",
    "wildfires": "wildfire_occurrence",
    "wildfire": "wildfire_occurrence"
}

HAZARD_PHYSICAL_SUMMARIES = {
    "floods": "Flood risk is driven predominantly by acute 1-day and 3-day precipitation pulses interacting with antecedent 7-day soil saturation and low-elevation drainage basins.",
    "landslides": "Landslide susceptibility is governed by steep topographic slope angles (>25°) coupled with sub-surface pore water pressure buildup from 30-day antecedent rainfall.",
    "earthquakes": "Secondary aftershock clustering hazard is driven by mainshock magnitude (rupture energy release), 365-day regional background seismicity, and proximity to active GEM fault boundaries.",
    "cyclones": "Tropical cyclone rapid intensification (RI) is primarily driven by existing 6-hour wind momentum, central sea-level pressure deepening, and thermodynamic headroom beneath Maximum Potential Intensity.",
    "wildfires": "Wildfire ignition susceptibility is dominated by low surface relative humidity, elevated Fire Weather Index (FWI), and high ambient air temperature desiccating fine dead forest fuels."
}

@router.get("/explanations/{hazard}", response_model=HazardExplanationResponse, tags=["Model Explainability"])
def get_hazard_explanation(
    hazard: str,
    task: Optional[str] = Query(None, description="Optional task name (defaults to primary operational task)")
) -> HazardExplanationResponse:
    """
    Returns global TreeSHAP feature attributions, physical interpretation,
    and SHAP diagnostic plot paths for the specified hazard.
    """
    hazard_norm = hazard.lower().strip()
    if hazard_norm not in PRIMARY_TASKS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hazard '{hazard}' not recognized. Supported: floods, landslides, earthquakes, cyclones, wildfires."
        )
        
    canon_hazard = "floods" if "flood" in hazard_norm else \
                   "landslides" if "landslide" in hazard_norm else \
                   "earthquakes" if "earthquake" in hazard_norm else \
                   "cyclones" if "cyclone" in hazard_norm else "wildfires"

    task_name = task or PRIMARY_TASKS[hazard_norm]
    meta = registry.get_metadata(canon_hazard, task_name)
    
    if meta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No metadata found for hazard '{canon_hazard}' and task '{task_name}'."
        )
        
    top_shap = meta.get("top_features_shap", [])
    enriched_features = []
    for item in top_shap:
        feat_name = item.get("feature", "")
        enriched_features.append({
            "feature": feat_name,
            "mean_abs_shap": item.get("mean_abs_shap", 0.0),
            "physical_role": PHYSICAL_INTERPRETATIONS.get(feat_name, "Physical predictor.")
        })
        
    phys_summary = HAZARD_PHYSICAL_SUMMARIES.get(
        canon_hazard,
        "TreeSHAP attributions indicate consistent physical relationship with historical hazard observations."
    )

    return HazardExplanationResponse(
        hazard_name=canon_hazard.capitalize(),
        task_name=task_name,
        method="TreeSHAP (Tree Explainer)",
        top_global_features=enriched_features,
        physical_interpretation=phys_summary,
        shap_summary_plot_url=meta.get("shap_summary_plot"),
        shap_bar_plot_url=meta.get("shap_bar_plot")
    )
