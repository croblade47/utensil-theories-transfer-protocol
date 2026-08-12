import React, { useState } from 'react';
import { Terminal, Copy, Check, Plus, Sparkles, BookOpen, Layers, Sliders, ChevronRight } from 'lucide-react';
import { PromptLibrary, PromptItem, BookletTier } from '../types';

interface Step2PromptsProps {
  libraries: PromptLibrary[];
  onAddPromptToLibrary: (libId: string, prompt: PromptItem) => void;
  onSendPromptToBooklet: (prompt: PromptItem) => void;
}

export const Step2Prompts: React.FC<Step2PromptsProps> = ({
  libraries,
  onAddPromptToLibrary,
  onSendPromptToBooklet
}) => {
  const [selectedLibId, setSelectedLibId] = useState<string>(libraries[0]?.id || 'lib-1');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // Prompt Architect Form State
  const [showArchitect, setShowArchitect] = useState(false);
  const [promptTitle, setPromptTitle] = useState('');
  const [promptTier, setPromptTier] = useState<BookletTier>('beginner');
  const [objective, setObjective] = useState('');
  const [format, setFormat] = useState('1 sentence summary + 3 bullet points.');
  const [constraints, setConstraints] = useState('6th-grade reading level, no jargon, max 120 words.');
  const [reasoningReq, setReasoningReq] = useState(false);
  const [variableInput, setVariableInput] = useState('TOPIC');

  const activeLibrary = libraries.find(l => l.id === selectedLibId) || libraries[0];

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleBuildPrompt = (e: React.FormEvent) => {
    e.preventDefault();
    if (!promptTitle || !objective) return;

    const compiledText = `OBJECTIVE: ${objective}. FORMAT: ${format}. CONSTRAINTS: ${constraints}.${reasoningReq ? ' REASONING: Explain steps before answering.' : ''}`;

    const newPrompt: PromptItem = {
      id: `p-${Date.now()}`,
      title: promptTitle,
      libraryId: selectedLibId,
      tier: promptTier,
      objective,
      format,
      constraints,
      reasoningReq,
      compiledPrompt: compiledText,
      variables: variableInput ? variableInput.split(',').map(s => s.trim()) : [],
      difficulty: promptTier === 'beginner' ? 'Easy' : 'Advanced'
    };

    onAddPromptToLibrary(selectedLibId, newPrompt);
    setShowArchitect(false);
    setPromptTitle('');
    setObjective('');
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="inline-flex items-center gap-2 text-xs font-mono font-semibold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20 mb-2">
            <Terminal className="w-3.5 h-3.5" />
            <span>STEP 2: BUILD HIGH-IMPACT PROMPT SYSTEMS</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
            High-Impact Prompt Engineering Studio
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Build high-precision prompts using the 4-part framework across Libraries 1 through 6.
          </p>
        </div>

        <button
          onClick={() => setShowArchitect(!showArchitect)}
          className="btn-primary text-xs px-4 py-2.5 shrink-0 bg-gradient-to-r from-emerald-600 to-cyan-600"
        >
          <Plus className="w-4 h-4" />
          <span>{showArchitect ? 'Close Builder' : 'Open 4-Part Prompt Architect'}</span>
        </button>
      </div>

      {/* 4-Part Prompt Architect Form */}
      {showArchitect && (
        <form onSubmit={handleBuildPrompt} className="glass-card p-6 border-emerald-500/40 space-y-4 animate-fadeIn">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="font-heading font-bold text-white text-base flex items-center gap-2">
              <Sliders className="w-4 h-4 text-emerald-400" />
              <span>4-Part High-Impact Prompt Architect</span>
            </h3>
            <span className="text-xs text-slate-400 font-mono">Formula: Objective $\rightarrow$ Format $\rightarrow$ Constraints $\rightarrow$ Reasoning</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Prompt Title</label>
              <input
                type="text"
                value={promptTitle}
                onChange={(e) => setPromptTitle(e.target.value)}
                placeholder="e.g. 6th-Grade Math Explainer"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-emerald-500"
                required
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Target Library</label>
              <select
                value={selectedLibId}
                onChange={(e) => setSelectedLibId(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-emerald-500"
              >
                {libraries.map(l => (
                  <option key={l.id} value={l.id}>{l.title}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Booklet Tier</label>
              <select
                value={promptTier}
                onChange={(e) => setPromptTier(e.target.value as BookletTier)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-emerald-500"
              >
                <option value="beginner">Beginner (Snap & Run)</option>
                <option value="advanced">Advanced (Remember Me)</option>
              </select>
            </div>
          </div>

          {/* 4 Steps Inputs */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
            <div>
              <label className="text-xs font-semibold text-emerald-400 block mb-1">1. Define Objective First</label>
              <textarea
                value={objective}
                onChange={(e) => setObjective(e.target.value)}
                placeholder="What single specific goal must the AI accomplish?"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-emerald-500 h-16"
                required
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-cyan-400 block mb-1">2. Define Desired Output Format</label>
              <textarea
                value={format}
                onChange={(e) => setFormat(e.target.value)}
                placeholder="3 bullet points, markdown table, or 1-sentence summary."
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-cyan-500 h-16"
                required
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-amber-400 block mb-1">3. Define Constraints</label>
              <textarea
                value={constraints}
                onChange={(e) => setConstraints(e.target.value)}
                placeholder="Max 120 words, 6th-grade vocabulary, zero technical jargon."
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-amber-500 h-16"
                required
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-rose-400 block mb-1">4. Variables & Reasoning Option</label>
              <div className="space-y-2">
                <input
                  type="text"
                  value={variableInput}
                  onChange={(e) => setVariableInput(e.target.value)}
                  placeholder="Variables e.g. TOPIC, PATIENT_AGE"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-rose-500"
                />
                <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer pt-1">
                  <input
                    type="checkbox"
                    checked={reasoningReq}
                    onChange={(e) => setReasoningReq(e.target.checked)}
                    className="rounded border-slate-800 bg-slate-950 text-emerald-500"
                  />
                  <span>Require Step-by-Step Chain-of-Thought Reasoning</span>
                </label>
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button type="submit" className="btn-primary text-xs px-5 py-2.5 bg-gradient-to-r from-emerald-600 to-cyan-600">
              Compile & Save Prompt
            </button>
          </div>
        </form>
      )}

      {/* Library Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        {libraries.map((lib) => (
          <button
            key={lib.id}
            onClick={() => setSelectedLibId(lib.id)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold shrink-0 transition-all ${
              selectedLibId === lib.id
                ? 'bg-gradient-to-r from-emerald-600 to-cyan-600 text-white shadow-lg shadow-emerald-500/20'
                : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            <span>{lib.title}</span>
            <span className="ml-2 font-mono text-[10px] bg-slate-950/60 px-1.5 py-0.5 rounded-full">
              {lib.prompts.length}
            </span>
          </button>
        ))}
      </div>

      {/* Active Library Description */}
      <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between">
        <div>
          <h3 className="font-heading font-bold text-white text-base">{activeLibrary.title}</h3>
          <p className="text-xs text-slate-400 mt-0.5">{activeLibrary.description}</p>
        </div>
        <span className="font-mono text-xs font-bold text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
          {activeLibrary.keyword}
        </span>
      </div>

      {/* Prompts Cards List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {activeLibrary.prompts.map((p) => (
          <div key={p.id} className="glass-card p-6 space-y-4 flex flex-col justify-between border-slate-800 hover:border-emerald-500/50 transition-all">
            
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className={`text-[10px] font-mono px-2.5 py-0.5 rounded-full font-bold ${
                  p.tier === 'beginner' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                }`}>
                  {p.tier === 'beginner' ? 'Beginner (Snap & Run)' : 'Advanced (Remember Me)'}
                </span>
                <div className="flex gap-1">
                  {p.variables.map((v, idx) => (
                    <span key={idx} className="text-[10px] font-mono bg-slate-950 text-cyan-400 border border-cyan-500/30 px-2 py-0.5 rounded">
                      [{v}]
                    </span>
                  ))}
                </div>
              </div>

              <h3 className="font-heading font-bold text-white text-base">{p.title}</h3>

              {/* Formatted Prompt Output Box */}
              <div className="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-2 font-mono text-xs">
                <span className="text-[10px] text-slate-500 font-bold block uppercase">Compiled Prompt Template:</span>
                <p className="text-slate-300 leading-relaxed whitespace-pre-line">{p.compiledPrompt}</p>
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-400 font-mono">
                <div><strong>Format:</strong> {p.format}</div>
                <div><strong>Constraints:</strong> {p.constraints}</div>
              </div>
            </div>

            {/* Action Row */}
            <div className="pt-3 border-t border-slate-800 flex items-center justify-between gap-2">
              <button
                onClick={() => handleCopy(p.id, p.compiledPrompt)}
                className="btn-secondary text-xs py-1.5 px-3 flex items-center gap-1.5"
              >
                {copiedId === p.id ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedId === p.id ? 'Copied!' : 'Copy Prompt'}</span>
              </button>

              <button
                onClick={() => onSendPromptToBooklet(p)}
                className="btn-primary text-xs py-1.5 px-3 bg-gradient-to-r from-emerald-600 to-cyan-600"
              >
                <BookOpen className="w-3.5 h-3.5" />
                <span>Send to Step 3 Booklet</span>
              </button>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
};
