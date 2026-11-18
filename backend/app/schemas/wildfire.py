"""
HAZARDX AI — Wildfire Prediction Pydantic Schemas
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .common import FeatureAttribution

class WildfireFeatures(BaseModel):
    temp_2m_celsius: float = Field(..., ge=-60.0, le=60.0, description="Daily mean 2m air temperature (°C)")
    relative_humidity_pct: float = Field(..., ge=0.0, le=100.0, description="Surface relative humidity (%)")
    wind_speed_10m_ms: float = Field(..., ge=0.0, le=60.0, description="10m surface wind speed (m/s)")
    precip_7d_sum_mm: float = Field(..., ge=0.0, le=2000.0, description="7-day cumulative precipitation (mm)")
    precip_30d_sum_mm: float = Field(..., ge=0.0, le=4000.0, description="30-day cumulative precipitation (mm)")
    soil_temp_celsius: float = Field(..., ge=-50.0, le=60.0, description="Topsoil temperature (°C)")
    fwi_fire_weather_index: float = Field(..., ge=0.0, description="Canadian Forest Fire Weather Index (FWI) proxy")
    slope_degrees: float = Field(..., ge=0.0, le=90.0, description="Terrain slope angle (degrees)")
    elevation_m: float = Field(..., ge=-500.0, le=9000.0, description="Copernicus DEM surface elevation (m)")
    distance_to_road_km: float = Field(..., ge=0.0, le=50.0, description="Distance to nearest road / human access corridor (km)")

class WildfirePredictionResponse(BaseModel):
    hazard_name: str = "Wildfires"
    wildfire_susceptibility_predicted: bool
    raw_model_score: float
    calibrated_susceptibility_score: float
    risk_category: str
    alert_level: str
    action_guidance: str
    estimated_log_frp_mw: Optional[float] = Field(None, description="[EXPERIMENTAL] Estimated log10 Fire Radiative Power (MW)")
    estimated_duration_days: Optional[float] = Field(None, description="[UNAVAILABLE FOR OPERATIONAL USE] Blocked due to low test variance")
    important_contributing_features: List[FeatureAttribution]
    model_version: str = "1.0.0"
    input_validation_status: str = "VALID"
    limitations_and_warnings: List[str]

