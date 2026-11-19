"""
HAZARDX AI — Geospatial Risk Assessment Pydantic Schemas
Defines request and response models for multi-hazard location profiling,
environmental feature synthesis, and SHAP-explained risk inference.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class GeospatialAssessmentRequest(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Target location latitude (-90 to +90)")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Target location longitude (-180 to +180)")
    hazards: Optional[List[str]] = Field(
        default=["floods", "landslides", "earthquakes", "wildfires", "cyclones"],
        description="List of natural hazards to evaluate"
    )
    scenario_params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional scenario overrides (e.g. mainshock_mag, precip_override_mm)"
    )

class EnvironmentalContext(BaseModel):
    elevation_m: float
    slope_degrees: float
    aspect_degrees: float
    plan_curvature: float
    topographic_wetness_index: float
    dist_to_active_fault_km: float
    nearest_fault_slip_type: str
    temp_2m_celsius: float
    relative_humidity_pct: float
    wind_speed_10m_ms: float
    surface_pressure_hpa: float
    precip_1d_mm: float
    precip_30d_sum_mm: float
    river_discharge_m3s: float
    fwi_fire_weather_index: float
    weather_description: str
    data_freshness: str = "LIVE"
    source_attribution: str = "Copernicus DEM, GEM Active Faults, Open-Meteo NWP & GloFAS"

class HazardAssessmentResult(BaseModel):
    hazard: str
    model_name: str
    predicted: bool
    probability: float
    calibrated_probability: Optional[float] = None
    risk_category: str  # GREEN, YELLOW, ORANGE, RED
    alert_level: str
    guidance: str
    operational_status: str
    secondary_prediction: Optional[Dict[str, Any]] = None
    top_features: List[Dict[str, Any]] = []
    defined_target: Optional[str] = None
    confidence_or_uncertainty: Optional[str] = None
    data_sources: Optional[List[str]] = None
    data_freshness: Optional[str] = "LIVE"

class GeospatialAssessmentResponse(BaseModel):
    latitude: float
    longitude: float
    location_name: str
    timestamp: str
    environmental_context: EnvironmentalContext
    assessments: Dict[str, HazardAssessmentResult]
    overall_composite_risk: str
    overall_summary: str
    feature_completeness_pct: float
    disclaimer: str = (
        "HAZARDX AI multi-hazard assessments are synthesized from authentic scientific "
        "observations and calibrated machine learning models. Earthquake assessments quantify "
        "regional aftershock hazard susceptibility and do NOT predict exact earthquake occurrences."
    )

class LocationProfileResponse(BaseModel):
    latitude: float
    longitude: float
    timestamp: str
    environmental_context: EnvironmentalContext
    nearest_fault: Dict[str, Any]
    terrain: Dict[str, Any]
    weather: Dict[str, Any]
    hydrology: Dict[str, Any]

class LocationSearchResult(BaseModel):
    id: str
    name: str
    state: Optional[str] = None
    country: str
    display_name: str
    latitude: float
    longitude: float
    place_type: str = "city"
    importance: float = 0.5

class LocationSearchResponse(BaseModel):
    query: str
    count: int
    results: List[LocationSearchResult]


