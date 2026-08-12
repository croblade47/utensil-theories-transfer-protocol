import React, { useState } from 'react';
import { BookOpen, Printer, Scissors, Eye, Edit3, Plus, Sparkles, CheckCircle2, Download, Layers, QrCode, ExternalLink, Image as ImageIcon, FileText } from 'lucide-react';
import { BookletTemplate, BookletPage, BookletTier } from '../types';

interface Step3BookletStudioProps {
  booklets: BookletTemplate[];
  activeBooklet: BookletTemplate;
  setActiveBooklet: (booklet: BookletTemplate) => void;
  onSaveBooklet: (booklet: BookletTemplate) => void;
  openFoldingGuide: () => void;
}

export const Step3BookletStudio: React.FC<Step3BookletStudioProps> = ({
  booklets,
  activeBooklet,
  setActiveBooklet,
  onSaveBooklet,
  openFoldingGuide
}) => {
  const [viewMode, setViewMode] = useState<'editor' | 'imposition_sheet' | 'cover_art'>('editor');
  const [selectedPageIndex, setSelectedPageIndex] = useState<number>(0);
  const [bookletTitle, setBookletTitle] = useState(activeBooklet.title);

  const selectedPage = activeBooklet.pages[selectedPageIndex] || activeBooklet.pages[0];

  const getStandalonePrintUrl = (bookNum: number) => {
    switch(bookNum) {
      case 1: return '/book1_home_and_planning_print.html';
      case 2: return '/book2_education_and_study_print.html';
      case 3: return '/book3_entertainment_and_games_print.html';
      case 4: return '/book4_small_business_print.html';
      case 5: return '/book5_personal_productivity_print.html';
      case 6: return '/book6_creative_hobbies_print.html';
      case 7: return '/book7_family_and_relationships_print.html';
      case 8: return '/book8_health_and_wellness_print.html';
      default: return '/master_print_catalog.html';
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const handlePageTextChange = (text: string) => {
    const updatedPages = [...activeBooklet.pages];
    updatedPages[selectedPageIndex] = { ...selectedPage, bodyText: text };
    const updatedBooklet = { ...activeBooklet, pages: updatedPages };
    setActiveBooklet(updatedBooklet);
    onSaveBooklet(updatedBooklet);
  };

  const handlePromptBoxChange = (promptText: string) => {
    const updatedPages = [...activeBooklet.pages];
    updatedPages[selectedPageIndex] = { ...selectedPage, promptBox: promptText };
    const updatedBooklet = { ...activeBooklet, pages: updatedPages };
    setActiveBooklet(updatedBooklet);
    onSaveBooklet(updatedBooklet);
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="inline-flex items-center gap-2 text-xs font-mono font-semibold text-amber-400 bg-amber-500/10 px-2.5 py-1 rounded-full border border-amber-500/20 mb-2">
            <BookOpen className="w-3.5 h-3.5" />
            <span>STEP 3: 8-PAGE ZINE & COVER DESIGN STUDIO</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold font-heading text-white">
            1-Sheet Zine Imposition & Cover Studio
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Build pixel-perfect covers with the 8-Book Category Color System and Action-Encoded QR Codes.
          </p>
        </div>

        {/* Print & Action Controls */}
        <div className="flex flex-wrap items-center gap-2 shrink-0">
          <a
            href="/master_print_catalog.html"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary text-xs px-3 py-2 flex items-center gap-1.5 bg-gradient-to-r from-cyan-600 to-indigo-600 shadow-md"
          >
            <FileText className="w-4 h-4" />
            <span>Master Print Catalog (All 8 Books)</span>
          </a>

          <a
            href={getStandalonePrintUrl(activeBooklet.bookNumber)}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-secondary text-xs px-3 py-2 flex items-center gap-1 text-cyan-300 border-cyan-500/40"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            <span>Print Book #{activeBooklet.bookNumber} Zine Sheet</span>
          </a>

          <button
            onClick={openFoldingGuide}
            className="btn-secondary text-xs px-3 py-2"
          >
            <Scissors className="w-4 h-4 text-amber-400" />
            <span>Folding Guide</span>
          </button>
        </div>
      </div>

      {/* 8-Book Collection Switcher Bar */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-xs font-mono text-slate-400 font-bold uppercase">Select Category (Book 1 to 8 Collection):</span>
          <span className="text-xs text-cyan-400 font-mono">8 Color Matched Categories</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
          {booklets.map((b) => (
            <button
              key={b.id}
              onClick={() => {
                setActiveBooklet(b);
                setBookletTitle(b.title);
                setSelectedPageIndex(0);
              }}
              style={{ background: b.coverGradient }}
              className={`p-2.5 rounded-xl text-left border transition-all flex flex-col justify-between h-22 shadow-md ${
                activeBooklet.id === b.id
                  ? 'ring-2 ring-white ring-offset-2 ring-offset-slate-950 scale-[1.03]'
                  : 'opacity-85 hover:opacity-100 border-white/20'
              }`}
            >
              <div className="flex items-center justify-between text-[9px] font-mono font-bold text-white/90">
                <span>No. {b.bookNumber}</span>
                <span>{b.priceTag}</span>
              </div>
              <div className="bg-white/90 text-slate-950 px-1.5 py-0.5 rounded text-[9px] font-black uppercase text-center tracking-wider font-mono my-1">
                {b.category}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* View Mode Toggle Bar */}
      <div className="flex items-center justify-between bg-slate-950 p-2 rounded-xl border border-slate-800">
        <div className="flex items-center gap-2">
          <span className="font-heading font-bold text-sm text-white px-2">Active: {activeBooklet.title}</span>
          <span className="text-xs font-mono text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/30">
            Book #{activeBooklet.bookNumber} of 8
          </span>
        </div>

        <div className="flex gap-1 bg-slate-900 p-1 rounded-lg border border-slate-800 shrink-0">
          <button
            onClick={() => setViewMode('editor')}
            className={`px-3 py-1 rounded-md text-xs font-semibold transition-all ${
              viewMode === 'editor' ? 'bg-amber-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            8-Page Editor
          </button>
          <button
            onClick={() => setViewMode('cover_art')}
            className={`px-3 py-1 rounded-md text-xs font-semibold transition-all ${
              viewMode === 'cover_art' ? 'bg-amber-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            Cover Art Mode
          </button>
          <button
            onClick={() => setViewMode('imposition_sheet')}
            className={`px-3 py-1 rounded-md text-xs font-semibold transition-all ${
              viewMode === 'imposition_sheet' ? 'bg-amber-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            Print Sheet View
          </button>
        </div>
      </div>

      {/* VIEW MODE 1: WYSIWYG 8-PAGE EDITOR */}
      {viewMode === 'editor' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left Column: 8 Page Selector */}
          <div className="glass-card p-4 space-y-3 border-slate-800">
            <h3 className="font-heading font-bold text-white text-sm flex items-center justify-between">
              <span>Booklet Page Sequence</span>
              <span className="text-xs text-amber-400 font-mono">8 Pages</span>
            </h3>

            <div className="space-y-2">
              {activeBooklet.pages.map((p, idx) => (
                <button
                  key={p.pageNumber}
                  onClick={() => setSelectedPageIndex(idx)}
                  className={`w-full text-left p-3 rounded-xl border transition-all flex items-center justify-between ${
                    selectedPageIndex === idx
                      ? 'bg-amber-500/20 border-amber-500/50 text-white shadow-md'
                      : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:text-white hover:bg-slate-900'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-md bg-slate-800 text-amber-300 font-mono font-bold text-xs flex items-center justify-center">
                      {p.pageNumber}
                    </span>
                    <div>
                      <p className="font-heading font-semibold text-xs text-white">{p.title}</p>
                      <span className="text-[10px] text-slate-500 font-mono">{p.contentType.toUpperCase()}</span>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Center Column: Live Page Preview Card */}
          <div className="lg:col-span-2 space-y-4">
            
            {/* If Page 1 (Cover Page), render the Pixel-Perfect Cover Design! */}
            {selectedPage.pageNumber === 1 ? (
              <div 
                style={{ background: activeBooklet.coverGradient }}
                className="p-8 rounded-2xl min-h-[460px] max-w-md mx-auto shadow-2xl relative border border-white/30 flex flex-col justify-between text-white overflow-hidden"
              >
                {/* Thin Silver Inset Border */}
                <div className="absolute inset-3 border border-white/40 rounded-xl pointer-events-none"></div>

                {/* Top Bar */}
                <div className="flex items-center justify-between relative z-10 text-xs font-mono">
                  <span className="text-white/80 uppercase font-black text-[10px] tracking-widest">UTENSIL THEORIES</span>
                  <span className="text-white bg-black/40 border border-white/30 px-2 py-0.5 rounded-full font-bold">No. {activeBooklet.bookNumber} of 8</span>
                </div>

                {/* Prominent Easy-to-See Category Banner */}
                <div className="text-center relative z-10 my-2">
                  <span className="inline-block bg-white text-slate-950 font-sans font-black text-xs uppercase tracking-[0.2em] px-4 py-1.5 rounded shadow-lg">
                    {activeBooklet.category}
                  </span>
                </div>

                {/* Center Title & Subtitle */}
                <div className="text-center relative z-10 my-4">
                  <h1 className="font-serif italic font-extrabold text-4xl text-white tracking-tight drop-shadow-md">
                    Utensil Theories
                  </h1>
                  <div className="text-[10px] font-sans font-extrabold uppercase tracking-[0.35em] text-white/90 mt-2 border-t border-white/30 pt-2 inline-block px-4">
                    AI Made Easy.
                  </div>
                </div>

                {/* Bottom Bar: $2 Starburst & QR */}
                <div className="flex items-end justify-between relative z-10">
                  {/* Starburst */}
                  <div className="relative w-16 h-16 flex items-center justify-center">
                    <div 
                      className="absolute inset-0 bg-amber-300"
                      style={{
                        clipPath: 'polygon(50% 0%, 61% 12%, 75% 4%, 79% 19%, 95% 18%, 91% 33%, 100% 45%, 90% 57%, 98% 71%, 83% 77%, 84% 93%, 69% 90%, 60% 100%, 48% 90%, 35% 98%, 32% 84%, 16% 85%, 21% 70%, 7% 62%, 17% 49%, 4% 37%, 18% 28%, 12% 13%, 28% 14%, 35% 2%)'
                      }}
                    ></div>
                    <span className="relative z-10 font-extrabold text-black text-2xl -rotate-6">{activeBooklet.priceTag}</span>
                  </div>

                  {/* QR Block */}
                  <div className="bg-white p-2 rounded-lg text-center shadow-lg text-slate-900">
                    <QrCode className="w-10 h-10 text-slate-900 mx-auto" />
                    <span className="text-[8px] font-extrabold tracking-widest block mt-0.5">SCAN ME</span>
                  </div>
                </div>

              </div>
            ) : (
              /* Standard Page Render */
              <div className="glass-card p-8 border-2 border-amber-500/30 bg-slate-950 rounded-2xl min-h-[400px] flex flex-col justify-between shadow-2xl relative">
                
                <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                  <span className="text-xs font-mono text-amber-400 font-bold uppercase">
                    PAGE {selectedPage.pageNumber} OF 8 • [{selectedPage.contentType.toUpperCase()}]
                  </span>
                  <span className="text-xs text-slate-400 font-mono">{activeBooklet.title}</span>
                </div>

                {/* Page Content Display */}
                <div className="my-6 space-y-4">
                  <h2 className="text-2xl font-extrabold font-heading text-white">{selectedPage.title}</h2>
                  <p className="text-sm text-slate-300 leading-relaxed">{selectedPage.bodyText}</p>

                  {/* Form Block Grid Render if type is block_form */}
                  {selectedPage.contentType === 'block_form' && selectedPage.blockFields && (
                    <div className="space-y-3 bg-slate-900 p-4 rounded-xl border border-slate-800">
                      <span className="text-[10px] font-mono text-cyan-400 font-bold uppercase">Printed Handwriting Block-Letter Grid</span>
                      {selectedPage.blockFields.map((field, fIdx) => (
                        <div key={fIdx}>
                          <label className="text-[11px] font-mono text-slate-400 uppercase">{field.label}</label>
                          <div className="block-grid justify-start">
                            {field.sampleBoxes.map((boxChar, bIdx) => (
                              <div key={bIdx} className="block-letter-box active">{boxChar}</div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Prompt Box Render */}
                  {selectedPage.promptBox && (
                    <div className="bg-slate-900 p-4 rounded-xl border border-amber-500/40 space-y-2 font-mono text-xs">
                      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                        <span className="text-amber-400 font-bold uppercase text-[10px]">Printed LLM Vision Prompt:</span>
                        <span className="text-cyan-400 text-[10px] flex items-center gap-1">
                          <QrCode className="w-3.5 h-3.5" /> Action-Encoded QR Embedded
                        </span>
                      </div>
                      <p className="text-slate-200">{selectedPage.promptBox}</p>
                    </div>
                  )}
                </div>

                {/* Page Footer */}
                <div className="pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-500 font-mono">
                  <span>Utensil Theories Transfer Protocol</span>
                  <span>Page {selectedPage.pageNumber}</span>
                </div>
              </div>
            )}

            {/* Quick Edit Inputs */}
            <div className="glass-card p-4 space-y-3 border-slate-800">
              <h4 className="font-heading font-bold text-white text-xs uppercase text-amber-400">
                Edit Page {selectedPage.pageNumber} Content
              </h4>

              <div className="space-y-2">
                <div>
                  <label className="text-[11px] font-mono text-slate-400 block mb-1">Body Text</label>
                  <textarea
                    value={selectedPage.bodyText}
                    onChange={(e) => handlePageTextChange(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-amber-500 h-16"
                  />
                </div>
              </div>
            </div>

          </div>

        </div>
      )}

      {/* VIEW MODE 2: COVER ART MODE */}
      {viewMode === 'cover_art' && (
        <div className="glass-card p-6 space-y-6 border-slate-800 text-center">
          <div className="max-w-xl mx-auto space-y-4">
            <h3 className="font-heading font-bold text-white text-xl">
              Book #{activeBooklet.bookNumber} Cover: {activeBooklet.category}
            </h3>
            <p className="text-xs text-slate-400">
              Matched Color Theme: <strong className="text-white">{activeBooklet.category}</strong> ({activeBooklet.coverGradient})
            </p>

            <div className="flex flex-wrap items-center justify-center gap-3">
              <a
                href="/master_print_catalog.html"
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary text-xs px-6 py-2.5 inline-flex items-center gap-2 bg-gradient-to-r from-cyan-600 to-indigo-600 shadow-lg"
              >
                <FileText className="w-4 h-4" />
                <span>Open Master Print Catalog (All 8 Books)</span>
              </a>

              <a
                href={getStandalonePrintUrl(activeBooklet.bookNumber)}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-secondary text-xs px-5 py-2.5 inline-flex items-center gap-2 text-cyan-300"
              >
                <ExternalLink className="w-4 h-4" />
                <span>Open Book #{activeBooklet.bookNumber} Standalone Printable Sheet</span>
              </a>
            </div>
          </div>
        </div>
      )}

      {/* VIEW MODE 3: IMPOSITION SHEET VIEW */}
      {viewMode === 'imposition_sheet' && (
        <div className="space-y-4">
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between">
            <div>
              <h3 className="font-heading font-bold text-white text-sm">Physical 8-Page Imposition Layout (Book #{activeBooklet.bookNumber})</h3>
              <p className="text-xs text-slate-400">
                Arrangement for single-sheet 8.5" x 11" or A4 printing (Top: 8, 1, 4, 5 / Bottom: 7, 2, 3, 6).
              </p>
            </div>
            <div className="flex gap-2">
              <a
                href={getStandalonePrintUrl(activeBooklet.bookNumber)}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary text-xs px-4 py-2 flex items-center gap-1.5"
              >
                <Printer className="w-4 h-4" />
                <span>Print Standalone Book #{activeBooklet.bookNumber} Sheet</span>
              </a>
            </div>
          </div>

          <div className="print-page-wrapper bg-white p-4 text-slate-950 rounded-2xl shadow-2xl overflow-hidden min-h-[500px]">
            <div className="zine-imposition-sheet grid grid-cols-4 grid-rows-2 gap-2 h-full border-2 border-dashed border-slate-300 p-2">
              {[8, 1, 4, 5, 7, 2, 3, 6].map((pageNum) => {
                const pageData = activeBooklet.pages.find(p => p.pageNumber === pageNum);
                return (
                  <div key={pageNum} className="zine-page-cell border border-slate-300 p-3 bg-white flex flex-col justify-between h-48 rounded">
                    <div>
                      <div className="flex items-center justify-between text-[9px] font-mono text-slate-400 border-b border-slate-200 pb-1 mb-1">
                        <span>PAGE {pageNum}</span>
                        <span>{pageData?.contentType.toUpperCase()}</span>
                      </div>
                      <h4 className="font-bold text-xs text-slate-900">{pageData?.title}</h4>
                      <p className="text-[10px] text-slate-600 mt-1 line-clamp-3">{pageData?.bodyText}</p>
                    </div>
                    <div className="flex items-center justify-between text-[8px] font-mono text-slate-400 border-t border-slate-100 pt-1">
                      <span className="font-bold text-slate-800">[QR CODE]</span>
                      <span>Utensil • Pg {pageNum}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
