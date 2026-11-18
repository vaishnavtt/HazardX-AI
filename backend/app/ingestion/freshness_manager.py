"""
HAZARDX AI — Centralized Data Freshness Policy & Provenance Engine
Evaluates observation age against authoritative provider update schedules and assigns
strict freshness tiers (FRESH, ACCEPTABLE, STALE, UNAVAILABLE) and provenance categories.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional
from ..utils.logging_config import get_logger

logger = get_logger("freshness_manager")

# Freshness window thresholds in seconds (Fresh limit, Stale threshold)
FRESHNESS_THRESHOLDS: Dict[str, Tuple[int, int]] = {
    "usgs_earthquakes": (900, 1800),          # Fresh <= 15 min, Stale > 30 min
    "nasa_firms": (10800, 21600),             # Fresh <= 3 hours, Stale > 6 hours
    "open_meteo_weather": (7200, 14400),      # Fresh <= 2 hours, Stale > 4 hours
    "glofas_floods": (86400, 172800),         # Fresh <= 24 hours, Stale > 48 hours
    "noaa_nhc_cyclones": (10800, 21600),      # Fresh <= 3 hours, Stale > 6 hours
    "nasa_glc_landslides": (86400, 172800),   # Fresh <= 24 hours, Stale > 48 hours
    "imd_rsmc": (21600, 43200)                # Fresh <= 6 hours, Stale > 12 hours
}

class FreshnessManager:
    def __init__(self):
        pass

    def evaluate_source_freshness(self, source_id: str, last_updated_iso: Optional[str]) -> Dict[str, Any]:
        """
        Calculates age and determines strict freshness tier for a specific external provider.
        """
        if not last_updated_iso:
            return {
                "source_id": source_id,
                "status": "UNAVAILABLE",
                "age_seconds": None,
                "age_human": "Never updated",
                "is_stale": True
            }

        try:
            cleaned = last_updated_iso.replace("Z", "+00:00")
            dt = datetime.fromisoformat(cleaned)
            now = datetime.now(timezone.utc)
            age_sec = max(0.0, (now - dt).total_seconds())

            fresh_lim, stale_lim = FRESHNESS_THRESHOLDS.get(source_id, (3600, 7200))

            if age_sec <= fresh_lim:
                status = "FRESH"
                is_stale = False
            elif age_sec <= stale_lim:
                status = "ACCEPTABLE"
                is_stale = False
            else:
                status = "STALE"
                is_stale = True

            # Human-readable format
            if age_sec < 60:
                age_human = f"{int(age_sec)} seconds ago"
            elif age_sec < 3600:
                age_human = f"{int(age_sec // 60)} minutes ago"
            elif age_sec < 86400:
                age_human = f"{age_sec / 3600:.1f} hours ago"
            else:
                age_human = f"{age_sec / 86400:.1f} days ago"

            return {
                "source_id": source_id,
                "status": status,
                "age_seconds": round(age_sec, 1),
                "age_human": age_human,
                "is_stale": is_stale,
                "fresh_threshold_sec": fresh_lim,
                "stale_threshold_sec": stale_lim
            }
        except Exception as e:
            logger.warning(f"Error parsing timestamp {last_updated_iso} for {source_id}: {e}")
            return {
                "source_id": source_id,
                "status": "UNKNOWN",
                "age_seconds": None,
                "age_human": "Invalid timestamp",
                "is_stale": True
            }

freshness_manager = FreshnessManager()

