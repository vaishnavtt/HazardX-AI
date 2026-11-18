import React from 'react';
import { AlertCircle, RotateCcw } from 'lucide-react';
import { LiquidButton } from '../ui/LiquidButton';

interface ErrorStateProps {
  title?: string;
  message: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Service Unavailable or Data Delay',
  message,
  onRetry,
}) => {
  return (
    <div className="rounded-3xl glass-panel p-8 text-center my-6 border border-rose-500/30 bg-rose-500/5 shadow-2xl">
      <span className="glass-specular-sheen" />
      <div className="inline-flex p-3 rounded-2xl bg-rose-500/20 text-rose-400 mb-3 border border-rose-500/30">
        <AlertCircle className="w-6 h-6" />
      </div>
      <h3 className="text-base font-bold text-rose-300 tracking-tight mb-2">
        {title}
      </h3>
      <p className="text-xs text-rose-200/90 max-w-md mx-auto mb-5 leading-relaxed">
        {message}
      </p>
      {onRetry && (
        <LiquidButton
          variant="danger"
          size="sm"
          onClick={onRetry}
          leftIcon={<RotateCcw className="w-3.5 h-3.5" />}
        >
          Retry Connection
        </LiquidButton>
      )}
    </div>
  );
};

export default ErrorState;
