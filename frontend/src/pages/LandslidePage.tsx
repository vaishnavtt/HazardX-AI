import React, { useState } from 'react';
import { api, formatApiError } from '../api/client';
import type { LandslideFeatures, LandslidePredictionResponse } from '../types/hazard';
import { AlertBadge } from '../components/common/AlertBadge';
import { StatusIndicator } from '../components/common/StatusIndicator';
import { ShapTable } from '../components/common/ShapTable';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { Mountain, Send, Sparkles, RotateCcw } from 'lucide-react';

const PRESET_HIGH_SLOPE: LandslideFeatures = {
  precip_1d_mm: 95.0,
  precip_3d_sum_mm: 165.0,
  precip_7d_sum_mm: 245.0,
  precip_30d_sum_mm: 430.0,
  api_30d_index: 68.0,
  temp_2m_celsius: 18.0,
  soil_temp_celsius: 16.5,
  slope_degrees: 36.5,
  elevation_m: 1250.0,
  aspect_degrees: 140.0,
  plan_curvature: -0.045,
  soil_clay_fraction_pct: 38.0,
  distance_to_road_km: 0.12,
  distance_to_stream_km: 0.22,
};

const PRESET_STABLE: LandslideFeatures = {
  precip_1d_mm: 5.0,
  precip_3d_sum_mm: 12.0,
  precip_7d_sum_mm: 22.0,
  precip_30d_sum_mm: 45.0,
  api_30d_index: 10.0,
  temp_2m_celsius: 20.0,
  soil_temp_celsius: 19.0,
  slope_degrees: 6.5,
  elevation_m: 180.0,
  aspect_degrees: 90.0,
  plan_curvature: 0.01,
  soil_clay_fraction_pct: 18.0,
  distance_to_road_km: 2.5,
  distance_to_stream_km: 1.8,
};

export const LandslidePage: React.FC = () => {
  const [formData, setFormData] = useState<LandslideFeatures>(PRESET_HIGH_SLOPE);
  const [result, setResult] = useState<LandslidePredictionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (field: keyof LandslideFeatures, value: string) => {
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
      const res = await api.predictLandslide(formData);
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
            <div className="p-1.5 rounded-md bg-amber-950/60 border border-amber-800/40 text-amber-400">
              <Mountain className="w-4 h-4" />
            </div>
            <span className="text-xs font-mono uppercase text-amber-400 font-semibold tracking-wider">
              Geomorphological Hazard Intelligence
            </span>
          </div>
          <h1 className="text-2xl font-bold font-mono text-white">
            Landslide Susceptibility & Magnitude Assessment
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Evaluates rainfall-triggered slope failure probability and mass movement magnitude using high-resolution DEM slope, clay fraction, and 30-day antecedent precipitation.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <StatusIndicator status="OPERATIONAL" />
          <span className="text-xs font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded border border-slate-800">
            PR-AUC: <strong className="text-cyan-300">0.8407</strong>
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Form Inputs (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/40">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
              <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-300">
                Topographic & Hydrological Covariates
              </h2>
              {/* Presets */}
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setFormData(PRESET_HIGH_SLOPE)}
                  className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-1 rounded bg-amber-950/50 hover:bg-amber-900/60 text-amber-300 border border-amber-800/40"
                >
                  <Sparkles className="w-3 h-3" />
                  <span>Steep Slope Preset</span>
                </button>
                <button
                  type="button"
                  onClick={() => setFormData(PRESET_STABLE)}
                  className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700"
                >
                  <RotateCcw className="w-3 h-3" />
                  <span>Lowland Stable Preset</span>
                </button>
              </div>
            </div>

            <form onSubmit={handlePredict} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
                <div>
                  <label className="text-slate-400 block mb-1">Terrain Slope Angle (°)</label>
                  <input
                    type="number"
                    step="0.1"
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
                  <label className="text-slate-400 block mb-1">30-Day Antecedent Precip (mm)</label>
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
                  <label className="text-slate-400 block mb-1">30-Day Antecedent Precip Index</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.api_30d_index}
                    onChange={(e) => handleChange('api_30d_index', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">1-Day Pulse Rainfall (mm)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.precip_1d_mm}
                    onChange={(e) => handleChange('precip_1d_mm', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">3-Day Pulse Rainfall (mm)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.precip_3d_sum_mm}
                    onChange={(e) => handleChange('precip_3d_sum_mm', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Soil Clay Fraction (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                    value={formData.soil_clay_fraction_pct}
                    onChange={(e) => handleChange('soil_clay_fraction_pct', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Topographic Plan Curvature</label>
                  <input
                    type="number"
                    step="0.005"
                    min="-5"
                    max="5"
                    value={formData.plan_curvature}
                    onChange={(e) => handleChange('plan_curvature', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Distance to Road Cut (km)</label>
                  <input
                    type="number"
                    step="0.05"
                    min="0"
                    value={formData.distance_to_road_km}
                    onChange={(e) => handleChange('distance_to_road_km', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Distance to Valley Stream (km)</label>
                  <input
                    type="number"
                    step="0.05"
                    min="0"
                    value={formData.distance_to_stream_km}
                    onChange={(e) => handleChange('distance_to_stream_km', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full mt-2 inline-flex items-center justify-center gap-2 py-2.5 rounded-lg text-xs font-mono font-bold uppercase tracking-wider bg-amber-600 hover:bg-amber-500 disabled:opacity-50 text-white shadow-lg shadow-amber-600/20 transition-all"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Execute Landslide Failure Assessment</span>
              </button>
            </form>
          </div>
        </div>

        {/* Prediction Results & TreeSHAP (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          {loading && <LoadingState message="Analyzing Slope Stability..." subMessage="Computing pore-water accumulation & hillslope shear stresses..." />}

          {error && <ErrorState message={error} onRetry={() => setError(null)} />}

          {result && !loading && (
            <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/40 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-300">
                  Landslide Risk Output
                </span>
                <AlertBadge level={result.alert_level} size="md" />
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs font-mono">
                <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                  <span className="text-slate-400 block text-[10px] uppercase">
                    Susceptibility Score
                  </span>
                  <span className="text-xl font-bold text-white">
                    {(result.raw_model_score * 100).toFixed(1)}%
                  </span>
                  <span className="text-[10px] text-slate-400 block mt-0.5">
                    1:1 Case-Control Sample
                  </span>
                </div>

                <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                  <span className="text-slate-400 block text-[10px] uppercase">
                    Calibrated Occurrence Odds
                  </span>
                  <span className="text-xl font-bold text-amber-400">
                    {(result.calibrated_susceptibility_score * 100).toFixed(2)}%
                  </span>
                  <span className="text-[10px] text-slate-400 block mt-0.5">
                    Prior Frequency: 0.2%
                  </span>
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 space-y-2 text-xs font-mono">
                <div className="flex justify-between">
                  <span className="text-slate-400">Magnitude Forecast:</span>
                  <span className="text-amber-300 font-semibold">{result.hazard_magnitude_label}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Failure Predicted:</span>
                  <span className={result.landslide_occurrence_predicted ? 'text-rose-400 font-semibold' : 'text-emerald-400 font-semibold'}>
                    {result.landslide_occurrence_predicted ? 'SLOPE INSTABILITY DETECTED' : 'STABLE HILLSLOPE'}
                  </span>
                </div>
                <div className="pt-2 border-t border-slate-800/80">
                  <span className="text-slate-400 block text-[10px] uppercase mb-0.5">Action Guidance:</span>
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
                    <span className="text-amber-400">&bull;</span>
                    <span>{w}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {!result && !loading && (
            <div className="p-8 rounded-xl border border-dashed border-slate-800 text-center text-slate-500 font-mono text-xs">
              <Mountain className="w-8 h-8 mx-auto text-slate-600 mb-2" />
              Configure terrain and antecedent precipitation features to evaluate hillslope failure vulnerability.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

