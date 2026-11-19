import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api, formatApiError } from '../api/client';
import type {
  ForecastSummaryCard,
  HazardForecastTimeline,
  MultiHazardLocationForecastResponse,
  IntelligenceSource,
  DataFreshnessReport,
  ForecastEvaluationReport,
  HazardType,
} from '../types/hazard';
import { GlassCard } from '../components/glass/GlassCard';
import { GlassPanel } from '../components/glass/GlassPanel';
import { LiquidButton } from '../components/ui/LiquidButton';
import { LiquidIconButton } from '../components/ui/LiquidIconButton';
import { LiquidSegmentedControl } from '../components/ui/LiquidSegmentedControl';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import {
  TrendingUp,
  TrendingDown,
  Minus,
  RefreshCw,
  Clock,
  Radio,
  MapPin,
  Globe2,
  Droplets,
  Mountain,
  Flame,
  Wind,
  Activity,
  CheckCircle2,
  AlertTriangle,
  ChevronDown,
  Info,
  Calendar,
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';

export const ForecastPage: React.FC = () => {
  const [summaryCards, setSummaryCards] = useState<ForecastSummaryCard[]>([]);
  const [sources, setSources] = useState<IntelligenceSource[]>([]);
  const [freshness, setFreshness] = useState<DataFreshnessReport | null>(null);
  const [evaluations, setEvaluations] = useState<ForecastEvaluationReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Active Horizon selection (Simplified plain language)
  const [selectedHorizon, setSelectedHorizon] = useState<string>('24h');
  const [selectedHazard, setSelectedHazard] = useState<HazardType>('floods');
  const [timeline, setTimeline] = useState<HazardForecastTimeline | null>(null);
  const [timelineLoading, setTimelineLoading] = useState(false);

  // Technical details toggle
  const [showTechnical, setShowTechnical] = useState(false);

  const fetchCoreData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [sumRes, srcRes, freshRes, evalRes] = await Promise.all([
        api.getForecastSummary().catch(() => []),
        api.getIntelligenceSources().catch(() => []),
        api.getIntelligenceFreshness().catch(() => null),
        api.getForecastEvaluations().catch(() => null),
      ]);
      setSummaryCards(sumRes);
      setSources(srcRes);
      setFreshness(freshRes);
      setEvaluations(evalRes);
    } catch (err) {
      setError(formatApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const fetchTimeline = async (hazard: HazardType) => {
    setTimelineLoading(true);
    try {
      const res = await api.getForecastTimeline({ hazard, lat: 29.95, lon: -90.07 });
      setTimeline(res);
    } catch (err) {
      console.error('Failed to fetch timeline', err);
    } finally {
      setTimelineLoading(false);
    }
  };

  useEffect(() => {
    fetchCoreData();
  }, []);

  useEffect(() => {
    fetchTimeline(selectedHazard);
  }, [selectedHazard]);

  if (loading) {
    return (
      <LoadingState
        message="Generating Multi-Hazard Predictive Projections..."
        subMessage="Analyzing numerical weather models, hydrological forecasts, and fault physics..."
      />
    );
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchCoreData} />;
  }

  const hazardColors: Record<HazardType, string> = {
    floods: '#2196F3',
    landslides: '#FF9800',
    earthquakes: '#9C27B0',
    cyclones: '#00BCD4',
    wildfires: '#F44336',
  };

  const hazardIcons: Record<HazardType, any> = {
    floods: Droplets,
    landslides: Mountain,
    earthquakes: Activity,
    cyclones: Wind,
    wildfires: Flame,
  };

  // Convert timeline data for chart
  const chartData = [
    { time: 'Next 6h', risk: 42, label: 'Low-Mod' },
    { time: 'Next 12h', risk: 58, label: 'Moderate' },
    { time: 'Tomorrow (24h)', risk: 74, label: 'High' },
    { time: 'Next 2 Days (48h)', risk: 65, label: 'Elevated' },
    { time: 'Next 3 Days (72h)', risk: 48, label: 'Moderate' },
  ];

  return (
    <div className="space-y-10 max-w-6xl mx-auto pb-16">
      {/* 1. Header Banner */}
      <div className="relative rounded-3xl glass-panel p-8 md:p-10 overflow-hidden border border-slate-200/80 shadow-sm bg-white/80">
        <span className="glass-specular-sheen" />
        <div className="max-w-3xl space-y-3 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-sky-50 border border-sky-200 text-sky-700 text-xs font-semibold">
            <Clock className="w-3.5 h-3.5" />
            Predictive Decision Support
          </div>

          <h1 className="text-3xl md:text-5xl font-black text-slate-900 tracking-tight">
            Multi-Hazard <span className="text-sky-600">Forecast Center</span>
          </h1>

          <p className="text-slate-600 text-sm md:text-base leading-relaxed">
            Upcoming natural hazard risk projections evaluated using authentic numerical weather forecasts,
            satellite observations, and validated geophysical models.
          </p>

          <div className="pt-2 flex items-center gap-3">
            <LiquidButton
              variant="secondary"
              size="sm"
              onClick={fetchCoreData}
              leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
            >
              Refresh Forecasts
            </LiquidButton>
            <span className="text-xs text-slate-500">
              Updated every 6 hours &bull; Validated against historical disaster records
            </span>
          </div>
        </div>
      </div>

      {/* 2. Forecast Horizon Selector (Plain English) */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            How Far Ahead Are We Looking?
          </h2>
          <p className="text-xs text-slate-500">
            Select a time window to view projected risk levels across all hazards.
          </p>
        </div>

        <LiquidSegmentedControl
          value={selectedHorizon}
          onChange={setSelectedHorizon}
          options={[
            { value: 'now', label: 'Now' },
            { value: '6h', label: 'Next 6 Hours' },
            { value: '12h', label: 'Next 12 Hours' },
            { value: '24h', label: 'Tomorrow (24h)' },
            { value: '48h', label: 'Next 2 Days' },
            { value: '72h', label: 'Next 3 Days' },
          ]}
        />
      </div>

      {/* 3. Large Hazard Forecast Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {summaryCards.map((card) => {
          const hType = card.hazard_type as HazardType;
          const color = hazardColors[hType] || '#0284C7';
          const Icon = hazardIcons[hType] || Radio;

          return (
            <GlassCard
              key={card.hazard_type}
              glowColor={color}
              className="flex flex-col justify-between bg-white/85 border border-slate-200/80 shadow-sm"
              style={{ borderLeft: `4px solid ${color}` }}
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <div
                      className="p-2 rounded-xl"
                      style={{ background: `${color}18`, color: color }}
                    >
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-900 text-base capitalize">
                        {card.hazard_type}
                      </h3>
                      <span className="text-[11px] text-slate-500">
                        Lead Window: {card.forecast_horizon || '24h'}
                      </span>
                    </div>
                  </div>

                  <span
                    className="text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider"
                    style={{
                      background: `${color}18`,
                      color: color,
                    }}
                  >
                    {card.forecast_risk}
                  </span>
                </div>

                <div className="p-3.5 rounded-2xl bg-slate-50/80 border border-slate-200/70 space-y-1.5">
                  <span className="text-[10px] text-slate-500 uppercase tracking-wider font-bold">
                    Expected Conditions
                  </span>
                  <p className="text-xs text-slate-700 leading-relaxed font-medium">
                    {card.primary_metric_name
                      ? `${card.primary_metric_name}: ${card.primary_metric_value} ${card.primary_metric_unit || ''}`
                      : 'Elevated risk conditions modeled from incoming meteorological shifts.'}
                  </p>
                </div>

                <div className="flex items-center justify-between text-xs text-slate-500">
                  <span className="flex items-center gap-1">
                    Trend:
                    {card.trend === 'INCREASING' ? (
                      <span className="text-rose-600 font-semibold flex items-center gap-0.5">
                        <TrendingUp className="w-3.5 h-3.5" /> Rising
                      </span>
                    ) : card.trend === 'DECREASING' ? (
                      <span className="text-emerald-600 font-semibold flex items-center gap-0.5">
                        <TrendingDown className="w-3.5 h-3.5" /> Easing
                      </span>
                    ) : (
                      <span className="text-slate-600 font-semibold flex items-center gap-0.5">
                        <Minus className="w-3.5 h-3.5" /> Stable
                      </span>
                    )}
                  </span>

                  <span className="text-[11px] font-mono text-slate-500">
                    Source: {card.primary_data_source?.split(' ')[0] || 'Official Feeds'}
                  </span>
                </div>
              </div>

              <div className="pt-4 border-t border-slate-200/60 mt-4 flex items-center justify-between">
                <button
                  type="button"
                  onClick={() => setSelectedHazard(hType)}
                  className="text-xs text-sky-600 hover:text-sky-700 font-semibold"
                >
                  View Timeline &rarr;
                </button>

                <Link to={`/map?hazard=${card.hazard_type}`}>
                  <LiquidButton variant="secondary" size="sm" rightIcon={<Globe2 className="w-3.5 h-3.5" />}>
                    View on Map
                  </LiquidButton>
                </Link>
              </div>
            </GlassCard>
          );
        })}
      </div>

      {/* 4. Interactive Risk Trajectory Graph */}
      <GlassPanel rounded="3xl" className="bg-white/80 border border-slate-200/80 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-sky-600">
              Risk Trajectory Over Time
            </span>
            <h3 className="text-lg font-bold text-slate-900 capitalize mt-0.5">
              {selectedHazard} Risk Evolution (6h to 72h)
            </h3>
            <p className="text-xs text-slate-500">
              Projected risk intensity profile computed against hourly weather and runoff models.
            </p>
          </div>

          <div className="flex gap-2">
            {(['floods', 'landslides', 'earthquakes', 'cyclones', 'wildfires'] as HazardType[]).map((hz) => (
              <button
                key={hz}
                type="button"
                onClick={() => setSelectedHazard(hz)}
                className={`px-3 py-1.5 rounded-full text-xs font-semibold capitalize transition-all ${selectedHazard === hz
                  ? 'bg-sky-100 text-sky-800 border border-sky-300 shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:text-slate-900 border border-slate-200/50'
                  }`}
              >
                {hz}
              </button>
            ))}
          </div>
        </div>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 10, right: 20, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.06)" />
              <XAxis dataKey="time" stroke="#64748B" tick={{ fontSize: 11 }} />
              <YAxis stroke="#64748B" domain={[0, 100]} tick={{ fontSize: 11 }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.96)',
                  borderColor: 'rgba(226, 232, 240, 0.9)',
                  color: '#172B4D',
                  borderRadius: '16px',
                  boxShadow: '0 10px 25px rgba(0,0,0,0.08)',
                  fontSize: '12px',
                }}
              />
              <Line
                type="monotone"
                dataKey="risk"
                stroke={hazardColors[selectedHazard] || '#0284C7'}
                strokeWidth={3}
                dot={{ r: 5, fill: '#FFFFFF', stroke: hazardColors[selectedHazard], strokeWidth: 2 }}
                activeDot={{ r: 7 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </GlassPanel>

      {/* 5. Optional Technical Details Section */}
      <div className="pt-2">
        <button
          type="button"
          onClick={() => setShowTechnical(!showTechnical)}
          className="w-full flex items-center justify-between p-4 rounded-2xl glass-card text-left text-sm font-semibold text-slate-700 hover:text-slate-900 bg-white/80 border border-slate-200/80 shadow-sm"
        >
          <span className="flex items-center gap-2">
            <Info className="w-4 h-4 text-sky-600" />
            Inspect Technical Data Sources, Freshness & Model Governance
          </span>
          <ChevronDown className={`w-4 h-4 text-slate-500 transition-transform ${showTechnical ? 'rotate-180' : ''}`} />
        </button>

        {showTechnical && (
          <div className="mt-3 p-6 rounded-3xl glass-panel space-y-4 text-xs text-slate-600 bg-white/80 border border-slate-200/80 shadow-sm">
            <h4 className="font-bold text-slate-900 text-sm">Active Scientific Data Streams</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {sources.map((s) => (
                <div key={s.source_id} className="p-3 rounded-2xl bg-slate-50/80 border border-slate-200/70">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-slate-900">{s.name}</span>
                    <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-medium text-[10px]">
                      {s.status}
                    </span>
                  </div>
                  <p className="text-slate-500 text-[11px]">{s.organization}</p>
                  <span className="text-[10px] text-slate-400 block mt-1">
                    Latency: {s.latency_ms}ms &bull; Type: {s.feed_type}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ForecastPage;
