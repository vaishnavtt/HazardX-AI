import React, { useState } from 'react';
import { api, formatApiError } from '../api/client';
import type {
  MultiHazardPredictionRequest,
  MultiHazardPredictionResponse,
  HazardType,
} from '../types/hazard';
import { AlertBadge } from '../components/common/AlertBadge';
import { ShapTable } from '../components/common/ShapTable';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import {
  Layers,
  Send,
  Droplets,
  Mountain,
  Activity,
  Wind,
  Flame,
  CheckSquare,
  Square,
  ShieldAlert,
  Sparkles,
} from 'lucide-react';

const COMPOUND_PRESETS: Record<string, { label: string; desc: string; data: MultiHazardPredictionRequest }> = {
  cascade_coastal: {
    label: 'Coastal Typhoon & Basin Inundation Cascade',
    desc: 'Simulates a major Category 3/4 tropical cyclone making landfall, generating torrential 1-day rainfall, river surge, and hillslope failures.',
    data: {
      cyclone: {
        current_wind_kt: 110.0,
        current_pres_hpa: 948.0,
        dist_to_land_km: 25.0,
        landfall_flag: 0,
        past_delta_wind_6h: 20.0,
        past_delta_wind_12h: 35.0,
        past_delta_pres_6h: -18.0,
        translational_speed_kt: 16.0,
        heading_degrees: 300.0,
        coriolis_param: 0.000055,
        pot_intensity_headroom: 35.0,
      },
      flood: {
        precip_1d_mm: 120.0,
        precip_3d_sum_mm: 190.0,
        precip_7d_sum_mm: 260.0,
        precip_14d_sum_mm: 310.0,
        api_14d_index: 52.0,
        temp_2m_celsius: 26.0,
        soil_temp_celsius: 24.0,
        river_discharge_m3s: 650.0,
        river_discharge_7d_mean_m3s: 480.0,
        river_discharge_ratio_7d: 1.35,
        elevation_m: 25.0,
        slope_degrees: 3.5,
        topographic_wetness_index: 13.5,
        distance_to_river_km: 0.2,
      },
      landslide: {
        precip_1d_mm: 120.0,
        precip_3d_sum_mm: 190.0,
        precip_7d_sum_mm: 260.0,
        precip_30d_sum_mm: 480.0,
        api_30d_index: 75.0,
        temp_2m_celsius: 22.0,
        soil_temp_celsius: 20.0,
        slope_degrees: 38.0,
        elevation_m: 850.0,
        aspect_degrees: 155.0,
        plan_curvature: -0.05,
        soil_clay_fraction_pct: 42.0,
        distance_to_road_km: 0.08,
        distance_to_stream_km: 0.15,
      },
    },
  },
  seismic_aftershock: {
    label: 'Major Mw 7.2 Crustal Rupture',
    desc: 'Simulates a shallow Mw 7.2 strike-slip earthquake triggering regional aftershocks across active fault lines.',
    data: {
      earthquake: {
        mainshock_mag: 7.2,
        focal_depth_km: 12.0,
        dist_to_active_fault_km: 1.0,
        nearest_fault_slip_type: 'Strike-Slip',
        prior_count_7d_100km: 28,
        prior_count_30d_100km: 65,
        prior_count_365d_100km: 260,
        prior_max_mag_30d: 5.8,
        cumulative_energy_log_joules: 15.4,
        seismic_rate_accel_ratio: 3.1,
        regional_b_value: 0.85,
      },
    },
  },
  wildfire_redflag: {
    label: 'Continental Drought Firestorm',
    desc: 'Simulates desiccating Diablo winds combined with low relative humidity and high Fire Weather Index.',
    data: {
      wildfire: {
        temp_2m_celsius: 40.0,
        relative_humidity_pct: 8.0,
        wind_speed_10m_ms: 16.0,
        precip_7d_sum_mm: 0.0,
        precip_30d_sum_mm: 0.5,
        soil_temp_celsius: 43.0,
        fwi_fire_weather_index: 68.0,
        slope_degrees: 25.0,
        elevation_m: 820.0,
        distance_to_road_km: 0.5,
      },
    },
  },
};

export const MultiHazardPage: React.FC = () => {
  const [selectedPreset, setSelectedPreset] = useState<string>('cascade_coastal');
  const [requestData, setRequestData] = useState<MultiHazardPredictionRequest>(
    COMPOUND_PRESETS.cascade_coastal.data
  );
  const [result, setResult] = useState<MultiHazardPredictionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handlePresetSelect = (presetKey: string) => {
    setSelectedPreset(presetKey);
    setRequestData(COMPOUND_PRESETS[presetKey].data);
    setResult(null);
  };

  const handleExecute = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.predictAll(requestData);
      setResult(res);
    } catch (err) {
      setError(formatApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const hazardsIncluded = Object.keys(requestData) as (keyof MultiHazardPredictionRequest)[];

  return (
    <div className="space-y-6">
      {/* Module Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="p-1.5 rounded-md bg-cyan-950/60 border border-cyan-800/40 text-cyan-400">
              <Layers className="w-4 h-4" />
            </div>
            <span className="text-xs font-mono uppercase text-cyan-400 font-semibold tracking-wider">
              Integrated Multi-Hazard Assessment
            </span>
          </div>
          <h1 className="text-2xl font-bold font-mono text-white">
            Unified Multi-Hazard Intelligence & Composite Alert
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Simulate compound disaster scenarios across Floods, Landslides, Earthquakes, Cyclones, and Wildfires. Submits concurrent feature payloads to calculate composite emergency alert levels.
          </p>
        </div>

        <button
          onClick={handleExecute}
          disabled={loading}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-xs font-mono font-bold uppercase tracking-wider bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white shadow-lg shadow-cyan-600/20 transition-all"
        >
          <Send className="w-3.5 h-3.5" />
          <span>Execute Unified Assessment</span>
        </button>
      </div>

      {/* Preset Scenario Selector */}
      <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/40">
        <h2 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-300 mb-3 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-cyan-400" />
          <span>Select Multi-Hazard Disaster Scenario:</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {Object.entries(COMPOUND_PRESETS).map(([key, p]) => (
            <button
              key={key}
              onClick={() => handlePresetSelect(key)}
              className={`p-3 rounded-lg border text-left transition-all ${
                selectedPreset === key
                  ? 'bg-cyan-950/30 border-cyan-500/60 shadow-md'
                  : 'bg-slate-950/60 border-slate-800 hover:border-slate-700'
              }`}
            >
              <span className="font-mono text-xs font-bold text-white block mb-1">
                {p.label}
              </span>
              <p className="text-[11px] text-slate-400 leading-normal font-sans">
                {p.desc}
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Active Hazards Payload Overview */}
      <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/30">
        <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400 mb-2">
          Configured Hazard Payloads in Current Request:
        </h3>
        <div className="flex flex-wrap gap-2 text-xs font-mono">
          {requestData.flood && (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-sky-950/40 border border-sky-800/40 text-sky-300">
              <Droplets className="w-3.5 h-3.5" />
              <span>Floods (14 Covariates)</span>
            </span>
          )}
          {requestData.landslide && (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-amber-950/40 border border-amber-800/40 text-amber-300">
              <Mountain className="w-3.5 h-3.5" />
              <span>Landslides (14 Covariates)</span>
            </span>
          )}
          {requestData.earthquake && (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-purple-950/40 border border-purple-800/40 text-purple-300">
              <Activity className="w-3.5 h-3.5" />
              <span>Earthquakes (11 Covariates)</span>
            </span>
          )}
          {requestData.cyclone && (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-teal-950/40 border border-teal-800/40 text-teal-300">
              <Wind className="w-3.5 h-3.5" />
              <span>Cyclones (11 Covariates)</span>
            </span>
          )}
          {requestData.wildfire && (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-orange-950/40 border border-orange-800/40 text-orange-300">
              <Flame className="w-3.5 h-3.5" />
              <span>Wildfires (10 Covariates)</span>
            </span>
          )}
        </div>
      </div>

      {/* Execution Results */}
      {loading && <LoadingState message="Processing Unified Multi-Hazard Analysis..." subMessage="Evaluating concurrent risk vectors and deriving composite alert level..." />}

      {error && <ErrorState message={error} onRetry={handleExecute} />}

      {result && !loading && (
        <div className="space-y-6">
          {/* Composite Highest Alert Level Banner */}
          <div className="p-6 rounded-xl border border-slate-700 bg-slate-900/60 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <span className="text-[11px] font-mono uppercase text-slate-400 block mb-1">
                COMPOSITE EMERGENCY STATUS ACROSS EVALUATED DOMAINS
              </span>
              <div className="flex items-center gap-3">
                <h2 className="text-2xl font-bold font-mono text-white">
                  Multi-Hazard Composite Alert Level:
                </h2>
                <AlertBadge level={result.composite_highest_alert_level} size="lg" />
              </div>
              <p className="text-xs text-slate-400 mt-2 font-mono">
                Evaluated Domains: <strong className="text-cyan-300">{result.hazards_evaluated.join(', ').toUpperCase()}</strong> &bull; Timestamp: {result.timestamp}
              </p>
            </div>
          </div>

          {/* Individual Hazard Result Breakdown Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {/* Floods */}
            {result.results.flood && (
              <div className="p-5 rounded-xl border border-sky-500/30 bg-sky-950/10 space-y-3 font-mono text-xs">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span className="flex items-center gap-2 font-bold text-sky-400 text-sm">
                    <Droplets className="w-4 h-4" />
                    <span>Flood Assessment</span>
                  </span>
                  <AlertBadge level={result.results.flood.alert_level} size="sm" />
                </div>
                <div className="grid grid-cols-2 gap-2 text-slate-300">
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-400 block text-[10px]">Susceptibility</span>
                    <span className="font-bold text-white text-base">
                      {(result.results.flood.raw_model_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-400 block text-[10px]">Severity Class</span>
                    <span className="font-bold text-sky-300 text-sm">
                      {result.results.flood.severity_label}
                    </span>
                  </div>
                </div>
                <p className="text-[11px] text-slate-400 font-sans">
                  {result.results.flood.action_guidance}
                </p>
              </div>
            )}

            {/* Landslides */}
            {result.results.landslide && (
              <div className="p-5 rounded-xl border border-amber-500/30 bg-amber-950/10 space-y-3 font-mono text-xs">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span className="flex items-center gap-2 font-bold text-amber-400 text-sm">
                    <Mountain className="w-4 h-4" />
                    <span>Landslide Assessment</span>
                  </span>
                  <AlertBadge level={result.results.landslide.alert_level} size="sm" />
                </div>
                <div className="grid grid-cols-2 gap-2 text-slate-300">
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-400 block text-[10px]">Susceptibility</span>
                    <span className="font-bold text-white text-base">
                      {(result.results.landslide.raw_model_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-400 block text-[10px]">Magnitude Class</span>
                    <span className="font-bold text-amber-300 text-sm">
                      {result.results.landslide.hazard_magnitude_label}
                    </span>
                  </div>
                </div>
                <p className="text-[11px] text-slate-400 font-sans">
                  {result.results.landslide.action_guidance}
                </p>
              </div>
            )}

            {/* Earthquakes */}
            {result.results.earthquake && (
              <div className="p-5 rounded-xl border border-purple-500/30 bg-purple-950/10 space-y-3 font-mono text-xs">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span className="flex items-center gap-2 font-bold text-purple-400 text-sm">
                    <Activity className="w-4 h-4" />
                    <span>Earthquake Aftershocks</span>
                  </span>
                  <AlertBadge level={result.results.earthquake.alert_level} size="sm" />
                </div>
                <div className="grid grid-cols-2 gap-2 text-slate-300">
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-400 block text-[10px]">Hazard Prob (M&ge;5.0)</span>
                    <span className="font-bold text-white text-base">
                      {(result.results.earthquake.hazard_probability * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-400 block text-[10px]">Est. Max Aftershock</span>
                    <span className="font-bold text-purple-300 text-sm">
                      {result.results.earthquake.estimated_max_aftershock_magnitude !== null
                        ? `Mw ${result.results.earthquake.estimated_max_aftershock_magnitude}`
                        : 'N/A'}
                    </span>
                  </div>
                </div>
                <p className="text-[11px] text-slate-400 font-sans">
                  {result.results.earthquake.action_guidance}
                </p>
              </div>
            )}

            {/* Cyclones */}
            {result.results.cyclone && (
              <div className="p-5 rounded-xl border border-teal-500/30 bg-teal-950/10 space-y-3 font-mono text-xs">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span className="flex items-center gap-2 font-bold text-teal-400 text-sm">
                    <Wind className="w-4 h-4" />
                    <span>Cyclone Intensification</span>
                  </span>
                  <AlertBadge level={result.results.cyclone.alert_level} size="sm" />
                </div>
                <div className="grid grid-cols-2 gap-2 text-slate-300">
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-400 block text-[10px]">24h RI Probability</span>
                    <span className="font-bold text-white text-base">
                      {(result.results.cyclone.rapid_intensification_probability * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-400 block text-[10px]">Projected Wind (24h)</span>
                    <span className="font-bold text-teal-300 text-sm">
                      {result.results.cyclone.projected_wind_24h_kt} kt
                    </span>
                  </div>
                </div>
                <p className="text-[11px] text-slate-400 font-sans">
                  {result.results.cyclone.action_guidance}
                </p>
              </div>
            )}

            {/* Wildfires */}
            {result.results.wildfire && (
              <div className="p-5 rounded-xl border border-orange-500/30 bg-orange-950/10 space-y-3 font-mono text-xs">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span className="flex items-center gap-2 font-bold text-orange-400 text-sm">
                    <Flame className="w-4 h-4" />
                    <span>Wildfire Ignition</span>
                  </span>
                  <AlertBadge level={result.results.wildfire.alert_level} size="sm" />
                </div>
                <div className="grid grid-cols-2 gap-2 text-slate-300">
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-400 block text-[10px]">Ignition Susceptibility</span>
                    <span className="font-bold text-white text-base">
                      {(result.results.wildfire.raw_model_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-400 block text-[10px]">Est. Log FRP</span>
                    <span className="font-bold text-orange-300 text-sm">
                      {result.results.wildfire.estimated_log_frp_mw !== null
                        ? `${result.results.wildfire.estimated_log_frp_mw} MW`
                        : 'N/A'}
                    </span>
                  </div>
                </div>
                <p className="text-[11px] text-slate-400 font-sans">
                  {result.results.wildfire.action_guidance}
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

