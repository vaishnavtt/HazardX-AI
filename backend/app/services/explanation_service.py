"""
HAZARDX AI — Real-Time Model Explainability Service
Computes TreeSHAP feature attributions on-the-fly for single inference requests,
providing interpretable physical feedback to emergency analysts.
"""

import numpy as np
import pandas as pd
import shap
from typing import List, Dict, Any, Optional
from ..schemas.common import FeatureAttribution
from ..utils.logging_config import get_logger

logger = get_logger("explanation_service")

# Predefined physical descriptions for key environmental covariates
PHYSICAL_INTERPRETATIONS = {
    # Floods
    "precip_1d_mm": "Acute 24-hour rainfall intensity causing flash runoff and localized catchment inundation.",
    "precip_3d_sum_mm": "3-day cumulative rainfall causing soil saturation and small river surge.",
    "precip_7d_sum_mm": "7-day cumulative rainfall driving regional hydrologic basin storage capacity.",
    "precip_14d_sum_mm": "14-day antecedent rainfall establishing catchment water saturation baseline.",
    "api_14d_index": "Antecedent Precipitation Index quantifying remaining soil moisture storage deficit.",
    "river_discharge_m3s": "Copernicus GloFAS river channel discharge rate relative to channel bankfull capacity.",
    "elevation_m": "Surface elevation; low-elevation basins and coastal plains collect overland runoff.",
    "slope_degrees": "Terrain slope angle; flatter slopes impede drainage, prolonging water ponding.",
    "topographic_wetness_index": "DEM Topographic Wetness Index modeling topographic water accumulation potential.",
    "distance_to_river_km": "Proximity to primary river channel determining overbank flooding vulnerability.",
    "soil_temp_celsius": "Topsoil temperature influencing infiltration rate and evapotranspiration.",
    "temp_2m_celsius": "Surface air temperature modulating snowmelt and atmospheric moisture capacity.",
    
    # Landslides
    "precip_30d_sum_mm": "30-day cumulative precipitation driving deep pore-water pressure accumulation.",
    "api_30d_index": "30-day Antecedent Precipitation Index reflecting hillslope hydrological saturation.",
    "soil_clay_fraction_pct": "Soil clay fraction governing plasticity, cohesive shear strength, and liquefaction risk.",
    "aspect_degrees": "Hillslope sun/wind exposure orientation affecting soil moisture retention.",
    "plan_curvature": "Topographic curvature; concave slopes focus subsurface pore water flow.",
    "distance_to_road_km": "Proximity to anthropogenic road cuts and slope excavation destabilization.",
    "distance_to_stream_km": "Proximity to valley stream toe-erosion destabilizing slope base.",
    
    # Earthquakes
    "prior_count_365d_100km": "1-year regional background seismicity rate reflecting tectonic loading state.",
    "prior_count_30d_100km": "30-day precursory seismic activity indicating active micro-fracturing.",
    "focal_depth_km": "Mainshock hypocentral depth; shallow ruptures concentrate crustal stress triggering aftershocks.",
    "dist_to_active_fault_km": "Proximity to mapped GEM active faults capable of hosting secondary ruptures.",
    "nearest_fault_slip_type": "Tectonic faulting mechanism (thrust/strike-slip vs extensional normal faults).",
    "mainshock_mag": "Triggering earthquake moment magnitude dictating rupture surface area and energy.",
    "cumulative_energy_log_joules": "Log10 cumulative radiated seismic energy in the surrounding crustal volume.",
    "regional_b_value": "Gutenberg-Richter b-value; lower b-values indicate high ambient shear stress.",
    
    # Cyclones
    "past_delta_wind_6h": "6-hour intensification momentum indicating active inner-core vortex spin-up.",
    "past_delta_wind_12h": "12-hour sustained intensification trend.",
    "coriolis_param": "Coriolis parameter f = 2*Omega*sin(lat) providing planetary vorticity for vortex spin-up.",
    "current_wind_kt": "Current intensity determining existing storm structure and destructive wind field.",
    "past_delta_pres_6h": "6-hour central pressure drop reflecting deepening convective eyewall.",
    "pot_intensity_headroom": "Thermodynamic headroom beneath the ocean's Maximum Potential Intensity (MPI).",
    "dist_to_land_km": "Distance to land; approaching topography increases frictional dissipation.",
    "landfall_flag": "Landfall status; terrain interaction rapidly degrades storm energy source.",
    
    # Wildfires
    "relative_humidity_pct": "Surface atmospheric relative humidity governing fine dead fuel moisture equilibrium.",
    "fwi_fire_weather_index": "Canadian Forest Fire Weather Index integrating fuel moisture and fire spread potential.",
    "wind_speed_10m_ms": "Surface 10m wind speed driving flame front propagation and spot fire generation."
}

class ExplanationService:
    def __init__(self):
        self._explainers: Dict[str, shap.TreeExplainer] = {}

    def get_explainer(self, model_key: str, model: Any) -> shap.TreeExplainer:
        if model_key not in self._explainers:
            try:
                self._explainers[model_key] = shap.TreeExplainer(model)
            except Exception as e:
                logger.warning(f"Could not initialize TreeExplainer for {model_key}: {e}")
                return None
        return self._explainers[model_key]

    def explain_prediction(
        self,
        model_key: str,
        model: Any,
        features_df: pd.DataFrame,
        is_binary: bool = True,
        top_k: int = 5
    ) -> List[FeatureAttribution]:
        """
        Calculates local TreeSHAP attributions for a single-row feature DataFrame.
        """
        explainer = self.get_explainer(model_key, model)
        feature_names = features_df.columns.tolist()
        
        if explainer is None:
            # Fallback to feature importance if TreeExplainer fails
            importances = getattr(model, "feature_importances_", np.zeros(len(feature_names)))
            sorted_idx = np.argsort(importances)[::-1][:top_k]
            return [
                FeatureAttribution(
                    feature=feature_names[i],
                    importance_score=float(round(importances[i], 4)),
                    direction="RISK_INCREASING",
                    description=PHYSICAL_INTERPRETATIONS.get(feature_names[i], "Physical environmental predictor.")
                )
                for i in sorted_idx
            ]
            
        try:
            shap_values = explainer(features_df)
            raw_vals = shap_values.values
            
            # For binary classification or regression
            if len(raw_vals.shape) == 1:
                vals = raw_vals
            elif len(raw_vals.shape) == 2:
                vals = raw_vals[0]
            elif len(raw_vals.shape) == 3:
                # Multiclass (take active class index 1)
                vals = raw_vals[0, :, 1]
            else:
                vals = np.zeros(len(feature_names))
                
            abs_vals = np.abs(vals)
            sorted_indices = np.argsort(abs_vals)[::-1][:top_k]
            
            attributions = []
            for idx in sorted_indices:
                feat = feature_names[idx]
                score = float(round(vals[idx], 4))
                direction = "RISK_INCREASING" if score >= 0 else "RISK_DECREASING"
                desc = PHYSICAL_INTERPRETATIONS.get(feat, "Key physical and environmental predictor.")
                attributions.append(
                    FeatureAttribution(
                        feature=feat,
                        importance_score=score,
                        direction=direction,
                        description=desc
                    )
                )
            return attributions
            
        except Exception as e:
            logger.error(f"Error computing TreeSHAP for {model_key}: {e}")
            return []

explanation_service = ExplanationService()

