"""
HAZARDX AI — Health Check Endpoint
"""

from datetime import datetime, timezone
from fastapi import APIRouter
from backend.app.schemas.common import HealthResponse
from backend.app.services.model_registry import registry
from backend.app.config import settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["System Health"])
def get_health() -> HealthResponse:
    """
    Returns system status, loaded model counts, and operational health status.
    """
    operational = []
    experimental = []
    
    for key in registry.models.keys():
        status = settings.MODEL_STATUS.get(key, "OPERATIONAL")
        if status == "OPERATIONAL":
            operational.append(key)
        elif status == "EXPERIMENTAL":
            experimental.append(key)
            
    return HealthResponse(
        status="healthy" if len(operational) > 0 else "degraded",
        version="1.0.0",
        service="HAZARDX AI Early Warning Backend",
        models_loaded=len(registry.models),
        operational_models=operational,
        experimental_models=experimental,
        timestamp=datetime.now(timezone.utc).isoformat()
    )
