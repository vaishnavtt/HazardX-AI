"""
HAZARDX AI — Configurable Alert Rules and Scientific Thresholds
Defines physical and model-derived decision thresholds for Floods, Landslides,
Earthquakes (Aftershock Hazard), Cyclones, and Wildfires.
"""

from typing import Dict, Any, Tuple
from ..schemas.alert import AlertSeverity

class AlertRules:
    """
    Standard scientific alert threshold engine.
    Produces (severity, confidence, primary_metric_summary).
    """

    @staticmethod
    def evaluate_flood(
        anomaly_ratio: float,
        precip_1d_mm: float,
        discharge_m3s: float,
        model_score: float = 0.0
    ) -> Tuple[AlertSeverity, float, str]:
        metric = f"Discharge Anomaly: {anomaly_ratio:.2f}x | 1d Rain: {precip_1d_mm:.1f} mm | Flow: {discharge_m3s:.1f} m³/s"
        
        if anomaly_ratio >= 2.5 or model_score >= 0.70 or precip_1d_mm >= 100.0:
            conf = max(0.85, min(0.98, model_score or 0.88))
            return ("RED", conf, metric)
        elif anomaly_ratio >= 1.8 or model_score >= 0.50 or precip_1d_mm >= 60.0:
            conf = max(0.70, min(0.85, model_score or 0.75))
            return ("ORANGE", conf, metric)
        elif anomaly_ratio >= 1.35 or model_score >= 0.30 or precip_1d_mm >= 35.0:
            conf = max(0.55, min(0.70, model_score or 0.60))
            return ("YELLOW", conf, metric)
        else:
            return ("GREEN", 0.95, metric)

    @staticmethod
    def evaluate_landslide(
        slope_degrees: float,
        precip_1d_mm: float,
        precip_30d_mm: float,
        model_score: float = 0.0
    ) -> Tuple[AlertSeverity, float, str]:
        metric = f"Slope: {slope_degrees:.1f}° | 1d Rain: {precip_1d_mm:.1f} mm | 30d Rain: {precip_30d_mm:.1f} mm"

        if slope_degrees >= 25.0 and (precip_1d_mm >= 80.0 or model_score >= 0.65):
            conf = max(0.82, min(0.96, model_score or 0.85))
            return ("RED", conf, metric)
        elif slope_degrees >= 20.0 and (precip_1d_mm >= 50.0 or (precip_30d_mm >= 200.0 and precip_1d_mm >= 25.0) or model_score >= 0.45):
            conf = max(0.70, min(0.82, model_score or 0.72))
            return ("ORANGE", conf, metric)
        elif slope_degrees >= 15.0 and (precip_1d_mm >= 30.0 or model_score >= 0.25):
            conf = max(0.55, min(0.70, model_score or 0.58))
            return ("YELLOW", conf, metric)
        else:
            return ("GREEN", 0.95, metric)

    @staticmethod
    def evaluate_earthquake(
        magnitude: float,
        depth_km: float,
        dist_fault_km: float,
        aftershock_hazard_prob: float = 0.0
    ) -> Tuple[AlertSeverity, float, str]:
        """
        Important Scientific Governance: Evaluates regional aftershock susceptibility following an observed mainshock.
        Does NOT claim exact future earthquake prediction.
        """
        metric = f"Mainshock: M {magnitude:.1f} | Depth: {depth_km:.1f} km | Fault Dist: {dist_fault_km:.1f} km"

        if magnitude >= 6.5 or (aftershock_hazard_prob >= 0.65 and dist_fault_km <= 50.0):
            conf = max(0.85, min(0.98, aftershock_hazard_prob or 0.90))
            return ("RED", conf, metric)
        elif magnitude >= 5.5 or aftershock_hazard_prob >= 0.45:
            conf = max(0.70, min(0.85, aftershock_hazard_prob or 0.75))
            return ("ORANGE", conf, metric)
        elif magnitude >= 4.5 or aftershock_hazard_prob >= 0.25:
            conf = max(0.60, min(0.70, aftershock_hazard_prob or 0.65))
            return ("YELLOW", conf, metric)
        else:
            return ("GREEN", 0.95, metric)

    @staticmethod
    def evaluate_cyclone(
        intensity_kt: float,
        min_pres_hpa: float,
        ri_prob: float = 0.0,
        delta_v_24h: float = 0.0,
        dist_land_km: float = 500.0
    ) -> Tuple[AlertSeverity, float, str]:
        metric = f"Wind: {intensity_kt:.0f} kt | Pressure: {min_pres_hpa:.0f} hPa | RI Prob: {(ri_prob*100):.0f}%"

        # Saffir-Simpson Hurricane / Typhoon Thresholds
        if intensity_kt >= 96.0 or (ri_prob >= 0.50 and dist_land_km <= 250.0):
            conf = max(0.88, min(0.99, ri_prob or 0.92))
            return ("RED", conf, metric)
        elif intensity_kt >= 64.0 or ri_prob >= 0.35 or delta_v_24h >= 20.0:
            conf = max(0.72, min(0.88, ri_prob or 0.78))
            return ("ORANGE", conf, metric)
        elif intensity_kt >= 34.0 or ri_prob >= 0.20:
            conf = max(0.60, min(0.72, ri_prob or 0.65))
            return ("YELLOW", conf, metric)
        else:
            return ("GREEN", 0.95, metric)

    @staticmethod
    def evaluate_wildfire(
        frp_mw: float,
        brightness_k: float,
        fwi: float = 15.0,
        wind_ms: float = 5.0,
        model_score: float = 0.0
    ) -> Tuple[AlertSeverity, float, str]:
        """
        Important Scientific Governance: Satellite thermal anomalies represent radiative heat signatures
        and are evaluated alongside Fire Weather Index (FWI) conditions.
        """
        metric = f"Thermal FRP: {frp_mw:.1f} MW | FWI: {fwi:.1f} | Temp: {brightness_k:.1f} K | Wind: {wind_ms:.1f} m/s"

        if (frp_mw >= 50.0 and fwi >= 30.0) or model_score >= 0.70:
            conf = max(0.80, min(0.95, model_score or 0.85))
            return ("RED", conf, metric)
        elif (frp_mw >= 25.0 and fwi >= 20.0) or model_score >= 0.50:
            conf = max(0.68, min(0.80, model_score or 0.72))
            return ("ORANGE", conf, metric)
        elif frp_mw >= 10.0 or fwi >= 18.0 or model_score >= 0.30:
            conf = max(0.55, min(0.68, model_score or 0.60))
            return ("YELLOW", conf, metric)
        else:
            return ("GREEN", 0.95, metric)

alert_rules = AlertRules()

