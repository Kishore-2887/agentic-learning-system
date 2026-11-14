import React from 'react';
import { Sparkles, Bot, CheckCircle2, PlusCircle } from 'lucide-react';
import { SettingsData } from '../types';

interface NavbarProps {
  settings: SettingsData | null;
  onNavigate: (view: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ settings, onNavigate }) => {
  const providerLabel = settings?.llm_provider
    ? settings.llm_provider.toUpperCase()
    : 'MOCK AI';

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800 bg-slate-900/90 backdrop-blur-md">
      <div className="flex h-16 items-center justify-between px-6">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 text-white shadow-lg shadow-indigo-500/25">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base font-bold tracking-tight text-white">
                LearnAgent <span className="text-indigo-400 font-mono text-xs">v1.0</span>
              </h1>
              <span className="hidden sm:inline-block px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-full">
                Autonomous Self-Evaluation
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">
              Multi-Agent Pedagogical Content Generation & Quality Assurance
            </p>
          </div>
        </div>

        {/* Right Info & Actions */}
        <div className="flex items-center gap-3">
          {/* Active Model Pill */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/80 text-xs text-slate-300">
            <Bot className="w-3.5 h-3.5 text-indigo-400" />
            <span className="text-slate-400">Engine:</span>
            <span className="font-semibold text-slate-200 font-mono">{providerLabel}</span>
          </div>

          {/* System Online Status */}
          <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-emerald-950/30 border border-emerald-500/30 text-emerald-400 text-xs font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Agent Graph Online</span>
          </div>

          {/* Create Button */}
          <button
            onClick={() => onNavigate('create')}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/20 transition-all"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Generate Content</span>
          </button>
        </div>
      </div>
    </header>
  );
};

