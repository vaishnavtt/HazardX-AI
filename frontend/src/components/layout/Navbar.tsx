import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { api } from '../../api/client';
import { Shield, Clock, Menu, X, MapPin } from 'lucide-react';
import { LiquidButton } from '../ui/LiquidButton';
import { LiquidIconButton } from '../ui/LiquidIconButton';

interface NavbarProps {
  onToggleSidebar?: () => void;
  isSidebarOpen?: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({ onToggleSidebar, isSidebarOpen }) => {
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean | null>(null);
  const [currentTime, setCurrentTime] = useState<string>('');
  const location = useLocation();

  useEffect(() => {
    const updateClock = () => {
      const now = new Date();
      setCurrentTime(now.toUTCString().replace('GMT', 'UTC'));
    };
    updateClock();
    const clockInterval = setInterval(updateClock, 1000);

    const checkHealth = async () => {
      try {
        const health = await api.getHealth();
        setIsBackendHealthy(health.status === 'healthy');
      } catch (e) {
        setIsBackendHealthy(false);
      }
    };
    checkHealth();
    const healthInterval = setInterval(checkHealth, 30000);

    return () => {
      clearInterval(clockInterval);
      clearInterval(healthInterval);
    };
  }, []);

  return (
    <header className="h-16 glass-header sticky top-0 z-40 px-4 lg:px-8 flex items-center justify-between border-b border-slate-200/80 bg-white/90">
      {/* Brand & Identity */}
      <div className="flex items-center gap-3">
        {onToggleSidebar && (
          <div className="lg:hidden">
            <LiquidIconButton
              icon={isSidebarOpen ? <X className="w-5 h-5 text-slate-700" /> : <Menu className="w-5 h-5 text-slate-700" />}
              label="Toggle navigation"
              variant="ghost"
              size="sm"
              onClick={onToggleSidebar}
            />
          </div>
        )}

        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-2xl bg-gradient-to-br from-cyan-600 to-blue-600 flex items-center justify-center shadow-md shadow-cyan-600/20 border border-white/60 transition-transform group-hover:scale-105">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-base font-bold tracking-tight text-slate-900">
                HAZARD<span className="text-cyan-700">X</span> AI
              </span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-cyan-100 text-cyan-800 border border-cyan-300">
                LIVE
              </span>
            </div>
            <p className="text-[11px] text-slate-500 hidden sm:block font-medium">
              Global Multi-Hazard Intelligence & Early Warning
            </p>
          </div>
        </Link>
      </div>

      {/* Quick Location Action & Telemetry */}
      <div className="flex items-center gap-3">
        {/* Check Location Quick Button */}
        {location.pathname !== '/check-location' && (
          <Link to="/check-location" className="hidden sm:inline-flex">
            <LiquidButton
              variant="secondary"
              size="sm"
              leftIcon={<MapPin className="w-3.5 h-3.5 text-cyan-700" />}
            >
              Check My Location
            </LiquidButton>
          </Link>
        )}

        {/* UTC Clock */}
        <div className="hidden md:flex items-center gap-1.5 text-xs text-slate-600 bg-slate-100 border border-slate-200 px-3 py-1.5 rounded-full font-mono shadow-xs">
          <Clock className="w-3.5 h-3.5 text-slate-500" />
          <span>{currentTime || 'Syncing UTC...'}</span>
        </div>

        {/* Live System Indicator */}
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-300 text-emerald-800 text-xs font-semibold shadow-xs">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="hidden sm:inline">
            {isBackendHealthy === false ? 'Offline' : 'Sensors Connected'}
          </span>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
