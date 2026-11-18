"""
HAZARDX AI — Hydrological & River Network Feature Extractor
Extracts Copernicus GloFAS river discharge, 7-day anomaly ratios,
and estimates proximity to fluvial channels.
"""

from typing import Dict, Any
from ..integrations.glofas_client import glofas_client
from ..utils.logging_config import get_logger

logger = get_logger("hydrology_features")

class HydrologyFeatureService:
    def __init__(self):
        pass

    async def get_hydrological_features(self, lat: float, lon: float, twi: float = 8.0) -> Dict[str, Any]:
        """
        Retrieves authentic river discharge metrics from Copernicus GloFAS
        and estimates channel proximity.
        """
        glofas_obs = await glofas_client.get_river_discharge(lat, lon)

        # Distance to river channel estimation using TWI (Topographic Wetness Index):
        # Valleys and floodplains (TWI > 10) are directly adjacent to channels (< 0.5 km)
        # Ridgetops and hillslopes (TWI < 6) are several kilometers from major channels.
        if twi >= 12.0:
            dist_river_km = 0.15
        elif twi >= 9.0:
            dist_river_km = 0.50 + (12.0 - twi) * 0.35
        elif twi >= 6.0:
            dist_river_km = 1.50 + (9.0 - twi) * 0.80
        else:
            dist_river_km = 4.00 + (6.0 - twi) * 1.50

        return {
            "river_discharge_m3s": glofas_obs.current_discharge_m3s,
            "river_discharge_7d_mean_m3s": glofas_obs.mean_discharge_7d_m3s,
            "river_discharge_ratio_7d": glofas_obs.discharge_anomaly_ratio,
            "distance_to_river_km": round(max(0.05, min(30.0, dist_river_km)), 2)
        }

hydrology_feature_service = HydrologyFeatureService()

