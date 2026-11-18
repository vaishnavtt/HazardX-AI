"""
HAZARDX AI — External Data Aggregation & Telemetry Service
Orchestrates real-time scientific data feeds, provides multi-hazard event filtering,
and monitors data source health and cache performance.
"""

import time
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from ..schemas.external_data import (
    LiveEarthquakeEvent,
    LiveWildfireEvent,
    LiveCycloneEvent,
    LiveFloodObservation,
    LiveLandslideObservation,
    CurrentWeatherObservation,
    SourceHealthStatus,
    LiveStatusResponse,
    GenericLiveFeedResponse
)
from ..integrations import (
    usgs_client,
    firms_client,
    weather_client,
    glofas_client,
    cyclone_client,
    landslide_client
)
from .data_storage_service import storage_service
from ..config import settings
from ..utils.logging_config import get_logger

logger = get_logger("external_data_service")

class ExternalDataService:
    def __init__(self):
        self.sources_catalog = [
            {
                "source_id": "usgs_earthquakes",
                "name": "USGS Earthquake Hazards Program (FDSNWS)",
                "endpoint": "https://earthquake.usgs.gov/fdsnws/event/1/",
                "requires_api_key": False,
                "api_key_configured": True,
                "update_frequency": "Every 1 to 5 minutes"
            },
            {
                "source_id": "nasa_firms",
                "name": "NASA FIRMS (MODIS / VIIRS Active Fire Detections)",
                "endpoint": "https://firms.modaps.eosdis.nasa.gov/api/area/",
                "requires_api_key": True,
                "api_key_configured": bool(settings.NASA_FIRMS_MAP_KEY),
                "update_frequency": "Every 15 minutes (NRT Open Streams)"
            },
            {
                "source_id": "open_meteo_weather",
                "name": "Open-Meteo Global NWP & ERA5 Weather Reanalysis",
                "endpoint": "https://api.open-meteo.com/v1/forecast",
                "requires_api_key": False,
                "api_key_configured": True,
                "update_frequency": "Hourly / Real-time"
            },
            {
                "source_id": "glofas_floods",
                "name": "Copernicus GloFAS River Discharge (Open-Meteo Flood)",
                "endpoint": "https://flood-api.open-meteo.com/v1/flood",
                "requires_api_key": False,
                "api_key_configured": True,
                "update_frequency": "Daily at 00:00 UTC"
            },
            {
                "source_id": "noaa_nhc_cyclones",
                "name": "NOAA National Hurricane Center (NHC) & IBTrACS",
                "endpoint": "https://www.nhc.noaa.gov/CurrentStorms.json",
                "requires_api_key": False,
                "api_key_configured": True,
                "update_frequency": "Every 3 hours / Live Advisory"
            },
            {
                "source_id": "nasa_glc_landslides",
                "name": "NASA Global Landslide Catalog & Hydrometeorological Triggers",
                "endpoint": "NASA GLC Archive & ERA5 Infiltration Stencil",
                "requires_api_key": False,
                "api_key_configured": True,
                "update_frequency": "Daily & Real-Time Stencil"
            }
        ]

    async def get_live_earthquakes(self, min_magnitude: float = 2.5, limit: int = 100) -> GenericLiveFeedResponse:
        events = await usgs_client.get_recent_earthquakes(min_magnitude=min_magnitude, limit=limit)
        return GenericLiveFeedResponse(
            hazard_type="earthquakes",
            total_records=len(events),
            records_returned=len(events),
            data_freshness="LIVE" if events and events[0].data_freshness == "LIVE" else "RECENT",
            retrieval_timestamp=datetime.now(timezone.utc).isoformat(),
            source_attribution="USGS Earthquake Hazards Program (FDSNWS ComCat)",
            data=[e.model_dump() for e in events]
        )

    async def get_live_wildfires(self, min_confidence: str = "nominal", limit: int = 100) -> GenericLiveFeedResponse:
        events = await firms_client.get_recent_fires(min_confidence=min_confidence, limit=limit)
        return GenericLiveFeedResponse(
            hazard_type="wildfires",
            total_records=len(events),
            records_returned=len(events),
            data_freshness="LIVE" if events and events[0].data_freshness == "LIVE" else "RECENT",
            retrieval_timestamp=datetime.now(timezone.utc).isoformat(),
            source_attribution="NASA FIRMS (MODIS / VIIRS Active Fire Detections)",
            data=[e.model_dump() for e in events]
        )

    async def get_live_cyclones(self, limit: int = 50) -> GenericLiveFeedResponse:
        events = await cyclone_client.get_active_cyclones(limit=limit)
        freshness = "LIVE" if events and any(e.data_freshness == "LIVE" for e in events) else "RECENT"
        return GenericLiveFeedResponse(
            hazard_type="cyclones",
            total_records=len(events),
            records_returned=len(events),
            data_freshness=freshness,
            retrieval_timestamp=datetime.now(timezone.utc).isoformat(),
            source_attribution="NOAA NHC & NOAA IBTrACS Official Tropical Archives",
            data=[e.model_dump() for e in events]
        )

    async def get_live_floods(self, lat: float, lon: float, location_name: str = "Target River Reach") -> LiveFloodObservation:
        return await glofas_client.get_river_discharge(lat, lon, location_name=location_name)

    async def get_live_landslides(self, limit: int = 20) -> GenericLiveFeedResponse:
        events = await landslide_client.get_active_landslide_triggers(limit=limit)
        return GenericLiveFeedResponse(
            hazard_type="landslides",
            total_records=len(events),
            records_returned=len(events),
            data_freshness="LIVE",
            retrieval_timestamp=datetime.now(timezone.utc).isoformat(),
            source_attribution="NASA Global Landslide Catalog & Open-Meteo ERA5 / NWP Reanalysis",
            data=[e.model_dump() for e in events]
        )

    async def get_live_weather(self, lat: float, lon: float) -> CurrentWeatherObservation:
        return await weather_client.get_current_weather(lat, lon)

    async def get_unified_events(
        self,
        hazard_type: Optional[str] = None,
        min_lat: Optional[float] = None,
        max_lat: Optional[float] = None,
        min_lon: Optional[float] = None,
        max_lon: Optional[float] = None,
        limit: int = 150
    ) -> GenericLiveFeedResponse:
        """
        Retrieves unified multi-hazard live and recent observations across all 5 hazards.
        """
        # Ensure fresh data is populated
        cached_events = storage_service.query_live_events(
            hazard_type=hazard_type,
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            limit=limit
        )

        if not cached_events:
            # Trigger background pull for earthquakes, fires, and cyclones if database is fresh
            await usgs_client.get_recent_earthquakes(limit=40)
            await firms_client.get_recent_fires(limit=40)
            await cyclone_client.get_active_cyclones(limit=10)
            await landslide_client.get_active_landslide_triggers(limit=10)

            cached_events = storage_service.query_live_events(
                hazard_type=hazard_type,
                min_lat=min_lat,
                max_lat=max_lat,
                min_lon=min_lon,
                max_lon=max_lon,
                limit=limit
            )

        return GenericLiveFeedResponse(
            hazard_type=hazard_type or "all_multi_hazards",
            total_records=len(cached_events),
            records_returned=len(cached_events),
            data_freshness="LIVE",
            retrieval_timestamp=datetime.now(timezone.utc).isoformat(),
            source_attribution="HAZARDX AI Unified Multi-Hazard Telemetry Engine",
            data=cached_events
        )

    def get_sources_status(self) -> LiveStatusResponse:
        statuses: List[SourceHealthStatus] = []
        for src in self.sources_catalog:
            info = storage_service.get_source_health_summary(src["source_id"])
            statuses.append(SourceHealthStatus(
                source_id=src["source_id"],
                name=src["name"],
                status=info["status"],
                endpoint=src["endpoint"],
                requires_api_key=src["requires_api_key"],
                api_key_configured=src["api_key_configured"],
                last_checked=info["last_checked"],
                last_success=info["last_success"],
                response_time_ms=info["response_time_ms"],
                update_frequency=src["update_frequency"]
            ))

        cache_count = storage_service.get_active_cache_count()
        return LiveStatusResponse(
            system_status="OPERATIONAL",
            timestamp=datetime.now(timezone.utc).isoformat(),
            sources=statuses,
            cache_entries_active=cache_count,
            data_policy="100% Authentic Scientific APIs & Feeds. No fabricated observations."
        )

external_data_service = ExternalDataService()

