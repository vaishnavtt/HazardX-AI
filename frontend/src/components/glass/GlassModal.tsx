import React, { useEffect } from 'react';
import { X } from 'lucide-react';
import { LiquidIconButton } from '../ui/LiquidIconButton';

export interface GlassModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl';
}

export const GlassModal: React.FC<GlassModalProps> = ({
  isOpen,
  onClose,
  title,
  subtitle,
  children,
  footer,
  maxWidth = 'lg',
}) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const maxWidthClass = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl',
  }[maxWidth];

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto"
      role="dialog"
      aria-modal="true"
    >
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-slate-900/40 backdrop-blur-md transition-opacity"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Modal Surface */}
      <div 
        className={`relative w-full ${maxWidthClass} rounded-3xl glass-panel p-6 shadow-2xl z-10 border border-slate-200/80 my-8 animate-in fade-in zoom-in-95 duration-200`}
      >
        <span className="glass-specular-sheen" />

        {/* Header */}
        <div className="flex items-start justify-between pb-4 border-b border-slate-200/60 mb-4">
          <div>
            <h3 className="text-xl font-bold text-slate-900 tracking-tight">{title}</h3>
            {subtitle && <p className="text-xs text-slate-500 mt-1">{subtitle}</p>}
          </div>
          <LiquidIconButton
            icon={<X className="w-4 h-4" />}
            label="Close modal"
            variant="ghost"
            size="sm"
            onClick={onClose}
          />
        </div>

        {/* Body */}
        <div className="py-2 text-slate-700 max-h-[70vh] overflow-y-auto pr-1">
          {children}
        </div>

        {/* Footer */}
        {footer && (
          <div className="pt-4 border-t border-slate-200/60 mt-4 flex items-center justify-end gap-3">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
};

export default GlassModal;
