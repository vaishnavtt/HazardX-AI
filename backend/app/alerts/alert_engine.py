"""
HAZARDX AI — Real-Time Alert Generation Engine
Evaluates observational data streams and model inference outputs to synthesize,
deduplicate, persist, and dispatch multi-hazard disaster alerts.
"""

from typing import List, Dict, Any, Optional
from .alert_classifier import alert_classifier
from .alert_manager import alert_manager
from .notification_service import notification_service
from ..schemas.alert import AlertItem
from ..services.external_data_service import external_data_service
from ..utils.logging_config import get_logger

logger = get_logger("alert_engine")

class AlertEngine:
    def __init__(self):
        pass

    async def evaluate_live_streams(self) -> List[AlertItem]:
        """
        Polls cached authentic live streams across all 5 hazard domains,
        evaluates alert conditions, deduplicates, and manages notifications.
        """
        generated_alerts: List[AlertItem] = []

        # 1. Evaluate Earthquakes (USGS ComCat)
        try:
            eq_feed = await external_data_service.get_live_earthquakes(min_magnitude=3.5, limit=25)
            for eq in eq_feed.data:
                mag = float(eq.get("magnitude", 0.0))
                # Alert condition: M >= 4.5
                if mag >= 4.5:
                    payload = alert_classifier.classify_earthquake(
                        lat=float(eq["latitude"]),
                        lon=float(eq["longitude"]),
                        location_name=eq.get("location", f"M {mag:.1f} Earthquake"),
                        magnitude=mag,
                        depth_km=float(eq.get("depth_km", 10.0)),
                        dist_fault_km=15.0, # Regional proximity
                        aftershock_prob=min(0.95, 0.20 + (mag - 4.5) * 0.25),
                        source=eq.get("source", "USGS Earthquake Hazards Program")
                    )
                    payload["model_prediction"] = {"mainshock_mag": mag, "aftershock_susceptibility": payload["confidence_score"]}
                    alert_item, is_new = alert_manager.create_or_update_alert(payload)
                    generated_alerts.append(alert_item)
                    if is_new or payload["severity"] in ["ORANGE", "RED"]:
                        await notification_service.notify_alert(alert_item)
        except Exception as e:
            logger.error(f"Error evaluating live earthquakes for alerts: {e}")

        # 2. Evaluate Wildfires (NASA FIRMS)
        try:
            wf_feed = await external_data_service.get_live_wildfires(min_confidence="nominal", limit=30)
            for wf in wf_feed.data:
                frp = float(wf.get("frp_mw", 0.0))
                # Alert condition: FRP >= 25 MW
                if frp >= 25.0:
                    payload = alert_classifier.classify_wildfire(
                        lat=float(wf["latitude"]),
                        lon=float(wf["longitude"]),
                        location_name=f"Thermal Anomaly Sector ({float(wf['latitude']):.2f}, {float(wf['longitude']):.2f})",
                        frp_mw=frp,
                        brightness_k=float(wf.get("brightness_kelvin", 320.0)),
                        fwi=min(80.0, 15.0 + (frp / 2.0)),
                        source=wf.get("source", "NASA FIRMS")
                    )
                    payload["model_prediction"] = {"frp_mw": frp, "satellite": wf.get("satellite", "MODIS")}
                    alert_item, is_new = alert_manager.create_or_update_alert(payload)
                    generated_alerts.append(alert_item)
                    if is_new or payload["severity"] in ["ORANGE", "RED"]:
                        await notification_service.notify_alert(alert_item)
        except Exception as e:
            logger.error(f"Error evaluating live wildfires for alerts: {e}")

        # 3. Evaluate Cyclones (NOAA NHC / IBTrACS)
        try:
            cy_feed = await external_data_service.get_live_cyclones(limit=10)
            for storm in cy_feed.data:
                wind = float(storm.get("intensity_kt", 0.0))
                if wind >= 35.0:  # Tropical Storm or Hurricane
                    payload = alert_classifier.classify_cyclone(
                        lat=float(storm["latitude"]),
                        lon=float(storm["longitude"]),
                        storm_name=storm.get("name", "Active Tropical Cyclone"),
                        intensity_kt=wind,
                        min_pres_hpa=float(storm.get("min_pressure_hpa") or 990.0),
                        ri_prob=min(0.95, max(0.10, (wind - 35.0) / 100.0)),
                        source=storm.get("source", "NOAA NHC / IBTrACS")
                    )
                    payload["model_prediction"] = {"wind_kt": wind, "basin": storm.get("basin", "Global Ocean Basin")}
                    alert_item, is_new = alert_manager.create_or_update_alert(payload)
                    generated_alerts.append(alert_item)
                    if is_new or payload["severity"] in ["ORANGE", "RED"]:
                        await notification_service.notify_alert(alert_item)
        except Exception as e:
            logger.error(f"Error evaluating live cyclones for alerts: {e}")

        # 4. Evaluate Landslides (NASA GLC Corridors)
        try:
            ls_feed = await external_data_service.get_live_landslides(limit=10)
            for ls in ls_feed.data:
                p1 = float(ls.get("precip_1d_mm", 0.0))
                p30 = float(ls.get("precip_30d_mm", 0.0))
                slope = float(ls.get("slope_degrees", 25.0))
                if ls.get("elevated_moisture_hazard", False) or p1 >= 30.0:
                    payload = alert_classifier.classify_landslide(
                        lat=float(ls["latitude"]),
                        lon=float(ls["longitude"]),
                        location_name=ls.get("location_name", "Mountain Corridor"),
                        slope_degrees=slope,
                        precip_1d_mm=p1,
                        precip_30d_mm=p30,
                        model_score=min(0.90, max(0.20, (p1 / 100.0) * (slope / 30.0))),
                        source=ls.get("source", "NASA GLC & ERA5 Reanalysis")
                    )
                    payload["model_prediction"] = {"precip_1d_mm": p1, "slope_degrees": slope}
                    alert_item, is_new = alert_manager.create_or_update_alert(payload)
                    generated_alerts.append(alert_item)
                    if is_new or payload["severity"] in ["ORANGE", "RED"]:
                        await notification_service.notify_alert(alert_item)
        except Exception as e:
            logger.error(f"Error evaluating live landslides for alerts: {e}")

        # 5. Expire stale alerts older than operational window
        expired_count = alert_manager.expire_stale_alerts(max_age_hours=48)
        if expired_count > 0:
            logger.info(f"Automatically expired {expired_count} stale alert(s).")

        return generated_alerts

alert_engine = AlertEngine()

