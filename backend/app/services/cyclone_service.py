"""
HAZARDX AI — Tropical Cyclone Inference & Rapid Intensification Service
"""

import pandas as pd
from ..schemas.cyclone import CycloneFeatures, CyclonePredictionResponse
from ..services.model_registry import registry
from ..services.explanation_service import explanation_service
from ..utils.calibration import categorize_hazard_risk
from ..utils.logging_config import get_logger

logger = get_logger("cyclone_service")

class CycloneService:
    def __init__(self):
        self.hazard = "cyclones"
        self.ri_meta = registry.get_metadata(self.hazard, "rapid_intensification") or {}
        self.feature_order = self.ri_meta.get("features", [
            'current_wind_kt', 'current_pres_hpa', 'dist_to_land_km', 'landfall_flag',
            'past_delta_wind_6h', 'past_delta_wind_12h', 'past_delta_pres_6h',
            'translational_speed_kt', 'heading_degrees', 'coriolis_param', 'pot_intensity_headroom'
        ])

    def predict(self, features: CycloneFeatures) -> CyclonePredictionResponse:
        # Construct DataFrame adhering strictly to the training schema ordering
        feat_dict = features.model_dump()
        df = pd.DataFrame([[feat_dict[f] for f in self.feature_order]], columns=self.feature_order)
        
        # 1. Rapid Intensification (RI) Model Inference (Operational)
        ri_model = registry.get_model(self.hazard, "rapid_intensification")
        if ri_model is None:
            raise RuntimeError("Cyclone rapid intensification model is not loaded in registry.")
            
        prob_matrix = ri_model.predict_proba(df)
        ri_prob = float(prob_matrix[0, 1])
        predicted_ri = bool(ri_prob >= 0.50)
        
        # 2. Continuous 24h Intensity Change Model Inference (Operational)
        int_model = registry.get_model(self.hazard, "intensity_change_24h")
        if int_model is None:
            raise RuntimeError("Cyclone 24h intensity change model is not loaded in registry.")
            
        pred_delta_wind = float(int_model.predict(df)[0])
        projected_wind = max(10.0, float(features.current_wind_kt + pred_delta_wind))
        
        # 3. Risk Category & Guidance (Dual-Trigger: Combines Saffir-Simpson Wind Intensity with Rapid Intensification Potential)
        wind_max = max(features.current_wind_kt, projected_wind)
        if wind_max >= 96.0 or ri_prob >= 0.45:
            risk_cat = "RAPID_INTENSIFICATION_ALERT"
            alert_lvl = "RED"
            guidance = f"Major cyclonic storm threat ({wind_max:.0f} kt projected winds or high RI potential). Initiate immediate coastal evacuation and emergency protocols."
        elif wind_max >= 64.0 or ri_prob >= 0.25:
            risk_cat = "MODERATE_RI_POTENTIAL"
            alert_lvl = "YELLOW"
            guidance = f"Cyclone-force winds ({wind_max:.0f} kt) or elevated RI potential. Secure coastal infrastructure, moor vessels, and heed civil defense orders."
        else:
            risk_cat = "LOW_RI_RISK"
            alert_lvl = "GREEN"
            guidance = "Routine background tropical conditions; no active destructive storm threat."
        
        # 4. Real-Time TreeSHAP Explanation for RI
        attributions = explanation_service.explain_prediction(
            model_key="cyclones_rapid_intensification",
            model=ri_model,
            features_df=df,
            is_binary=True,
            top_k=5
        )
        
        warnings = [
            "Rapid Intensification (RI) is defined meteorologically as an intensity increase of >= 30 knots (15.4 m/s) over a 24-hour window.",
            "Operational continuous 24h intensity change forecast achieved R^2 = 0.4426 (RMSE 13.99 kt).",
            "Inner-core eyewall replacement cycles and localized ocean heat content variations may cause abrupt departures from statistical forecasts."
        ]
        
        return CyclonePredictionResponse(
            hazard_name="Cyclones",
            rapid_intensification_predicted=predicted_ri,
            rapid_intensification_probability=round(ri_prob, 4),
            predicted_24h_intensity_change_kt=round(pred_delta_wind, 2),
            projected_wind_24h_kt=round(projected_wind, 2),
            risk_category=risk_cat,
            alert_level=alert_lvl,
            action_guidance=guidance,
            important_contributing_features=attributions,
            model_version=self.ri_meta.get("version", "1.0.0"),
            input_validation_status="VALID",
            limitations_and_warnings=warnings
        )

cyclone_service = CycloneService()

