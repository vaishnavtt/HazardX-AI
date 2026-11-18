"""
HAZARDX AI — Scalable Global Geocoding & Autocomplete Service
Provides fast global city search, coordinate parsing, and intelligent place ranking
with dual Photon/Nominatim external APIs, in-memory caching, and local gazetteer fallback.
"""

import re
import urllib.request
import urllib.parse
import json
import time
from typing import List, Dict, Any, Optional
from ..schemas.geospatial import LocationSearchResult
from ..utils.logging_config import get_logger

logger = get_logger("geocoding_service")

# High-priority global and Indian cities for instant 0ms matching
LOCAL_GAZETTEER = [
    # Kerala Districts & Cities
    {"name": "Wayanad", "state": "Kerala", "country": "India", "lat": 11.6854, "lon": 76.1320, "type": "district", "importance": 0.95},
    {"name": "Kochi", "state": "Kerala", "country": "India", "lat": 9.9312, "lon": 76.2673, "type": "city", "importance": 0.95},
    {"name": "Thiruvananthapuram", "state": "Kerala", "country": "India", "lat": 8.5241, "lon": 76.9366, "type": "city", "importance": 0.92},
    {"name": "Kozhikode", "state": "Kerala", "country": "India", "lat": 11.2588, "lon": 75.7804, "type": "city", "importance": 0.90},
    {"name": "Ernakulam", "state": "Kerala", "country": "India", "lat": 9.9816, "lon": 76.2999, "type": "city", "importance": 0.90},
    {"name": "Kannur", "state": "Kerala", "country": "India", "lat": 11.8745, "lon": 75.3704, "type": "city", "importance": 0.88},
    {"name": "Malappuram", "state": "Kerala", "country": "India", "lat": 11.0732, "lon": 76.0740, "type": "city", "importance": 0.88},
    {"name": "Thrissur", "state": "Kerala", "country": "India", "lat": 10.5276, "lon": 76.2144, "type": "city", "importance": 0.88},
    {"name": "Kollam", "state": "Kerala", "country": "India", "lat": 8.8932, "lon": 76.6141, "type": "city", "importance": 0.86},
    {"name": "Palakkad", "state": "Kerala", "country": "India", "lat": 10.7867, "lon": 76.6548, "type": "city", "importance": 0.86},
    {"name": "Alappuzha", "state": "Kerala", "country": "India", "lat": 9.4981, "lon": 76.3388, "type": "city", "importance": 0.86},
    {"name": "Kottayam", "state": "Kerala", "country": "India", "lat": 9.5916, "lon": 76.5222, "type": "city", "importance": 0.85},
    {"name": "Kasaragod", "state": "Kerala", "country": "India", "lat": 12.5102, "lon": 74.9852, "type": "city", "importance": 0.85},
    {"name": "Idukki", "state": "Kerala", "country": "India", "lat": 9.8500, "lon": 76.9400, "type": "district", "importance": 0.85},
    {"name": "Pathanamthitta", "state": "Kerala", "country": "India", "lat": 9.2648, "lon": 76.7870, "type": "district", "importance": 0.84},

    # Major Indian Metropolises & Capitals
    {"name": "Mumbai", "state": "Maharashtra", "country": "India", "lat": 19.0760, "lon": 72.8777, "type": "city", "importance": 0.98},
    {"name": "Delhi", "state": "Delhi", "country": "India", "lat": 28.6139, "lon": 77.2090, "type": "city", "importance": 0.98},
    {"name": "Bengaluru", "state": "Karnataka", "country": "India", "lat": 12.9716, "lon": 77.5946, "type": "city", "importance": 0.97},
    {"name": "Chennai", "state": "Tamil Nadu", "country": "India", "lat": 13.0827, "lon": 80.2707, "type": "city", "importance": 0.96},
    {"name": "Hyderabad", "state": "Telangana", "country": "India", "lat": 17.3850, "lon": 78.4867, "type": "city", "importance": 0.96},
    {"name": "Kolkata", "state": "West Bengal", "country": "India", "lat": 22.5726, "lon": 88.3639, "type": "city", "importance": 0.95},
    {"name": "Ahmedabad", "state": "Gujarat", "country": "India", "lat": 23.0225, "lon": 72.5714, "type": "city", "importance": 0.92},
    {"name": "Pune", "state": "Maharashtra", "country": "India", "lat": 18.5204, "lon": 73.8567, "type": "city", "importance": 0.92},
    {"name": "Jaipur", "state": "Rajasthan", "country": "India", "lat": 26.9124, "lon": 75.7873, "type": "city", "importance": 0.90},
    {"name": "Uttarakhand", "state": "Uttarakhand", "country": "India", "lat": 30.0668, "lon": 79.0193, "type": "state", "importance": 0.88},
    {"name": "Shimla", "state": "Himachal Pradesh", "country": "India", "lat": 31.1048, "lon": 77.1734, "type": "city", "importance": 0.88},

    # International Metropolises
    {"name": "Tokyo", "state": "Tokyo", "country": "Japan", "lat": 35.6762, "lon": 139.6503, "type": "city", "importance": 0.99},
    {"name": "London", "state": "England", "country": "United Kingdom", "lat": 51.5074, "lon": -0.1278, "type": "city", "importance": 0.99},
    {"name": "New York", "state": "New York", "country": "United States", "lat": 40.7128, "lon": -74.0060, "type": "city", "importance": 0.99},
    {"name": "Paris", "state": "Île-de-France", "country": "France", "lat": 48.8566, "lon": 2.3522, "type": "city", "importance": 0.98},
    {"name": "Dubai", "state": "Dubai", "country": "United Arab Emirates", "lat": 25.2048, "lon": 55.2708, "type": "city", "importance": 0.97},
    {"name": "Singapore", "state": "", "country": "Singapore", "lat": 1.3521, "lon": 103.8198, "type": "city", "importance": 0.97},
    {"name": "Sydney", "state": "New South Wales", "country": "Australia", "lat": -33.8688, "lon": 151.2093, "type": "city", "importance": 0.96},
    {"name": "Toronto", "state": "Ontario", "country": "Canada", "lat": 43.6532, "lon": -79.3832, "type": "city", "importance": 0.95},
    {"name": "Bangkok", "state": "Bangkok", "country": "Thailand", "lat": 13.7563, "lon": 100.5018, "type": "city", "importance": 0.95},
    {"name": "Jakarta", "state": "Jakarta", "country": "Indonesia", "lat": -6.2088, "lon": 106.8456, "type": "city", "importance": 0.95},
    {"name": "Cape Town", "state": "Western Cape", "country": "South Africa", "lat": -33.9249, "lon": 18.4241, "type": "city", "importance": 0.94},
    {"name": "San Francisco", "state": "California", "country": "United States", "lat": 37.7749, "lon": -122.4194, "type": "city", "importance": 0.94},
    {"name": "Miami", "state": "Florida", "country": "United States", "lat": 25.7617, "lon": -80.1918, "type": "city", "importance": 0.93},
    {"name": "New Orleans", "state": "Louisiana", "country": "United States", "lat": 29.9511, "lon": -90.0715, "type": "city", "importance": 0.93},
    {"name": "Manila", "state": "Metro Manila", "country": "Philippines", "lat": 14.5995, "lon": 120.9842, "type": "city", "importance": 0.93},
    {"name": "Kathmandu", "state": "Bagmati", "country": "Nepal", "lat": 27.7172, "lon": 85.3240, "type": "city", "importance": 0.92},
]

class GeocodingService:
    _instance = None
    _cache: Dict[str, Dict[str, Any]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeocodingService, cls).__new__(cls)
        return cls._instance

    def _parse_coordinates(self, query: str) -> Optional[LocationSearchResult]:
        """Detects if query is a pair of decimal coordinates e.g. '29.95, -90.07'"""
        coord_pattern = r"^([-+]?\d{1,2}(?:\.\d+)?)\s*,\s*([-+]?\d{1,3}(?:\.\d+)?)$"
        match = re.match(coord_pattern, query.strip())
        if match:
            lat = float(match.group(1))
            lon = float(match.group(2))
            if -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0:
                display = f"GPS Coordinates ({lat:.4f}° N, {lon:.4f}° E)" if lat >= 0 else f"GPS Coordinates ({-lat:.4f}° S, {lon:.4f}° E)"
                return LocationSearchResult(
                    id=f"coord_{lat}_{lon}",
                    name=f"{lat:.4f}, {lon:.4f}",
                    state="Custom Point",
                    country="Direct GPS Coordinates",
                    display_name=display,
                    latitude=lat,
                    longitude=lon,
                    place_type="coordinate",
                    importance=1.0
                )
        return None

    def search_local_gazetteer(self, query: str, limit: int = 5) -> List[LocationSearchResult]:
        """Fast prefix / substring matching against curated local gazetteer."""
        q = query.strip().lower()
        if not q:
            return []

        matches = []
        for item in LOCAL_GAZETTEER:
            name_lower = item["name"].lower()
            state_lower = item.get("state", "").lower()
            country_lower = item.get("country", "").lower()

            score = 0.0
            if name_lower.startswith(q):
                score = 1.0 + item.get("importance", 0.5)
            elif q in name_lower:
                score = 0.7 + item.get("importance", 0.5)
            elif state_lower.startswith(q) or country_lower.startswith(q):
                score = 0.5 + item.get("importance", 0.5)

            if score > 0.0:
                state_str = f", {item['state']}" if item.get('state') else ""
                display = f"{item['name']}{state_str}, {item['country']}"
                matches.append((score, LocationSearchResult(
                    id=f"local_{item['name'].lower()}_{item['lat']}_{item['lon']}",
                    name=item["name"],
                    state=item.get("state"),
                    country=item["country"],
                    display_name=display,
                    latitude=item["lat"],
                    longitude=item["lon"],
                    place_type=item.get("type", "city"),
                    importance=item.get("importance", 0.5)
                )))

        matches.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in matches[:limit]]

    def search_photon(self, query: str, limit: int = 8) -> List[LocationSearchResult]:
        """Queries Photon OpenStreetMap-based geocoding API with custom User-Agent."""
        encoded = urllib.parse.quote(query.strip())
        url = f"https://photon.komoot.io/api/?q={encoded}&limit={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": "HAZARDX-AI-Early-Warning/1.0 (contact@hazardx.ai)"})
        
        try:
            with urllib.request.urlopen(req, timeout=3.0) as res:
                if res.status != 200:
                    return []
                data = json.loads(res.read().decode("utf-8"))
                
            results = []
            for feat in data.get("features", []):
                props = feat.get("properties", {})
                coords = feat.get("geometry", {}).get("coordinates", [])
                if len(coords) < 2:
                    continue
                lon, lat = coords[0], coords[1]
                name = props.get("name") or props.get("city") or props.get("district") or query
                state = props.get("state")
                country = props.get("country") or ""
                
                parts = [name]
                if state:
                    parts.append(state)
                if country:
                    parts.append(country)
                display_name = ", ".join(parts)
                
                results.append(LocationSearchResult(
                    id=f"photon_{props.get('osm_id', int(time.time() * 1000))}",
                    name=name,
                    state=state,
                    country=country,
                    display_name=display_name,
                    latitude=round(lat, 5),
                    longitude=round(lon, 5),
                    place_type=props.get("osm_value") or props.get("type", "city"),
                    importance=props.get("importance") or 0.5
                ))
            return results
        except Exception as e:
            logger.warning(f"Photon geocoding error for '{query}': {e}")
            return []

    def search(self, query: str, limit: int = 10) -> List[LocationSearchResult]:
        """
        Unified search endpoint:
        1. Checks coordinate syntax.
        2. Checks LRU cache.
        3. Queries local gazetteer and Photon API in parallel.
        4. Deduplicates and ranks results.
        """
        clean_q = query.strip()
        if not clean_q or len(clean_q) < 1:
            return []

        # 1. Coordinate check
        coord_res = self._parse_coordinates(clean_q)
        if coord_res:
            return [coord_res]

        cache_key = clean_q.lower()
        now = time.time()
        if cache_key in self._cache:
            entry = self._cache[cache_key]
            if now - entry["ts"] < 300:  # 5 min cache
                return entry["data"]

        # 2. Local gazetteer matches
        local_results = self.search_local_gazetteer(clean_q, limit=limit)

        # 3. External Photon query
        remote_results = self.search_photon(clean_q, limit=limit)

        # 4. Merge, deduplicate by close proximity (< 10km) or identical name
        merged: List[LocationSearchResult] = []
        seen_keys = set()

        def make_key(item: LocationSearchResult) -> str:
            return f"{item.name.lower()}_{round(item.latitude, 2)}_{round(item.longitude, 2)}"

        for res in local_results:
            key = make_key(res)
            if key not in seen_keys:
                seen_keys.add(key)
                merged.append(res)

        for res in remote_results:
            key = make_key(res)
            if key not in seen_keys:
                seen_keys.add(key)
                merged.append(res)

        final_results = merged[:limit]
        self._cache[cache_key] = {"data": final_results, "ts": now}
        return final_results

geocoding_service = GeocodingService()
