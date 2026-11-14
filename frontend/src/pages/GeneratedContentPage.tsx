import React, { useEffect, useState } from 'react';
import { ContentListItem, ContentDetail, RevisionHistory } from '../types';
import { fetchContentList, fetchContentDetail, fetchContentHistory } from '../services/api';
import { ContentViewer } from '../components/ContentViewer';
import {
  BookOpen,
  Search,
  History,
  FileCheck2,
  AlertTriangle,
  ArrowRight,
  TrendingUp,
  Layers
} from 'lucide-react';

interface GeneratedContentPageProps {
  initialContentId?: string | null;
  onNavigate: (view: string, contentId?: string) => void;
}

export const GeneratedContentPage: React.FC<GeneratedContentPageProps> = ({
  initialContentId,
  onNavigate
}) => {
  const [contentList, setContentList] = useState<ContentListItem[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(initialContentId || null);
  const [detail, setDetail] = useState<ContentDetail | null>(null);
  const [history, setHistory] = useState<RevisionHistory[]>([]);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    async function loadList() {
      try {
        const items = await fetchContentList();
        setContentList(items);
        if (!selectedId && items.length > 0) {
          setSelectedId(items[0].id);
        }
      } catch (err) {
        console.error('Failed to load content list:', err);
      } finally {
        setLoading(false);
      }
    }
    loadList();
  }, []);

  useEffect(() => {
    if (!selectedId) return;

    async function loadDetail() {
      setDetailLoading(true);
      try {
        const [det, hist] = await Promise.all([
          fetchContentDetail(selectedId!),
          fetchContentHistory(selectedId!)
        ]);
        setDetail(det);
        setHistory(hist);
      } catch (err) {
        console.error('Failed to load content detail:', err);
      } finally {
        setDetailLoading(false);
      }
    }
    loadDetail();
  }, [selectedId]);

  const filteredItems = contentList.filter((item) => {
    const matchesSearch = item.title.toLowerCase().includes(search.toLowerCase()) ||
                          item.topic.toLowerCase().includes(search.toLowerCase());
    const matchesStatus = statusFilter === 'all' || item.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6">
      {/* Top Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-indigo-400" />
            Generated Educational Curricula Library
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Browse, inspect, and export verified educational materials and revision histories
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search topics or titles..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9 pr-3 py-1.5 rounded-xl bg-slate-850 border border-slate-700 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          {/* Status Tabs */}
          <div className="flex bg-slate-850 p-1 rounded-xl border border-slate-700 text-xs">
            {['all', 'approved', 'manual_review'].map((st) => (
              <button
                key={st}
                onClick={() => setStatusFilter(st)}
                className={`px-3 py-1 rounded-lg font-medium transition-colors ${
                  statusFilter === st ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {st === 'all' ? 'All' : st === 'approved' ? 'Approved' : 'Manual Review'}
              </button>
            ))}
          </div>

          {/* Revision History Toggle */}
          <button
            onClick={() => setShowHistory(!showHistory)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-semibold transition-colors ${
              showHistory
                ? 'bg-indigo-600 text-white border-indigo-500'
                : 'bg-slate-800 text-slate-300 border-slate-700 hover:text-white'
            }`}
          >
            <History className="w-4 h-4" />
            <span>Revision History ({history.length})</span>
          </button>
        </div>
      </div>

      {/* Main Split Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Side Content List */}
        <div className="lg:col-span-4 space-y-3">
          <div className="text-xs font-semibold text-slate-400 px-1 font-mono uppercase">
            Curriculum Modules ({filteredItems.length})
          </div>

          <div className="space-y-2 max-h-[780px] overflow-y-auto pr-1">
            {filteredItems.map((item) => {
              const isSelected = item.id === selectedId;

              return (
                <div
                  key={item.id}
                  onClick={() => setSelectedId(item.id)}
                  className={`p-4 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-indigo-950/40 border-indigo-500 shadow-md ring-1 ring-indigo-500/30'
                      : 'bg-slate-900 border-slate-800 hover:bg-slate-850 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                      v{item.version}
                    </span>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider ${
                      item.status === 'approved'
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                    }`}>
                      {item.status}
                    </span>
                  </div>

                  <h4 className="text-sm font-semibold text-slate-100 line-clamp-1 mb-1">
                    {item.title}
                  </h4>
                  <p className="text-xs text-slate-400 line-clamp-1 mb-3">
                    {item.topic}
                  </p>

                  <div className="flex items-center justify-between text-[11px] pt-2 border-t border-slate-800/80 text-slate-400">
                    <span>{item.education_level}</span>
                    {item.overall_score !== null && item.overall_score !== undefined && (
                      <span className={`font-mono font-bold ${item.overall_score >= 80 ? 'text-emerald-400' : 'text-amber-400'}`}>
                        {item.overall_score.toFixed(1)}/100
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Main Viewer */}
        <div className="lg:col-span-8 space-y-6">
          {showHistory && (
            <div className="p-6 rounded-2xl bg-slate-900 border border-indigo-500/40 shadow-xl space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  <History className="w-5 h-5 text-indigo-400" />
                  <h3 className="text-sm font-semibold text-slate-100">
                    Self-Evaluation & Remediation Revision Log
                  </h3>
                </div>
                <button
                  onClick={() => setShowHistory(false)}
                  className="text-xs text-slate-400 hover:text-slate-200"
                >
                  Dismiss
                </button>
              </div>

              {history.length === 0 ? (
                <p className="text-xs text-slate-400 py-3">
                  This curriculum satisfied all quality criteria on initial generation without requiring remediation.
                </p>
              ) : (
                <div className="space-y-3">
                  {history.map((rev) => (
                    <div key={rev.id} className="p-4 rounded-xl bg-slate-850 border border-slate-800 text-xs space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-indigo-300">Pass #{rev.iteration} Remediation</span>
                        <div className="flex items-center gap-2 font-mono text-[11px]">
                          <span className="text-rose-400">{rev.previous_score.toFixed(1)}/100</span>
                          <span>→</span>
                          <span className="text-emerald-400 font-bold">{rev.new_score.toFixed(1)}/100</span>
                        </div>
                      </div>

                      <p className="text-slate-300 leading-relaxed text-[11px] whitespace-pre-line">
                        {rev.changes_summary}
                      </p>

                      {rev.modified_sections && rev.modified_sections.length > 0 && (
                        <div className="pt-2 flex flex-wrap gap-1.5">
                          <span className="text-slate-500 text-[10px]">Modified:</span>
                          {rev.modified_sections.map((sec, sIdx) => (
                            <span key={sIdx} className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-mono">
                              {sec}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {detailLoading ? (
            <div className="flex items-center justify-center h-96 bg-slate-900 border border-slate-800 rounded-2xl">
              <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
          ) : detail ? (
            <ContentViewer
              content={detail.raw_json}
              markdownText={detail.markdown_text}
              version={detail.version}
              status={detail.status}
            />
          ) : (
            <div className="p-12 text-center bg-slate-900 border border-slate-800 rounded-2xl">
              <p className="text-slate-400 text-sm">Select a curriculum module from the left list to view.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

