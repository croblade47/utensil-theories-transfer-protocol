import React, { useState } from 'react';
import { Search, Plus, Filter, CheckCircle2, Sparkles, Star, ChevronRight } from 'lucide-react';
import { AISolution, ResearchArea } from '../types';

interface Step1SolutionsProps {
  solutions: AISolution[];
  researchAreas: ResearchArea[];
  onAddSolution: (newSol: AISolution) => void;
  onSendToPromptStudio: (sol: AISolution) => void;
}

export const Step1Solutions: React.FC<Step1SolutionsProps> = ({
  solutions,
  researchAreas,
  onAddSolution,
  onSendToPromptStudio
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);

  // Form State
  const [formTitle, setFormTitle] = useState('');
  const [formCategory, setFormCategory] = useState('health');
  const [formProblem, setFormProblem] = useState('');
  const [formSolution, setFormSolution] = useState('');
  const [formAudience, setFormAudience] = useState('');
  const [formBeginnerPrompt, setFormBeginnerPrompt] = useState('');

  const filteredSolutions = solutions.filter((s) => {
    const matchesCategory = selectedCategory === 'all' || s.categoryId === selectedCategory;
    const matchesSearch = s.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          s.problem.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          s.tags.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  const handleCreateSolution = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formTitle || !formProblem || !formSolution) return;

    const catObj = researchAreas.find(r => r.id === formCategory) || researchAreas[0];

    const newSol: AISolution = {
      id: `sol-${Date.now()}`,
      title: formTitle,
      categoryId: formCategory,
      categoryName: catObj.name,
      problem: formProblem,
      solution: formSolution,
      plainLanguageSummary: formSolution,
      targetAudience: formAudience || 'General Public',
      nonTechScore: 95,
      measurableValueScore: 94,
      plainLanguageScore: 96,
      commonProblemScore: 97,
      tags: ['Custom', catObj.name],
      beginnerPrompt: formBeginnerPrompt || `OBJECTIVE: Solve ${formProblem}. FORMAT: 3 bullet points. CONSTRAINTS: 6th-grade language.`,
      advancedPrompt: `Remember Me Profile: [USER_NAME]. Advanced solution for ${formTitle}.`
    };

    onAddSolution(newSol);
    setShowAddForm(false);
    setFormTitle('');
    setFormProblem('');
    setFormSolution('');
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="inline-flex items-center gap-2 text-xs font-mono font-semibold text-cyan-400 bg-cyan-500/10 px-2.5 py-1 rounded-full border border-cyan-500/20 mb-2">
            <Search className="w-3.5 h-3.5" />
            <span>STEP 1: IDENTIFY REAL-WORLD AI SOLUTIONS</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
            Real-World AI Solution Matrix
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Assess everyday problems across 8 research areas. Every solution must solve a common problem in plain language.
          </p>
        </div>

        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="btn-primary text-xs px-4 py-2.5 shrink-0"
        >
          <Plus className="w-4 h-4" />
          <span>{showAddForm ? 'Close Form' : 'Add New Solution Vector'}</span>
        </button>
      </div>

      {/* Custom Solution Creator Form */}
      {showAddForm && (
        <form onSubmit={handleCreateSolution} className="glass-card p-6 border-cyan-500/40 space-y-4 animate-fadeIn">
          <h3 className="font-heading font-bold text-white text-base">Propose New AI Solution Vector</h3>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Solution Title</label>
              <input
                type="text"
                value={formTitle}
                onChange={(e) => setFormTitle(e.target.value)}
                placeholder="e.g. Senior Gardening Voice Companion"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-cyan-500"
                required
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Research Area</label>
              <select
                value={formCategory}
                onChange={(e) => setFormCategory(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-cyan-500"
              >
                {researchAreas.map(r => (
                  <option key={r.id} value={r.id}>{r.name}</option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1">Real-World Problem Description</label>
            <textarea
              value={formProblem}
              onChange={(e) => setFormProblem(e.target.value)}
              placeholder="What specific everyday frustration does the user encounter?"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-cyan-500 h-20"
              required
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1">AI Solution Strategy</label>
            <textarea
              value={formSolution}
              onChange={(e) => setFormSolution(e.target.value)}
              placeholder="How does AI solve this in plain language?"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-cyan-500 h-20"
              required
            />
          </div>

          <div className="flex justify-end pt-2">
            <button type="submit" className="btn-primary text-xs px-5 py-2">
              Save Solution to Catalog
            </button>
          </div>
        </form>
      )}

      {/* Category Pills & Search */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Category Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full md:w-auto pb-2 md:pb-0 scrollbar-none">
          <button
            onClick={() => setSelectedCategory('all')}
            className={`px-3 py-1.5 rounded-full text-xs font-medium shrink-0 transition-all ${
              selectedCategory === 'all'
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-semibold'
                : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            All Areas ({solutions.length})
          </button>
          {researchAreas.map((area) => (
            <button
              key={area.id}
              onClick={() => setSelectedCategory(area.id)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium shrink-0 transition-all ${
                selectedCategory === area.id
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-semibold'
                  : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              {area.name}
            </button>
          ))}
        </div>

        {/* Search Bar */}
        <div className="relative w-full md:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search solutions..."
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-white outline-none focus:border-cyan-500"
          />
        </div>

      </div>

      {/* Solutions Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredSolutions.map((sol) => (
          <div key={sol.id} className="glass-card p-6 space-y-4 flex flex-col justify-between border-slate-800 hover:border-cyan-500/50 transition-all">
            
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-mono text-cyan-400 bg-cyan-500/10 px-2.5 py-0.5 rounded-full border border-cyan-500/20 font-semibold">
                  {sol.categoryName}
                </span>
                <div className="flex gap-1">
                  {sol.tags.map((t, idx) => (
                    <span key={idx} className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded-md">
                      #{t}
                    </span>
                  ))}
                </div>
              </div>

              <h3 className="font-heading font-bold text-white text-lg">{sol.title}</h3>

              <div className="space-y-2 text-xs">
                <div className="bg-rose-500/10 border border-rose-500/20 p-2.5 rounded-lg text-rose-200">
                  <strong className="text-rose-400 block font-mono text-[10px] uppercase mb-0.5">Everyday Problem:</strong>
                  {sol.problem}
                </div>

                <div className="bg-emerald-500/10 border border-emerald-500/20 p-2.5 rounded-lg text-emerald-200">
                  <strong className="text-emerald-400 block font-mono text-[10px] uppercase mb-0.5">AI Solution Strategy:</strong>
                  {sol.solution}
                </div>
              </div>
            </div>

            {/* Success Criteria Ratings Bar */}
            <div className="pt-3 border-t border-slate-800 space-y-3">
              <div className="grid grid-cols-4 gap-1 text-center text-[10px] font-mono">
                <div className="bg-slate-950 p-1.5 rounded border border-slate-800">
                  <span className="text-slate-500 block">Common</span>
                  <strong className="text-emerald-400 font-bold">{sol.commonProblemScore}%</strong>
                </div>
                <div className="bg-slate-950 p-1.5 rounded border border-slate-800">
                  <span className="text-slate-500 block">Non-Tech</span>
                  <strong className="text-cyan-400 font-bold">{sol.nonTechScore}%</strong>
                </div>
                <div className="bg-slate-950 p-1.5 rounded border border-slate-800">
                  <span className="text-slate-500 block">Value</span>
                  <strong className="text-amber-400 font-bold">{sol.measurableValueScore}%</strong>
                </div>
                <div className="bg-slate-950 p-1.5 rounded border border-slate-800">
                  <span className="text-slate-500 block">Plain Lang</span>
                  <strong className="text-indigo-400 font-bold">{sol.plainLanguageScore}%</strong>
                </div>
              </div>

              <button
                onClick={() => onSendToPromptStudio(sol)}
                className="w-full btn-secondary text-xs py-2 justify-center hover:border-cyan-500/50"
              >
                <span>Send to Step 2 Prompt Studio</span>
                <ChevronRight className="w-4 h-4 text-cyan-400" />
              </button>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
};
