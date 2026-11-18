import React from 'react';

export interface GlassPanelProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  rounded?: 'lg' | 'xl' | '2xl' | '3xl' | 'full';
}

export const GlassPanel: React.FC<GlassPanelProps> = ({
  children,
  rounded = '2xl',
  className = '',
  ...props
}) => {
  const roundedClass = {
    lg: 'rounded-lg',
    xl: 'rounded-xl',
    '2xl': 'rounded-2xl',
    '3xl': 'rounded-3xl',
    full: 'rounded-full'
  }[rounded];

  return (
    <div className={`glass-panel ${roundedClass} p-5 relative overflow-hidden ${className}`} {...props}>
      <span className="glass-specular-sheen" />
      {children}
    </div>
  );
};

export default GlassPanel;

