@echo off
setlocal enabledelayedexpansion
title HAZARDX AI - Stop Platform Services
cls

echo ===============================================================================
echo                HAZARDX AI - SHUTTING DOWN PLATFORM SERVICES
echo ===============================================================================
echo.

set KILLED_COUNT=0

:: 1. Terminate Backend on Port 8000
echo Checking for FastAPI Backend on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
    set PID=%%a
    if defined PID (
        if not "!PID!"=="0" (
            echo Terminating Backend process PID: !PID!
            taskkill /F /PID !PID! >nul 2>&1
            set /a KILLED_COUNT+=1
        )
    )
)

:: 2. Terminate Frontend on Port 5173
echo Checking for Vite Frontend on port 5173...
for /f "tokens=5" %%b in ('netstat -ano ^| findstr ":5173" ^| findstr "LISTENING"') do (
    set PID=%%b
    if defined PID (
        if not "!PID!"=="0" (
            echo Terminating Frontend process PID: !PID!
            taskkill /F /PID !PID! >nul 2>&1
            set /a KILLED_COUNT+=1
        )
    )
)

echo.
echo ===============================================================================
if !KILLED_COUNT! gtr 0 (
    echo [SUCCESS] HAZARDX AI services stopped cleanly (!KILLED_COUNT! processes terminated).
) else (
    echo [INFO] No active HAZARDX AI services were detected on ports 8000 or 5173.
)
echo ===============================================================================
echo.
timeout /t 3 /nobreak >nul
