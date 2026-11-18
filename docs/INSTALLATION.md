# HAZARDX AI — Complete Installation & Setup Guide
**Document ID:** `HAZARDX-DOCS-INST-005`  
**Platform Version:** `v1.0.0-PROD`  

---

## 1. System Prerequisites

Before installing HAZARDX AI, verify that your environment satisfies:
- **Operating System:** Windows 10/11, Ubuntu 20.04+, macOS 12+
- **Python:** Python 3.11+ (verified on 3.11.9)
- **Node.js:** Node.js v18.0.0+ and npm 9.0.0+
- **Hardware:** Minimum 4 GB RAM (8 GB recommended); 2 GB available disk space; standard CPU (no GPU required).

---

## 2. Windows Installation (Recommended)

### Step 1: Clone Repository
```powershell
git clone https://github.com/vaishnavtt/HazardX-AI.git
cd HazardX-AI
```

### Step 2: Install Python Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Install Frontend Dependencies
```powershell
cd frontend
npm install
cd ..
```

### Step 4: One-Click Operational Launch
Double-click `START_HAZARDX.bat` in Windows File Explorer or run:
```powershell
.\START_HAZARDX.bat
```
The launcher will start the backend on port 8000, start the frontend on port 5173, and open `http://localhost:5173` in your browser.

### Shutdown
Double-click `STOP_HAZARDX.bat` to cleanly terminate background services.

---

## 3. Linux & macOS Installation

```bash
git clone https://github.com/vaishnavtt/HazardX-AI.git
cd HazardX-AI

# Install backend dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..

# Launch platform
chmod +x start_hazardx.sh
./start_hazardx.sh
```

---

## 4. Docker Deployment

```bash
# Build and run containerized platform
docker-compose up --build -d

# Check service health
docker-compose ps
```
The application will be accessible at `http://localhost:8000`.
