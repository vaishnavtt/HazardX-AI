"""
HAZARDX AI — Alert Management Pydantic Schemas
Defines request/response models for intelligent early warnings,
severity levels, alert lifecycle states, and notification tracking.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

AlertSeverity = Literal["GREEN", "YELLOW", "ORANGE", "RED"]
AlertStatus = Literal["ACTIVE", "ACKNOWLEDGED", "RESOLVED", "EXPIRED"]
HazardType = Literal["floods", "landslides", "earthquakes", "cyclones", "wildfires"]

class AlertItem(BaseModel):
    alert_id: str
    hazard_type: HazardType
    severity: AlertSeverity
    title: str
    description: str
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    location_name: Optional[str] = None
    source: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    status: AlertStatus = "ACTIVE"
    model_prediction: Dict[str, Any] = Field(default_factory=dict)
    guidance: str
    created_at: str
    updated_at: str
    acknowledged_at: Optional[str] = None
    acknowledged_by: Optional[str] = None
    resolved_at: Optional[str] = None
    resolved_by: Optional[str] = None
    resolution_notes: Optional[str] = None
    dedup_key: str
    notification_sent: bool = False
    disclaimer: str = (
        "HAZARDX AI Decision Support Advisory — Artificial intelligence disaster intelligence. "
        "Not an official government evacuation order. Official civil protection advisories supersede this assessment."
    )

class AlertCreateRequest(BaseModel):
    hazard_type: HazardType
    severity: AlertSeverity
    title: str
    description: str
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    location_name: Optional[str] = None
    source: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    model_prediction: Optional[Dict[str, Any]] = None
    guidance: str

class AlertAcknowledgeRequest(BaseModel):
    acknowledged_by: str = Field(default="Duty Disaster Analyst", min_length=2, max_length=100)
    notes: Optional[str] = None

class AlertResolveRequest(BaseModel):
    resolved_by: str = Field(default="Operations Supervisor", min_length=2, max_length=100)
    resolution_notes: str = Field(..., min_length=3, max_length=1000)

class AlertAuditLogItem(BaseModel):
    id: int
    alert_id: str
    previous_status: Optional[str]
    new_status: str
    action_type: str
    performed_by: str
    notes: Optional[str]
    timestamp: str

class AlertListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[AlertItem]

class AlertSummaryResponse(BaseModel):
    total_active: int
    total_severe_red: int
    total_high_orange: int
    total_moderate_yellow: int
    by_hazard: Dict[str, int]
    recent_alerts: List[AlertItem]
    monitor_status: Dict[str, Any]
    data_policy: str = "Authentic scientific observations & calibrated XGBoost models only."

class MonitorStatusResponse(BaseModel):
    is_running: bool
    interval_seconds: int
    last_run_timestamp: Optional[str]
    next_run_timestamp: Optional[str]
    total_cycles_completed: int
    total_alerts_generated: int
    total_alerts_updated: int
    last_cycle_duration_ms: Optional[float]
    last_error: Optional[str]

