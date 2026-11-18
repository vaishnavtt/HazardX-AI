"""
HAZARDX AI — External Intelligence Telemetry, Freshness & Ingestion Endpoints
Serves comprehensive provider registry, latency telemetry, data freshness tiers,
and scheduler control operations.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status

from backend.app.ingestion.ingestion_manager import ingestion_manager
from backend.app.ingestion.scheduler import scheduler
from backend.app.services.data_storage_service import storage_service
from backend.app.utils.logging_config import get_logger

logger = get_logger("intelligence_api")
router = APIRouter(prefix="", tags=["Disaster Intelligence & Ingestion Telemetry"])

@router.get("/intelligence/sources")
async def get_intelligence_sources() -> List[Dict[str, Any]]:
    """
    Returns the complete registry of authoritative scientific data sources with endpoints,
    authentication requirements, and update intervals.
    """
    try:
        return ingestion_manager.get_source_registry_status()
    except Exception as e:
        logger.error(f"Error fetching intelligence sources: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/intelligence/health")
async def get_intelligence_health() -> Dict[str, Any]:
    """
    Returns live health telemetry, HTTP response codes, and latency metrics across all feeds.
    """
    try:
        sources = ingestion_manager.get_source_registry_status()
        healthy_count = sum(1 for s in sources if s["health_status"] == "HEALTHY")
        degraded_count = sum(1 for s in sources if s["health_status"] == "DEGRADED")

        overall = "HEALTHY" if healthy_count == len(sources) else "DEGRADED" if healthy_count > 0 else "UNAVAILABLE"

        return {
            "overall_status": overall,
            "total_sources": len(sources),
            "healthy_count": healthy_count,
            "degraded_count": degraded_count,
            "active_cache_entries": storage_service.get_active_cache_count(),
            "sources": sources
        }
    except Exception as e:
        logger.error(f"Error fetching intelligence health: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/intelligence/freshness")
async def get_intelligence_freshness() -> Dict[str, Any]:
    """
    Returns detailed age analysis, freshness tiers (FRESH, ACCEPTABLE, STALE, UNAVAILABLE),
    and provenance classifications.
    """
    try:
        sources = ingestion_manager.get_source_registry_status()
        stale_sources = [s["source_id"] for s in sources if s["is_stale"]]

        return {
            "all_fresh": len(stale_sources) == 0,
            "stale_source_count": len(stale_sources),
            "stale_sources": stale_sources,
            "sources": [
                {
                    "source_id": s["source_id"],
                    "name": s["name"],
                    "data_category": s["data_category"],
                    "freshness_status": s["freshness_status"],
                    "age_human": s["age_human"],
                    "is_stale": s["is_stale"],
                    "last_checked": s["last_checked"]
                }
                for s in sources
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching intelligence freshness: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/ingestion/status")
async def get_ingestion_status() -> Dict[str, Any]:
    """
    Returns background ingestion scheduler status, polling interval, and last execution summary.
    """
    return scheduler.get_status()

@router.post("/ingestion/trigger")
async def trigger_ingestion_cycle() -> Dict[str, Any]:
    """
    Manually triggers an immediate ingestion cycle across all active scientific feeds.
    """
    try:
        summary = await scheduler.trigger_cycle()
        return summary
    except Exception as e:
        logger.error(f"Error triggering manual ingestion cycle: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
