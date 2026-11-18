import React from 'react';
import type { OperationalStatus } from '../../types/hazard';
import { CheckCircle2, FlaskConical, Ban } from 'lucide-react';

interface StatusIndicatorProps {
  status: OperationalStatus | string;
  size?: 'sm' | 'md';
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({ status, size = 'md' }) => {
  const normStatus = status.toUpperCase();

  if (normStatus === 'OPERATIONAL') {
    return (
      <span className={`inline-flex items-center gap-1.5 font-mono text-xs rounded border border-emerald-500/40 bg-emerald-950/40 text-emerald-400 px-2 py-0.5`}>
        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
        <span>OPERATIONAL</span>
      </span>
    );
  }

  if (normStatus === 'EXPERIMENTAL') {
    return (
      <span className={`inline-flex items-center gap-1.5 font-mono text-xs rounded border border-amber-500/40 bg-amber-950/40 text-amber-300 px-2 py-0.5`}>
        <FlaskConical className="w-3.5 h-3.5 text-amber-300" />
        <span>EXPERIMENTAL</span>
      </span>
    );
  }

  return (
    <span className={`inline-flex items-center gap-1.5 font-mono text-xs rounded border border-rose-500/40 bg-rose-950/40 text-rose-300 px-2 py-0.5`}>
      <Ban className="w-3.5 h-3.5 text-rose-400" />
      <span>UNAVAILABLE FOR OPERATIONAL USE</span>
    </span>
  );
};

