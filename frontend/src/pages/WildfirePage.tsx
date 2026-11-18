import React, { useState } from 'react';
import { api, formatApiError } from '../api/client';
import type { WildfireFeatures, WildfirePredictionResponse } from '../types/hazard';
import { AlertBadge } from '../components/common/AlertBadge';
import { StatusIndicator } from '../components/common/StatusIndicator';
import { ShapTable } from '../components/common/ShapTable';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { Flame, Send, Sparkles, RotateCcw, AlertTriangle } from 'lucide-react';

const PRESET_EXTREME_FIRE: WildfireFeatures = {
  temp_2m_celsius: 38.0,
  relative_humidity_pct: 9.5,
  wind_speed_10m_ms: 14.0,
  precip_7d_sum_mm: 0.0,
  precip_30d_sum_mm: 1.0,
  soil_temp_celsius: 40.0,
  fwi_fire_weather_index: 54.0,
  slope_degrees: 22.0,
  elevation_m: 680.0,
  distance_to_road_km: 0.7,
};

const PRESET_HUMID: WildfireFeatures = {
  temp_2m_celsius: 18.0,
  relative_humidity_pct: 75.0,
  wind_speed_10m_ms: 3.5,
  precip_7d_sum_mm: 45.0,
  precip_30d_sum_mm: 110.0,
  soil_temp_celsius: 16.0,
  fwi_fire_weather_index: 4.0,
  slope_degrees: 10.0,
  elevation_m: 250.0,
  distance_to_road_km: 3.0,
};

export const WildfirePage: React.FC = () => {
  const [formData, setFormData] = useState<WildfireFeatures>(PRESET_EXTREME_FIRE);
  const [result, setResult] = useState<WildfirePredictionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (field: keyof WildfireFeatures, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: parseFloat(value) || 0,
    }));
  };

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await api.predictWildfire(formData);
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
            <div className="p-1.5 rounded-md bg-orange-950/60 border border-orange-800/40 text-orange-400">
              <Flame className="w-4 h-4" />
            </div>
            <span className="text-xs font-mono uppercase text-orange-400 font-semibold tracking-wider">
              Ecological / Thermal Hazard Intelligence
            </span>
          </div>
          <h1 className="text-2xl font-bold font-mono text-white">
            Wildfire Ignition Susceptibility & Fire Weather Index
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Evaluates forest and shrubland ignition susceptibility using surface relative humidity, Canadian FWI index, 10m wind velocity, and prolonged fuel moisture deficit.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <StatusIndicator status="OPERATIONAL" />
          <span className="text-xs font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded border border-slate-800">
            PR-AUC: <strong className="text-orange-300">0.8272</strong>
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Form Inputs (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/40">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
              <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-300">
                Fire Weather & Canopy Covariates
              </h2>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setFormData(PRESET_EXTREME_FIRE)}
                  className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-1 rounded bg-orange-950/50 hover:bg-orange-900/60 text-orange-300 border border-orange-800/40"
                >
                  <Sparkles className="w-3 h-3" />
                  <span>Diablo Wind Red Flag Preset</span>
                </button>
                <button
                  type="button"
                  onClick={() => setFormData(PRESET_HUMID)}
                  className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700"
                >
                  <RotateCcw className="w-3 h-3" />
                  <span>Humid Low Risk</span>
                </button>
              </div>
            </div>

            <form onSubmit={handlePredict} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
                <div>
                  <label className="text-slate-400 block mb-1">2m Air Temperature (°C)</label>
                  <input
                    type="number"
                    step="0.5"
                    min="-60"
                    max="60"
                    value={formData.temp_2m_celsius}
                    onChange={(e) => handleChange('temp_2m_celsius', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Surface Relative Humidity (%)</label>
                  <input
                    type="number"
                    step="0.5"
                    min="0"
                    max="100"
                    value={formData.relative_humidity_pct}
                    onChange={(e) => handleChange('relative_humidity_pct', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">10m Surface Wind Speed (m/s)</label>
                  <input
                    type="number"
                    step="0.5"
                    min="0"
                    max="60"
                    value={formData.wind_speed_10m_ms}
                    onChange={(e) => handleChange('wind_speed_10m_ms', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Fire Weather Index (FWI)</label>
                  <input
                    type="number"
                    step="0.5"
                    min="0"
                    value={formData.fwi_fire_weather_index}
                    onChange={(e) => handleChange('fwi_fire_weather_index', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">7-Day Cumulative Rainfall (mm)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.precip_7d_sum_mm}
                    onChange={(e) => handleChange('precip_7d_sum_mm', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">30-Day Cumulative Rainfall (mm)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.precip_30d_sum_mm}
                    onChange={(e) => handleChange('precip_30d_sum_mm', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Topsoil Temperature (°C)</label>
                  <input
                    type="number"
                    step="0.5"
                    min="-50"
                    max="60"
                    value={formData.soil_temp_celsius}
                    onChange={(e) => handleChange('soil_temp_celsius', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Terrain Slope Angle (°)</label>
                  <input
                    type="number"
                    step="0.5"
                    min="0"
                    max="90"
                    value={formData.slope_degrees}
                    onChange={(e) => handleChange('slope_degrees', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Elevation (m a.s.l.)</label>
                  <input
                    type="number"
                    step="1"
                    value={formData.elevation_m}
                    onChange={(e) => handleChange('elevation_m', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Distance to Road Access (km)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.distance_to_road_km}
                    onChange={(e) => handleChange('distance_to_road_km', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full mt-2 inline-flex items-center justify-center gap-2 py-2.5 rounded-lg text-xs font-mono font-bold uppercase tracking-wider bg-orange-600 hover:bg-orange-500 disabled:opacity-50 text-white shadow-lg shadow-orange-600/20 transition-all"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Execute Wildfire Ignition Inference</span>
              </button>
            </form>
          </div>
        </div>

        {/* Prediction Results & TreeSHAP (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          {loading && <LoadingState message="Modeling Fire Weather Equilibrium..." subMessage="Evaluating dead fuel moisture deficit & flame propagation..." />}

          {error && <ErrorState message={error} onRetry={() => setError(null)} />}

          {result && !loading && (
            <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/40 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-300">
                  Wildfire Risk Output
                </span>
                <AlertBadge level={result.alert_level} size="md" />
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs font-mono">
                <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                  <span className="text-slate-400 block text-[10px] uppercase">
                    Raw Susceptibility
                  </span>
                  <span className="text-xl font-bold text-white">
                    {(result.raw_model_score * 100).toFixed(1)}%
                  </span>
                  <span className="text-[10px] text-slate-400 block mt-0.5">
                    1:1 Thermal Anomaly Sample
                  </span>
                </div>

                <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                  <span className="text-slate-400 block text-[10px] uppercase">
                    Calibrated Occurrence Odds
                  </span>
                  <span className="text-xl font-bold text-orange-400">
                    {(result.calibrated_susceptibility_score * 100).toFixed(2)}%
                  </span>
                  <span className="text-[10px] text-slate-400 block mt-0.5">
                    Climatological Prior: 0.2%
                  </span>
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 space-y-2 text-xs font-mono">
                <div className="flex justify-between">
                  <span className="text-slate-400">Est. Fire Radiative Power:</span>
                  <span className="text-amber-300 font-semibold">
                    {result.estimated_log_frp_mw !== null ? `${result.estimated_log_frp_mw} log10(MW)` : 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Ignition Vulnerability:</span>
                  <span className={result.wildfire_susceptibility_predicted ? 'text-rose-400 font-semibold' : 'text-emerald-400 font-semibold'}>
                    {result.wildfire_susceptibility_predicted ? 'HIGH IGNITION SUSCEPTIBILITY' : 'LOW IGNITION POTENTIAL'}
                  </span>
                </div>
              </div>

              {/* Blocked model notification */}
              <div className="p-3 rounded-lg bg-rose-950/20 border border-rose-900/40 text-xs font-mono">
                <div className="flex items-center gap-1.5 text-rose-400 font-semibold mb-1">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>FIRE DURATION REGRESSION BLOCKED</span>
                </div>
                <p className="text-[11px] text-rose-300/80 leading-normal">
                  Fire duration prediction ($R^2 = -214.75$) has been blocked from operational inference due to zero test variance and lack of statistical generalization.
                </p>
              </div>

              <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 text-xs font-mono">
                <span className="text-slate-400 block text-[10px] uppercase mb-0.5">Fire Management Guidance:</span>
                <p className="text-slate-300 font-sans text-xs leading-relaxed">
                  {result.action_guidance}
                </p>
              </div>

              {/* TreeSHAP Local Attributions */}
              <ShapTable attributions={result.important_contributing_features} />

              <div className="text-[11px] font-mono text-slate-400 space-y-1 bg-slate-950/40 p-3 rounded-lg border border-slate-800">
                <span className="text-slate-300 font-semibold block mb-1">Scientific Boundaries:</span>
                {result.limitations_and_warnings.map((w, idx) => (
                  <div key={idx} className="flex items-start gap-1.5">
                    <span className="text-orange-400">&bull;</span>
                    <span>{w}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {!result && !loading && (
            <div className="p-8 rounded-xl border border-dashed border-slate-800 text-center text-slate-500 font-mono text-xs">
              <Flame className="w-8 h-8 mx-auto text-slate-600 mb-2" />
              Enter prevailing relative humidity, wind speed, and cumulative rainfall to compute fine fuel ignition risk.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

