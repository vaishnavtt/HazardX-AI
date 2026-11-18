import React, { useState } from 'react';
import { api, formatApiError } from '../api/client';
import type { EarthquakeFeatures, EarthquakePredictionResponse } from '../types/hazard';
import { AlertBadge } from '../components/common/AlertBadge';
import { StatusIndicator } from '../components/common/StatusIndicator';
import { ShapTable } from '../components/common/ShapTable';
import { DisclaimerBanner } from '../components/common/DisclaimerBanner';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { Activity, Send, Sparkles, RotateCcw, ShieldAlert, AlertTriangle } from 'lucide-react';

const SLIP_TYPES = [
  'Subduction_Thrust',
  'Strike-Slip',
  'Normal',
  'Reverse',
  'Dextral',
  'Sinistral',
  'Normal-Dextral',
  'Normal-Sinistral',
  'Reverse-Strike-Slip',
  'Anticline',
  'Spreading_Ridge',
  'Unknown',
];

const PRESET_KUMAMOTO: EarthquakeFeatures = {
  mainshock_mag: 7.0,
  focal_depth_km: 10.0,
  dist_to_active_fault_km: 1.5,
  nearest_fault_slip_type: 'Strike-Slip',
  prior_count_7d_100km: 22,
  prior_count_30d_100km: 55,
  prior_count_365d_100km: 240,
  prior_max_mag_30d: 6.2,
  cumulative_energy_log_joules: 15.1,
  seismic_rate_accel_ratio: 2.8,
  regional_b_value: 0.88,
};

const PRESET_QUIESCENT: EarthquakeFeatures = {
  mainshock_mag: 5.1,
  focal_depth_km: 180.0,
  dist_to_active_fault_km: 45.0,
  nearest_fault_slip_type: 'Subduction_Thrust',
  prior_count_7d_100km: 1,
  prior_count_30d_100km: 4,
  prior_count_365d_100km: 25,
  prior_max_mag_30d: 3.2,
  cumulative_energy_log_joules: 11.2,
  seismic_rate_accel_ratio: 0.8,
  regional_b_value: 1.15,
};

export const EarthquakePage: React.FC = () => {
  const [formData, setFormData] = useState<EarthquakeFeatures>(PRESET_KUMAMOTO);
  const [result, setResult] = useState<EarthquakePredictionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (field: keyof EarthquakeFeatures, value: string) => {
    if (field === 'nearest_fault_slip_type') {
      setFormData((prev) => ({ ...prev, [field]: value }));
    } else if (field.includes('count')) {
      setFormData((prev) => ({ ...prev, [field]: parseInt(value, 10) || 0 }));
    } else {
      setFormData((prev) => ({ ...prev, [field]: parseFloat(value) || 0 }));
    }
  };

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await api.predictEarthquake(formData);
      setResult(res);
    } catch (err) {
      setError(formatApiError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Module Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="p-1.5 rounded-md bg-purple-950/60 border border-purple-800/40 text-purple-400">
              <Activity className="w-4 h-4" />
            </div>
            <span className="text-xs font-mono uppercase text-purple-400 font-semibold tracking-wider">
              Seismological Hazard Intelligence
            </span>
          </div>
          <h1 className="text-2xl font-bold font-mono text-white">
            Regional Aftershock Clustering Hazard Assessment
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Evaluates secondary rupture and aftershock clustering hazard in a [0, 30-day] window within 100 km of a major shallow mainshock ($M \ge 5.0$).
          </p>
        </div>

        <div className="flex items-center gap-2">
          <StatusIndicator status="OPERATIONAL" />
          <span className="text-xs font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded border border-slate-800">
            PR-AUC: <strong className="text-purple-300">0.8464</strong>
          </span>
        </div>
      </div>

      {/* Mandatory Seismological Disclaimer */}
      <DisclaimerBanner type="earthquake" />

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Form Inputs (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/40">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
              <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-300">
                Seismotectonic & Rupture Features
              </h2>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setFormData(PRESET_KUMAMOTO)}
                  className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-1 rounded bg-purple-950/50 hover:bg-purple-900/60 text-purple-300 border border-purple-800/40"
                >
                  <Sparkles className="w-3 h-3" />
                  <span>Mw 7.0 Sequence Preset</span>
                </button>
                <button
                  type="button"
                  onClick={() => setFormData(PRESET_QUIESCENT)}
                  className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700"
                >
                  <RotateCcw className="w-3 h-3" />
                  <span>Deep Quiescent Preset</span>
                </button>
              </div>
            </div>

            <form onSubmit={handlePredict} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
                <div>
                  <label className="text-slate-400 block mb-1">Triggering Mainshock Mag (Mw)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="4.5"
                    max="10.0"
                    value={formData.mainshock_mag}
                    onChange={(e) => handleChange('mainshock_mag', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Hypocentral Depth (km)</label>
                  <input
                    type="number"
                    step="1"
                    min="0"
                    max="700"
                    value={formData.focal_depth_km}
                    onChange={(e) => handleChange('focal_depth_km', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Distance to Active GEM Fault (km)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.dist_to_active_fault_km}
                    onChange={(e) => handleChange('dist_to_active_fault_km', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Nearest Fault Slip Regime</label>
                  <select
                    value={formData.nearest_fault_slip_type}
                    onChange={(e) => handleChange('nearest_fault_slip_type', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                  >
                    {SLIP_TYPES.map((st) => (
                      <option key={st} value={st}>
                        {st.replace('_', ' ')}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Prior 7-Day Seismic Count (100km)</label>
                  <input
                    type="number"
                    min="0"
                    value={formData.prior_count_7d_100km}
                    onChange={(e) => handleChange('prior_count_7d_100km', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Prior 30-Day Seismic Count (100km)</label>
                  <input
                    type="number"
                    min="0"
                    value={formData.prior_count_30d_100km}
                    onChange={(e) => handleChange('prior_count_30d_100km', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Prior 365-Day Seismicity Rate</label>
                  <input
                    type="number"
                    min="0"
                    value={formData.prior_count_365d_100km}
                    onChange={(e) => handleChange('prior_count_365d_100km', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Prior Max Magnitude (30 Days)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="10"
                    value={formData.prior_max_mag_30d}
                    onChange={(e) => handleChange('prior_max_mag_30d', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Log10 Cumulative Energy (J)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.cumulative_energy_log_joules}
                    onChange={(e) => handleChange('cumulative_energy_log_joules', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Gutenberg-Richter b-Value</label>
                  <input
                    type="number"
                    step="0.05"
                    min="0.2"
                    max="2.5"
                    value={formData.regional_b_value}
                    onChange={(e) => handleChange('regional_b_value', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full mt-2 inline-flex items-center justify-center gap-2 py-2.5 rounded-lg text-xs font-mono font-bold uppercase tracking-wider bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white shadow-lg shadow-purple-600/20 transition-all"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Evaluate Regional Aftershock Hazard</span>
              </button>
            </form>
          </div>
        </div>

        {/* Prediction Results & TreeSHAP (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          {loading && <LoadingState message="Computing Seismological Hazard..." subMessage="Evaluating Coulomb stress transfer & secondary aftershock clustering..." />}

          {error && <ErrorState message={error} onRetry={() => setError(null)} />}

          {result && !loading && (
            <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/40 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-300">
                  Aftershock Hazard Assessment
                </span>
                <AlertBadge level={result.alert_level} size="md" />
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs font-mono">
                <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                  <span className="text-slate-400 block text-[10px] uppercase">
                    Aftershock Hazard Prob
                  </span>
                  <span className="text-xl font-bold text-white">
                    {(result.hazard_probability * 100).toFixed(1)}%
                  </span>
                  <span className="text-[10px] text-purple-400 block mt-0.5">
                    M &ge; 5.0 Trigger Within 30d
                  </span>
                </div>

                <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                  <span className="text-slate-400 block text-[10px] uppercase">
                    Est. Max Aftershock Mag
                  </span>
                  <span className="text-xl font-bold text-amber-400">
                    {result.estimated_max_aftershock_magnitude !== null ? `Mw ${result.estimated_max_aftershock_magnitude.toFixed(1)}` : 'N/A'}
                  </span>
                  <span className="text-[10px] text-amber-300/80 block mt-0.5">
                    [EXPERIMENTAL ADVISORY]
                  </span>
                </div>
              </div>

              {/* Blocked model notification */}
              <div className="p-3 rounded-lg bg-rose-950/20 border border-rose-900/40 text-xs font-mono">
                <div className="flex items-center gap-1.5 text-rose-400 font-semibold mb-1">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>AFTERSHOCK COUNT REGRESSION BLOCKED</span>
                </div>
                <p className="text-[11px] text-rose-300/80 leading-normal">
                  The aftershock count regression model ($R^2 = -0.0401$) has been restricted from operational output by model governance due to heavy-tailed Omori-Utsu dispersion.
                </p>
              </div>

              <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 space-y-2 text-xs font-mono">
                <div className="flex justify-between">
                  <span className="text-slate-400">Hazard Cluster Status:</span>
                  <span className={result.elevated_aftershock_hazard_predicted ? 'text-rose-400 font-semibold' : 'text-emerald-400 font-semibold'}>
                    {result.elevated_aftershock_hazard_predicted ? 'ELEVATED AFTERSHOCK CLUSTERING' : 'QUIESCENT BACKGROUND'}
                  </span>
                </div>
                <div className="pt-2 border-t border-slate-800/80">
                  <span className="text-slate-400 block text-[10px] uppercase mb-0.5">Emergency Guidance:</span>
                  <p className="text-slate-300 font-sans text-xs leading-relaxed">
                    {result.action_guidance}
                  </p>
                </div>
              </div>

              {/* TreeSHAP Local Attributions */}
              <ShapTable attributions={result.important_contributing_features} />

              <div className="text-[11px] font-mono text-slate-400 space-y-1 bg-slate-950/40 p-3 rounded-lg border border-slate-800">
                <span className="text-slate-300 font-semibold block mb-1">Scientific Boundaries:</span>
                {result.limitations_and_warnings.map((w, idx) => (
                  <div key={idx} className="flex items-start gap-1.5">
                    <span className="text-purple-400">&bull;</span>
                    <span>{w}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {!result && !loading && (
            <div className="p-8 rounded-xl border border-dashed border-slate-800 text-center text-slate-500 font-mono text-xs">
              <Activity className="w-8 h-8 mx-auto text-slate-600 mb-2" />
              Enter triggering mainshock magnitude, depth, and fault properties to evaluate secondary aftershock hazard.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

