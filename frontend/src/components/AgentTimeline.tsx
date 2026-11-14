import React from 'react';
import {
  Compass,
  FileCode,
  SearchCheck,
  RefreshCw,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Clock
} from 'lucide-react';

interface AgentTimelineProps {
  currentAgent: string;
  status: string;
  retryCount: number;
  maxRetries: number;
  score?: number;
  threshold?: number;
}

export const AgentTimeline: React.FC<AgentTimelineProps> = ({
  currentAgent,
  status,
  retryCount,
  maxRetries,
  score,
  threshold = 80
}) => {
  const steps = [
    {
      id: 'planner',
      name: 'Content Planner',
      role: 'Instructional Architecture',
      icon: Compass,
      description: 'Breaks down topic & defines evaluation rubric'
    },
    {
      id: 'generator',
      name: 'Content Generator',
      role: 'Curriculum Synthesis',
      icon: FileCode,
      description: 'Generates structured explanations, examples & quizzes'
    },
    {
      id: 'evaluator',
      name: 'Quality Evaluator',
      role: '6-Dimension Audit',
      icon: SearchCheck,
      description: 'Evaluates accuracy, gaps & flags unsupported claims'
    },
    {
      id: 'improver',
      name: 'Content Improver',
      role: 'Targeted Remediation',
      icon: RefreshCw,
      description: `Iterative refinement loop (Attempt ${retryCount}/${maxRetries})`
    },
    {
      id: 'validator',
      name: 'Final Validator',
      role: 'Publication Compliance',
      icon: ShieldCheck,
      description: 'Verifies consistency & authorizes release'
    }
  ];

  const getStepState = (stepId: string) => {
    const order = ['planner', 'generator', 'evaluator', 'improver', 'validator'];
    const currentIndex = order.indexOf(currentAgent);
    const stepIndex = order.indexOf(stepId);

    if (status === 'completed' || status === 'approved') return 'completed';
    if (status === 'failed') {
      if (stepId === currentAgent) return 'error';
    }
    if (status === 'manual_review') {
      if (stepId === 'validator' || stepId === 'improver') return 'warning';
      if (stepIndex <= 2) return 'completed';
    }

    if (currentAgent === stepId) return 'active';
    if (currentIndex > stepIndex) return 'completed';
    return 'pending';
  };

  return (
    <div className="w-full bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between pb-5 border-b border-slate-800 mb-6">
        <div>
          <h3 className="text-base font-semibold text-slate-100 flex items-center gap-2">
            Multi-Agent LangGraph Execution Pipeline
            {retryCount > 0 && (
              <span className="px-2 py-0.5 text-xs font-mono font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-md">
                Loop Iteration #{retryCount}
              </span>
            )}
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Autonomous multi-agent collaboration with feedback-driven refinement loop
          </p>
        </div>

        <div className="flex items-center gap-4 text-xs font-mono">
          <div className="flex items-center gap-1.5 text-slate-400">
            <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
            <span>Agent: <strong className="text-indigo-300 uppercase">{currentAgent}</strong></span>
          </div>
          {score !== undefined && (
            <div className="px-2.5 py-1 rounded bg-slate-800 border border-slate-700 text-slate-300">
              Score: <span className={score >= threshold ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold'}>{score.toFixed(1)}/100</span>
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 relative">
        {steps.map((step, idx) => {
          const state = getStepState(step.id);
          const Icon = step.icon;

          let ringColor = 'border-slate-800 bg-slate-850 text-slate-500';
          let statusBadge = (
            <span className="flex items-center gap-1 text-[11px] text-slate-500">
              <Clock className="w-3 h-3" /> Queued
            </span>
          );

          if (state === 'active') {
            ringColor = 'border-indigo-500 bg-indigo-950/40 text-indigo-400 ring-2 ring-indigo-500/30';
            statusBadge = (
              <span className="flex items-center gap-1 text-[11px] text-indigo-400 font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-ping"></span>
                Processing...
              </span>
            );
          } else if (state === 'completed') {
            ringColor = 'border-emerald-500/40 bg-emerald-950/20 text-emerald-400';
            statusBadge = (
              <span className="flex items-center gap-1 text-[11px] text-emerald-400 font-medium">
                <CheckCircle2 className="w-3 h-3 text-emerald-400" /> Completed
              </span>
            );
          } else if (state === 'warning') {
            ringColor = 'border-amber-500/50 bg-amber-950/20 text-amber-400';
            statusBadge = (
              <span className="flex items-center gap-1 text-[11px] text-amber-400 font-medium">
                <AlertTriangle className="w-3 h-3 text-amber-400" /> Human Review
              </span>
            );
          }

          return (
            <div
              key={step.id}
              className={`relative flex flex-col p-4 rounded-xl border transition-all duration-300 ${ringColor}`}
            >
              <div className="flex items-center justify-between mb-3">
                <div className={`p-2 rounded-lg ${state === 'active' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400'}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <span className="text-[10px] font-mono font-semibold text-slate-500">0{idx + 1}</span>
              </div>

              <h4 className="text-sm font-semibold text-slate-100">{step.name}</h4>
              <span className="text-[11px] text-indigo-400 font-mono mb-2">{step.role}</span>
              <p className="text-xs text-slate-400 leading-relaxed mb-4 flex-1">
                {step.description}
              </p>

              <div className="pt-2 border-t border-slate-800/80">
                {statusBadge}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

