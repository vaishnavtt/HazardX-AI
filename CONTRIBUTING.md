# Contributing to HAZARDX AI

Thank you for your interest in contributing to **HAZARDX AI: Global Multi-Hazard Intelligence and Early Warning System**!

We welcome contributions from meteorologists, hydrologists, seismologists, data scientists, full-stack engineers, and open-source developers.

---

## Code of Conduct
By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Development Workflow

1. **Fork the Repository:** Create your own branch (`git checkout -b feature/amazing-hazard-feature`).
2. **Set Up Local Environment:** Follow the setup guide in [docs/INSTALLATION.md](docs/INSTALLATION.md).
3. **Run Existing Test Suite:**
   ```bash
   python -m pytest backend/tests
   npm run build --prefix frontend
   ```
4. **Adhere to Scientific Governance Rules:**
   - Never claim deterministic prediction of earthquakes.
   - Any new machine learning model must be evaluated on independent holdout data ($R^2 > 0.20$ or $\text{PR-AUC} > 0.30$).
   - Never display ungrounded synthetic or fake data when upstream APIs fail.
5. **Commit with Meaningful Messages:** Follow Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`).
6. **Open a Pull Request:** Describe the physical scientific rationale and software tests accompanying your changes.

---

## Reporting Issues & Vulnerabilities
To report a bug, open an issue on GitHub. To report a security vulnerability, refer to our [Security Policy](SECURITY.md).
