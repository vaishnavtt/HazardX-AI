"""
HAZARDX AI — External Live Data Pydantic Schemas
Defines structured representations for real-time natural hazard observations,
weather feeds, hydrological sensors, and API status monitoring.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LiveEarthquakeEvent(BaseModel):
    id: str
    title: str
    magnitude: float
    depth_km: float
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    event_time: str
    location: str
    significance: Optional[int] = None
    url: Optional[str] = None
    data_freshness: str = "LIVE"
    source: str = "USGS Earthquake Hazards Program"

class LiveWildfireEvent(BaseModel):
    id: str
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    brightness_kelvin: float
    frp_mw: float
    confidence: str
    acq_time: str
    satellite: str
    daynight: str
    data_freshness: str = "LIVE"
    source: str = "NASA FIRMS (MODIS / VIIRS)"

class LiveCycloneEvent(BaseModel):
    id: str
    name: str
    basin: str
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    intensity_kt: float
    min_pressure_hpa: Optional[float] = None
    speed_kt: Optional[float] = None
    heading_deg: Optional[float] = None
    observation_time: str
    classification: str
    data_freshness: str = "LIVE"
    source: str = "NOAA NHC / JTWC / IBTrACS"

class LiveFloodObservation(BaseModel):
    id: str
    location_name: str
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    current_discharge_m3s: float
    mean_discharge_7d_m3s: float
    max_forecast_discharge_m3s: float
    discharge_anomaly_ratio: float
    flood_threshold_exceeded: bool
    observation_time: str
    data_freshness: str = "LIVE"
    source: str = "Copernicus GloFAS via Open-Meteo Flood API"

class LiveLandslideObservation(BaseModel):
    id: str
    location_name: str
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    precip_1d_mm: float
    precip_30d_mm: float
    slope_degrees: float
    elevated_moisture_hazard: bool
    observation_time: str
    data_freshness: str = "LIVE"
    source: str = "NASA GLC & Open-Meteo ERA5 Reanalysis"

class CurrentWeatherObservation(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    elevation_m: float
    temperature_2m_c: float
    relative_humidity_pct: float
    precipitation_mm: float
    surface_pressure_hpa: float
    wind_speed_10m_ms: float
    wind_direction_10m_deg: float
    weather_code: int
    weather_description: str
    observation_time: str
    data_freshness: str = "LIVE"
    source: str = "Open-Meteo Global Numerical Weather Prediction"

class SourceHealthStatus(BaseModel):
    source_id: str
    name: str
    status: str  # HEALTHY, DEGRADED, UNAVAILABLE
    endpoint: str
    requires_api_key: bool
    api_key_configured: bool
    last_checked: str
    last_success: Optional[str] = None
    response_time_ms: Optional[float] = None
    update_frequency: str

class LiveStatusResponse(BaseModel):
    system_status: str
    timestamp: str
    sources: List[SourceHealthStatus]
    cache_entries_active: int
    data_policy: str = "100% Authentic Scientific APIs & Feeds. No fabricated observations."

class GenericLiveFeedResponse(BaseModel):
    hazard_type: str
    total_records: int
    records_returned: int
    data_freshness: str
    retrieval_timestamp: str
    source_attribution: str
    data: List[Dict[str, Any]]

