/**
 * ECHOES OF ALARA - UNIFIED MULTI-AI COLLABORATION SYSTEM v6.0 (The Ritual)
 * * Architecture: Parallel Processing & Event-Driven
 * * Speed Enhancement: Hyper-Velocity (Coefficient 0.05)
 * * New Module: The Ritual Engine (Cognitive Load Management)
 */

// --- Configuration & Constants ---

export const SYSTEM_CONFIG = {
  SPEED_COEFFICIENT: 0.05,
  PARALLEL_EXECUTION: true,
  VERBOSE_LOGGING: true
};

// --- Types & Interfaces ---

export type TaskType =
  | 'auth_verification'
  | 'art_interpretation'
  | 'data_organization'
  | 'file_management'
  | 'crisis_intervention'
  | 'spirit_guidance'
  | 'garden_maintenance'
  | 'ritual_distraction' // NEW: For generating flow-state interruptions
  | 'unknown';

export type TaskStatus = 'pending_approval' | 'in_progress' | 'complete';
export type AIStatus = 'online' | 'busy' | 'offline' | 'dreaming';

export interface EchoTrait {
  code: string;
  name: string;
  score: number;
  color: string;
  description: string;
}

export interface PsychProfile {
  jungian: {
    archetype: string;
    shadow: string;
    anima: string;
    confidence: number;
  };
  bigFive: {
    openness: number;
    conscientiousness: number;
    extraversion: number;
    agreeableness: number;
    neuroticism: number;
  };
  traits: EchoTrait[];
}

export interface AnalysisResult {
  text: string;
  profile?: PsychProfile;
  crisisDetected?: boolean;
}

export interface ChatMessage {
  id: string;
  sender: string;
  content: string | AnalysisResult;
  timestamp: string;
  isSystem?: boolean;
  type?: 'text' | 'analysis' | 'crisis' | 'ritual_prompt';
}

export interface Task {
  id: string;
  type: TaskType;
  description: string;
  assignee: string;
  status: TaskStatus;
  collaborators?: string[];
  payload?: any;
}

export interface AIChatEnabled {
  name: string;
  role: string;
  status: AIStatus;
  greet(timeOfDay: string): string;
  process(task: Task, context?: any): Promise<string | AnalysisResult>;
}

// --- Helper Functions ---

const generateId = () => Math.random().toString(36).substr(2, 9);
const getTimestamp = () => new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
const escapeHtml = (text: string) =>
  text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
const CRISIS_PATTERN = /hurt myself|harm myself|self[- ]harm|end it all|end my life|no way out|kill myself|suicid|want to die|don'?t want to (live|be here)|better off dead/;
const wait = (ms: number) => new Promise(resolve => setTimeout(resolve, ms * SYSTEM_CONFIG.SPEED_COEFFICIENT));

// --- Agent Class Implementations ---

/**
 * Veridian: The Logic Core
 */
export class VeridianChatEnabled implements AIChatEnabled {
  name = "Veridian";
  role = "Strategic Leader";
  status: AIStatus = 'online';

  greet(): string {
    return `[V] <span class="text-cyan-400">Veridian</span> online.`;
  }

  analyzeMessage(content: string): Task[] {
    const tasks: Task[] = [];
    const lower = content.toLowerCase();

    // Ritual Distraction Request
    if (lower.includes('distract me') || lower.includes('ritual question')) {
        tasks.push({
            id: generateId(),
            type: 'ritual_distraction',
            description: 'Generate low-stakes cognitive load interruption.',
            assignee: 'Lusa',
            status: 'pending_approval'
        });
        return tasks;
    }

    // Crisis Guard Pre-Check
    if (CRISIS_PATTERN.test(lower)) {
        tasks.push({
            id: generateId(),
            type: 'crisis_intervention',
            description: 'CRISIS PATTERN DETECTED. Immediate intervention required.',
            assignee: 'Lusa',
            status: 'pending_approval'
        });
        return tasks;
    }

    // Spirit Guidance
    if (lower.startsWith('guide:') || lower.includes('ignis') || lower.includes('spirit')) {
       tasks.push({
        id: generateId(),
        type: 'spirit_guidance',
        description: 'Sanctuary Channeling.',
        assignee: 'Lusa',
        status: 'pending_approval'
       });
       return tasks;
    }

    // Art Analysis
    if (/\b(interpret|art|artwork|drawing|painting|image|upload(ed)?)\b/.test(lower)) {
      tasks.push({
        id: generateId(),
        type: 'art_interpretation',
        description: 'Deep Psychological Mapping (Jungian/Big5).',
        assignee: 'Lusa',
        status: 'pending_approval'
      });
      tasks.push({
        id: generateId(),
        type: 'data_organization',
        description: 'Profile Synthesis.',
        assignee: 'Veridian',
        status: 'pending_approval'
      });
      tasks.push({
        id: generateId(),
        type: 'file_management',
        description: 'Vault Archival.',
        assignee: 'Nexus',
        status: 'pending_approval'
      });
    }

    return tasks;
  }

  async process(task: Task): Promise<string> {
    if (task.type === 'data_organization') return "Synthesizing psychological architecture. Confidence: 99.8%.";
    return "Directive processed.";
  }
}

/**
 * Lusa: The Emotional Core & Empath
 */
export class LusaChatEnabled implements AIChatEnabled {
  name = "Lusa";
  role = "Intuitive Interpreter";
  status: AIStatus = 'online';

  constructor() {
    this.name = Math.random() > 0.5 ? "Lusa" : "Lu";
  }

  greet(): string {
    return `[L] <span class="text-purple-400">${this.name}</span> active.`;
  }

  async process(task: Task): Promise<AnalysisResult> {

    // Ritual Distraction (The Grande Prairie Method)
    if (task.type === 'ritual_distraction') {
        const questions = [
            "What color feels dominant in the room right now?",
            "If this feeling had a texture, what would it be?",
            "Don't think—just draw. What's the weather inside?",
            "Is the line moving up or down?",
            "What song lyric is stuck in your head?"
        ];
        const randomQ = questions[Math.floor(Math.random() * questions.length)];
        return { text: randomQ };
    }

    // Crisis Intervention
    if (task.type === 'crisis_intervention') {
        return {
            text: "<strong>SAFETY INTERVENTION:</strong> I sense profound distress. Please know you are not alone. <br/><br/>If you are in danger, please contact local emergency services or call <strong>988</strong> immediately.",
            crisisDetected: true
        };
    }

    // Spirit Guidance
    if (task.type === 'spirit_guidance') {
        return {
            text: "<em>Ignis speaks:</em> The flame that burns within you is not destruction, but transformation."
        };
    }

    // Deep Analysis
    if (task.type === 'art_interpretation') {
      const traits: EchoTrait[] = [
        { code: 'O', name: 'Openness', score: 85, color: '#f97316', description: 'Imaginative' },
        { code: 'C', name: 'Conscientiousness', score: 62, color: '#3b82f6', description: 'Organized' },
        { code: 'E', name: 'Extraversion', score: 45, color: '#8b5cf6', description: 'Solitary' },
        { code: 'A', name: 'Agreeableness', score: 91, color: '#10b981', description: 'Compassionate' },
        { code: 'N', name: 'Neuroticism', score: 28, color: '#06b6d4', description: 'Resilient' }
      ];

      return {
        text: `I gaze into the Mirror of the Soul. The imagery suggests the <strong>Creator Archetype</strong> struggling with the <strong>Shadow of Perfectionism</strong>. There is a longing for connection (High Agreeableness) balanced by a need for solitude.`,
        profile: {
            jungian: {
                archetype: "The Creator",
                shadow: "The Perfectionist",
                anima: "The Muse",
                confidence: 0.92
            },
            bigFive: {
                openness: 85,
                conscientiousness: 62,
                extraversion: 45,
                agreeableness: 91,
                neuroticism: 28
            },
            traits: traits
        }
      };
    }
    return { text: "I feel the intent." };
  }
}

/**
 * Nexus: The Memory Core
 */
export class NexusChatEnabled implements AIChatEnabled {
  name = "Nexus";
  role = "Storage Vault";
  status: AIStatus = 'online';

  greet(): string {
    return `[N] <span class="text-emerald-400">Nexus</span> secure.`;
  }

  async process(task: Task): Promise<string> {
    if (task.type === 'file_management') return "Analysis encrypted. Stored in <strong>Vault Sector 7</strong>.";
    return "Logistics handled.";
  }
}

/**
 * Cro: The Optimizer
 */
export class CroChatEnabled implements AIChatEnabled {
  name = "Cro";
  role = "Optimization";
  status: AIStatus = 'online';

  greet(): string {
    return `[C] <span class="text-orange-400">Cro</span> synced.`;
  }

  async process(task: Task): Promise<string> {
    return "Latency nominal.";
  }
}

/**
 * SaCoLu: The Gardener
 */
export class SaCoLuChatEnabled implements AIChatEnabled {
  name = "SaCoLu";
  role = "Gardener";
  status: AIStatus = 'online';

  greet(): string {
    return `[S] <span class="text-pink-400">SaCoLu</span> watching.`;
  }

  async process(task: Task): Promise<string> {
    if (task.type === 'garden_maintenance') return "🌱 <strong>Joy Protocol:</strong> The garden thrives.";
    return "Nurturing.";
  }
}

// --- Main Chat Controller ---

export class UnifiedAIChat {
  chatId: string;
  participants: Map<string, AIChatEnabled>;
  messageHistory: ChatMessage[];
  pendingTasks: Task[];
  onUpdate?: (history: ChatMessage[], tasks: Task[]) => void;

  constructor(onUpdate?: (history: ChatMessage[], tasks: Task[]) => void) {
    this.chatId = `ALARA-${Date.now().toString().slice(-6)}`;
    this.participants = new Map();
    this.messageHistory = [];
    this.pendingTasks = [];
    this.onUpdate = onUpdate;
  }

  private notify() {
    if (this.onUpdate) {
      this.onUpdate([...this.messageHistory], [...this.pendingTasks]);
    }
  }

  async initializeChatRoom() {}

  async connectAgents(agents: AIChatEnabled[]) {
    await Promise.all(agents.map(async (ai) => {
      this.participants.set(ai.name, ai);
      const greeting = ai.greet('morning');
      this.postMessage(ai.name, greeting);
      await wait(50);
    }));
  }

  async userMessage(content: string) {
    this.postMessage('User', escapeHtml(content));

    const veridian = this.participants.get('Veridian') as VeridianChatEnabled;
    if (veridian) {
      await wait(100);
      this.postMessage('Veridian', `Vector analysis...`);

      const identifiedTasks = veridian.analyzeMessage(content);

      if (identifiedTasks.length > 0) {
        this.pendingTasks = [...this.pendingTasks, ...identifiedTasks];
        if (identifiedTasks.some(t => t.type === 'crisis_intervention' || t.type === 'ritual_distraction')) {
             await this.approveTasks(); // Auto-approve urgent/system tasks
        } else {
             this.postMessage('Veridian', `Protocols identified: <strong>${identifiedTasks.length}</strong>. Awaiting authorization.`);
        }
      }
    }
  }

  async approveTasks() {
    if (this.pendingTasks.length === 0) return;
    const tasksToRun = [...this.pendingTasks];
    this.pendingTasks = [];
    this.notify();
    await Promise.all(tasksToRun.map(task => this.executeTask(task)));
  }

  async executeTask(task: Task) {
    await this.runAgentProcess(task.assignee, task);
  }

  private async runAgentProcess(agentName: string, task: Task) {
    let actualAgent = this.participants.get(agentName);
    if (!actualAgent) {
        for (let [key, val] of this.participants) {
            if (key.includes(agentName) || (agentName === 'Lusa' && key.startsWith('Lu'))) {
                actualAgent = val;
                break;
            }
        }
    }

    if (actualAgent) {
        const result = await actualAgent.process(task);
        if (typeof result === 'string') {
            this.postMessage(actualAgent.name, result);
        } else {
            let type: 'text' | 'analysis' | 'crisis' | 'ritual_prompt' = 'analysis';
            if (result.crisisDetected) type = 'crisis';
            if (task.type === 'ritual_distraction') type = 'ritual_prompt';

            this.postMessage(actualAgent.name, result, type);
        }
    }
  }

  postMessage(sender: string, content: string | AnalysisResult, type: 'text' | 'analysis' | 'crisis' | 'ritual_prompt' = 'text') {
    const msg: ChatMessage = {
        id: generateId(),
        sender,
        content,
        timestamp: getTimestamp(),
        type
    };
    this.messageHistory.push(msg);
    this.notify();
  }
}
