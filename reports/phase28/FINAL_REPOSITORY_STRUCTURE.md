# HAZARDX AI – Phase 28: Final Repository Structure Report

**Date:** November 19, 2026  
**Project:** HAZARDX AI – Global Multi-Hazard Intelligence and Early Warning System  
**Repository:** [https://github.com/vaishnavtt/HazardX-AI](https://github.com/vaishnavtt/HazardX-AI)  
**Branch:** `main` | **Tag:** `v1.0.0`  

---

## 1. Top-Level Repository Architecture

```text
hazardai/
├── .github/
│   └── workflows/
│       ├── backend-tests.yml              # CI automated pytest workflow
│       ├── frontend-build.yml             # CI Vite TypeScript build verification
│       └── security-checks.yml            # CI vulnerability and security audit
├── backend/
│   ├── app/
│   │   ├── alerts/                        # Alert deduplication, rules, and notifications
│   │   ├── api/v1/endpoints/              # 10 modular REST API endpoints
│   │   ├── forecasting/                   # Multi-horizon forecasting & Omori models
│   │   ├── geospatial/                    # Coordinate clipping, terrain & geocoding
│   │   ├── ingestion/                     # Live telemetry schedulers & validators
│   │   ├── integrations/                  # USGS, GloFAS, FIRMS, Open-Meteo, IMD clients
│   │   ├── schemas/                       # Pydantic data transfer objects
│   │   ├── services/                      # Domain prediction & explanation services
│   │   ├── utils/                         # Logging, telemetry, and common math
│   │   ├── config.py                      # Operational governance & quarantine flags
│   │   └── main.py                        # FastAPI application root & middleware
│   ├── tests/                             # Unit tests for prediction services
│   ├── Dockerfile                         # Backend container definition
│   └── requirements.txt                   # Backend Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/                    # UI elements, GlassPanel, Navigation, Modals
│   │   ├── pages/                         # Dashboard, Map, Forecasts, CheckLocation, Alerts, PastEvents, About
│   │   ├── services/                      # Axios API clients
│   │   ├── types/                         # TypeScript interface definitions
│   │   ├── utils/                         # Formatting and geospatial helpers
│   │   ├── App.tsx                        # Router layout and synchronous component tree
│   │   └── main.tsx                       # React DOM entrypoint
│   ├── public/                            # Static icons and assets
│   ├── package.json                       # Node dependencies
│   ├── vite.config.ts                     # Vite build and reverse proxy configuration
│   └── tsconfig.json                      # Strict TypeScript compiler options
├── data/
│   ├── model_ready/                       # Holdout test sets (cyclones, earthquakes, floods, landslides, wildfires)
│   ├── reports/                           # Historical exploratory and validation reports
│   └── hazardx_live.db                    # Pre-populated SQLite database for local demonstration
├── models/
│   ├── cyclones/                          # RI classification & 24h intensity models
│   ├── earthquakes/                       # Aftershock hazard & max magnitude models
│   ├── floods/                            # Inundation occurrence & stage severity models
│   ├── landslides/                        # Slope failure occurrence & magnitude models
│   ├── wildfires/                         # Ignition occurrence & FRP intensity models
│   ├── model_comparison_dashboard.json    # Holdout benchmark statistics
│   └── model_comparison_dashboard.csv     # Tabular model performance metrics
├── docs/
│   ├── images/                            # High-resolution application screenshots (01 to 08)
│   ├── ARCHITECTURE.md                    # System architecture & component flows
│   ├── AI_ML_METHODOLOGY.md               # Training, calibration, and SHAP explanations
│   ├── DATA_SOURCES.md                    # Provenance of USGS, GloFAS, FIRMS, ERA5, IMD
│   ├── API_DOCUMENTATION.md               # Complete REST API reference and payloads
│   ├── INSTALLATION.md                    # Bare-metal and container installation instructions
│   ├── SCIENTIFIC_LIMITATIONS.md          # Scientific uncertainties and non-prediction policies
│   ├── MODEL_GOVERNANCE.md                # Quarantine criteria and deployment standards
│   ├── FORECASTING_METHODOLOGY.md         # Multi-horizon decay and Omori-Utsu mechanics
│   ├── DEPLOYMENT.md                      # Production deployment and systemd configuration
│   └── FAQ.md                             # Frequently asked technical and domain questions
├── reports/
│   ├── phase22/                           # Independent Release Verification Reports (5 files)
│   ├── phase23/                           # Application Stability & Error Hardening Reports (5 files)
│   ├── phase24/                           # Performance & Resource Optimization Reports (4 files)
│   ├── phase25/                           # Deployment & Installation Readiness Reports (4 files)
│   ├── phase26/                           # Professional GitHub Documentation Reports (4 files)
│   ├── phase27/                           # Automated CI & Quality Gate Reports (6 files)
│   └── phase28/                           # GitHub Publication & Release Reports (4 files)
├── scripts/
│   ├── audit/                             # Dataset and environmental verification scripts
│   ├── data_collection/                   # Automated data harvesting tools
│   ├── eda/                               # Quality, duplicate, and spatial analysis scripts
│   ├── ml_pipeline/                       # Training, evaluation, and calibration pipeline
│   ├── ml_prep/                           # Dataset curation and feature engineering scripts
│   └── e2e_browser_test.cjs               # Headless Puppeteer browser testing suite
├── tests/
│   ├── test_model_pipeline.py             # Pytest suite validating end-to-end inference
│   └── conftest.py                        # Test configuration and fixtures
├── .dockerignore                          # Docker build exclusion definitions
├── .env.example                           # Sanitized environment template
├── .gitignore                             # Git ignore rules for virtualenvs, caches, secrets
├── CHANGELOG.md                           # Chronological development and release changelog
├── CITATION.cff                           # Academic citation metadata
├── CODE_OF_CONDUCT.md                     # Contributor Covenant Code of Conduct
├── CONTRIBUTING.md                        # Community guidelines for contributions
├── Dockerfile                             # Multi-stage production container
├── docker-compose.yml                     # Unified multi-service orchestration
├── LICENSE                                # MIT License
├── README.md                              # Comprehensive project presentation
├── SECURITY.md                            # Security vulnerability disclosure guidelines
├── START_HAZARDX.bat                      # Windows CMD dual-process launcher
├── STOP_HAZARDX.bat                       # Windows CMD cleanup script
├── start_hazardx.ps1                      # Windows PowerShell automated launcher
├── start_hazardx.sh                       # Linux / macOS Bash automated launcher
└── requirements.txt                       # Unified root Python dependency manifest
```

---

## 2. Directory Metrics & Verification

| Directory | File Count | Purpose | Tracking Status |
| :--- | :--- | :--- | :--- |
| `.github/` | 3 | Automated Continuous Integration | Tracked |
| `backend/` | 52 | FastAPI backend services & routes | Tracked |
| `frontend/` | 39 | React 19 UI & Leaflet mapping | Tracked |
| `data/` | 32 | Holdout datasets & demonstration SQLite DB | Tracked (`raw/` & `processed/` ignored) |
| `models/` | 38 | 12 ML models, encoders, and registries | Tracked |
| `docs/` | 19 | Markdown technical guides & screenshots | Tracked |
| `reports/` | 58 | Complete engineering audit audit trails | Tracked |
| `scripts/` | 44 | Data pipeline, training, and testing tools | Tracked |
| `tests/` | 3 | Pytest test execution modules | Tracked |
| Root | 18 | Launchers, Dockerfiles, licenses, README | Tracked |
| **Total** | **556** | **Full Production HAZARDX AI System** | **Tracked on GitHub `main`** |

---

## 3. Storage Governance Summary

- **Total Tracked Code & Asset Footprint:** ~72.4 MB (well within standard repository size guidelines).
- **Excluded Untracked Assets:**
  - `data/raw/` (~695 MB of external raw datasets).
  - `data/processed/` (~154 MB of regenerated catalogs).
  - `node_modules/` (~480 MB of frontend packages).
  - `.venv/` (~950 MB of Python dependencies).
  - `frontend/dist/` (compiled build outputs).
  - `*.db-wal` & `*.db-shm` (ephemeral database lock journals).

**Final Structure Audit Status: VERIFIED & COMPLIANT**
