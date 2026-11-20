"""
HAZARDX AI — Spatial Feature Engineering & Location Profiler Service
Synthesizes comprehensive environmental feature vectors for any target geographic coordinate
and formats them strictly according to each hazard model's training schema and unit requirements.
"""

import math
from typing import Dict, Any, Tuple, Optional
from ..schemas.geospatial import EnvironmentalContext
from ..schemas.flood import FloodFeatures
from ..schemas.landslide import LandslideFeatures
from ..schemas.earthquake import EarthquakeFeatures
from ..schemas.wildfire import WildfireFeatures
from ..schemas.cyclone import CycloneFeatures
from .terrain_features import terrain_service
from .weather_features import weather_feature_service
from .hydrology_features import hydrology_feature_service
from ..integrations.usgs_client import usgs_client
from ..utils.logging_config import get_logger

logger = get_logger("spatial_feature_service")

class SpatialFeatureService:
    def __init__(self):
        pass

    async def get_environmental_context(self, lat: float, lon: float) -> Tuple[EnvironmentalContext, Dict[str, Any]]:
        """
        Gathers terrain, fault, meteorological, and hydrological context from authentic sources.
        """
        terrain = await terrain_service.get_terrain_morphometry(lat, lon)
        dist_fault, slip_type = terrain_service.get_nearest_fault_info(lat, lon)
        weather = await weather_feature_service.get_comprehensive_weather_features(lat, lon)
        hydro = await hydrology_feature_service.get_hydrological_features(lat, lon, twi=terrain["topographic_wetness_index"])

        env_context = EnvironmentalContext(
            elevation_m=terrain["elevation_m"],
            slope_degrees=terrain["slope_degrees"],
            aspect_degrees=terrain["aspect_degrees"],
            plan_curvature=terrain["plan_curvature"],
            topographic_wetness_index=terrain["topographic_wetness_index"],
            dist_to_active_fault_km=dist_fault,
            nearest_fault_slip_type=slip_type,
            temp_2m_celsius=weather["temp_2m_celsius"],
            relative_humidity_pct=weather["relative_humidity_pct"],
            wind_speed_10m_ms=weather["wind_speed_10m_ms"],
            surface_pressure_hpa=weather["surface_pressure_hpa"],
            precip_1d_mm=weather["precip_1d_mm"],
            precip_30d_sum_mm=weather["precip_30d_sum_mm"],
            river_discharge_m3s=hydro["river_discharge_m3s"],
            fwi_fire_weather_index=weather["fwi_fire_weather_index"],
            weather_description=weather["weather_description"],
            data_freshness="LIVE"
        )

        raw_bundles = {
            "terrain": terrain,
            "fault": {"dist_to_active_fault_km": dist_fault, "slip_type": slip_type},
            "weather": weather,
            "hydrology": hydro
        }

        return env_context, raw_bundles

    def build_flood_features(self, env: EnvironmentalContext, raw: Dict[str, Any], overrides: Optional[Dict[str, Any]] = None) -> FloodFeatures:
        ov = overrides or {}
        w = raw.get("weather", {})
        h = raw.get("hydrology", {})

        p1 = float(ov.get("precip_1d_mm", env.precip_1d_mm))
        p3 = float(ov.get("precip_3d_sum_mm", w.get("precip_3d_sum_mm", p1 * 1.5)))
        p7 = float(ov.get("precip_7d_sum_mm", w.get("precip_7d_sum_mm", p3 * 1.8)))
        p14 = float(ov.get("precip_14d_sum_mm", w.get("precip_14d_sum_mm", p7 * 1.6)))
        api14 = float(ov.get("api_14d_index", w.get("api_14d_index", p1 * 0.8)))

        q = float(ov.get("river_discharge_m3s", env.river_discharge_m3s))
        q7 = float(h.get("river_discharge_7d_mean_m3s", q))
        q_ratio = q / max(0.1, q7)

        return FloodFeatures(
            precip_1d_mm=round(p1, 1),
            precip_3d_sum_mm=round(p3, 1),
            precip_7d_sum_mm=round(p7, 1),
            precip_14d_sum_mm=round(p14, 1),
            api_14d_index=round(api14, 2),
            temp_2m_celsius=env.temp_2m_celsius,
            soil_temp_celsius=float(w.get("soil_temp_celsius", env.temp_2m_celsius - 2.0)),
            river_discharge_m3s=round(q, 2),
            river_discharge_7d_mean_m3s=round(q7, 2),
            river_discharge_ratio_7d=round(q_ratio, 2),
            elevation_m=env.elevation_m,
            slope_degrees=env.slope_degrees,
            topographic_wetness_index=env.topographic_wetness_index,
            distance_to_river_km=float(h.get("distance_to_river_km", 1.0))
        )

    def build_landslide_features(self, env: EnvironmentalContext, raw: Dict[str, Any], overrides: Optional[Dict[str, Any]] = None) -> LandslideFeatures:
        ov = overrides or {}
        w = raw.get("weather", {})
        h = raw.get("hydrology", {})

        p1 = float(ov.get("precip_1d_mm", env.precip_1d_mm))
        p3 = float(ov.get("precip_3d_sum_mm", w.get("precip_3d_sum_mm", p1 * 1.5)))
        p7 = float(ov.get("precip_7d_sum_mm", w.get("precip_7d_sum_mm", p3 * 1.8)))
        p30 = float(ov.get("precip_30d_sum_mm", env.precip_30d_sum_mm))
        api30 = float(ov.get("api_30d_index", w.get("api_30d_index", p1 * 1.2)))

        return LandslideFeatures(
            precip_1d_mm=round(p1, 1),
            precip_3d_sum_mm=round(p3, 1),
            precip_7d_sum_mm=round(p7, 1),
            precip_30d_sum_mm=round(p30, 1),
            api_30d_index=round(api30, 2),
            temp_2m_celsius=env.temp_2m_celsius,
            soil_temp_celsius=float(w.get("soil_temp_celsius", env.temp_2m_celsius - 2.0)),
            slope_degrees=env.slope_degrees,
            elevation_m=env.elevation_m,
            aspect_degrees=env.aspect_degrees,
            plan_curvature=env.plan_curvature,
            soil_clay_fraction_pct=float(ov.get("soil_clay_fraction_pct", 28.5)),
            distance_to_road_km=float(ov.get("distance_to_road_km", 0.45)),
            distance_to_stream_km=float(h.get("distance_to_river_km", 0.65))
        )

    async def build_earthquake_features(
        self, lat: float, lon: float, env: EnvironmentalContext, raw: Dict[str, Any], overrides: Optional[Dict[str, Any]] = None
    ) -> EarthquakeFeatures:
        ov = overrides or {}
        
        # Real-time radial background seismicity from USGS (past 30 days within 100km)
        radial_events = await usgs_client.query_radial_earthquakes(lat, lon, radius_km=100.0, days_back=30, min_magnitude=2.0)
        
        count_30d = len(radial_events)
        now_ms = raw.get("timestamp_ms") or (1000 * 1700000000)
        past_7d_ms = 7 * 86400 * 1000
        count_7d = sum(1 for e in radial_events if e.get("time_ms", 0) >= (now_ms - past_7d_ms)) if radial_events else 0
        count_365d = count_30d * 12  # Annualized Poisson rate estimate

        mags = [e["mag"] for e in radial_events if e.get("mag")]
        prior_max_m = max(mags) if mags else 0.0

        # Cumulative seismic energy log10(Joules): log10(E) = 4.8 + 1.5 * M
        if mags:
            tot_energy = sum(10.0 ** (4.8 + 1.5 * m) for m in mags)
            cum_energy = math.log10(max(1.0, tot_energy))
        else:
            cum_energy = 0.0

        rate_7d = count_7d / 7.0
        rate_30d = max(0.01, count_30d / 30.0) if count_30d > 0 else 0.0
        accel_ratio = (rate_7d / rate_30d) if rate_30d > 0 else 1.0

        # Strict physical gating: Only evaluate mainshock if explicitly passed in scenario overrides
        # or if an actual qualifying M >= 4.0 mainshock occurred in radial USGS monitoring
        if "mainshock_mag" in ov:
            main_m = float(ov["mainshock_mag"])
            depth = float(ov.get("focal_depth_km", 10.0))
        elif mags and max(mags) >= 4.0:
            main_m = float(max(mags))
            depth = float(radial_events[0].get("depth_km", 10.0))
        else:
            main_m = 0.0
            depth = 0.0

        return EarthquakeFeatures(
            mainshock_mag=main_m,
            focal_depth_km=depth,
            dist_to_active_fault_km=env.dist_to_active_fault_km,
            nearest_fault_slip_type=env.nearest_fault_slip_type,
            prior_count_7d_100km=int(count_7d),
            prior_count_30d_100km=int(count_30d),
            prior_count_365d_100km=int(count_365d),
            prior_max_mag_30d=round(prior_max_m, 2),
            cumulative_energy_log_joules=round(cum_energy, 2),
            seismic_rate_accel_ratio=round(accel_ratio, 2),
            regional_b_value=1.02
        )

    def build_wildfire_features(self, env: EnvironmentalContext, raw: Dict[str, Any], overrides: Optional[Dict[str, Any]] = None) -> WildfireFeatures:
        ov = overrides or {}
        w = raw.get("weather", {})

        return WildfireFeatures(
            temp_2m_celsius=env.temp_2m_celsius,
            relative_humidity_pct=env.relative_humidity_pct,
            wind_speed_10m_ms=env.wind_speed_10m_ms,
            precip_7d_sum_mm=float(w.get("precip_7d_sum_mm", 0.0)),
            precip_30d_sum_mm=env.precip_30d_sum_mm,
            soil_temp_celsius=float(w.get("soil_temp_celsius", env.temp_2m_celsius - 2.0)),
            fwi_fire_weather_index=env.fwi_fire_weather_index,
            slope_degrees=env.slope_degrees,
            elevation_m=env.elevation_m,
            distance_to_road_km=float(ov.get("distance_to_road_km", 0.50))
        )

    def build_cyclone_features(self, lat: float, lon: float, env: EnvironmentalContext, raw: Dict[str, Any], overrides: Optional[Dict[str, Any]] = None) -> CycloneFeatures:
        ov = overrides or {}
        # Coriolis parameter f = 2 * Omega * sin(lat)
        omega = 7.2921159e-5
        f_coriolis = 2.0 * omega * math.sin(math.radians(lat))

        if "current_wind_kt" in ov:
            wind = float(ov["current_wind_kt"])
            pres = float(ov.get("current_pres_hpa", 996.0))
            dist_land = float(ov.get("dist_to_land_km", 85.0))
            speed = float(ov.get("translational_speed_kt", 11.5))
            head = float(ov.get("heading_degrees", 315.0))
        else:
            # Derive local wind from NWP 10m wind speed: 1 m/s = 1.94384 kt
            local_wind_kt = round(env.wind_speed_10m_ms * 1.94384, 1)
            wind = max(0.0, local_wind_kt)
            pres = 1013.25
            dist_land = 100.0
            speed = 10.0
            head = 315.0

        return CycloneFeatures(
            current_wind_kt=wind,
            current_pres_hpa=pres,
            dist_to_land_km=dist_land,
            landfall_flag=int(dist_land <= 10.0),
            past_delta_wind_6h=float(ov.get("past_delta_wind_6h", 0.0)),
            past_delta_wind_12h=float(ov.get("past_delta_wind_12h", 0.0)),
            past_delta_pres_6h=float(ov.get("past_delta_pres_6h", 0.0)),
            translational_speed_kt=speed,
            heading_degrees=head,
            coriolis_param=round(f_coriolis, 7),
            pot_intensity_headroom=float(ov.get("pot_intensity_headroom", max(0.0, 150.0 - wind)))
        )

spatial_feature_service = SpatialFeatureService()
