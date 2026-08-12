import React, { useState, useEffect } from 'react';
import { ProtocolStep, UserAccount, AISolution, PromptLibrary, PromptItem, BookletTemplate, MarketMetric, SecurityAlertNotification } from './types';
import { 
  INITIAL_RESEARCH_AREAS, 
  INITIAL_SOLUTIONS, 
  INITIAL_PROMPT_LIBRARIES, 
  INITIAL_BOOKLET_TEMPLATES, 
  INITIAL_MARKET_METRICS,
  DEFAULT_SENIOR_USER 
} from './data/initialData';

import { Navbar } from './components/Navbar';
import { VoiceAssistantBanner } from './components/VoiceAssistantBanner';
import { DashboardView } from './components/DashboardView';
import { Step1Solutions } from './components/Step1Solutions';
import { Step2Prompts } from './components/Step2Prompts';
import { Step3BookletStudio } from './components/Step3BookletStudio';
import { Step4Analytics } from './components/Step4Analytics';
import { SimulationSuite } from './components/SimulationSuite';
import { SeniorAccountModal } from './components/SeniorAccountModal';
import { VoiceSecurityHotline } from './components/VoiceSecurityHotline';
import { FoldingGuideModal } from './components/FoldingGuideModal';

export const App: React.FC = () => {
  // Navigation & User State
  const [currentStep, setStep] = useState<ProtocolStep>('dashboard');
  const [userAccount, setUserAccount] = useState<UserAccount | null>(DEFAULT_SENIOR_USER);
  const [seniorMode, setSeniorMode] = useState<boolean>(false);
  const [voiceAssistantActive, setVoiceAssistantActive] = useState<boolean>(false);
  const [voiceText, setVoiceText] = useState<string>("Welcome to the Utensil Theories Transfer Protocol Studio.");

  // Data Collections with LocalStorage Persistence
  const [solutions, setSolutions] = useState<AISolution[]>(() => {
    const saved = localStorage.getItem('uttp_solutions');
    return saved ? JSON.parse(saved) : INITIAL_SOLUTIONS;
  });

  const [libraries, setLibraries] = useState<PromptLibrary[]>(() => {
    const saved = localStorage.getItem('uttp_libraries');
    return saved ? JSON.parse(saved) : INITIAL_PROMPT_LIBRARIES;
  });

  const [booklets, setBooklets] = useState<BookletTemplate[]>(() => {
    const saved = localStorage.getItem('uttp_booklets');
    return saved ? JSON.parse(saved) : INITIAL_BOOKLET_TEMPLATES;
  });

  const [activeBooklet, setActiveBooklet] = useState<BookletTemplate>(booklets[0]);

  const [metrics, setMetrics] = useState<MarketMetric[]>(() => {
    const saved = localStorage.getItem('uttp_metrics');
    return saved ? JSON.parse(saved) : INITIAL_MARKET_METRICS;
  });

  // Modal States
  const [showAccountModal, setShowAccountModal] = useState<boolean>(false);
  const [showPhoneHotlineModal, setShowPhoneHotlineModal] = useState<boolean>(false);
  const [showFoldingGuideModal, setShowFoldingGuideModal] = useState<boolean>(false);

  // Sync to LocalStorage
  useEffect(() => {
    localStorage.setItem('uttp_solutions', JSON.stringify(solutions));
  }, [solutions]);

  useEffect(() => {
    localStorage.setItem('uttp_libraries', JSON.stringify(libraries));
  }, [libraries]);

  useEffect(() => {
    localStorage.setItem('uttp_booklets', JSON.stringify(booklets));
  }, [booklets]);

  useEffect(() => {
    localStorage.setItem('uttp_metrics', JSON.stringify(metrics));
  }, [metrics]);

  // Senior Accessibility Body Class Toggle
  useEffect(() => {
    if (seniorMode) {
      document.body.classList.add('senior-mode');
    } else {
      document.body.classList.remove('senior-mode');
    }
  }, [seniorMode]);

  // Calculations for Navbar metrics
  const totalDistributed = metrics.reduce((acc, m) => acc + m.distributedCount, 0);
  const totalSold = metrics.reduce((acc, m) => acc + m.soldCount, 0);
  const totalRevenue = metrics.reduce((acc, m) => acc + m.totalRevenue, 0);
  const totalPromptsCount = libraries.reduce((acc, l) => acc + l.prompts.length, 0);

  // Handler Actions
  const handleAddSolution = (newSol: AISolution) => {
    setSolutions([newSol, ...solutions]);
  };

  const handleAddPromptToLibrary = (libId: string, prompt: PromptItem) => {
    setLibraries(libraries.map(lib => {
      if (lib.id === libId) {
        return { ...lib, prompts: [prompt, ...lib.prompts] };
      }
      return lib;
    }));
  };

  const handleSendSolutionToPrompt = (sol: AISolution) => {
    setStep('step2');
    setVoiceText(`Prompt Studio opened for ${sol.title}.`);
  };

  const handleSendPromptToBooklet = (prompt: PromptItem) => {
    const updatedPages = [...activeBooklet.pages];
    if (updatedPages[1]) {
      updatedPages[1] = {
        ...updatedPages[1],
        title: prompt.title,
        promptBox: prompt.compiledPrompt
      };
    }
    const updatedBooklet = { ...activeBooklet, pages: updatedPages };
    setActiveBooklet(updatedBooklet);
    setBooklets(booklets.map(b => b.id === updatedBooklet.id ? updatedBooklet : b));
    setStep('step3');
    setVoiceText(`Prompt inserted into Page 2 of ${activeBooklet.title}.`);
  };

  const handleSaveBooklet = (updatedBooklet: BookletTemplate) => {
    setBooklets(booklets.map(b => b.id === updatedBooklet.id ? updatedBooklet : b));
  };

  const handleAddMetric = (newMetric: MarketMetric) => {
    setMetrics([newMetric, ...metrics]);
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] text-slate-100 flex flex-col font-sans selection:bg-cyan-500 selection:text-slate-950">
      
      {/* Top Navbar */}
      <Navbar
        currentStep={currentStep}
        setStep={(step) => {
          setStep(step);
          setVoiceText(`Navigated to ${step.toUpperCase()}.`);
        }}
        userAccount={userAccount}
        openAccountModal={() => setShowAccountModal(true)}
        openPhoneHotlineModal={() => setShowPhoneHotlineModal(true)}
        seniorMode={seniorMode}
        setSeniorMode={setSeniorMode}
        voiceAssistantActive={voiceAssistantActive}
        toggleVoiceAssistant={() => setVoiceAssistantActive(!voiceAssistantActive)}
        totalBookletsCount={booklets.length}
        totalPromptsCount={totalPromptsCount}
      />

      {/* Voice Assistant Banner */}
      <VoiceAssistantBanner
        active={voiceAssistantActive}
        onClose={() => setVoiceAssistantActive(false)}
        currentPromptText={voiceText}
      />

      {/* Main View Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {currentStep === 'dashboard' && (
          <DashboardView
            setStep={setStep}
            booklets={booklets}
            solutions={solutions}
            totalDistributed={totalDistributed}
            totalSold={totalSold}
            totalRevenue={totalRevenue}
            openFoldingGuide={() => setShowFoldingGuideModal(true)}
            openAccountModal={() => setShowAccountModal(true)}
            openPhoneHotline={() => setShowPhoneHotlineModal(true)}
          />
        )}

        {currentStep === 'step1' && (
          <Step1Solutions
            solutions={solutions}
            researchAreas={INITIAL_RESEARCH_AREAS}
            onAddSolution={handleAddSolution}
            onSendToPromptStudio={handleSendSolutionToPrompt}
          />
        )}

        {currentStep === 'step2' && (
          <Step2Prompts
            libraries={libraries}
            onAddPromptToLibrary={handleAddPromptToLibrary}
            onSendPromptToBooklet={handleSendPromptToBooklet}
          />
        )}

        {currentStep === 'step3' && (
          <Step3BookletStudio
            booklets={booklets}
            activeBooklet={activeBooklet}
            setActiveBooklet={setActiveBooklet}
            onSaveBooklet={handleSaveBooklet}
            openFoldingGuide={() => setShowFoldingGuideModal(true)}
          />
        )}

        {currentStep === 'step4' && (
          <Step4Analytics
            metrics={metrics}
            onAddMetric={handleAddMetric}
          />
        )}

        {currentStep === 'simulations' && (
          <SimulationSuite />
        )}

      </main>

      {/* Modals */}
      {showAccountModal && (
        <SeniorAccountModal
          userAccount={userAccount}
          setUserAccount={setUserAccount}
          onClose={() => setShowAccountModal(false)}
          openPhoneHotline={() => {
            setShowAccountModal(false);
            setShowPhoneHotlineModal(true);
          }}
        />
      )}

      {showPhoneHotlineModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <VoiceSecurityHotline
            userAccount={userAccount}
            onClose={() => setShowPhoneHotlineModal(false)}
          />
        </div>
      )}

      {showFoldingGuideModal && (
        <FoldingGuideModal
          onClose={() => setShowFoldingGuideModal(false)}
        />
      )}

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/60 py-6 text-center text-xs text-slate-500 font-mono no-print">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>🚀 Utensil Theories Transfer Protocol v2.6 • AI Learning Materials System</span>
          <span>Tested on Google Gemini & Microsoft Copilot • Open Educational Resource</span>
        </div>
      </footer>

    </div>
  );
};

export default App;
