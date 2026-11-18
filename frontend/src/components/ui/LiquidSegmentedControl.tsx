import React from 'react';

export interface SegmentOption<T extends string = string> {
  value: T;
  label: string;
  icon?: React.ReactNode;
  badge?: string | number;
}

export interface LiquidSegmentedControlProps<T extends string = string> {
  options: SegmentOption<T>[];
  value: T;
  onChange: (value: T) => void;
  size?: 'sm' | 'md';
  className?: string;
}

export function LiquidSegmentedControl<T extends string = string>({
  options,
  value,
  onChange,
  size = 'md',
  className = '',
}: LiquidSegmentedControlProps<T>) {
  const sizeClasses = {
    sm: 'p-1 gap-1 text-xs',
    md: 'p-1.5 gap-1.5 text-sm'
  }[size];

  const itemSizeClasses = {
    sm: 'px-3 py-1',
    md: 'px-4 py-1.5'
  }[size];

  return (
    <div 
      className={`inline-flex items-center rounded-full bg-slate-900/60 backdrop-blur-xl border border-white/12 shadow-inner select-none ${sizeClasses} ${className}`}
      role="tablist"
    >
      {options.map((opt) => {
        const isSelected = opt.value === value;
        return (
          <button
            key={opt.value}
            type="button"
            role="tab"
            aria-selected={isSelected}
            onClick={() => onChange(opt.value)}
            className={`relative flex items-center justify-center gap-1.5 rounded-full font-medium transition-all duration-250 cursor-pointer ${itemSizeClasses} ${
              isSelected
                ? 'text-white shadow-lg shadow-black/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
            }`}
          >
            {/* Liquid glass pill background for active tab */}
            {isSelected && (
              <span 
                className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500/30 to-cyan-500/30 border border-cyan-400/50 backdrop-blur-md -z-10"
                style={{
                  boxShadow: '0 4px 16px -2px rgba(34, 211, 238, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.4)'
                }}
              >
                <span className="glass-specular-sheen" />
              </span>
            )}

            {opt.icon && <span className="shrink-0">{opt.icon}</span>}
            <span>{opt.label}</span>

            {opt.badge !== undefined && (
              <span className={`text-[10px] px-1.5 py-0.5 rounded-full font-semibold ${
                isSelected ? 'bg-cyan-400/20 text-cyan-200' : 'bg-white/10 text-slate-300'
              }`}>
                {opt.badge}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}

export default LiquidSegmentedControl;
