'use client';

import React, { useState, useEffect, useRef } from 'react';
import {
  Upload, Cpu, Zap, Activity, CheckCircle2,
  BrainCircuit, Database, Palette, Sparkles,
  ArrowRight, ShieldCheck, Play, Leaf, Fingerprint,
  Lock, LogIn, User, LayoutDashboard, History,
  BookOpen, MessageCircle, AlertTriangle, Phone, Star, Share2,
  Clock, Music, RefreshCw, Eye
} from 'lucide-react';
import {
  UnifiedAIChat,
  VeridianChatEnabled,
  LusaChatEnabled,
  NexusChatEnabled,
  CroChatEnabled,
  SaCoLuChatEnabled,
  ChatMessage,
  Task,
  EchoTrait,
  PsychProfile
} from '@/lib/unified-ai-system';

// --- UI Components ---

const AgentBadge = ({ name, status }: { name: string; status: 'online' | 'busy' | 'offline' }) => {
  const getIcon = () => {
    if (name === 'Veridian') return <BrainCircuit className="w-3 h-3 text-cyan-400" />;
    if (name.startsWith('Lu')) return <Palette className="w-3 h-3 text-purple-400" />;
    if (name === 'Nexus') return <Database className="w-3 h-3 text-emerald-400" />;
    if (name === 'Cro') return <Zap className="w-3 h-3 text-orange-400" />;
    if (name === 'SaCoLu') return <Leaf className="w-3 h-3 text-pink-400" />;
    return <Cpu className="w-3 h-3" />;
  };

  const getColor = () => {
    if (name === 'Veridian') return 'border-cyan-500/30 bg-cyan-950/40 text-cyan-100';
    if (name.startsWith('Lu')) return 'border-purple-500/30 bg-purple-950/40 text-purple-100';
    if (name === 'Nexus') return 'border-emerald-500/30 bg-emerald-950/40 text-emerald-100';
    if (name === 'Cro') return 'border-orange-500/30 bg-orange-950/40 text-orange-100';
    if (name === 'SaCoLu') return 'border-pink-500/30 bg-pink-950/40 text-pink-100';
    return 'border-gray-500/30 bg-gray-950/30';
  };

  return (
    <div className={`flex items-center space-x-2 px-3 py-1 rounded-lg border ${getColor()} transition-all duration-300`}>
      {getIcon()}
      <span className="text-[10px] font-bold tracking-wider uppercase">{name}</span>
      <div className={`w-1 h-1 rounded-full ${status === 'online' ? 'bg-green-400 animate-pulse' : 'bg-gray-500'}`} />
    </div>
  );
};

const TraitBar = ({ trait }: { trait: EchoTrait }) => (
  <div className="mb-2">
    <div className="flex justify-between items-end mb-1">
        <span className="text-[10px] font-bold text-gray-300 uppercase tracking-wider">{trait.name}</span>
        <span className="text-[10px] font-mono text-gray-400">{trait.score}%</span>
    </div>
    <div className="h-1.5 w-full bg-gray-800 rounded-full overflow-hidden">
        <div
            className="h-full rounded-full transition-all duration-1000 ease-out"
            style={{ width: `${trait.score}%`, backgroundColor: trait.color }}
        />
    </div>
  </div>
);

const ChatBubble = ({ msg }: { msg: ChatMessage }) => {
  const isUser = msg.sender === 'User';
  const isSystem = msg.sender === 'System';

  if (isSystem) {
    return (
      <div className="flex justify-center my-4">
        <div className="text-[9px] uppercase tracking-widest text-gray-600 flex items-center gap-2 bg-black/20 px-3 py-1 rounded-full">
          <Activity className="w-3 h-3" />
          {typeof msg.content === 'string' ? msg.content : 'System Event'}
        </div>
      </div>
    );
  }

  // Ritual Prompt (Lusa Distraction)
  if (msg.type === 'ritual_prompt') {
      const content = msg.content as any;
      return (
        <div className="flex justify-center my-6 animate-in fade-in slide-in-from-top-4 duration-500">
             <div className="bg-purple-900/40 border border-purple-500/30 px-6 py-3 rounded-full shadow-[0_0_20px_rgba(168,85,247,0.2)] flex items-center gap-3 backdrop-blur-sm">
                <Sparkles className="w-4 h-4 text-purple-300 animate-pulse" />
                <span className="text-sm font-medium text-purple-100 italic">"{content.text}"</span>
             </div>
        </div>
      );
  }

  // Crisis Intervention UI
  if (msg.type === 'crisis') {
     const content = msg.content as any;
     return (
        <div className="flex justify-start mb-4 animate-in zoom-in-95 duration-300">
            <div className="max-w-[90%] rounded-xl border border-red-500/50 bg-red-950/90 text-white shadow-[0_0_30px_rgba(239,68,68,0.2)] p-6">
                <div className="flex items-center gap-3 mb-4 text-red-400 border-b border-red-500/30 pb-2">
                    <AlertTriangle className="w-6 h-6" />
                    <h3 className="font-bold uppercase tracking-wider">Safety Protocol Activated</h3>
                </div>
                <div className="prose prose-invert prose-sm mb-6" dangerouslySetInnerHTML={{ __html: content.text }} />
                <a href="tel:988" className="w-full bg-red-600 hover:bg-red-500 text-white py-3 rounded-lg font-bold flex items-center justify-center gap-2 transition-colors">
                    <Phone className="w-4 h-4" /> Call Crisis Lifeline (988)
                </a>
            </div>
        </div>
     );
  }

  // Structured Analysis Result
  if (msg.type === 'analysis' && typeof msg.content !== 'string') {
    const analysis = msg.content;
    const profile = analysis.profile;
    return (
        <div className="flex justify-start mb-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
            <div className="max-w-[95%] md:max-w-[85%] rounded-2xl rounded-bl-none border border-purple-500/30 bg-[#1a1025]/90 text-gray-200 shadow-lg overflow-hidden">
                <div className="flex items-center justify-between px-4 py-2 border-b border-purple-500/20 bg-purple-900/10">
                    <span className="text-xs font-bold uppercase tracking-wider text-purple-400">Lusa Analysis</span>
                    <span className="text-[9px] text-gray-500 font-mono">{msg.timestamp}</span>
                </div>
                <div className="p-5">
                     <div
                        className="prose prose-invert prose-sm max-w-none mb-6 text-sm leading-relaxed"
                        dangerouslySetInnerHTML={{ __html: analysis.text }}
                    />

                    {profile && (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {/* Jungian Card */}
                            <div className="bg-black/30 rounded-xl p-4 border border-white/5">
                                <h4 className="text-[10px] font-bold uppercase text-gray-500 mb-3 flex items-center gap-2">
                                    <User className="w-3 h-3" /> Jungian Framework
                                </h4>
                                <div className="space-y-2 text-xs">
                                    <div className="flex justify-between">
                                        <span className="text-gray-400">Archetype</span>
                                        <span className="text-white font-medium">{profile.jungian.archetype}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-400">Shadow</span>
                                        <span className="text-purple-300 font-medium">{profile.jungian.shadow}</span>
                                    </div>
                                    <div className="mt-2 h-1 bg-gray-800 rounded-full overflow-hidden">
                                        <div className="h-full bg-purple-500" style={{ width: `${profile.jungian.confidence * 100}%` }} />
                                    </div>
                                </div>
                            </div>

                            {/* Big 5 Traits */}
                            <div className="bg-black/30 rounded-xl p-4 border border-white/5">
                                <h4 className="text-[10px] font-bold uppercase text-gray-500 mb-3 flex items-center gap-2">
                                    <Activity className="w-3 h-3" /> Big Five
                                </h4>
                                <div className="space-y-2">
                                    {profile.traits.map((t) => (
                                        <TraitBar key={t.code} trait={t} />
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3 animate-in fade-in slide-in-from-bottom-2 duration-300`}>
      <div className={`max-w-[85%] rounded-2xl px-5 py-3 text-sm leading-relaxed shadow-lg backdrop-blur-sm
        ${isUser
          ? 'bg-gradient-to-br from-indigo-600 to-violet-600 text-white rounded-br-none'
          : 'bg-[#15151a]/95 border border-gray-800 text-gray-300 rounded-bl-none'
        }
      `}>
        {!isUser && (
          <div className="flex items-center justify-between mb-2 pb-2 border-b border-white/5">
            <span className={`text-[10px] font-bold uppercase tracking-wider flex items-center gap-2
              ${msg.sender === 'Veridian' ? 'text-cyan-400' :
                msg.sender.startsWith('Lu') ? 'text-purple-400' :
                msg.sender === 'Nexus' ? 'text-emerald-400' :
                msg.sender === 'Cro' ? 'text-orange-400' :
                msg.sender === 'SaCoLu' ? 'text-pink-400' : 'text-gray-400'
              }
            `}>
              {msg.sender}
            </span>
            <span className="text-[9px] text-gray-600 font-mono opacity-60">{msg.timestamp}</span>
          </div>
        )}
        <div
          className="prose prose-invert prose-sm max-w-none"
          dangerouslySetInnerHTML={{ __html: typeof msg.content === 'string' ? msg.content : '' }}
        />
      </div>
    </div>
  );
};

// --- Main Application ---

export default function EchoesOfAlaraPage() {
  const [authState, setAuthState] = useState<'login' | 'app'>('login');
  const [activeTab, setActiveTab] = useState<'journey' | 'ritual' | 'sanctuary' | 'mirror' | 'oracle'>('journey');

  // App State
  const [artFile, setArtFile] = useState<File | null>(null);
  const [chatInstance, setChatInstance] = useState<UnifiedAIChat | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [pendingTasks, setPendingTasks] = useState<Task[]>([]);
  const [psychProfile, setPsychProfile] = useState<PsychProfile | null>(null);
  const [vaultItems, setVaultItems] = useState<any[]>([]);
  const [crisisMode, setCrisisMode] = useState(false);

  // Ritual Mode State
  const [ritualState, setRitualState] = useState<'intro' | 'setup' | 'active' | 'upload'>('intro');
  const [ritualTime, setRitualTime] = useState(0);
  const [ritualGenre, setRitualGenre] = useState('');

  const chatEndRef = useRef<HTMLDivElement>(null);
  const sanctuaryEndRef = useRef<HTMLDivElement>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // Initialize System on Login
  useEffect(() => {
    if (authState === 'app' && !chatInstance) {
      const system = new UnifiedAIChat((history, tasks) => {
        setMessages(history);
        setPendingTasks(tasks);

        const lastMsg = history[history.length - 1];

        if (lastMsg && lastMsg.sender === 'Nexus' && typeof lastMsg.content === 'string' && lastMsg.content.includes('Vault Sector')) {
            setVaultItems(prev => [...prev, {
                id: Math.random().toString(),
                date: new Date().toLocaleDateString(),
                summary: 'Analysis #' + (prev.length + 1).toString().padStart(3, '0')
            }]);
        }

        if (lastMsg && lastMsg.type === 'analysis') {
            const content = lastMsg.content as any;
            if (content.profile) setPsychProfile(content.profile);
        }

        if (lastMsg && lastMsg.type === 'crisis') {
            setCrisisMode(true);
        }
      });
      setChatInstance(system);

      const init = async () => {
        await system.initializeChatRoom();
        const v = new VeridianChatEnabled();
        const l = new LusaChatEnabled();
        const n = new NexusChatEnabled();
        const c = new CroChatEnabled();
        const s = new SaCoLuChatEnabled();
        await system.connectAgents([v, l, n, c, s]);
      };
      init();
    }
  }, [authState, chatInstance]);

  // Ritual Logic
  useEffect(() => {
    if (ritualState === 'active') {
        timerRef.current = setInterval(() => {
            setRitualTime(prev => {
                const next = prev + 1;

                // Track Switch Check (Every 90s)
                if (next % 90 === 0 && next > 0) {
                    // console.log("Changing track..."); // Sim only
                }

                // Lusa Distraction Check (Every 120s)
                if (next % 120 === 0 && next > 0 && chatInstance) {
                    chatInstance.userMessage("distract me");
                }

                return next;
            });
        }, 1000);
    } else {
        if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [ritualState, chatInstance]);

  // Auto-scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    sanctuaryEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, activeTab]);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setAuthState('app');
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setArtFile(e.target.files[0]);
    }
  };

  // Takes the file directly when called right after an upload,
  // because the artFile state hasn't updated yet at that point.
  const startAnalysis = (file: File | null = artFile) => {
    if (!chatInstance || !file) return;
    // If coming from ritual, switch back to council view
    if (activeTab === 'ritual') setActiveTab('journey');
    chatInstance.userMessage(`Uploaded artwork: ${file.name}. Analyze psychological framework.`);
  };

  const approveTasks = () => {
    if (!chatInstance) return;
    chatInstance.approveTasks();
  };

  const sendSpiritMessage = (text: string) => {
    if (!chatInstance) return;
    chatInstance.userMessage(`guide: ${text}`);
  };

  const formatTime = (sec: number) => {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  // --- LOGIN SCREEN ---
  if (authState === 'login') {
    return (
        <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center p-4">
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                <div className="absolute top-[-20%] left-[-20%] w-[70%] h-[70%] rounded-full bg-purple-900/20 blur-[150px]" />
                <div className="absolute bottom-[-20%] right-[-20%] w-[70%] h-[70%] rounded-full bg-cyan-900/10 blur-[150px]" />
            </div>

            <div className="relative w-full max-w-md bg-[#13131a] border border-gray-800 rounded-2xl p-8 shadow-2xl backdrop-blur-xl animate-in fade-in zoom-in-95 duration-500">
                <div className="flex flex-col items-center mb-8">
                    <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl flex items-center justify-center mb-4 shadow-lg shadow-purple-900/40">
                        <Fingerprint className="w-6 h-6 text-white" />
                    </div>
                    <h1 className="text-2xl font-bold text-white mb-1">Echoes of Alara</h1>
                    <p className="text-sm text-gray-500">Unified Neural Interface v6.0</p>
                </div>

                <form onSubmit={handleLogin} className="space-y-4">
                    <div>
                        <label className="block text-xs font-medium text-gray-400 mb-1 ml-1">Identity Token</label>
                        <div className="relative">
                            <User className="absolute left-3 top-3 w-4 h-4 text-gray-600" />
                            <input
                                type="email"
                                defaultValue="garrett@alara.echo"
                                className="w-full bg-black/30 border border-gray-800 rounded-xl py-2.5 pl-10 pr-4 text-sm text-gray-200 focus:outline-none focus:border-purple-500/50 focus:bg-purple-900/10 transition-all"
                            />
                        </div>
                    </div>
                    <div>
                        <label className="block text-xs font-medium text-gray-400 mb-1 ml-1">Access Key</label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-3 w-4 h-4 text-gray-600" />
                            <input
                                type="password"
                                defaultValue="password"
                                className="w-full bg-black/30 border border-gray-800 rounded-xl py-2.5 pl-10 pr-4 text-sm text-gray-200 focus:outline-none focus:border-purple-500/50 focus:bg-purple-900/10 transition-all"
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white py-3 rounded-xl font-medium transition-all shadow-lg shadow-purple-900/20 flex items-center justify-center gap-2 mt-2"
                    >
                        <LogIn className="w-4 h-4" />
                        Initialize Session
                    </button>
                </form>
            </div>
        </div>
    );
  }

  // --- MAIN APP ---
  return (
    <div className="min-h-screen bg-[#0f0f13] text-gray-200 flex flex-col md:flex-row font-sans">

      {/* SIDEBAR NAVIGATION */}
      <div className="w-full md:w-[80px] bg-[#0a0a0f] border-r border-gray-800 flex md:flex-col items-center py-4 md:py-8 gap-6 z-20 overflow-x-auto md:overflow-visible">
         <div className="hidden md:flex w-10 h-10 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg items-center justify-center shadow-lg shadow-purple-900/30 mb-4 shrink-0">
            <span className="font-bold text-white text-xs">EA</span>
         </div>

         <button
            onClick={() => setActiveTab('journey')}
            className={`p-3 rounded-xl transition-all shrink-0 ${activeTab === 'journey' ? 'bg-gray-800 text-cyan-400' : 'text-gray-500 hover:text-gray-300'}`}
            title="Journey (Council)"
         >
            <LayoutDashboard className="w-5 h-5" />
         </button>

         <button
            onClick={() => setActiveTab('ritual')}
            className={`p-3 rounded-xl transition-all shrink-0 ${activeTab === 'ritual' ? 'bg-gray-800 text-rose-400' : 'text-gray-500 hover:text-gray-300'}`}
            title="The Ritual (Create)"
         >
            <Eye className="w-5 h-5" />
         </button>

         <button
            onClick={() => setActiveTab('sanctuary')}
            className={`p-3 rounded-xl transition-all shrink-0 ${activeTab === 'sanctuary' ? 'bg-gray-800 text-orange-400' : 'text-gray-500 hover:text-gray-300'}`}
            title="Sanctuary (Spirit Guides)"
         >
            <Sparkles className="w-5 h-5" />
         </button>

         <button
            onClick={() => setActiveTab('mirror')}
            className={`p-3 rounded-xl transition-all shrink-0 ${activeTab === 'mirror' ? 'bg-gray-800 text-purple-400' : 'text-gray-500 hover:text-gray-300'}`}
            title="Mirror (Profile)"
         >
            <Activity className="w-5 h-5" />
         </button>

         <button
            onClick={() => setActiveTab('oracle')}
            className={`p-3 rounded-xl transition-all shrink-0 ${activeTab === 'oracle' ? 'bg-gray-800 text-emerald-400' : 'text-gray-500 hover:text-gray-300'}`}
            title="Oracle (Pricing)"
         >
            <Zap className="w-5 h-5" />
         </button>

         <div className="md:mt-auto ml-auto md:ml-0">
            <button onClick={() => setAuthState('login')} className="p-3 text-gray-600 hover:text-red-400 transition-colors">
                <LogIn className="w-5 h-5 rotate-180" />
            </button>
         </div>
      </div>

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 flex overflow-hidden">

        {/* === VIEW: JOURNEY (MAIN COUNCIL) === */}
        {activeTab === 'journey' && (
            <div className="flex-1 flex flex-col md:flex-row h-full animate-in fade-in duration-300">
                {/* Context Panel */}
                <div className="w-full md:w-[350px] bg-[#0a0a0f] border-r border-gray-800 p-6 flex flex-col">
                    <div className="mb-6">
                        <h3 className="text-xs font-bold uppercase tracking-widest text-gray-500 mb-4">Council Uplink</h3>
                        <div className="flex flex-wrap gap-2">
                            <AgentBadge name="Veridian" status="online" />
                            <AgentBadge name="Lusa" status="online" />
                            <AgentBadge name="Nexus" status="online" />
                            <AgentBadge name="Cro" status="online" />
                            <AgentBadge name="SaCoLu" status="online" />
                        </div>
                    </div>
                    {/* Upload */}
                    <div className="flex-1 flex flex-col justify-center mb-6">
                         <div className="border-2 border-dashed border-gray-800 rounded-2xl p-6 text-center hover:bg-gray-800/20 transition-all group relative">
                            <input
                              type="file"
                              id="art-upload"
                              className="hidden"
                              accept="image/*"
                              onChange={handleFileUpload}
                            />
                            {artFile ? (
                                <div className="space-y-4">
                                    <div className="w-12 h-12 mx-auto bg-purple-500/20 rounded-full flex items-center justify-center text-purple-400">
                                        <CheckCircle2 className="w-6 h-6" />
                                    </div>
                                    <div className="text-sm text-gray-300 font-medium truncate">{artFile.name}</div>
                                    <button
                                        onClick={() => startAnalysis()}
                                        disabled={pendingTasks.length > 0}
                                        className="w-full py-2.5 bg-purple-600 hover:bg-purple-500 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl text-sm font-medium transition-all shadow-lg shadow-purple-900/20"
                                    >
                                        Begin Analysis
                                    </button>
                                </div>
                            ) : (
                                <label htmlFor="art-upload" className="cursor-pointer block">
                                    <div className="w-12 h-12 mx-auto bg-gray-800 rounded-xl flex items-center justify-center text-gray-500 group-hover:text-purple-400 group-hover:scale-110 transition-all mb-3">
                                        <Upload className="w-6 h-6" />
                                    </div>
                                    <div className="text-sm text-gray-400 font-medium">Upload Artifact</div>
                                    <div className="text-[10px] text-gray-600 mt-1">JPG, PNG</div>
                                </label>
                            )}
                         </div>
                    </div>
                    {/* Queue */}
                    {pendingTasks.length > 0 && (
                      <div className="p-4 bg-gray-900/50 border border-gray-800 rounded-xl animate-in slide-in-from-bottom-4">
                        <div className="flex items-center justify-between mb-3">
                          <span className="text-[10px] font-bold uppercase text-cyan-400 flex items-center gap-2">
                            <Cpu className="w-3 h-3" /> Processing
                          </span>
                          <span className="text-[9px] bg-cyan-950 text-cyan-400 px-2 py-0.5 rounded-full">
                            {pendingTasks.length} TASKS
                          </span>
                        </div>
                        <button
                          onClick={approveTasks}
                          className="w-full py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-[10px] font-bold uppercase tracking-wider rounded-lg transition-colors shadow-lg shadow-cyan-900/20"
                        >
                          Authorize Protocols
                        </button>
                      </div>
                    )}
                </div>
                {/* Chat Stream */}
                <div className="flex-1 bg-[#050507] relative flex flex-col">
                    <div className="absolute top-0 right-0 w-[400px] h-[400px] bg-purple-900/5 rounded-full blur-[100px] pointer-events-none" />
                    <div className="h-14 border-b border-gray-800 flex items-center justify-between px-6 bg-[#0a0a0f]/80 backdrop-blur-md z-10">
                        <div className="flex items-center gap-2">
                            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                            <span className="text-xs font-medium text-gray-400 uppercase tracking-widest">Unified Neural Stream</span>
                        </div>
                    </div>
                    <div className="flex-1 overflow-y-auto p-6 scroll-smooth">
                        {messages.length === 0 ? (
                            <div className="h-full flex flex-col items-center justify-center text-gray-700 opacity-50 gap-3">
                                <Activity className="w-10 h-10" />
                                <p className="text-xs uppercase tracking-widest">Awaiting Input Vector</p>
                            </div>
                        ) : (
                            messages.map((msg) => <ChatBubble key={msg.id} msg={msg} />)
                        )}
                        <div ref={chatEndRef} />
                    </div>
                    <div className="p-4 bg-[#0a0a0f] border-t border-gray-800">
                         {/* Hidden Input for demo continuity */}
                        <div className="w-full bg-gray-900/50 border border-gray-800 rounded-xl px-4 py-3 text-sm text-gray-500 flex items-center justify-between">
                            <span>System Idle.</span>
                            <div className="flex gap-1">
                                <span className="w-1 h-1 bg-gray-600 rounded-full" />
                                <span className="w-1 h-1 bg-gray-600 rounded-full" />
                                <span className="w-1 h-1 bg-gray-600 rounded-full" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )}

        {/* === VIEW: THE RITUAL (NEW!) === */}
        {activeTab === 'ritual' && (
            <div className="flex-1 bg-[#0a0a0f] relative overflow-hidden flex flex-col animate-in fade-in duration-500">
                <div className="absolute inset-0 bg-gradient-to-br from-purple-900/10 to-blue-900/10 pointer-events-none" />

                {/* Intro Screen */}
                {ritualState === 'intro' && (
                    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center max-w-2xl mx-auto z-10">
                        <div className="w-16 h-16 bg-gradient-to-br from-rose-500 to-purple-600 rounded-full flex items-center justify-center mb-6 shadow-2xl shadow-rose-900/50 animate-pulse">
                            <Eye className="w-8 h-8 text-white" />
                        </div>
                        <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">The Grande Prairie Method</h2>
                        <div className="prose prose-invert text-gray-300 mb-8 leading-relaxed">
                            <p className="text-lg">The tree test psychologists use... but with a twist that makes it actually work.</p>
                            <p>Developed through 200+ real-world sessions, this method bypasses your conscious mind to reveal what your art REALLY says about you.</p>
                            <p className="font-medium text-rose-300">It's not magic. It's psychology + perfect timing.</p>
                        </div>
                        <button onClick={() => setRitualState('setup')} className="px-8 py-4 bg-white text-black rounded-full font-bold text-lg hover:scale-105 transition-transform flex items-center gap-2">
                            Begin The Ritual <ArrowRight className="w-5 h-5" />
                        </button>
                    </div>
                )}

                {/* Setup Screen */}
                {ritualState === 'setup' && (
                    <div className="flex-1 flex flex-col items-center justify-center p-8 z-10">
                        <h2 className="text-2xl font-bold text-white mb-8">Choose Your Atmosphere</h2>
                        <div className="grid grid-cols-2 gap-4 max-w-md w-full">
                            {['Ambient Flow', 'Deep Focus', 'Nature\'s Pulse', 'Lo-Fi Drift'].map(genre => (
                                <button
                                    key={genre}
                                    onClick={() => { setRitualGenre(genre); setRitualTime(0); setRitualState('active'); }}
                                    className="p-6 bg-gray-900/50 border border-gray-800 hover:border-rose-500 hover:bg-rose-900/10 rounded-xl text-left transition-all group"
                                >
                                    <Music className="w-6 h-6 text-gray-500 group-hover:text-rose-400 mb-3" />
                                    <div className="font-bold text-gray-200 group-hover:text-white">{genre}</div>
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {/* Active Ritual */}
                {ritualState === 'active' && (
                    <div className="flex-1 flex flex-col items-center justify-center p-8 z-10 relative">
                        {/* Background Pulse */}
                        <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-20">
                             <div className={`w-[500px] h-[500px] bg-rose-500/30 rounded-full blur-[100px] transition-all duration-1000 ${ritualTime % 2 === 0 ? 'scale-100' : 'scale-110'}`} />
                        </div>

                        {/* Top Bar */}
                        <div className="absolute top-0 left-0 right-0 p-6 flex justify-between items-center bg-gradient-to-b from-black/50 to-transparent">
                            <div className="flex items-center gap-2 text-rose-400">
                                <Music className="w-4 h-4 animate-spin-slow" />
                                <span className="text-xs font-bold uppercase tracking-widest">{ritualGenre}</span>
                            </div>
                            <div className="text-xs text-gray-500">PHASE: CREATION</div>
                        </div>

                        {/* Main Timer Display */}
                        <div className="text-center mb-12">
                            <div className="text-8xl font-bold text-white font-mono tracking-tighter mb-4">
                                {formatTime(ritualTime)}
                            </div>
                            {ritualTime < 360 ? (
                                <p className="text-gray-400 animate-pulse">Let your mind wander. Just create.</p>
                            ) : (
                                <p className="text-rose-400 font-bold animate-bounce">BONUS WINDOW OPEN. KEEP GOING.</p>
                            )}
                        </div>

                        {/* Progress Bar (Zeigarnik Visual) */}
                        <div className="w-full max-w-xl h-2 bg-gray-800 rounded-full overflow-hidden mb-12 relative">
                             <div
                                className="h-full bg-gradient-to-r from-rose-500 to-purple-600 transition-all duration-1000 ease-linear"
                                style={{ width: `${(ritualTime / 480) * 100}%` }}
                             />
                             {/* Markers */}
                             <div className="absolute top-0 bottom-0 left-[75%] w-0.5 bg-white/50" /> {/* 6 min mark */}
                        </div>

                        {/* Dynamic Prompts (Lusa) */}
                        <div className="h-24 flex items-center justify-center">
                            {messages.filter(m => m.type === 'ritual_prompt').slice(-1).map(msg => (
                                <ChatBubble key={msg.id} msg={msg} />
                            ))}
                        </div>

                        {/* Controls */}
                        <div className="mt-8 flex gap-4">
                            <button
                                onClick={() => { setRitualState('intro'); setRitualTime(0); }}
                                className="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-full text-sm font-medium transition-colors"
                            >
                                Cancel Ritual
                            </button>
                            {ritualTime >= 360 && (
                                <button
                                    onClick={() => setRitualState('upload')}
                                    className="px-8 py-3 bg-white text-black hover:bg-gray-200 rounded-full font-bold transition-all animate-in zoom-in slide-in-from-bottom-4"
                                >
                                    Complete & Upload
                                </button>
                            )}
                        </div>
                    </div>
                )}

                {/* Upload Phase */}
                {ritualState === 'upload' && (
                    <div className="flex-1 flex flex-col items-center justify-center p-8 z-10">
                         <div className="max-w-md w-full text-center">
                             <h2 className="text-2xl font-bold text-white mb-2">The Cycle is Complete.</h2>
                             <p className="text-gray-400 mb-8">Your unconscious mind has spoken. Let's see what it said.</p>

                             <div className="border-2 border-dashed border-gray-700 rounded-2xl p-8 hover:border-rose-500/50 hover:bg-gray-800/30 transition-all group cursor-pointer relative">
                                <input
                                  type="file"
                                  className="absolute inset-0 opacity-0 cursor-pointer"
                                  accept="image/*"
                                  onChange={(e) => {
                                      const file = e.target.files?.[0] ?? null;
                                      handleFileUpload(e);
                                      if (file) {
                                          setActiveTab('journey'); // Go to analysis
                                          setRitualState('intro');
                                          setRitualTime(0);
                                          startAnalysis(file);
                                      }
                                  }}
                                />
                                <div className="w-16 h-16 mx-auto bg-rose-500/20 rounded-full flex items-center justify-center text-rose-400 group-hover:scale-110 transition-transform mb-4">
                                    <Upload className="w-8 h-8" />
                                </div>
                                <div className="font-medium text-white">Upload Your Artwork</div>
                             </div>
                         </div>
                    </div>
                )}
            </div>
        )}

        {/* === VIEW: SANCTUARY (SPIRIT CHAT) === */}
        {activeTab === 'sanctuary' && (
            <div className="flex-1 flex flex-col bg-[#0f0f13] animate-in fade-in duration-300">
                <header className="h-16 border-b border-gray-800 flex items-center justify-between px-8 bg-[#0a0a0f]">
                     <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-orange-500 to-red-600 flex items-center justify-center shadow-lg shadow-orange-900/30">
                            <span className="font-bold text-white">I</span>
                        </div>
                        <div>
                            <div className="font-bold text-slate-200">Ignis (The Phoenix)</div>
                            <div className="text-xs text-orange-400">Spirit Guide • Passion • Rebirth</div>
                        </div>
                     </div>
                </header>
                <div className="flex-1 p-8 overflow-y-auto space-y-6">
                    {/* Filter only sanctuary/guide messages */}
                    {messages.filter(m => m.type !== 'analysis' && m.type !== 'crisis' && m.type !== 'ritual_prompt' && !m.sender.includes('Veridian') && !m.sender.includes('Nexus')).map(msg => (
                        <div key={msg.id} className={`flex ${msg.sender === 'User' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-[70%] p-4 rounded-2xl ${
                                msg.sender === 'User' ? 'bg-orange-600 text-white rounded-br-none' : 'bg-gray-800 text-gray-300 rounded-bl-none'
                            }`}>
                                {typeof msg.content === 'string' ? msg.content : '...'}
                            </div>
                        </div>
                    ))}
                    <div ref={sanctuaryEndRef} />
                </div>
                <div className="p-6 border-t border-gray-800 bg-[#0a0a0f]">
                     <form onSubmit={(e) => {
                        e.preventDefault();
                        const input = (e.target as any).msg.value;
                        if(input) sendSpiritMessage(input);
                        (e.target as any).msg.value = '';
                     }} className="flex gap-2">
                        <input name="msg" type="text" placeholder="Speak to the spirits..." className="flex-1 bg-gray-900 border border-gray-800 rounded-full px-6 py-3 text-white focus:outline-none focus:border-orange-500" />
                        <button type="submit" className="p-3 bg-orange-600 hover:bg-orange-500 rounded-full text-white"><ArrowRight className="w-5 h-5"/></button>
                     </form>
                </div>
            </div>
        )}

        {/* === VIEW: MIRROR (PROFILE) === */}
        {activeTab === 'mirror' && (
            <div className="flex-1 p-8 overflow-y-auto animate-in fade-in zoom-in-95 duration-300">
                <div className="max-w-4xl mx-auto">
                    <header className="mb-8 flex justify-between items-end">
                        <div>
                            <h2 className="text-3xl font-bold text-white mb-2">The Mirror</h2>
                            <p className="text-gray-400 text-sm">Reflecting the architecture of your soul.</p>
                        </div>
                        {psychProfile && (
                             <div className="text-right">
                                <div className="text-3xl font-bold text-purple-400">{(psychProfile.jungian.confidence * 100).toFixed(0)}%</div>
                                <div className="text-xs text-gray-500 uppercase">Resonance</div>
                             </div>
                        )}
                    </header>

                    {!psychProfile ? (
                        <div className="p-12 border border-gray-800 bg-gray-900/50 rounded-2xl text-center">
                            <Fingerprint className="w-12 h-12 text-gray-600 mx-auto mb-4" />
                            <p className="text-gray-400">No reflection found. Initiate an analysis in the Journey tab.</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {/* Archetype Card */}
                            <div className="bg-[#13131a] border border-gray-800 p-8 rounded-2xl relative overflow-hidden">
                                <div className="absolute top-0 right-0 w-32 h-32 bg-purple-500/10 rounded-full blur-3xl" />
                                <h3 className="text-sm font-bold text-gray-500 uppercase mb-6 tracking-wider">Dominant Archetype</h3>
                                <div className="text-4xl font-bold text-white mb-2">{psychProfile.jungian.archetype}</div>
                                <div className="text-purple-400 mb-6">The Shadow: {psychProfile.jungian.shadow}</div>
                                <div className="h-1 bg-gray-800 rounded-full overflow-hidden">
                                    <div className="h-full bg-purple-500" style={{ width: `${psychProfile.jungian.confidence * 100}%` }} />
                                </div>
                            </div>

                            {/* Vault History */}
                            <div className="bg-[#13131a] border border-gray-800 p-8 rounded-2xl">
                                <h3 className="text-sm font-bold text-gray-500 uppercase mb-6 tracking-wider">Vault History</h3>
                                <div className="space-y-4">
                                    {vaultItems.map((item, i) => (
                                        <div key={i} className="flex items-center justify-between p-3 bg-gray-900/50 rounded-xl">
                                            <span className="text-sm text-gray-300">{item.summary}</span>
                                            <span className="text-xs text-gray-600">{item.date}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Full Traits */}
                            <div className="md:col-span-2 bg-[#13131a] border border-gray-800 p-8 rounded-2xl">
                                <h3 className="text-sm font-bold text-gray-500 uppercase mb-6 tracking-wider">Psychometric Spectrum</h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
                                     {psychProfile.traits.map(t => <TraitBar key={t.code} trait={t} />)}
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        )}

        {/* === VIEW: ORACLE (PRICING) === */}
        {activeTab === 'oracle' && (
            <div className="flex-1 p-8 overflow-y-auto animate-in fade-in duration-300 flex items-center justify-center">
                 <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl w-full">
                    {[
                      { name: "Initiate", price: "$0", features: ["3 Analyses/mo", "Basic Spirit Guide", "Standard Vault"] },
                      { name: "Seeker", price: "$4.99", features: ["15 Analyses/mo", "Deep Psych Mapping", "Priority Council"] },
                      { name: "Oracle", price: "$12.99", features: ["Unlimited Access", "Crisis Priority", "Full Archival"] },
                    ].map((tier, idx) => (
                      <div key={idx} className={`relative p-8 rounded-2xl border ${idx === 1 ? 'bg-[#0f0f15] border-emerald-500 shadow-2xl shadow-emerald-900/20 transform scale-105' : 'bg-[#13131a] border-gray-800'}`}>
                        {idx === 1 && (
                          <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-emerald-500 text-black text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-widest">
                            Most Popular
                          </div>
                        )}
                        <h3 className="text-xl font-bold text-white mb-2">{tier.name}</h3>
                        <div className="text-3xl font-serif text-emerald-400 mb-6">{tier.price}<span className="text-sm text-gray-500 font-sans">/mo</span></div>
                        <ul className="space-y-4 mb-8">
                          {tier.features.map((feat, fIdx) => (
                            <li key={fIdx} className="flex items-center gap-3 text-sm text-gray-300">
                              <Star className="w-4 h-4 text-emerald-600 fill-current" /> {feat}
                            </li>
                          ))}
                        </ul>
                        <button className={`w-full py-3 rounded-xl font-bold transition-colors ${
                          idx === 1 ? 'bg-emerald-600 hover:bg-emerald-500 text-white' : 'bg-gray-800 hover:bg-gray-700 text-gray-300'
                        }`}>
                          Choose {tier.name}
                        </button>
                      </div>
                    ))}
                  </div>
            </div>
        )}

      </div>
    </div>
  );
}
