import React from 'react';

export interface GlassStatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ReactNode;
  hazardColor?: string; // hex color (Flood #2196F3, etc.)
  badge?: string;
  trend?: 'up' | 'down' | 'stable';
  onClick?: () => void;
}

export const GlassStatCard: React.FC<GlassStatCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  hazardColor = '#60A5FA',
  badge,
  onClick,
}) => {
  return (
    <div
      onClick={onClick}
      className={`glass-card p-5 relative overflow-hidden transition-all duration-300 ${
        onClick ? 'cursor-pointer hover:scale-[1.02] hover:border-white/30' : ''
      }`}
      style={{
        borderLeft: `4px solid ${hazardColor}`
      }}
    >
      <span className="glass-specular-sheen" />

      {/* Subtle ambient colored glow in corner */}
      <span
        aria-hidden="true"
        className="absolute -top-10 -right-10 w-24 h-24 rounded-full blur-xl opacity-20 pointer-events-none"
        style={{ background: hazardColor }}
      />

      <div className="flex items-start justify-between mb-3">
        <span className="text-xs font-medium uppercase tracking-wider text-slate-400">
          {title}
        </span>
        <div 
          className="p-2.5 rounded-xl border border-white/10 shrink-0"
          style={{ background: `${hazardColor}18`, color: hazardColor }}
        >
          {icon}
        </div>
      </div>

      <div className="flex items-baseline gap-2 mb-1">
        <span className="text-3xl font-bold tracking-tight text-white">{value}</span>
        {badge && (
          <span 
            className="text-[11px] font-semibold px-2 py-0.5 rounded-full"
            style={{ background: `${hazardColor}25`, color: hazardColor }}
          >
            {badge}
          </span>
        )}
      </div>

      {subtitle && (
        <p className="text-xs text-slate-400 line-clamp-1 mt-1">{subtitle}</p>
      )}
    </div>
  );
};

export default GlassStatCard;
