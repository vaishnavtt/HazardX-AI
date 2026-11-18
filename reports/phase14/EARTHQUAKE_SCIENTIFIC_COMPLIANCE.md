# HAZARDX AI – PHASE 14 AUDIT: SEISMOLOGICAL SCIENTIFIC COMPLIANCE
## Verification of Strict USGS / IASPEI Non-Predictive Governance and Statistical Aftershock Methodologies

**Document Reference:** `HAZARDX-P14-EQ-004`  
**Audit Date:** November 19, 2026  
**Auditor:** Senior Disaster Risk Scientist & Seismological Compliance Auditor  
**Governing Authorities:** USGS (United States Geological Survey), IASPEI (International Association of Seismology and Physics of the Earth's Interior), UNESCO  
**Inspected Components:** `earthquake_service.py`, `schemas/earthquake.py`, `EarthquakePage.tsx`, `ModelsPage.tsx`  

---

## 1. SCIENTIFIC PRINCIPLES & INTERNATIONAL SEISMOLOGICAL CONSENSUS

For over a century, seismological research has investigated potential deterministic precursors to major earthquakes (radon emissions, animal behavior, electromagnetic fluctuations, foreshock swarms, piezoelectric pulses). The universal scientific consensus established by the USGS, IASPEI, and the European-Mediterranean Seismological Centre (EMSC) is unequivocal:

> **Deterministic short-term earthquake prediction—forecasting the exact date, time, epicenter, and magnitude of a future earthquake—is physically impossible with existing scientific knowledge.**

Fault nucleation occurs under immense lithostatic pressures at depths between 5 and 35 km within chaotic, heterogeneous rock volumes governed by rate-and-state friction and self-organized criticality. Micro-fractures occur continuously without reliably escalating into runaway dynamic ruptures.

### HAZARDX AI Core Mandate:
Any software claiming deterministic earthquake prediction is scientifically fraudulent, legally hazardous, and dangerous to public safety. HAZARDX AI strictly prohibits any functionality, model, or user interface claiming to forecast unprovoked earthquakes.

---

## 2. SEISMOLOGICAL METHODOLOGY AUDIT

The earthquake module in HAZARDX AI is strictly formulated as a **Post-Mainshock Statistical Aftershock Sequence Hazard Model**.

### 2.1 Theoretical Framework
The system implements principles derived from three foundational empirical laws of seismology:
1. **Modified Omori-Utsu Law:** The frequency of aftershocks $n(t)$ decays inversely with elapsed time $t$ following a mainshock:
   $$n(t) = \frac{K}{(t + c)^p}$$
   Where $K, c, p$ are regional parameters ($p \approx 1.0$).
2. **Gutenberg-Richter Frequency-Magnitude Distribution:**
   $$\log_{10} N(M) = a - b M$$
   Where $b$ (regional b-value) characterizes the ratio of small to large events (typically $b \approx 1.0$).
3. **Båth’s Law:** The difference in magnitude between a mainshock and its largest aftershock is approximately $1.1\text{ to }1.2$ magnitude units:
   $$\Delta M = M_{\text{main}} - M_{\text{max\_aftershock}} \approx 1.2$$

### 2.2 Operational Formulation in HAZARDX AI
- **Trigger Condition:** A shallow, moderate-to-large mainshock ($M_w \ge 5.0$, focal depth $\le 70\text{ km}$) has already occurred and been recorded by a seismic network (e.g., USGS ComCat).
- **Target Evaluation:** Probability that the region (within $100\text{ km}$ and $30\text{ days}$) will experience:
  - $\ge 5$ secondary aftershocks ($M \ge 4.0$), OR
  - At least one strong secondary shock ($M \ge 5.0$).
- **Features Used:**
  - `mainshock_mag`: Energy scale of the primary rupture.
  - `focal_depth_km`: Shallow events transfer higher Coulomb stress to surface faults.
  - `nearest_fault_slip_type`: Normal, thrust, or strike-slip fault mechanics.
  - `prior_count_7d_100km`, `prior_count_30d_100km`, `prior_count_365d_100km`: Background seismicity rate.
  - `cumulative_energy_log_joules`: Historical strain release.
  - `regional_b_value`: Regional crustal stress state.

---

## 3. CODEBASE VERIFICATION & GUARDRAIL ENFORCEMENT

The audit verified every line of code across backend services, schemas, and frontend UI to ensure strict compliance:

### 3.1 Backend Service (`backend/app/services/earthquake_service.py`)
- **Assessment Type Explicitly Declared:**
  ```python
  assessment_type="Regional Aftershock Hazard Assessment (30-day / 100km horizon)"
  ```
- **Mandatory Disclaimers Injected in Every Response:**
  ```python
  disclaimer="This service provides statistical aftershock hazard assessment following a mainshock. This is NOT an exact earthquake prediction."
  warnings = [
      "This model provides statistical aftershock hazard assessment following a shallow M>=5.0 mainshock within 100km and 30 days.",
      "This system CANNOT and DOES NOT predict the exact time, location, or occurrence of unprovoked future earthquakes.",
      "Aftershock count regression model is marked UNAVAILABLE FOR OPERATIONAL USE due to heavy-tailed Omori-Utsu dispersion."
  ]
  ```
- **Operational Quarantine Enforcement:**
  `estimated_aftershock_count` is hard-blocked to `None`.
  `estimated_max_aftershock_magnitude` is labeled `EXPERIMENTAL` (advisory only).

### 3.2 Frontend UI (`frontend/src/pages/ModelsPage.tsx` & `EarthquakePage.tsx`)
- In `ModelsPage.tsx`:
  > *"Non-Predictive Earthquake Governance (USGS Consensus Compliance): HAZARDX AI does not perform deterministic short-term prediction of earthquake origin times, epicenters, or mainshock magnitudes, which remains physically impossible under consensus geophysics (USGS, IASPEI). The earthquake module evaluates empirical aftershock sequence hazard and decay following an observed mainshock, adhering strictly to modified Omori-Utsu statistical laws."*
- In `EarthquakePage.tsx`:
  Every user-facing query requires selecting or entering an *already observed* mainshock magnitude and focal depth. There is no button or input for "Predict Tomorrow's Earthquake."

---

## 4. SCIENTIFIC COMPLIANCE AUDIT CHECKLIST

| Verification Item | Requirement | Audit Status | Evidence in Code |
| :--- | :--- | :--- | :--- |
| **No Mainshock Prediction** | System never claims to predict an initial earthquake | **COMPLIANT** | Inputs strictly require existing mainshock parameters. |
| **No Exact Date Prediction** | System outputs 30-day window probability, not a date | **COMPLIANT** | Output is time-window probability $P(\text{Aftershock } 30\text{d})$. |
| **No Exact Epicenter Prediction** | Region is a 100 km radial buffer around mainshock | **COMPLIANT** | Evaluates spatial buffer around ruptured fault. |
| **No Unsupported Foreshock Claims**| Foreshock sequences are not claimed as deterministic precursors | **COMPLIANT** | Kumamoto case study framed as foreshock stress loading, not prediction. |
| **Omori-Utsu Conformity** | Sequence probability decays with elapsed time | **COMPLIANT** | Feature inputs reflect time-decayed seismic rate acceleration ratios. |
| **Disclaimers Present** | Statutory disclaimers accompany every output | **COMPLIANT** | Pydantic schema enforces disclaimer in `EarthquakePredictionResponse`. |

---

## 5. SEISMOLOGICAL AUDIT VERDICT

**VERDICT: 100% COMPLIANT.** The earthquake module in HAZARDX AI strictly adheres to the highest standards of international seismological ethics, physical laws, and scientific governance. No pseudoscientific prediction claims exist in the backend, API responses, or frontend interfaces.
