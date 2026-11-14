import React, { useEffect, useState, useRef } from 'react';
import { WorkflowStatus } from '../types';
import { fetchWorkflowStatus } from '../services/api';
import { AgentTimeline } from '../components/AgentTimeline';
import { ScoreGauge } from '../components/ScoreGauge';
import {
  Terminal,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  ArrowRight,
  BookOpen,
  BarChart3,
  ShieldCheck,
  History,
  Check,
  X
} from 'lucide-react';

interface LiveWorkflowProps {
  requestId: string | null;
  onNavigate: (view: string, contentId?: string) => void;
}

export const LiveWorkflow: React.FC<LiveWorkflowProps> = ({ requestId, onNavigate }) => {
  const [statusData, setStatusData] = useState<WorkflowStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!requestId) {
      setLoading(false);
      return;
    }

    let intervalId: any = null;

    async function pollStatus() {
      try {
        const data = await fetchWorkflowStatus(requestId!);
        setStatusData(data);
        setError(null);

        if (data.status === 'completed' || data.status === 'manual_review' || data.status === 'failed') {
          if (intervalId) clearInterval(intervalId);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to poll workflow status');
      } finally {
        setLoading(false);
      }
    }

    pollStatus();
    intervalId = setInterval(pollStatus, 1200);

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [requestId]);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [statusData?.logs]);

  if (!requestId) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center bg-slate-900 border border-slate-800 rounded-2xl max-w-xl mx-auto space-y-4">
        <div className="p-4 rounded-full bg-slate-800 text-slate-400">
          <Terminal className="w-8 h-8" />
        </div>
        <h3 className="text-lg font-bold text-slate-100">No Active Agent Workflow</h3>
        <p className="text-xs text-slate-400 leading-relaxed max-w-md">
          To observe the autonomous multi-agent pipeline in real-time, generate the assessment lesson on 'Introduction to RAG'.
        </p>
        <button
          onClick={() => onNavigate('create')}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30 transition-all"
        >
          <span>Start Generation</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    );
  }

  const isTerminal = statusData?.status === 'completed' || statusData?.status === 'manual_review';

  return (
    <div className="space-y-6">
      {/* Top Banner Status */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-mono text-slate-400">Request ID: {requestId}</span>
            <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider ${
              statusData?.status === 'completed'
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                : statusData?.status === 'manual_review'
                ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                : 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20'
            }`}>
              {statusData?.status || 'INITIALIZING'}
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-100">
            Autonomous Self-Evaluating Agent Pipeline
          </h2>
        </div>

        {isTerminal && statusData?.content_id && (
          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigate('evaluation', statusData.content_id)}
              className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition-colors"
            >
              <BarChart3 className="w-4 h-4 text-indigo-400" />
              <span>View Audit Report</span>
            </button>
            <button
              onClick={() => onNavigate('content', statusData.content_id)}
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30 transition-colors"
            >
              <BookOpen className="w-4 h-4" />
              <span>Read Shipping Lesson</span>
            </button>
          </div>
        )}
      </div>

      {/* Visual Pipeline Timeline */}
      <AgentTimeline
        currentAgent={statusData?.current_agent || 'planner'}
        status={statusData?.status || 'running'}
        retryCount={statusData?.retry_count || 0}
        maxRetries={statusData?.max_retries || 2}
        score={statusData?.latest_score}
        threshold={statusData?.quality_threshold || 80}
      />

      {/* Hard Pass/Fail Checkpoints Bar */}
      {statusData?.checkpoints && statusData.checkpoints.length > 0 && (
        <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-200">
              <ShieldCheck className="w-4 h-4 text-indigo-400" />
              <span>Rubric Checkpoints (Hard Pass/Fail — No Partial Credit)</span>
            </div>
            <span className={`text-[11px] font-mono font-bold ${
              statusData.all_checkpoints_passed ? 'text-emerald-400' : 'text-amber-400'
            }`}>
              {statusData.all_checkpoints_passed ? 'ALL CHECKS CLEARED' : 'CHECKPOINTS FAILED (REJECTED)'}
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
            {statusData.checkpoints.map((cp, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-xl border text-xs flex items-start gap-2.5 ${
                  cp.passed
                    ? 'bg-emerald-950/20 border-emerald-500/30 text-emerald-300'
                    : 'bg-rose-950/20 border-rose-500/30 text-rose-300'
                }`}
              >
                <div className={`p-1 rounded shrink-0 mt-0.5 ${cp.passed ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}`}>
                  {cp.passed ? <Check className="w-3.5 h-3.5" /> : <X className="w-3.5 h-3.5" />}
                </div>
                <div>
                  <span className="font-semibold block">{cp.label}: {cp.passed ? 'PASS' : 'FAIL'}</span>
                  <p className="text-[11px] opacity-80 leading-relaxed mt-0.5">{cp.reason}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Rejection Log (Required by Take-Home Specification) */}
      {statusData?.rejection_log && statusData.rejection_log.length > 0 && (
        <div className="p-5 rounded-2xl bg-amber-950/20 border border-amber-500/30 shadow-xl space-y-3">
          <div className="flex items-center gap-2 text-xs font-bold text-amber-300">
            <History className="w-4 h-4 text-amber-400" />
            <span>Rejection Log: What Failed, Why, and What Was Changed on Retry</span>
          </div>

          <div className="space-y-3">
            {statusData.rejection_log.map((rej, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-slate-900 border border-amber-500/30 text-xs space-y-2">
                <div className="flex items-center justify-between text-[11px] font-mono">
                  <span className="font-bold text-amber-400">Pass #{rej.iteration} Rejection</span>
                  <span className="text-slate-400">{new Date(rej.timestamp).toLocaleTimeString()}</span>
                </div>
                <div className="text-slate-300 whitespace-pre-line text-[11px] leading-relaxed">
                  {rej.changes_made_on_retry ? rej.changes_made_on_retry : (
                    <>
                      <p><strong className="text-rose-400">Failed Checkpoints:</strong> {rej.failed_checkpoints.join(', ')}</p>
                      <p className="mt-1"><strong className="text-amber-400">Evaluator Reason:</strong> {rej.critique}</p>
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Split Details: Score Meter & Real-Time Terminal Log */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Score & Iteration Status */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-6 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold text-slate-100 mb-1">Quality Assessment</h3>
            <p className="text-xs text-slate-400">Current evaluation score vs threshold</p>
          </div>

          <div className="flex justify-center py-2">
            <ScoreGauge
              score={statusData?.latest_score ?? 0}
              threshold={statusData?.quality_threshold ?? 80}
              size="lg"
            />
          </div>

          <div className="space-y-3 pt-4 border-t border-slate-800 text-xs">
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-400">Required Threshold:</span>
              <span className="font-mono font-bold text-slate-100">
                {statusData?.quality_threshold ?? 80.0}/100
              </span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-400">Remediation Retries:</span>
              <span className="font-mono font-bold text-slate-100">
                {statusData?.retry_count ?? 0} / {statusData?.max_retries ?? 2}
              </span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-400">Final Decision:</span>
              <span className={`font-mono font-bold ${
                statusData?.final_decision === 'APPROVED' ? 'text-emerald-400' : 'text-amber-400'
              }`}>
                {statusData?.final_decision || 'Evaluating...'}
              </span>
            </div>
          </div>
        </div>

        {/* Real-Time Terminal Logs */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col h-[520px]">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
            <div className="flex items-center gap-2">
              <Terminal className="w-4 h-4 text-indigo-400" />
              <h3 className="text-sm font-semibold text-slate-100 font-mono">Agent Reasoning & Event Stream</h3>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="text-[11px] font-mono text-slate-400">Active</span>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto space-y-3 font-mono text-xs pr-2">
            {statusData?.logs.map((log, idx) => {
              const isError = log.status === 'failed';
              const isWarning = log.status === 'warning';

              return (
                <div
                  key={idx}
                  className={`p-3 rounded-xl border transition-all ${
                    isError
                      ? 'bg-rose-950/20 border-rose-500/30 text-rose-300'
                      : isWarning
                      ? 'bg-amber-950/20 border-amber-500/30 text-amber-300'
                      : 'bg-slate-950/60 border-slate-800/80 text-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5 text-[10px] text-slate-500">
                    <div className="flex items-center gap-2">
                      <span className="px-1.5 py-0.5 rounded uppercase font-bold text-indigo-400 bg-indigo-950/50 border border-indigo-800/50">
                        {log.agent}
                      </span>
                      <span>{log.action}</span>
                    </div>
                    <span>{new Date(log.timestamp).toLocaleTimeString()}</span>
                  </div>

                  <p className="text-xs leading-relaxed text-slate-200 whitespace-pre-wrap">
                    {log.message}
                  </p>
                </div>
              );
            })}
            <div ref={logsEndRef} />
          </div>
        </div>
      </div>
    </div>
  );
};
