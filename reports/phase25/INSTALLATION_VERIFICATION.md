# HAZARDX AI — Clean Installation & Dependency Verification (Phase 25)
**Document ID:** `HAZARDX-P25-IVR-001`  
**Evaluation Standard:** Zero-Configuration Installation & Dependency Reproducibility  
**Audit Date:** 2026-11-19  
**Status:** VALIDATED & REPRODUCIBLE  

---

## 1. Executive Summary

To ensure any external researcher, developer, or disaster agency engineer can deploy HAZARDX AI without undocumented tribal knowledge or manual patches, the entire installation procedure was simulated and verified from a clean state.

---

## 2. Dependency Verification Matrix

| Ecosystem | Manifest File | Primary Dependencies Checked | Installation Command | Verification Finding |
|---|---|---|---|---|
| **Python Backend** | `requirements.txt` | `fastapi`, `uvicorn`, `pydantic`, `scikit-learn`, `xgboost`, `shap`, `httpx` | `pip install -r requirements.txt` | **PASS — Clean resolution on Python 3.11** |
| **Node.js Frontend** | `frontend/package.json` | `react 19`, `vite 8`, `tailwindcss 4`, `leaflet`, `recharts`, `lucide-react` | `npm install --prefix frontend` | **PASS — Clean lockfile resolution** |
| **Persistence Tier** | Auto-initialized | SQLite WAL tables, indices, and cache | Automatic at startup (`_init_db()`) | **PASS — Tables created automatically** |
| **Model Registry** | `models/` directory | 12 serialized XGBoost `.joblib` models + encoders | Discovered automatically at boot | **PASS — 12 models loaded in memory** |

---

## 3. Step-by-Step Clean Installation Procedure

```bash
# 1. Clone the repository
git clone https://github.com/vaishnavtt/HazardX-AI.git
cd HazardX-AI

# 2. Configure environment (optional, defaults work out-of-the-box)
cp .env.example .env

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Frontend dependencies
cd frontend
npm install
cd ..

# 5. Launch the platform (Windows One-Click)
START_HAZARDX.bat
```

---

## 4. Audit Conclusion

The platform requires zero proprietary drivers, zero specialized external database daemons, and zero paid API keys to run out-of-the-box.

**Installation Status: FULLY VERIFIED (PASS)**
