import React, { useState } from 'react';
import { UserCheck, ShieldCheck, Camera, PhoneCall, Sparkles, Key, FileText, Lock } from 'lucide-react';
import { UserAccount } from '../types';
import { SeniorBookletScanner } from './SeniorBookletScanner';

interface SeniorAccountModalProps {
  userAccount: UserAccount | null;
  setUserAccount: (account: UserAccount | null) => void;
  onClose: () => void;
  openPhoneHotline: () => void;
}

export const SeniorAccountModal: React.FC<SeniorAccountModalProps> = ({
  userAccount,
  setUserAccount,
  onClose,
  openPhoneHotline
}) => {
  const [activeTab, setActiveTab] = useState<'profile' | 'register' | 'ocr_scan'>('profile');
  const [formName, setFormName] = useState('');
  const [formPhone, setFormPhone] = useState('');
  const [formPassphrase, setFormPassphrase] = useState('');

  const handleRegisterQuick = (role: 'admin' | 'senior') => {
    if (!formName) {
      alert("Please enter your name.");
      return;
    }

    const newAcc: UserAccount = {
      id: `usr-${Date.now()}`,
      name: formName,
      email: `${formName.toLowerCase().replace(/\s+/g, '.')}@utensiltheories.org`,
      phone: formPhone || '(555) 019-2834',
      role,
      securityLevel: role === 'senior' ? 'ultra_vault' : 'standard',
      blockLetterVerified: false,
      voiceVerified: true,
      registeredAt: new Date().toISOString().split('T')[0],
      recognizedDeviceIds: ['device-current-session'],
      memoryContext: {
        preferredTone: role === 'senior' ? 'Warm, direct, large font' : 'Professional technical',
        securityPassphrase: formPassphrase || 'SUNSHINE'
      }
    };

    setUserAccount(newAcc);
    setActiveTab('profile');
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-xl w-full shadow-2xl space-y-6">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-cyan-500 flex items-center justify-center text-white font-bold">
              <UserCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-heading font-bold text-lg text-white">
                User Account & Security Management
              </h3>
              <p className="text-xs text-slate-400">
                Utensil Theories Transfer Protocol Security Hub
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-sm">✕</button>
        </div>

        {/* OCR Scanner Mode */}
        {activeTab === 'ocr_scan' ? (
          <SeniorBookletScanner
            onAccountCreated={(acc) => {
              setUserAccount(acc);
              setActiveTab('profile');
            }}
            onClose={() => setActiveTab('profile')}
          />
        ) : (
          <>
            {/* Tabs */}
            <div className="flex gap-2 bg-slate-950 p-1 rounded-xl border border-slate-800">
              <button
                onClick={() => setActiveTab('profile')}
                className={`flex-1 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeTab === 'profile' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'
                }`}
              >
                Current Profile
              </button>
              <button
                onClick={() => setActiveTab('register')}
                className={`flex-1 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeTab === 'register' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'
                }`}
              >
                Register New User
              </button>
            </div>

            {activeTab === 'profile' && userAccount && (
              <div className="space-y-4">
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-heading font-bold text-white text-base">{userAccount.name}</h4>
                      <p className="text-xs text-slate-400 font-mono">{userAccount.email}</p>
                    </div>
                    <span className={`px-2.5 py-1 rounded-full text-xs font-mono font-bold ${
                      userAccount.role === 'senior' ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                    }`}>
                      {userAccount.role.toUpperCase()}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-xs border-t border-slate-800 pt-3">
                    <div>
                      <span className="text-slate-500 font-mono">Security Level:</span>
                      <p className="font-semibold text-emerald-400 flex items-center gap-1 mt-0.5">
                        <Lock className="w-3.5 h-3.5" />
                        {userAccount.securityLevel === 'ultra_vault' ? 'Ultra Vault (Reverse Call Protected)' : 'Standard'}
                      </p>
                    </div>
                    <div>
                      <span className="text-slate-500 font-mono">Handwriting Block OCR:</span>
                      <p className="font-semibold text-cyan-400 mt-0.5">
                        {userAccount.blockLetterVerified ? '✓ Verified' : 'Standard'}
                      </p>
                    </div>
                  </div>

                  {/* Remember Me Context Card */}
                  {userAccount.memoryContext && (
                    <div className="bg-slate-900 p-3 rounded-lg border border-slate-800 text-xs space-y-1">
                      <span className="text-[11px] font-mono text-indigo-400 font-bold uppercase">Remember Me Context Memory</span>
                      <p className="text-slate-300"><strong className="text-white">Tone:</strong> {userAccount.memoryContext.preferredTone}</p>
                      {userAccount.memoryContext.securityPassphrase && (
                        <p className="text-slate-300"><strong className="text-white">Voice Passphrase:</strong> {userAccount.memoryContext.securityPassphrase}</p>
                      )}
                    </div>
                  )}
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={openPhoneHotline}
                    className="flex-1 btn-secondary text-xs justify-center py-2"
                  >
                    <PhoneCall className="w-4 h-4 text-indigo-400" />
                    <span>Test Voice Hotline</span>
                  </button>
                  <button
                    onClick={() => setUserAccount(null)}
                    className="text-xs text-rose-400 hover:text-rose-300 px-3 py-2 border border-rose-500/30 rounded-xl"
                  >
                    Sign Out
                  </button>
                </div>
              </div>
            )}

            {activeTab === 'register' && (
              <div className="space-y-4">
                
                {/* 1-Click OCR Scanner Option Banner */}
                <div className="bg-gradient-to-r from-cyan-950/80 to-indigo-950/80 border border-cyan-500/40 p-4 rounded-xl flex items-center justify-between">
                  <div>
                    <h5 className="font-heading font-bold text-sm text-cyan-300">
                      Scan Printable Block-Letter Booklet
                    </h5>
                    <p className="text-xs text-slate-300 mt-0.5">
                      Snap photo of paper form `[ A ][ L ][ E ][ X ]` for instant setup.
                    </p>
                  </div>
                  <button
                    onClick={() => setActiveTab('ocr_scan')}
                    className="btn-primary text-xs px-3 py-1.5 shrink-0"
                  >
                    <Camera className="w-3.5 h-3.5" />
                    <span>AI Camera Scan</span>
                  </button>
                </div>

                {/* Form Registration */}
                <div className="space-y-3">
                  <div>
                    <label className="text-xs font-semibold text-slate-300 block mb-1">Full Name</label>
                    <input
                      type="text"
                      value={formName}
                      onChange={(e) => setFormName(e.target.value)}
                      placeholder="e.g. Margaret Miller"
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:border-indigo-500 outline-none"
                    />
                  </div>

                  <div>
                    <label className="text-xs font-semibold text-slate-300 block mb-1">Phone Number (For Reverse Call Alerts)</label>
                    <input
                      type="text"
                      value={formPhone}
                      onChange={(e) => setFormPhone(e.target.value)}
                      placeholder="(555) 019-2834"
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:border-indigo-500 outline-none"
                    />
                  </div>

                  <div>
                    <label className="text-xs font-semibold text-slate-300 block mb-1">Voice Secret Passphrase (Spoken on Phone)</label>
                    <input
                      type="text"
                      value={formPassphrase}
                      onChange={(e) => setFormPassphrase(e.target.value)}
                      placeholder="e.g. SUNSHINE"
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:border-indigo-500 outline-none font-mono"
                    />
                  </div>

                  <div className="flex gap-2 pt-2">
                    <button
                      onClick={() => handleRegisterQuick('senior')}
                      className="flex-1 btn-primary bg-gradient-to-r from-amber-600 to-indigo-600 text-xs justify-center py-2.5"
                    >
                      <ShieldCheck className="w-4 h-4" />
                      <span>Register Senior User (Ultra-Vault)</span>
                    </button>
                    <button
                      onClick={() => handleRegisterQuick('admin')}
                      className="btn-secondary text-xs px-4 py-2.5"
                    >
                      Register Admin
                    </button>
                  </div>
                </div>

              </div>
            )}
          </>
        )}

      </div>
    </div>
  );
};
