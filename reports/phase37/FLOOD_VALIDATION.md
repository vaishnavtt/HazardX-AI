# Phase 37 — Flood Hazard Validation & Bayesian Prior Audit

## 1. Audit of Bayesian Prior Odds Correction

In `backend/app/utils/calibration.py` (lines 10–27):
```python
def adjust_case_control_probability(p_model: float, real_world_prior: float) -> float:
    p_clamped = max(1e-6, min(1.0 - 1e-6, p_model))
    pi_clamped = max(1e-6, min(1.0 - 1e-6, real_world_prior))
    logit_model = math.log(p_clamped / (1.0 - p_clamped))
    logit_prior = math.log(pi_clamped / (1.0 - pi_clamped))
    logit_calibrated = logit_model + logit_prior
    return float(round(1.0 / (1.0 + math.exp(-logit_calibrated)), 6))
```

### 1.1 Mathematical Verification
Let $Y \in \{0, 1\}$ be the event occurrence indicator, and $X$ be the feature vector.
In a 1:1 case-control balanced training set, $P_{\text{train}}(Y=1) = \pi_{\text{train}} = 0.5$.
Using Bayes' rule:
$$\ln\left(\frac{P(Y=1 \mid X)}{P(Y=0 \mid X)}\right) = \ln\left(\frac{P(X \mid Y=1)}{P(X \mid Y=0)}\right) + \ln\left(\frac{\pi_{\text{pop}}}{1 - \pi_{\text{pop}}}\right)$$
Since $\ln(\pi_{\text{train}} / (1 - \pi_{\text{train}})) = \ln(1) = 0$, the log-odds output of the model equals the log-likelihood ratio.
Adding $\text{logit}(\pi_{\text{pop}})$ correctly recovers the population posterior log-odds.
**Conclusion on Formula:** The mathematical formula itself is formally correct for case-control reweighting.

### 1.2 Flaw 1: Fixed Global Climatological Scalar
The system sets `CLIMATOLOGICAL_PRIORS["floods"] = 0.005` (representing $\approx 1.8$ flood days per year globally).
Applying this identical prior everywhere ignores:
- **Geomorphic Position:** A 10-year active floodplain adjacent to a major river has a prior far higher than a high-altitude granite ridge.
- **Catchment Scale:** Upstream basin area ($A_{\text{catchment}}$) strongly influences lag times and peak discharge magnitude.

### 1.3 Flaw 2: The Palakkad Alert Incoherence Discrepancy
In `backend/app/services/flood_service.py` (lines 53–54):
```python
risk_cat, alert_lvl, guidance = categorize_hazard_risk(self.hazard, raw_prob)
```
Notice: `categorize_hazard_risk` received **`raw_prob`** ($0.72$), but `geospatial.py` mapped the risk probability to **`calibrated_susceptibility_score`** ($0.0106$).
In Palakkad, Kerala:
- The card displayed: `Alert: ORANGE`, `Estimated Probability: 1.06%`.
- An emergency advisory (`ORANGE`) was issued for a $1\%$ event probability.

**Mandated Correction:**
Risk categorization and alert levels must be derived strictly from calibrated probabilities or standardized physical metrics (such as GloFAS return period thresholds: 2-year, 5-year, 20-year), eliminating the disconnect between alert levels and displayed probabilities.
