import React from 'react';

interface ScoreGaugeProps {
  score: number;
  threshold?: number;
  size?: 'sm' | 'md' | 'lg';
  showDetails?: boolean;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({
  score,
  threshold = 80,
  size = 'md',
  showDetails = true
}) => {
  const isPassing = score >= threshold;
  const radius = size === 'sm' ? 28 : size === 'lg' ? 68 : 46;
  const stroke = size === 'sm' ? 4 : size === 'lg' ? 8 : 6;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (Math.min(Math.max(score, 0), 100) / 100) * circumference;

  const colorClass = isPassing
    ? 'text-emerald-500 stroke-emerald-500'
    : score >= 70
    ? 'text-amber-500 stroke-amber-500'
    : 'text-rose-500 stroke-rose-500';

  const badgeBg = isPassing
    ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
    : score >= 70
    ? 'bg-amber-500/10 text-amber-400 border-amber-500/20'
    : 'bg-rose-500/10 text-rose-400 border-rose-500/20';

  const dimensions = radius * 2;

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative flex items-center justify-center">
        <svg height={dimensions} width={dimensions} className="transform -rotate-90">
          <circle
            stroke="currentColor"
            fill="transparent"
            strokeWidth={stroke}
            className="text-slate-800"
            r={normalizedRadius}
            cx={radius}
            cy={radius}
          />
          <circle
            stroke="currentColor"
            fill="transparent"
            strokeWidth={stroke}
            strokeDasharray={`${circumference} ${circumference}`}
            style={{ strokeDashoffset, transition: 'stroke-dashoffset 0.8s ease-in-out' }}
            strokeLinecap="round"
            className={colorClass}
            r={normalizedRadius}
            cx={radius}
            cy={radius}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className={`font-bold font-mono ${size === 'sm' ? 'text-sm' : size === 'lg' ? 'text-3xl' : 'text-xl'}`}>
            {score.toFixed(1)}
          </span>
          {size !== 'sm' && (
            <span className="text-[10px] text-slate-400 font-medium uppercase tracking-wider">
              / 100
            </span>
          )}
        </div>
      </div>

      {showDetails && (
        <div className="mt-2 text-center">
          <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold border ${badgeBg}`}>
            {isPassing ? 'PASSED (≥80)' : 'IMPROVEMENT REQ.'}
          </span>
        </div>
      )}
    </div>
  );
};

