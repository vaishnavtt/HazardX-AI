"""
HAZARDX AI — USGS Earthquake API Integration Client
Retrieves authentic, real-time seismic event feeds and historical queries from
the USGS Earthquake Hazards Program (FDSNWS Event Web Service).
"""

import time
import httpx
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from ..schemas.external_data import LiveEarthquakeEvent
from ..services.data_storage_service import storage_service
from ..utils.logging_config import get_logger

logger = get_logger("usgs_client")

USGS_FEED_M25_DAY = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"
USGS_FEED_M45_WEEK = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson"
USGS_QUERY_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

class USGSClient:
    def __init__(self, timeout_sec: float = 12.0):
        self.timeout = timeout_sec
        self.headers = {"User-Agent": "HAZARDX-AI/1.0 (Disaster-Intelligence-Platform)"}

    async def get_recent_earthquakes(self, min_magnitude: float = 2.5, limit: int = 100) -> List[LiveEarthquakeEvent]:
        """
        Retrieves authentic real-time earthquakes from USGS GeoJSON feed past 24 hours.
        """
        cache_key = f"usgs_recent_m{min_magnitude}"
        cached = storage_service.get_cache(cache_key)
        if cached:
            logger.debug("Returning cached USGS earthquake events")
            return [LiveEarthquakeEvent(**e) for e in cached[:limit]]

        feed_url = USGS_FEED_M25_DAY if min_magnitude <= 3.0 else USGS_FEED_M45_WEEK
        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.get(feed_url, headers=self.headers)
                latency_ms = (time.time() - t0) * 1000

                if r.status_code == 200:
                    data = r.json()
                    features = data.get("features", [])
                    events: List[LiveEarthquakeEvent] = []

                    for feat in features:
                        props = feat.get("properties", {})
                        geom = feat.get("geometry", {})
                        coords = geom.get("coordinates", [0, 0, 0])
                        mag = float(props.get("mag") or 0.0)

                        if mag < min_magnitude:
                            continue

                        # Milliseconds to ISO 8601 UTC string
                        time_ms = props.get("time", 0)
                        event_time = datetime.fromtimestamp(time_ms / 1000.0, timezone.utc).isoformat()

                        ev = LiveEarthquakeEvent(
                            id=f"usgs_{feat.get('id', '')}",
                            title=props.get("title", f"M {mag:.1f} Earthquake"),
                            magnitude=round(mag, 2),
                            depth_km=round(float(coords[2] if len(coords) > 2 else 10.0), 1),
                            latitude=round(float(coords[1]), 4),
                            longitude=round(float(coords[0]), 4),
                            event_time=event_time,
                            location=props.get("place") or "Unknown Region",
                            significance=props.get("sig"),
                            url=props.get("url"),
                            data_freshness="LIVE",
                            source="USGS Earthquake Hazards Program"
                        )
                        events.append(ev)

                    storage_service.log_api_call("usgs_earthquakes", 200, latency_ms, len(events))
                    # Cache for 3 minutes (USGS feeds update every 1-5 minutes)
                    events_dict = [e.model_dump() for e in events]
                    storage_service.set_cache(cache_key, feed_url, events_dict, ttl_seconds=180)

                    # Persist events to SQLite for historical tracking
                    storage_service.save_live_events([
                        {
                            "id": e.id,
                            "hazard_type": "earthquakes",
                            "title": e.title,
                            "lat": e.latitude,
                            "lon": e.longitude,
                            "event_time": e.event_time,
                            "severity": "RED" if e.magnitude >= 6.0 else "YELLOW" if e.magnitude >= 4.5 else "GREEN",
                            "primary_metric": f"M {e.magnitude} | Depth: {e.depth_km} km",
                            "source": e.source,
                            "magnitude": e.magnitude
                        }
                        for e in events
                    ])

                    return events[:limit]
                else:
                    storage_service.log_api_call("usgs_earthquakes", r.status_code, latency_ms, 0, f"HTTP {r.status_code}")
                    logger.warning(f"USGS feed returned HTTP {r.status_code}")
        except Exception as e:
            latency_ms = (time.time() - t0) * 1000
            storage_service.log_api_call("usgs_earthquakes", 500, latency_ms, 0, str(e))
            logger.error(f"Error querying USGS feed: {e}")

        # Fallback to persistent SQLite storage if network is unreachable
        persisted = storage_service.query_live_events(hazard_type="earthquakes", limit=limit)
        fallback_events = []
        for p in persisted:
            fallback_events.append(LiveEarthquakeEvent(
                id=p["id"],
                title=p["title"],
                magnitude=float(p.get("magnitude", 4.0)),
                depth_km=float(p.get("depth_km", 10.0)),
                latitude=float(p["lat"]),
                longitude=float(p["lon"]),
                event_time=p["event_time"],
                location=p.get("location", p["title"]),
                data_freshness="RECENT",
                source="USGS Earthquake Hazards Program (Persistent Cache)"
            ))
        return fallback_events

    async def query_radial_earthquakes(
        self,
        lat: float,
        lon: float,
        radius_km: float = 100.0,
        days_back: int = 30,
        min_magnitude: float = 2.0
    ) -> List[Dict[str, Any]]:
        """
        Queries USGS ComCat for earthquakes in a circular radius around a given point.
        Critical for Phase 7 location seismicity background rate calculation.
        """
        cache_key = f"usgs_radial_{lat:.2f}_{lon:.2f}_r{int(radius_km)}_d{days_back}"
        cached = storage_service.get_cache(cache_key)
        if cached:
            return cached

        endtime = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        start_ts = datetime.now(timezone.utc).timestamp() - (days_back * 86400)
        starttime = datetime.fromtimestamp(start_ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

        params = {
            "format": "geojson",
            "latitude": lat,
            "longitude": lon,
            "maxradiuskm": radius_km,
            "starttime": starttime,
            "endtime": endtime,
            "minmagnitude": min_magnitude,
            "limit": 500
        }

        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.get(USGS_QUERY_URL, params=params, headers=self.headers)
                latency_ms = (time.time() - t0) * 1000
                if r.status_code == 200:
                    data = r.json()
                    feats = data.get("features", [])
                    events = []
                    for f in feats:
                        p = f.get("properties", {})
                        g = f.get("geometry", {})
                        c = g.get("coordinates", [0, 0, 0])
                        events.append({
                            "id": f.get("id"),
                            "mag": float(p.get("mag") or 0.0),
                            "time_ms": p.get("time", 0),
                            "depth_km": float(c[2] if len(c) > 2 else 10.0),
                            "lat": float(c[1]),
                            "lon": float(c[0])
                        })
                    storage_service.set_cache(cache_key, USGS_QUERY_URL, events, ttl_seconds=600)
                    return events
        except Exception as e:
            logger.warning(f"Error querying radial USGS seismicity for ({lat}, {lon}): {e}")
        return []

usgs_client = USGSClient()

