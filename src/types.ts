export type ProtocolStep = 'dashboard' | 'step1' | 'step2' | 'step3' | 'step4' | 'simulations';

export type BookletTier = 'beginner' | 'advanced';

export interface SeniorMemoryContext {
  age?: number;
  techLevel?: string;
  healthConditions?: string[];
  mobilityNotes?: string;
  preferredTone?: string;
  emergencyContact?: string;
  securityPassphrase?: string;
}

export interface UserAccount {
  id: string;
  name: string;
  email: string;
  phone: string;
  role: 'admin' | 'senior';
  securityLevel: 'standard' | 'ultra_vault';
  memoryContext?: SeniorMemoryContext;
  registeredAt: string;
  blockLetterVerified: boolean;
  voiceVerified: boolean;
  recognizedDeviceIds: string[];
}

export interface ResearchArea {
  id: string;
  name: string;
  iconName: string;
  description: string;
  color: string;
}

export interface AISolution {
  id: string;
  title: string;
  categoryId: string;
  categoryName: string;
  problem: string;
  solution: string;
  plainLanguageSummary: string;
  targetAudience: string;
  nonTechScore: number;
  measurableValueScore: number;
  plainLanguageScore: number;
  commonProblemScore: number;
  tags: string[];
  beginnerPrompt: string;
  advancedPrompt: string;
}

export interface PromptItem {
  id: string;
  title: string;
  libraryId: string;
  tier: BookletTier;
  objective: string;
  format: string;
  constraints: string;
  reasoningReq: boolean;
  compiledPrompt: string;
  variables: string[];
  difficulty: string;
}

export interface PromptLibrary {
  id: string;
  title: string;
  keyword: string;
  description: string;
  prompts: PromptItem[];
}

export interface BlockLetterGridField {
  label: string;
  fieldKey: string;
  maxLetters: number;
  value: string;
  sampleBoxes: string[];
}

export interface BookletPage {
  pageNumber: number;
  title: string;
  contentType: 'cover' | 'prompt' | 'visual_guide' | 'back_cover' | 'block_form';
  bodyText: string;
  promptBox?: string;
  tipBox?: string;
  diagramType?: string;
  blockFields?: BlockLetterGridField[];
}

export interface BookletTemplate {
  id: string;
  bookNumber: number; // e.g. 1 of 8
  title: string;
  category: string;
  coverGradient: string; // e.g. 'linear-gradient(145deg, #0A1F5C 0%, #0066FF 100%)'
  priceTag: string; // e.g. '$2'
  tier: BookletTier;
  description: string;
  sheetOrder: number[]; // e.g. [8, 1, 4, 5, 7, 2, 3, 6]
  pages: BookletPage[];
  author: string;
  printCount: number;
}

export interface MarketMetric {
  id: string;
  bookletId: string;
  bookletTitle: string;
  producedCount: number;
  distributedCount: number;
  soldCount: number;
  unitPrice: number;
  totalRevenue: number;
  productionTimeHours: number;
  averageRating: number;
  repeatInterestRate: number;
  feedbackNotes: string[];
  phase: 'prototype' | 'market_testing' | 'analysis';
  dateLogged: string;
}

export interface SimulationResult {
  id: string;
  scenarioTitle: string;
  difficultyArea: string;
  modelName: 'Google Gemini' | 'Microsoft Copilot' | string;
  tier: BookletTier;
  promptText: string;
  rawOutput: string;
  plainLanguageScore: number;
  zeroTechScore: number;
  executionTimeMs: number;
  status: 'PASSED' | 'FAILED';
}

export interface SecurityAlertNotification {
  id: string;
  timestamp: string;
  attemptedLocation: string;
  attemptedIp: string;
  deviceFingerprint: string;
  status: 'pending' | 'authorized' | 'blocked';
  passcodeIssued: string;
}
