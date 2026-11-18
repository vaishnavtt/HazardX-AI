import React, { useState } from 'react';
import { api, formatApiError } from '../api/client';
import type { CycloneFeatures, CyclonePredictionResponse } from '../types/hazard';
import { AlertBadge } from '../components/common/AlertBadge';
import { StatusIndicator } from '../components/common/StatusIndicator';
import { ShapTable } from '../components/common/ShapTable';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { Wind, Send, Sparkles, RotateCcw, Compass } from 'lucide-react';

const PRESET_IDA_RI: CycloneFeatures = {
  current_wind_kt: 80.0,
  current_pres_hpa: 968.0,
  dist_to_land_km: 280.0,
  landfall_flag: 0,
  past_delta_wind_6h: 15.0,
  past_delta_wind_12h: 25.0,
  past_delta_pres_6h: -14.0,
  translational_speed_kt: 14.0,
  heading_degrees: 310.0,
  coriolis_param: 0.000065,
  pot_intensity_headroom: 55.0,
};

const PRESET_STEADY: CycloneFeatures = {
  current_wind_kt: 45.0,
  current_pres_hpa: 998.0,
  dist_to_land_km: 150.0,
  landfall_flag: 0,
  past_delta_wind_6h: 0.0,
  past_delta_wind_12h: 5.0,
  past_delta_pres_6h: -1.0,
  translational_speed_kt: 10.0,
  heading_degrees: 270.0,
  coriolis_param: 0.000045,
  pot_intensity_headroom: 15.0,
};

export const CyclonePage: React.FC = () => {
  const [formData, setFormData] = useState<CycloneFeatures>(PRESET_IDA_RI);
  const [result, setResult] = useState<CyclonePredictionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (field: keyof CycloneFeatures, value: string) => {
    if (field === 'landfall_flag') {
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
      const res = await api.predictCyclone(formData);
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
            <div className="p-1.5 rounded-md bg-teal-950/60 border border-teal-800/40 text-teal-400">
              <Wind className="w-4 h-4" />
            </div>
            <span className="text-xs font-mono uppercase text-teal-400 font-semibold tracking-wider">
              Meteorological Hazard Intelligence
            </span>
          </div>
          <h1 className="text-2xl font-bold font-mono text-white">
            Tropical Cyclone Rapid Intensification (RI) & Wind Change
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Evaluates 24-hour explosive intensification potential (&ge; +30 kt increase) and continuous wind velocity changes using vortex history and thermodynamic headroom.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <StatusIndicator status="OPERATIONAL" />
          <span className="text-xs font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded border border-slate-800">
            PR-AUC: <strong className="text-teal-300">0.3543</strong> (5.35x baseline)
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Form Inputs (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/40">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
              <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-300">
                Vortex Kinematics & Thermodynamic Features
              </h2>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setFormData(PRESET_IDA_RI)}
                  className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-1 rounded bg-teal-950/50 hover:bg-teal-900/60 text-teal-300 border border-teal-800/40"
                >
                  <Sparkles className="w-3 h-3" />
                  <span>Explosive RI Preset</span>
                </button>
                <button
                  type="button"
                  onClick={() => setFormData(PRESET_STEADY)}
                  className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700"
                >
                  <RotateCcw className="w-3 h-3" />
                  <span>Steady Tropical Storm</span>
                </button>
              </div>
            </div>

            <form onSubmit={handlePredict} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
                <div>
                  <label className="text-slate-400 block mb-1">Current Sustained Wind (kt)</label>
                  <input
                    type="number"
                    step="1"
                    min="10"
                    max="220"
                    value={formData.current_wind_kt}
                    onChange={(e) => handleChange('current_wind_kt', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Central Pressure (hPa)</label>
                  <input
                    type="number"
                    step="1"
                    min="850"
                    max="1030"
                    value={formData.current_pres_hpa}
                    onChange={(e) => handleChange('current_pres_hpa', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Past 6h Wind Delta (kt)</label>
                  <input
                    type="number"
                    step="1"
                    value={formData.past_delta_wind_6h}
                    onChange={(e) => handleChange('past_delta_wind_6h', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Past 12h Wind Delta (kt)</label>
                  <input
                    type="number"
                    step="1"
                    value={formData.past_delta_wind_12h}
                    onChange={(e) => handleChange('past_delta_wind_12h', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Past 6h Pressure Delta (hPa)</label>
                  <input
                    type="number"
                    step="1"
                    value={formData.past_delta_pres_6h}
                    onChange={(e) => handleChange('past_delta_pres_6h', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">MPI Thermodynamic Headroom (kt)</label>
                  <input
                    type="number"
                    step="1"
                    value={formData.pot_intensity_headroom}
                    onChange={(e) => handleChange('pot_intensity_headroom', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Distance to Land (km)</label>
                  <input
                    type="number"
                    step="1"
                    min="0"
                    value={formData.dist_to_land_km}
                    onChange={(e) => handleChange('dist_to_land_km', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Translational Speed (kt)</label>
                  <input
                    type="number"
                    step="1"
                    min="0"
                    max="80"
                    value={formData.translational_speed_kt}
                    onChange={(e) => handleChange('translational_speed_kt', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Track Heading (°)</label>
                  <input
                    type="number"
                    step="1"
                    min="0"
                    max="360"
                    value={formData.heading_degrees}
                    onChange={(e) => handleChange('heading_degrees', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>

                <div>
                  <label className="text-slate-400 block mb-1">Coriolis Parameter (s⁻¹)</label>
                  <input
                    type="number"
                    step="0.000005"
                    value={formData.coriolis_param}
                    onChange={(e) => handleChange('coriolis_param', e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-hidden focus:border-cyan-500"
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full mt-2 inline-flex items-center justify-center gap-2 py-2.5 rounded-lg text-xs font-mono font-bold uppercase tracking-wider bg-teal-600 hover:bg-teal-500 disabled:opacity-50 text-white shadow-lg shadow-teal-600/20 transition-all"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Execute Cyclone RI & Intensity Forecast</span>
              </button>
            </form>
          </div>
        </div>

        {/* Prediction Results & TreeSHAP (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          {loading && <LoadingState message="Modeling Vortex Intensification..." subMessage="Computing eyewall angular momentum & 24h intensity delta..." />}

          {error && <ErrorState message={error} onRetry={() => setError(null)} />}

          {result && !loading && (
            <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/40 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-300">
                  Cyclone Forecast Output
                </span>
                <AlertBadge level={result.alert_level} size="md" />
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs font-mono">
                <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                  <span className="text-slate-400 block text-[10px] uppercase">
                    Rapid Intensification (RI) Prob
                  </span>
                  <span className="text-xl font-bold text-teal-300">
                    {(result.rapid_intensification_probability * 100).toFixed(1)}%
                  </span>
                  <span className="text-[10px] text-slate-400 block mt-0.5">
                    Clim Base: ~5.5% (+30 kt / 24h)
                  </span>
                </div>

                <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                  <span className="text-slate-400 block text-[10px] uppercase">
                    Projected 24h Wind Speed
                  </span>
                  <span className="text-xl font-bold text-white">
                    {result.projected_wind_24h_kt} kt
                  </span>
                  <span className="text-[10px] text-teal-400 block mt-0.5">
                    Delta: {result.predicted_24h_intensity_change_kt > 0 ? `+${result.predicted_24h_intensity_change_kt}` : result.predicted_24h_intensity_change_kt} kt
                  </span>
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 space-y-2 text-xs font-mono">
                <div className="flex justify-between">
                  <span className="text-slate-400">RI Alert Tier:</span>
                  <span className="text-teal-300 font-semibold">{result.risk_category}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">RI Occurrence Flag:</span>
                  <span className={result.rapid_intensification_predicted ? 'text-rose-400 font-semibold' : 'text-emerald-400 font-semibold'}>
                    {result.rapid_intensification_predicted ? 'EXPLOSIVE RI ALERT (+30 KT)' : 'NORMAL INTENSIFICATION'}
                  </span>
                </div>
                <div className="pt-2 border-t border-slate-800/80">
                  <span className="text-slate-400 block text-[10px] uppercase mb-0.5">Meteorological Guidance:</span>
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
                    <span className="text-teal-400">&bull;</span>
                    <span>{w}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {!result && !loading && (
            <div className="p-8 rounded-xl border border-dashed border-slate-800 text-center text-slate-500 font-mono text-xs">
              <Wind className="w-8 h-8 mx-auto text-slate-600 mb-2" />
              Configure vortex central pressure, wind tendencies, and MPI headroom to forecast 24-hour intensification trajectory.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

