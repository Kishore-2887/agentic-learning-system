import React, { useState } from 'react';
import { generateContent } from '../services/api';
import {
  Sparkles,
  Plus,
  Trash2,
  Sliders,
  BookOpen,
  ArrowRight,
  Info,
  Bug,
  CheckCircle2,
  GraduationCap
} from 'lucide-react';

interface CreateContentProps {
  onWorkflowStarted: (requestId: string) => void;
}

export const CreateContent: React.FC<CreateContentProps> = ({ onWorkflowStarted }) => {
  const [topic, setTopic] = useState('Introduction to RAG (Retrieval-Augmented Generation)');
  const [targetAudience, setTargetAudience] = useState(
    '12th-grade graduate from India, limited English vocabulary, non-English-medium background, wants to kickstart an AI career'
  );
  const [educationLevel, setEducationLevel] = useState('12th Grade Pass (Zero AI Background)');
  const [contentType, setContentType] = useState('lesson');
  const [objectives, setObjectives] = useState<string[]>([
    'Understand why regular AI hallucinates or has outdated knowledge',
    'Explain RAG using the simple Open-Book vs Closed-Book Exam analogy',
    'Trace the 3 steps: Retrieve (Search), Augment (Attach notes), Generate (Write answer)',
    'Understand why RAG is the #1 job-ready skill for starting an AI career in India'
  ]);
  const [newObjective, setNewObjective] = useState('');
  const [qualityThreshold, setQualityThreshold] = useState<number>(80);
  const [maxRetries, setMaxRetries] = useState<number>(2);
  const [injectDeliberateFlaw, setInjectDeliberateFlaw] = useState(true);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const presets = [
    {
      title: '🎯 Submission Topic: Introduction to RAG',
      badge: 'Official Assessment',
      topic: 'Introduction to RAG (Retrieval-Augmented Generation)',
      audience: '12th-grade graduate from India, limited English vocabulary, non-English-medium background, wants to kickstart an AI career',
      level: '12th Grade Pass (Zero AI Background)',
      type: 'lesson',
      objectives: [
        'Understand why regular AI hallucinates or has outdated knowledge',
        'Explain RAG using the simple Open-Book vs Closed-Book Exam analogy',
        'Trace the 3 steps: Retrieve (Search), Augment (Attach notes), Generate (Write answer)',
        'Understand why RAG is the #1 job-ready skill for starting an AI career in India'
      ]
    },
    {
      title: 'Fine-Tuning vs RAG: When to Use What?',
      badge: 'Advanced Analogy',
      topic: 'Fine-Tuning vs RAG: When to Teach AI vs When to Give it Notes',
      audience: '12th-grade pass student transitioning into Junior AI Engineer role',
      level: 'Beginner / Intermediate',
      type: 'tutorial',
      objectives: [
        'Compare studying medicine for 5 years (Fine-Tuning) vs reading a patient report (RAG)',
        'Understand cost and GPU differences',
        'Identify which companies need RAG vs Fine-Tuning'
      ]
    },
    {
      title: 'What are Vector Embeddings? (The Library Analogy)',
      badge: 'Foundations',
      topic: 'What are Vector Embeddings? Searching by Meaning, Not Just Keywords',
      audience: 'Non-English medium 12th graduate starting AI from zero',
      level: 'Beginner',
      type: 'lesson',
      objectives: [
        'Understand keyword search vs semantic meaning search',
        'Explain embeddings using grocery store and library shelf analogies',
        'See how computers calculate similarity between sentences'
      ]
    }
  ];

  const handleApplyPreset = (p: typeof presets[0]) => {
    setTopic(p.topic);
    setTargetAudience(p.audience);
    setEducationLevel(p.level);
    setContentType(p.type);
    setObjectives(p.objectives);
  };

  const handleAddObjective = () => {
    if (newObjective.trim()) {
      setObjectives([...objectives, newObjective.trim()]);
      setNewObjective('');
    }
  };

  const handleRemoveObjective = (index: number) => {
    setObjectives(objectives.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim() || !targetAudience.trim()) {
      setError('Please provide both a topic and target audience.');
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const response = await generateContent({
        topic: topic.trim(),
        target_audience: targetAudience.trim(),
        education_level: educationLevel,
        learning_objectives: objectives,
        content_type: contentType,
        quality_threshold: qualityThreshold,
        max_retries: maxRetries
      });

      onWorkflowStarted(response.request_id);
    } catch (err: any) {
      setError(err.message || 'An error occurred while launching the agent workflow.');
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 mb-2">
          <GraduationCap className="w-4 h-4" />
          <span>GenAI Engineer Take-Home Assessment Specification</span>
        </div>
        <h2 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
          <BookOpen className="w-6 h-6 text-indigo-400" />
          Self-Evaluating Lesson Content Generator
        </h2>
        <p className="text-sm text-slate-400 mt-1 leading-relaxed">
          Tailored for: <strong className="text-slate-200">12th-grade graduate from India, limited English vocabulary, non-English-medium background, starting from zero</strong>.
          The multi-agent loop evaluates against a 6-checkpoint hard pass/fail rubric, rejects weaknesses, and auto-remediates.
        </p>
      </div>

      {/* Target Assessment Topic Preset */}
      <div className="space-y-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 font-mono">
          Assessment Presets
        </span>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {presets.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleApplyPreset(preset)}
              className={`text-left p-3.5 rounded-xl border transition-all group ${
                topic === preset.topic
                  ? 'bg-indigo-950/40 border-indigo-500 ring-1 ring-indigo-500/30'
                  : 'bg-slate-900 border-slate-800 hover:border-indigo-500/60 hover:bg-slate-850'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-slate-200 group-hover:text-indigo-300">
                  {preset.title}
                </span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
                  {preset.badge}
                </span>
              </div>
              <span className="text-[11px] text-slate-400 line-clamp-2">
                Audience: 12th-grade Indian student • {preset.type}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Video Demo Feature Callout */}
      <div className="p-4 rounded-xl bg-gradient-to-r from-amber-950/40 to-slate-900 border border-amber-500/30 flex items-start justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-xs font-bold text-amber-300">
            <Bug className="w-4 h-4 text-amber-400" />
            <span>Loom Video Requirement: Evaluator Catching Deliberate Error</span>
          </div>
          <p className="text-xs text-amber-200/80 leading-relaxed max-w-2xl">
            In Draft 1, the Generator deliberately includes a factual misconception (stating RAG retrains model weights) and dense jargon.
            The Evaluator will strictly catch and reject it with <strong className="text-amber-300 font-mono">FAIL checkpoints</strong>, and the Content Improver will remediate it in Pass 2!
          </p>
        </div>

        <div className="flex items-center gap-2 shrink-0 pt-1">
          <label className="text-xs text-slate-300 font-medium">Inject Demo Flaw:</label>
          <input
            type="checkbox"
            checked={injectDeliberateFlaw}
            onChange={(e) => setInjectDeliberateFlaw(e.target.checked)}
            className="w-4 h-4 accent-amber-500 rounded cursor-pointer"
          />
        </div>
      </div>

      {/* Main Generation Form */}
      <form onSubmit={handleSubmit} className="p-6 md:p-8 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-6">
        {error && (
          <div className="p-4 rounded-xl bg-rose-950/30 border border-rose-500/30 text-rose-300 text-xs">
            {error}
          </div>
        )}

        {/* Topic */}
        <div className="space-y-2">
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300">
            Topic for Submission <span className="text-indigo-400">*</span>
          </label>
          <input
            type="text"
            required
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="w-full px-4 py-3 rounded-xl bg-slate-850 border border-slate-700/80 text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        {/* Target Audience & Education Level */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300">
              Specific Target Audience <span className="text-indigo-400">*</span>
            </label>
            <input
              type="text"
              required
              value={targetAudience}
              onChange={(e) => setTargetAudience(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-slate-850 border border-slate-700/80 text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div className="space-y-2">
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300">
              Education Level
            </label>
            <input
              type="text"
              value={educationLevel}
              onChange={(e) => setEducationLevel(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-slate-850 border border-slate-700/80 text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        {/* Learning Objectives */}
        <div className="space-y-3">
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300">
            Learning Objectives (Beginner-Friendly Pedagogical Flow)
          </label>
          <div className="space-y-2">
            {objectives.map((obj, i) => (
              <div key={i} className="flex items-center justify-between p-2.5 rounded-lg bg-slate-850 border border-slate-800 text-xs text-slate-200">
                <span className="flex-1 mr-2">• {obj}</span>
                <button
                  type="button"
                  onClick={() => handleRemoveObjective(i)}
                  className="text-slate-500 hover:text-rose-400 transition-colors p-1"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>

          <div className="flex gap-2">
            <input
              type="text"
              value={newObjective}
              onChange={(e) => setNewObjective(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleAddObjective(); } }}
              placeholder="Add another objective..."
              className="flex-1 px-3 py-2 rounded-lg bg-slate-850 border border-slate-800 text-slate-200 text-xs focus:outline-none focus:border-indigo-500"
            />
            <button
              type="button"
              onClick={handleAddObjective}
              className="flex items-center gap-1 px-3 py-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white text-xs font-medium border border-slate-700"
            >
              <Plus className="w-3.5 h-3.5" /> Add
            </button>
          </div>
        </div>

        {/* Advanced Settings */}
        <div className="pt-2 border-t border-slate-800">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center gap-2 text-xs font-medium text-slate-400 hover:text-slate-200"
          >
            <Sliders className="w-3.5 h-3.5 text-indigo-400" />
            <span>{showAdvanced ? 'Hide Rubric & Loop Controls' : 'Show Rubric & Loop Controls'}</span>
          </button>

          {showAdvanced && (
            <div className="mt-4 p-4 rounded-xl bg-slate-850/60 border border-slate-800 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-300 font-medium">Quality Gate Score Threshold:</span>
                  <span className="font-mono font-bold text-indigo-400">{qualityThreshold}/100</span>
                </div>
                <input
                  type="range"
                  min="70"
                  max="90"
                  value={qualityThreshold}
                  onChange={(e) => setQualityThreshold(Number(e.target.value))}
                  className="w-full accent-indigo-500"
                />
                <span className="text-[11px] text-slate-500 block">
                  Must pass all 6 hard checkpoints and score ≥ 80 to ship.
                </span>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-300 font-medium">Max Loop Retries:</span>
                  <span className="font-mono font-bold text-indigo-400">{maxRetries} (as per rubric)</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="3"
                  value={maxRetries}
                  onChange={(e) => setMaxRetries(Number(e.target.value))}
                  className="w-full accent-indigo-500"
                />
                <span className="text-[11px] text-slate-500 block">
                  Guarantees the loop always terminates (1–2 retries max).
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Submit */}
        <div className="pt-4 flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <Info className="w-4 h-4 text-indigo-400" />
            <span>Autonomous generate → evaluate → regenerate loop</span>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-sm font-semibold shadow-lg shadow-indigo-600/30 transition-all"
          >
            {submitting ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Orchestrating Agents...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Run Agentic Workflow</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
