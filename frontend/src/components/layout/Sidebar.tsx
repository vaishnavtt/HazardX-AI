import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import {
  Home,
  Globe2,
  Radio,
  MapPin,
  Bell,
  History,
  Info,
  ChevronDown,
  Cpu,
  Droplets,
  Mountain,
  Activity,
  Wind,
  Flame,
  Layers,
} from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const [showAdvanced, setShowAdvanced] = useState(false);

  // Recommended Public-Facing 7-Item Navigation
  const publicNavItems = [
    { name: 'Home', path: '/', icon: Home },
    { name: 'Live Map', path: '/map', icon: Globe2 },
    { name: 'Forecasts', path: '/forecasts', icon: Radio },
    { name: 'Check My Location', path: '/check-location', icon: MapPin },
    { name: 'Active Alerts', path: '/alerts', icon: Bell },
    { name: 'Past Events', path: '/past-events', icon: History },
    { name: 'About HAZARDX AI', path: '/about', icon: Info },
  ];

  // Advanced Section for Technical/Scientific Drill-down
  const advancedNavItems = [
    { name: 'Model Governance', path: '/models', icon: Cpu },
    { name: 'Flood Intelligence', path: '/hazards/floods', icon: Droplets, color: '#2196F3' },
    { name: 'Landslide Intelligence', path: '/hazards/landslides', icon: Mountain, color: '#FF9800' },
    { name: 'Earthquake Aftershocks', path: '/hazards/earthquakes', icon: Activity, color: '#9C27B0' },
    { name: 'Cyclone Intelligence', path: '/hazards/cyclones', icon: Wind, color: '#00BCD4' },
    { name: 'Wildfire Intelligence', path: '/hazards/wildfires', icon: Flame, color: '#F44336' },
    { name: 'Multi-Hazard Unified', path: '/multi-hazard', icon: Layers },
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-sm lg:hidden"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed top-16 bottom-0 left-0 z-40 w-64 glass-sidebar bg-white/95 border-r border-slate-200/80 flex flex-col transition-transform duration-300 ease-out lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <span className="glass-specular-sheen" />

        {/* Primary Navigation List */}
        <div className="flex-1 overflow-y-auto px-4 py-5 space-y-1.5">
          <div className="text-[11px] font-bold tracking-wider text-slate-400 uppercase px-3 pb-2">
            Public Early Warning
          </div>

          {publicNavItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === '/'}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-2xl text-sm font-semibold transition-all duration-200 ${
                    isActive
                      ? 'bg-cyan-50 text-cyan-900 border border-cyan-200 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0 text-cyan-700" />
                <span>{item.name}</span>
              </NavLink>
            );
          })}

          {/* Advanced Section Divider */}
          <div className="pt-4 border-t border-slate-200/80 mt-4">
            <button
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="w-full flex items-center justify-between px-3 py-2 text-xs font-bold text-slate-500 hover:text-slate-800 transition-colors uppercase tracking-wider rounded-xl"
            >
              <span>Advanced Simulators</span>
              <ChevronDown className={`w-3.5 h-3.5 transition-transform duration-200 ${showAdvanced ? 'rotate-180' : ''}`} />
            </button>

            {showAdvanced && (
              <div className="mt-1 space-y-1 pl-1 animate-in fade-in duration-150">
                {advancedNavItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <NavLink
                      key={item.path}
                      to={item.path}
                      onClick={onClose}
                      className={({ isActive }) =>
                        `flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium transition-all ${
                          isActive
                            ? 'bg-cyan-50 text-cyan-900 border border-cyan-200 font-semibold'
                            : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                        }`
                      }
                    >
                      <Icon 
                        className="w-3.5 h-3.5 shrink-0" 
                        style={item.color ? { color: item.color } : { color: '#087EA4' }} 
                      />
                      <span className="truncate">{item.name}</span>
                    </NavLink>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        {/* Footer / Emergency Notice */}
        <div className="p-4 border-t border-slate-200/80 text-center">
          <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200">
            <span className="text-[11px] font-bold text-cyan-800 block mb-0.5">
              Live Global Monitor
            </span>
            <p className="text-[10px] text-slate-500 leading-tight">
              Automated scientific guidance. In emergency, call local emergency services.
            </p>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
