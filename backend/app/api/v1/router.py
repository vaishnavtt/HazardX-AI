"""
HAZARDX AI — API v1 Router Aggregator
"""

from fastapi import APIRouter
from .endpoints import health, models, predictions, explanations, dashboard, live_data, geospatial, alerts, forecasts, intelligence

api_router = APIRouter()

# Include all sub-routers
api_router.include_router(health.router)
api_router.include_router(models.router)
api_router.include_router(predictions.router)
api_router.include_router(explanations.router)
api_router.include_router(dashboard.router)
api_router.include_router(live_data.router)
api_router.include_router(geospatial.router)
api_router.include_router(alerts.router)
api_router.include_router(forecasts.router)
api_router.include_router(intelligence.router)

