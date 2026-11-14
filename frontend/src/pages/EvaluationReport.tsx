import React, { useEffect, useState } from 'react';
import { EvaluationReport as EvalReportType, ContentListItem } from '../types';
import { fetchContentEvaluations, fetchContentList } from '../services/api';
import { ScoreGauge } from '../components/ScoreGauge';
import { DimensionChart } from '../components/DimensionChart';
import {
  BarChart3,
  CheckCircle2,
  AlertTriangle,
  FileQuestion,
  Lightbulb,
  ShieldAlert,
  History,
  Layers
} from 'lucide-react';

interface EvaluationReportProps {
  contentId?: string | null;
  onNavigate: (view: string, contentId?: string) => void;
}

export const EvaluationReport: React.FC<EvaluationReportProps> = ({ contentId, onNavigate }) => {
  const [items, setItems] = useState<ContentListItem[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(contentId || null);
  const [evaluations, setEvaluations] = useState<EvalReportType[]>([]);
  const [selectedIteration, setSelectedIteration] = useState<number>(1);
  const [loading, setLoading] = useState(true);
  const [chartType, setChartType] = useState<'bar' | 'radar'>('bar');

  useEffect(() => {
    async function loadInitial() {
      try {
        const list = await fetchContentList();
        setItems(list);
        if (!selectedId && list.length > 0) {
          setSelectedId(list[0].id);
        }
      } catch (err) {
        console.error('Failed to load content list for evaluation:', err);
      }
    }
    loadInitial();
  }, []);

  useEffect(() => {
    if (!selectedId) {
      setLoading(false);
      return;
    }

    async function loadEvals() {
      setLoading(true);
      try {
        const evals = await fetchContentEvaluations(selectedId!);
        setEvaluations(evals);
        if (evals.length > 0) {
          setSelectedIteration(evals[evals.length - 1].iteration);
        }
      } catch (err) {
        console.error('Failed to load evaluations:', err);
      } finally {
        setLoading(false);
      }
    }
    loadEvals();
  }, [selectedId]);

  const currentEval = evaluations.find(e => e.iteration === selectedIteration) || evaluations[0];

  return (
    <div className="space-y-6">
      {/* Top Header & Content Selector */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-indigo-400" />
            Independent Quality & Factual Evaluation Report
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Scrutinizing pedagogical rigor, dimensional rubrics, and source-verified claims
          </p>
        </div>

        {/* Content Item Selector Dropdown */}
        <div className="flex items-center gap-3">
          <label className="text-xs font-semibold text-slate-400">Curriculum Module:</label>
          <select
            value={selectedId || ''}
            onChange={(e) => setSelectedId(e.target.value)}
            className="px-3 py-2 rounded-xl bg-slate-850 border border-slate-700 text-slate-200 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {items.map((it) => (
              <option key={it.id} value={it.id}>
                {it.title} (v{it.version} - {it.status})
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-80">
          <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : !currentEval ? (
        <div className="p-12 text-center bg-slate-900 border border-slate-800 rounded-2xl">
          <p className="text-slate-400 text-sm">No evaluation report found for the selected module.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Iteration Selector Pill Bar (If Multi-Iteration Refinement Occurred) */}
          {evaluations.length > 1 && (
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs text-slate-300">
                <History className="w-4 h-4 text-indigo-400" />
                <span>Multi-Pass Self-Evaluation Progression:</span>
              </div>
              <div className="flex items-center gap-2">
                {evaluations.map((ev) => (
                  <button
                    key={ev.iteration}
                    onClick={() => setSelectedIteration(ev.iteration)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
                      selectedIteration === ev.iteration
                        ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                        : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    Iteration {ev.iteration}: {ev.overall_score.toFixed(1)}/100
                    {ev.passed ? ' (PASSED)' : ' (FAILED)'}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Core Score & Dimension Overview */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Score Card */}
            <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col justify-between items-center text-center">
              <div>
                <span className="text-[11px] font-mono uppercase tracking-wider text-slate-500 block mb-1">
                  Iteration #{currentEval.iteration} Evaluation
                </span>
                <h3 className="text-base font-bold text-slate-100">Overall Quality Score</h3>
              </div>

              <div className="py-6">
                <ScoreGauge score={currentEval.overall_score} threshold={80} size="lg" />
              </div>

              <div className="w-full pt-4 border-t border-slate-800 text-xs text-slate-400 flex items-center justify-between">
                <span>Threshold: 80.0 / 100</span>
                <span className={`font-semibold ${currentEval.passed ? 'text-emerald-400' : 'text-amber-400'}`}>
                  {currentEval.passed ? 'PASSED QUALITY GATE' : 'FAILED - REMEDIATED'}
                </span>
              </div>
            </div>

            {/* Dimension Breakdown Chart */}
            <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div>
                  <h3 className="text-sm font-semibold text-slate-100">Dimensional Scoring Matrix</h3>
                  <p className="text-xs text-slate-400">Strictly weighted evaluation formula</p>
                </div>

                <div className="flex bg-slate-800 p-1 rounded-lg border border-slate-700">
                  <button
                    onClick={() => setChartType('bar')}
                    className={`px-2.5 py-1 text-xs font-medium rounded ${chartType === 'bar' ? 'bg-indigo-600 text-white' : 'text-slate-400'}`}
                  >
                    Bar Chart
                  </button>
                  <button
                    onClick={() => setChartType('radar')}
                    className={`px-2.5 py-1 text-xs font-medium rounded ${chartType === 'radar' ? 'bg-indigo-600 text-white' : 'text-slate-400'}`}
                  >
                    Radar Chart
                  </button>
                </div>
              </div>

              <DimensionChart
                data={{
                  factual_accuracy: currentEval.factual_accuracy,
                  relevance: currentEval.relevance,
                  completeness: currentEval.completeness,
                  clarity_readability: currentEval.clarity_readability,
                  educational_effectiveness: currentEval.educational_effectiveness,
                  structure_organization: currentEval.structure_organization,
                }}
                chartType={chartType}
              />
            </div>
          </div>

          {/* Identified Errors & Unsupported Claims */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Identified Flaws / Weaknesses */}
            <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
              <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
                <AlertTriangle className="w-5 h-5 text-amber-400" />
                <h3 className="text-sm font-semibold text-slate-100">
                  Identified Weaknesses & Errors ({currentEval.identified_errors.length})
                </h3>
              </div>

              {currentEval.identified_errors.length === 0 ? (
                <div className="p-6 text-center text-xs text-emerald-400 bg-emerald-950/20 border border-emerald-500/20 rounded-xl flex items-center justify-center gap-2">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>No critical or moderate factual errors detected in this pass.</span>
                </div>
              ) : (
                <div className="space-y-3">
                  {currentEval.identified_errors.map((err, i) => (
                    <div key={i} className="p-3.5 rounded-xl bg-slate-850 border border-slate-800 text-xs space-y-1.5">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-slate-200">{err.section}</span>
                        <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase ${
                          err.severity === 'critical'
                            ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                            : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                        }`}>
                          {err.severity}
                        </span>
                      </div>
                      <p className="text-slate-300 leading-relaxed text-[11px]">{err.description}</p>
                      {err.unsupported_claim && (
                        <div className="inline-flex items-center gap-1 text-[10px] text-rose-400 font-semibold mt-1">
                          <ShieldAlert className="w-3 h-3" /> Flagged Unsupported Claim
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Missing Pedagogical Concepts */}
            <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
              <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
                <FileQuestion className="w-5 h-5 text-indigo-400" />
                <h3 className="text-sm font-semibold text-slate-100">
                  Missing Concepts ({currentEval.missing_concepts.length})
                </h3>
              </div>

              {currentEval.missing_concepts.length === 0 ? (
                <div className="p-6 text-center text-xs text-emerald-400 bg-emerald-950/20 border border-emerald-500/20 rounded-xl flex items-center justify-center gap-2">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Curriculum scope is comprehensive for the target education level.</span>
                </div>
              ) : (
                <ul className="space-y-2 text-xs">
                  {currentEval.missing_concepts.map((concept, i) => (
                    <li key={i} className="flex items-start gap-2 p-3 rounded-lg bg-slate-850 border border-slate-800 text-slate-300">
                      <span className="text-indigo-400 font-bold">•</span>
                      <span>{concept}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>

          {/* Actionable Improvement Recommendations */}
          <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
            <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
              <Lightbulb className="w-5 h-5 text-indigo-400" />
              <h3 className="text-sm font-semibold text-slate-100">
                Actionable Remediation Recommendations
              </h3>
            </div>

            <div className="space-y-2">
              {currentEval.improvement_recommendations.map((rec, i) => (
                <div key={i} className="flex items-start gap-3 p-3.5 rounded-xl bg-slate-850 border border-slate-800 text-xs text-slate-300">
                  <span className="w-5 h-5 rounded-full bg-indigo-600/20 text-indigo-400 flex items-center justify-center text-[10px] font-bold shrink-0">
                    {i + 1}
                  </span>
                  <span className="leading-relaxed">{rec}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

