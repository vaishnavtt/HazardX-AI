"""
HAZARDX AI — Tropical Cyclone Prediction Pydantic Schemas
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .common import FeatureAttribution

class CycloneFeatures(BaseModel):
    current_wind_kt: float = Field(..., ge=0.0, le=220.0, description="Current 1-min / 10-min sustained wind speed (knots, 0 if calm)")
    current_pres_hpa: float = Field(..., ge=850.0, le=1030.0, description="Current central minimum sea-level pressure (hPa)")
    dist_to_land_km: float = Field(..., ge=0.0, description="Distance from vortex center to nearest coastline (km)")
    landfall_flag: int = Field(..., ge=0, le=1, description="Binary indicator (1 = storm center is over land, 0 = over ocean)")
    past_delta_wind_6h: float = Field(..., ge=-100.0, le=100.0, description="Intensity change over past 6 hours (knots)")
    past_delta_wind_12h: float = Field(..., ge=-150.0, le=150.0, description="Intensity change over past 12 hours (knots)")
    past_delta_pres_6h: float = Field(..., ge=-100.0, le=100.0, description="Central pressure change over past 6 hours (hPa)")
    translational_speed_kt: float = Field(..., ge=0.0, le=80.0, description="Storm forward translational speed (knots)")
    heading_degrees: float = Field(..., ge=0.0, le=360.0, description="Compass azimuth heading of storm track (degrees)")
    coriolis_param: float = Field(..., description="Coriolis parameter f = 2*Omega*sin(lat) (s⁻¹)")
    pot_intensity_headroom: float = Field(..., description="Headroom between current wind and Maximum Potential Intensity (knots)")

class CyclonePredictionResponse(BaseModel):
    hazard_name: str = "Cyclones"
    rapid_intensification_predicted: bool
    rapid_intensification_probability: float = Field(..., description="Probability of Delta V >= 30 kt increase within 24 hours")
    predicted_24h_intensity_change_kt: float = Field(..., description="Operational continuous 24h wind change forecast (knots)")
    projected_wind_24h_kt: float = Field(..., description="Current wind + predicted 24h change (knots)")
    risk_category: str
    alert_level: str
    action_guidance: str
    important_contributing_features: List[FeatureAttribution]
    model_version: str = "1.0.0"
    input_validation_status: str = "VALID"
    limitations_and_warnings: List[str]

