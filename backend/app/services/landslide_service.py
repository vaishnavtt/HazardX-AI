"""
HAZARDX AI — Landslide Inference & Risk Assessment Service
"""

import pandas as pd
from ..schemas.landslide import LandslideFeatures, LandslidePredictionResponse
from ..services.model_registry import registry
from ..services.explanation_service import explanation_service
from ..utils.calibration import adjust_case_control_probability, categorize_hazard_risk
from ..config import settings
from ..utils.logging_config import get_logger

logger = get_logger("landslide_service")

class LandslideService:
    def __init__(self):
        self.hazard = "landslides"
        self.occ_meta = registry.get_metadata(self.hazard, "landslide_occurrence") or {}
        self.feature_order = self.occ_meta.get("features", [
            'precip_1d_mm', 'precip_3d_sum_mm', 'precip_7d_sum_mm', 'precip_30d_sum_mm',
            'api_30d_index', 'temp_2m_celsius', 'soil_temp_celsius', 'slope_degrees',
            'elevation_m', 'aspect_degrees', 'plan_curvature', 'soil_clay_fraction_pct',
            'distance_to_road_km', 'distance_to_stream_km'
        ])

    def predict(self, features: LandslideFeatures) -> LandslidePredictionResponse:
        feat_dict = features.model_dump()
        df = pd.DataFrame([[feat_dict[f] for f in self.feature_order]], columns=self.feature_order)
        
        # 1. Occurrence Model Inference
        occ_model = registry.get_model(self.hazard, "landslide_occurrence")
        if occ_model is None:
            raise RuntimeError("Landslide occurrence model is not loaded in registry.")
            
        prob_matrix = occ_model.predict_proba(df)
        raw_prob = float(prob_matrix[0, 1])
        predicted_occ = bool(raw_prob >= 0.50)
        
        # 2. Bayesian Prior Calibration
        prior = settings.CLIMATOLOGICAL_PRIORS.get("landslides", 0.002)
        calibrated_prob = adjust_case_control_probability(raw_prob, prior)
        
        # 3. Magnitude Classification
        mag_class = 0
        mag_label = "None / Stable Slope"
        mag_model = registry.get_model(self.hazard, "landslide_magnitude")
        if mag_model is not None and predicted_occ:
            mag_class = int(mag_model.predict(df)[0])
            labels = {0: "None", 1: "Small to Medium Mass Movement", 2: "Large / Catastrophic Debris Flow"}
            mag_label = labels.get(mag_class, "Small to Medium Mass Movement")
            
        # 4. Risk Category & Guidance
        risk_cat, alert_lvl, guidance = categorize_hazard_risk(self.hazard, raw_prob)
        
        # 5. Real-Time TreeSHAP Explanation
        attributions = explanation_service.explain_prediction(
            model_key="landslides_landslide_occurrence",
            model=occ_model,
            features_df=df,
            is_binary=True,
            top_k=5
        )
        
        warnings = [
            "Model models precipitation-induced slope instability; earthquake-triggered failures require peak ground acceleration (PGA).",
            "Trained on balanced case-control samples; raw score represents relative hillslope susceptibility.",
            "Copernicus DEM 90m slope gradient represents macro-topography; local road embankment cuts may have localized steeper micro-slopes."
        ]
        
        return LandslidePredictionResponse(
            hazard_name="Landslides",
            landslide_occurrence_predicted=predicted_occ,
            raw_model_score=round(raw_prob, 4),
            calibrated_susceptibility_score=calibrated_prob,
            risk_category=risk_cat,
            alert_level=alert_lvl,
            hazard_magnitude_class=mag_class,
            hazard_magnitude_label=mag_label,
            action_guidance=guidance,
            important_contributing_features=attributions,
            model_version=self.occ_meta.get("version", "1.0.0"),
            input_validation_status="VALID",
            limitations_and_warnings=warnings
        )

landslide_service = LandslideService()

