import React from 'react';
import { 
  Rocket, 
  Search, 
  Terminal, 
  BookOpen, 
  BarChart3, 
  PlayCircle, 
  Sparkles, 
  Printer, 
  ShieldCheck, 
  CheckCircle2, 
  ArrowRight,
  TrendingUp,
  Award
} from 'lucide-react';
import { ProtocolStep, BookletTemplate, AISolution } from '../types';

interface DashboardViewProps {
  setStep: (step: ProtocolStep) => void;
  booklets: BookletTemplate[];
  solutions: AISolution[];
  totalDistributed: number;
  totalSold: number;
  totalRevenue: number;
  openFoldingGuide: () => void;
  openAccountModal: () => void;
  openPhoneHotline: () => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  setStep,
  booklets,
  solutions,
  totalDistributed,
  totalSold,
  totalRevenue,
  openFoldingGuide,
  openAccountModal,
  openPhoneHotline
}) => {
  return (
    <div className="space-y-8 animate-fadeIn">
      
      {/* Hero Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-950 via-slate-900 to-cyan-950 border border-slate-800 p-6 sm:p-10 shadow-2xl">
        <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute bottom-0 left-0 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 text-xs font-mono font-semibold">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>UTENSIL THEORIES TRANSFER PROTOCOL • SYSTEM HUB</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold font-heading text-white tracking-tight leading-tight">
            Transforming AI Knowledge into <span className="bg-gradient-to-r from-cyan-400 via-emerald-400 to-amber-300 bg-clip-text text-transparent">Printable 8-Page Booklets</span> for Everyday People.
          </h1>

          <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
            Identify real-world problems, build high-impact prompt systems, format compact single-sheet folded zines, and test market demand through small-scale sales and real-world feedback loops.
          </p>

          {/* Action Button Row */}
          <div className="flex flex-wrap items-center gap-3 pt-2">
            <button
              onClick={() => setStep('step3')}
              className="btn-primary text-sm px-5 py-3 rounded-xl shadow-xl shadow-cyan-500/20"
            >
              <Printer className="w-4 h-4" />
              <span>Launch 8-Page Zine Studio</span>
            </button>

            <button
              onClick={() => setStep('simulations')}
              className="btn-secondary text-sm px-5 py-3 rounded-xl"
            >
              <PlayCircle className="w-4 h-4 text-cyan-400" />
              <span>Run Gemini & Copilot Test Suite</span>
            </button>

            <button
              onClick={openFoldingGuide}
              className="text-xs text-amber-300 hover:text-amber-200 underline px-3 py-2"
            >
              How to Fold a 1-Sheet Zine →
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Counter Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="glass-card p-4 flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Search className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-mono">Solutions Cataloged</p>
            <h3 className="text-2xl font-extrabold font-heading text-white">{solutions.length}</h3>
          </div>
        </div>

        <div className="glass-card p-4 flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <BookOpen className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-mono">Booklets Designed</p>
            <h3 className="text-2xl font-extrabold font-heading text-white">{booklets.length}</h3>
          </div>
        </div>

        <div className="glass-card p-4 flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
            <TrendingUp className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-mono">Total Distributed</p>
            <h3 className="text-2xl font-extrabold font-heading text-white">{totalDistributed} <span className="text-xs font-normal text-slate-400">units</span></h3>
          </div>
        </div>

        <div className="glass-card p-4 flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-mono">Total Sales Revenue</p>
            <h3 className="text-2xl font-extrabold font-heading text-white">${totalRevenue.toFixed(2)}</h3>
          </div>
        </div>
      </div>

      {/* 4-Step Protocol Visual Architecture Grid */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold font-heading text-white flex items-center gap-2">
          <span>The 4-Step Transfer Protocol Workflow</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          
          {/* Step 1 Card */}
          <div 
            onClick={() => setStep('step1')}
            className="glass-card p-5 cursor-pointer hover:border-cyan-500/50 space-y-3 group"
          >
            <div className="flex items-center justify-between">
              <span className="w-8 h-8 rounded-lg bg-cyan-500/20 text-cyan-300 font-mono font-bold flex items-center justify-center text-sm">01</span>
              <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-cyan-400 group-hover:translate-x-1 transition-all" />
            </div>
            <h3 className="font-heading font-bold text-white text-base">Step 1: Solution Matrix</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Identify real-world problems across 8 research areas evaluated against 4 success criteria.
            </p>
            <div className="text-[11px] text-cyan-400 font-mono font-semibold pt-1">Explore Solutions →</div>
          </div>

          {/* Step 2 Card */}
          <div 
            onClick={() => setStep('step2')}
            className="glass-card p-5 cursor-pointer hover:border-emerald-500/50 space-y-3 group"
          >
            <div className="flex items-center justify-between">
              <span className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-300 font-mono font-bold flex items-center justify-center text-sm">02</span>
              <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-emerald-400 group-hover:translate-x-1 transition-all" />
            </div>
            <h3 className="font-heading font-bold text-white text-base">Step 2: Prompt Architect</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              High-impact prompt engineering across Libraries 1-6 enforcing Objective, Format, Constraints, Reasoning.
            </p>
            <div className="text-[11px] text-emerald-400 font-mono font-semibold pt-1">Build Prompts →</div>
          </div>

          {/* Step 3 Card */}
          <div 
            onClick={() => setStep('step3')}
            className="glass-card p-5 cursor-pointer hover:border-amber-500/50 space-y-3 group"
          >
            <div className="flex items-center justify-between">
              <span className="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-300 font-mono font-bold flex items-center justify-center text-sm">03</span>
              <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-amber-400 group-hover:translate-x-1 transition-all" />
            </div>
            <h3 className="font-heading font-bold text-white text-base">Step 3: Zine Format Studio</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Single-sheet folded 8-page booklet imposition generator with Beginner & Advanced printable templates.
            </p>
            <div className="text-[11px] text-amber-400 font-mono font-semibold pt-1">Design & Print →</div>
          </div>

          {/* Step 4 Card */}
          <div 
            onClick={() => setStep('step4')}
            className="glass-card p-5 cursor-pointer hover:border-rose-500/50 space-y-3 group"
          >
            <div className="flex items-center justify-between">
              <span className="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-300 font-mono font-bold flex items-center justify-center text-sm">04</span>
              <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-rose-400 group-hover:translate-x-1 transition-all" />
            </div>
            <h3 className="font-heading font-bold text-white text-base">Step 4: Market Analytics</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Track prototype feedback, market sales, unit margin, and repeat interest across 3 release phases.
            </p>
            <div className="text-[11px] text-rose-400 font-mono font-semibold pt-1">Track Sales & Feedback →</div>
          </div>

        </div>
      </div>

      {/* Featured Ready-to-Print Booklet Templates */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold font-heading text-white">Ready-to-Print Booklet Templates</h2>
          <button onClick={() => setStep('step3')} className="text-xs text-cyan-400 hover:text-cyan-300 font-mono">
            View All Templates ({booklets.length}) →
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {booklets.map((b) => (
            <div key={b.id} className="glass-card p-5 flex flex-col justify-between space-y-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full font-bold uppercase ${
                    b.tier === 'beginner' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                  }`}>
                    {b.tier === 'beginner' ? 'Beginner (Snap & Run)' : 'Advanced (Remember Me)'}
                  </span>
                  <span className="text-[11px] text-slate-400 font-mono">{b.pages.length} Pages</span>
                </div>
                <h3 className="font-heading font-bold text-white text-base">{b.title}</h3>
                <p className="text-xs text-slate-400 line-clamp-3">{b.description}</p>
              </div>

              <div className="pt-2 border-t border-slate-800 flex items-center justify-between">
                <span className="text-[11px] text-slate-500 font-mono">Printed {b.printCount}x</span>
                <button
                  onClick={() => setStep('step3')}
                  className="btn-secondary text-xs px-3 py-1.5"
                >
                  <Printer className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Print Zine</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
