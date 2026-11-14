import React, { useState, useEffect, Component, ErrorInfo, ReactNode } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { CreateContent } from './pages/CreateContent';
import { LiveWorkflow } from './pages/LiveWorkflow';
import { EvaluationReport } from './pages/EvaluationReport';
import { GeneratedContentPage } from './pages/GeneratedContentPage';
import { SettingsPage } from './pages/SettingsPage';
import { SettingsData } from './types';
import { fetchSettings } from './services/api';

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center p-6">
          <div className="max-w-md p-6 bg-slate-900 border border-rose-500/40 rounded-2xl text-center space-y-4">
            <h2 className="text-lg font-bold text-rose-400">Application Rendering Notice</h2>
            <p className="text-xs text-slate-300 leading-relaxed">
              {this.state.error?.message || 'An unexpected rendering error occurred.'}
            </p>
            <button
              onClick={() => {
                this.setState({ hasError: false, error: null });
                window.location.reload();
              }}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-xl"
            >
              Reload Application
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

export const App: React.FC = () => {
  const [currentView, setCurrentView] = useState('dashboard');
  const [activeWorkflowId, setActiveWorkflowId] = useState<string | null>(null);
  const [selectedContentId, setSelectedContentId] = useState<string | null>(null);
  const [settings, setSettings] = useState<SettingsData | null>(null);

  useEffect(() => {
    async function loadSettings() {
      try {
        const s = await fetchSettings();
        setSettings(s);
      } catch (err) {
        console.error('Failed to load initial settings:', err);
      }
    }
    loadSettings();
  }, []);

  const handleNavigate = (view: string, contentId?: string, workflowId?: string) => {
    if (contentId) setSelectedContentId(contentId);
    if (workflowId) setActiveWorkflowId(workflowId);
    setCurrentView(view);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleWorkflowStarted = (requestId: string) => {
    setActiveWorkflowId(requestId);
    setCurrentView('workflow');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
        {/* Top Navbar */}
        <Navbar settings={settings} onNavigate={handleNavigate} />

        {/* Main Body */}
        <div className="flex-1 flex overflow-hidden">
          {/* Sidebar */}
          <Sidebar
            currentView={currentView}
            onNavigate={(view) => handleNavigate(view)}
            activeWorkflowId={activeWorkflowId}
          />

          {/* View Port */}
          <main className="flex-1 overflow-y-auto p-6 md:p-8">
            <div className="max-w-7xl mx-auto">
              {currentView === 'dashboard' && (
                <Dashboard onNavigate={handleNavigate} />
              )}

              {currentView === 'create' && (
                <CreateContent onWorkflowStarted={handleWorkflowStarted} />
              )}

              {currentView === 'workflow' && (
                <LiveWorkflow
                  requestId={activeWorkflowId}
                  onNavigate={handleNavigate}
                />
              )}

              {currentView === 'evaluation' && (
                <EvaluationReport
                  contentId={selectedContentId}
                  onNavigate={handleNavigate}
                />
              )}

              {currentView === 'content' && (
                <GeneratedContentPage
                  initialContentId={selectedContentId}
                  onNavigate={handleNavigate}
                />
              )}

              {currentView === 'settings' && (
                <SettingsPage
                  onSettingsUpdated={(newSettings) => setSettings(newSettings)}
                />
              )}
            </div>
          </main>
        </div>
      </div>
    </ErrorBoundary>
  );
};

export default App;
