"""
HAZARDX AI — Flood Inference & Risk Assessment Service
"""

import pandas as pd
from ..schemas.flood import FloodFeatures, FloodPredictionResponse
from ..services.model_registry import registry
from ..services.explanation_service import explanation_service
from ..utils.calibration import adjust_case_control_probability, categorize_hazard_risk
from ..config import settings
from ..utils.logging_config import get_logger

logger = get_logger("flood_service")

class FloodService:
    def __init__(self):
        self.hazard = "floods"
        self.occ_meta = registry.get_metadata(self.hazard, "flood_occurrence") or {}
        self.feature_order = self.occ_meta.get("features", [
            'precip_1d_mm', 'precip_3d_sum_mm', 'precip_7d_sum_mm', 'precip_14d_sum_mm',
            'api_14d_index', 'temp_2m_celsius', 'soil_temp_celsius', 'river_discharge_m3s',
            'river_discharge_7d_mean_m3s', 'river_discharge_ratio_7d', 'elevation_m',
            'slope_degrees', 'topographic_wetness_index', 'distance_to_river_km'
        ])

    def predict(self, features: FloodFeatures) -> FloodPredictionResponse:
        # Construct DataFrame strictly adhering to the training schema ordering
        feat_dict = features.model_dump()
        df = pd.DataFrame([[feat_dict[f] for f in self.feature_order]], columns=self.feature_order)
        
        # 1. Occurrence Model Inference
        occ_model = registry.get_model(self.hazard, "flood_occurrence")
        if occ_model is None:
            raise RuntimeError("Flood occurrence model is not loaded in registry.")
            
        prob_matrix = occ_model.predict_proba(df)
        raw_prob = float(prob_matrix[0, 1])
        predicted_occ = bool(raw_prob >= 0.50)
        
        # 2. Bayesian Prior Calibration
        prior = settings.CLIMATOLOGICAL_PRIORS.get("floods", 0.005)
        calibrated_prob = adjust_case_control_probability(raw_prob, prior)
        
        # 3. Severity Classification
        sev_class = 0
        sev_label = "None / No Inundation"
        sev_model = registry.get_model(self.hazard, "flood_severity")
        if sev_model is not None and predicted_occ:
            sev_class = int(sev_model.predict(df)[0])
            labels = {0: "None", 1: "Large Flood Event", 2: "Extreme / Decadal Inundation"}
            sev_label = labels.get(sev_class, "Large Flood Event")
            
        # 4. Risk Category & Guidance
        risk_cat, alert_lvl, guidance = categorize_hazard_risk(self.hazard, raw_prob)

        warnings = [
            "Model trained on 1:1 case-control historical disasters; raw_model_score represents relative environmental susceptibility.",
            "Calibrated susceptibility reflects daily empirical occurrence odds under local hydrological conditions.",
            "ECMWF ERA5 28km resolution models regional river basin inundation; hyper-local urban cloudbursts require radar precipitation networks."
        ]

        # Hydrological discharge anomaly and rainfall reconciliation:
        # If river discharge is at or below baseline (ratio <= 1.25) and recent rain is low (3d < 15mm, 1d < 5mm),
        # river reach is quiescent, so raw topographic susceptibility should not generate false alerts.
        q_ratio = float(features.river_discharge_ratio_7d)
        p_1d = float(features.precip_1d_mm)
        p_3d = float(features.precip_3d_sum_mm)

        if q_ratio <= 1.25 and p_1d < 5.0 and p_3d < 15.0 and alert_lvl != "GREEN":
            risk_cat = "LOW"
            alert_lvl = "GREEN"
            guidance = f"Hydrological status normal (river discharge anomaly ratio {q_ratio:.2f}x baseline; 24h rain {p_1d:.1f} mm). Fluvial inundation threat is low."
            warnings.append("Hydrological baseline reconciliation: normal river discharge and minimal rainfall keep flood threat at baseline despite floodplain terrain proximity.")
        elif q_ratio >= 2.0 or p_1d >= 75.0:
            if alert_lvl in ["GREEN", "YELLOW"]:
                risk_cat = "HIGH"
                alert_lvl = "ORANGE"
                guidance = f"Significant hydrological surge detected (discharge ratio {q_ratio:.2f}x baseline, 24h rain {p_1d:.1f} mm). River reach approaching or exceeding bankfull capacity."
                warnings.append("Hydrological surge detected: discharge ratio significantly exceeds 7-day baseline.")

        # 5. Real-Time TreeSHAP Explanation
        attributions = explanation_service.explain_prediction(
            model_key="floods_flood_occurrence",
            model=occ_model,
            features_df=df,
            is_binary=True,
            top_k=5
        )
        
        return FloodPredictionResponse(
            hazard_name="Floods",
            flood_occurrence_predicted=predicted_occ,
            raw_model_score=round(raw_prob, 4),
            calibrated_susceptibility_score=calibrated_prob,
            risk_category=risk_cat,
            alert_level=alert_lvl,
            severity_class=sev_class,
            severity_label=sev_label,
            action_guidance=guidance,
            important_contributing_features=attributions,
            model_version=self.occ_meta.get("version", "1.0.0"),
            input_validation_status="VALID",
            limitations_and_warnings=warnings
        )

flood_service = FloodService()

