# HAZARDX AI - PowerShell Platform Launcher
# One-Click Startup for Windows PowerShell

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "              HAZARDX AI - GLOBAL MULTI-HAZARD INTELLIGENCE" -ForegroundColor Cyan
Write-Host "                 PowerShell Operational Platform Startup" -ForegroundColor Cyan
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verify Directory
if (-not (Test-Path "backend\app\main.py")) {
    Write-Host "[ERROR] Must run from HAZARDX AI project root directory!" -ForegroundColor Red
    Write-Host "Current location: $PWD"
    exit 1
}

# 2. Check Python
Write-Host "[1/5] Checking Python environment..." -ForegroundColor Yellow
try {
    $pythonVer = python --version 2>&1
    Write-Host "      Found: $pythonVer" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not found in PATH! Please install Python 3.11+." -ForegroundColor Red
    exit 1
}

# 3. Check Node & npm
Write-Host "[2/5] Checking Node.js and npm..." -ForegroundColor Yellow
try {
    $nodeVer = node --version 2>&1
    Write-Host "      Found: Node $nodeVer" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js is not found in PATH! Please install Node.js LTS." -ForegroundColor Red
    exit 1
}

# 4. Check & Start FastAPI Backend (Port 8000)
Write-Host "[3/5] Checking FastAPI Backend (Port 8000)..." -ForegroundColor Yellow
$backendActive = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($backendActive) {
    Write-Host "      FastAPI Backend is ALREADY RUNNING on port 8000." -ForegroundColor Green
} else {
    Write-Host "      Starting FastAPI Backend on http://127.0.0.1:8000..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000" -WindowStyle Minimized
    Start-Sleep -Seconds 3
}

# 5. Check & Start Vite Frontend (Port 5173)
Write-Host "[4/5] Checking Vite Frontend (Port 5173)..." -ForegroundColor Yellow
$frontendActive = Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue
if ($frontendActive) {
    Write-Host "      Vite Frontend is ALREADY RUNNING on port 5173." -ForegroundColor Green
} else {
    Write-Host "      Starting Vite Frontend on http://localhost:5173..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev --prefix frontend" -WindowStyle Minimized
    Start-Sleep -Seconds 3
}

# 6. Launch Browser
Write-Host "[5/5] Launching HAZARDX AI in default browser..." -ForegroundColor Yellow
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "                HAZARDX AI IS RUNNING SUCCESSFULLY!" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "  - Web Mission Control:  http://localhost:5173" -ForegroundColor White
Write-Host "  - FastAPI Backend API:  http://127.0.0.1:8000" -ForegroundColor White
Write-Host "  - API Documentation:    http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "  To stop the application cleanly, run:  .\STOP_HAZARDX.bat" -ForegroundColor Yellow
Write-Host "===============================================================================" -ForegroundColor Cyan
