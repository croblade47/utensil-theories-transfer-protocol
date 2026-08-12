import React, { useState } from 'react';
import { BarChart3, TrendingUp, DollarSign, Users, Star, Plus, CheckCircle2, MessageSquare, Award } from 'lucide-react';
import { MarketMetric } from '../types';

interface Step4AnalyticsProps {
  metrics: MarketMetric[];
  onAddMetric: (newMetric: MarketMetric) => void;
}

export const Step4Analytics: React.FC<Step4AnalyticsProps> = ({ metrics, onAddMetric }) => {
  const [showLogForm, setShowLogForm] = useState(false);

  // Form State
  const [formBookletTitle, setFormBookletTitle] = useState('Everyday AI Prompting Handbook');
  const [formProduced, setFormProduced] = useState(50);
  const [formDistributed, setFormDistributed] = useState(45);
  const [formSold, setFormSold] = useState(38);
  const [formUnitPrice, setFormUnitPrice] = useState(4.00);
  const [formHours, setFormHours] = useState(2.0);
  const [formRating, setFormRating] = useState(4.9);
  const [formRepeat, setFormRepeat] = useState(90);
  const [formFeedback, setFormFeedback] = useState('Super easy for seniors to understand!');

  const totalProduced = metrics.reduce((acc, m) => acc + m.producedCount, 0);
  const totalDistributed = metrics.reduce((acc, m) => acc + m.distributedCount, 0);
  const totalSold = metrics.reduce((acc, m) => acc + m.soldCount, 0);
  const totalRevenue = metrics.reduce((acc, m) => acc + m.totalRevenue, 0);

  const handleCreateMetric = (e: React.FormEvent) => {
    e.preventDefault();
    const newM: MarketMetric = {
      id: `m-${Date.now()}`,
      bookletId: 'bk-custom',
      bookletTitle: formBookletTitle,
      producedCount: formProduced,
      distributedCount: formDistributed,
      soldCount: formSold,
      unitPrice: formUnitPrice,
      totalRevenue: formSold * formUnitPrice,
      productionTimeHours: formHours,
      averageRating: formRating,
      repeatInterestRate: formRepeat,
      feedbackNotes: [formFeedback],
      phase: 'market_testing',
      dateLogged: new Date().toISOString().split('T')[0]
    };

    onAddMetric(newM);
    setShowLogForm(false);
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="inline-flex items-center gap-2 text-xs font-mono font-semibold text-rose-400 bg-rose-500/10 px-2.5 py-1 rounded-full border border-rose-500/20 mb-2">
            <BarChart3 className="w-3.5 h-3.5" />
            <span>STEP 4: TEST, SELL, AND IMPROVE ANALYTICS</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
            Market Demand & Sales Analytics Board
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Track prototype feedback, small-scale sales, production time, and customer repeat interest across release phases.
          </p>
        </div>

        <button
          onClick={() => setShowLogForm(!showLogForm)}
          className="btn-primary text-xs px-4 py-2.5 shrink-0 bg-gradient-to-r from-rose-600 to-indigo-600"
        >
          <Plus className="w-4 h-4" />
          <span>{showLogForm ? 'Close Form' : 'Log New Market Release Batch'}</span>
        </button>
      </div>

      {/* Metric Highlights Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="glass-card p-4">
          <span className="text-xs text-slate-400 font-mono">Total Produced</span>
          <h3 className="text-2xl font-extrabold font-heading text-white mt-1">{totalProduced}</h3>
          <p className="text-[10px] text-slate-500 mt-1">Across 3 releases</p>
        </div>

        <div className="glass-card p-4">
          <span className="text-xs text-slate-400 font-mono">Total Distributed</span>
          <h3 className="text-2xl font-extrabold font-heading text-emerald-400 mt-1">{totalDistributed}</h3>
          <p className="text-[10px] text-emerald-500/70 mt-1">{((totalDistributed / totalProduced) * 100).toFixed(0)}% Conversion</p>
        </div>

        <div className="glass-card p-4">
          <span className="text-xs text-slate-400 font-mono">Total Booklets Sold</span>
          <h3 className="text-2xl font-extrabold font-heading text-cyan-400 mt-1">{totalSold}</h3>
          <p className="text-[10px] text-cyan-500/70 mt-1">{((totalSold / totalDistributed) * 100).toFixed(0)}% Sell-through</p>
        </div>

        <div className="glass-card p-4">
          <span className="text-xs text-slate-400 font-mono">Total Sales Revenue</span>
          <h3 className="text-2xl font-extrabold font-heading text-amber-400 mt-1">${totalRevenue.toFixed(2)}</h3>
          <p className="text-[10px] text-amber-500/70 mt-1">Avg ${ (totalRevenue / totalSold || 0).toFixed(2) } / unit</p>
        </div>
      </div>

      {/* New Log Form */}
      {showLogForm && (
        <form onSubmit={handleCreateMetric} className="glass-card p-6 border-rose-500/40 space-y-4 animate-fadeIn">
          <h3 className="font-heading font-bold text-white text-base">Log Market Testing Release Batch</h3>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Booklet Title</label>
              <input
                type="text"
                value={formBookletTitle}
                onChange={(e) => setFormBookletTitle(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-rose-500"
                required
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Number Produced</label>
              <input
                type="number"
                value={formProduced}
                onChange={(e) => setFormProduced(Number(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-rose-500"
                required
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Number Sold</label>
              <input
                type="number"
                value={formSold}
                onChange={(e) => setFormSold(Number(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-rose-500"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Unit Price ($)</label>
              <input
                type="number"
                step="0.5"
                value={formUnitPrice}
                onChange={(e) => setFormUnitPrice(Number(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-rose-500"
                required
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Customer Feedback Note</label>
              <input
                type="text"
                value={formFeedback}
                onChange={(e) => setFormFeedback(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-rose-500"
              />
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button type="submit" className="btn-primary text-xs px-5 py-2.5 bg-gradient-to-r from-rose-600 to-indigo-600">
              Save Market Log
            </button>
          </div>
        </form>
      )}

      {/* Releases Table */}
      <div className="space-y-4">
        <h3 className="font-heading font-bold text-white text-base">Market Testing Release Logs</h3>

        <div className="space-y-4">
          {metrics.map((m) => (
            <div key={m.id} className="glass-card p-5 space-y-4 border-slate-800">
              
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="font-heading font-bold text-white text-base">{m.bookletTitle}</h4>
                    <span className="text-[10px] font-mono bg-rose-500/20 text-rose-300 border border-rose-500/30 px-2 py-0.5 rounded-full uppercase">
                      {m.phase.replace('_', ' ')}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5">Logged: {m.dateLogged}</p>
                </div>

                <div className="flex items-center gap-4 text-xs font-mono">
                  <div>
                    <span className="text-slate-500 block">Unit Price</span>
                    <strong className="text-white">${m.unitPrice.toFixed(2)}</strong>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Total Revenue</span>
                    <strong className="text-amber-400">${m.totalRevenue.toFixed(2)}</strong>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Rating</span>
                    <strong className="text-emerald-400 flex items-center gap-1">
                      <Star className="w-3.5 h-3.5 fill-emerald-400" />
                      {m.averageRating} / 5.0
                    </strong>
                  </div>
                </div>
              </div>

              {/* Progress Bars for Produced vs Distributed vs Sold */}
              <div className="space-y-2">
                <div className="flex justify-between text-xs text-slate-400 font-mono">
                  <span>Sales Conversion: {m.soldCount} sold out of {m.producedCount} produced</span>
                  <span className="text-cyan-400 font-bold">{((m.soldCount / m.producedCount) * 100).toFixed(0)}%</span>
                </div>
                
                <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden flex border border-slate-800">
                  <div 
                    style={{ width: `${(m.soldCount / m.producedCount) * 100}%` }} 
                    className="bg-gradient-to-r from-emerald-500 to-cyan-500 h-full"
                  />
                  <div 
                    style={{ width: `${((m.distributedCount - m.soldCount) / m.producedCount) * 100}%` }} 
                    className="bg-indigo-500/40 h-full"
                  />
                </div>
              </div>

              {/* Feedback Notes */}
              {m.feedbackNotes && m.feedbackNotes.length > 0 && (
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs space-y-1">
                  <span className="text-[10px] text-rose-400 font-mono font-bold uppercase flex items-center gap-1">
                    <MessageSquare className="w-3 h-3" /> Customer Feedback & Objections:
                  </span>
                  {m.feedbackNotes.map((note, idx) => (
                    <p key={idx} className="text-slate-300 italic">"{note}"</p>
                  ))}
                </div>
              )}

            </div>
          ))}
        </div>

      </div>

    </div>
  );
};
