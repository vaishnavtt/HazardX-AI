"""
HAZARDX AI — Backend Configuration & Settings
Defines environment variables, path mappings, model operational statuses, and system limits.
"""

import os
from typing import List, Dict, Any
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "HAZARDX AI — Multi-Hazard Intelligence & Early Warning API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = (
        "Production-grade FastAPI decision-support backend integrating five natural hazard modules: "
        "Floods, Landslides, Earthquakes (Aftershock Hazard), Cyclones, and Wildfires."
    )
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = ["*"]

    # Base Paths
    APP_DIR: str = os.path.dirname(os.path.abspath(__file__))
    BACKEND_DIR: str = os.path.dirname(APP_DIR)
    ROOT_DIR: str = os.path.dirname(BACKEND_DIR)
    MODELS_DIR: str = os.path.join(ROOT_DIR, "models")
    DATA_DIR: str = os.path.join(ROOT_DIR, "data", "model_ready")
    REPORTS_DIR: str = os.path.join(ROOT_DIR, "reports")
    
    # External API Keys (Optional, fallback to open public endpoints)
    NASA_FIRMS_MAP_KEY: str = ""

    # Alert Management & Background Monitoring
    ALERT_MONITOR_ENABLED: bool = True
    ALERT_MONITOR_INTERVAL_SECONDS: int = 180
    ALERT_MAX_AGE_HOURS: int = 48
    ALERT_DEDUP_WINDOW_HOURS: int = 12

    # Ingestion Scheduler Settings (Phase 10)
    INGESTION_SCHEDULER_ENABLED: bool = False
    INGESTION_INTERVAL_SECONDS: int = 300
    TESTING: bool = False

    # Notification & SMTP Settings (Optional, graceful fallback)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_TLS: bool = True
    ALERT_EMAIL_FROM: str = "alerts@hazardx.ai"
    ALERT_EMAIL_RECIPIENTS: str = ""
    ALERT_EMAIL_MIN_SEVERITY: str = "ORANGE"

    # Model Operational Status Registry
    MODEL_STATUS: Dict[str, str] = {
        "floods_flood_occurrence": "OPERATIONAL",
        "floods_flood_severity": "OPERATIONAL",
        "landslides_landslide_occurrence": "OPERATIONAL",
        "landslides_landslide_magnitude": "OPERATIONAL",
        "earthquakes_aftershock_hazard": "OPERATIONAL",
        "earthquakes_max_aftershock_mag": "EXPERIMENTAL",
        "earthquakes_aftershock_count": "UNAVAILABLE_FOR_OPERATIONAL_USE",
        "cyclones_rapid_intensification": "OPERATIONAL",
        "cyclones_intensity_change_24h": "OPERATIONAL",
        "wildfires_wildfire_occurrence": "OPERATIONAL",
        "wildfires_frp_intensity": "EXPERIMENTAL",
        "wildfires_fire_duration": "UNAVAILABLE_FOR_OPERATIONAL_USE"
    }

    # Case-Control Base Rate Priors for Calibration (per-event climatological frequency)
    CLIMATOLOGICAL_PRIORS: Dict[str, float] = {
        "floods": 0.005,      # 0.5% base daily probability for extreme flood events
        "landslides": 0.002,  # 0.2% base daily probability for steep slope failure
        "wildfires": 0.002    # 0.2% base daily probability for wildfire ignition
    }

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
