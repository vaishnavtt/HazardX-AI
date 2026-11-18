"""
HAZARDX AI — Ingestion Data Quality & Physical Sanity Validator
Enforces physical plausibility bounds on all incoming observational and numerical forecast data
to detect sensor failures, corrupted responses, and out-of-distribution values.
"""

from typing import Dict, Any, List, Tuple
from ..utils.logging_config import get_logger

logger = get_logger("data_validator")

# Physical reality bounds for scientific measurements
PHYSICAL_BOUNDS = {
    "temperature_celsius": (-70.0, 60.0),
    "relative_humidity_pct": (0.0, 100.0),
    "wind_speed_ms": (0.0, 150.0),
    "precipitation_mm": (0.0, 2000.0),
    "surface_pressure_hpa": (850.0, 1085.0),
    "river_discharge_m3s": (0.0, 350000.0),
    "earthquake_magnitude": (0.0, 10.0),
    "earthquake_depth_km": (-5.0, 800.0),
    "frp_mw": (0.0, 15000.0),
    "cyclone_wind_kt": (10.0, 220.0),
    "soil_moisture_m3m3": (0.0, 1.0)
}

class IngestionDataValidator:
    def __init__(self):
        pass

    def validate_coordinates(self, lat: float, lon: float) -> Tuple[bool, str]:
        if not (-90.0 <= lat <= 90.0):
            return False, f"Latitude {lat} out of range [-90, 90]"
        if not (-180.0 <= lon <= 180.0):
            return False, f"Longitude {lon} out of range [-180, 180]"
        return True, "Valid"

    def validate_measurement(self, param_name: str, value: float) -> Tuple[bool, str]:
        if param_name not in PHYSICAL_BOUNDS:
            return True, "No bounds registered"

        min_val, max_val = PHYSICAL_BOUNDS[param_name]
        if value < min_val or value > max_val:
            return False, f"Value {value} for {param_name} exceeds physical bounds [{min_val}, {max_val}]"
        return True, "Valid"

    def sanitize_weather_bundle(self, bundle: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates and clips extreme or corrupted meteorological values to physical bounds.
        """
        cleaned = dict(bundle)
        if "temperature_2m_c" in cleaned:
            cleaned["temperature_2m_c"] = max(-60.0, min(58.0, float(cleaned["temperature_2m_c"])))
        if "relative_humidity_pct" in cleaned:
            cleaned["relative_humidity_pct"] = max(1.0, min(100.0, float(cleaned["relative_humidity_pct"])))
        if "wind_speed_10m_ms" in cleaned:
            cleaned["wind_speed_10m_ms"] = max(0.0, min(120.0, float(cleaned["wind_speed_10m_ms"])))
        if "precipitation_mm" in cleaned:
            cleaned["precipitation_mm"] = max(0.0, float(cleaned["precipitation_mm"]))
        return cleaned

data_validator = IngestionDataValidator()

