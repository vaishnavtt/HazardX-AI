import React from 'react';
import { Loader2, Radio } from 'lucide-react';

interface LoadingStateProps {
  message?: string;
  subMessage?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  message = 'Loading Hazard Intelligence...',
  subMessage = 'Querying live satellite feeds & calculating risk probabilities...',
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center rounded-3xl glass-panel shadow-2xl my-8">
      <span className="glass-specular-sheen" />
      <div className="relative mb-5">
        <div className="w-14 h-14 rounded-full border-2 border-cyan-400/20 border-t-cyan-400 animate-spin" />
        <Radio className="w-6 h-6 text-cyan-400 absolute inset-0 m-auto animate-pulse" />
      </div>
      <h3 className="text-base font-bold text-white tracking-tight mb-1.5">
        {message}
      </h3>
      <p className="text-xs text-slate-300 max-w-md leading-relaxed">
        {subMessage}
      </p>
    </div>
  );
};

export default LoadingState;
