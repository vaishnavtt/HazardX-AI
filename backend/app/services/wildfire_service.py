"""
HAZARDX AI — Wildfire Inference & Susceptibility Service
"""

import pandas as pd
from typing import Optional
from ..schemas.wildfire import WildfireFeatures, WildfirePredictionResponse
from ..services.model_registry import registry
from ..services.explanation_service import explanation_service
from ..utils.calibration import adjust_case_control_probability, categorize_hazard_risk
from ..config import settings
from ..utils.logging_config import get_logger

logger = get_logger("wildfire_service")

class WildfireService:
    def __init__(self):
        self.hazard = "wildfires"
        self.occ_meta = registry.get_metadata(self.hazard, "wildfire_occurrence") or {}
        self.feature_order = self.occ_meta.get("features", [
            'temp_2m_celsius', 'relative_humidity_pct', 'wind_speed_10m_ms',
            'precip_7d_sum_mm', 'precip_30d_sum_mm', 'soil_temp_celsius',
            'fwi_fire_weather_index', 'slope_degrees', 'elevation_m', 'distance_to_road_km'
        ])

    def predict(self, features: WildfireFeatures) -> WildfirePredictionResponse:
        # Construct DataFrame strictly adhering to the training schema ordering
        feat_dict = features.model_dump()
        df = pd.DataFrame([[feat_dict[f] for f in self.feature_order]], columns=self.feature_order)
        
        # 1. Occurrence Model Inference (Operational)
        occ_model = registry.get_model(self.hazard, "wildfire_occurrence")
        if occ_model is None:
            raise RuntimeError("Wildfire occurrence model is not loaded in registry.")
            
        prob_matrix = occ_model.predict_proba(df)
        raw_prob = float(prob_matrix[0, 1])
        predicted_occ = bool(raw_prob >= 0.50)
        
        # 2. Bayesian Prior Calibration
        prior = settings.CLIMATOLOGICAL_PRIORS.get("wildfires", 0.002)
        calibrated_prob = adjust_case_control_probability(raw_prob, prior)
        
        # 3. FRP Intensity Model Inference (EXPERIMENTAL / ADVISORY ONLY)
        frp_pred: Optional[float] = None
        frp_status = registry.get_operational_status(self.hazard, "frp_intensity")
        frp_model = registry.get_model(self.hazard, "frp_intensity")
        if frp_model is not None and predicted_occ:
            try:
                raw_frp = float(frp_model.predict(df)[0])
                frp_pred = round(raw_frp, 3)
            except Exception as e:
                logger.warning(f"Failed to infer FRP intensity: {e}")
                
        # 4. Fire Duration Model Inference (UNAVAILABLE FOR OPERATIONAL USE)
        # Blocked from operational prediction due to R^2 = -214.75
        duration_pred: Optional[float] = None
        
        # 5. Risk Category & Guidance
        risk_cat, alert_lvl, guidance = categorize_hazard_risk(self.hazard, raw_prob)
        
        # 6. Real-Time TreeSHAP Explanation
        attributions = explanation_service.explain_prediction(
            model_key="wildfires_wildfire_occurrence",
            model=occ_model,
            features_df=df,
            is_binary=True,
            top_k=5
        )
        
        warnings = [
            "Model trained on 1:1 case-control historical fire detections; raw_model_score represents relative ignition susceptibility.",
            "Calibrated susceptibility reflects empirical local background probability under prevailing fire weather conditions.",
            "FRP intensity forecast is experimental (R^2 = 0.2154) and provided for research guidance only.",
            "Fire duration prediction is BLOCKED from operational use due to lack of statistical validation generalization (R^2 = -214.75)."
        ]
        
        return WildfirePredictionResponse(
            hazard_name="Wildfires",
            wildfire_susceptibility_predicted=predicted_occ,
            raw_model_score=round(raw_prob, 4),
            calibrated_susceptibility_score=calibrated_prob,
            risk_category=risk_cat,
            alert_level=alert_lvl,
            action_guidance=guidance,
            estimated_log_frp_mw=frp_pred,
            estimated_duration_days=duration_pred,
            important_contributing_features=attributions,
            model_version=self.occ_meta.get("version", "1.0.0"),
            input_validation_status="VALID",
            limitations_and_warnings=warnings
        )

wildfire_service = WildfireService()

