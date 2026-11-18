# Changelog

All notable changes to the **HAZARDX AI** platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-11-19 (Production Release Candidate 1)

### Added
- **12 Trained XGBoost Ensembles:** Deployed operational models for Floods, Landslides, Earthquakes, Cyclones, and Wildfires.
- **TreeSHAP Explainability Engine:** Real-time cooperative game-theoretic feature attribution calculated in $< 3$ ms per inference.
- **Probability Calibration:** Isotonic and Sigmoid post-processing reducing Brier scores by up to 50%.
- **Multi-Horizon Forecasting:** Projections across 6h, 12h, 24h, 48h, and 72h lead times with 90% uncertainty intervals.
- **7 Live Scientific Stream Connectors:** Resilient asynchronous clients for USGS, NASA FIRMS, Open-Meteo, GloFAS, NOAA NHC, IMD RSMC, and NASA GLC.
- **4-Tier Data Freshness Engine:** Automatic classification (`FRESH`, `RECENT`, `DELAYED`, `STALE`) based on genuine telemetry timestamps.
- **Apple Light Theme UI:** Translucent Liquid Glass aesthetic with frosted borders, specular sheens, and WCAG 2.1 AA accessibility.
- **Operational Launchers:** `START_HAZARDX.bat`, `STOP_HAZARDX.bat`, `start_hazardx.ps1`, `start_hazardx.sh`.
- **Multi-Stage Docker Support:** `Dockerfile` and `docker-compose.yml` for containerized deployments.

### Changed
- **Holdout Test Set Reconciliation:** Standardized evaluation on the genuine empirical holdout test partition ($N = 23,561$).
- **Contamination Reclassification:** Reclassified 2015 Gorkha Earthquake and 2013 Typhoon Haiyan as In-Sample Historical Case Studies; remaining 8 landmark disasters verified clean out-of-sample.
- **SQLite Concurrency:** Switched SQLite database to Write-Ahead Logging (`WAL`) mode with `NORMAL` synchronous pragma.

### Fixed
- **Wayanad Landslide Disaster Date:** Corrected typographical error in summary tables to reflect true historical date of July 30, 2024.
- **Leaflet Navigation Collision:** Fixed `Map container is already initialized` error when navigating between routes.
- **Vite Object Property Parse Error:** Quoted numeric object keys in `GlassPanel.tsx`.

### Quarantined
- **`earthquakes_aftershock_count`:** Quarantined ($R^2 = -0.0401$) due to unmodeled fault micro-asperities.
- **`wildfires_fire_duration`:** Quarantined ($R^2 = -214.75$) due to unmodeled human firefighting suppression dynamics.
