"""
HAZARDX AI — Central Model Registry Service
Loads, caches, and manages all 12 trained XGBoost models, encoders, and metadata.
Guarantees fast in-memory access and enforces operational governance boundaries.
"""

import os
import json
import joblib
from typing import Dict, Any, Optional
from ..config import settings
from ..utils.logging_config import get_logger

logger = get_logger("model_registry")

class ModelRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelRegistry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.models: Dict[str, Any] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
        self.encoders: Dict[str, Any] = {}
        self.load_all_artifacts()
        self._initialized = True

    def _get_key(self, hazard: str, task: str) -> str:
        return f"{hazard}_{task}"

    def load_all_artifacts(self):
        """Loads all 12 trained models and encoders from disk."""
        logger.info(f"Loading HAZARDX AI models from: {settings.MODELS_DIR}")
        
        hazards = ["floods", "landslides", "earthquakes", "cyclones", "wildfires"]
        loaded_count = 0
        
        for h in hazards:
            h_dir = os.path.join(settings.MODELS_DIR, h)
            if not os.path.exists(h_dir):
                logger.warning(f"Hazard model directory not found: {h_dir}")
                continue
                
            # Scan directory for model files
            for fname in os.listdir(h_dir):
                if fname.endswith("_metadata.json"):
                    meta_path = os.path.join(h_dir, fname)
                    try:
                        with open(meta_path, "r", encoding="utf-8") as f:
                            meta = json.load(f)
                            
                        task_name = meta["task_name"]
                        key = self._get_key(h, task_name)
                        self.metadata[key] = meta
                        
                        # Load corresponding joblib model
                        joblib_name = f"{h}_{task_name}_xgboost.joblib"
                        joblib_path = os.path.join(h_dir, joblib_name)
                        if os.path.exists(joblib_path):
                            model = joblib.load(joblib_path)
                            self.models[key] = model
                            loaded_count += 1
                            logger.info(f"Loaded model [{key}] (Status: {settings.MODEL_STATUS.get(key, 'OPERATIONAL')})")
                        else:
                            logger.error(f"Joblib model artifact missing for metadata: {joblib_path}")
                    except Exception as e:
                        logger.error(f"Failed to load artifact {fname}: {e}")

            # Load encoders if present
            enc_name = f"{h}_categorical_encoder.joblib"
            enc_path = os.path.join(h_dir, enc_name)
            if os.path.exists(enc_path):
                try:
                    self.encoders[h] = joblib.load(enc_path)
                    logger.info(f"Loaded categorical encoder for {h}")
                except Exception as e:
                    logger.error(f"Failed to load encoder for {h}: {e}")

        logger.info(f"Successfully initialized ModelRegistry with {loaded_count} models.")

    def get_model(self, hazard: str, task: str) -> Optional[Any]:
        key = self._get_key(hazard, task)
        return self.models.get(key)

    def get_metadata(self, hazard: str, task: str) -> Optional[Dict[str, Any]]:
        key = self._get_key(hazard, task)
        return self.metadata.get(key)

    def get_encoder(self, hazard: str) -> Optional[Any]:
        return self.encoders.get(hazard)

    def get_operational_status(self, hazard: str, task: str) -> str:
        key = self._get_key(hazard, task)
        return settings.MODEL_STATUS.get(key, "OPERATIONAL")

    def is_operational(self, hazard: str, task: str) -> bool:
        return self.get_operational_status(hazard, task) == "OPERATIONAL"

registry = ModelRegistry()

