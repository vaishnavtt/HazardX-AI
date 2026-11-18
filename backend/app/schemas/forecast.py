"""
HAZARDX AI — Multi-Hazard Forecasting & Early Warning Schemas
Standardized data contracts for multi-horizon hazard forecasts (6h, 12h, 24h, 48h, 72h),
data provenance tracking, uncertainty quantification, and predictive risk profiling.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum

class ForecastHorizon(str, Enum):
    H6 = "6h"
    H12 = "12h"
    H24 = "24h"
    H48 = "48h"
    H72 = "72h"

class RiskCategory(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    VERY_HIGH = "VERY HIGH"
    EXTREME = "EXTREME"

class DataProvenanceType(str, Enum):
    LIVE_OBSERVATION = "LIVE_OBSERVATION"
    LIVE_FORECAST = "LIVE_FORECAST"
    CACHED_OBSERVATION = "CACHED_OBSERVATION"
    CACHED_FORECAST = "CACHED_FORECAST"
    HISTORICAL = "HISTORICAL"
    MODEL_INFERENCE = "MODEL_INFERENCE"
    SIMULATED = "SIMULATED"

class SourceFreshness(str, Enum):
    FRESH = "FRESH"
    ACCEPTABLE = "ACCEPTABLE"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"

class HorizonForecastItem(BaseModel):
    horizon: ForecastHorizon
    valid_from: str
    valid_until: str
    risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_category: RiskCategory
    primary_metric_label: str
    primary_metric_value: float
    primary_metric_unit: str
    contributing_factors: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_level: str  # "HIGH", "MODERATE", "LOW", "STATISTICAL_ESTIMATE"
    uncertainty_range: Optional[Dict[str, float]] = None
    data_sources: List[str] = Field(default_factory=list)
    data_provenance: DataProvenanceType = DataProvenanceType.LIVE_FORECAST

class SingleHazardForecast(BaseModel):
    hazard_type: str
    geographic_location: str
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    forecast_generated_at: str
    forecast_valid_from: str
    forecast_valid_until: str
    forecast_horizon: ForecastHorizon
    risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_category: RiskCategory
    model_name: str
    model_version: str = "v1.0"
    model_status: str  # "OPERATIONAL", "EXPERIMENTAL", "STATISTICAL_MODEL", "BLOCKED"
    contributing_features: Dict[str, Any] = Field(default_factory=dict)
    explanation: str
    confidence_or_uncertainty: Dict[str, Any] = Field(default_factory=dict)
    data_sources: List[str] = Field(default_factory=list)
    data_freshness: str = "LIVE"
    data_provenance: DataProvenanceType = DataProvenanceType.LIVE_FORECAST
    warnings: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    secondary_metrics: Dict[str, Any] = Field(default_factory=dict)

class HazardForecastTimeline(BaseModel):
    hazard_type: str
    geographic_location: str
    latitude: float
    longitude: float
    generated_at: str
    model_name: str
    model_status: str
    horizons: Dict[str, HorizonForecastItem]
    overall_trend: str  # "INCREASING", "PEAKING", "DECREASING", "STABLE"
    peak_risk_horizon: ForecastHorizon
    peak_risk_score: float
    disclaimer: str

class MultiHazardLocationForecastResponse(BaseModel):
    location_name: str
    latitude: float
    longitude: float
    generated_at: str
    composite_risk_category: RiskCategory
    composite_risk_score: float
    primary_hazard: str
    hazard_forecasts: Dict[str, SingleHazardForecast]
    timeline_by_hazard: Dict[str, HazardForecastTimeline]
    active_observations_summary: Dict[str, Any]
    sources_used: List[Dict[str, Any]]
    limitations: List[str]
    disclaimer: str

class LocationForecastRequest(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    location_name: Optional[str] = "User Specified Location"
    hazards: Optional[List[str]] = None  # None = all 5
    selected_horizon: Optional[ForecastHorizon] = ForecastHorizon.H24

class ForecastSummaryCard(BaseModel):
    hazard_type: str
    current_status: str
    forecast_risk: RiskCategory
    forecast_horizon: ForecastHorizon
    peak_score: float
    last_updated: str
    main_contributing_factors: List[str]
    primary_data_source: str
    data_provenance: DataProvenanceType
    model_status: str
    trend: str

