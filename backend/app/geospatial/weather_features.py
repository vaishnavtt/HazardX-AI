"""
HAZARDX AI — Weather & Fire Weather Index Feature Extractor
Extracts multi-timescale meteorological features (current NWP + ERA5 reanalysis)
and computes the Canadian/McArthur Fire Weather Index (FWI).
"""

import math
from typing import Dict, Any
from ..integrations.weather_client import weather_client
from ..utils.logging_config import get_logger

logger = get_logger("weather_features")

class WeatherFeatureService:
    def __init__(self):
        pass

    async def get_comprehensive_weather_features(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Extracts real-time atmospheric measurements, antecedent precipitation sums,
        and computes empirical Fire Weather Index (FWI).
        """
        curr = await weather_client.get_current_weather(lat, lon)
        precip_hist = await weather_client.get_antecedent_precipitation_history(lat, lon, days_back=30)

        t_c = curr.temperature_2m_c
        rh_pct = curr.relative_humidity_pct
        w_ms = curr.wind_speed_10m_ms
        p_1d = precip_hist.get("precip_1d_mm", 0.0)
        p_7d = precip_hist.get("precip_7d_sum_mm", 0.0)
        p_30d = precip_hist.get("precip_30d_sum_mm", 0.0)

        # Compute empirical Canadian / McArthur Fire Weather Index (FWI)
        # Higher temperature, lower humidity, higher wind, and lower 30d rain -> higher FWI
        fwi = self._calculate_fire_weather_index(t_c, rh_pct, w_ms, p_7d, p_30d)

        return {
            "temp_2m_celsius": round(t_c, 1),
            "relative_humidity_pct": round(rh_pct, 1),
            "wind_speed_10m_ms": round(w_ms, 1),
            "surface_pressure_hpa": round(curr.surface_pressure_hpa, 1),
            "precip_1d_mm": round(p_1d, 1),
            "precip_3d_sum_mm": round(precip_hist.get("precip_3d_sum_mm", 0.0), 1),
            "precip_7d_sum_mm": round(p_7d, 1),
            "precip_14d_sum_mm": round(precip_hist.get("precip_14d_sum_mm", 0.0), 1),
            "precip_30d_sum_mm": round(p_30d, 1),
            "api_14d_index": round(precip_hist.get("api_14d_index", 0.0), 2),
            "api_30d_index": round(precip_hist.get("api_30d_index", 0.0), 2),
            "soil_temp_celsius": round(precip_hist.get("soil_temp_celsius", t_c - 2.0), 1),
            "fwi_fire_weather_index": round(fwi, 2),
            "weather_description": curr.weather_description
        }

    def _calculate_fire_weather_index(
        self, temp_c: float, rh_pct: float, wind_ms: float, precip_7d: float, precip_30d: float
    ) -> float:
        """
        Computes calibrated Fire Weather Index based on the McArthur Forest Fire Danger formulation.
        """
        # Drought factor based on 30-day precipitation deficit (scale 1.0 to 10.0)
        rain_deficit = max(0.0, 100.0 - precip_30d)
        drought_factor = min(10.0, max(1.0, 1.0 + (rain_deficit / 12.0) - (precip_7d / 15.0)))

        # Atmospheric fire danger index:
        # FWI = 2.0 * exp(-0.450 + 0.987*ln(DF) - 0.0345*RH + 0.0338*T + 0.0234*(V*3.6))
        wind_kmh = wind_ms * 3.6
        ln_df = math.log(max(1.0, drought_factor))

        exponent = -0.450 + (0.987 * ln_df) - (0.0345 * rh_pct) + (0.0338 * temp_c) + (0.0234 * wind_kmh)
        fwi = 2.0 * math.exp(max(-3.0, min(4.0, exponent)))

        return max(0.5, min(100.0, fwi))

weather_feature_service = WeatherFeatureService()

