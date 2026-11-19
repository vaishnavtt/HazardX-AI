# Phase 34 — Model Versioning, Registry Structure and Promotion Criteria

## 1. Executive Summary

This report establishes the semantic versioning protocol, serialised artifact storage standards, and release promotion criteria for HAZARDX AI models.

---

## 2. Model Versioning Protocol

All models follow Semantic Versioning (`MAJOR.MINOR.PATCH`):
- **MAJOR (e.g. 2.0.0):** Breaking change in feature contract (new input dimensions, modified spatial resolution, or changed label definitions).
- **MINOR (e.g. 1.1.0):** Retrained weights with additional geographic training samples or updated calibration parameters without altering feature schemas.
- **PATCH (e.g. 1.0.1):** Bug fixes in pre-condition gating or minor numerical threshold adjustments.

---

## 3. Storage Hierarchy & Metadata Architecture

Serialized model weights and their corresponding metadata are stored under the versioned registry hierarchy:
```
data/models/
├── flood/
│   ├── flood_occurrence_v1.0.0.pkl
│   ├── flood_severity_v1.0.0.pkl
│   └── metadata.json
├── landslide/
│   ├── landslide_occurrence_v1.0.0.pkl
│   ├── landslide_magnitude_v1.0.0.pkl
│   └── metadata.json
├── wildfire/
│   ├── wildfire_occurrence_v1.0.0.pkl
│   ├── wildfire_frp_v1.0.0.pkl
│   └── metadata.json
├── earthquake/
│   ├── omori_decay_params_v1.0.0.json
│   └── metadata.json
└── cyclone/
    ├── cyclone_ri_v1.0.0.pkl
    ├── cyclone_intensity_v1.0.0.pkl
    └── metadata.json
```

### 3.1 Metadata Contract Schema
Every serialized model must have a companion `metadata.json` defining:
```json
{
  "model_identifier": "wildfires_wildfire_occurrence",
  "version": "1.0.0",
  "trained_at": "2026-03-15T10:00:00Z",
  "git_commit": "e3b8a1c",
  "algorithm": "XGBClassifier",
  "features": ["temp_2m_celsius", "relative_humidity_pct", "wind_speed_10m_ms", "..."],
  "test_metrics": {
    "roc_auc": 0.880,
    "brier_score": 0.0246,
    "expected_calibration_error": 0.028
  },
  "governance_status": "OPERATIONAL",
  "calibration_method": "BayesianPriorOddsInversion"
}
```

---

## 4. Rollback and Disaster Recovery Procedures

1. **Automated Canary Deployment:** New model weights are initially evaluated against 10% of shadow traffic.
2. **Instant Rollback:** If live inference error rates exceed $0.5\%$ or drift alerts trigger, the registry pointer switches back to the previous stable release artifact within $< 100\text{ ms}$ without requiring service restarts.
