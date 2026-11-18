import React from 'react';
import { GlobalHazardMap } from '../components/map/GlobalHazardMap';
import { Globe2, ShieldAlert, Radio, TrendingUp, Sparkles, MapPin } from 'lucide-react';
import { GlassPanel } from '../components/glass/GlassPanel';

export const MapPage: React.FC = () => {
  return (
    <div className="space-y-6 pb-12">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200/80 pb-5">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-50 border border-cyan-200 text-cyan-800 text-xs font-semibold mb-2">
            <Globe2 className="w-3.5 h-3.5 text-cyan-700" />
            Global GIS Intelligence Map
          </div>
          <h1 className="text-2xl md:text-3xl font-black text-slate-900 tracking-tight">
            Live Natural Hazard <span className="text-cyan-700">Interactive Map</span>
          </h1>
          <p className="text-xs md:text-sm text-slate-600 mt-1 max-w-3xl">
            Explore active satellite detections, physical sensor feeds, and 72-hour forecast risk zones. 
            Click any hazard zone or marker for full details, or click any location on Earth to check its risks.
          </p>
        </div>

        {/* Telemetry pill */}
        <div className="flex flex-wrap items-center gap-2 shrink-0">
          <div className="flex items-center gap-2 bg-white border border-slate-200 px-3.5 py-1.5 rounded-full text-xs font-mono shadow-xs">
            <Radio className="w-3.5 h-3.5 text-emerald-600 animate-pulse" />
            <span className="text-slate-500">FEEDS:</span>
            <span className="text-emerald-700 font-bold">5 HAZARD STREAMS</span>
          </div>
          <div className="flex items-center gap-2 bg-white border border-slate-200 px-3.5 py-1.5 rounded-full text-xs font-mono shadow-xs">
            <TrendingUp className="w-3.5 h-3.5 text-cyan-700" />
            <span className="text-slate-500">HORIZONS:</span>
            <span className="text-cyan-800 font-bold">6h &rarr; 72h</span>
          </div>
        </div>
      </div>

      {/* Interactive Global Multi-Hazard Map Component */}
      <GlobalHazardMap />

      {/* Information Banner on Geospatial Integrity */}
      <div className="p-5 rounded-3xl glass-panel text-xs text-slate-700 flex items-start gap-3.5 border border-slate-200">
        <ShieldAlert className="w-5 h-5 text-cyan-700 mt-0.5 shrink-0" />
        <div className="leading-relaxed">
          <span className="font-bold text-slate-900 block mb-1">
            Geospatial Integrity & Cartographic Color Standards
          </span>
          All plotted zones and markers represent authentic observations or validated forecast corridors derived from official scientific feeds:
          <strong> Copernicus GloFAS (Floods)</strong>, <strong>NASA GLC & Open-Meteo Infiltration (Landslides)</strong>, <strong>USGS Seismicity & Fault Catalogs (Earthquakes)</strong>, <strong>NOAA NHC & IMD RSMC (Cyclones)</strong>, and <strong>NASA FIRMS Thermal VIIRS (Wildfires)</strong>.
          Hazard types are strictly assigned non-overlapping colors (<span className="text-[#2196F3] font-bold">Blue</span>, <span className="text-[#FF9800] font-bold">Orange</span>, <span className="text-[#9C27B0] font-bold">Purple</span>, <span className="text-[#00BCD4] font-bold">Cyan</span>, <span className="text-[#F44336] font-bold">Red</span>), and risk severity is represented through fill opacity and stroke weight.
        </div>
      </div>
    </div>
  );
};

export default MapPage;
