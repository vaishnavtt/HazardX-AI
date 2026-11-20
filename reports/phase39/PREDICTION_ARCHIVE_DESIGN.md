# HAZARDX AI — PREDICTION ARCHIVE SYSTEM DESIGN
**Document ID:** `HX-RPT-PH39-01`  
**Phase:** Phase 39 — Prospective Validation, Archival & Live Monitoring  
**Author:** Backend Architect & MLOps Infrastructure Engineer  
**Date:** November 20, 2026  
**Status:** APPROVED & DEPLOYED  

---

## 1. Executive Summary

To support prospective scientific validation and prevent retrofitting of machine learning models to known disaster events, HAZARDX AI incorporates an immutable prediction archive architecture. Every risk assessment executed via API or the web dashboard automatically creates an auditable prediction snapshot.

This document outlines the architecture, database schema, indexing strategies, and querying mechanisms of the prospective prediction archive.

---

## 2. Archive Database Schema & Storage

The prediction archive is managed by `PredictionArchiveService` (`backend/app/services/prediction_archive_service.py`) and stored in the high-concurrency WAL-mode SQLite database `data/hazardx_live.db`.

```sql
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
);

CREATE INDEX IF NOT EXISTS idx_pred_hazard ON prediction_archive(hazard_type);
CREATE INDEX IF NOT EXISTS idx_pred_status ON prediction_archive(verification_status);
CREATE INDEX IF NOT EXISTS idx_pred_time ON prediction_archive(timestamp);
CREATE INDEX IF NOT EXISTS idx_pred_coords ON prediction_archive(lat, lon);
```

---

## 3. Asynchronous Non-Blocking Recording

Prediction snapshots are recorded at the completion of `/api/v1/geospatial/assess` requests:
- Recording runs in safe exception-handled blocks, ensuring that even under database lock contention, user API responses are never delayed or degraded.
- Features are serialized to compact JSON snapshots preserving complete provenance of raw weather, DEM, fault, and discharge inputs.
- Each prediction is tagged with a UUIDv4 and ISO 8601 UTC timestamp.

---

## 4. Verification Lifecycle & State Machine

```
   [Inference Generated]
            │
            ▼
    ┌───────────────┐
    │    PENDING    │  (Awaiting 24h verification window)
    └───────┬───────┘
            │
            ├───────────────────────┬────────────────────────┐
            ▼                       ▼                        ▼
    [Predicted Positive]    [Predicted Positive]    [Predicted Negative]
    [Event Observed]        [No Event Observed]     [No Event Observed]
            │                       │                        │
            ▼                       ▼                        ▼
     VERIFIED_HIT              FALSE_ALARM           CORRECT_REJECTION
```

---

## 5. Security & Immutability

1. **Tamper-Evident Logs:** Once written, `raw_score`, `calibrated_prob`, and `features_json` cannot be modified. Only `verification_status`, `outcome_observed`, and `verified_at` can be updated by the verification service.
2. **Data Retention:** Active rolling window retains high-frequency snapshots for 180 days before automated partitioning to cold parquet archives.
