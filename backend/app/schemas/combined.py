"""
HAZARDX AI — Combined Multi-Hazard Prediction Pydantic Schemas
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

from .flood import FloodFeatures, FloodPredictionResponse
from .landslide import LandslideFeatures, LandslidePredictionResponse
from .earthquake import EarthquakeFeatures, EarthquakePredictionResponse
from .cyclone import CycloneFeatures, CyclonePredictionResponse
from .wildfire import WildfireFeatures, WildfirePredictionResponse

class MultiHazardPredictionRequest(BaseModel):
    flood: Optional[FloodFeatures] = Field(None, description="Features for flood prediction (optional)")
    landslide: Optional[LandslideFeatures] = Field(None, description="Features for landslide prediction (optional)")
    earthquake: Optional[EarthquakeFeatures] = Field(None, description="Features for earthquake aftershock prediction (optional)")
    cyclone: Optional[CycloneFeatures] = Field(None, description="Features for tropical cyclone prediction (optional)")
    wildfire: Optional[WildfireFeatures] = Field(None, description="Features for wildfire prediction (optional)")

class MultiHazardPredictionResponse(BaseModel):
    timestamp: str
    hazards_evaluated: List[str]
    composite_highest_alert_level: str = Field(..., description="Highest alert level among all evaluated hazards (GREEN, YELLOW, ORANGE, RED)")
    results: Dict[str, Any] = Field(..., description="Per-hazard evaluation output objects")

