import React from 'react';
import { Loader2 } from 'lucide-react';

export type LiquidButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'success';
export type LiquidButtonSize = 'sm' | 'md' | 'lg';

export interface LiquidButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: LiquidButtonVariant;
  size?: LiquidButtonSize;
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  glow?: boolean;
}

export const LiquidButton: React.FC<LiquidButtonProps> = ({
  children,
  variant = 'secondary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  glow = false,
  className = '',
  disabled,
  ...props
}) => {
  const sizeClasses = {
    sm: 'px-3.5 py-1.5 text-xs gap-1.5',
    md: 'px-5 py-2.5 text-sm gap-2',
    lg: 'px-7 py-3.5 text-base gap-2.5'
  }[size];

  const variantClass = `liquid-btn-${variant}`;

  return (
    <button
      className={`liquid-btn-base ${variantClass} ${sizeClasses} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {/* Liquid specular highlight sheen across upper pill */}
      <span className="glass-specular-sheen" />

      {/* Optional ambient colored glow halo */}
      {glow && (
        <span 
          aria-hidden="true" 
          className="absolute -inset-1 rounded-full bg-cyan-400/20 blur-md opacity-75 pointer-events-none -z-10" 
        />
      )}

      {/* Loading Spinner */}
      {isLoading ? (
        <Loader2 className="w-4 h-4 animate-spin shrink-0 text-current" />
      ) : (
        leftIcon && <span className="shrink-0 flex items-center justify-center">{leftIcon}</span>
      )}

      {/* Button Content */}
      <span className="relative z-10 font-medium tracking-wide flex items-center gap-1.5">
        {children}
      </span>

      {/* Right Icon */}
      {!isLoading && rightIcon && (
        <span className="shrink-0 flex items-center justify-center">{rightIcon}</span>
      )}
    </button>
  );
};

export default LiquidButton;
