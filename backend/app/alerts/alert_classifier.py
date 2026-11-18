"""
HAZARDX AI — Alert Severity Classification and Messaging Synthesis
Constructs structured alert payloads, actionable decision-support guidance,
and transparent scientific disclaimers for each hazard domain.
"""

from typing import Dict, Any, Optional
from .alert_rules import alert_rules
from ..schemas.alert import AlertSeverity

STANDARD_DISCLAIMER = (
    "HAZARDX AI Decision Support Advisory — Generated via calibrated machine learning and scientific observation. "
    "This advisory is intended for early warning decision support and does NOT constitute an official government evacuation order. "
    "Civil protection and meteorological agency advisories supersede this assessment."
)

class AlertClassifier:
    @staticmethod
    def classify_flood(
        lat: float,
        lon: float,
        location_name: str,
        discharge_m3s: float,
        anomaly_ratio: float,
        precip_1d_mm: float = 0.0,
        model_score: float = 0.0,
        source: str = "Copernicus GloFAS via Open-Meteo"
    ) -> Dict[str, Any]:
        severity, conf, metric = alert_rules.evaluate_flood(anomaly_ratio, precip_1d_mm, discharge_m3s, model_score)
        
        guidance_map = {
            "RED": "Immediate flood barrier deployment recommended. Inspect critical bridge embankments and low-lying transit corridors.",
            "ORANGE": "Heightened hydrological vigilance required. Monitor river gauge telemetry and issue preparatory municipal notices.",
            "YELLOW": "Elevated runoff conditions observed. Review localized drainage channels and monitor forecast precipitation.",
            "GREEN": "Normal baseflow conditions. Routine monitoring active."
        }

        title_map = {
            "RED": f"SEVERE INUNDATION WARNING: {location_name}",
            "ORANGE": f"HIGH FLOOD RISK ADVISORY: {location_name}",
            "YELLOW": f"FLOOD WATCH: {location_name}",
            "GREEN": f"Normal Streamflow: {location_name}"
        }

        desc = (
            f"Copernicus GloFAS river discharge anomaly of {anomaly_ratio:.2f}x historical baseline "
            f"({discharge_m3s:.1f} m³/s). 24h precipitation total is {precip_1d_mm:.1f} mm. "
            f"Calibrated flood occurrence susceptibility score: {model_score:.3f}."
        )

        return {
            "hazard_type": "floods",
            "severity": severity,
            "title": title_map[severity],
            "description": desc,
            "latitude": lat,
            "longitude": lon,
            "location_name": location_name,
            "source": source,
            "confidence_score": conf,
            "guidance": guidance_map[severity],
            "disclaimer": STANDARD_DISCLAIMER
        }

    @staticmethod
    def classify_landslide(
        lat: float,
        lon: float,
        location_name: str,
        slope_degrees: float,
        precip_1d_mm: float,
        precip_30d_mm: float,
        model_score: float = 0.0,
        source: str = "NASA GLC & ERA5 Reanalysis"
    ) -> Dict[str, Any]:
        severity, conf, metric = alert_rules.evaluate_landslide(slope_degrees, precip_1d_mm, precip_30d_mm, model_score)

        guidance_map = {
            "RED": "High risk of rapid debris flow or deep-seated slope failure. Restrict mountain road access and inspect steep colluvial slopes.",
            "ORANGE": "Elevated soil saturation on steep terrain. Inspect retaining structures and drainage culverts along transportation corridors.",
            "YELLOW": "Precipitation infiltration approaching triggering thresholds on moderate slopes. Maintain observational vigilance.",
            "GREEN": "Stable hillslope moisture regime. Baseline monitoring active."
        }

        title_map = {
            "RED": f"CRITICAL SLOPE FAILURE WARNING: {location_name}",
            "ORANGE": f"HIGH LANDSLIDE SUSCEPTIBILITY: {location_name}",
            "YELLOW": f"LANDSLIDE ADVISORY: {location_name}",
            "GREEN": f"Stable Terrain Conditions: {location_name}"
        }

        desc = (
            f"Hillslope gradient of {slope_degrees:.1f}° with antecedent 24h precipitation of {precip_1d_mm:.1f} mm "
            f"and 30-day accumulation of {precip_30d_mm:.1f} mm. Calibrated slope failure model score: {model_score:.3f}."
        )

        return {
            "hazard_type": "landslides",
            "severity": severity,
            "title": title_map[severity],
            "description": desc,
            "latitude": lat,
            "longitude": lon,
            "location_name": location_name,
            "source": source,
            "confidence_score": conf,
            "guidance": guidance_map[severity],
            "disclaimer": STANDARD_DISCLAIMER
        }

    @staticmethod
    def classify_earthquake(
        lat: float,
        lon: float,
        location_name: str,
        magnitude: float,
        depth_km: float,
        dist_fault_km: float = 20.0,
        aftershock_prob: float = 0.0,
        source: str = "USGS Earthquake Hazards Program"
    ) -> Dict[str, Any]:
        severity, conf, metric = alert_rules.evaluate_earthquake(magnitude, depth_km, dist_fault_km, aftershock_prob)

        guidance_map = {
            "RED": "Substantial regional aftershock hazard. Conduct urgent structural inspections of unreinforced masonry and critical bridges.",
            "ORANGE": "Elevated secondary seismic clustering hazard within 100km radius. Maintain civil protection standby posture.",
            "YELLOW": "Moderate aftershock activity anticipated. Routine structural safety assessments advised.",
            "GREEN": "Low background seismic activity. Regional tectonic monitoring normal."
        }

        title_map = {
            "RED": f"HIGH AFTERSHOCK HAZARD WARNING: {location_name} (M {magnitude:.1f})",
            "ORANGE": f"ELEVATED SEISMIC AFTERSHOCK ADVISORY: {location_name} (M {magnitude:.1f})",
            "YELLOW": f"SEISMIC MONITORING WATCH: {location_name} (M {magnitude:.1f})",
            "GREEN": f"Quiescent Background Seismicity: {location_name}"
        }

        eq_disclaimer = (
            "IMPORTANT SEISMIC GOVERNANCE: This alert represents a statistical assessment of regional AFTERSHOCK susceptibility "
            "following an observed mainshock. HAZARDX AI does NOT predict exact future earthquake times, locations, or magnitudes."
        )

        desc = (
            f"Observed mainshock of M {magnitude:.1f} at depth of {depth_km:.1f} km, located {dist_fault_km:.1f} km from "
            f"nearest mapped active fault. Statistical 30-day regional aftershock hazard probability is {(aftershock_prob*100):.1f}%."
        )

        return {
            "hazard_type": "earthquakes",
            "severity": severity,
            "title": title_map[severity],
            "description": desc,
            "latitude": lat,
            "longitude": lon,
            "location_name": location_name,
            "source": source,
            "confidence_score": conf,
            "guidance": guidance_map[severity],
            "disclaimer": eq_disclaimer
        }

    @staticmethod
    def classify_cyclone(
        lat: float,
        lon: float,
        storm_name: str,
        intensity_kt: float,
        min_pres_hpa: float,
        ri_prob: float = 0.0,
        delta_v_24h: float = 0.0,
        dist_land_km: float = 200.0,
        source: str = "NOAA NHC / IBTrACS"
    ) -> Dict[str, Any]:
        severity, conf, metric = alert_rules.evaluate_cyclone(intensity_kt, min_pres_hpa, ri_prob, delta_v_24h, dist_land_km)

        guidance_map = {
            "RED": "Severe hurricane/typhoon wind threat. Secure coastal port infrastructure, activate storm surge defenses, and review emergency shelters.",
            "ORANGE": "Tropical cyclone intensification likely. Prepare marine and coastal assets for gale-force to storm-force winds.",
            "YELLOW": "Tropical disturbance/storm monitoring active. Track atmospheric steering flow and marine sea-surface temperatures.",
            "GREEN": "Sub-tropical or low intensity depression. Normal maritime tracking."
        }

        title_map = {
            "RED": f"MAJOR CYCLONE WARNING: {storm_name} ({intensity_kt:.0f} kt)",
            "ORANGE": f"CYCLONE INTENSIFICATION ADVISORY: {storm_name} ({intensity_kt:.0f} kt)",
            "YELLOW": f"TROPICAL STORM WATCH: {storm_name}",
            "GREEN": f"Tropical Depression Monitoring: {storm_name}"
        }

        desc = (
            f"Active tropical cyclone {storm_name} with sustained winds of {intensity_kt:.0f} kt and minimum central pressure "
            f"of {min_pres_hpa:.0f} hPa. Machine learning rapid intensification (RI) probability is {(ri_prob*100):.1f}% "
            f"with predicted 24h wind change of {delta_v_24h:+.1f} kt."
        )

        return {
            "hazard_type": "cyclones",
            "severity": severity,
            "title": title_map[severity],
            "description": desc,
            "latitude": lat,
            "longitude": lon,
            "location_name": f"Cyclone {storm_name}",
            "source": source,
            "confidence_score": conf,
            "guidance": guidance_map[severity],
            "disclaimer": STANDARD_DISCLAIMER
        }

    @staticmethod
    def classify_wildfire(
        lat: float,
        lon: float,
        location_name: str,
        frp_mw: float,
        brightness_k: float,
        fwi: float = 15.0,
        wind_ms: float = 5.0,
        model_score: float = 0.0,
        source: str = "NASA FIRMS (MODIS / VIIRS)"
    ) -> Dict[str, Any]:
        severity, conf, metric = alert_rules.evaluate_wildfire(frp_mw, brightness_k, fwi, wind_ms, model_score)

        guidance_map = {
            "RED": "Extreme thermal anomaly under dangerous fire weather conditions. Aerial and ground verification required; inspect containment perimeters.",
            "ORANGE": "Significant thermal signature detected under elevated fire weather conditions (FWI >= 25). Pre-position initial attack firefighting resources.",
            "YELLOW": "Moderate thermal anomaly observed. Cross-reference with agricultural burning schedules and local dispatch records.",
            "GREEN": "Low intensity or isolated thermal anomaly. Routine satellite pass monitoring."
        }

        title_map = {
            "RED": f"CRITICAL WILDFIRE CONFLAGRATION ALERT: {location_name}",
            "ORANGE": f"HIGH WILDFIRE SUSCEPTIBILITY ADVISORY: {location_name}",
            "YELLOW": f"THERMAL ANOMALY WATCH: {location_name}",
            "GREEN": f"Thermal Detection (Routine): {location_name}"
        }

        fire_disclaimer = (
            "IMPORTANT SATELLITE THERMAL GOVERNANCE: Satellite thermal detections identify radiative heat signatures (FRP) and must "
            "NOT be assumed to represent an uncontained wildfire without ground-truth verification (agricultural burning, industrial heat)."
        )

        desc = (
            f"Satellite active fire detection with Fire Radiative Power (FRP) of {frp_mw:.1f} MW and brightness temperature "
            f"of {brightness_k:.1f} K. Local Fire Weather Index (FWI) is {fwi:.1f} with 10m surface winds of {wind_ms:.1f} m/s. "
            f"Wildfire model occurrence susceptibility score: {model_score:.3f}."
        )

        return {
            "hazard_type": "wildfires",
            "severity": severity,
            "title": title_map[severity],
            "description": desc,
            "latitude": lat,
            "longitude": lon,
            "location_name": location_name,
            "source": source,
            "confidence_score": conf,
            "guidance": guidance_map[severity],
            "disclaimer": fire_disclaimer
        }

    @staticmethod
    def classify_forecast_alert(
        hazard_type: str,
        lat: float,
        lon: float,
        location_name: str,
        forecast_horizon: str,
        valid_from: str,
        valid_until: str,
        risk_score: float,
        risk_category: str,
        primary_metric_label: str,
        primary_metric_value: float,
        primary_metric_unit: str,
        forecast_evidence: str,
        model_name: str,
        data_freshness: str = "LIVE",
        source: str = "HAZARDX Multi-Horizon Forecaster"
    ) -> Dict[str, Any]:
        """
        Synthesizes an intelligent, forward-looking early warning watch or advisory.
        Maps validated risk score to alert severity without artificially triggering RED alerts.
        """
        # Strict validated threshold mapping
        if risk_score >= 0.80 and risk_category == "EXTREME":
            severity = "RED"
            status_prefix = "DEVELOPING CRITICAL WARNING"
        elif risk_score >= 0.60 or risk_category in ["VERY HIGH", "HIGH"]:
            severity = "ORANGE"
            status_prefix = "FORECAST HAZARD ADVISORY"
        elif risk_score >= 0.35 or risk_category == "MODERATE":
            severity = "YELLOW"
            status_prefix = "DEVELOPING HAZARD WATCH"
        else:
            severity = "GREEN"
            status_prefix = "BASELINE MONITORING"

        title = f"{status_prefix} (+{forecast_horizon}): {location_name} [{hazard_type.upper()}]"

        desc = (
            f"Forecast {hazard_type} hazard risk projected over the next {forecast_horizon} "
            f"(valid from {valid_from[:16]} to {valid_until[:16]}). "
            f"Evaluated risk score: {risk_score:.3f} ({risk_category}). "
            f"Primary forecast driver: {primary_metric_label} at {primary_metric_value} {primary_metric_unit}. "
            f"Evidence: {forecast_evidence}."
        )

        guidance_map = {
            "RED": f"Emergency managers: Prepare rapid response mobilization. Coordinate cross-agency protective measures for {location_name}.",
            "ORANGE": f"Operations: Stage preliminary resources and monitor incoming numerical updates for +{forecast_horizon} forecast window.",
            "YELLOW": f"Analyst Watch: Elevated meteorological/hydrological indicators developing over +{forecast_horizon}. Maintain vigilance.",
            "GREEN": f"Routine conditions expected over +{forecast_horizon}. Baseline monitoring active."
        }

        return {
            "hazard_type": hazard_type.lower(),
            "severity": severity,
            "title": title,
            "description": desc,
            "latitude": lat,
            "longitude": lon,
            "location_name": location_name,
            "source": source,
            "confidence_score": round(risk_score, 3),
            "guidance": guidance_map[severity],
            "model_prediction": {
                "is_forecast": True,
                "forecast_horizon": forecast_horizon,
                "valid_from": valid_from,
                "valid_until": valid_until,
                "risk_score": risk_score,
                "risk_category": risk_category,
                "primary_metric": f"{primary_metric_label}: {primary_metric_value} {primary_metric_unit}",
                "forecast_evidence": forecast_evidence,
                "data_freshness": data_freshness,
                "model_name": model_name
            },
            "disclaimer": STANDARD_DISCLAIMER
        }

alert_classifier = AlertClassifier()

