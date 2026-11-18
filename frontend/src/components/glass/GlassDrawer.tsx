import React from 'react';
import { X } from 'lucide-react';
import { LiquidIconButton } from '../ui/LiquidIconButton';

export interface GlassDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  width?: string;
}

export const GlassDrawer: React.FC<GlassDrawerProps> = ({
  isOpen,
  onClose,
  title,
  subtitle,
  children,
  footer,
  width = 'w-88 sm:w-96',
}) => {
  if (!isOpen) return null;

  return (
    <div 
      className={`absolute top-3 right-3 bottom-3 ${width} glass-panel rounded-3xl p-5 shadow-2xl z-40 flex flex-col border border-white/16 animate-in slide-in-from-right duration-250`}
    >
      <span className="glass-specular-sheen" />

      {/* Header */}
      <div className="flex items-start justify-between pb-3.5 border-b border-white/10 shrink-0">
        <div className="pr-2">
          <h3 className="text-base font-bold text-white tracking-tight leading-snug">{title}</h3>
          {subtitle && <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>}
        </div>
        <LiquidIconButton
          icon={<X className="w-4 h-4" />}
          label="Close detail view"
          variant="ghost"
          size="sm"
          onClick={onClose}
        />
      </div>

      {/* Scrollable Body */}
      <div className="flex-1 overflow-y-auto py-3 space-y-4 pr-1 text-sm text-slate-200">
        {children}
      </div>

      {/* Footer */}
      {footer && (
        <div className="pt-3 border-t border-white/10 shrink-0 flex items-center justify-end gap-2">
          {footer}
        </div>
      )}
    </div>
  );
};

export default GlassDrawer;
