import React from 'react';
import { AlertCircle, ShieldAlert, Info } from 'lucide-react';

interface DisclaimerBannerProps {
  type?: 'earthquake' | 'warning' | 'info';
  title?: string;
  children?: React.ReactNode;
}

export const DisclaimerBanner: React.FC<DisclaimerBannerProps> = ({
  type = 'warning',
  title,
  children,
}) => {
  if (type === 'earthquake') {
    return (
      <div className="rounded-lg border border-purple-500/40 bg-purple-950/30 p-4 text-purple-200">
        <div className="flex items-start gap-3">
          <ShieldAlert className="w-5 h-5 text-purple-400 mt-0.5 shrink-0" />
          <div className="text-xs leading-relaxed">
            <span className="font-semibold text-purple-300 font-mono uppercase tracking-wider block mb-1">
              Scientific Boundary & Legal Disclaimer
            </span>
            {children || (
              <span>
                This service provides statistical aftershock hazard assessment following a mainshock within 100 km and a 30-day temporal window. 
                <strong> This is NOT an exact or unprovoked earthquake prediction.</strong> Earthquakes cannot be predicted with exact time, location, and magnitude under modern seismological physics.
              </span>
            )}
          </div>
        </div>
      </div>
    );
  }

  if (type === 'info') {
    return (
      <div className="rounded-lg border border-cyan-500/30 bg-cyan-950/20 p-4 text-cyan-200">
        <div className="flex items-start gap-3">
          <Info className="w-5 h-5 text-cyan-400 mt-0.5 shrink-0" />
          <div className="text-xs leading-relaxed">
            {title && <span className="font-semibold text-cyan-300 font-mono uppercase tracking-wider block mb-1">{title}</span>}
            {children}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-amber-500/40 bg-amber-950/30 p-4 text-amber-200">
      <div className="flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-amber-400 mt-0.5 shrink-0" />
        <div className="text-xs leading-relaxed">
          {title && <span className="font-semibold text-amber-300 font-mono uppercase tracking-wider block mb-1">{title}</span>}
          {children}
        </div>
      </div>
    </div>
  );
};

