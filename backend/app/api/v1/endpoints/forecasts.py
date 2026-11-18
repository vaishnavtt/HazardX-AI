"""
HAZARDX AI — Multi-Hazard Forecasting & Early Warning Endpoints
Serves forward-looking predictive risk assessments, multi-horizon timelines (6h, 12h, 24h, 48h, 72h),
and location-specific multi-hazard forecast synthesis.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query, HTTPException, status, Path

from backend.app.schemas.forecast import (
    ForecastHorizon,
    RiskCategory,
    SingleHazardForecast,
    HazardForecastTimeline,
    ForecastSummaryCard,
    LocationForecastRequest,
    MultiHazardLocationForecastResponse
)
from backend.app.forecasting.forecast_service import forecast_service
from backend.app.forecasting.forecast_registry import FORECAST_REGISTRY
from backend.app.services.data_storage_service import storage_service
from backend.app.utils.logging_config import get_logger

logger = get_logger("forecasts_api")
router = APIRouter(prefix="/forecasts", tags=["Multi-Hazard Forecasting"])

# Default representative monitoring stations for global overview
REPRESENTATIVE_BASINS = {
    "floods": {"name": "Lower Mississippi River Reach", "lat": 29.95, "lon": -90.07},
    "landslides": {"name": "Himalayan Corridor (Uttarakhand)", "lat": 30.3165, "lon": 78.0322},
    "wildfires": {"name": "Southern California Chaparral Basin", "lat": 34.05, "lon": -118.25},
    "earthquakes": {"name": "San Andreas Fault Zone (Ridgecrest)", "lat": 35.62, "lon": -117.67},
    "cyclones": {"name": "Western North Atlantic Tropical Basin", "lat": 25.0, "lon": -75.0}
}

@router.get("/summary", response_model=List[ForecastSummaryCard])
async def get_forecast_summary() -> List[ForecastSummaryCard]:
    """
    Returns high-level multi-hazard forecast cards across all five hazards for the next 24-hour horizon.
    """
    cards = []
    try:
        # Floods
        f_b = REPRESENTATIVE_BASINS["floods"]
        f_fc, f_time = await forecast_service.forecast_flood(f_b["lat"], f_b["lon"], f_b["name"])
        cards.append(ForecastSummaryCard(
            hazard_type="floods",
            current_status="MONITORING",
            forecast_risk=f_fc.risk_category,
            forecast_horizon=f_fc.forecast_horizon,
            peak_score=f_time.peak_risk_score,
            last_updated=f_fc.forecast_generated_at,
            main_contributing_factors=["GloFAS River Discharge Forecast", "7-Day Cumulative Runoff"],
            primary_data_source=f_fc.data_sources[0] if f_fc.data_sources else "Copernicus GloFAS",
            data_provenance=f_fc.data_provenance,
            model_status="OPERATIONAL",
            trend=f_time.overall_trend
        ))

        # Landslides
        ls_b = REPRESENTATIVE_BASINS["landslides"]
        ls_fc, ls_time = await forecast_service.forecast_landslide(ls_b["lat"], ls_b["lon"], ls_b["name"])
        cards.append(ForecastSummaryCard(
            hazard_type="landslides",
            current_status="MONITORING",
            forecast_risk=ls_fc.risk_category,
            forecast_horizon=ls_fc.forecast_horizon,
            peak_score=ls_time.peak_risk_score,
            last_updated=ls_fc.forecast_generated_at,
            main_contributing_factors=["Forecast Rainfall Infiltration", "Geotechnical Slope Stability"],
            primary_data_source=ls_fc.data_sources[0] if ls_fc.data_sources else "Open-Meteo NWP",
            data_provenance=ls_fc.data_provenance,
            model_status="OPERATIONAL",
            trend=ls_time.overall_trend
        ))

        # Wildfires
        wf_b = REPRESENTATIVE_BASINS["wildfires"]
        wf_fc, wf_time = await forecast_service.forecast_wildfire(wf_b["lat"], wf_b["lon"], wf_b["name"])
        cards.append(ForecastSummaryCard(
            hazard_type="wildfires",
            current_status="ACTIVE",
            forecast_risk=wf_fc.risk_category,
            forecast_horizon=wf_fc.forecast_horizon,
            peak_score=wf_time.peak_risk_score,
            last_updated=wf_fc.forecast_generated_at,
            main_contributing_factors=["Forecast Max Temperature", "Min Relative Humidity", "Wind Gusts"],
            primary_data_source=wf_fc.data_sources[0] if wf_fc.data_sources else "Open-Meteo Weather",
            data_provenance=wf_fc.data_provenance,
            model_status="OPERATIONAL (Duration BLOCKED)",
            trend=wf_time.overall_trend
        ))

        # Earthquakes
        eq_b = REPRESENTATIVE_BASINS["earthquakes"]
        eq_fc, eq_time = await forecast_service.forecast_earthquake(eq_b["lat"], eq_b["lon"], eq_b["name"])
        cards.append(ForecastSummaryCard(
            hazard_type="earthquakes",
            current_status="SEISMIC_SURVEILLANCE",
            forecast_risk=eq_fc.risk_category,
            forecast_horizon=eq_fc.forecast_horizon,
            peak_score=eq_time.peak_risk_score,
            last_updated=eq_fc.forecast_generated_at,
            main_contributing_factors=["USGS Real-Time ComCat", "Omori-Utsu Temporal Decay Law"],
            primary_data_source="USGS ComCat",
            data_provenance=eq_fc.data_provenance,
            model_status="OPERATIONAL (Probabilistic Aftershocks Only)",
            trend="DECREASING"
        ))

        # Cyclones
        cy_b = REPRESENTATIVE_BASINS["cyclones"]
        cy_fc, cy_time = await forecast_service.forecast_cyclone(cy_b["lat"], cy_b["lon"], cy_b["name"])
        cards.append(ForecastSummaryCard(
            hazard_type="cyclones",
            current_status="ADVISORY_WATCH",
            forecast_risk=cy_fc.risk_category,
            forecast_horizon=cy_fc.forecast_horizon,
            peak_score=cy_time.peak_risk_score,
            last_updated=cy_fc.forecast_generated_at,
            main_contributing_factors=["24h Rapid Intensification Risk", "SST & Vertical Wind Shear"],
            primary_data_source="NOAA National Hurricane Center",
            data_provenance=cy_fc.data_provenance,
            model_status="OPERATIONAL",
            trend=cy_time.overall_trend
        ))

        return cards
    except Exception as e:
        logger.error(f"Error serving forecast summary cards: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/timeline", response_model=HazardForecastTimeline)
async def get_hazard_forecast_timeline(
    hazard: str = Query(..., description="Hazard domain: floods, landslides, wildfires, earthquakes, cyclones"),
    lat: Optional[float] = Query(None, ge=-90.0, le=90.0),
    lon: Optional[float] = Query(None, ge=-180.0, le=180.0),
    location_name: Optional[str] = Query(None)
) -> HazardForecastTimeline:
    """
    Returns the multi-horizon timeline breakdown (6h, 12h, 24h, 48h, 72h) for a specific hazard.
    """
    h_lower = hazard.lower()
    if h_lower not in REPRESENTATIVE_BASINS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported hazard '{hazard}'. Must be one of {list(REPRESENTATIVE_BASINS.keys())}"
        )

    coords = REPRESENTATIVE_BASINS[h_lower]
    target_lat = lat if lat is not None else coords["lat"]
    target_lon = lon if lon is not None else coords["lon"]
    loc_str = location_name or coords["name"]

    try:
        if h_lower == "floods":
            _, timeline = await forecast_service.forecast_flood(target_lat, target_lon, loc_str)
        elif h_lower == "landslides":
            _, timeline = await forecast_service.forecast_landslide(target_lat, target_lon, loc_str)
        elif h_lower == "wildfires":
            _, timeline = await forecast_service.forecast_wildfire(target_lat, target_lon, loc_str)
        elif h_lower == "earthquakes":
            _, timeline = await forecast_service.forecast_earthquake(target_lat, target_lon, loc_str)
        elif h_lower == "cyclones":
            _, timeline = await forecast_service.forecast_cyclone(target_lat, target_lon, loc_str)
        else:
            raise HTTPException(status_code=400, detail="Invalid hazard")

        return timeline
    except Exception as e:
        logger.error(f"Error serving forecast timeline for {hazard}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/assess-location", response_model=MultiHazardLocationForecastResponse)
async def assess_location_forecast(request: LocationForecastRequest) -> MultiHazardLocationForecastResponse:
    """
    Performs comprehensive multi-hazard predictive risk assessment for an arbitrary geographic coordinate
    across all standard forecast horizons (6h, 12h, 24h, 48h, 72h).
    """
    try:
        response = await forecast_service.assess_location_forecast(
            lat=request.latitude,
            lon=request.longitude,
            location_name=request.location_name or f"Point ({request.latitude:.2f}, {request.longitude:.2f})",
            hazards=request.hazards
        )

        # Persist summary record in hazard_forecasts table
        storage_service.save_hazard_forecast({
            "hazard_type": response.primary_hazard,
            "location_name": response.location_name,
            "latitude": response.latitude,
            "longitude": response.longitude,
            "forecast_horizon": "24h",
            "risk_score": response.composite_risk_score,
            "risk_category": response.composite_risk_category.value,
            "valid_from": response.generated_at,
            "valid_until": response.generated_at
        })

        return response
    except Exception as e:
        logger.error(f"Error assessing location forecast: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/evaluations")
async def get_forecast_evaluations() -> Dict[str, Any]:
    """
    Returns validated quantitative performance benchmarks, Brier scores, and time-aware evaluation
    metrics across 6h, 12h, 24h, 48h, and 72h horizons.
    """
    return {
        "framework": "HAZARDX AI Time-Aware Multi-Horizon Validation Suite",
        "evaluation_timestamp": "2026-11-18T06:50:00Z",
        "forecast_registry": FORECAST_REGISTRY,
        "governance_status": {
            "earthquakes_aftershock_count": "BLOCKED (R² = -0.0401; suppressed)",
            "wildfires_fire_duration": "BLOCKED (R² = -214.75; suppressed)"
        }
    }
