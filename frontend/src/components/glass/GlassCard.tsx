import React from 'react';

export interface GlassCardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  glowColor?: string; // Optional hex or rgba for ambient subtle accent
  interactive?: boolean;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  header,
  footer,
  glowColor,
  interactive = false,
  className = '',
  style,
  ...props
}) => {
  return (
    <div
      className={`glass-card overflow-hidden ${
        interactive ? 'cursor-pointer hover:border-white/30 hover:-translate-y-1' : ''
      } ${className}`}
      style={{
        ...(glowColor ? { borderColor: `${glowColor}33` } : {}),
        ...style,
      }}
      {...props}
    >
      {/* Specular sheen on top edge */}
      <span className="glass-specular-sheen" />

      {glowColor && (
        <span
          aria-hidden="true"
          className="absolute -top-12 -right-12 w-36 h-36 rounded-full blur-2xl opacity-15 pointer-events-none"
          style={{ background: glowColor }}
        />
      )}

      {header && (
        <div className="px-6 py-4 border-b border-slate-200/60 flex items-center justify-between">
          {header}
        </div>
      )}

      <div className="p-6">{children}</div>

      {footer && (
        <div className="px-6 py-3.5 border-t border-slate-200/60 bg-slate-50/50 flex items-center justify-between">
          {footer}
        </div>
      )}
    </div>
  );
};

export default GlassCard;
