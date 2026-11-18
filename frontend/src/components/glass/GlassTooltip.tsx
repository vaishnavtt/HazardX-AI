import React, { useState } from 'react';
import { HelpCircle } from 'lucide-react';

export interface GlassTooltipProps {
  content: string | React.ReactNode;
  children?: React.ReactNode;
  title?: string;
  className?: string;
}

export const GlassTooltip: React.FC<GlassTooltipProps> = ({
  content,
  children,
  title,
  className = '',
}) => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div className={`relative inline-flex items-center ${className}`}>
      <span
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        onClick={() => setIsVisible(!isVisible)}
        className="cursor-pointer text-slate-400 hover:text-cyan-400 transition-colors inline-flex items-center"
      >
        {children || <HelpCircle className="w-3.5 h-3.5 ml-1" />}
      </span>

      {isVisible && (
        <div 
          className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 p-3 rounded-2xl glass-panel shadow-2xl z-50 text-xs text-slate-200 border border-white/20 animate-in fade-in zoom-in-95 pointer-events-none"
        >
          <span className="glass-specular-sheen" />
          {title && <span className="block font-semibold text-white mb-1">{title}</span>}
          <div>{content}</div>
        </div>
      )}
    </div>
  );
};

export default GlassTooltip;
