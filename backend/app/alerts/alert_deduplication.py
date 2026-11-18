"""
HAZARDX AI — Spatial-Temporal Alert Deduplication Engine
Prevents alert storming and duplicates by clustering physical observations
within geographical thresholds and temporal aggregation windows.
"""

import time
import math
from typing import Tuple, Optional
from ..schemas.alert import AlertSeverity

SEVERITY_RANKS = {
    "GREEN": 1,
    "YELLOW": 2,
    "ORANGE": 3,
    "RED": 4
}

class AlertDeduplicator:
    def __init__(self, window_hours: int = 12):
        self.window_hours = window_hours

    def generate_dedup_key(self, hazard: str, lat: float, lon: float, custom_window_hours: int = 12, horizon: Optional[str] = None) -> str:
        """
        Generates a deterministic spatio-temporal cluster key.
        Floods/landslides/wildfires clustered to 0.25 degree cells (~25km).
        Earthquakes/cyclones clustered to 0.50 degree cells (~50km).
        """
        h_lower = hazard.lower()
        if h_lower in ["earthquakes", "cyclones"]:
            grid_step = 0.50
        else:
            grid_step = 0.25

        grid_lat = round(lat / grid_step) * grid_step
        grid_lon = round(lon / grid_step) * grid_step

        now_sec = time.time()
        window_sec = (custom_window_hours or self.window_hours) * 3600
        time_bucket = int(now_sec // window_sec)

        base_key = f"{h_lower}_{grid_lat:.2f}_{grid_lon:.2f}_t{time_bucket}"
        if horizon:
            return f"{base_key}_{horizon.lower()}"
        return base_key

    def should_escalate(self, old_severity: AlertSeverity, new_severity: AlertSeverity) -> bool:
        """
        Returns True if the new severity represents a higher risk level than the existing alert.
        """
        old_rank = SEVERITY_RANKS.get(old_severity, 1)
        new_rank = SEVERITY_RANKS.get(new_severity, 1)
        return new_rank > old_rank

alert_deduplicator = AlertDeduplicator()

