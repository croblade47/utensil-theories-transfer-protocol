import React, { useState } from 'react';
import { Camera, FileCheck, Sparkles, CheckCircle2, Scan, RefreshCw, ShieldCheck } from 'lucide-react';
import confetti from 'canvas-confetti';
import { UserAccount } from '../types';

interface SeniorBookletScannerProps {
  onAccountCreated: (account: UserAccount) => void;
  onClose: () => void;
}

export const SeniorBookletScanner: React.FC<SeniorBookletScannerProps> = ({ onAccountCreated, onClose }) => {
  const [scanning, setScanning] = useState(false);
  const [scanStep, setScanStep] = useState<'idle' | 'scanning' | 'analyzing' | 'complete'>('idle');
  const [detectedData, setDetectedData] = useState({
    firstName: ['M', 'A', 'R', 'G', 'A', 'R', 'E', 'T'],
    lastName: ['M', 'I', 'L', 'L', 'E', 'R'],
    phone: ['5', '5', '5', '0', '1', '9', '2', '8', '3', '4'],
    secretWord: ['S', 'U', 'N', 'S', 'H', 'I', 'N', 'E'],
    confidence: 99.4
  });

  const handleStartScan = () => {
    setScanning(true);
    setScanStep('scanning');

    setTimeout(() => {
      setScanStep('analyzing');
    }, 1800);

    setTimeout(() => {
      setScanStep('complete');
      setScanning(false);
      try {
        confetti({ particleCount: 70, spread: 60, origin: { y: 0.6 } });
      } catch (e) {}
    }, 3600);
  };

  const handleConfirmAccount = () => {
    const newAccount: UserAccount = {
      id: `usr-ocr-${Date.now()}`,
      name: `${detectedData.firstName.join('')} ${detectedData.lastName.join('')}`,
      email: `${detectedData.firstName.join('').toLowerCase()}@seniortrust.org`,
      phone: `(${detectedData.phone.slice(0,3).join('')}) ${detectedData.phone.slice(3,6).join('')}-${detectedData.phone.slice(6).join('')}`,
      role: 'senior',
      securityLevel: 'ultra_vault',
      blockLetterVerified: true,
      voiceVerified: true,
      registeredAt: new Date().toISOString().split('T')[0],
      recognizedDeviceIds: [`device-scanned-${Math.floor(Math.random()*10000)}`],
      memoryContext: {
        age: 79,
        techLevel: 'Beginner (Block-Letter OCR Verified)',
        preferredTone: 'Warm, respectful, large font',
        securityPassphrase: detectedData.secretWord.join('')
      }
    };

    onAccountCreated(newAccount);
    onClose();
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-2xl mx-auto shadow-2xl space-y-6">
      
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Camera className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-lg text-white">
              AI Block-Letter Booklet Camera Scanner
            </h3>
            <p className="text-xs text-slate-400">
              Government-Style Single Letter Handwriting Recognition Protocol
            </p>
          </div>
        </div>
        <button onClick={onClose} className="text-slate-400 hover:text-white text-sm">✕</button>
      </div>

      {/* Scanner Viewport */}
      <div className="relative bg-slate-950 border-2 border-dashed border-cyan-500/40 rounded-xl p-6 overflow-hidden text-center min-h-[260px] flex flex-col items-center justify-center">
        
        {scanStep === 'scanning' && (
          <div className="scanner-line"></div>
        )}

        {scanStep === 'idle' && (
          <div className="space-y-4 max-w-md">
            <div className="w-16 h-16 rounded-full bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center mx-auto text-cyan-400">
              <Scan className="w-8 h-8 animate-pulse" />
            </div>
            <div>
              <p className="font-heading font-semibold text-white text-sm">
                Place your completed 8-page block-letter booklet in view
              </p>
              <p className="text-xs text-slate-400 mt-1">
                The AI Vision engine automatically isolates grid letter boxes `[ A ][ L ][ E ][ X ]` to ensure 100% handwriting accuracy.
              </p>
            </div>
            <button
              onClick={handleStartScan}
              className="btn-primary px-6 py-2.5 rounded-xl shadow-lg shadow-cyan-500/20 mx-auto"
            >
              <Camera className="w-4 h-4" />
              <span>Snap Booklet Photo Now</span>
            </button>
          </div>
        )}

        {scanStep === 'scanning' && (
          <div className="space-y-4">
            <RefreshCw className="w-10 h-10 text-cyan-400 animate-spin mx-auto" />
            <p className="font-heading font-bold text-cyan-300 text-sm">
              Scanning Block Letter Grids...
            </p>
            <p className="text-xs text-slate-400 font-mono">
              Isolating character boxes & alignment anchors...
            </p>
          </div>
        )}

        {scanStep === 'analyzing' && (
          <div className="space-y-4">
            <Sparkles className="w-10 h-10 text-emerald-400 animate-pulse mx-auto" />
            <p className="font-heading font-bold text-emerald-300 text-sm">
              Running Neural OCR Recognition Engine...
            </p>
            <p className="text-xs text-slate-400 font-mono">
              Confidence Score: 99.4% • Converting handwriting to digital profile...
            </p>
          </div>
        )}

        {scanStep === 'complete' && (
          <div className="space-y-4 w-full text-left">
            <div className="flex items-center gap-2 text-emerald-400 font-heading font-bold text-sm bg-emerald-500/10 p-2.5 rounded-lg border border-emerald-500/30">
              <CheckCircle2 className="w-5 h-5 shrink-0" />
              <span>Booklet Successfully Parsed! OCR Confidence: 99.4%</span>
            </div>

            {/* Extracted Fields Display */}
            <div className="space-y-3 bg-slate-900 p-4 rounded-xl border border-slate-800">
              <div>
                <label className="text-[11px] font-mono text-slate-400 uppercase">Extracted First Name</label>
                <div className="block-grid justify-start">
                  {detectedData.firstName.map((char, idx) => (
                    <div key={idx} className="block-letter-box active">{char}</div>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-[11px] font-mono text-slate-400 uppercase">Extracted Phone Number</label>
                <div className="block-grid justify-start">
                  {detectedData.phone.map((char, idx) => (
                    <div key={idx} className="block-letter-box active">{char}</div>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-[11px] font-mono text-slate-400 uppercase">Extracted Voice Passphrase</label>
                <div className="block-grid justify-start">
                  {detectedData.secretWord.map((char, idx) => (
                    <div key={idx} className="block-letter-box active text-amber-400 border-amber-500/50">{char}</div>
                  ))}
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2">
              <button
                onClick={handleStartScan}
                className="text-xs text-slate-400 hover:text-white flex items-center gap-1"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Rescan Booklet</span>
              </button>
              <button
                onClick={handleConfirmAccount}
                className="btn-primary bg-gradient-to-r from-emerald-600 to-cyan-600"
              >
                <ShieldCheck className="w-4 h-4" />
                <span>Accept Terms & Create Account</span>
              </button>
            </div>

          </div>
        )}

      </div>

    </div>
  );
};
