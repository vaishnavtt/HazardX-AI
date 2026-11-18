import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { api, formatApiError } from '../api/client';
import {
  MapPin,
  Crosshair,
  ShieldAlert,
  Droplets,
  Mountain,
  Activity,
  Flame,
  Wind,
  Layers,
  Globe2,
  ChevronDown,
  Info,
  CheckCircle2,
  AlertTriangle,
  Compass
} from 'lucide-react';
import { GlassPanel } from '../components/glass/GlassPanel';
import { GlassCard } from '../components/glass/GlassCard';
import { LiquidButton } from '../components/ui/LiquidButton';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { GlobalLocationSearch } from '../components/search/GlobalLocationSearch';
import type { GeospatialAssessmentResponse, LocationSearchResult } from '../types/hazard';

interface CityPreset {
  name: string;
  country: string;
  lat: number;
  lon: number;
}

const POPULAR_CITIES: CityPreset[] = [
  { name: 'Wayanad', country: 'India', lat: 11.6854, lon: 76.1320 },
  { name: 'Kochi', country: 'India', lat: 9.9312, lon: 76.2673 },
  { name: 'London', country: 'United Kingdom', lat: 51.5074, lon: -0.1278 },
  { name: 'Tokyo', country: 'Japan', lat: 35.6762, lon: 139.6503 },
  { name: 'New York', country: 'United States', lat: 40.7128, lon: -74.0060 },
  { name: 'Miami', country: 'United States', lat: 25.7617, lon: -80.1918 },
  { name: 'San Francisco', country: 'United States', lat: 37.7749, lon: -122.4194 },
  { name: 'New Orleans', country: 'United States', lat: 29.9511, lon: -90.0715 },
];

export const LocationAssessmentPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const [lat, setLat] = useState<number>(() => {
    const pLat = searchParams.get('lat');
    return pLat ? parseFloat(pLat) : 11.6854;
  });

  const [lon, setLon] = useState<number>(() => {
    const pLon = searchParams.get('lon');
    return pLon ? parseFloat(pLon) : 76.1320;
  });

  const [locationName, setLocationName] = useState<string>('Wayanad, Kerala, India');
  const [assessment, setAssessment] = useState<GeospatialAssessmentResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [showAdvancedEnv, setShowAdvancedEnv] = useState<boolean>(false);

  const handleUseMyLocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser.');
      return;
    }

    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const uLat = parseFloat(pos.coords.latitude.toFixed(4));
        const uLon = parseFloat(pos.coords.longitude.toFixed(4));
        setLat(uLat);
        setLon(uLon);
        setLocationName('Your Current GPS Location');
        runAssessment(uLat, uLon);
      },
      (err) => {
        setLoading(false);
        setError(`Could not access device location: ${err.message}. Please select a city or search above.`);
      }
    );
  };

  const runAssessment = async (targetLat: number, targetLon: number) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.assessLocationRisk({
        latitude: targetLat,
        longitude: targetLon,
        hazards: ['floods', 'landslides', 'earthquakes', 'cyclones', 'wildfires'],
      });
      setAssessment(res);
      setSearchParams({ lat: targetLat.toString(), lon: targetLon.toString() });
    } catch (err) {
      setError(formatApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleSelectSearchResult = (loc: LocationSearchResult) => {
    setLat(loc.latitude);
    setLon(loc.longitude);
    setLocationName(loc.display_name || loc.name);
    runAssessment(loc.latitude, loc.longitude);
  };

  useEffect(() => {
    const pLat = searchParams.get('lat');
    const pLon = searchParams.get('lon');
    if (pLat && pLon) {
      const parsedLat = parseFloat(pLat);
      const parsedLon = parseFloat(pLon);
      setLat(parsedLat);
      setLon(parsedLon);
      setLocationName(`Coordinates (${parsedLat.toFixed(2)}, ${parsedLon.toFixed(2)})`);
      runAssessment(parsedLat, parsedLon);
    } else {
      runAssessment(lat, lon);
    }
  }, []);

  const hazardMeta: Record<string, { label: string; color: string; icon: any; dataSrc: string }> = {
    floods: {
      label: 'Flood Risk',
      color: '#2196F3',
      icon: Droplets,
      dataSrc: 'Copernicus GloFAS River Model & Open-Meteo',
    },
    landslides: {
      label: 'Landslide Risk',
      color: '#FF9800',
      icon: Mountain,
      dataSrc: 'Copernicus DEM Terrain & Rainfall Infiltration',
    },
    earthquakes: {
      label: 'Earthquake Aftershock Hazard',
      color: '#9C27B0',
      icon: Activity,
      dataSrc: 'USGS Seismicity Catalogs & GEM Faults (Omori Decay)',
    },
    cyclones: {
      label: 'Tropical Cyclone Hazard',
      color: '#00BCD4',
      icon: Wind,
      dataSrc: 'NOAA National Hurricane Center & IMD RSMC',
    },
    wildfires: {
      label: 'Wildfire Hazard',
      color: '#F44336',
      icon: Flame,
      dataSrc: 'NASA FIRMS VIIRS Satellites & Weather Fire Index',
    },
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-16">
      {/* 1. Header Banner & Global Autocomplete Search */}
      <div className="relative rounded-3xl glass-panel p-8 md:p-10 border border-slate-200/90 shadow-xl overflow-hidden bg-white/90">
        <span className="glass-specular-sheen" />

        <div className="max-w-3xl space-y-3 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-50 border border-cyan-200 text-cyan-800 text-xs font-semibold">
            <MapPin className="w-3.5 h-3.5 text-cyan-700" />
            Global Location Intelligence
          </div>

          <h1 className="text-3xl md:text-4xl font-black text-slate-900 tracking-tight">
            Check Hazard Risks <span className="text-cyan-700">Near You</span>
          </h1>

          <p className="text-slate-600 text-sm md:text-base leading-relaxed">
            Search any city, town, or global GPS coordinate to inspect live and forecast natural hazard
            threats across all five monitored disaster domains.
          </p>
        </div>

        {/* Global Autocomplete Search Bar & GPS Trigger */}
        <div className="mt-8 pt-6 border-t border-slate-200/80 relative z-20 flex flex-col sm:flex-row gap-3">
          <div className="flex-1">
            <GlobalLocationSearch
              placeholder="Search worldwide city, town, or coordinates (e.g. Wayanad, Kochi, London, Tokyo, 29.95, -90.07)..."
              onSelectLocation={handleSelectSearchResult}
            />
          </div>

          <div className="shrink-0 flex items-center">
            <LiquidButton
              type="button"
              variant="secondary"
              onClick={handleUseMyLocation}
              leftIcon={<Crosshair className="w-4 h-4 text-cyan-700" />}
            >
              Use My GPS
            </LiquidButton>
          </div>
        </div>

        {/* Quick Popular City Pills */}
        <div className="mt-4 flex flex-wrap items-center gap-2 text-xs text-slate-500 relative z-10">
          <span className="font-semibold text-slate-700">Quick Places:</span>
          {POPULAR_CITIES.map((city) => (
            <button
              key={city.name}
              type="button"
              onClick={() => {
                setLat(city.lat);
                setLon(city.lon);
                setLocationName(`${city.name}, ${city.country}`);
                runAssessment(city.lat, city.lon);
              }}
              className="px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-slate-700 hover:border-cyan-500 hover:text-cyan-800 hover:bg-cyan-50/50 transition-all font-medium"
            >
              {city.name}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <ErrorState message={error} onRetry={() => runAssessment(lat, lon)} />
      )}

      {loading && (
        <LoadingState
          message={`Evaluating Multi-Hazard Telemetry for ${locationName}...`}
          subMessage="Synthesizing Copernicus DEM terrain, Open-Meteo weather, and USGS fault catalogs..."
        />
      )}

      {/* Assessment Results */}
      {!loading && assessment && (
        <div className="space-y-6">
          {/* Location Summary Header Card */}
          <GlassPanel rounded="3xl">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200/80">
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-cyan-700">
                  Target Assessment Location
                </span>
                <h2 className="text-2xl font-bold text-slate-900 tracking-tight mt-0.5">
                  {locationName}
                </h2>
                <p className="text-xs text-slate-500 font-mono mt-0.5">
                  Coordinates: {assessment.latitude.toFixed(4)}° N, {assessment.longitude.toFixed(4)}° E
                </p>
              </div>

              <div className="flex items-center gap-3">
                <div className="text-right">
                  <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold block">
                    Overall Risk for This Location
                  </span>
                  <span
                    className={`text-sm font-bold px-3 py-1 rounded-full inline-block mt-0.5 ${
                      assessment.overall_composite_risk === 'RED'
                        ? 'bg-rose-100 text-rose-800 border border-rose-300'
                        : assessment.overall_composite_risk === 'ORANGE'
                        ? 'bg-amber-100 text-amber-800 border border-amber-300'
                        : assessment.overall_composite_risk === 'YELLOW'
                        ? 'bg-yellow-100 text-yellow-800 border border-yellow-300'
                        : 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                    }`}
                  >
                    {assessment.overall_composite_risk} ADVISORY
                  </span>
                </div>

                <Link to={`/map?lat=${assessment.latitude}&lon=${assessment.longitude}&zoom=9`}>
                  <LiquidButton variant="secondary" size="sm" rightIcon={<Globe2 className="w-4 h-4 text-cyan-700" />}>
                    View on Map
                  </LiquidButton>
                </Link>
              </div>
            </div>

            <p className="text-sm text-slate-700 mt-4 leading-relaxed font-normal">
              {assessment.overall_summary || 'Multi-hazard environmental synthesis completed successfully across all 5 hazard vectors.'}
            </p>
          </GlassPanel>

          {/* 5 Hazard Assessment Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {Object.entries(assessment.assessments).map(([hazardKey, rawData]) => {
              const hData = rawData as any;
              const meta = hazardMeta[hazardKey] || {
                label: hazardKey.toUpperCase(),
                color: '#087EA4',
                icon: Layers,
                dataSrc: 'HAZARDX Official Feeds',
              };
              const Icon = meta.icon;

              return (
                <GlassCard
                  key={hazardKey}
                  glowColor={meta.color}
                  className="flex flex-col justify-between"
                  style={{ borderLeft: `4px solid ${meta.color}` }}
                >
                  <div className="space-y-3.5">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2.5">
                        <div
                          className="p-2.5 rounded-xl shadow-xs"
                          style={{ background: `${meta.color}15`, color: meta.color }}
                        >
                          <Icon className="w-5 h-5" />
                        </div>
                        <h3 className="font-bold text-slate-900 text-base">{meta.label}</h3>
                      </div>

                      <span
                        className="text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider"
                        style={{
                          background: `${meta.color}18`,
                          color: meta.color,
                          border: `1px solid ${meta.color}35`,
                        }}
                      >
                        {hData.risk_category || hData.alert_level}
                      </span>
                    </div>

                    <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-1">
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider font-bold">
                        What is increasing the risk?
                      </span>
                      <p className="text-xs text-slate-700 leading-relaxed">
                        {hData.top_features && hData.top_features.length > 0
                          ? `Driven primarily by ${hData.top_features.slice(0, 2).map((f: any) => ((f.feature_name || f.feature || '') as string).replace(/_/g, ' ')).join(' and ')}.`
                          : 'Evaluated against verified meteorological shifts and local topography.'}
                      </p>
                    </div>

                    <div className="text-[11px] text-slate-500 flex items-center justify-between pt-1">
                      <span>Source: {meta.dataSrc.split('&')[0]}</span>
                      <span className="font-mono text-slate-600 font-medium">Horizon: 24h</span>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-slate-100 mt-3 flex items-center justify-between text-xs">
                    <span className="text-slate-600">
                      Estimated Threat Score: <strong className="text-slate-900 font-mono">{((hData.probability || 0.1) * 100).toFixed(0)}%</strong>
                    </span>
                    <Link to={`/map?hazard=${hazardKey}&lat=${assessment.latitude}&lon=${assessment.longitude}`}>
                      <span className="text-cyan-700 font-semibold hover:underline">View on Map &rarr;</span>
                    </Link>
                  </div>
                </GlassCard>
              );
            })}
          </div>

          {/* Advanced Environmental Context (Collapsible) */}
          <div className="pt-2">
            <button
              type="button"
              onClick={() => setShowAdvancedEnv(!showAdvancedEnv)}
              className="w-full flex items-center justify-between p-4 rounded-2xl glass-card text-left text-sm font-semibold text-slate-700 hover:text-slate-900"
            >
              <span className="flex items-center gap-2">
                <Info className="w-4 h-4 text-cyan-700" />
                Inspect Local Terrain & Environmental Sensor Telemetry
              </span>
              <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform ${showAdvancedEnv ? 'rotate-180' : ''}`} />
            </button>

            {showAdvancedEnv && assessment.environmental_context && (
              <div className="mt-3 p-6 rounded-3xl glass-panel grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200">
                  <span className="text-slate-500 block mb-0.5 font-medium">Elevation (DEM)</span>
                  <span className="text-sm font-bold text-slate-900 font-mono">
                    {assessment.environmental_context.elevation_m.toFixed(1)} m
                  </span>
                </div>

                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200">
                  <span className="text-slate-500 block mb-0.5 font-medium">Hillslope Angle</span>
                  <span className="text-sm font-bold text-slate-900 font-mono">
                    {assessment.environmental_context.slope_degrees.toFixed(1)}°
                  </span>
                </div>

                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200">
                  <span className="text-slate-500 block mb-0.5 font-medium">Active Fault Dist</span>
                  <span className="text-sm font-bold text-slate-900 font-mono">
                    {assessment.environmental_context.dist_to_active_fault_km.toFixed(1)} km
                  </span>
                </div>

                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200">
                  <span className="text-slate-500 block mb-0.5 font-medium">24h Rainfall (NWP)</span>
                  <span className="text-sm font-bold text-slate-900 font-mono">
                    {assessment.environmental_context.precip_1d_mm.toFixed(1)} mm
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default LocationAssessmentPage;
