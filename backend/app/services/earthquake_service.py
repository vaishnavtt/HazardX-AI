"""
HAZARDX AI — Earthquake Aftershock Hazard Inference Service
"""

import numpy as np
import pandas as pd
from ..schemas.earthquake import EarthquakeFeatures, EarthquakePredictionResponse
from ..services.model_registry import registry
from ..services.explanation_service import explanation_service
from ..utils.calibration import categorize_hazard_risk
from ..config import settings
from ..utils.logging_config import get_logger

logger = get_logger("earthquake_service")

class EarthquakeService:
    def __init__(self):
        self.hazard = "earthquakes"
        self.haz_meta = registry.get_metadata(self.hazard, "aftershock_hazard") or {}
        self.feature_order = self.haz_meta.get("features", [
            'mainshock_mag', 'focal_depth_km', 'dist_to_active_fault_km', 'nearest_fault_slip_type',
            'prior_count_7d_100km', 'prior_count_30d_100km', 'prior_count_365d_100km',
            'prior_max_mag_30d', 'cumulative_energy_log_joules', 'seismic_rate_accel_ratio',
            'regional_b_value'
        ])

    def predict(self, features: EarthquakeFeatures) -> EarthquakePredictionResponse:
        feat_dict = features.model_dump()
        
        # 1. Prepare raw feature row
        row = [feat_dict[f] for f in self.feature_order]
        df = pd.DataFrame([row], columns=self.feature_order)
        
        # 2. Encode categorical fault slip type using saved training encoder
        encoder = registry.get_encoder(self.hazard)
        if encoder is not None:
            try:
                slip_val = str(df.at[0, 'nearest_fault_slip_type'])
                encoded_val = encoder.transform([[slip_val]])[0][0]
                df['nearest_fault_slip_type'] = float(encoded_val)
            except Exception as e:
                logger.warning(f"Fault slip encoding fallback: {e}")
                df['nearest_fault_slip_type'] = -1.0
        else:
            df['nearest_fault_slip_type'] = 0.0
            
        df = df.astype(np.float64)
        
        # 3. Aftershock Hazard Binary Classification
        haz_model = registry.get_model(self.hazard, "aftershock_hazard")
        if haz_model is None:
            raise RuntimeError("Earthquake aftershock hazard model is not loaded in registry.")
            
        prob_matrix = haz_model.predict_proba(df)
        hazard_prob = float(prob_matrix[0, 1])
        predicted_hazard = bool(hazard_prob >= 0.50)
        
        # 4. Risk Category & Guidance
        risk_cat, alert_lvl, guidance = categorize_hazard_risk(self.hazard, hazard_prob)
        
        # 5. Secondary Regression Models (Governed by Operational Status)
        est_max_mag = None
        max_mag_model = registry.get_model(self.hazard, "max_aftershock_mag")
        if max_mag_model is not None and predicted_hazard:
            # Marked EXPERIMENTAL in registry
            raw_mag = float(max_mag_model.predict(df)[0])
            est_max_mag = round(max(3.0, min(9.5, raw_mag)), 2)
            
        # 6. Real-Time TreeSHAP Explanation
        attributions = explanation_service.explain_prediction(
            model_key="earthquakes_aftershock_hazard",
            model=haz_model,
            features_df=df,
            is_binary=True,
            top_k=5
        )
        
        warnings = [
            "This model provides statistical aftershock hazard assessment following a shallow M>=5.0 mainshock within 100km and 30 days.",
            "This system CANNOT and DOES NOT predict the exact time, location, or occurrence of unprovoked future earthquakes.",
            "Aftershock count regression model is marked UNAVAILABLE FOR OPERATIONAL USE due to heavy-tailed Omori-Utsu dispersion."
        ]
        
        return EarthquakePredictionResponse(
            hazard_name="Earthquakes",
            assessment_type="Regional Aftershock Hazard Assessment (30-day / 100km horizon)",
            disclaimer="This service provides statistical aftershock hazard assessment following a mainshock. This is NOT an exact earthquake prediction.",
            elevated_aftershock_hazard_predicted=predicted_hazard,
            hazard_probability=round(hazard_prob, 4),
            risk_category=risk_cat,
            alert_level=alert_lvl,
            action_guidance=guidance,
            estimated_max_aftershock_magnitude=est_max_mag,
            estimated_aftershock_count=None,  # Blocked from operational exposure
            important_contributing_features=attributions,
            model_version=self.haz_meta.get("version", "1.0.0"),
            input_validation_status="VALID",
            limitations_and_warnings=warnings
        )

earthquake_service = EarthquakeService()

