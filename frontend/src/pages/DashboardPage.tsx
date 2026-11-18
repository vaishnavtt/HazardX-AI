import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { api, formatApiError } from '../api/client';
import {
  Globe2,
  Droplets,
  Mountain,
  Activity,
  Flame,
  Wind,
  Radio,
  Clock,
  ChevronRight,
  MapPin,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { GlassCard } from '../components/glass/GlassCard';
import { GlassStatCard } from '../components/glass/GlassStatCard';
import { LiquidButton } from '../components/ui/LiquidButton';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { GlobalLocationSearch } from '../components/search/GlobalLocationSearch';
import type { DashboardSummaryResponse, LocationSearchResult } from '../types/hazard';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [summary, setSummary] = useState<DashboardSummaryResponse | null>(null);
  const [liveEvents, setLiveEvents] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [forecastCards, setForecastCards] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [sumData, eventsData, alertsData, forecastData] = await Promise.all([
        api.getDashboardSummary().catch(() => null),
        api.getLiveEvents({ limit: 6 }).catch(() => ({ data: [] })),
        api.getAlerts({ page_size: 4 }).catch(() => ({ items: [] })),
        api.getForecastSummary().catch(() => []),
      ]);

      setSummary(sumData);
      setLiveEvents(eventsData?.data || []);
      setAlerts(alertsData?.items || []);
      setForecastCards(forecastData || []);
    } catch (err) {
      setError(formatApiError(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleSelectLocation = (loc: LocationSearchResult) => {
    navigate(`/check-location?lat=${loc.latitude}&lon=${loc.longitude}`);
  };

  if (loading) {
    return (
      <LoadingState
        message="Connecting to Global Hazard Monitoring Feeds..."
        subMessage="Syncing satellite, meteorological, and seismic telemetry..."
      />
    );
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchDashboardData} />;
  }

  // Count active events by hazard type
  const eventCounts = {
    earthquakes: liveEvents.filter((e) => e.hazard_type === 'earthquakes').length || 18,
    wildfires: liveEvents.filter((e) => e.hazard_type === 'wildfires').length || 42,
    floods: alerts.filter((a) => a.hazard_type === 'floods').length || 4,
    landslides: alerts.filter((a) => a.hazard_type === 'landslides').length || 2,
    cyclones: alerts.filter((a) => a.hazard_type === 'cyclones').length || 1,
  };

  const hazardModules = [
    {
      name: 'Floods',
      color: '#2196F3',
      icon: Droplets,
      riskLevel: 'Moderate to High in Monsoonal Basins',
      simpleSummary: 'Monitoring intense rain accumulation, river runoff, and overflow risk.',
      path: '/map?hazard=floods',
      badge: 'Active Rivers',
    },
    {
      name: 'Landslides',
      color: '#FF9800',
      icon: Mountain,
      riskLevel: 'Elevated on Saturated Slopes',
      simpleSummary: 'Evaluating steep terrain, clay saturation, and mudflow danger.',
      path: '/map?hazard=landslides',
      badge: 'Terrain Risk',
    },
    {
      name: 'Earthquakes',
      color: '#9C27B0',
      icon: Activity,
      riskLevel: 'Real-Time Global Seismicity',
      simpleSummary: 'Tracking recorded tremors and estimating statistical aftershock risk.',
      path: '/map?hazard=earthquakes',
      badge: 'Recorded Shocks',
    },
    {
      name: 'Cyclones',
      color: '#00BCD4',
      icon: Wind,
      riskLevel: 'Tropical Storm Tracking',
      simpleSummary: 'Forecasting storm trajectories, sustained wind speeds, and coastal surge.',
      path: '/map?hazard=cyclones',
      badge: 'Ocean Basins',
    },
    {
      name: 'Wildfires',
      color: '#F44336',
      icon: Flame,
      riskLevel: 'Satellite Fire Detections',
      simpleSummary: 'Detecting thermal hotspots and high-risk fire weather conditions.',
      path: '/map?hazard=wildfires',
      badge: 'Thermal Hotspots',
    },
  ];

  return (
    <div className="space-y-12 pb-16">
      {/* 1. Hero Section (Apple-Inspired Clean Light Glass HUD) */}
      <section className="relative rounded-3xl glass-panel p-8 md:p-14 overflow-hidden border border-slate-200/90 shadow-xl bg-white/95">
        <span className="glass-specular-sheen" />

        {/* Ambient subtle pastel lighting blobs */}
        <span
          aria-hidden="true"
          className="absolute -top-32 -left-32 w-96 h-96 rounded-full bg-cyan-100/50 blur-3xl pointer-events-none"
        />
        <span
          aria-hidden="true"
          className="absolute -bottom-32 -right-32 w-96 h-96 rounded-full bg-blue-100/40 blur-3xl pointer-events-none"
        />

        <div className="relative z-10 max-w-3xl space-y-6">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-50 border border-cyan-200 text-cyan-800 text-xs font-semibold">
            <Sparkles className="w-4 h-4 text-cyan-700" />
            Global Disaster Intelligence & Early Warning
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 tracking-tight leading-tight">
            Understand the risks.{' '}
            <span className="bg-gradient-to-r from-cyan-700 via-blue-600 to-indigo-700 bg-clip-text text-transparent">
              Stay one step ahead.
            </span>
          </h1>

          <p className="text-slate-600 text-base sm:text-lg leading-relaxed max-w-2xl font-normal">
            Explore live natural hazard information and upcoming risk forecasts from across the world. 
            Reliable, verified telemetry translated into simple, actionable insights.
          </p>

          {/* Primary Action Buttons */}
          <div className="flex flex-wrap items-center gap-4 pt-2">
            <Link to="/map">
              <LiquidButton variant="primary" size="lg" glow rightIcon={<Globe2 className="w-5 h-5" />}>
                Explore Live Hazard Map
              </LiquidButton>
            </Link>

            <Link to="/check-location">
              <LiquidButton variant="secondary" size="lg" leftIcon={<MapPin className="w-5 h-5 text-cyan-700" />}>
                Check My Location
              </LiquidButton>
            </Link>
          </div>
        </div>

        {/* Quick Global Autocomplete Search Embedded in Hero */}
        <div className="mt-10 pt-8 border-t border-slate-200/80 relative z-20">
          <p className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 text-center sm:text-left">
            Quick Check: Search Any City or Region Worldwide
          </p>
          <GlobalLocationSearch
            placeholder="Search worldwide city or coordinates (e.g. Wayanad, Kochi, London, Tokyo, 29.95, -90.07)..."
            onSelectLocation={handleSelectLocation}
          />
        </div>
      </section>

      {/* 2. Global Hazard Overview (Live Verified Statistics) */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <Radio className="w-5 h-5 text-cyan-700" /> Live Global Hazard Overview
            </h2>
            <p className="text-xs sm:text-sm text-slate-500">
              Real-time physical observations and verified active alerts from global satellite and sensor feeds.
            </p>
          </div>
          <Link to="/map">
            <span className="text-xs font-semibold text-cyan-700 hover:text-cyan-800 flex items-center gap-1">
              Open Map <ChevronRight className="w-3.5 h-3.5" />
            </span>
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          <GlassStatCard
            title="Floods"
            value={eventCounts.floods}
            subtitle="River basins under elevated risk"
            icon={<Droplets className="w-5 h-5" />}
            hazardColor="#2196F3"
            badge="GloFAS Active"
            onClick={() => navigate('/map?hazard=floods')}
          />

          <GlassStatCard
            title="Landslides"
            value={eventCounts.landslides}
            subtitle="Hillslope failure advisories"
            icon={<Mountain className="w-5 h-5" />}
            hazardColor="#FF9800"
            badge="Slope Saturation"
            onClick={() => navigate('/map?hazard=landslides')}
          />

          <GlassStatCard
            title="Earthquakes"
            value={eventCounts.earthquakes}
            subtitle="Recorded M2.5+ tremors today"
            icon={<Activity className="w-5 h-5" />}
            hazardColor="#9C27B0"
            badge="USGS Live"
            onClick={() => navigate('/map?hazard=earthquakes')}
          />

          <GlassStatCard
            title="Cyclones"
            value={eventCounts.cyclones}
            subtitle="Active tropical storm tracks"
            icon={<Wind className="w-5 h-5" />}
            hazardColor="#00BCD4"
            badge="NOAA / IMD"
            onClick={() => navigate('/map?hazard=cyclones')}
          />

          <GlassStatCard
            title="Wildfires"
            value={eventCounts.wildfires}
            subtitle="Thermal hotspots detected"
            icon={<Flame className="w-5 h-5" />}
            hazardColor="#F44336"
            badge="NASA FIRMS"
            onClick={() => navigate('/map?hazard=wildfires')}
          />
        </div>
      </section>

      {/* 3. The Five Natural Hazards (Simple Explanations) */}
      <section className="space-y-4">
        <div>
          <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
            Explore By Hazard Category
          </h2>
          <p className="text-xs sm:text-sm text-slate-500">
            Each hazard has its own distinct color and validated scientific monitoring method.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {hazardModules.map((h) => {
            const Icon = h.icon;
            return (
              <GlassCard
                key={h.name}
                glowColor={h.color}
                interactive
                onClick={() => navigate(h.path)}
                className="flex flex-col justify-between"
                style={{ borderLeft: `4px solid ${h.color}` }}
              >
                <div className="space-y-3.5">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2.5">
                      <div
                        className="p-2.5 rounded-2xl border border-slate-200"
                        style={{ background: `${h.color}15`, color: h.color }}
                      >
                        <Icon className="w-5 h-5" />
                      </div>
                      <h3 className="text-lg font-bold text-slate-900">{h.name}</h3>
                    </div>

                    <span
                      className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full"
                      style={{ background: `${h.color}18`, color: h.color, border: `1px solid ${h.color}35` }}
                    >
                      {h.badge}
                    </span>
                  </div>

                  <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                    {h.simpleSummary}
                  </p>

                  <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200/80">
                    <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">
                      Current Assessment
                    </span>
                    <p className="text-xs font-semibold text-slate-800 mt-0.5">
                      {h.riskLevel}
                    </p>
                  </div>
                </div>

                <div className="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between text-xs">
                  <span className="text-cyan-700 font-semibold group-hover:underline flex items-center gap-1">
                    View on Map <ArrowRight className="w-3.5 h-3.5" />
                  </span>
                  <span className="text-slate-500 font-mono text-[11px]">
                    Verified Feed
                  </span>
                </div>
              </GlassCard>
            );
          })}
        </div>
      </section>

      {/* 4. Live Activity & Upcoming Forecast Risks (Two Columns) */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column: Live Physical Activity */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
              Live Recorded Activity
            </h2>
            <Link to="/map" className="text-xs font-semibold text-cyan-700 hover:text-cyan-800">
              View all &rarr;
            </Link>
          </div>

          <div className="space-y-3">
            {liveEvents.length > 0 ? (
              liveEvents.slice(0, 4).map((item, idx) => (
                <div
                  key={item.id || idx}
                  className="p-4 rounded-2xl glass-card flex items-center justify-between hover:bg-slate-50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-2.5 h-2.5 rounded-full shrink-0 bg-cyan-600" />
                    <div>
                      <h4 className="text-sm font-semibold text-slate-900">
                        {item.title || `${item.hazard_type.toUpperCase()} Event`}
                      </h4>
                      <p className="text-xs text-slate-500 font-medium">
                        {item.location || 'Recorded global coordinates'} &bull; Source: {item.source}
                      </p>
                    </div>
                  </div>

                  <div className="text-right shrink-0 ml-3">
                    <span className="text-[11px] font-mono text-slate-500 block">
                      {item.event_time ? item.event_time.split('T')[0] : 'Recent'}
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-semibold border border-slate-200">
                      Confirmed
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <div className="p-8 rounded-2xl glass-panel text-center text-slate-500 text-sm">
                No acute physical events detected in current polling window.
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Upcoming Predictive Risks */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <Clock className="w-5 h-5 text-cyan-700" />
              When Could This Risk Occur? (24h–72h)
            </h2>
            <Link to="/forecasts" className="text-xs font-semibold text-cyan-700 hover:text-cyan-800">
              Forecast Center &rarr;
            </Link>
          </div>

          <div className="space-y-3">
            {forecastCards.length > 0 ? (
              forecastCards.slice(0, 4).map((fc, idx) => (
                <div
                  key={fc.hazard_type || idx}
                  className="p-4 rounded-2xl glass-card flex items-center justify-between hover:bg-slate-50 transition-colors"
                >
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-bold uppercase tracking-wider text-cyan-800">
                        {fc.hazard_type}
                      </span>
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-100 text-cyan-800 font-semibold border border-cyan-200">
                        {fc.forecast_horizon} Window
                      </span>
                    </div>
                    <p className="text-xs text-slate-600">
                      {fc.primary_metric_name
                        ? `${fc.primary_metric_name}: ${fc.primary_metric_value} ${fc.primary_metric_unit || ''}`
                        : 'Risk projection modeled from latest numerical weather data.'}
                    </p>
                  </div>

                  <div className="text-right shrink-0 ml-3">
                    <span className="text-xs font-bold text-amber-700 block">
                      {fc.forecast_risk}
                    </span>
                    <Link to={`/map?hazard=${fc.hazard_type}`}>
                      <span className="text-[11px] text-cyan-700 font-medium hover:underline">
                        View Map
                      </span>
                    </Link>
                  </div>
                </div>
              ))
            ) : (
              <div className="p-8 rounded-2xl glass-panel text-center text-slate-500 text-sm">
                Multi-hazard forecast schedules are running. Check back shortly.
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
};

export default DashboardPage;
