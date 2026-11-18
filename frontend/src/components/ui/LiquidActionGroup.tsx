import React from 'react';

export interface LiquidActionGroupProps {
  children: React.ReactNode;
  className?: string;
  orientation?: 'horizontal' | 'vertical';
}

export const LiquidActionGroup: React.FC<LiquidActionGroupProps> = ({
  children,
  className = '',
  orientation = 'horizontal'
}) => {
  return (
    <div
      className={`inline-flex items-center gap-2 p-1.5 rounded-full bg-slate-900/60 backdrop-blur-xl border border-white/10 shadow-lg ${
        orientation === 'vertical' ? 'flex-col' : 'flex-row'
      } ${className}`}
      role="group"
    >
      {children}
    </div>
  );
};

export default LiquidActionGroup;
