"""
HAZARDX AI — Statistical Omori-Utsu & Reasenberg-Jones Aftershock Forecaster
Provides probabilistic forecasting of aftershock occurrences following a significant mainshock
in strict accordance with USGS aftershock sequence methodologies.
(NOT deterministic earthquake prediction).
"""

import math
from datetime import datetime, timezone
from typing import Dict, Any, List

class OmoriAftershockForecaster:
    """
    Standard Reasenberg & Jones (1989, 1994) / Utsu (1961) generic model parameters:
    a = -1.67 (generic global productivity)
    b = 1.00 (Gutenberg-Richter scaling)
    p = 1.05 (Omori temporal decay exponent)
    c = 0.05 days (~1.2 hours offset)
    """
    def __init__(self, a: float = -1.67, b: float = 1.00, p: float = 1.05, c: float = 0.05):
        self.a = a
        self.b = b
        self.p = p
        self.c = c

    def calculate_aftershock_probability(
        self,
        mainshock_mag: float,
        target_mag: float,
        time_since_mainshock_days: float,
        forecast_window_days: float,
        distance_km: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculates expected rate lambda and Poisson probability P(N >= 1) of an aftershock
        with magnitude >= target_mag in the future window [t, t + delta_t] at distance r.
        Includes USGS/Kagan-style spatial distance attenuation kernel.
        """
        if mainshock_mag < 4.0:
            return {
                "mainshock_mag": round(mainshock_mag, 2),
                "target_mag": round(target_mag, 2),
                "distance_km": round(distance_km, 1),
                "time_since_mainshock_days": round(time_since_mainshock_days, 3),
                "forecast_window_days": round(forecast_window_days, 3),
                "expected_count": 0.0,
                "probability": 0.0
            }

        t = max(0.001, time_since_mainshock_days)
        dt = max(0.001, forecast_window_days)

        # Reasenberg-Jones formula
        # 10^(a + b*(Mm - Mtarget))
        k_val = 10.0 ** (self.a + self.b * (mainshock_mag - target_mag))

        if abs(self.p - 1.0) < 1e-4:
            integral = math.log((t + dt + self.c) / (t + self.c))
        else:
            integral = ((t + dt + self.c) ** (1.0 - self.p) - (t + self.c) ** (1.0 - self.p)) / (1.0 - self.p)

        # Spatial distance attenuation kernel rho(r) = 1 / (1 + (r / r0)^2)
        # r0 scales with fault rupture length L(Mw) ~ 10^(-2.0 + 0.5 * Mw) (Wells & Coppersmith 1994)
        r0 = max(2.0, 10.0 ** (-2.0 + 0.5 * mainshock_mag))
        spatial_weight = 1.0 / (1.0 + (distance_km / r0) ** 2)

        expected_count = max(0.0, k_val * integral * spatial_weight)
        
        if expected_count < 1e-6:
            prob = 0.0
        else:
            prob = 1.0 - math.exp(-expected_count)
            prob = min(0.9999, prob)

        return {
            "mainshock_mag": round(mainshock_mag, 2),
            "target_mag": round(target_mag, 2),
            "distance_km": round(distance_km, 1),
            "time_since_mainshock_days": round(t, 3),
            "forecast_window_days": round(dt, 3),
            "expected_count": round(expected_count, 4),
            "probability": round(prob, 4)
        }

    def forecast_horizons(self, mainshock_mag: float, elapsed_hours: float = 2.0, distance_km: float = 0.0) -> Dict[str, Any]:
        """
        Calculates aftershock probabilities across standard forecast horizons: 6h, 12h, 24h, 48h, 72h
        for M4.0+ and M5.0+ aftershocks at a given epicentral distance.
        """
        t_days = max(0.01, elapsed_hours / 24.0)
        horizons_map = {
            "6h": 6.0 / 24.0,
            "12h": 12.0 / 24.0,
            "24h": 24.0 / 24.0,
            "48h": 48.0 / 24.0,
            "72h": 72.0 / 24.0
        }

        results = {}
        for h_name, dt_days in horizons_map.items():
            m4_calc = self.calculate_aftershock_probability(mainshock_mag, 4.0, t_days, dt_days, distance_km=distance_km)
            m5_calc = self.calculate_aftershock_probability(mainshock_mag, 5.0, t_days, dt_days, distance_km=distance_km)

            p_m4 = m4_calc["probability"]
            if mainshock_mag < 4.0 or p_m4 < 0.05:
                risk_cat = "QUIESCENT"
            elif p_m4 >= 0.80:
                risk_cat = "EXTREME"
            elif p_m4 >= 0.60:
                risk_cat = "VERY HIGH"
            elif p_m4 >= 0.40:
                risk_cat = "HIGH"
            elif p_m4 >= 0.20:
                risk_cat = "MODERATE"
            else:
                risk_cat = "LOW"

            results[h_name] = {
                "horizon": h_name,
                "prob_m4_plus": p_m4,
                "prob_m5_plus": m5_calc["probability"],
                "expected_m4_count": m4_calc["expected_count"],
                "risk_score": p_m4,
                "risk_category": risk_cat,
                "distance_km": round(distance_km, 1),
                "model_type": "Omori-Utsu / Reasenberg-Jones Spatial & Temporal Decay",
                "disclaimer": "Probabilistic aftershock assessment following mainshock. NOT an exact earthquake prediction."
            }

        return results

omori_model = OmoriAftershockForecaster()

