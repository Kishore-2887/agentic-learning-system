import React, { useState } from 'react';
import { EducationalContent } from '../types';
import {
  Download,
  Copy,
  Printer,
  Check,
  BookOpen,
  FileCode,
  FileText,
  Lightbulb,
  CheckCircle,
  HelpCircle,
  ChevronDown,
  ChevronUp
} from 'lucide-react';

interface ContentViewerProps {
  content: EducationalContent;
  markdownText: string;
  version?: number;
  status?: string;
}

export const ContentViewer: React.FC<ContentViewerProps> = ({
  content,
  markdownText,
  version = 1,
  status = 'approved'
}) => {
  const [activeTab, setActiveTab] = useState<'formatted' | 'markdown' | 'json'>('formatted');
  const [copied, setCopied] = useState(false);
  const [revealedAnswers, setRevealedAnswers] = useState<Record<number, boolean>>({});

  const handleCopy = () => {
    navigator.clipboard.writeText(markdownText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([markdownText], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${content.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-v${version}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handlePrint = () => {
    window.print();
  };

  const toggleAnswer = (idx: number) => {
    setRevealedAnswers(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
      {/* Top Header & Toolbar */}
      <div className="p-5 border-b border-slate-800 flex flex-wrap items-center justify-between gap-4 bg-slate-900/80 backdrop-blur-sm">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2 py-0.5 text-xs font-mono font-semibold rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              Revision v{version}
            </span>
            <span className={`px-2 py-0.5 text-xs font-semibold rounded ${
              status === 'approved'
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
            }`}>
              {status.toUpperCase()}
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-100">{content.title}</h2>
        </div>

        {/* View Switcher & Export Actions */}
        <div className="flex items-center gap-2">
          <div className="flex bg-slate-800 p-1 rounded-lg border border-slate-700">
            <button
              onClick={() => setActiveTab('formatted')}
              className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                activeTab === 'formatted' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5" /> Reader View
            </button>
            <button
              onClick={() => setActiveTab('markdown')}
              className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                activeTab === 'markdown' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <FileText className="w-3.5 h-3.5" /> Markdown
            </button>
            <button
              onClick={() => setActiveTab('json')}
              className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                activeTab === 'json' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <FileCode className="w-3.5 h-3.5" /> Raw JSON
            </button>
          </div>

          <div className="flex items-center gap-1 border-l border-slate-800 pl-2">
            <button
              onClick={handleCopy}
              title="Copy Markdown"
              className="p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-colors"
            >
              {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
            </button>
            <button
              onClick={handleDownload}
              title="Download .md"
              className="p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-colors"
            >
              <Download className="w-4 h-4" />
            </button>
            <button
              onClick={handlePrint}
              title="Print / Save PDF"
              className="p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-colors"
            >
              <Printer className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="p-6 md:p-8">
        {activeTab === 'formatted' && (
          <div className="max-w-4xl mx-auto space-y-8 print:text-black">
            {/* Metadata Card */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 p-4 rounded-xl bg-slate-850 border border-slate-800 text-xs">
              <div>
                <span className="text-slate-400 block mb-0.5">Target Audience:</span>
                <span className="font-semibold text-slate-200">{content.target_audience}</span>
              </div>
              <div>
                <span className="text-slate-400 block mb-0.5">Education Level:</span>
                <span className="font-semibold text-slate-200">{content.education_level}</span>
              </div>
              <div>
                <span className="text-slate-400 block mb-0.5">Key Focus Area:</span>
                <span className="font-semibold text-slate-200">{content.topic}</span>
              </div>
            </div>

            {/* Executive Summary */}
            <div className="space-y-3">
              <h3 className="text-sm font-semibold uppercase tracking-wider text-indigo-400">Executive Summary</h3>
              <p className="text-slate-300 leading-relaxed text-base bg-slate-850/50 p-4 rounded-xl border border-slate-800/80">
                {content.summary}
              </p>
            </div>

            {/* Key Concepts Badges */}
            <div className="space-y-2">
              <h3 className="text-sm font-semibold uppercase tracking-wider text-indigo-400">Core Concepts</h3>
              <div className="flex flex-wrap gap-2">
                {content.key_concepts.map((concept, i) => (
                  <span
                    key={i}
                    className="px-3 py-1 rounded-lg text-xs font-mono bg-indigo-950/40 text-indigo-300 border border-indigo-800/50"
                  >
                    {concept}
                  </span>
                ))}
              </div>
            </div>

            <hr className="border-slate-800" />

            {/* Instructional Sections */}
            <div className="space-y-8">
              {content.sections.map((section, idx) => (
                <article key={idx} className="space-y-4">
                  <h3 className="text-xl font-bold text-slate-100 flex items-center gap-3">
                    <span className="flex items-center justify-center w-7 h-7 rounded-lg bg-indigo-600/20 text-indigo-400 text-sm font-mono font-bold">
                      {idx + 1}
                    </span>
                    {section.title}
                  </h3>

                  <p className="text-slate-300 leading-relaxed text-base pl-10 whitespace-pre-line">
                    {section.explanation}
                  </p>

                  {/* Callout Box */}
                  {section.callout_note && (
                    <div className="ml-10 p-4 rounded-xl bg-blue-950/30 border border-blue-500/30 flex items-start gap-3">
                      <Lightbulb className="w-5 h-5 text-blue-400 shrink-0 mt-0.5" />
                      <p className="text-xs text-blue-200 leading-relaxed">
                        <strong className="font-semibold block text-blue-300 mb-0.5">Instructor Callout:</strong>
                        {section.callout_note}
                      </p>
                    </div>
                  )}

                  {/* Examples */}
                  {section.examples && section.examples.length > 0 && (
                    <div className="ml-10 space-y-2">
                      <h5 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                        Illustrative Examples & Case Studies
                      </h5>
                      <div className="space-y-2">
                        {section.examples.map((ex, exIdx) => (
                          <div
                            key={exIdx}
                            className="p-3 rounded-lg bg-slate-850 border border-slate-800 text-xs text-slate-300 leading-relaxed"
                          >
                            {ex}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Key Terms */}
                  {section.key_terms && section.key_terms.length > 0 && (
                    <div className="ml-10 flex items-center gap-2 text-xs text-slate-400">
                      <span className="font-medium">Key Terms:</span>
                      {section.key_terms.map((term, tIdx) => (
                        <span key={tIdx} className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[11px]">
                          {term}
                        </span>
                      ))}
                    </div>
                  )}
                </article>
              ))}
            </div>

            <hr className="border-slate-800" />

            {/* Practice Questions */}
            {content.practice_questions && content.practice_questions.length > 0 && (
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <HelpCircle className="w-5 h-5 text-indigo-400" />
                  <h3 className="text-lg font-bold text-slate-100">Practice & Mastery Assessment</h3>
                </div>

                <div className="space-y-3">
                  {content.practice_questions.map((q, idx) => (
                    <div key={idx} className="p-5 rounded-xl bg-slate-850 border border-slate-800 space-y-3">
                      <p className="text-sm font-semibold text-slate-200">
                        Q{idx + 1}. {q.question}
                      </p>

                      {q.options && (
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                          {q.options.map((opt, oIdx) => (
                            <div key={oIdx} className="p-2.5 rounded-lg bg-slate-900 border border-slate-800/80 text-slate-300">
                              {opt}
                            </div>
                          ))}
                        </div>
                      )}

                      <div>
                        <button
                          onClick={() => toggleAnswer(idx)}
                          className="flex items-center gap-1.5 text-xs font-semibold text-indigo-400 hover:text-indigo-300 transition-colors"
                        >
                          {revealedAnswers[idx] ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                          {revealedAnswers[idx] ? 'Hide Solution' : 'Reveal Solution & Explanation'}
                        </button>

                        {revealedAnswers[idx] && (
                          <div className="mt-3 p-3 rounded-lg bg-emerald-950/20 border border-emerald-500/30 text-xs space-y-1">
                            <span className="font-bold text-emerald-400 block">Correct Answer: {q.answer}</span>
                            <p className="text-emerald-200/90 leading-relaxed">{q.explanation}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Key Takeaways */}
            {content.key_takeaways && content.key_takeaways.length > 0 && (
              <div className="space-y-3 p-5 rounded-xl bg-indigo-950/20 border border-indigo-500/30">
                <h3 className="text-sm font-bold uppercase tracking-wider text-indigo-300 flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-indigo-400" /> Key Takeaways
                </h3>
                <ul className="space-y-2">
                  {content.key_takeaways.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-xs text-indigo-100 leading-relaxed">
                      <span className="text-indigo-400 font-bold">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* References */}
            {content.references_and_further_reading && content.references_and_further_reading.length > 0 && (
              <div className="space-y-2 text-xs text-slate-400">
                <h4 className="font-semibold uppercase tracking-wider text-slate-500">References & Further Reading</h4>
                <ol className="list-decimal list-inside space-y-1">
                  {content.references_and_further_reading.map((ref, idx) => (
                    <li key={idx} className="text-slate-400">{ref}</li>
                  ))}
                </ol>
              </div>
            )}
          </div>
        )}

        {activeTab === 'markdown' && (
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 overflow-x-auto whitespace-pre-wrap leading-relaxed">
            {markdownText}
          </div>
        )}

        {activeTab === 'json' && (
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-emerald-400 overflow-x-auto whitespace-pre leading-relaxed">
            {JSON.stringify(content, null, 2)}
          </div>
        )}
      </div>
    </div>
  );
};

