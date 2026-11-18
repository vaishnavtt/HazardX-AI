"""
HAZARDX AI — Prediction Inference Endpoints for All Five Hazards
"""

from datetime import datetime, timezone
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, status

from backend.app.schemas.flood import FloodFeatures, FloodPredictionResponse
from backend.app.schemas.landslide import LandslideFeatures, LandslidePredictionResponse
from backend.app.schemas.earthquake import EarthquakeFeatures, EarthquakePredictionResponse
from backend.app.schemas.cyclone import CycloneFeatures, CyclonePredictionResponse
from backend.app.schemas.wildfire import WildfireFeatures, WildfirePredictionResponse
from backend.app.schemas.combined import MultiHazardPredictionRequest, MultiHazardPredictionResponse

from backend.app.services.flood_service import flood_service
from backend.app.services.landslide_service import landslide_service
from backend.app.services.earthquake_service import earthquake_service
from backend.app.services.cyclone_service import cyclone_service
from backend.app.services.wildfire_service import wildfire_service
from backend.app.utils.logging_config import get_logger

logger = get_logger("predictions_api")
router = APIRouter()

ALERT_SEVERITY_ORDER = {
    "GREEN": 1,
    "YELLOW": 2,
    "ORANGE": 3,
    "RED": 4
}

@router.post("/predict/flood", response_model=FloodPredictionResponse, tags=["Hazard Predictions"])
def predict_flood(features: FloodFeatures) -> FloodPredictionResponse:
    """
    Evaluates fluvial/pluvial flood inundation probability and severity class.
    """
    try:
        return flood_service.predict(features)
    except Exception as e:
        logger.error(f"Error in flood prediction: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/predict/landslide", response_model=LandslidePredictionResponse, tags=["Hazard Predictions"])
def predict_landslide(features: LandslideFeatures) -> LandslidePredictionResponse:
    """
    Evaluates rainfall-triggered landslide slope failure susceptibility and magnitude.
    """
    try:
        return landslide_service.predict(features)
    except Exception as e:
        logger.error(f"Error in landslide prediction: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/predict/earthquake", response_model=EarthquakePredictionResponse, tags=["Hazard Predictions"])
def predict_earthquake(features: EarthquakeFeatures) -> EarthquakePredictionResponse:
    """
    Evaluates regional secondary aftershock clustering hazard following an M >= 5.0 mainshock.
    Mandatory Disclaimer: This is NOT an exact earthquake prediction.
    """
    try:
        return earthquake_service.predict(features)
    except Exception as e:
        logger.error(f"Error in earthquake aftershock prediction: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/predict/cyclone", response_model=CyclonePredictionResponse, tags=["Hazard Predictions"])
def predict_cyclone(features: CycloneFeatures) -> CyclonePredictionResponse:
    """
    Evaluates tropical cyclone 24-hour rapid intensification (RI) risk and continuous 24h intensity change.
    """
    try:
        return cyclone_service.predict(features)
    except Exception as e:
        logger.error(f"Error in cyclone prediction: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/predict/wildfire", response_model=WildfirePredictionResponse, tags=["Hazard Predictions"])
def predict_wildfire(features: WildfireFeatures) -> WildfirePredictionResponse:
    """
    Evaluates wildfire ignition susceptibility under fire weather conditions.
    """
    try:
        return wildfire_service.predict(features)
    except Exception as e:
        logger.error(f"Error in wildfire prediction: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/predict/all", response_model=MultiHazardPredictionResponse, tags=["Hazard Predictions"])
def predict_all(request: MultiHazardPredictionRequest) -> MultiHazardPredictionResponse:
    """
    Multi-hazard unified assessment: Evaluates any combination of provided hazard features
    and produces an integrated composite hazard alert level.
    """
    results: Dict[str, Any] = {}
    evaluated: List[str] = []
    highest_severity = 0
    highest_alert_str = "GREEN"

    # Evaluate floods
    if request.flood is not None:
        try:
            res = flood_service.predict(request.flood)
            results["flood"] = res.model_dump()
            evaluated.append("floods")
            sev = ALERT_SEVERITY_ORDER.get(res.alert_level, 1)
            if sev > highest_severity:
                highest_severity = sev
                highest_alert_str = res.alert_level
        except Exception as e:
            logger.error(f"Error in multi-hazard flood inference: {e}")
            results["flood"] = {"error": str(e)}

    # Evaluate landslides
    if request.landslide is not None:
        try:
            res = landslide_service.predict(request.landslide)
            results["landslide"] = res.model_dump()
            evaluated.append("landslides")
            sev = ALERT_SEVERITY_ORDER.get(res.alert_level, 1)
            if sev > highest_severity:
                highest_severity = sev
                highest_alert_str = res.alert_level
        except Exception as e:
            logger.error(f"Error in multi-hazard landslide inference: {e}")
            results["landslide"] = {"error": str(e)}

    # Evaluate earthquakes
    if request.earthquake is not None:
        try:
            res = earthquake_service.predict(request.earthquake)
            results["earthquake"] = res.model_dump()
            evaluated.append("earthquakes")
            sev = ALERT_SEVERITY_ORDER.get(res.alert_level, 1)
            if sev > highest_severity:
                highest_severity = sev
                highest_alert_str = res.alert_level
        except Exception as e:
            logger.error(f"Error in multi-hazard earthquake inference: {e}")
            results["earthquake"] = {"error": str(e)}

    # Evaluate cyclones
    if request.cyclone is not None:
        try:
            res = cyclone_service.predict(request.cyclone)
            results["cyclone"] = res.model_dump()
            evaluated.append("cyclones")
            sev = ALERT_SEVERITY_ORDER.get(res.alert_level, 1)
            if sev > highest_severity:
                highest_severity = sev
                highest_alert_str = res.alert_level
        except Exception as e:
            logger.error(f"Error in multi-hazard cyclone inference: {e}")
            results["cyclone"] = {"error": str(e)}

    # Evaluate wildfires
    if request.wildfire is not None:
        try:
            res = wildfire_service.predict(request.wildfire)
            results["wildfire"] = res.model_dump()
            evaluated.append("wildfires")
            sev = ALERT_SEVERITY_ORDER.get(res.alert_level, 1)
            if sev > highest_severity:
                highest_severity = sev
                highest_alert_str = res.alert_level
        except Exception as e:
            logger.error(f"Error in multi-hazard wildfire inference: {e}")
            results["wildfire"] = {"error": str(e)}

    if not evaluated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one hazard feature set must be provided in the request."
        )

    return MultiHazardPredictionResponse(
        timestamp=datetime.now(timezone.utc).isoformat(),
        hazards_evaluated=evaluated,
        composite_highest_alert_level=highest_alert_str,
        results=results
    )
