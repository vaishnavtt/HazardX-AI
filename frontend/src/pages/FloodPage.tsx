import React, { useState } from 'react';
import { api, formatApiError } from '../api/client';
import type { FloodFeatures, FloodPredictionResponse } from '../types/hazard';
import { AlertBadge } from '../components/common/AlertBadge';
import { StatusIndicator } from '../components/common/StatusIndicator';
import { ShapTable } from '../components/common/ShapTable';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { Droplets, Send, Sparkles, RotateCcw, ShieldCheck, AlertCircle } from 'lucide-react';

const PRESET_SEVERE: FloodFeatures = {
  precip_1d_mm: 88.5,
  precip_3d_sum_mm: 145.0,
  precip_7d_sum_mm: 215.0,
  precip_14d_sum_mm: 290.0,
  api_14d_index: 45.2,
  temp_2m_celsius: 24.0,
  soil_temp_celsius: 22.5,
  river_discharge_m3s: 520.0,
  river_discharge_7d_mean_m3s: 430.0,
  river_discharge_ratio_7d: 1.21,
  elevation_m: 42.0,
  slope_degrees: 2.2,
  topographic_wetness_index: 12.1,
  distance_to_river_km: 0.35,
};

const PRESET_LOW: FloodFeatures = {
  precip_1d_mm: 2.5,
  precip_3d_sum_mm: 8.0,
  precip_7d_sum_mm: 15.0,
  precip_14d_sum_mm: 25.0,
  api_14d_index: 4.0,
  temp_2m_celsius: 21.0,
  soil_temp_celsius: 19.5,
  river_discharge_m3s: 45.0,
  river_discharge_7d_mean_m3s: 50.0,
  river_discharge_ratio_7d: 0.90,
  elevation_m: 350.0,
  slope_degrees: 14.5,
  topographic_wetness_index: 6.2,
  distance_to_river_km: 8.5,
};

export const FloodPage: React.FC = () => {
  const [formData, setFormData] = useState<FloodFeatures>(PRESET_SEVERE);
  const [result, setResult] = useState<FloodPredictionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (field: keyof FloodFeatures, value: string) => {
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
      const res = await api.predictFlood(formData);
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
            <div className="p-1.5 rounded-md bg-sky-950/60 border border-sky-800/40 text-sky-400">
              <Droplets className="w-4 h-4" />
            </div>
            <span className="text-xs font-mono uppercase text-sky-400 font-semibold tracking-wider">
              Hydrological Hazard Intelligence
            </span>
          </div>
          <h1 className="text-2xl font-bold font-mono text-white">
            Flood Inundation & Severity Prediction
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Evaluates 24-hour riverine overbank and pluvial flash flood probability using GloFAS discharge, ERA5 precipitation accumulation, and Copernicus DEM topography.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <StatusIndicator status="OPERATIONAL" />
          <span className="text-xs font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded border border-slate-800">
            PR-AUC: <strong className="text-cyan-300">0.8156</strong>
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Input Parameters Form (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/40">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
              <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-300">
                Hydrological Environmental Features
              </h2>
              {/* Presets */}
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setFormData(PRESET_SEVERE)}
                  className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-1 rounded bg-sky-950/50 hover:bg-sky-900/60 text-sky-300 border border-sky-800/40"
                >
                  <Sparkles className="w-3 h-3" />
                  <span>Severe Pulse Preset</span>
                </button>
                <button
                  type="button"
                  onClick={() => setFormData(PRESET_LOW)}
                  className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700"
                >
                  <RotateCcw className="w-3 h-3" />
                  <span>Low Risk Preset</span>
                </button>
              </div>
            </div>

            <form onSubmit={handlePredict} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
                <div>
                  <label className="text-slate-400 block mb-1">1-Day Rainfall (mm)</label>
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
                  <label className="text-slate-400 block mb-1">3-Day Cumulative Rainfall (mm)</label>
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
                  <label className="text-slate-400 block mb-1">14-Day Cumulative Rainfall (mm)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.precip_14d_sum_mm}
                    onChange={(e) => handleChange('precip_14d_sum_mm', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">14-Day Antecedent Precip Index</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.api_14d_index}
                    onChange={(e) => handleChange('api_14d_index', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">GloFAS River Discharge (m³/s)</label>
                  <input
                    type="number"
                    step="1"
                    min="0"
                    value={formData.river_discharge_m3s}
                    onChange={(e) => handleChange('river_discharge_m3s', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">River Discharge 7d Mean (m³/s)</label>
                  <input
                    type="number"
                    step="1"
                    min="0"
                    value={formData.river_discharge_7d_mean_m3s}
                    onChange={(e) => handleChange('river_discharge_7d_mean_m3s', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Discharge Ratio (Current / 7d)</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={formData.river_discharge_ratio_7d}
                    onChange={(e) => handleChange('river_discharge_ratio_7d', e.target.value)}
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
                  <label className="text-slate-400 block mb-1">Terrain Slope (degrees)</label>
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
                  <label className="text-slate-400 block mb-1">Topographic Wetness Index</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.topographic_wetness_index}
                    onChange={(e) => handleChange('topographic_wetness_index', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Distance to River Channel (km)</label>
                  <input
                    type="number"
                    step="0.05"
                    min="0"
                    value={formData.distance_to_river_km}
                    onChange={(e) => handleChange('distance_to_river_km', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full mt-2 inline-flex items-center justify-center gap-2 py-2.5 rounded-lg text-xs font-mono font-bold uppercase tracking-wider bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white shadow-lg shadow-cyan-600/20 transition-all"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Execute XGBoost Flood Inference</span>
              </button>
            </form>
          </div>
        </div>

        {/* Prediction Results & TreeSHAP (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          {loading && <LoadingState message="Evaluating Flood Inundation..." subMessage="Executing XGBoost occurrence & severity classifiers with TreeSHAP..." />}

          {error && <ErrorState message={error} onRetry={() => setError(null)} />}

          {result && !loading && (
            <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/40 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-300">
                  Inference Output
                </span>
                <AlertBadge level={result.alert_level} size="md" />
              </div>

              {/* Primary Score Cards */}
              <div className="grid grid-cols-2 gap-3 text-xs font-mono">
                <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                  <span className="text-slate-400 block text-[10px] uppercase">
                    Raw Susceptibility Score
                  </span>
                  <span className="text-xl font-bold text-white">
                    {(result.raw_model_score * 100).toFixed(1)}%
                  </span>
                  <span className="text-[10px] text-slate-400 block mt-0.5">
                    1:1 Balanced Sample Basis
                  </span>
                </div>

                <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                  <span className="text-slate-400 block text-[10px] uppercase">
                    Calibrated Daily Odds
                  </span>
                  <span className="text-xl font-bold text-cyan-400">
                    {(result.calibrated_susceptibility_score * 100).toFixed(2)}%
                  </span>
                  <span className="text-[10px] text-slate-400 block mt-0.5">
                    Climatological Prior: 0.5%
                  </span>
                </div>
              </div>

              {/* Severity & Action Guidance */}
              <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 space-y-2 text-xs font-mono">
                <div className="flex justify-between">
                  <span className="text-slate-400">Severity Tier:</span>
                  <span className="text-slate-200 font-semibold">{result.severity_label}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Occurrence Forecast:</span>
                  <span className={result.flood_occurrence_predicted ? 'text-rose-400 font-semibold' : 'text-emerald-400 font-semibold'}>
                    {result.flood_occurrence_predicted ? 'INUNDATION PREDICTED' : 'QUIESCENT / NO OVERBANK'}
                  </span>
                </div>
                <div className="pt-2 border-t border-slate-800/80">
                  <span className="text-slate-400 block text-[10px] uppercase mb-0.5">Guidance:</span>
                  <p className="text-slate-300 font-sans text-xs leading-relaxed">
                    {result.action_guidance}
                  </p>
                </div>
              </div>

              {/* TreeSHAP Local Attributions */}
              <ShapTable attributions={result.important_contributing_features} />

              {/* Scientific Warnings */}
              <div className="text-[11px] font-mono text-slate-400 space-y-1 bg-slate-950/40 p-3 rounded-lg border border-slate-800">
                <span className="text-slate-300 font-semibold block mb-1">Scientific Boundaries:</span>
                {result.limitations_and_warnings.map((w, idx) => (
                  <div key={idx} className="flex items-start gap-1.5">
                    <span className="text-cyan-400">&bull;</span>
                    <span>{w}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {!result && !loading && (
            <div className="p-8 rounded-xl border border-dashed border-slate-800 text-center text-slate-500 font-mono text-xs">
              <Droplets className="w-8 h-8 mx-auto text-slate-600 mb-2" />
              Configure hydrological parameters and click &ldquo;Execute XGBoost Flood Inference&rdquo; to assess catchment risk.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

