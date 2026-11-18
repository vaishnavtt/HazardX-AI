import React from 'react';
import type { AlertLevel } from '../../types/hazard';
import { AlertTriangle, CheckCircle, ShieldAlert, AlertOctagon } from 'lucide-react';

interface AlertBadgeProps {
  level: AlertLevel;
  size?: 'sm' | 'md' | 'lg';
  showIcon?: boolean;
}

export const AlertBadge: React.FC<AlertBadgeProps> = ({
  level,
  size = 'md',
  showIcon = true,
}) => {
  const configs: Record<AlertLevel, { bg: string; text: string; border: string; label: string; icon: React.ReactNode }> = {
    GREEN: {
      bg: 'bg-emerald-950/60',
      text: 'text-emerald-400',
      border: 'border-emerald-500/40',
      label: 'QUIESCENT / LOW',
      icon: <CheckCircle className="w-3.5 h-3.5" />,
    },
    YELLOW: {
      bg: 'bg-amber-950/60',
      text: 'text-amber-300',
      border: 'border-amber-500/40',
      label: 'ADVISORY / MODERATE',
      icon: <AlertTriangle className="w-3.5 h-3.5" />,
    },
    ORANGE: {
      bg: 'bg-orange-950/60',
      text: 'text-orange-300',
      border: 'border-orange-500/40',
      label: 'HIGH ALERT',
      icon: <AlertOctagon className="w-3.5 h-3.5" />,
    },
    RED: {
      bg: 'bg-rose-950/70',
      text: 'text-rose-300',
      border: 'border-rose-500/50',
      label: 'SEVERE / CRITICAL',
      icon: <ShieldAlert className="w-3.5 h-3.5" />,
    },
  };

  const config = configs[level] || configs.GREEN;

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5 gap-1',
    md: 'text-xs px-2.5 py-1 gap-1.5',
    lg: 'text-sm px-3 py-1.5 gap-2 font-semibold',
  };

  return (
    <span
      className={`inline-flex items-center rounded-md border font-mono tracking-wider uppercase ${config.bg} ${config.text} ${config.border} ${sizeClasses[size]}`}
    >
      {showIcon && config.icon}
      <span>{config.label}</span>
    </span>
  );
};

