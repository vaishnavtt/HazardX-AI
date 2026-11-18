import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';

export interface DropdownOption<T extends string = string> {
  value: T;
  label: string;
  description?: string;
  icon?: React.ReactNode;
}

export interface LiquidDropdownProps<T extends string = string> {
  options: DropdownOption<T>[];
  value: T;
  onChange: (value: T) => void;
  label?: string;
  size?: 'sm' | 'md';
  className?: string;
}

export function LiquidDropdown<T extends string = string>({
  options,
  value,
  onChange,
  label,
  size = 'md',
  className = '',
}: LiquidDropdownProps<T>) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const selectedOption = options.find((o) => o.value === value) || options[0];

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-xs gap-1.5',
    md: 'px-4 py-2 text-sm gap-2'
  }[size];

  return (
    <div className={`relative inline-block text-left ${className}`} ref={containerRef}>
      {label && <span className="block text-xs font-medium text-slate-400 mb-1.5">{label}</span>}

      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={`liquid-btn-base liquid-btn-secondary ${sizeClasses} w-full justify-between rounded-xl`}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
      >
        <span className="glass-specular-sheen" />
        <span className="flex items-center gap-2 truncate">
          {selectedOption?.icon}
          <span className="font-medium text-slate-100">{selectedOption?.label}</span>
        </span>
        <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 z-50 mt-2 min-w-[200px] w-full rounded-2xl glass-panel p-1.5 shadow-2xl animate-in fade-in zoom-in-95 duration-150">
          <ul role="listbox" className="space-y-1">
            {options.map((opt) => {
              const isSelected = opt.value === value;
              return (
                <li
                  key={opt.value}
                  role="option"
                  aria-selected={isSelected}
                  onClick={() => {
                    onChange(opt.value);
                    setIsOpen(false);
                  }}
                  className={`flex items-center justify-between px-3 py-2 rounded-xl text-sm cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-blue-500/20 text-cyan-300 font-medium border border-blue-500/30'
                      : 'text-slate-300 hover:bg-white/10 hover:text-white'
                  }`}
                >
                  <div className="flex items-center gap-2.5 truncate">
                    {opt.icon && <span className="shrink-0">{opt.icon}</span>}
                    <div className="flex flex-col text-left">
                      <span>{opt.label}</span>
                      {opt.description && (
                        <span className="text-[11px] text-slate-400">{opt.description}</span>
                      )}
                    </div>
                  </div>
                  {isSelected && <Check className="w-4 h-4 text-cyan-400 shrink-0 ml-2" />}
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
}

export default LiquidDropdown;
