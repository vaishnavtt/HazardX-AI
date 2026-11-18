# HAZARDX AI — FINAL DEPLOYMENT & OPERATIONS GUIDE

**Author:** DevOps & Systems Infrastructure Team  
**Date:** March 2026  
**Document Classification:** Final Project Milestone Deliverable  
**Repository Location:** `C:\Users\thott\Desktop\hazardai`  
**Target Environment:** Windows 10/11 & Containerized Docker Orchestration

---

## 1. Executive Summary

This guide provides complete, non-technical instructions for launching, operating, and maintaining the **HAZARDX AI** platform on a local Windows computer or in production containers.

The application is configured for **one-click startup** without requiring manual terminal configuration or complex developer environments.

---

## 2. One-Click Windows Operation (Primary Method)

The project includes pre-configured, automated batch scripts designed for everyday operators:

### 2.1 Starting HAZARDX AI
To start the platform:
1. Open the project directory: `C:\Users\thott\Desktop\hazardai`
2. Double-click `START_HAZARDX.bat` (or run `.\START_HAZARDX.bat` from terminal).
3. The script will automatically:
   - Verify Python 3.11, Node.js, and npm.
   - Detect and launch the FastAPI backend on `http://127.0.0.1:8000` (port 8000).
   - Detect and launch the Vite React frontend on `http://localhost:5173` (port 5173).
   - Automatically open your default web browser to `http://localhost:5173`.
   - Prevent duplicate server instances if already listening.

### 2.2 Stopping HAZARDX AI
To stop the platform:
1. Double-click `STOP_HAZARDX.bat` in the project directory.
2. The script terminates only the processes running on ports 8000 and 5173 without affecting any unrelated system applications.

---

## 3. System Requirements & Port Allocations

- **Operating System:** Windows 10 / 11, Linux, or macOS.
- **Hardware Profile Tested:** Intel Core i5 / AMD Ryzen 5, 16 GB RAM, NVIDIA RTX 4050 Laptop GPU (or standard integrated graphics; GPU acceleration is optional).
- **Core Dependencies:**
  - Python: `3.11.x`
  - Node.js: `v18.x` – `v22.x`
  - npm: `9.x` – `10.x`
- **Network Ports:**
  - `8000`: FastAPI Backend API (`http://127.0.0.1:8000`)
  - `5173`: React Web Application (`http://localhost:5173`)

---

## 4. Manual Developer Commands (Alternative)

If manual execution is preferred:

### Terminal 1: Backend
```powershell
cd C:\Users\thott\Desktop\hazardai
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Terminal 2: Frontend
```powershell
cd C:\Users\thott\Desktop\hazardai\frontend
npm run dev
```

### Run Automated Backend Tests
```powershell
cd C:\Users\thott\Desktop\hazardai
python -m pytest backend/tests/ -v
```

### Run Frontend Production Build
```powershell
cd C:\Users\thott\Desktop\hazardai\frontend
npm run build
```

---

## 5. Docker Multi-Container Production Deployment

The project provides complete Docker support:
- `docker-compose.yml`: Multi-container configuration mounting persistent volumes for SQLite and datasets.
- `Dockerfile.backend`: Python 3.11 Slim container with pre-loaded XGBoost artifacts.
- `Dockerfile.frontend`: Multi-stage Node 20 build with Nginx reverse proxy.

### To Launch with Docker:
```bash
docker-compose up -d --build
```
Access points:
- Web Application: `http://localhost:80`
- API Documentation: `http://localhost:80/docs`
