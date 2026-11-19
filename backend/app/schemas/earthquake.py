"""
HAZARDX AI — Earthquake Aftershock Hazard Pydantic Schemas
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from .common import FeatureAttribution

VALID_SLIP_TYPES = [
    'Anticline', 'Dextral', 'Dextral-Normal', 'Dextral-Reverse',
    'Dextral_Transform', 'Normal', 'Normal-Dextral',
    'Normal-Sinistral', 'Reverse', 'Reverse-Dextral',
    'Reverse-Sinistral', 'Reverse-Strike-Slip', 'Sinistral',
    'Sinistral-Normal', 'Sinistral-Reverse', 'Sinistral_Transform',
    'Spreading_Ridge', 'Strike-Slip', 'Subduction_Thrust', 'Unknown'
]

class EarthquakeFeatures(BaseModel):
    mainshock_mag: float = Field(..., ge=0.0, le=10.0, description="Triggering earthquake magnitude (Mw, 0.0 if quiescent)")
    focal_depth_km: float = Field(..., ge=0.0, le=700.0, description="Hypocentral depth (km)")
    dist_to_active_fault_km: float = Field(..., ge=0.0, description="3D distance to nearest GEM active fault vertex (km)")
    nearest_fault_slip_type: str = Field(default="Subduction_Thrust", description="Tectonic slip regime")
    prior_count_7d_100km: int = Field(..., ge=0, description="Preceding 7-day earthquake count within 100km")
    prior_count_30d_100km: int = Field(..., ge=0, description="Preceding 30-day earthquake count within 100km")
    prior_count_365d_100km: int = Field(..., ge=0, description="Preceding 1-year background earthquake count within 100km")
    prior_max_mag_30d: float = Field(..., ge=0.0, le=10.0, description="Maximum magnitude observed within 100km in prior 30 days")
    cumulative_energy_log_joules: float = Field(..., description="Log10 cumulative radiated seismic energy (Joules)")
    seismic_rate_accel_ratio: float = Field(..., ge=0.0, description="Ratio of 7-day to 30-day normalized seismicity rate")
    regional_b_value: float = Field(..., ge=0.2, le=2.5, description="Gutenberg-Richter b-value parameter")

    @field_validator('nearest_fault_slip_type')
    @classmethod
    def validate_slip_type(cls, v: str) -> str:
        if v not in VALID_SLIP_TYPES:
            raise ValueError(f"Invalid fault slip type: '{v}'. Must be one of {VALID_SLIP_TYPES}")
        return v

class EarthquakePredictionResponse(BaseModel):
    hazard_name: str = "Earthquakes"
    assessment_type: str = "Regional Aftershock Hazard Assessment (30-day / 100km horizon)"
    disclaimer: str = "This service provides statistical aftershock hazard assessment following a mainshock. This is NOT an exact earthquake prediction."
    elevated_aftershock_hazard_predicted: bool
    hazard_probability: float
    risk_category: str
    alert_level: str
    action_guidance: str
    estimated_max_aftershock_magnitude: Optional[float] = Field(None, description="[EXPERIMENTAL] Estimated upper bound of secondary magnitude")
    estimated_aftershock_count: Optional[float] = Field(None, description="[UNAVAILABLE FOR OPERATIONAL USE] Heavy-tailed dispersion notice")
    important_contributing_features: List[FeatureAttribution]
    model_version: str = "1.0.0"
    input_validation_status: str = "VALID"
    limitations_and_warnings: List[str]
