import React from 'react';
import { 
  Rocket, 
  LayoutDashboard, 
  Search, 
  Terminal, 
  BookOpen, 
  BarChart3, 
  PlayCircle, 
  UserCheck, 
  Mic, 
  ShieldCheck, 
  PhoneCall,
  Volume2
} from 'lucide-react';
import { ProtocolStep, UserAccount } from '../types';

interface NavbarProps {
  currentStep: ProtocolStep;
  setStep: (step: ProtocolStep) => void;
  userAccount: UserAccount | null;
  openAccountModal: () => void;
  openPhoneHotlineModal: () => void;
  seniorMode: boolean;
  setSeniorMode: (val: boolean) => void;
  voiceAssistantActive: boolean;
  toggleVoiceAssistant: () => void;
  totalBookletsCount: number;
  totalPromptsCount: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentStep,
  setStep,
  userAccount,
  openAccountModal,
  openPhoneHotlineModal,
  seniorMode,
  setSeniorMode,
  voiceAssistantActive,
  toggleVoiceAssistant,
  totalBookletsCount,
  totalPromptsCount
}) => {
  return (
    <header className="sticky top-0 z-40 bg-slate-950/80 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo & Protocol Badge */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 via-cyan-400 to-emerald-400 p-0.5 flex items-center justify-center shadow-lg shadow-indigo-500/20 cursor-pointer" onClick={() => setStep('dashboard')}>
              <div className="w-full h-full bg-slate-900 rounded-[10px] flex items-center justify-center">
                <Rocket className="w-5 h-5 text-cyan-400" />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-heading font-extrabold text-lg bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                  Utensil Theories
                </span>
                <span className="bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-xs px-2 py-0.5 rounded-full font-mono font-semibold">
                  UTTP v2.6
                </span>
              </div>
              <p className="text-xs text-slate-400 font-medium">Transfer Protocol & Production Studio</p>
            </div>
          </div>

          {/* Core Navigation Tabs */}
          <nav className="hidden md:flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setStep('dashboard')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                currentStep === 'dashboard'
                  ? 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <LayoutDashboard className="w-4 h-4" />
              <span>Dashboard</span>
            </button>

            <button
              onClick={() => setStep('step1')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                currentStep === 'step1'
                  ? 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Search className="w-4 h-4 text-cyan-400" />
              <span>Step 1: Solutions</span>
            </button>

            <button
              onClick={() => setStep('step2')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                currentStep === 'step2'
                  ? 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <Terminal className="w-4 h-4 text-emerald-400" />
              <span>Step 2: Prompts</span>
              <span className="bg-emerald-500/20 text-emerald-300 text-xs px-1.5 py-0.2 rounded-full font-mono">
                {totalPromptsCount}
              </span>
            </button>

            <button
              onClick={() => setStep('step3')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                currentStep === 'step3'
                  ? 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <BookOpen className="w-4 h-4 text-amber-400" />
              <span>Step 3: Zine Studio</span>
              <span className="bg-amber-500/20 text-amber-300 text-xs px-1.5 py-0.2 rounded-full font-mono">
                {totalBookletsCount}
              </span>
            </button>

            <button
              onClick={() => setStep('step4')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                currentStep === 'step4'
                  ? 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <BarChart3 className="w-4 h-4 text-rose-400" />
              <span>Step 4: Analytics</span>
            </button>

            <button
              onClick={() => setStep('simulations')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                currentStep === 'simulations'
                  ? 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <PlayCircle className="w-4 h-4 text-indigo-400" />
              <span>Simulations</span>
            </button>
          </nav>

          {/* Quick Actions, User Profile & Hotline */}
          <div className="flex items-center gap-2">
            
            {/* Voice Assistant Toggle */}
            <button
              onClick={toggleVoiceAssistant}
              title="Toggle Senior Voice Companion (Reads screens & accepts spoken answers)"
              className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                voiceAssistantActive
                  ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-300 shadow-md shadow-emerald-500/20 animate-pulse'
                  : 'bg-slate-900 border-slate-700 text-slate-400 hover:text-white'
              }`}
            >
              <Volume2 className="w-4 h-4" />
              <span className="hidden sm:inline">Voice Assistant</span>
            </button>

            {/* Phone Security Hotline Button */}
            <button
              onClick={openPhoneHotlineModal}
              title="Simulate Calling Voice Verification Hotline"
              className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 hover:bg-indigo-500/20 transition-all"
            >
              <PhoneCall className="w-4 h-4 text-indigo-400" />
              <span className="hidden sm:inline">1-800 Hotline</span>
            </button>

            {/* Senior Accessibility Mode Toggle */}
            <button
              onClick={() => setSeniorMode(!seniorMode)}
              className={`px-2.5 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                seniorMode
                  ? 'bg-amber-500/20 border-amber-500/50 text-amber-300'
                  : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white'
              }`}
              title="Toggle Large-Print Senior High Contrast Mode"
            >
              {seniorMode ? 'Senior Mode [ON]' : 'Senior Mode'}
            </button>

            {/* User Account Button */}
            <button
              onClick={openAccountModal}
              className="flex items-center gap-2 bg-gradient-to-r from-slate-800 to-slate-900 border border-slate-700 hover:border-cyan-500/50 px-3 py-1.5 rounded-xl transition-all"
            >
              <UserCheck className="w-4 h-4 text-cyan-400" />
              <div className="text-left hidden lg:block">
                <p className="text-xs font-semibold text-white leading-tight">
                  {userAccount ? userAccount.name : 'Sign In / Register'}
                </p>
                <p className="text-[10px] text-cyan-400 font-mono">
                  {userAccount ? `${userAccount.role.toUpperCase()} • ${userAccount.securityLevel === 'ultra_vault' ? '🔒 Vault' : 'Standard'}` : 'Guest User'}
                </p>
              </div>
            </button>
          </div>

        </div>
      </div>
    </header>
  );
};
