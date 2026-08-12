import React, { useState } from 'react';
import { PhoneCall, ShieldAlert, KeyRound, Smartphone, AlertTriangle, CheckCircle2, Lock, Volume2, StopCircle } from 'lucide-react';
import { UserAccount, SecurityAlertNotification } from '../types';

interface VoiceSecurityHotlineProps {
  userAccount: UserAccount | null;
  onClose: () => void;
  onSecurityAlertFired?: (alert: SecurityAlertNotification) => void;
}

export const VoiceSecurityHotline: React.FC<VoiceSecurityHotlineProps> = ({
  userAccount,
  onClose,
  onSecurityAlertFired
}) => {
  const [callState, setCallState] = useState<'idle' | 'calling' | 'speaking' | 'otp_issued'>('idle');
  const [issuedOtp, setIssuedOtp] = useState<string | null>(null);
  const [badActorTesting, setBadActorTesting] = useState(false);
  const [alertNotification, setAlertNotification] = useState<SecurityAlertNotification | null>(null);
  const [audioAlertPlaying, setAudioAlertPlaying] = useState(false);

  const startHotlineCall = () => {
    setCallState('calling');
    setTimeout(() => {
      setCallState('speaking');
    }, 1500);

    setTimeout(() => {
      const generatedOtp = Math.floor(1000 + Math.random() * 9000).toString();
      setIssuedOtp(generatedOtp);
      setCallState('otp_issued');
    }, 3500);
  };

  const playVoiceAlertAudio = (text: string) => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95;
    utterance.pitch = 0.9;
    utterance.onstart = () => setAudioAlertPlaying(true);
    utterance.onend = () => setAudioAlertPlaying(false);
    utterance.onerror = () => setAudioAlertPlaying(false);
    window.speechSynthesis.speak(utterance);
  };

  const stopVoiceAlertAudio = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setAudioAlertPlaying(false);
    }
  };

  const simulateBadActorLogin = () => {
    if (!issuedOtp) {
      alert("Please dial hotline first to generate a dynamic passcode!");
      return;
    }

    setBadActorTesting(true);
    const newAlert: SecurityAlertNotification = {
      id: `alt-${Date.now()}`,
      timestamp: new Date().toLocaleTimeString(),
      attemptedLocation: 'New York, NY (Unrecognized Device)',
      attemptedIp: '198.51.100.42',
      deviceFingerprint: 'Chrome 122 on Windows (Unrecognized)',
      status: 'pending',
      passcodeIssued: issuedOtp
    };

    setAlertNotification(newAlert);
    if (onSecurityAlertFired) {
      onSecurityAlertFired(newAlert);
    }

    // Play automated phone call alert audio
    const alertMessage = `SECURITY ALERT FOR ${userAccount ? userAccount.name : 'ACCOUNT OWNER'}. A login attempt to your sensitive information vault was made from an unrecognized device using dynamic passcode ${issuedOtp.split('').join(' ')}. Device identification granting is required. Press 1 to authorize this device, or Press 2 to lock your account immediately.`;
    playVoiceAlertAudio(alertMessage);
  };

  const handleResolveAlert = (status: 'authorized' | 'blocked') => {
    if (alertNotification) {
      setAlertNotification({ ...alertNotification, status });
    }
    stopVoiceAlertAudio();
    if (status === 'blocked') {
      playVoiceAlertAudio("Account vault locked immediately. Unrecognized device has been blacklisted.");
    } else {
      playVoiceAlertAudio("Device authorized. Access granted for this session.");
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-2xl mx-auto shadow-2xl space-y-6">
      
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
            <PhoneCall className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-heading font-bold text-lg text-white">
              Voice Security Hotline & Reverse Call Protocol
            </h3>
            <p className="text-xs text-slate-400">
              1-800-UTENSIL Voice Verification & Device Identification Defense
            </p>
          </div>
        </div>
        <button onClick={onClose} className="text-slate-400 hover:text-white text-sm">✕</button>
      </div>

      {/* Grid: Hotline Call Simulator vs Bad Actor Threat Tester */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        {/* Left Box: Hotline Dialing */}
        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-bold text-indigo-400 uppercase">1-800-UTENSIL Hotline</span>
            <span className="bg-indigo-500/20 text-indigo-300 text-[10px] px-2 py-0.5 rounded-full font-mono">
              DYNAMIC OTP
            </span>
          </div>

          <div className="text-center py-4 space-y-3">
            <div className="w-14 h-14 rounded-full bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center mx-auto text-indigo-400">
              <PhoneCall className={`w-7 h-7 ${callState === 'calling' ? 'animate-bounce' : ''}`} />
            </div>

            {callState === 'idle' && (
              <div>
                <p className="text-sm font-semibold text-white">Dial Senior Hotline</p>
                <p className="text-xs text-slate-400 mt-1">Speak secret passphrase to receive dynamic passcode.</p>
                <button
                  onClick={startHotlineCall}
                  className="btn-primary mt-3 text-xs px-4 py-2"
                >
                  Dial 1-800-UTENSIL
                </button>
              </div>
            )}

            {callState === 'calling' && (
              <p className="text-xs text-indigo-300 font-mono animate-pulse">
                Dialing 1-800-UTENSIL... Connecting...
              </p>
            )}

            {callState === 'speaking' && (
              <p className="text-xs text-emerald-300 font-mono animate-pulse">
                Verifying Voice Sample: "SUNSHINE"... Passphrase Matched!
              </p>
            )}

            {callState === 'otp_issued' && issuedOtp && (
              <div className="space-y-2">
                <p className="text-xs text-slate-400">Your Dynamic Passcode:</p>
                <div className="text-2xl font-mono font-extrabold text-cyan-400 bg-slate-900 border border-cyan-500/40 py-2 rounded-lg tracking-widest">
                  {issuedOtp}
                </div>
                <p className="text-[11px] text-slate-400">Expires in 60s • Single-Use</p>
              </div>
            )}
          </div>
        </div>

        {/* Right Box: Bad Actor Threat Simulation */}
        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-bold text-rose-400 uppercase">Anti-Fraud Security Defense</span>
            <span className="bg-rose-500/20 text-rose-300 text-[10px] px-2 py-0.5 rounded-full font-mono">
              REVERSE CALL GUARD
            </span>
          </div>

          <div className="space-y-3">
            <p className="text-xs text-slate-300">
              Test what happens when an unauthorized user attempts to use your passcode on an unrecognized device.
            </p>

            <button
              onClick={simulateBadActorLogin}
              disabled={!issuedOtp}
              className={`w-full py-2.5 px-3 rounded-xl text-xs font-semibold flex items-center justify-center gap-2 transition-all ${
                issuedOtp
                  ? 'bg-rose-500/20 border border-rose-500/40 text-rose-300 hover:bg-rose-500/30'
                  : 'bg-slate-900 border border-slate-800 text-slate-600 cursor-not-allowed'
              }`}
            >
              <AlertTriangle className="w-4 h-4 text-rose-400" />
              <span>Simulate Bad Actor Login Attempt</span>
            </button>
          </div>
        </div>

      </div>

      {/* Reverse Call Security Alert Popup Modal */}
      {alertNotification && (
        <div className="bg-gradient-to-r from-rose-950/90 via-slate-950 to-amber-950/90 border-2 border-rose-500 rounded-xl p-4 space-y-3 animate-pulse shadow-2xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-rose-400 font-heading font-bold text-sm">
              <ShieldAlert className="w-5 h-5 shrink-0" />
              <span>REVERSE CALL ALERT: UNRECOGNIZED DEVICE LOGIN ATTEMPT!</span>
            </div>
            {audioAlertPlaying && (
              <button onClick={stopVoiceAlertAudio} className="text-xs text-rose-300 underline flex items-center gap-1">
                <StopCircle className="w-3.5 h-3.5" /> Stop Phone Call Audio
              </button>
            )}
          </div>

          <p className="text-xs text-slate-200">
            A login attempt to sensitive financial/health data was detected from IP <span className="font-mono text-amber-300">{alertNotification.attemptedIp}</span> using passcode <span className="font-mono text-cyan-300">{alertNotification.passcodeIssued}</span>.
          </p>

          <div className="flex items-center justify-between pt-2 border-t border-rose-500/30">
            <span className="text-xs text-slate-400 font-mono">
              Status: {alertNotification.status.toUpperCase()}
            </span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => handleResolveAlert('blocked')}
                className="bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs px-3 py-1.5 rounded-lg flex items-center gap-1"
              >
                <Lock className="w-3.5 h-3.5" />
                <span>BLOCK & LOCK VAULT</span>
              </button>
              <button
                onClick={() => handleResolveAlert('authorized')}
                className="bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs px-3 py-1.5 rounded-lg flex items-center gap-1"
              >
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>AUTHORIZE DEVICE</span>
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
