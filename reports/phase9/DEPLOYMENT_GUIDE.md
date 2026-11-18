# HAZARDX AI — PRODUCTION DEPLOYMENT & OPERATIONS GUIDE
**Multi-Hazard Platform Infrastructure, Docker Containerization & Runbooks**
*HAZARDX AI Platform — Version 1.0.0*

---

## 1. System Requirements & Prerequisites

### Minimum Hardware Requirements:
- **CPU:** 4 vCPUs (x86_64 or ARM64)
- **RAM:** 8 GB RAM (16 GB recommended for high-volume geospatial raster processing)
- **Disk Storage:** 20 GB available SSD space (for SQLite live database, trained XGBoost model artifacts, and caching)

### Software Prerequisites:
- **Operating System:** Linux (Ubuntu 22.04 LTS / Debian 12 / RHEL 9), macOS (13+), or Windows 11 with WSL2
- **Docker Engine:** `24.0+` with Docker Compose V2 (`2.20+`)
- *For Local Development:*
  - Python `3.11.x`
  - Node.js `20.x LTS` and npm `10.x`

---

## 2. Environment Variables Configuration

Create a `.env` file in the project root based on the following template:

```bash
# =============================================================================
# HAZARDX AI — System Configuration
# =============================================================================

# Application Environment
APP_ENV=production
DEBUG=False
HOST=0.0.0.0
PORT=8000

# SQLite Database Persistence
DB_PATH=/app/data/hazardx_live.db

# External Scientific API Keys (Optional but Recommended for Higher Quota)
NASA_FIRMS_MAP_KEY=your_nasa_firms_map_key_here
OPEN_METEO_API_KEY=your_open_meteo_key_here

# Intelligent Early Warning Background Worker
ALERT_MONITOR_ENABLED=True
ALERT_MONITOR_INTERVAL_SECONDS=180
ALERT_MAX_AGE_HOURS=48
ALERT_DEDUP_WINDOW_HOURS=12

# Notification Service (SMTP)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your_smtp_api_key_or_password
SMTP_TLS=True
ALERT_EMAIL_FROM=alerts@hazardx.ai
ALERT_EMAIL_RECIPIENTS=duty_officer@agency.gov,operations@agency.gov
ALERT_EMAIL_MIN_SEVERITY=ORANGE
```

> [!NOTE]
> If SMTP credentials are empty or unconfigured, the notification service automatically runs in graceful fallback mode: alerts are recorded in SQLite, dispatched via REST/UI, and logged as simulated dispatches without raising errors.

---

## 3. Option 1: Docker Compose Deployment (Recommended)

Docker Compose provides multi-container orchestration connecting the FastAPI backend, Nginx frontend, and persistent data volumes.

### Step 1: Clone Repository & Configure Environment
```bash
cd c:/Users/thott/Desktop/hazardai
cp .env.example .env  # or edit .env directly
```

### Step 2: Build & Start Containers
```bash
docker compose up -d --build
```

### Step 3: Verify Container Health
```bash
docker compose ps
```
Both containers will report `healthy`:
- `hazardx-backend`: Listens on port `8000` (FastAPI REST API).
- `hazardx-frontend`: Listens on port `3000` (Nginx serving React SPA and reverse proxying `/api/` calls).

### Step 4: Access Mission Control UI
Open your web browser and navigate to:
- **Frontend Dashboard:** [http://localhost:3000](http://localhost:3000)
- **Interactive Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check Endpoint:** [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

### Step 5: Stop Containers
```bash
docker compose down
```

---

## 4. Option 2: Local Development Setup

For local development without Docker containers:

### Step 1: Backend Setup
```bash
# Navigate to project root
cd c:/Users/thott/Desktop/hazardai

# Create & activate virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install master dependencies
pip install -r requirements.txt

# Start FastAPI backend with hot reloading
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Step 2: Frontend Setup
```bash
# Open a second terminal
cd c:/Users/thott/Desktop/hazardai/frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
The Vite development server will start at [http://localhost:5173](http://localhost:5173).

---

## 5. Production Operations & Maintenance Runbook

### 1. Database Maintenance & WAL Mode
The system uses SQLite at `data/hazardx_live.db`. For high concurrency, SQLite is configured in Write-Ahead Logging (WAL) mode:
```bash
sqlite3 data/hazardx_live.db "PRAGMA journal_mode=WAL;"
```

### 2. Backup Strategy
Perform automated daily backups of SQLite database:
```bash
# Online SQLite backup without taking server offline
sqlite3 data/hazardx_live.db ".backup data/hazardx_live_backup_$(date +%Y%m%d).db"
```

### 3. Monitoring Background Alert Worker
Check background alert daemon status via API:
```bash
curl http://localhost:8000/api/v1/alerts/monitor/status
```
Response:
```json
{
  "is_running": true,
  "interval_seconds": 180,
  "total_cycles_completed": 42,
  "total_alerts_generated": 15,
  "last_cycle_duration_ms": 320.5
}
```

To manually trigger an immediate cycle:
```bash
curl -X POST http://localhost:8000/api/v1/alerts/monitor/trigger
```

### 4. Running the Complete Automated Test Suite
```bash
python -m pytest backend/tests/ -v
```
All 46 tests across alerts, predictions, geospatial intelligence, and end-to-end workflows will execute.

