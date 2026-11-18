# HAZARDX AI — Environment Configuration & Secrets Hygiene Audit (Phase 25)
**Document ID:** `HAZARDX-P25-ECA-003`  
**Evaluation Standard:** 12-Factor App Config & OWASP Credential Hygiene  
**Audit Date:** 2026-11-19  
**Status:** SANITIZED & VALIDATED  

---

## 1. Executive Summary

Disaster intelligence platforms must never embed production secrets, database credentials, or private email passwords in version control. All configuration must be externalized into environment variables with sensible, zero-configuration defaults for open-source evaluation.

This report evaluates `.env.example`, `.gitignore`, and the configuration binding engine in `backend/app/config.py`.

---

## 2. Environment Variable Reference Guide

| Variable Name | Default Value | Required? | Purpose & Impact |
|---|---|---|---|
| `HOST` | `127.0.0.1` | No | Server binding interface (`0.0.0.0` for Docker/network). |
| `PORT` | `8000` | No | ASGI server listening port. |
| `DEBUG` | `false` | No | Enables detailed diagnostic logs; set to `false` in production. |
| `API_V1_PREFIX` | `/api/v1` | No | Base routing prefix for all REST microservices. |
| `NASA_FIRMS_MAP_KEY` | *(Empty)* | Optional | NASA FIRMS MAP_KEY for direct active fire streaming. Defaults to open VIIRS public feed. |
| `ALERT_MONITOR_ENABLED` | `true` | No | Controls background daemon evaluating real-time early warnings. |
| `ALERT_MONITOR_INTERVAL_SECONDS` | `180` | No | Polling frequency for background telemetry ingestion. |
| `ALERT_MAX_AGE_HOURS` | `48` | No | Expiration window for resolving historical alerts. |
| `ALERT_DEDUP_WINDOW_HOURS` | `12` | No | Deduplication suppression window for duplicate alerts. |
| `SMTP_HOST` | *(Empty)* | Optional | SMTP mail host for email alerts. Falls back to mock logger if unconfigured. |
| `SMTP_PORT` | `587` | Optional | Standard SMTP submission port with TLS. |
| `ALERT_EMAIL_MIN_SEVERITY` | `ORANGE` | No | Minimum threshold (`YELLOW`, `ORANGE`, `RED`) to trigger email dispatch. |
| `VITE_API_BASE_URL` | `http://127.0.0.1:8000/api/v1` | No | Frontend API proxy endpoint. |

---

## 3. Credential Hygiene and Secret Sanitization

- **Static Secret Scan:** Verified 0 hardcoded credentials in the repository.
- **Sanitized Template:** `.env.example` provides complete documentation while keeping all sensitive credential fields empty.
- **Git Protection:** `.gitignore` excludes `.env`, `.env.local`, `*.pem`, `*.key`, and temporary secrets.

---

## 4. Audit Conclusion

The environment configuration architecture is completely sanitized, adheres to 12-factor principles, and allows seamless out-of-the-box local startup.

**Configuration Status: SANITIZED & APPROVED (PASS)**
