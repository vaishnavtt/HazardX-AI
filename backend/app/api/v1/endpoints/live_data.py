"""
HAZARDX AI — Real-Time Disaster Intelligence Endpoints
Serves live and recent observational data from authentic scientific APIs
(USGS, NASA FIRMS, Open-Meteo, Copernicus GloFAS, NOAA NHC, NASA GLC).
"""

from typing import Optional
from fastapi import APIRouter, Query, HTTPException, status
from backend.app.schemas.external_data import (
    GenericLiveFeedResponse,
    LiveStatusResponse,
    LiveFloodObservation,
    CurrentWeatherObservation
)
from backend.app.services.external_data_service import external_data_service
from backend.app.utils.logging_config import get_logger

logger = get_logger("live_data_api")
router = APIRouter(prefix="/live", tags=["Real-Time Intelligence"])

@router.get("/earthquakes", response_model=GenericLiveFeedResponse)
async def get_live_earthquakes(
    min_magnitude: float = Query(2.5, ge=1.0, le=9.5, description="Minimum earthquake magnitude (M2.5+ default)"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of events to return")
) -> GenericLiveFeedResponse:
    """
    Retrieves authentic real-time earthquake observations from USGS ComCat (M2.5+).
    """
    try:
        return await external_data_service.get_live_earthquakes(min_magnitude=min_magnitude, limit=limit)
    except Exception as e:
        logger.error(f"Error serving live earthquakes: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/wildfires", response_model=GenericLiveFeedResponse)
async def get_live_wildfires(
    min_confidence: str = Query("nominal", pattern="^(low|nominal|high)$", description="Minimum thermal anomaly confidence"),
    limit: int = Query(100, ge=1, le=500, description="Maximum active fire hotspots to return")
) -> GenericLiveFeedResponse:
    """
    Retrieves authentic satellite active fire detections from NASA FIRMS (MODIS / VIIRS).
    """
    try:
        return await external_data_service.get_live_wildfires(min_confidence=min_confidence, limit=limit)
    except Exception as e:
        logger.error(f"Error serving live wildfires: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/cyclones", response_model=GenericLiveFeedResponse)
async def get_live_cyclones(
    limit: int = Query(50, ge=1, le=100, description="Maximum number of storms to return")
) -> GenericLiveFeedResponse:
    """
    Retrieves active tropical cyclone tracks from NOAA NHC and verified recent systems from NOAA IBTrACS.
    """
    try:
        return await external_data_service.get_live_cyclones(limit=limit)
    except Exception as e:
        logger.error(f"Error serving live cyclones: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/floods", response_model=LiveFloodObservation)
async def get_live_floods(
    lat: float = Query(..., ge=-90.0, le=90.0, description="Latitude of river reach"),
    lon: float = Query(..., ge=-180.0, le=180.0, description="Longitude of river reach"),
    location_name: str = Query("Target River Reach", description="Descriptive name of the monitoring reach")
) -> LiveFloodObservation:
    """
    Retrieves authentic river discharge and forecast anomaly from Copernicus GloFAS via Open-Meteo.
    """
    try:
        return await external_data_service.get_live_floods(lat=lat, lon=lon, location_name=location_name)
    except Exception as e:
        logger.error(f"Error serving flood observation: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/landslides", response_model=GenericLiveFeedResponse)
async def get_live_landslides(
    limit: int = Query(20, ge=1, le=50, description="Maximum monitoring corridors to return")
) -> GenericLiveFeedResponse:
    """
    Retrieves real-time landslide triggers across high-susceptibility global corridors (NASA GLC + ERA5 precip).
    """
    try:
        return await external_data_service.get_live_landslides(limit=limit)
    except Exception as e:
        logger.error(f"Error serving landslide observations: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/weather", response_model=CurrentWeatherObservation)
async def get_live_weather(
    lat: float = Query(..., ge=-90.0, le=90.0, description="Target latitude"),
    lon: float = Query(..., ge=-180.0, le=180.0, description="Target longitude")
) -> CurrentWeatherObservation:
    """
    Retrieves authentic current meteorological conditions from Open-Meteo Global NWP.
    """
    try:
        return await external_data_service.get_live_weather(lat=lat, lon=lon)
    except Exception as e:
        logger.error(f"Error serving weather: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/events", response_model=GenericLiveFeedResponse)
async def get_unified_events(
    hazard_type: Optional[str] = Query(None, description="Filter by hazard: floods, landslides, earthquakes, cyclones, wildfires"),
    min_lat: Optional[float] = Query(None, ge=-90.0, le=90.0),
    max_lat: Optional[float] = Query(None, ge=-90.0, le=90.0),
    min_lon: Optional[float] = Query(None, ge=-180.0, le=180.0),
    max_lon: Optional[float] = Query(None, ge=-180.0, le=180.0),
    limit: int = Query(100, ge=1, le=300)
) -> GenericLiveFeedResponse:
    """
    Retrieves unified live and recent multi-hazard events with bounding box and type filters.
    """
    try:
        return await external_data_service.get_unified_events(
            hazard_type=hazard_type,
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            limit=limit
        )
    except Exception as e:
        logger.error(f"Error serving unified events: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/status", response_model=LiveStatusResponse)
def get_sources_status() -> LiveStatusResponse:
    """
    Monitors data source health, latency, authentication status, and active cache entries.
    """
    try:
        return external_data_service.get_sources_status()
    except Exception as e:
        logger.error(f"Error serving sources status: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
