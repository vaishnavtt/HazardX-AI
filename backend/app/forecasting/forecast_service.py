"""
HAZARDX AI — Multi-Hazard Forecasting & Predictive Risk Service
Synthesizes live NWP weather forecasts, GloFAS hydrological trajectories, terrain morphometry,
and calibrated XGBoost models to generate multi-horizon forecasts (6h, 12h, 24h, 48h, 72h).
"""

import time
import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple

from ..schemas.forecast import (
    ForecastHorizon,
    RiskCategory,
    DataProvenanceType,
    SingleHazardForecast,
    HazardForecastTimeline,
    HorizonForecastItem,
    MultiHazardLocationForecastResponse
)
from ..schemas.flood import FloodFeatures
from ..schemas.landslide import LandslideFeatures
from ..schemas.earthquake import EarthquakeFeatures
from ..schemas.wildfire import WildfireFeatures
from ..schemas.cyclone import CycloneFeatures

from ..services.flood_service import flood_service
from ..services.landslide_service import landslide_service
from ..services.earthquake_service import earthquake_service
from ..services.cyclone_service import cyclone_service
from ..services.wildfire_service import wildfire_service
from ..geospatial.spatial_feature_service import spatial_feature_service
from ..integrations.glofas_client import glofas_client
from ..integrations.weather_client import weather_client
from ..integrations.cyclone_client import cyclone_client
from ..integrations.usgs_client import usgs_client
from ..integrations.nasa_firms_client import nasa_firms_client
from .omori_aftershock_model import omori_model
from ..utils.logging_config import get_logger

logger = get_logger("forecast_service")

ALERT_SEVERITY_WEIGHTS = {
    "GREEN": 1,
    "YELLOW": 2,
    "ORANGE": 3,
    "RED": 4
}

class ForecastService:
    def __init__(self):
        pass

    def _determine_risk_category(self, score: float) -> RiskCategory:
        if score >= 0.80:
            return RiskCategory.EXTREME
        elif score >= 0.60:
            return RiskCategory.VERY_HIGH
        elif score >= 0.40:
            return RiskCategory.HIGH
        elif score >= 0.20:
            return RiskCategory.MODERATE
        return RiskCategory.LOW

    # =========================================================================
    # 1. FLOOD FORECASTING
    # =========================================================================
    async def forecast_flood(
        self, lat: float, lon: float, location_name: str = "Target River Reach"
    ) -> Tuple[SingleHazardForecast, HazardForecastTimeline]:
        """
        Forecasts flood occurrence, discharge anomaly, and reach severity over 6h, 12h, 24h, 48h, and 72h.
        """
        now = datetime.now(timezone.utc)
        now_str = now.isoformat()

        # Ingest GloFAS multi-day discharge and Open-Meteo multi-hour weather
        hydro_fc = await glofas_client.get_multiday_discharge_forecast(lat, lon, location_name)
        weather_fc = await weather_client.get_multihour_weather_forecast(lat, lon)
        env_context, raw_bundles = await spatial_feature_service.get_environmental_context(lat, lon)

        horizons_dict: Dict[str, HorizonForecastItem] = {}
        peak_score = 0.0
        peak_horizon = ForecastHorizon.H24

        horizons_order = [
            (ForecastHorizon.H6, 6, "6h"),
            (ForecastHorizon.H12, 12, "12h"),
            (ForecastHorizon.H24, 24, "24h"),
            (ForecastHorizon.H48, 48, "48h"),
            (ForecastHorizon.H72, 72, "72h")
        ]

        # Prior historical precipitation baseline
        p_prior_14d = float(env_context.precip_30d_sum_mm * 0.45)

        for f_enum, hours, h_key in horizons_order:
            h_weather = weather_fc["horizons"].get(h_key, {})
            h_hydro = hydro_fc["horizons"].get(h_key, {})

            q_val = float(h_hydro.get("discharge_m3s", hydro_fc["current_discharge_m3s"]))
            q_ratio = float(h_hydro.get("anomaly_ratio", 1.0))
            cum_p = float(h_weather.get("cum_precip_mm", 0.0))

            # Reconstruct FloodFeatures for this horizon
            p1 = cum_p if hours <= 24 else cum_p * (24.0 / hours)
            p3 = cum_p if hours <= 72 else cum_p * (72.0 / hours)
            p7 = p3 + env_context.precip_1d_mm * 2.0
            api14 = (p1 * 0.85) + (p_prior_14d * 0.15)

            feats = FloodFeatures(
                precip_1d_mm=round(p1, 1),
                precip_3d_sum_mm=round(p3, 1),
                precip_7d_sum_mm=round(p7, 1),
                precip_14d_sum_mm=round(p7 * 1.5, 1),
                api_14d_index=round(api14, 2),
                temp_2m_celsius=float(h_weather.get("max_temp_c", env_context.temp_2m_celsius)),
                soil_temp_celsius=float(h_weather.get("mean_soil_temp_c", env_context.temp_2m_celsius - 2.0)),
                river_discharge_m3s=round(q_val, 2),
                river_discharge_7d_mean_m3s=round(hydro_fc["mean_7d_m3s"], 2),
                river_discharge_ratio_7d=round(q_ratio, 2),
                elevation_m=env_context.elevation_m,
                slope_degrees=env_context.slope_degrees,
                topographic_wetness_index=env_context.topographic_wetness_index,
                distance_to_river_km=float(raw_bundles.get("hydrology", {}).get("distance_to_river_km", 1.0))
            )

            # Evaluate XGBoost Model
            f_pred = flood_service.predict(feats)
            score = round(f_pred.calibrated_susceptibility_score, 4)
            cat = self._determine_risk_category(score)

            if score > peak_score:
                peak_score = score
                peak_horizon = f_enum

            valid_until = (now + timedelta(hours=hours)).isoformat()

            horizons_dict[h_key] = HorizonForecastItem(
                horizon=f_enum,
                valid_from=now_str,
                valid_until=valid_until,
                risk_score=score,
                risk_category=cat,
                primary_metric_label="Forecast River Discharge",
                primary_metric_value=round(q_val, 1),
                primary_metric_unit="m³/s",
                contributing_factors=[
                    {"name": "Discharge Anomaly", "value": f"{q_ratio:.1f}x 7d normal"},
                    {"name": "Forecast Cumulative Rain", "value": f"{cum_p:.1f} mm"},
                    {"name": "Severity Class", "value": f_pred.severity_label}
                ],
                confidence_level="HIGH" if weather_fc["data_provenance"] == "LIVE_FORECAST" else "MODERATE",
                data_sources=["Copernicus GloFAS", "Open-Meteo ECMWF/GFS"],
                data_provenance=DataProvenanceType.LIVE_FORECAST
            )

        # Baseline 24h primary forecast
        h24_item = horizons_dict["24h"]
        single_fc = SingleHazardForecast(
            hazard_type="floods",
            geographic_location=location_name,
            latitude=lat,
            longitude=lon,
            forecast_generated_at=now_str,
            forecast_valid_from=now_str,
            forecast_valid_until=h24_item.valid_until,
            forecast_horizon=ForecastHorizon.H24,
            risk_score=h24_item.risk_score,
            risk_category=h24_item.risk_category,
            model_name="floods_flood_occurrence_xgboost",
            model_version="v1.0",
            model_status="OPERATIONAL",
            contributing_features={
                "discharge_m3s": h24_item.primary_metric_value,
                "discharge_anomaly_ratio": hydro_fc["horizons"]["24h"]["anomaly_ratio"],
                "forecast_precip_24h_mm": weather_fc["horizons"]["24h"]["cum_precip_mm"],
                "topographic_wetness_index": env_context.topographic_wetness_index
            },
            explanation=f"Flood risk in {location_name} over the next 24 hours is {h24_item.risk_category.value}. GloFAS discharge trajectory indicates {hydro_fc['trend'].lower()} flows at {h24_item.primary_metric_value} m³/s with {weather_fc['horizons']['24h']['cum_precip_mm']} mm rainfall accumulation.",
            confidence_or_uncertainty={"confidence": "High", "hydrologic_model": "GloFAS v4 Gridded Routing"},
            data_sources=["Copernicus GloFAS via Open-Meteo Flood API", "Open-Meteo Global NWP"],
            data_freshness="LIVE",
            data_provenance=DataProvenanceType.LIVE_FORECAST,
            warnings=["GloFAS is a continental gridded routing model; localized sub-grid levee breaches require ground-based gauge confirmation."] if h24_item.risk_score >= 0.6 else [],
            limitations=["Does not account for urban storm drain backflow.", "Assumes open river channels without ice-jam blockages."],
            secondary_metrics={"trend": hydro_fc["trend"], "peak_discharge_m3s": hydro_fc["peak_forecast_discharge_m3s"]}
        )

        timeline = HazardForecastTimeline(
            hazard_type="floods",
            geographic_location=location_name,
            latitude=lat,
            longitude=lon,
            generated_at=now_str,
            model_name="floods_flood_occurrence_xgboost",
            model_status="OPERATIONAL",
            horizons=horizons_dict,
            overall_trend=hydro_fc["trend"],
            peak_risk_horizon=peak_horizon,
            peak_risk_score=peak_score,
            disclaimer="Automated predictive early warning decision support. Not a statutory evacuation order."
        )

        return single_fc, timeline

    # =========================================================================
    # 2. LANDSLIDE FORECASTING
    # =========================================================================
    async def forecast_landslide(
        self, lat: float, lon: float, location_name: str = "Target Slope"
    ) -> Tuple[SingleHazardForecast, HazardForecastTimeline]:
        """
        Forecasts rainfall-triggered landslide susceptibility over 6h, 12h, 24h, 48h, and 72h.
        """
        now = datetime.now(timezone.utc)
        now_str = now.isoformat()

        weather_fc = await weather_client.get_multihour_weather_forecast(lat, lon)
        env_context, raw_bundles = await spatial_feature_service.get_environmental_context(lat, lon)
        terrain = raw_bundles.get("terrain", {})

        horizons_dict: Dict[str, HorizonForecastItem] = {}
        peak_score = 0.0
        peak_horizon = ForecastHorizon.H24

        horizons_order = [
            (ForecastHorizon.H6, 6, "6h"),
            (ForecastHorizon.H12, 12, "12h"),
            (ForecastHorizon.H24, 24, "24h"),
            (ForecastHorizon.H48, 48, "48h"),
            (ForecastHorizon.H72, 72, "72h")
        ]

        slope = env_context.slope_degrees
        p_hist_30d = float(env_context.precip_30d_sum_mm)

        for f_enum, hours, h_key in horizons_order:
            h_weather = weather_fc["horizons"].get(h_key, {})
            cum_p = float(h_weather.get("cum_precip_mm", 0.0))
            soil_m = float(h_weather.get("mean_soil_moisture_m3m3", 0.25))

            # Horizon-specific precipitation integration
            p1 = cum_p if hours <= 24 else cum_p * (24.0 / hours)
            p3 = cum_p if hours <= 72 else cum_p * (72.0 / hours)
            p7 = p3 + env_context.precip_1d_mm * 2.0
            p30 = p_hist_30d + cum_p
            api30 = (p1 * 0.90) + (p_hist_30d * 0.10)

            feats = LandslideFeatures(
                precip_1d_mm=round(p1, 1),
                precip_3d_sum_mm=round(p3, 1),
                precip_7d_sum_mm=round(p7, 1),
                precip_30d_sum_mm=round(p30, 1),
                api_30d_index=round(api30, 2),
                temp_2m_celsius=float(h_weather.get("max_temp_c", env_context.temp_2m_celsius)),
                soil_temp_celsius=float(h_weather.get("mean_soil_temp_c", env_context.temp_2m_celsius - 2.0)),
                slope_degrees=slope,
                elevation_m=env_context.elevation_m,
                aspect_degrees=float(terrain.get("aspect_degrees", 180.0)),
                plan_curvature=float(terrain.get("plan_curvature", 0.0)),
                soil_clay_fraction_pct=float(terrain.get("soil_clay_fraction_pct", 30.0)),
                distance_to_road_km=float(terrain.get("distance_to_road_km", 0.5)),
                distance_to_stream_km=float(terrain.get("distance_to_stream_km", 0.5))
            )

            # Evaluate XGBoost Landslide Occurrence
            ls_pred = landslide_service.predict(feats)
            base_score = ls_pred.calibrated_susceptibility_score

            # Soil moisture infiltration scaling factor
            # High soil moisture (> 0.38 m³/m³) on steep slopes (> 25 deg) boosts physical risk
            moisture_factor = min(1.35, max(0.85, 0.85 + (soil_m * 1.1))) if slope >= 20.0 else 0.80
            adj_score = round(min(0.99, base_score * moisture_factor), 4)

            cat = self._determine_risk_category(adj_score)
            if adj_score > peak_score:
                peak_score = adj_score
                peak_horizon = f_enum

            valid_until = (now + timedelta(hours=hours)).isoformat()

            horizons_dict[h_key] = HorizonForecastItem(
                horizon=f_enum,
                valid_from=now_str,
                valid_until=valid_until,
                risk_score=adj_score,
                risk_category=cat,
                primary_metric_label="Forecast Cumulative Rain",
                primary_metric_value=round(cum_p, 1),
                primary_metric_unit="mm",
                contributing_factors=[
                    {"name": "Slope Angle", "value": f"{slope:.1f}°"},
                    {"name": "Topsoil Moisture", "value": f"{soil_m:.3f} m³/m³"},
                    {"name": "Susceptibility Magnitude", "value": ls_pred.hazard_magnitude_label}
                ],
                confidence_level="HIGH" if slope >= 20.0 else "MODERATE",
                data_sources=["Open-Meteo ERA5 / NWP", "SRTM / Copernicus DEM"],
                data_provenance=DataProvenanceType.LIVE_FORECAST
            )

        h24_item = horizons_dict["24h"]
        single_fc = SingleHazardForecast(
            hazard_type="landslides",
            geographic_location=location_name,
            latitude=lat,
            longitude=lon,
            forecast_generated_at=now_str,
            forecast_valid_from=now_str,
            forecast_valid_until=h24_item.valid_until,
            forecast_horizon=ForecastHorizon.H24,
            risk_score=h24_item.risk_score,
            risk_category=h24_item.risk_category,
            model_name="landslides_landslide_occurrence_xgboost",
            model_version="v1.0",
            model_status="OPERATIONAL",
            contributing_features={
                "slope_degrees": slope,
                "cum_precip_24h_mm": weather_fc["horizons"]["24h"]["cum_precip_mm"],
                "soil_moisture_m3m3": weather_fc["horizons"]["24h"]["mean_soil_moisture_m3m3"],
                "elevation_m": env_context.elevation_m
            },
            explanation=f"Landslide susceptibility for {location_name} over next 24h is {h24_item.risk_category.value}. Slope angle is {slope:.1f}° with {weather_fc['horizons']['24h']['cum_precip_mm']} mm forecast rain and {weather_fc['horizons']['24h']['mean_soil_moisture_m3m3']} m³/m³ soil moisture.",
            confidence_or_uncertainty={"confidence": "Moderate to High", "trigger": "Rainfall Infiltration"},
            data_sources=["Open-Meteo Global NWP", "Copernicus DEM Morphometry"],
            data_freshness="LIVE",
            data_provenance=DataProvenanceType.LIVE_FORECAST,
            warnings=["Steep terrain with intense rainfall accumulation accelerates slope destabilization."] if h24_item.risk_score >= 0.6 else [],
            limitations=["NASA GLC catalog provides historical inventory only; forecast is driven by meteorological rain infiltration.", "Does not account for recent seismic fracturing without tectonic event coupling."],
            secondary_metrics={"slope": slope, "elevation_m": env_context.elevation_m}
        )

        timeline = HazardForecastTimeline(
            hazard_type="landslides",
            geographic_location=location_name,
            latitude=lat,
            longitude=lon,
            generated_at=now_str,
            model_name="landslides_landslide_occurrence_xgboost",
            model_status="OPERATIONAL",
            horizons=horizons_dict,
            overall_trend="INCREASING" if peak_horizon in [ForecastHorizon.H48, ForecastHorizon.H72] else "STABLE",
            peak_risk_horizon=peak_horizon,
            peak_risk_score=peak_score,
            disclaimer="Automated predictive early warning decision support. Not a statutory evacuation order."
        )

        return single_fc, timeline

    # =========================================================================
    # 3. WILDFIRE FORECASTING
    # =========================================================================
    async def forecast_wildfire(
        self, lat: float, lon: float, location_name: str = "Target Region"
    ) -> Tuple[SingleHazardForecast, HazardForecastTimeline]:
        """
        Forecasts wildfire ignition & spread susceptibility over 6h, 12h, 24h, 48h, and 72h.
        (Preserves BLOCKED status on fire duration model).
        """
        now = datetime.now(timezone.utc)
        now_str = now.isoformat()

        weather_fc = await weather_client.get_multihour_weather_forecast(lat, lon)
        env_context, raw_bundles = await spatial_feature_service.get_environmental_context(lat, lon)
        terrain = raw_bundles.get("terrain", {})

        active_fires = await nasa_firms_client.get_active_fires_near(lat, lon, radius_km=50.0)
        num_hotspots = len(active_fires)

        horizons_dict: Dict[str, HorizonForecastItem] = {}
        peak_score = 0.0
        peak_horizon = ForecastHorizon.H24

        horizons_order = [
            (ForecastHorizon.H6, 6, "6h"),
            (ForecastHorizon.H12, 12, "12h"),
            (ForecastHorizon.H24, 24, "24h"),
            (ForecastHorizon.H48, 48, "48h"),
            (ForecastHorizon.H72, 72, "72h")
        ]

        for f_enum, hours, h_key in horizons_order:
            h_weather = weather_fc["horizons"].get(h_key, {})
            max_t = float(h_weather.get("max_temp_c", 22.0))
            min_rh = float(h_weather.get("min_rh_pct", 50.0))
            max_w = float(h_weather.get("max_wind_speed_ms", 4.0))
            cum_p = float(h_weather.get("cum_precip_mm", 0.0))
            fwi_val = float(h_weather.get("fwi_score", 10.0))
            soil_t = float(h_weather.get("mean_soil_temp_c", max_t - 2.0))

            feats = WildfireFeatures(
                temp_2m_celsius=max_t,
                relative_humidity_pct=min_rh,
                wind_speed_10m_ms=max_w,
                precip_7d_sum_mm=round(cum_p + env_context.precip_1d_mm, 1),
                precip_30d_sum_mm=env_context.precip_30d_sum_mm,
                soil_temp_celsius=soil_t,
                fwi_fire_weather_index=fwi_val,
                slope_degrees=env_context.slope_degrees,
                elevation_m=env_context.elevation_m,
                distance_to_road_km=0.8
            )

            wf_pred = wildfire_service.predict(feats)
            score = round(wf_pred.calibrated_susceptibility_score, 4)
            cat = (
                RiskCategory.EXTREME if wf_pred.risk_category in ["EXTREME", "SEVERE_CRITICAL"] else
                RiskCategory.VERY_HIGH if wf_pred.risk_category == "VERY_HIGH" else
                RiskCategory.HIGH if wf_pred.risk_category == "HIGH" else
                RiskCategory.MODERATE if wf_pred.risk_category == "MODERATE" else
                RiskCategory.LOW
            )

            if score > peak_score:
                peak_score = score
                peak_horizon = f_enum

            valid_until = (now + timedelta(hours=hours)).isoformat()

            horizons_dict[h_key] = HorizonForecastItem(
                horizon=f_enum,
                valid_from=now_str,
                valid_until=valid_until,
                risk_score=score,
                risk_category=cat,
                primary_metric_label="Fire Weather Index (FWI)",
                primary_metric_value=round(fwi_val, 1),
                primary_metric_unit="FWI Index",
                contributing_factors=[
                    {"name": "Canadian FWI", "value": f"{fwi_val:.1f} ({wf_pred.risk_category})"},
                    {"name": "NASA FIRMS Hotspots", "value": f"{num_hotspots} detected within 50 km"},
                    {"name": "Max Temperature", "value": f"{max_t:.1f}°C"},
                    {"name": "Min Humidity", "value": f"{min_rh:.1f}%"},
                    {"name": "Peak Wind", "value": f"{max_w * 3.6:.1f} km/h"}
                ],
                confidence_level="HIGH" if weather_fc["data_provenance"] == "LIVE_FORECAST" else "MODERATE",
                data_sources=["Open-Meteo Global NWP (ECMWF/GFS)", "NASA FIRMS Active Fires"],
                data_provenance=DataProvenanceType.LIVE_FORECAST
            )

        h24_item = horizons_dict["24h"]
        single_fc = SingleHazardForecast(
            hazard_type="wildfires",
            geographic_location=location_name,
            latitude=lat,
            longitude=lon,
            forecast_generated_at=now_str,
            forecast_valid_from=now_str,
            forecast_valid_until=h24_item.valid_until,
            forecast_horizon=ForecastHorizon.H24,
            risk_score=h24_item.risk_score,
            risk_category=h24_item.risk_category,
            model_name="wildfires_wildfire_occurrence_xgboost",
            model_version="v1.0",
            model_status="OPERATIONAL",
            contributing_features={
                "fwi_score": weather_fc["horizons"]["24h"]["fwi_score"],
                "active_firms_hotspots_50km": num_hotspots,
                "max_temp_c": weather_fc["horizons"]["24h"]["max_temp_c"],
                "min_rh_pct": weather_fc["horizons"]["24h"]["min_rh_pct"],
                "max_wind_ms": weather_fc["horizons"]["24h"]["max_wind_speed_ms"]
            },
            explanation=f"Wildfire ignition susceptibility in {location_name} over next 24h is {h24_item.risk_category.value}. Canadian FWI is {weather_fc['horizons']['24h']['fwi_score']:.1f} ({h24_item.risk_category.value} danger) with {num_hotspots} active FIRMS satellite thermal anomalies within 50 km.",
            confidence_or_uncertainty={"confidence": "High", "model": "XGBoost Ignition Susceptibility + McArthur FWI"},
            data_sources=["Open-Meteo NWP Forecast", "NASA FIRMS Active Fire Validation"],
            data_freshness="LIVE",
            data_provenance=DataProvenanceType.LIVE_FORECAST,
            warnings=["High wind gusts and dry air elevate fire propagation potential."] if h24_item.risk_score >= 0.6 else [],
            limitations=[
                "NASA FIRMS provides satellite active thermal detections of EXISTING fires, not future ignitions.",
                "Fire duration model is STRICTLY BLOCKED from operational use (R² = -214.75; output suppressed)."
            ],
            secondary_metrics={"duration_days": None, "model_duration_governance": "BLOCKED"}
        )

        timeline = HazardForecastTimeline(
            hazard_type="wildfires",
            geographic_location=location_name,
            latitude=lat,
            longitude=lon,
            generated_at=now_str,
            model_name="wildfires_wildfire_occurrence_xgboost",
            model_status="OPERATIONAL",
            horizons=horizons_dict,
            overall_trend="INCREASING" if peak_horizon in [ForecastHorizon.H48, ForecastHorizon.H72] else "STABLE",
            peak_risk_horizon=peak_horizon,
            peak_risk_score=peak_score,
            disclaimer="Automated predictive early warning decision support. Not a statutory evacuation order."
        )

        return single_fc, timeline

    # =========================================================================
    # 4. EARTHQUAKE AFTERSHOCK FORECASTING
    # =========================================================================
    async def forecast_earthquake(
        self, lat: float, lon: float, location_name: str = "Regional Seismic Zone", mainshock_mag: Optional[float] = None
    ) -> Tuple[SingleHazardForecast, HazardForecastTimeline]:
        """
        Provides statistical aftershock decay forecasting (Omori-Utsu / Reasenberg-Jones)
        following recent seismic activity.
        (STRICT GOVERNANCE: Deterministic earthquake prediction is scientifically impossible and strictly forbidden).
        """
        now = datetime.now(timezone.utc)
        now_str = now.isoformat()

        # Ingest recent seismic events to find nearest significant mainshock
        recent_eqs = await usgs_client.get_recent_earthquakes(min_magnitude=3.5, limit=50)
        nearest_mag: Optional[float] = mainshock_mag
        elapsed_hours = 2.0
        nearest_dist_km: Optional[float] = None

        if not mainshock_mag and recent_eqs:
            for eq in recent_eqs:
                dist = math.sqrt((eq.latitude - lat)**2 + (eq.longitude - lon)**2) * 111.0
                if dist <= 250.0 and eq.magnitude >= 4.0:
                    if nearest_mag is None or eq.magnitude > nearest_mag:
                        nearest_mag = eq.magnitude
                        nearest_dist_km = dist
                        try:
                            eq_dt = datetime.fromisoformat(eq.event_time.replace("Z", "+00:00"))
                            elapsed_hours = max(0.5, (now - eq_dt).total_seconds() / 3600.0)
                        except Exception:
                            elapsed_hours = 2.0

        has_mainshock = nearest_mag is not None and nearest_mag >= 4.0

        # Calculate Omori-Utsu statistical decay across horizons if mainshock occurred
        if has_mainshock:
            omori_res = omori_model.forecast_horizons(nearest_mag, elapsed_hours, distance_km=nearest_dist_km or 0.0)
        else:
            omori_res = {
                h: {"prob_m4_plus": 0.0, "prob_m5_plus": 0.0, "expected_m4_count": 0.0}
                for h in ["6h", "12h", "24h", "48h", "72h"]
            }

        horizons_dict: Dict[str, HorizonForecastItem] = {}
        peak_score = 0.0
        peak_horizon = ForecastHorizon.H6

        horizons_order = [
            (ForecastHorizon.H6, 6, "6h"),
            (ForecastHorizon.H12, 12, "12h"),
            (ForecastHorizon.H24, 24, "24h"),
            (ForecastHorizon.H48, 48, "48h"),
            (ForecastHorizon.H72, 72, "72h")
        ]

        for f_enum, hours, h_key in horizons_order:
            h_data = omori_res.get(h_key, {})
            score = float(h_data.get("prob_m4_plus", 0.0))
            cat = self._determine_risk_category(score)

            if score > peak_score:
                peak_score = score
                peak_horizon = f_enum

            valid_until = (now + timedelta(hours=hours)).isoformat()

            factors = [
                {"name": "Reference Mainshock", "value": f"M {nearest_mag:.1f}" if has_mainshock else "None detected (Quiescent)"},
                {"name": "P(M >= 4.0 Aftershock)", "value": f"{score * 100.0:.1f}%"},
                {"name": "Expected M4+ Count", "value": f"{h_data.get('expected_m4_count', 0.0):.2f}"}
            ]
            if not has_mainshock:
                factors.append({"name": "Seismic Status", "value": "No M4.0+ events within 250 km"})

            horizons_dict[h_key] = HorizonForecastItem(
                horizon=f_enum,
                valid_from=now_str,
                valid_until=valid_until,
                risk_score=score,
                risk_category=cat,
                primary_metric_label="P(M >= 4.0 Aftershock)",
                primary_metric_value=round(score * 100.0, 1),
                primary_metric_unit="%",
                contributing_factors=factors,
                confidence_level="STATISTICAL_ESTIMATE",
                data_sources=["USGS ComCat", "Omori-Utsu / Reasenberg-Jones Formulation"],
                data_provenance=DataProvenanceType.MODEL_INFERENCE
            )

        h24_item = horizons_dict["24h"]
        explanation_text = (
            f"Probabilistic aftershock hazard in {location_name} over next 24h is {h24_item.risk_category.value} ({h24_item.risk_score * 100:.1f}% chance of M4.0+ event). Calculated following M {nearest_mag:.1f} seismic event via Omori-Utsu temporal decay."
            if has_mainshock else
            f"Probabilistic aftershock hazard in {location_name} over next 24h is QUIESCENT (0.0% chance of M4.0+ event). No significant seismic mainshock (M >= 4.0) has occurred within 250 km."
        )

        single_fc = SingleHazardForecast(
            hazard_type="earthquakes",
            geographic_location=location_name,
            latitude=lat,
            longitude=lon,
            forecast_generated_at=now_str,
            forecast_valid_from=now_str,
            forecast_valid_until=h24_item.valid_until,
            forecast_horizon=ForecastHorizon.H24,
            risk_score=h24_item.risk_score,
            risk_category=h24_item.risk_category,
            model_name="omori_utsu_aftershock_statistical_decay",
            model_version="v1.0",
            model_status="STATISTICAL_MODEL",
            contributing_features={
                "reference_mainshock_mag": nearest_mag if has_mainshock else 0.0,
                "elapsed_hours_since_mainshock": round(elapsed_hours, 1) if has_mainshock else 0.0,
                "omori_decay_rate_p": 1.05,
                "gutenberg_richter_b": 1.00
            },
            explanation=explanation_text,
            confidence_or_uncertainty={"confidence": "Statistical Law (Empirical)", "decay_model": "Reasenberg-Jones 1989"},
            data_sources=["USGS Earthquake Hazards Program FDSNWS"],
            data_freshness="LIVE",
            data_provenance=DataProvenanceType.MODEL_INFERENCE,
            warnings=["Aftershocks decay with time (t^-p) but can occasionally trigger secondary high-consequence shaking."] if (nearest_mag and nearest_mag >= 5.5) else [],
            limitations=[
                "SCIENTIFIC NOTICE: Exact earthquake prediction (time, exact location, magnitude) is scientifically impossible.",
                "This output represents statistical aftershock decay probability following a known mainshock.",
                "Aftershock count regression model is STRICTLY BLOCKED (R² = -0.0401; suppressed)."
            ],
            secondary_metrics={"aftershock_count": None, "model_count_governance": "BLOCKED"}
        )

        timeline = HazardForecastTimeline(
            hazard_type="earthquakes",
            geographic_location=location_name,
            latitude=lat,
            longitude=lon,
            generated_at=now_str,
            model_name="omori_utsu_aftershock_statistical_decay",
            model_status="STATISTICAL_MODEL",
            horizons=horizons_dict,
            overall_trend="DECREASING",  # Omori decay is monotonically decreasing
            peak_risk_horizon=ForecastHorizon.H6,
            peak_risk_score=horizons_dict["6h"].risk_score,
            disclaimer="Probabilistic aftershock assessment following mainshock. NOT an exact earthquake prediction."
        )

        return single_fc, timeline

    # =========================================================================
    # 5. CYCLONE FORECASTING
    # =========================================================================
    async def forecast_cyclone(
        self, lat: float, lon: float, location_name: str = "Maritime Basin", storm_id: Optional[str] = None
    ) -> Tuple[SingleHazardForecast, HazardForecastTimeline]:
        """
        Forecasts tropical cyclone 24h intensity changes, rapid intensification (RI),
        and track proximity over 6h, 12h, 24h, 48h, and 72h.
        """
        now = datetime.now(timezone.utc)
        now_str = now.isoformat()

        cyclones = await cyclone_client.get_active_cyclones(limit=10)
        selected_storm = None
        min_dist_km = 99999.0
        if cyclones:
            for c in cyclones:
                d = math.sqrt((c.latitude - lat)**2 + (c.longitude - lon)**2) * 111.0
                if storm_id and (c.id == storm_id or c.name.lower() == storm_id.lower()):
                    selected_storm = c
                    min_dist_km = d
                    break
                if d <= 800.0 and d < min_dist_km:
                    min_dist_km = d
                    selected_storm = c

        env_context, _ = await spatial_feature_service.get_environmental_context(lat, lon)
        # Cyclone threat is physically governed by active storm proximity (radius <= 1000 km)
        # and synoptic wind fields, without an artificial elevation cutoff.
        has_active_threat = (selected_storm is not None) and (min_dist_km <= 1000.0)

        curr_wind = float(selected_storm.intensity_kt) if (has_active_threat and selected_storm) else 0.0
        storm_name = selected_storm.name if (has_active_threat and selected_storm) else "None (No Active Cyclone)"
        provenance = (
            DataProvenanceType.LIVE_OBSERVATION
            if (has_active_threat and selected_storm and selected_storm.data_freshness == "LIVE")
            else DataProvenanceType.MODEL_INFERENCE
        )

        omega = 7.2921159e-5
        f_coriolis = 2.0 * omega * math.sin(math.radians(lat))

        if has_active_threat and selected_storm:
            feats_24h = CycloneFeatures(
                current_wind_kt=curr_wind,
                current_pres_hpa=float(selected_storm.min_pressure_hpa or 995.0),
                dist_to_land_km=min_dist_km,
                landfall_flag=1 if min_dist_km <= 50.0 else 0,
                past_delta_wind_6h=5.0,
                past_delta_wind_12h=10.0,
                past_delta_pres_6h=-4.0,
                translational_speed_kt=float(selected_storm.speed_kt or 12.0),
                heading_degrees=float(selected_storm.heading_deg or 315.0),
                coriolis_param=round(f_coriolis, 7),
                pot_intensity_headroom=max(0.0, 150.0 - curr_wind)
            )
            cy_pred = cyclone_service.predict(feats_24h)
            ri_prob_base = cy_pred.rapid_intensification_probability
            pred_delta_v = cy_pred.predicted_24h_intensity_change_kt
        else:
            ri_prob_base = 0.0
            pred_delta_v = 0.0

        horizons_order = [
            (ForecastHorizon.H6, 6, "6h", 0.25),
            (ForecastHorizon.H12, 12, "12h", 0.50),
            (ForecastHorizon.H24, 24, "24h", 1.00),
            (ForecastHorizon.H48, 48, "48h", 1.80),
            (ForecastHorizon.H72, 72, "72h", 2.20)
        ]

        horizons_dict: Dict[str, HorizonForecastItem] = {}
        peak_score = 0.0
        peak_horizon = ForecastHorizon.H24

        for f_enum, hours, h_key, scale in horizons_order:
            if has_active_threat:
                fc_wind = round(max(20.0, min(185.0, curr_wind + (pred_delta_v * scale))), 1)
                ri_prob = round(min(0.99, ri_prob_base * scale), 4)

                # Saffir-Simpson risk score mapping
                score = (
                    0.95 if fc_wind >= 137.0 else # Cat 5
                    0.85 if fc_wind >= 113.0 else # Cat 4
                    0.70 if fc_wind >= 96.0 else  # Cat 3
                    0.50 if fc_wind >= 64.0 else  # Cat 1-2
                    0.30 if fc_wind >= 34.0 else  # Tropical Storm
                    0.15
                )
            else:
                fc_wind = 0.0
                ri_prob = 0.0
                score = 0.0

            cat = self._determine_risk_category(score)
            if score > peak_score:
                peak_score = score
                peak_horizon = f_enum

            valid_until = (now + timedelta(hours=hours)).isoformat()

            factors = (
                [
                    {"name": "24h Rapid Intensification Prob", "value": f"{ri_prob * 100:.1f}%"},
                    {"name": "24h Wind Trajectory", "value": f"{pred_delta_v:+.1f} kt"},
                    {"name": "Storm Reference", "value": storm_name}
                ]
                if has_active_threat else
                [
                    {"name": "Active Storm Status", "value": "No cyclonic system within 800 km"},
                    {"name": "24h Rapid Intensification Prob", "value": "0.0%"},
                    {"name": "Distance to Nearest Storm", "value": f"{min_dist_km:.0f} km" if min_dist_km < 9000 else "None active"}
                ]
            )

            horizons_dict[h_key] = HorizonForecastItem(
                horizon=f_enum,
                valid_from=now_str,
                valid_until=valid_until,
                risk_score=score,
                risk_category=cat,
                primary_metric_label="Forecast Sustained Wind",
                primary_metric_value=fc_wind,
                primary_metric_unit="kt",
                contributing_factors=factors,
                confidence_level="HIGH" if selected_storm else "STATISTICAL_ESTIMATE",
                data_sources=["NOAA NHC / IBTrACS", "XGBoost RI & Intensity Trajectory"],
                data_provenance=provenance
            )

        h24_item = horizons_dict["24h"]
        single_fc = SingleHazardForecast(
            hazard_type="cyclones",
            geographic_location=location_name,
            latitude=lat,
            longitude=lon,
            forecast_generated_at=now_str,
            forecast_valid_from=now_str,
            forecast_valid_until=h24_item.valid_until,
            forecast_horizon=ForecastHorizon.H24,
            risk_score=h24_item.risk_score,
            risk_category=h24_item.risk_category,
            model_name="cyclones_rapid_intensification_xgboost",
            model_version="v1.0",
            model_status="OPERATIONAL",
            contributing_features={
                "current_wind_kt": curr_wind,
                "predicted_intensity_change_24h_kt": pred_delta_v,
                "rapid_intensification_prob_24h": ri_prob_base,
                "central_pressure_hpa": 1013.0 if not has_active_threat else float(selected_storm.min_pressure_hpa or 995.0)
            },
            explanation=(
                f"Cyclone intensity forecast for {storm_name} ({location_name}) indicates {h24_item.risk_category.value} hazard over next 24h. Predicted wind is {h24_item.primary_metric_value} kt with 24h RI probability of {ri_prob_base * 100:.1f}%."
                if has_active_threat else
                f"No active tropical cyclone within 800 km of {location_name}. Cyclonic wind threat and rapid intensification probability are 0.0%."
            ),
            confidence_or_uncertainty={"confidence": "High", "model": "XGBoost RI (ROC-AUC 0.871)"},
            data_sources=["NOAA National Hurricane Center (NHC)", "NOAA IBTrACS Benchmark"],
            data_freshness="LIVE" if provenance == DataProvenanceType.LIVE_OBSERVATION else "RECENT",
            data_provenance=provenance,
            warnings=["Rapid intensification watch: Ocean conditions favor explosive strengthening."] if ri_prob_base >= 0.40 else [],
            limitations=[
                "Official cyclone advisories are issued by NOAA NHC and regional RSMCs (e.g. IMD).",
                "During calm basins, verified historical benchmark systems illustrate operational capability."
            ],
            secondary_metrics={"delta_v_24h": pred_delta_v, "ri_flag": cy_pred.rapid_intensification_predicted if ('cy_pred' in locals() and cy_pred is not None) else False}
        )

        timeline = HazardForecastTimeline(
            hazard_type="cyclones",
            geographic_location=location_name,
            latitude=lat,
            longitude=lon,
            generated_at=now_str,
            model_name="cyclones_rapid_intensification_xgboost",
            model_status="OPERATIONAL",
            horizons=horizons_dict,
            overall_trend="INCREASING" if pred_delta_v > 5.0 else "STABLE",
            peak_risk_horizon=peak_horizon,
            peak_risk_score=peak_score,
            disclaimer="Automated predictive early warning decision support. Not a statutory evacuation order."
        )

        return single_fc, timeline

    # =========================================================================
    # 6. MULTI-HAZARD LOCATION FORECAST SYNTHESIS
    # =========================================================================
    async def assess_location_forecast(
        self, lat: float, lon: float, location_name: str = "Assessment Location", hazards: Optional[List[str]] = None
    ) -> MultiHazardLocationForecastResponse:
        """
        Executes comprehensive multi-hazard predictive risk assessment across all five hazards
        for an arbitrary geographic coordinate across all standard forecast horizons.
        """
        selected_hazards = [h.lower() for h in (hazards or ["floods", "landslides", "wildfires", "earthquakes", "cyclones"])]
        now_str = datetime.now(timezone.utc).isoformat()

        hazard_forecasts: Dict[str, SingleHazardForecast] = {}
        timelines: Dict[str, HazardForecastTimeline] = {}

        # 1. Floods
        if "floods" in selected_hazards:
            f_fc, f_time = await self.forecast_flood(lat, lon, location_name)
            hazard_forecasts["floods"] = f_fc
            timelines["floods"] = f_time

        # 2. Landslides
        if "landslides" in selected_hazards:
            ls_fc, ls_time = await self.forecast_landslide(lat, lon, location_name)
            hazard_forecasts["landslides"] = ls_fc
            timelines["landslides"] = ls_time

        # 3. Wildfires
        if "wildfires" in selected_hazards:
            wf_fc, wf_time = await self.forecast_wildfire(lat, lon, location_name)
            hazard_forecasts["wildfires"] = wf_fc
            timelines["wildfires"] = wf_time

        # 4. Earthquakes
        if "earthquakes" in selected_hazards:
            eq_fc, eq_time = await self.forecast_earthquake(lat, lon, location_name)
            hazard_forecasts["earthquakes"] = eq_fc
            timelines["earthquakes"] = eq_time

        # 5. Cyclones
        if "cyclones" in selected_hazards:
            cy_fc, cy_time = await self.forecast_cyclone(lat, lon, location_name)
            hazard_forecasts["cyclones"] = cy_fc
            timelines["cyclones"] = cy_time

        # Composite risk calculation
        composite_score = max((fc.risk_score for fc in hazard_forecasts.values()), default=0.1)
        primary_hazard = max(hazard_forecasts.items(), key=lambda x: x[1].risk_score)[0] if hazard_forecasts else "none"
        composite_cat = self._determine_risk_category(composite_score)

        return MultiHazardLocationForecastResponse(
            location_name=location_name,
            latitude=lat,
            longitude=lon,
            generated_at=now_str,
            composite_risk_category=composite_cat,
            composite_risk_score=round(composite_score, 4),
            primary_hazard=primary_hazard,
            hazard_forecasts=hazard_forecasts,
            timeline_by_hazard=timelines,
            active_observations_summary={
                "retrieved_at": now_str,
                "status": "OPERATIONAL"
            },
            sources_used=[
                {"name": "Copernicus GloFAS", "data_type": "Hydrological River Routing Forecast"},
                {"name": "Open-Meteo Global NWP", "data_type": "Hourly Meteorological NWP Forecast"},
                {"name": "USGS Earthquake Hazards Program", "data_type": "Real-Time Seismicity ComCat"},
                {"name": "NASA FIRMS", "data_type": "Active Fire Thermal Hotspots"},
                {"name": "NOAA NHC & IBTrACS", "data_type": "Tropical Cyclone Track & Intensity"}
            ],
            limitations=[
                "Deterministic earthquake prediction is scientifically impossible; aftershocks are modeled via statistical decay.",
                "Blocked models (earthquake count, wildfire duration) remain strictly suppressed from operational outputs.",
                "GloFAS river discharge represents gridded basin simulations rather than direct in-situ gauge readings."
            ],
            disclaimer="HAZARDX AI provides automated predictive early warning decision-support advisories. This is NOT an official government evacuation order. Adhere to civil protection directives."
        )

forecast_service = ForecastService()
