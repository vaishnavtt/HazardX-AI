"""
HAZARDX AI — Flood Prediction Pydantic Schemas
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .common import FeatureAttribution

class FloodFeatures(BaseModel):
    precip_1d_mm: float = Field(..., ge=0.0, le=1000.0, description="1-day precipitation total (mm)")
    precip_3d_sum_mm: float = Field(..., ge=0.0, le=2000.0, description="3-day cumulative precipitation (mm)")
    precip_7d_sum_mm: float = Field(..., ge=0.0, le=3000.0, description="7-day cumulative precipitation (mm)")
    precip_14d_sum_mm: float = Field(..., ge=0.0, le=4000.0, description="14-day cumulative precipitation (mm)")
    api_14d_index: float = Field(..., ge=0.0, le=1000.0, description="14-day antecedent precipitation index (mm)")
    temp_2m_celsius: float = Field(..., ge=-60.0, le=60.0, description="Mean 2m surface air temperature (°C)")
    soil_temp_celsius: float = Field(..., ge=-40.0, le=60.0, description="0-7cm topsoil temperature (°C)")
    river_discharge_m3s: float = Field(..., ge=0.0, description="Daily river discharge rate (m³/s)")
    river_discharge_7d_mean_m3s: float = Field(..., ge=0.0, description="7-day antecedent mean river discharge (m³/s)")
    river_discharge_ratio_7d: float = Field(..., ge=0.0, description="Ratio of current discharge to 7-day mean")
    elevation_m: float = Field(..., ge=-500.0, le=9000.0, description="Terrain elevation from Copernicus DEM (m)")
    slope_degrees: float = Field(..., ge=0.0, le=90.0, description="Local terrain slope angle (degrees)")
    topographic_wetness_index: float = Field(..., ge=0.0, le=30.0, description="Topographic Wetness Index (TWI)")
    distance_to_river_km: float = Field(..., ge=0.0, le=200.0, description="Distance to nearest major river channel (km)")

class FloodPredictionResponse(BaseModel):
    hazard_name: str = "Floods"
    flood_occurrence_predicted: bool
    raw_model_score: float = Field(..., description="Raw model probability score [0.0, 1.0] from balanced case-control training")
    calibrated_susceptibility_score: float = Field(..., description="Bayesian prior-adjusted real-world occurrence probability")
    risk_category: str = Field(..., description="LOW, MODERATE, HIGH, or SEVERE_CRITICAL")
    alert_level: str = Field(..., description="GREEN, YELLOW, ORANGE, or RED")
    severity_class: int = Field(..., description="0 = None, 1 = Large Flood, 2 = Extreme/Decadal Flood")
    severity_label: str
    action_guidance: str
    important_contributing_features: List[FeatureAttribution]
    model_version: str = "1.0.0"
    input_validation_status: str = "VALID"
    limitations_and_warnings: List[str]

