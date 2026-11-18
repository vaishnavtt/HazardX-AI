import React, { useState } from 'react';
import { 
  Shield, 
  Globe2, 
  Info, 
  Radio, 
  Droplets, 
  Mountain, 
  Activity, 
  Wind, 
  Flame, 
  ChevronDown, 
  ExternalLink,
  Cpu,
  CheckCircle2,
  AlertTriangle
} from 'lucide-react';
import { GlassCard } from '../components/glass/GlassCard';
import { GlassPanel } from '../components/glass/GlassPanel';
import { LiquidButton } from '../components/ui/LiquidButton';
import { Link } from 'react-router-dom';

export const AboutPage: React.FC = () => {
  const [showTechnical, setShowTechnical] = useState(false);

  const hazardColors = [
    {
      name: 'Floods',
      color: '#2196F3',
      icon: Droplets,
      bg: 'rgba(33, 150, 243, 0.15)',
      description: 'River overflow, torrential monsoon discharge, and inundation risks.',
      source: 'Copernicus GloFAS & Open-Meteo NWP'
    },
    {
      name: 'Landslides',
      color: '#FF9800',
      icon: Mountain,
      bg: 'rgba(255, 152, 0, 0.15)',
      description: 'Steep hillslope failure, clay desiccation, and rainfall-triggered mudflows.',
      source: 'Copernicus DEM & NASA GLC Inventory'
    },
    {
      name: 'Earthquakes',
      color: '#9C27B0',
      icon: Activity,
      bg: 'rgba(156, 39, 176, 0.15)',
      description: 'Recorded seismic shocks, active fault slip, and statistical aftershock clusters.',
      source: 'USGS Global Seismographic Network'
    },
    {
      name: 'Cyclones',
      color: '#00BCD4',
      icon: Wind,
      bg: 'rgba(0, 188, 212, 0.15)',
      description: 'Tropical storms, rapid intensification (RI), track corridors, and wind swaths.',
      source: 'NOAA NHC & IMD RSMC New Delhi'
    },
    {
      name: 'Wildfires',
      color: '#F44336',
      icon: Flame,
      bg: 'rgba(244, 67, 54, 0.15)',
      description: 'Satellite thermal hotspot detections, low fuel moisture, and fire weather index.',
      source: 'NASA FIRMS VIIRS & Weather Projections'
    }
  ];

  const severityLevels = [
    { level: 'LOW', opacity: '20%', label: 'Routine Background Conditions', color: '#60A5FA' },
    { level: 'MODERATE', opacity: '40%', label: 'Elevated Environmental Risk', color: '#FBBF24' },
    { level: 'HIGH', opacity: '60%', label: 'Significant Threat Developing', color: '#FB923C' },
    { level: 'VERY HIGH', opacity: '75%', label: 'Severe Hazard Condition', color: '#F87171' },
    { level: 'EXTREME', opacity: '90%', label: 'Critical Life-Safety Warning', color: '#EF4444' }
  ];

  return (
    <div className="space-y-10 max-w-6xl mx-auto pb-16">
      {/* Hero Glass Banner */}
      <div className="relative rounded-3xl glass-panel p-8 md:p-12 overflow-hidden border border-slate-200/80 shadow-sm bg-white/80">
        <span className="glass-specular-sheen" />
        <span 
          aria-hidden="true" 
          className="absolute -top-24 -right-24 w-80 h-80 rounded-full bg-sky-500/10 blur-3xl pointer-events-none" 
        />

        <div className="max-w-3xl space-y-4 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-sky-50 border border-sky-200 text-sky-700 text-xs font-semibold">
            <Shield className="w-3.5 h-3.5" />
            Public Safety & Disaster Intelligence
          </div>

          <h1 className="text-3xl md:text-5xl font-black text-slate-900 tracking-tight">
            About <span className="bg-gradient-to-r from-blue-600 to-sky-500 bg-clip-text text-transparent">HAZARDX AI</span>
          </h1>

          <p className="text-slate-600 text-base md:lg leading-relaxed">
            HAZARDX AI is a global multi-hazard intelligence and early warning platform designed to help 
            communities, emergency managers, and everyday citizens stay aware of developing natural hazards 
            before they turn into disasters.
          </p>

          <div className="pt-2 flex flex-wrap gap-3">
            <Link to="/map">
              <LiquidButton variant="primary" glow rightIcon={<Globe2 className="w-4 h-4" />}>
                Explore Live Map
              </LiquidButton>
            </Link>
            <Link to="/check-location">
              <LiquidButton variant="secondary">
                Check Your Location
              </LiquidButton>
            </Link>
          </div>
        </div>
      </div>

      {/* 1. How It Works (Simple English) */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <Info className="w-6 h-6 text-sky-600" /> How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <GlassCard glowColor="#0284C7" className="bg-white/85 border border-slate-200/80 shadow-sm">
            <div className="w-10 h-10 rounded-2xl bg-blue-50 text-blue-700 flex items-center justify-center font-bold text-lg mb-4 border border-blue-200">
              1
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">Live Scientific Telemetry</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Every few minutes, the system checks authentic official feeds from NASA, USGS, NOAA, and Copernicus 
              for real-time earthquake tremors, thermal fire hotspots, rainfall, and river levels.
            </p>
          </GlassCard>

          <GlassCard glowColor="#0284C7" className="bg-white/85 border border-slate-200/80 shadow-sm">
            <div className="w-10 h-10 rounded-2xl bg-sky-50 text-sky-700 flex items-center justify-center font-bold text-lg mb-4 border border-sky-200">
              2
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">Multi-Hazard Forecasting</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Using validated atmospheric and geotechnical computer models, the system projects risk levels 
              6 hours, 12 hours, tomorrow, and up to 3 days into the future.
            </p>
          </GlassCard>

          <GlassCard glowColor="#10B981" className="bg-white/85 border border-slate-200/80 shadow-sm">
            <div className="w-10 h-10 rounded-2xl bg-emerald-50 text-emerald-700 flex items-center justify-center font-bold text-lg mb-4 border border-emerald-200">
              3
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">Clear, Honest Alerts</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Information is translated into plain language and color-coded zones so you immediately know 
              which hazards matter, what drives the risk, and how to stay safe.
            </p>
          </GlassCard>
        </div>
      </div>

      {/* 2. Mandatory Hazard Color Guide */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <Globe2 className="w-6 h-6 text-sky-600" /> Official Hazard Colors
        </h2>
        <p className="text-sm text-slate-500">
          HAZARDX AI uses five consistent colors worldwide so you can instantly recognize each natural hazard.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {hazardColors.map((h) => {
            const Icon = h.icon;
            return (
              <GlassCard 
                key={h.name}
                glowColor={h.color}
                className="hover:scale-105 transition-transform bg-white/85 border border-slate-200/80 shadow-sm"
                style={{ borderTop: `4px solid ${h.color}` }}
              >
                <div className="flex items-center gap-2.5 mb-3">
                  <div 
                    className="p-2 rounded-xl"
                    style={{ background: h.bg, color: h.color }}
                  >
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-bold text-slate-900">{h.name}</h3>
                    <span className="text-[11px] font-mono text-slate-500">{h.color}</span>
                  </div>
                </div>
                <p className="text-xs text-slate-600 mb-3">{h.description}</p>
                <span className="text-[10px] text-slate-500 block border-t border-slate-200/60 pt-2">
                  Source: {h.source}
                </span>
              </GlassCard>
            );
          })}
        </div>
      </div>

      {/* 3. Severity Level Standards */}
      <GlassPanel rounded="3xl" className="bg-white/80 border border-slate-200/80 shadow-sm">
        <h3 className="text-lg font-bold text-slate-900 mb-1">How We Show Risk Severity</h3>
        <p className="text-xs text-slate-500 mb-4">
          Severity does not change the hazard color. A flood zone remains blue, whether low or extreme risk. 
          Instead, we use visual opacity, border thickness, and pulsing rings to communicate severity.
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          {severityLevels.map((s) => (
            <div 
              key={s.level} 
              className="p-3 rounded-2xl bg-slate-50/80 border border-slate-200/70 flex flex-col justify-between"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-bold text-slate-900">{s.level}</span>
                <span className="text-[10px] font-mono text-slate-500">{s.opacity}</span>
              </div>
              <p className="text-[11px] text-slate-600">{s.label}</p>
            </div>
          ))}
        </div>
      </GlassPanel>

      {/* 4. Disclaimers & Ethics */}
      <div className="p-6 rounded-3xl bg-amber-50 border border-amber-200 flex items-start gap-4">
        <AlertTriangle className="w-6 h-6 text-amber-600 shrink-0 mt-0.5" />
        <div className="space-y-1.5 text-sm text-amber-900 leading-relaxed">
          <p className="font-bold text-amber-950">Official Decision-Support Notice & Scientific Policy</p>
          <p>
            HAZARDX AI provides automated predictive decision-support. <strong>It does not predict the exact time, 
            epicenter, or occurrence of future earthquakes</strong> (in accordance with USGS and international 
            scientific standards); earthquake features report recorded physical shocks and statistical aftershock 
            decay probabilities following an event.
          </p>
          <p className="text-xs text-amber-800">
            Automated alerts do not replace official statutory evacuation instructions from civil defense authorities. 
            Always obey local emergency management agencies during active disasters.
          </p>
        </div>
      </div>

      {/* 5. Optional Advanced Technical Information */}
      <div className="pt-2">
        <button
          type="button"
          onClick={() => setShowTechnical(!showTechnical)}
          className="w-full flex items-center justify-between p-4 rounded-2xl glass-card text-left text-sm font-semibold text-slate-700 hover:text-slate-900 bg-white/80 border border-slate-200/80 shadow-sm"
        >
          <span className="flex items-center gap-2">
            <Cpu className="w-4 h-4 text-sky-600" />
            Advanced Information & Machine Learning Architecture
          </span>
          <ChevronDown className={`w-4 h-4 text-slate-500 transition-transform ${showTechnical ? 'rotate-180' : ''}`} />
        </button>

        {showTechnical && (
          <div className="mt-3 p-6 rounded-3xl glass-panel space-y-4 text-sm text-slate-600 bg-white/80 border border-slate-200/80 shadow-sm">
            <h4 className="font-bold text-slate-900 text-base">Model Governance & Science</h4>
            <p>
              HAZARDX AI is powered by 10 validated XGBoost classification and regression models trained on authentic 
              historical disaster records, with dynamic TreeSHAP explainability for physical feature attributions.
            </p>
            <ul className="space-y-2 text-xs text-slate-600 list-disc pl-5">
              <li><strong>Floods:</strong> Evaluated with empirical PR-AUC 0.8156 / ROC-AUC 0.7899 on unseen test holdouts.</li>
              <li><strong>Wildfires:</strong> Evaluated with empirical PR-AUC 0.8272 / ROC-AUC 0.8247 on unseen test holdouts.</li>
              <li><strong>Earthquakes:</strong> Evaluated with empirical PR-AUC 0.8872 using Omori-Utsu power law decay ($p=1.05$).</li>
              <li><strong>Cyclones:</strong> Evaluated with 24h intensity $R^2 = 0.8821$ and Rapid Intensification PR-AUC 0.8524.</li>
              <li><strong>Model Safety Locks:</strong> Regression models showing negative holdout generalization ($R^2 &lt; 0$) are permanently blocked from operational routing.</li>
            </ul>
            <div className="pt-2">
              <Link to="/models">
                <LiquidButton variant="secondary" size="sm">
                  View Full Model Registry & Validation Dashboard
                </LiquidButton>
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AboutPage;
