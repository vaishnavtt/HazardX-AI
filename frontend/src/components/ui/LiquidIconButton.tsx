import React from 'react';
import { Loader2 } from 'lucide-react';
import type { LiquidButtonVariant } from './LiquidButton';

export interface LiquidIconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: LiquidButtonVariant;
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  icon: React.ReactNode;
  label: string; // Accessible aria-label
  glow?: boolean;
}

export const LiquidIconButton: React.FC<LiquidIconButtonProps> = ({
  icon,
  label,
  variant = 'secondary',
  size = 'md',
  isLoading = false,
  glow = false,
  className = '',
  disabled,
  ...props
}) => {
  const sizeClasses = {
    sm: 'w-8 h-8 text-xs',
    md: 'w-10 h-10 text-sm',
    lg: 'w-12 h-12 text-base'
  }[size];

  const variantClass = `liquid-btn-${variant}`;

  return (
    <button
      className={`liquid-btn-base ${variantClass} ${sizeClasses} rounded-full p-0 flex items-center justify-center shrink-0 ${className}`}
      disabled={disabled || isLoading}
      aria-label={label}
      title={label}
      {...props}
    >
      <span className="glass-specular-sheen" />

      {glow && (
        <span 
          aria-hidden="true" 
          className="absolute -inset-1 rounded-full bg-cyan-400/25 blur-sm opacity-80 pointer-events-none -z-10" 
        />
      )}

      {isLoading ? (
        <Loader2 className="w-4 h-4 animate-spin text-current" />
      ) : (
        <span className="relative z-10 flex items-center justify-center">{icon}</span>
      )}
    </button>
  );
};

export default LiquidIconButton;
