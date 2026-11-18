import React from 'react';
import type { FeatureAttribution } from '../../types/hazard';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

interface ShapTableProps {
  attributions: FeatureAttribution[];
  title?: string;
}

export const ShapTable: React.FC<ShapTableProps> = ({
  attributions,
  title = 'TreeSHAP Feature Attributions (Local Explanation)',
}) => {
  if (!attributions || attributions.length === 0) {
    return (
      <div className="text-xs text-slate-500 italic p-4 text-center border border-slate-800 rounded-lg">
        No feature attributions available for this prediction.
      </div>
    );
  }

  // Calculate max score for relative bar scaling
  const maxScore = Math.max(...attributions.map(a => Math.abs(a.importance_score)), 0.01);

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
      <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
        <h4 className="text-xs font-mono font-semibold uppercase tracking-wider text-slate-300">
          {title}
        </h4>
        <span className="text-[11px] font-mono text-slate-400">
          Method: TreeExplainer
        </span>
      </div>

      <div className="space-y-3">
        {attributions.map((attr, idx) => {
          const isRiskIncreasing = attr.direction === 'RISK_INCREASING' || attr.importance_score > 0;
          const barWidthPercent = Math.min(100, Math.round((Math.abs(attr.importance_score) / maxScore) * 100));

          return (
            <div key={idx} className="bg-slate-950/50 p-2.5 rounded border border-slate-800/80">
              <div className="flex items-center justify-between text-xs mb-1">
                <span className="font-mono font-medium text-slate-200">
                  {attr.feature}
                </span>
                <div className="flex items-center gap-1.5 font-mono">
                  <span
                    className={`inline-flex items-center text-[11px] px-1.5 py-0.5 rounded font-semibold ${
                      isRiskIncreasing
                        ? 'bg-rose-950/80 text-rose-300 border border-rose-800/40'
                        : 'bg-emerald-950/80 text-emerald-300 border border-emerald-800/40'
                    }`}
                  >
                    {isRiskIncreasing ? (
                      <>
                        <ArrowUpRight className="w-3 h-3 mr-0.5" />
                        +{Math.abs(attr.importance_score).toFixed(3)} (RISK UP)
                      </>
                    ) : (
                      <>
                        <ArrowDownRight className="w-3 h-3 mr-0.5" />
                        -{Math.abs(attr.importance_score).toFixed(3)} (RISK DOWN)
                      </>
                    )}
                  </span>
                </div>
              </div>

              {/* Relative impact bar */}
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden my-1.5">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    isRiskIncreasing ? 'bg-rose-500' : 'bg-emerald-500'
                  }`}
                  style={{ width: `${barWidthPercent}%` }}
                />
              </div>

              <p className="text-[11px] text-slate-400 leading-normal">
                {attr.description}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

