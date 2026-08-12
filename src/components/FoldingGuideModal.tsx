import React, { useState } from 'react';
import { Scissors, FileText, Sparkles, CheckCircle2, ChevronRight, ChevronLeft } from 'lucide-react';

interface FoldingGuideModalProps {
  onClose: () => void;
}

export const FoldingGuideModal: React.FC<FoldingGuideModalProps> = ({ onClose }) => {
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    {
      title: "Step 1: Print Your 8-Page Imposition Sheet",
      description: "Print your booklet on a single sheet of standard paper (8.5\" x 11\" or A4). Select 'Actual Size' with borderless margins.",
      icon: FileText,
      diagram: "sheet_printed"
    },
    {
      title: "Step 2: Fold Lengthwise (Hamburger Fold)",
      description: "Fold the sheet in half along the central horizontal line so pages 8, 1, 4, 5 touch 7, 2, 3, 6.",
      icon: FileText,
      diagram: "fold_horizontal"
    },
    {
      title: "Step 3: Fold Widthwise into Quarters",
      description: "Fold the paper in half again widthwise, then unfold back to the single horizontal crease.",
      icon: FileText,
      diagram: "fold_quarters"
    },
    {
      title: "Step 4: Cut Central Slit Line",
      description: "Use scissors to cut along the dotted red line in the center of the sheet across the middle 2 panels.",
      icon: Scissors,
      diagram: "cut_slit"
    },
    {
      title: "Step 5: Pop Open & Assemble Into 8-Page Booklet",
      description: "Push both ends inward so the slit opens into a diamond, then fold flat to form your completed 8-page zine!",
      icon: Sparkles,
      diagram: "booklet_assembled"
    }
  ];

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-xl w-full shadow-2xl space-y-6">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-amber-400">
              <Scissors className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-heading font-bold text-lg text-white">
                1-Sheet Zine Folding & Cutting Guide
              </h3>
              <p className="text-xs text-slate-400">
                How to turn 1 sheet of paper into a completed 8-page mini booklet
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-sm">✕</button>
        </div>

        {/* Step Visualizer */}
        <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 text-center space-y-4 min-h-[260px] flex flex-col justify-between">
          
          <div className="flex items-center justify-between text-xs font-mono text-amber-400">
            <span>STEP {currentStep + 1} OF {steps.length}</span>
            <span>{steps[currentStep].title}</span>
          </div>

          {/* Interactive Diagram Placeholder */}
          <div className="my-4 py-8 bg-slate-900 rounded-lg border border-dashed border-slate-700 flex flex-col items-center justify-center gap-3">
            {currentStep === 0 && (
              <div className="grid grid-cols-4 grid-rows-2 gap-1.5 w-48 h-28 border-2 border-slate-600 bg-slate-950 p-1">
                <div className="bg-indigo-500/20 text-[9px] font-mono text-white flex items-center justify-center border border-indigo-500/40">Page 8</div>
                <div className="bg-cyan-500/20 text-[9px] font-mono text-white flex items-center justify-center border border-cyan-500/40">Page 1</div>
                <div className="bg-indigo-500/20 text-[9px] font-mono text-white flex items-center justify-center border border-indigo-500/40">Page 4</div>
                <div className="bg-indigo-500/20 text-[9px] font-mono text-white flex items-center justify-center border border-indigo-500/40">Page 5</div>
                <div className="bg-indigo-500/20 text-[9px] font-mono text-white flex items-center justify-center border border-indigo-500/40">Page 7</div>
                <div className="bg-indigo-500/20 text-[9px] font-mono text-white flex items-center justify-center border border-indigo-500/40">Page 2</div>
                <div className="bg-indigo-500/20 text-[9px] font-mono text-white flex items-center justify-center border border-indigo-500/40">Page 3</div>
                <div className="bg-amber-500/20 text-[9px] font-mono text-white flex items-center justify-center border border-amber-500/40">Page 6</div>
              </div>
            )}

            {currentStep === 3 && (
              <div className="relative w-48 h-24 border-2 border-amber-500 bg-slate-950 flex items-center justify-center">
                <div className="w-24 h-0 border-t-2 border-dashed border-rose-500 relative">
                  <Scissors className="w-4 h-4 text-rose-400 absolute -top-2 left-10 animate-bounce" />
                </div>
              </div>
            )}

            {currentStep === 4 && (
              <div className="w-20 h-28 bg-gradient-to-tr from-indigo-600 to-cyan-600 rounded-r-md border-l-4 border-amber-400 shadow-xl flex items-center justify-center text-white font-bold text-xs p-2 text-center">
                Completed 8-Page Booklet
              </div>
            )}

            {(currentStep === 1 || currentStep === 2) && (
              <div className="w-40 h-20 border-2 border-indigo-500 bg-slate-950 flex items-center justify-center text-indigo-300 font-mono text-xs">
                Folding Crease Line
              </div>
            )}

            <p className="text-xs text-slate-300 max-w-sm px-4">
              {steps[currentStep].description}
            </p>
          </div>

          {/* Controls */}
          <div className="flex items-center justify-between pt-2 border-t border-slate-800">
            <button
              onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
              disabled={currentStep === 0}
              className="btn-secondary text-xs disabled:opacity-40"
            >
              <ChevronLeft className="w-4 h-4" />
              <span>Previous</span>
            </button>

            <div className="flex gap-1">
              {steps.map((_, idx) => (
                <div
                  key={idx}
                  className={`w-2 h-2 rounded-full transition-all ${
                    idx === currentStep ? 'w-6 bg-amber-400' : 'bg-slate-700'
                  }`}
                />
              ))}
            </div>

            <button
              onClick={() => {
                if (currentStep < steps.length - 1) {
                  setCurrentStep(currentStep + 1);
                } else {
                  onClose();
                }
              }}
              className="btn-primary text-xs"
            >
              <span>{currentStep === steps.length - 1 ? 'Got It!' : 'Next Step'}</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

        </div>

      </div>
    </div>
  );
};
