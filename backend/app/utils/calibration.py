"""
HAZARDX AI — Calibration & Hazard Risk Categorization Utilities
Adjusts raw case-control model outputs for climatological base-rate priors
and assigns standardized hazard alert levels.
"""

import math
from typing import Tuple

def adjust_case_control_probability(p_model: float, real_world_prior: float) -> float:
    """
    Adjusts raw model predicted probability from a 1:1 case-control sample
    to a realistic real-world prior probability using Bayes' rule odds-correction.
    
    Formula:
      logit(p_calibrated) = logit(p_model) + ln(pi / (1 - pi))
    """
    # Guard bounds to prevent infinite logits
    p_clamped = max(1e-6, min(1.0 - 1e-6, p_model))
    pi_clamped = max(1e-6, min(1.0 - 1e-6, real_world_prior))
    
    logit_model = math.log(p_clamped / (1.0 - p_clamped))
    logit_prior = math.log(pi_clamped / (1.0 - pi_clamped))
    
    logit_calibrated = logit_model + logit_prior
    p_calibrated = 1.0 / (1.0 + math.exp(-logit_calibrated))
    return float(round(p_calibrated, 6))

def categorize_hazard_risk(hazard_type: str, raw_score: float) -> Tuple[str, str, str]:
    """
    Returns (risk_category, alert_level, action_guidance) based on hazard type and model score.
    """
    if hazard_type == "earthquakes":
        # Elevated aftershock hazard thresholding
        if raw_score < 0.25:
            return "QUIESCENT", "GREEN", "Normal background seismic monitoring; low probability of secondary ruptures."
        elif raw_score < 0.50:
            return "MODERATE_AFTERSHOCK_ADVISORY", "YELLOW", "Elevated seismic clustering detected; maintain structural vigilance."
        else:
            return "HIGH_AFTERSHOCK_WARNING", "RED", "Substantial aftershock hazard detected; inspect critical infrastructure and secure structures."
            
    elif hazard_type == "cyclones":
        # Rapid intensification probability
        if raw_score < 0.20:
            return "LOW_RI_RISK", "GREEN", "Normal intensification trajectory anticipated."
        elif raw_score < 0.40:
            return "MODERATE_RI_POTENTIAL", "YELLOW", "Atmospheric and oceanic conditions support potential intensification jump."
        else:
            return "RAPID_INTENSIFICATION_ALERT", "RED", "High risk of rapid intensification (+30 kt in 24h); initiate emergency coastal preparations."
            
    else:
        # Floods, Landslides, Wildfires (Susceptibility scoring)
        if raw_score < 0.30:
            return "LOW", "GREEN", "Normal baseline conditions; no immediate hazard advisory."
        elif raw_score < 0.60:
            return "MODERATE", "YELLOW", "Elevated environmental susceptibility; monitor local weather forecasts and terrain conditions."
        elif raw_score < 0.80:
            return "HIGH", "ORANGE", "High hazard danger; prepare emergency mitigation plans and flood/landslide barriers."
        else:
            return "SEVERE_CRITICAL", "RED", "Extreme hazard conditions imminent; issue immediate warnings and activate evacuation protocols."

