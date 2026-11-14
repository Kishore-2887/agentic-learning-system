import React from 'react';
import {
  LayoutDashboard,
  PlusCircle,
  GitFork,
  BarChart3,
  BookOpen,
  Settings,
  ShieldCheck
} from 'lucide-react';

interface SidebarProps {
  currentView: string;
  onNavigate: (view: string) => void;
  activeWorkflowId?: string | null;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentView, onNavigate, activeWorkflowId }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'create', label: 'Create Content', icon: PlusCircle },
    {
      id: 'workflow',
      label: 'Live Agent Workflow',
      icon: GitFork,
      badge: activeWorkflowId ? 'Active' : undefined
    },
    { id: 'evaluation', label: 'Evaluation Report', icon: BarChart3 },
    { id: 'content', label: 'Generated Content', icon: BookOpen },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/60 p-4 flex flex-col justify-between shrink-0">
      <div className="space-y-6">
        <div className="px-3">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 font-mono">
            Navigation
          </span>
        </div>

        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentView === item.id;

            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/25'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-850'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>

                {item.badge && (
                  <span className="px-1.5 py-0.5 text-[10px] font-mono rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 animate-pulse">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Agent Workflow Trust Guarantee Badge */}
      <div className="p-3.5 rounded-xl bg-slate-850/80 border border-slate-800 text-[11px] space-y-2">
        <div className="flex items-center gap-2 text-indigo-400 font-semibold">
          <ShieldCheck className="w-4 h-4 text-indigo-400 shrink-0" />
          <span>Independent Quality Gate</span>
        </div>
        <p className="text-slate-400 leading-relaxed text-[11px]">
          Content is guaranteed to undergo factual auditing and only publishes when passing the 80/100 threshold.
        </p>
      </div>
    </aside>
  );
};

