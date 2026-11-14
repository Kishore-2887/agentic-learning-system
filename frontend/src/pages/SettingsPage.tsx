import React, { useEffect, useState } from 'react';
import { SettingsData } from '../types';
import { fetchSettings, updateSettings } from '../services/api';
import {
  Settings as SettingsIcon,
  Bot,
  Sliders,
  Shield,
  Key,
  CheckCircle2,
  AlertCircle,
  Save
} from 'lucide-react';

interface SettingsPageProps {
  onSettingsUpdated: (data: SettingsData) => void;
}

export const SettingsPage: React.FC<SettingsPageProps> = ({ onSettingsUpdated }) => {
  const [settings, setSettings] = useState<SettingsData | null>(null);
  const [provider, setProvider] = useState('mock');
  const [openaiModel, setOpenaiModel] = useState('gpt-4o');
  const [geminiModel, setGeminiModel] = useState('gemini-1.5-pro');
  const [threshold, setThreshold] = useState(80);
  const [maxRetries, setMaxRetries] = useState(3);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchSettings();
        setSettings(data);
        setProvider(data.llm_provider);
        setOpenaiModel(data.openai_model);
        setGeminiModel(data.gemini_model);
        setThreshold(data.default_quality_threshold);
        setMaxRetries(data.max_improvement_attempts);
      } catch (err) {
        console.error('Failed to load settings:', err);
      }
    }
    load();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSaveSuccess(false);

    try {
      const updated = await updateSettings({
        llm_provider: provider,
        openai_model: openaiModel,
        gemini_model: geminiModel,
        default_quality_threshold: threshold,
        max_improvement_attempts: maxRetries
      });

      setSettings(updated);
      onSettingsUpdated(updated);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err: any) {
      setError(err.message || 'Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
          <SettingsIcon className="w-6 h-6 text-indigo-400" />
          AI Engine & Multi-Agent Quality Gate Settings
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Configure active model backends, self-evaluation thresholds, and autonomous retry boundaries.
        </p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {saveSuccess && (
          <div className="p-4 rounded-xl bg-emerald-950/30 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>Settings saved and applied successfully.</span>
          </div>
        )}

        {error && (
          <div className="p-4 rounded-xl bg-rose-950/30 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        {/* Provider Selection */}
        <div className="p-6 md:p-8 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-6">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
            <Bot className="w-5 h-5 text-indigo-400" />
            <h3 className="text-base font-semibold text-slate-100">AI Intelligence Provider</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Mock Provider */}
            <div
              onClick={() => setProvider('mock')}
              className={`p-5 rounded-xl border cursor-pointer transition-all ${
                provider === 'mock'
                  ? 'bg-indigo-950/40 border-indigo-500 ring-2 ring-indigo-500/30'
                  : 'bg-slate-850 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-slate-100">Mock AI Provider</span>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-emerald-500/10 text-emerald-400">
                  Ready (Offline)
                </span>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed mb-3">
                Built-in deterministic agentic simulation. Zero API costs, ideal for automated testing and offline demos.
              </p>
              <span className="text-[11px] font-mono text-indigo-400 font-semibold">
                Self-evaluation & remediation active
              </span>
            </div>

            {/* OpenAI */}
            <div
              onClick={() => setProvider('openai')}
              className={`p-5 rounded-xl border cursor-pointer transition-all ${
                provider === 'openai'
                  ? 'bg-indigo-950/40 border-indigo-500 ring-2 ring-indigo-500/30'
                  : 'bg-slate-850 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-slate-100">OpenAI API</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-semibold ${
                  settings?.openai_key_configured
                    ? 'bg-emerald-500/10 text-emerald-400'
                    : 'bg-amber-500/10 text-amber-400'
                }`}>
                  {settings?.openai_key_configured ? 'API Key Configured' : 'Needs Key'}
                </span>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed mb-3">
                Utilizes OpenAI GPT models (e.g. GPT-4o) with native JSON schema structured outputs.
              </p>
              <span className="text-[11px] font-mono text-indigo-400 font-semibold">
                Model: {openaiModel}
              </span>
            </div>

            {/* Google Gemini */}
            <div
              onClick={() => setProvider('google')}
              className={`p-5 rounded-xl border cursor-pointer transition-all ${
                provider === 'google'
                  ? 'bg-indigo-950/40 border-indigo-500 ring-2 ring-indigo-500/30'
                  : 'bg-slate-850 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-slate-100">Google Gemini API</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-semibold ${
                  settings?.gemini_key_configured
                    ? 'bg-emerald-500/10 text-emerald-400'
                    : 'bg-amber-500/10 text-amber-400'
                }`}>
                  {settings?.gemini_key_configured ? 'API Key Configured' : 'Needs Key'}
                </span>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed mb-3">
                Uses Google Gemini 1.5 Pro for multimodal reasoning and curriculum synthesis.
              </p>
              <span className="text-[11px] font-mono text-indigo-400 font-semibold">
                Model: {geminiModel}
              </span>
            </div>
          </div>
        </div>

        {/* Quality Gate Parameters */}
        <div className="p-6 md:p-8 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-6">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
            <Sliders className="w-5 h-5 text-indigo-400" />
            <h3 className="text-base font-semibold text-slate-100">Self-Evaluation Quality Gate Rules</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="space-y-3">
              <div className="flex justify-between items-center text-xs">
                <label className="font-semibold text-slate-200">
                  Minimum Passing Quality Threshold:
                </label>
                <span className="font-mono font-bold text-indigo-400 text-sm">
                  {threshold} / 100
                </span>
              </div>
              <input
                type="range"
                min="60"
                max="95"
                value={threshold}
                onChange={(e) => setThreshold(Number(e.target.value))}
                className="w-full accent-indigo-500"
              />
              <p className="text-[11px] text-slate-400 leading-relaxed">
                Default 80/100. Content scoring below this mark automatically routes to the Content Improvement Agent.
              </p>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between items-center text-xs">
                <label className="font-semibold text-slate-200">
                  Maximum Autonomous Remediation Retries:
                </label>
                <span className="font-mono font-bold text-indigo-400 text-sm">
                  {maxRetries} attempts
                </span>
              </div>
              <input
                type="range"
                min="1"
                max="5"
                value={maxRetries}
                onChange={(e) => setMaxRetries(Number(e.target.value))}
                className="w-full accent-indigo-500"
              />
              <p className="text-[11px] text-slate-400 leading-relaxed">
                Default 3. If content still fails after 3 passes, it is flagged for manual review rather than falsely approved.
              </p>
            </div>
          </div>
        </div>

        {/* Credentials Security Status */}
        <div className="p-6 md:p-8 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
            <Shield className="w-5 h-5 text-indigo-400" />
            <h3 className="text-base font-semibold text-slate-100">API Credentials & Security</h3>
          </div>

          <p className="text-xs text-slate-400 leading-relaxed">
            API keys are strictly managed on the server backend via the <code className="text-indigo-300 font-mono">.env</code> file.
            Keys are never exposed over API responses or client-side JavaScript.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
            <div className="p-3.5 rounded-xl bg-slate-850 border border-slate-800 flex items-center justify-between">
              <span className="text-slate-300">OPENAI_API_KEY</span>
              <span className={`px-2 py-0.5 rounded font-mono font-semibold text-[11px] ${
                settings?.openai_key_configured ? 'text-emerald-400 bg-emerald-950/40' : 'text-slate-500 bg-slate-800'
              }`}>
                {settings?.openai_key_configured ? 'LOADED IN BACKEND' : 'NOT SET'}
              </span>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-850 border border-slate-800 flex items-center justify-between">
              <span className="text-slate-300">GEMINI_API_KEY</span>
              <span className={`px-2 py-0.5 rounded font-mono font-semibold text-[11px] ${
                settings?.gemini_key_configured ? 'text-emerald-400 bg-emerald-950/40' : 'text-slate-500 bg-slate-800'
              }`}>
                {settings?.gemini_key_configured ? 'LOADED IN BACKEND' : 'NOT SET'}
              </span>
            </div>
          </div>
        </div>

        {/* Save CTA */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30 transition-all"
          >
            <Save className="w-4 h-4" />
            <span>{saving ? 'Updating Configuration...' : 'Save Configuration'}</span>
          </button>
        </div>
      </form>
    </div>
  );
};

