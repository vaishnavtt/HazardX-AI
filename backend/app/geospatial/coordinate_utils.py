"""
HAZARDX AI — Geospatial Coordinate Utilities
Mathematical primitives for geodesic distance calculations, spherical-to-Cartesian conversions,
and spatial bounding box calculations.
"""

import math
from typing import Tuple, Dict, Any

EARTH_RADIUS_KM = 6371.0088

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two geographic coordinates using the Haversine formula.
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return EARTH_RADIUS_KM * c

def latlon_to_cartesian_km(lat: float, lon: float) -> Tuple[float, float, float]:
    """
    Converts spherical geographic coordinates (WGS84) to 3D geocentric Cartesian coordinates (X, Y, Z in km)
    for exact Euclidean nearest-neighbor searching (KD-Tree).
    """
    phi = math.radians(lat)
    lam = math.radians(lon)
    x = EARTH_RADIUS_KM * math.cos(phi) * math.cos(lam)
    y = EARTH_RADIUS_KM * math.cos(phi) * math.sin(lam)
    z = EARTH_RADIUS_KM * math.sin(phi)
    return (x, y, z)

def calculate_bounding_box(lat: float, lon: float, radius_km: float) -> Dict[str, float]:
    """
    Calculates latitude and longitude bounds enclosing a given radius.
    """
    lat_delta = math.degrees(radius_km / EARTH_RADIUS_KM)
    # Adjust lon delta by latitude
    cos_lat = math.cos(math.radians(lat))
    lon_delta = math.degrees(radius_km / (EARTH_RADIUS_KM * max(0.01, cos_lat)))

    return {
        "min_lat": max(-90.0, lat - lat_delta),
        "max_lat": min(90.0, lat + lat_delta),
        "min_lon": max(-180.0, lon - lon_delta),
        "max_lon": min(180.0, lon + lon_delta)
    }

def is_within_bbox(lat: float, lon: float, min_lat: float, max_lat: float, min_lon: float, max_lon: float) -> bool:
    return (min_lat <= lat <= max_lat) and (min_lon <= lon <= max_lon)

