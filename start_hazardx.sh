#!/usr/bin/env bash
# HAZARDX AI - Unix Platform Launcher
# One-Click Startup for Linux and macOS

set -e

echo "==============================================================================="
echo "              HAZARDX AI - GLOBAL MULTI-HAZARD INTELLIGENCE"
echo "                   Unix Operational Platform Startup"
echo "==============================================================================="
echo ""

# 1. Verify Directory
if [ ! -f "backend/app/main.py" ]; then
    echo "[ERROR] Must run from HAZARDX AI project root directory!"
    echo "Current location: $(pwd)"
    exit 1
fi

# 2. Check Python
echo "[1/5] Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 is not found in PATH! Please install Python 3.11+."
    exit 1
fi
echo "      Found: $(python3 --version)"

# 3. Check Node & npm
echo "[2/5] Checking Node.js and npm..."
if ! command -v node &> /dev/null; then
    echo "[ERROR] node is not found in PATH! Please install Node.js LTS."
    exit 1
fi
echo "      Found: Node $(node -v)"

# 4. Check & Start FastAPI Backend (Port 8000)
echo "[3/5] Checking FastAPI Backend (Port 8000)..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "      FastAPI Backend is ALREADY RUNNING on port 8000."
else
    echo "      Starting FastAPI Backend on http://127.0.0.1:8000..."
    python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 &
    BACKEND_PID=$!
    echo "      Backend running under PID: $BACKEND_PID"
    sleep 3
fi

# 5. Check & Start Vite Frontend (Port 5173)
echo "[4/5] Checking Vite Frontend (Port 5173)..."
if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null ; then
    echo "      Vite Frontend is ALREADY RUNNING on port 5173."
else
    echo "      Starting Vite Frontend on http://localhost:5173..."
    npm run dev --prefix frontend &
    FRONTEND_PID=$!
    echo "      Frontend running under PID: $FRONTEND_PID"
    sleep 3
fi

# 6. Launch Browser
echo "[5/5] Launching HAZARDX AI in default browser..."
if command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:5173" &
elif command -v open &> /dev/null; then
    open "http://localhost:5173" &
fi

echo ""
echo "==============================================================================="
echo "                HAZARDX AI IS RUNNING SUCCESSFULLY!"
echo "==============================================================================="
echo "  - Web Mission Control:  http://localhost:5173"
echo "  - FastAPI Backend API:  http://127.0.0.1:8000"
echo "  - API Documentation:    http://127.0.0.1:8000/docs"
echo "==============================================================================="
