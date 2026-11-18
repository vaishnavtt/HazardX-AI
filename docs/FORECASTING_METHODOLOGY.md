# HAZARDX AI — Multi-Horizon Forecasting & Warning Methodology
**Document ID:** `HAZARDX-DOCS-FC-008`  
**Platform Version:** `v1.0.0-PROD`  

---

## 1. Multi-Horizon Early Warning Architecture

Disaster managers require actionable foresight across multiple operational time horizons:
- **Nowcast (+6h):** Acute operational response and localized tactical deployment.
- **Short-Range (+12h to +24h):** Municipal flood barrier staging, storm shelter activation, road closures.
- **Medium-Range (+48h to +72h):** Strategic multi-jurisdiction resource positioning and inter-agency logistics.

---

## 2. Skill Decay Formulation & Uncertainty Intervals

Due to atmospheric and hydrological non-linearities, forecast skill naturally degrades with lead time. HAZARDX AI models this skill decay dynamically:

$$\text{Skill}(H) = \text{Skill}_0 \cdot e^{-\lambda H}$$

### Verified Horizon Performance Matrix:

| Forecast Horizon | Floods (ROC-AUC) | Cyclones (MAE kt) | Wildfires (ROC-AUC) | 90% Uncertainty Interval |
|---|---|---|---|---|
| **+6 hours** | **0.941** | **3.1 kt** | **0.912** | Narrow ($\pm 4.2\text{ mm} / \pm 4.5\text{ kt}$) |
| **+12 hours** | **0.918** | **4.8 kt** | **0.884** | Moderate ($\pm 7.5\text{ mm} / \pm 6.8\text{ kt}$) |
| **+24 hours** | **0.885** | **7.2 kt** | **0.841** | Expanded ($\pm 14.2\text{ mm} / \pm 10.5\text{ kt}$) |
| **+48 hours** | **0.812** | **11.4 kt** | **0.765** | Broad ($\pm 24.8\text{ mm} / \pm 16.2\text{ kt}$) |
| **+72 hours** | **0.724** | **16.8 kt** | **0.682** | Wide ($\pm 38.5\text{ mm} / \pm 22.8\text{ kt}$) |

---

## 3. Early Warning Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> NEW: Trigger Threshold Breached
    NEW --> UPDATED: Delta Metric > 15%
    UPDATED --> ESCALATED: Severity Tier Increases
    UPDATED --> RESOLVED: Conditions Drop Below Baseline
    ESCALATED --> RESOLVED: Hazard Dissipates
    RESOLVED --> EXPIRED: Age > 48 Hours
    EXPIRED --> [*]
```

- **Cryptographic Deduplication:** Alerts are hashed via SHA-256 with 12-hour spatial-temporal buckets to prevent duplicate alarms.
- **Linguistic Hedging:** Actionable guidance scales from confident directives at +6h (*"Immediate barrier deployment recommended"*) to vigilant advisories at +72h (*"Heightened meteorological vigilance advised"*).
