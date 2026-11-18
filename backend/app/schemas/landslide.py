"""
HAZARDX AI — Landslide Prediction Pydantic Schemas
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .common import FeatureAttribution

class LandslideFeatures(BaseModel):
    precip_1d_mm: float = Field(..., ge=0.0, le=1000.0, description="1-day rainfall total (mm)")
    precip_3d_sum_mm: float = Field(..., ge=0.0, le=2000.0, description="3-day cumulative rainfall (mm)")
    precip_7d_sum_mm: float = Field(..., ge=0.0, le=3000.0, description="7-day cumulative rainfall (mm)")
    precip_30d_sum_mm: float = Field(..., ge=0.0, le=5000.0, description="30-day antecedent cumulative rainfall (mm)")
    api_30d_index: float = Field(..., ge=0.0, le=2000.0, description="30-day antecedent precipitation index (mm)")
    temp_2m_celsius: float = Field(..., ge=-60.0, le=60.0, description="Mean 2m air temperature (°C)")
    soil_temp_celsius: float = Field(..., ge=-40.0, le=60.0, description="Topsoil temperature (°C)")
    slope_degrees: float = Field(..., ge=0.0, le=90.0, description="Copernicus DEM slope gradient (degrees)")
    elevation_m: float = Field(..., ge=-500.0, le=9000.0, description="Surface elevation (m)")
    aspect_degrees: float = Field(..., ge=0.0, le=360.0, description="Terrain aspect angle (degrees)")
    plan_curvature: float = Field(..., ge=-5.0, le=5.0, description="Topographic plan curvature")
    soil_clay_fraction_pct: float = Field(..., ge=0.0, le=100.0, description="Estimated soil clay fraction percentage (%)")
    distance_to_road_km: float = Field(..., ge=0.0, le=50.0, description="Distance to nearest road cut (km)")
    distance_to_stream_km: float = Field(..., ge=0.0, le=50.0, description="Distance to nearest valley stream (km)")

class LandslidePredictionResponse(BaseModel):
    hazard_name: str = "Landslides"
    landslide_occurrence_predicted: bool
    raw_model_score: float
    calibrated_susceptibility_score: float
    risk_category: str
    alert_level: str
    hazard_magnitude_class: int = Field(..., description="0 = None, 1 = Small/Medium, 2 = Large/Catastrophic")
    hazard_magnitude_label: str
    action_guidance: str
    important_contributing_features: List[FeatureAttribution]
    model_version: str = "1.0.0"
    input_validation_status: str = "VALID"
    limitations_and_warnings: List[str]

