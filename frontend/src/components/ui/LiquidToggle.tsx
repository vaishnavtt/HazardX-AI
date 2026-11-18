import React from 'react';

export interface LiquidToggleProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  description?: string;
  disabled?: boolean;
  activeColor?: string; // hex or tailwind class
  className?: string;
}

export const LiquidToggle: React.FC<LiquidToggleProps> = ({
  checked,
  onChange,
  label,
  description,
  disabled = false,
  activeColor = '#60A5FA',
  className = '',
}) => {
  return (
    <label 
      className={`inline-flex items-center gap-3 cursor-pointer select-none ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
      onClick={(e) => {
        if (disabled) return;
        e.preventDefault();
        onChange(!checked);
      }}
    >
      {/* Switch track */}
      <div 
        className="relative inline-flex h-6 w-11 shrink-0 rounded-full border border-white/20 transition-all duration-300 ease-in-out backdrop-blur-md"
        style={{
          background: checked 
            ? `linear-gradient(135deg, ${activeColor} 0%, rgba(34, 211, 238, 0.7) 100%)` 
            : 'rgba(255, 255, 255, 0.10)',
          boxShadow: checked
            ? `0 4px 14px -2px ${activeColor}66, inset 0 1px 0 rgba(255, 255, 255, 0.5)`
            : 'inset 0 1px 3px rgba(0, 0, 0, 0.4)'
        }}
      >
        {/* Specular sheen */}
        <span className="glass-specular-sheen h-1/2" />

        {/* Sliding fluid thumb */}
        <span
          className={`pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow-md transform transition-transform duration-300 ease-out my-auto ml-0.5 ${
            checked ? 'translate-x-5' : 'translate-x-0'
          }`}
          style={{
            boxShadow: '0 2px 5px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.8)'
          }}
        />
      </div>

      {(label || description) && (
        <div className="flex flex-col text-left">
          {label && <span className="text-sm font-medium text-slate-100">{label}</span>}
          {description && <span className="text-xs text-slate-400">{description}</span>}
        </div>
      )}
    </label>
  );
};

export default LiquidToggle;
