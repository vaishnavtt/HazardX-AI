"""
HAZARDX AI — Alert Management & Early Warning REST API Endpoints
Provides alert querying, lifecycle management (acknowledge/resolve),
summary metrics, audit logging, and background monitor control.
"""

from typing import Optional
from fastapi import APIRouter, Query, Path, HTTPException, status
from backend.app.schemas.alert import (
    AlertItem,
    AlertListResponse,
    AlertSummaryResponse,
    AlertAuditLogItem,
    AlertAcknowledgeRequest,
    AlertResolveRequest,
    MonitorStatusResponse
)
from backend.app.alerts.alert_manager import alert_manager
from backend.app.alerts.alert_monitor import alert_monitor
from backend.app.utils.logging_config import get_logger

logger = get_logger("alerts_api")
router = APIRouter(prefix="/alerts", tags=["Intelligent Early Warning"])

@router.get("", response_model=AlertListResponse)
def list_alerts(
    hazard_type: Optional[str] = Query(None, description="Filter by hazard: floods, landslides, earthquakes, cyclones, wildfires"),
    severity: Optional[str] = Query(None, pattern="^(GREEN|YELLOW|ORANGE|RED)$", description="Filter by alert severity"),
    status: Optional[str] = Query(None, pattern="^(ACTIVE|ACKNOWLEDGED|RESOLVED|EXPIRED)$", description="Filter by lifecycle status"),
    min_lat: Optional[float] = Query(None, ge=-90.0, le=90.0),
    max_lat: Optional[float] = Query(None, ge=-90.0, le=90.0),
    min_lon: Optional[float] = Query(None, ge=-180.0, le=180.0),
    max_lon: Optional[float] = Query(None, ge=-180.0, le=180.0),
    start_date: Optional[str] = Query(None, description="ISO timestamp start filter"),
    end_date: Optional[str] = Query(None, description="ISO timestamp end filter"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size")
) -> AlertListResponse:
    """
    Returns a paginated list of multi-hazard alerts with extensive geographic, hazard, and severity filters.
    """
    try:
        return alert_manager.list_alerts(
            hazard_type=hazard_type,
            severity=severity,
            status=status,
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
            start_date=start_date,
            end_date=end_date,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        logger.error(f"Error querying alerts: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/summary", response_model=AlertSummaryResponse)
def get_alert_summary() -> AlertSummaryResponse:
    """
    Provides an operational summary of active alerts, severe threats, hazard breakdowns, and recent events.
    """
    try:
        mon_status = alert_monitor.get_status().model_dump()
        return alert_manager.get_summary(monitor_status=mon_status)
    except Exception as e:
        logger.error(f"Error serving alert summary: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/history", response_model=list[AlertAuditLogItem])
def get_alert_history(
    alert_id: Optional[str] = Query(None, description="Filter audit log by specific alert ID"),
    limit: int = Query(50, ge=1, le=200, description="Max audit entries to return")
) -> list[AlertAuditLogItem]:
    """
    Retrieves full audit trails of alert status transitions (generated, escalated, acknowledged, resolved, expired).
    """
    try:
        return alert_manager.get_audit_history(alert_id=alert_id, limit=limit)
    except Exception as e:
        logger.error(f"Error serving alert audit history: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/monitor/status", response_model=MonitorStatusResponse)
def get_monitor_status() -> MonitorStatusResponse:
    """
    Reports background alert monitoring worker health, cycle count, and last execution telemetry.
    """
    try:
        return alert_monitor.get_status()
    except Exception as e:
        logger.error(f"Error serving monitor status: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/monitor/trigger")
async def trigger_monitor_cycle():
    """
    Manually triggers an immediate alert monitoring and evaluation cycle.
    """
    try:
        result = await alert_monitor.trigger_cycle()
        return result
    except Exception as e:
        logger.error(f"Error triggering alert cycle: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{alert_id}", response_model=AlertItem)
def get_alert_detail(
    alert_id: str = Path(..., description="Unique alert identifier")
) -> AlertItem:
    """
    Retrieves detailed information for a single alert.
    """
    alert = alert_manager.get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert '{alert_id}' not found.")
    return alert

@router.post("/{alert_id}/acknowledge", response_model=AlertItem)
def acknowledge_alert(
    alert_id: str = Path(..., description="Unique alert identifier"),
    payload: AlertAcknowledgeRequest = AlertAcknowledgeRequest()
) -> AlertItem:
    """
    Sets alert status to ACKNOWLEDGED with operator identity and audit tracking.
    """
    updated = alert_manager.acknowledge_alert(
        alert_id=alert_id,
        acknowledged_by=payload.acknowledged_by,
        notes=payload.notes
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert '{alert_id}' not found.")
    return updated

@router.post("/{alert_id}/resolve", response_model=AlertItem)
def resolve_alert(
    alert_id: str = Path(..., description="Unique alert identifier"),
    payload: AlertResolveRequest = AlertResolveRequest(resolved_by="Operations Supervisor", resolution_notes="Hazard dissipated")
) -> AlertItem:
    """
    Resolves an active alert with required resolution documentation and audit tracking.
    """
    updated = alert_manager.resolve_alert(
        alert_id=alert_id,
        resolved_by=payload.resolved_by,
        resolution_notes=payload.resolution_notes
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert '{alert_id}' not found.")
    return updated

