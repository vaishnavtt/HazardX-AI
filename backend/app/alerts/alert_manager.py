"""
HAZARDX AI — Alert Lifecycle & State Management Service
Manages alert generation, acknowledgement, resolution, expiration, and audit trails.
"""

from typing import List, Dict, Any, Optional, Tuple
from ..schemas.alert import (
    AlertItem,
    AlertListResponse,
    AlertSummaryResponse,
    AlertAuditLogItem,
    AlertSeverity,
    AlertStatus,
    HazardType
)
from ..services.data_storage_service import storage_service
from .alert_deduplication import alert_deduplicator
from ..utils.logging_config import get_logger

logger = get_logger("alert_manager")

class AlertManager:
    def __init__(self):
        pass

    def create_or_update_alert(self, alert_payload: Dict[str, Any]) -> Tuple[AlertItem, bool]:
        """
        Creates a new alert or escalates an existing active alert matching the deduplication key.
        Returns (AlertItem, is_new).
        """
        hazard = alert_payload["hazard_type"]
        lat = float(alert_payload["latitude"])
        lon = float(alert_payload["longitude"])

        if "dedup_key" not in alert_payload:
            pred_meta = alert_payload.get("model_prediction", {})
            horizon = pred_meta.get("forecast_horizon") if isinstance(pred_meta, dict) else None
            alert_payload["dedup_key"] = alert_deduplicator.generate_dedup_key(hazard, lat, lon, horizon=horizon)

        alert_id, is_new = storage_service.save_or_update_alert(alert_payload)
        saved = storage_service.get_alert(alert_id)
        if not saved:
            raise RuntimeError(f"Failed to retrieve saved alert {alert_id}")
        return (AlertItem(**saved), is_new)

    def get_alert(self, alert_id: str) -> Optional[AlertItem]:
        saved = storage_service.get_alert(alert_id)
        if saved:
            return AlertItem(**saved)
        return None

    def list_alerts(
        self,
        hazard_type: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        min_lat: Optional[float] = None,
        max_lat: Optional[float] = None,
        min_lon: Optional[float] = None,
        max_lon: Optional[float] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> AlertListResponse:
        items_dict, total = storage_service.query_alerts(
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

        alert_items = [AlertItem(**d) for d in items_dict]
        return AlertListResponse(
            total=total,
            page=page,
            page_size=page_size,
            items=alert_items
        )

    def acknowledge_alert(
        self,
        alert_id: str,
        acknowledged_by: str = "Duty Disaster Analyst",
        notes: Optional[str] = None
    ) -> Optional[AlertItem]:
        success = storage_service.update_alert_status(
            alert_id=alert_id,
            new_status="ACKNOWLEDGED",
            performed_by=acknowledged_by,
            notes=notes or "Operator acknowledged alert"
        )
        if success:
            return self.get_alert(alert_id)
        return None

    def resolve_alert(
        self,
        alert_id: str,
        resolved_by: str = "Operations Supervisor",
        resolution_notes: str = "Conditions normalized"
    ) -> Optional[AlertItem]:
        success = storage_service.update_alert_status(
            alert_id=alert_id,
            new_status="RESOLVED",
            performed_by=resolved_by,
            notes=resolution_notes
        )
        if success:
            return self.get_alert(alert_id)
        return None

    def expire_stale_alerts(self, max_age_hours: int = 48) -> int:
        return storage_service.expire_stale_alerts(max_age_hours=max_age_hours)

    def get_summary(self, monitor_status: Optional[Dict[str, Any]] = None) -> AlertSummaryResponse:
        metrics = storage_service.get_alert_summary_metrics()
        recent = [AlertItem(**r) for r in metrics["recent_alerts"]]

        return AlertSummaryResponse(
            total_active=metrics["total_active"],
            total_severe_red=metrics["total_severe_red"],
            total_high_orange=metrics["total_high_orange"],
            total_moderate_yellow=metrics["total_moderate_yellow"],
            by_hazard=metrics["by_hazard"],
            recent_alerts=recent,
            monitor_status=monitor_status or {"is_running": False, "mode": "idle"}
        )

    def get_audit_history(self, alert_id: Optional[str] = None, limit: int = 50) -> List[AlertAuditLogItem]:
        raw_logs = storage_service.get_alert_audit_logs(alert_id=alert_id, limit=limit)
        return [AlertAuditLogItem(**log) for log in raw_logs]

alert_manager = AlertManager()

