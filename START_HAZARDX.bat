@echo off
setlocal enabledelayedexpansion
title HAZARDX AI - Global Multi-Hazard Intelligence Startup
cls

echo ===============================================================================
echo               HAZARDX AI - GLOBAL MULTI-HAZARD INTELLIGENCE
echo                  One-Click Operational Platform Startup
echo ===============================================================================
echo.

:: 1. Verify Directory
if not exist "backend\app\main.py" (
    echo [ERROR] Must run from HAZARDX AI project root directory!
    echo Current location: %CD%
    pause
    exit /b 1
)

:: 2. Check Python
echo [1/5] Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not found in PATH!
    echo Please install Python 3.11 from python.org and add it to PATH.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version') do set PYTHON_VER=%%v
echo       Found: !PYTHON_VER!

:: 3. Check Node & npm
echo [2/5] Checking Node.js and npm...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not found in PATH!
    echo Please install Node.js LTS from nodejs.org and add it to PATH.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('node --version') do set NODE_VER=%%v
echo       Found: Node !NODE_VER!

:: 4. Check & Start FastAPI Backend (Port 8000)
echo [3/5] Checking FastAPI Backend (Port 8000)...
set BACKEND_RUNNING=0
netstat -ano | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    set BACKEND_RUNNING=1
    echo       FastAPI Backend is ALREADY RUNNING on port 8000.
) else (
    echo       Starting FastAPI Backend on http://127.0.0.1:8000...
    start "HAZARDX_AI_BACKEND" /min cmd /c "python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000"
    timeout /t 3 /nobreak >nul
)

:: 5. Check & Start Vite Frontend (Port 5173)
echo [4/5] Checking Vite Frontend (Port 5173)...
set FRONTEND_RUNNING=0
netstat -ano | findstr ":5173" | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    set FRONTEND_RUNNING=1
    echo       Vite Frontend is ALREADY RUNNING on port 5173.
) else (
    echo       Starting Vite Frontend on http://localhost:5173...
    start "HAZARDX_AI_FRONTEND" /min cmd /c "npm run dev --prefix frontend"
    timeout /t 3 /nobreak >nul
)

:: 6. Launch Browser
echo [5/5] Launching HAZARDX AI in default browser...
timeout /t 2 /nobreak >nul
start http://localhost:5173

echo.
echo ===============================================================================
echo                HAZARDX AI IS RUNNING SUCCESSFULLY!
echo ===============================================================================
echo   - Web Mission Control:  http://localhost:5173
echo   - FastAPI Backend API:  http://127.0.0.1:8000
echo   - API Documentation:    http://127.0.0.1:8000/docs
echo.
echo   To stop the application cleanly, run:  STOP_HAZARDX.bat
echo ===============================================================================
echo.
echo Press any key to exit this launcher window (services keep running in background)...
pause >nul
