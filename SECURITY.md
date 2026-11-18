# Security Policy

## Supported Versions
Security updates and vulnerability patches are actively maintained for the following versions of HAZARDX AI:

| Version | Supported |
|---|---|
| `v1.0.x` | :white_check_mark: Active Support |
| `< 1.0.0`| :x: Unsupported (Preliminary Prototypes) |

---

## Reporting a Vulnerability

The HAZARDX AI engineering team takes software security seriously. If you discover a security vulnerability or suspect an exposed credential:

1. **Do NOT open a public GitHub issue.**
2. Send an email to the project maintainers with details, steps to reproduce, and impact assessment.
3. Maintainers will acknowledge receipt within 48 hours and work with you on a coordinated disclosure timeline.

---

## Security Invariants

- **Zero Hardcoded Secrets:** All credentials, tokens, and keys must be injected via environment variables.
- **Strict Input Validation:** All API inputs are sanitized and bounded through Pydantic v2 schemas.
- **SQL Injection Defense:** Parameterized queries only (`?` bind parameters).
