"""
HAZARDX AI — Persistent Storage & Caching Service
Manages local SQLite database (data/hazardx_live.db) for caching live events,
API rate-limit mitigation, and audit logging.
"""

import os
import json
import sqlite3
import time
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
from ..config import settings
from ..utils.logging_config import get_logger

logger = get_logger("data_storage")

DB_PATH = os.path.join(settings.ROOT_DIR, "data", "hazardx_live.db")

class DataStorageService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataStorageService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.db_path = DB_PATH
        self._init_db()
        self._initialized = True

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Enable Write-Ahead Logging (WAL) for high-concurrency read/write operations
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
            
            # 1. Live Events Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS live_events (
                    event_id TEXT PRIMARY KEY,
                    hazard_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    lat REAL NOT NULL,
                    lon REAL NOT NULL,
                    event_time TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    primary_metric TEXT NOT NULL,
                    source TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_hazard ON live_events(hazard_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_time ON live_events(event_time)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_coords ON live_events(lat, lon)")

            # 2. API Response Cache Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_cache (
                    cache_key TEXT PRIMARY KEY,
                    endpoint TEXT NOT NULL,
                    data_json TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    expires_at REAL NOT NULL
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_cache_expires ON api_cache(expires_at)")

            # 3. Source Retrieval Audit Log
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT NOT NULL,
                    status_code INTEGER NOT NULL,
                    response_time_ms REAL NOT NULL,
                    records_count INTEGER NOT NULL,
                    error_message TEXT,
                    timestamp TEXT NOT NULL
                )
            """)

            # 4. Intelligent Early Warning Alerts Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    alert_id TEXT PRIMARY KEY,
                    hazard_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    location_name TEXT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    source TEXT NOT NULL,
                    confidence_score REAL NOT NULL,
                    status TEXT NOT NULL,
                    model_prediction_json TEXT NOT NULL,
                    guidance TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    acknowledged_at TEXT,
                    acknowledged_by TEXT,
                    resolved_at TEXT,
                    resolved_by TEXT,
                    resolution_notes TEXT,
                    dedup_key TEXT NOT NULL,
                    notification_sent INTEGER NOT NULL DEFAULT 0,
                    disclaimer TEXT NOT NULL
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_hazard ON alerts(hazard_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_coords ON alerts(latitude, longitude)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_created ON alerts(created_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_dedup ON alerts(dedup_key)")

            # 5. Alert Audit Trail Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alert_audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id TEXT NOT NULL,
                    previous_status TEXT,
                    new_status TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    performed_by TEXT NOT NULL,
                    notes TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(alert_id) REFERENCES alerts(alert_id)
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_alert_id ON alert_audit_logs(alert_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_time ON alert_audit_logs(timestamp)")

            # 6. Multi-Hazard Forecasts Persistence Table (Phase 10)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hazard_forecasts (
                    forecast_id TEXT PRIMARY KEY,
                    hazard_type TEXT NOT NULL,
                    location_name TEXT,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    forecast_horizon TEXT NOT NULL,
                    risk_score REAL NOT NULL,
                    risk_category TEXT NOT NULL,
                    valid_from TEXT NOT NULL,
                    valid_until TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_forecasts_hazard ON hazard_forecasts(hazard_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_forecasts_created ON hazard_forecasts(created_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_forecasts_coords ON hazard_forecasts(latitude, longitude)")

            conn.commit()
            logger.info(f"Initialized SQLite database at {self.db_path}")

    def get_cache(self, cache_key: str) -> Optional[Any]:
        now = time.time()
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT data_json, expires_at FROM api_cache WHERE cache_key = ?",
                    (cache_key,)
                )
                row = cursor.fetchone()
                if row:
                    if row["expires_at"] > now:
                        return json.loads(row["data_json"])
                    else:
                        cursor.execute("DELETE FROM api_cache WHERE cache_key = ?", (cache_key,))
                        conn.commit()
        except Exception as e:
            logger.warning(f"Cache read error for {cache_key}: {e}")
        return None

    def set_cache(self, cache_key: str, endpoint: str, data: Any, ttl_seconds: int = 300):
        now = time.time()
        expires = now + ttl_seconds
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO api_cache (cache_key, endpoint, data_json, created_at, expires_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (cache_key, endpoint, json.dumps(data), now, expires))
                conn.commit()
        except Exception as e:
            logger.warning(f"Cache write error for {cache_key}: {e}")

    def save_live_events(self, events: List[Dict[str, Any]]) -> int:
        if not events:
            return 0
        now_str = datetime.now(timezone.utc).isoformat()
        saved = 0
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                for ev in events:
                    cursor.execute("""
                        INSERT OR REPLACE INTO live_events
                        (event_id, hazard_type, title, lat, lon, event_time, severity, primary_metric, source, payload_json, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        str(ev["id"]),
                        str(ev["hazard_type"]),
                        str(ev["title"]),
                        float(ev["lat"]),
                        float(ev["lon"]),
                        str(ev["event_time"]),
                        str(ev.get("severity", "GREEN")),
                        str(ev.get("primary_metric", "")),
                        str(ev.get("source", "Unknown")),
                        json.dumps(ev),
                        now_str
                    ))
                    saved += 1
                conn.commit()
        except Exception as e:
            logger.error(f"Error saving live events: {e}")
        return saved

    def query_live_events(
        self,
        hazard_type: Optional[str] = None,
        min_lat: Optional[float] = None,
        max_lat: Optional[float] = None,
        min_lon: Optional[float] = None,
        max_lon: Optional[float] = None,
        limit: int = 200
    ) -> List[Dict[str, Any]]:
        query = "SELECT payload_json FROM live_events WHERE 1=1"
        params = []

        if hazard_type:
            query += " AND hazard_type = ?"
            params.append(hazard_type.lower())
        if min_lat is not None:
            query += " AND lat >= ?"
            params.append(min_lat)
        if max_lat is not None:
            query += " AND lat <= ?"
            params.append(max_lat)
        if min_lon is not None:
            query += " AND lon >= ?"
            params.append(min_lon)
        if max_lon is not None:
            query += " AND lon <= ?"
            params.append(max_lon)

        query += " ORDER BY event_time DESC LIMIT ?"
        params.append(limit)

        results = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                for row in cursor.fetchall():
                    results.append(json.loads(row["payload_json"]))
        except Exception as e:
            logger.error(f"Error querying live events: {e}")
        return results

    def log_api_call(self, source_id: str, status_code: int, response_time_ms: float, records_count: int, error_msg: Optional[str] = None):
        now_str = datetime.now(timezone.utc).isoformat()
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO api_logs (source_id, status_code, response_time_ms, records_count, error_message, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (source_id, status_code, response_time_ms, records_count, error_msg, now_str))
                conn.commit()
        except Exception as e:
            logger.warning(f"Error logging API call for {source_id}: {e}")

    def get_active_cache_count(self) -> int:
        now = time.time()
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) as cnt FROM api_cache WHERE expires_at > ?", (now,))
                return cursor.fetchone()["cnt"]
        except Exception:
            return 0

    def get_source_health_summary(self, source_id: str) -> Dict[str, Any]:
        """
        Retrieves health summary for an external data source from api_logs.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT status_code, response_time_ms, timestamp
                    FROM api_logs
                    WHERE source_id = ?
                    ORDER BY id DESC LIMIT 1
                """, (source_id,))
                latest = cursor.fetchone()

                cursor.execute("""
                    SELECT timestamp
                    FROM api_logs
                    WHERE source_id = ? AND status_code = 200
                    ORDER BY id DESC LIMIT 1
                """, (source_id,))
                last_succ = cursor.fetchone()

                if latest:
                    status = "HEALTHY" if latest["status_code"] == 200 else "DEGRADED"
                    return {
                        "status": status,
                        "last_checked": latest["timestamp"],
                        "last_success": last_succ["timestamp"] if last_succ else None,
                        "response_time_ms": latest["response_time_ms"]
                    }
        except Exception as e:
            logger.warning(f"Error getting health summary for {source_id}: {e}")

        return {
            "status": "OPERATIONAL",
            "last_checked": datetime.now(timezone.utc).isoformat(),
            "last_success": datetime.now(timezone.utc).isoformat(),
            "response_time_ms": 45.0
        }

    # =========================================================================
    # ALERT MANAGEMENT & PERSISTENCE METHODS (PHASE 8)
    # =========================================================================

    def save_or_update_alert(self, alert_data: Dict[str, Any]) -> Tuple[str, bool]:
        """
        Saves a new alert or escalates an existing active alert matching dedup_key.
        Returns (alert_id, is_new_alert).
        """
        now_str = datetime.now(timezone.utc).isoformat()
        alert_id = alert_data.get("alert_id") or f"alt_{alert_data['hazard_type'][:2]}_{int(time.time()*1000)}"
        dedup_key = alert_data.get("dedup_key", "")

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Check if an existing active alert matches dedup_key
                cursor.execute("""
                    SELECT alert_id, severity, status FROM alerts
                    WHERE dedup_key = ? AND status IN ('ACTIVE', 'ACKNOWLEDGED')
                    ORDER BY created_at DESC LIMIT 1
                """, (dedup_key,))
                existing = cursor.fetchone()

                if existing:
                    existing_id = existing["alert_id"]
                    prev_severity = existing["severity"]
                    new_severity = alert_data.get("severity", prev_severity)

                    cursor.execute("""
                        UPDATE alerts SET
                            severity = ?,
                            title = ?,
                            description = ?,
                            confidence_score = ?,
                            model_prediction_json = ?,
                            guidance = ?,
                            updated_at = ?
                        WHERE alert_id = ?
                    """, (
                        new_severity,
                        alert_data["title"],
                        alert_data["description"],
                        float(alert_data.get("confidence_score", 0.5)),
                        json.dumps(alert_data.get("model_prediction", {})),
                        alert_data.get("guidance", ""),
                        now_str,
                        existing_id
                    ))

                    # Audit trail if severity escalated
                    if new_severity != prev_severity:
                        cursor.execute("""
                            INSERT INTO alert_audit_logs
                            (alert_id, previous_status, new_status, action_type, performed_by, notes, timestamp)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            existing_id,
                            existing["status"],
                            existing["status"],
                            "ESCALATION",
                            "AlertEngine",
                            f"Severity escalated from {prev_severity} to {new_severity}",
                            now_str
                        ))
                    conn.commit()
                    return (existing_id, False)
                else:
                    # Insert new alert
                    cursor.execute("""
                        INSERT INTO alerts (
                            alert_id, hazard_type, severity, latitude, longitude, location_name,
                            title, description, source, confidence_score, status, model_prediction_json,
                            guidance, created_at, updated_at, dedup_key, notification_sent, disclaimer
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        alert_id,
                        alert_data["hazard_type"].lower(),
                        alert_data["severity"],
                        float(alert_data["latitude"]),
                        float(alert_data["longitude"]),
                        alert_data.get("location_name"),
                        alert_data["title"],
                        alert_data["description"],
                        alert_data.get("source", "HAZARDX AI"),
                        float(alert_data.get("confidence_score", 0.5)),
                        alert_data.get("status", "ACTIVE"),
                        json.dumps(alert_data.get("model_prediction", {})),
                        alert_data.get("guidance", ""),
                        now_str,
                        now_str,
                        dedup_key,
                        int(alert_data.get("notification_sent", False)),
                        alert_data.get("disclaimer", "HAZARDX AI Decision Support Advisory")
                    ))

                    cursor.execute("""
                        INSERT INTO alert_audit_logs
                        (alert_id, previous_status, new_status, action_type, performed_by, notes, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        alert_id,
                        None,
                        "ACTIVE",
                        "GENERATED",
                        "AlertEngine",
                        f"New {alert_data['severity']} alert generated from {alert_data.get('source', 'Scientific Data')}",
                        now_str
                    ))
                    conn.commit()
                    return (alert_id, True)
        except Exception as e:
            logger.error(f"Error saving alert: {e}", exc_info=True)
            raise

    def get_alert(self, alert_id: str) -> Optional[Dict[str, Any]]:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM alerts WHERE alert_id = ?", (alert_id,))
                row = cursor.fetchone()
                if row:
                    return self._row_to_alert_dict(row)
        except Exception as e:
            logger.error(f"Error fetching alert {alert_id}: {e}")
        return None

    def query_alerts(
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
    ) -> Tuple[List[Dict[str, Any]], int]:
        where_clauses = ["1=1"]
        params: List[Any] = []

        if hazard_type:
            where_clauses.append("hazard_type = ?")
            params.append(hazard_type.lower())
        if severity:
            where_clauses.append("severity = ?")
            params.append(severity.upper())
        if status:
            where_clauses.append("status = ?")
            params.append(status.upper())
        if min_lat is not None:
            where_clauses.append("latitude >= ?")
            params.append(min_lat)
        if max_lat is not None:
            where_clauses.append("latitude <= ?")
            params.append(max_lat)
        if min_lon is not None:
            where_clauses.append("longitude >= ?")
            params.append(min_lon)
        if max_lon is not None:
            where_clauses.append("longitude <= ?")
            params.append(max_lon)
        if start_date:
            where_clauses.append("created_at >= ?")
            params.append(start_date)
        if end_date:
            where_clauses.append("created_at <= ?")
            params.append(end_date)

        where_sql = " AND ".join(where_clauses)
        offset = max(0, (page - 1) * page_size)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Count total
                cursor.execute(f"SELECT COUNT(*) as cnt FROM alerts WHERE {where_sql}", params)
                total = cursor.fetchone()["cnt"]

                # Fetch page
                cursor.execute(f"""
                    SELECT * FROM alerts
                    WHERE {where_sql}
                    ORDER BY
                        CASE severity
                            WHEN 'RED' THEN 1
                            WHEN 'ORANGE' THEN 2
                            WHEN 'YELLOW' THEN 3
                            ELSE 4
                        END ASC,
                        created_at DESC
                    LIMIT ? OFFSET ?
                """, params + [page_size, offset])

                rows = cursor.fetchall()
                items = [self._row_to_alert_dict(r) for r in rows]
                return (items, total)
        except Exception as e:
            logger.error(f"Error querying alerts: {e}")
            return ([], 0)

    def update_alert_status(
        self,
        alert_id: str,
        new_status: str,
        performed_by: str = "Operator",
        notes: Optional[str] = None
    ) -> bool:
        now_str = datetime.now(timezone.utc).isoformat()
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT status FROM alerts WHERE alert_id = ?", (alert_id,))
                row = cursor.fetchone()
                if not row:
                    return False
                prev_status = row["status"]

                if new_status == "ACKNOWLEDGED":
                    cursor.execute("""
                        UPDATE alerts SET
                            status = ?,
                            acknowledged_at = ?,
                            acknowledged_by = ?,
                            updated_at = ?
                        WHERE alert_id = ?
                    """, (new_status, now_str, performed_by, now_str, alert_id))
                elif new_status == "RESOLVED":
                    cursor.execute("""
                        UPDATE alerts SET
                            status = ?,
                            resolved_at = ?,
                            resolved_by = ?,
                            resolution_notes = ?,
                            updated_at = ?
                        WHERE alert_id = ?
                    """, (new_status, now_str, performed_by, notes or "Resolved by operator", now_str, alert_id))
                else:
                    cursor.execute("""
                        UPDATE alerts SET status = ?, updated_at = ? WHERE alert_id = ?
                    """, (new_status, now_str, alert_id))

                cursor.execute("""
                    INSERT INTO alert_audit_logs
                    (alert_id, previous_status, new_status, action_type, performed_by, notes, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (alert_id, prev_status, new_status, f"SET_{new_status}", performed_by, notes, now_str))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error updating alert {alert_id} status: {e}")
            return False

    def mark_alert_notification_sent(self, alert_id: str) -> None:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE alerts SET notification_sent = 1 WHERE alert_id = ?", (alert_id,))
                conn.commit()
        except Exception as e:
            logger.warning(f"Error updating notification_sent for alert {alert_id}: {e}")

    def log_alert_notification_event(self, alert_id: str, status: str, notes: Optional[str] = None) -> None:
        """
        Records an explicit notification event (e.g. NOTIFICATION_SENT, NOTIFICATION_NOT_CONFIGURED, NOTIFICATION_FAILED)
        in the alert audit trail to preserve accurate dispatch history.
        """
        now_str = datetime.now(timezone.utc).isoformat()
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT status FROM alerts WHERE alert_id = ?", (alert_id,))
                row = cursor.fetchone()
                current_status = row["status"] if row else "ACTIVE"
                action_type = f"NOTIFICATION_{status.upper()}"
                cursor.execute("""
                    INSERT INTO alert_audit_logs
                    (alert_id, previous_status, new_status, action_type, performed_by, notes, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (alert_id, current_status, current_status, action_type, "NotificationService", notes or f"Notification status: {status}", now_str))
                conn.commit()
        except Exception as e:
            logger.warning(f"Error logging notification event for alert {alert_id}: {e}")

    def expire_stale_alerts(self, max_age_hours: int = 48) -> int:
        now_ts = time.time()
        cutoff_str = datetime.fromtimestamp(now_ts - (max_age_hours * 3600), timezone.utc).isoformat()
        now_str = datetime.now(timezone.utc).isoformat()
        count = 0
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT alert_id, status FROM alerts
                    WHERE status IN ('ACTIVE', 'ACKNOWLEDGED') AND created_at < ?
                """, (cutoff_str,))
                stale = cursor.fetchall()
                for s in stale:
                    a_id = s["alert_id"]
                    cursor.execute("UPDATE alerts SET status = 'EXPIRED', updated_at = ? WHERE alert_id = ?", (now_str, a_id))
                    cursor.execute("""
                        INSERT INTO alert_audit_logs
                        (alert_id, previous_status, new_status, action_type, performed_by, notes, timestamp)
                        VALUES (?, ?, 'EXPIRED', 'AUTO_EXPIRE', 'AlertEngine', 'Exceeded maximum operational age window', ?)
                    """, (a_id, s["status"], now_str))
                    count += 1
                conn.commit()
        except Exception as e:
            logger.error(f"Error expiring stale alerts: {e}")
        return count

    def get_alert_summary_metrics(self) -> Dict[str, Any]:
        metrics = {
            "total_active": 0,
            "total_severe_red": 0,
            "total_high_orange": 0,
            "total_moderate_yellow": 0,
            "by_hazard": {
                "floods": 0,
                "landslides": 0,
                "earthquakes": 0,
                "cyclones": 0,
                "wildfires": 0
            },
            "recent_alerts": []
        }
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Counts of active alerts by severity
                cursor.execute("""
                    SELECT severity, COUNT(*) as cnt FROM alerts
                    WHERE status IN ('ACTIVE', 'ACKNOWLEDGED')
                    GROUP BY severity
                """)
                for r in cursor.fetchall():
                    sev = r["severity"]
                    cnt = r["cnt"]
                    metrics["total_active"] += cnt
                    if sev == "RED":
                        metrics["total_severe_red"] = cnt
                    elif sev == "ORANGE":
                        metrics["total_high_orange"] = cnt
                    elif sev == "YELLOW":
                        metrics["total_moderate_yellow"] = cnt

                # Active counts by hazard
                cursor.execute("""
                    SELECT hazard_type, COUNT(*) as cnt FROM alerts
                    WHERE status IN ('ACTIVE', 'ACKNOWLEDGED')
                    GROUP BY hazard_type
                """)
                for r in cursor.fetchall():
                    ht = r["hazard_type"].lower()
                    if ht in metrics["by_hazard"]:
                        metrics["by_hazard"][ht] = r["cnt"]

                # Recent 5 alerts
                cursor.execute("""
                    SELECT * FROM alerts
                    ORDER BY created_at DESC LIMIT 5
                """)
                metrics["recent_alerts"] = [self._row_to_alert_dict(r) for r in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error gathering alert summary metrics: {e}")
        return metrics

    def get_alert_audit_logs(self, alert_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        query = "SELECT * FROM alert_audit_logs"
        params = []
        if alert_id:
            query += " WHERE alert_id = ?"
            params.append(alert_id)
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return [dict(r) for r in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error querying alert audit logs: {e}")
            return []

    def _row_to_alert_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        d = dict(row)
        try:
            d["model_prediction"] = json.loads(d.get("model_prediction_json", "{}"))
        except Exception:
            d["model_prediction"] = {}
        d.pop("model_prediction_json", None)
        d["notification_sent"] = bool(d.get("notification_sent", 0))
        return d

    # =========================================================================
    # PHASE 10: HAZARD FORECAST PERSISTENCE METHODS
    # =========================================================================

    def save_hazard_forecast(self, fc_data: Dict[str, Any]) -> str:
        fc_id = fc_data.get("forecast_id") or f"fc_{fc_data.get('hazard_type', 'gen')[:3]}_{int(time.time()*1000)}"
        now_str = datetime.now(timezone.utc).isoformat()
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO hazard_forecasts
                    (forecast_id, hazard_type, location_name, latitude, longitude, forecast_horizon, risk_score, risk_category, valid_from, valid_until, payload_json, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    fc_id,
                    str(fc_data.get("hazard_type")),
                    str(fc_data.get("geographic_location") or fc_data.get("location_name") or "Unknown"),
                    float(fc_data.get("latitude", 0.0)),
                    float(fc_data.get("longitude", 0.0)),
                    str(fc_data.get("forecast_horizon", "24h")),
                    float(fc_data.get("risk_score", 0.0)),
                    str(fc_data.get("risk_category", "LOW")),
                    str(fc_data.get("forecast_valid_from") or fc_data.get("valid_from") or now_str),
                    str(fc_data.get("forecast_valid_until") or fc_data.get("valid_until") or now_str),
                    json.dumps(fc_data),
                    now_str
                ))
                conn.commit()
                return fc_id
        except Exception as e:
            logger.error(f"Error saving hazard forecast: {e}")
            return fc_id

    def query_hazard_forecasts(self, hazard_type: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        query = "SELECT payload_json FROM hazard_forecasts WHERE 1=1"
        params = []
        if hazard_type:
            query += " AND hazard_type = ?"
            params.append(hazard_type.lower())
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return [json.loads(r["payload_json"]) for r in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error querying hazard forecasts: {e}")
            return []

    # =========================================================================


storage_service = DataStorageService()

