import React, { useState, useEffect } from 'react';
import { Volume2, Mic, MicOff, StopCircle, Sparkles, CheckCircle2 } from 'lucide-react';

interface VoiceAssistantBannerProps {
  active: boolean;
  onClose: () => void;
  currentPromptText?: string;
  onTranscriptReceived?: (transcript: string) => void;
}

export const VoiceAssistantBanner: React.FC<VoiceAssistantBannerProps> = ({
  active,
  onClose,
  currentPromptText = "Welcome to the Utensil Theories Senior Voice Assistant. Tap 'Read Screen' to hear options out loud, or tap 'Speak Answer' to fill forms with your voice.",
  onTranscriptReceived
}) => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [lastTranscript, setLastTranscript] = useState('');

  // Text to Speech
  const speakText = (text: string) => {
    if (!('speechSynthesis' in window)) {
      alert("Text-to-speech is not supported in this browser.");
      return;
    }
    window.speechSynthesis.cancel(); // stop previous speech
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9; // clear, moderate pace for elderly listeners
    utterance.pitch = 1.0;
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    window.speechSynthesis.speak(utterance);
  };

  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  // Speech Recognition
  const startListening = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      // Fallback simulation for unsupported browsers
      const simulatedAnswer = prompt("Speech Recognition API not supported natively in this browser version. Enter your spoken answer below:");
      if (simulatedAnswer && onTranscriptReceived) {
        setLastTranscript(simulatedAnswer);
        onTranscriptReceived(simulatedAnswer);
      }
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => setIsListening(true);
      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setLastTranscript(transcript);
        if (onTranscriptReceived) {
          onTranscriptReceived(transcript);
        }
        setIsListening(false);
        speakText(`I heard: ${transcript}`);
      };
      recognition.onerror = () => setIsListening(false);
      recognition.onend = () => setIsListening(false);

      recognition.start();
    } catch (e) {
      setIsListening(false);
    }
  };

  useEffect(() => {
    if (active) {
      speakText("Senior Voice Companion is ready.");
    } else {
      stopSpeaking();
    }
  }, [active]);

  if (!active) return null;

  return (
    <div className="bg-gradient-to-r from-emerald-950/90 via-slate-900 to-indigo-950/90 border-b border-emerald-500/30 p-3 sm:p-4 transition-all animate-fadeIn">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
        
        {/* Banner Title & Message */}
        <div className="flex items-center gap-3 text-center sm:text-left">
          <div className="w-10 h-10 rounded-full bg-emerald-500/20 border border-emerald-400/40 flex items-center justify-center shrink-0">
            <Volume2 className={`w-5 h-5 text-emerald-400 ${isSpeaking ? 'animate-bounce' : ''}`} />
          </div>
          <div>
            <div className="flex items-center gap-2 justify-center sm:justify-start">
              <span className="font-heading font-bold text-sm text-emerald-300">Senior Voice Companion</span>
              <span className="bg-emerald-500/20 text-emerald-300 text-[10px] px-2 py-0.5 rounded-full font-mono">ACTIVE</span>
            </div>
            <p className="text-xs sm:text-sm text-slate-200 font-medium max-w-2xl line-clamp-2">
              "{currentPromptText}"
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2 shrink-0">
          
          {/* Read Screen Button */}
          {isSpeaking ? (
            <button
              onClick={stopSpeaking}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-rose-500/20 border border-rose-500/40 text-rose-300 hover:bg-rose-500/30 transition-all"
            >
              <StopCircle className="w-4 h-4" />
              <span>Stop Reading</span>
            </button>
          ) : (
            <button
              onClick={() => speakText(currentPromptText)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 hover:bg-emerald-500/30 transition-all"
            >
              <Volume2 className="w-4 h-4" />
              <span>Read Aloud</span>
            </button>
          )}

          {/* Speak Answer Button */}
          <button
            onClick={startListening}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
              isListening
                ? 'bg-amber-500/30 border-amber-500 text-amber-200 animate-pulse'
                : 'bg-indigo-500/20 border-indigo-500/40 text-indigo-300 hover:bg-indigo-500/30'
            }`}
          >
            {isListening ? <Mic className="w-4 h-4 text-amber-400 animate-bounce" /> : <MicOff className="w-4 h-4" />}
            <span>{isListening ? 'Listening...' : 'Speak Answer'}</span>
          </button>

          {/* Close Banner Button */}
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white px-2 py-1 text-xs"
          >
            ✕
          </button>
        </div>

      </div>

      {lastTranscript && (
        <div className="max-w-7xl mx-auto mt-2 pt-2 border-t border-emerald-500/20 flex items-center gap-2 text-xs text-emerald-300 font-mono">
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
          <span>Last Spoken Transcript: "{lastTranscript}"</span>
        </div>
      )}
    </div>
  );
};
