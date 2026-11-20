"""
HAZARDX AI — Prospective Prediction Archive & Outcome Verification Service
Maintains immutable audit records of all ML inferences, monitors prospective real-world
outcomes, and tracks empirical calibration drift (Brier score, hit rate, false alarm rate).
"""

import os
import json
import sqlite3
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional, Tuple

from ..config import settings
from ..utils.logging_config import get_logger

logger = get_logger("prediction_archive")
DB_PATH = os.path.join(settings.ROOT_DIR, "data", "hazardx_live.db")

class PredictionArchiveService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PredictionArchiveService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.db_path = DB_PATH
        self._init_table()
        self._initialized = True

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_table(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prediction_archive (
                    prediction_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    hazard_type TEXT NOT NULL,
                    lat REAL NOT NULL,
                    lon REAL NOT NULL,
                    location_name TEXT,
                    model_name TEXT NOT NULL,
                    model_version TEXT NOT NULL,
                    features_json TEXT NOT NULL,
                    raw_score REAL NOT NULL,
                    calibrated_prob REAL NOT NULL,
                    risk_category TEXT NOT NULL,
                    alert_level TEXT NOT NULL,
                    verification_window_hours REAL NOT NULL DEFAULT 24.0,
                    verification_status TEXT NOT NULL DEFAULT 'PENDING',
                    outcome_observed INTEGER,
                    outcome_details_json TEXT,
                    verified_at TEXT
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pred_hazard ON prediction_archive(hazard_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pred_status ON prediction_archive(verification_status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pred_time ON prediction_archive(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pred_coords ON prediction_archive(lat, lon)")
            conn.commit()

    def record_prediction(
        self,
        hazard_type: str,
        lat: float,
        lon: float,
        model_name: str,
        model_version: str,
        features: Dict[str, Any],
        raw_score: float,
        calibrated_prob: float,
        risk_category: str,
        alert_level: str,
        location_name: Optional[str] = None,
        verification_window_hours: float = 24.0
    ) -> str:
        """
        Records an immutable inference snapshot for prospective validation.
        """
        pred_id = str(uuid.uuid4())
        now_str = datetime.now(timezone.utc).isoformat()

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO prediction_archive (
                        prediction_id, timestamp, hazard_type, lat, lon, location_name,
                        model_name, model_version, features_json, raw_score, calibrated_prob,
                        risk_category, alert_level, verification_window_hours, verification_status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pred_id, now_str, hazard_type, round(lat, 5), round(lon, 5),
                    location_name or f"({lat:.4f}, {lon:.4f})",
                    model_name, model_version, json.dumps(features),
                    round(raw_score, 4), round(calibrated_prob, 6),
                    risk_category, alert_level, verification_window_hours, "PENDING"
                ))
                conn.commit()
            return pred_id
        except Exception as e:
            logger.error(f"Failed to record prediction snapshot: {e}")
            return pred_id

    def get_recent_predictions(
        self,
        limit: int = 50,
        hazard: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetches archived predictions with optional filtering.
        """
        query = "SELECT * FROM prediction_archive WHERE 1=1"
        params = []
        if hazard:
            query += " AND hazard_type = ?"
            params.append(hazard)
        if status:
            query += " AND verification_status = ?"
            params.append(status)
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()
                results = []
                for r in rows:
                    item = dict(r)
                    if item.get("features_json"):
                        try:
                            item["features"] = json.loads(item["features_json"])
                        except Exception:
                            item["features"] = {}
                    if item.get("outcome_details_json"):
                        try:
                            item["outcome_details"] = json.loads(item["outcome_details_json"])
                        except Exception:
                            item["outcome_details"] = {}
                    results.append(item)
                return results
        except Exception as e:
            logger.error(f"Error fetching archived predictions: {e}")
            return []

    def verify_prediction_outcome(
        self,
        prediction_id: str,
        outcome_observed: bool,
        outcome_details: Dict[str, Any]
    ) -> bool:
        """
        Updates a prediction's verification status based on subsequent real-world observations.
        """
        now_str = datetime.now(timezone.utc).isoformat()
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT raw_score, calibrated_prob, alert_level FROM prediction_archive WHERE prediction_id = ?",
                    (prediction_id,)
                )
                row = cursor.fetchone()
                if not row:
                    return False

                raw_score = row["raw_score"]
                alert_level = row["alert_level"]
                predicted_positive = (raw_score >= 0.50) or (alert_level in ["ORANGE", "RED"])

                if predicted_positive and outcome_observed:
                    v_status = "VERIFIED_HIT"
                elif predicted_positive and not outcome_observed:
                    v_status = "FALSE_ALARM"
                elif not predicted_positive and outcome_observed:
                    v_status = "MISSED_EVENT"
                else:
                    v_status = "VERIFIED_CORRECT_REJECTION"

                cursor.execute("""
                    UPDATE prediction_archive
                    SET verification_status = ?, outcome_observed = ?, outcome_details_json = ?, verified_at = ?
                    WHERE prediction_id = ?
                """, (
                    v_status, 1 if outcome_observed else 0, json.dumps(outcome_details), now_str, prediction_id
                ))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error verifying prediction {prediction_id}: {e}")
            return False

    def compute_reliability_metrics(self, hazard_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Computes empirical verification statistics: Brier Score, Hit Rate (Sensitivity),
        False Alarm Rate, and Sample Counts from verified predictions.
        """
        query = "SELECT raw_score, calibrated_prob, outcome_observed, verification_status FROM prediction_archive WHERE verification_status != 'PENDING'"
        params = []
        if hazard_type:
            query += " AND hazard_type = ?"
            params.append(hazard_type)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()

                if not rows:
                    return {
                        "hazard_type": hazard_type or "all",
                        "total_archived": 0,
                        "total_verified": 0,
                        "brier_score": None,
                        "hit_rate": None,
                        "false_alarm_rate": None,
                        "status": "INSUFFICIENT_VERIFIED_OUTCOMES"
                    }

                n = len(rows)
                brier_sum = 0.0
                hits = 0
                false_alarms = 0
                misses = 0
                correct_rejections = 0

                for r in rows:
                    prob = float(r["calibrated_prob"])
                    obs = int(r["outcome_observed"] or 0)
                    brier_sum += (prob - obs) ** 2

                    st = r["verification_status"]
                    if st == "VERIFIED_HIT":
                        hits += 1
                    elif st == "FALSE_ALARM":
                        false_alarms += 1
                    elif st == "MISSED_EVENT":
                        misses += 1
                    elif st == "VERIFIED_CORRECT_REJECTION":
                        correct_rejections += 1

                actual_positives = hits + misses
                actual_negatives = correct_rejections + false_alarms
                predicted_positives = hits + false_alarms

                hit_rate = (hits / actual_positives) if actual_positives > 0 else 1.0
                far = (false_alarms / actual_negatives) if actual_negatives > 0 else 0.0
                precision = (hits / predicted_positives) if predicted_positives > 0 else 1.0

                return {
                    "hazard_type": hazard_type or "all",
                    "total_verified": n,
                    "brier_score": round(brier_sum / n, 6),
                    "hit_rate": round(hit_rate, 4),
                    "false_alarm_rate": round(far, 4),
                    "precision": round(precision, 4),
                    "contingency_table": {
                        "hits": hits,
                        "false_alarms": false_alarms,
                        "misses": misses,
                        "correct_rejections": correct_rejections
                    },
                    "status": "OPERATIONAL_MONITORING"
                }
        except Exception as e:
            logger.error(f"Error computing reliability metrics: {e}")
            return {"status": "ERROR", "error": str(e)}

prediction_archive_service = PredictionArchiveService()
