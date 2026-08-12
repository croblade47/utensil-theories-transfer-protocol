import { 
  ResearchArea, 
  AISolution, 
  PromptLibrary, 
  BookletTemplate, 
  MarketMetric, 
  SimulationResult,
  UserAccount 
} from '../types';

export const INITIAL_RESEARCH_AREAS: ResearchArea[] = [
  { id: 'education', name: 'Education & Study', iconName: 'BookOpen', description: 'Simplifying complex subjects, visual study guides, and plain-language summaries.', color: '#F5A623' },
  { id: 'business', name: 'Small Business', iconName: 'Briefcase', description: 'Local marketing, budget pricing strategy, customer replies, and flyer generation.', color: '#708090' },
  { id: 'productivity', name: 'Personal Productivity', iconName: 'CheckSquare', description: 'Task prioritization, grocery inflation savings, and household routine planning.', color: '#3CB371' },
  { id: 'community', name: 'Home & Planning', iconName: 'Users', description: 'Household logistics, bill management, utility notices, and senior independence.', color: '#0066FF' },
  { id: 'travel', name: 'Family & Relationships', iconName: 'Heart', description: 'Mobility-accessible routes, family care, scheduling, and elder care.', color: '#F5CBA7' },
  { id: 'health', name: 'Health & Wellness', iconName: 'Activity', description: 'Medication schedule formatting, translating doctor jargon, and meal plans.', color: '#00CED1' },
  { id: 'hobbies', name: 'Creative Hobbies', iconName: 'Sparkles', description: 'Voice-assisted gardening guides, simple knitting steps, and woodworking blueprints.', color: '#9B59B6' },
  { id: 'entertainment', name: 'Entertainment & Games', iconName: 'Gamepad2', description: 'Family game guides, hobby trivia, storytelling, and creative prompts.', color: '#FF4500' },
];

export const INITIAL_SOLUTIONS: AISolution[] = [
  {
    id: 'sol-1',
    title: 'Senior Medication & Doctor Note Reader',
    categoryId: 'health',
    categoryName: 'Health & Wellness',
    problem: 'Seniors struggle to read tiny prescription labels and complex medical instructions.',
    solution: 'Point smartphone camera at doctor notes or pill bottles for an instant 3-bullet plain text daily schedule.',
    plainLanguageSummary: 'Turns complicated medicine labels into 3 simple daily steps with clear meal reminders.',
    targetAudience: 'Elderly patients, caregivers, and non-tech family members.',
    nonTechScore: 98,
    measurableValueScore: 95,
    plainLanguageScore: 99,
    commonProblemScore: 96,
    tags: ['Senior', 'Medication', 'Health', 'Snap & Run'],
    beginnerPrompt: 'Take a picture of this doctor note or pill bottle. 1. List medication names in large font. 2. Give exact times of day (Morning, Noon, Night) to take each with food or water. 3. Use 3 short bullet points only.',
    advancedPrompt: 'Remember Me Profile: [USER_NAME], Age [USER_AGE], Medical Notes: [USER_HEALTH_NOTES]. Analyze attached pill bottle image. Cross-reference schedule with daily routine. Output large-print format with alarm reminders.'
  },
  {
    id: 'sol-2',
    title: 'Small Biz $50 Weekend Marketing Booster',
    categoryId: 'business',
    categoryName: 'Small Business',
    problem: 'Local store owners do not know how to run marketing without high ad spend.',
    solution: 'Generates 3 zero-cost weekend promotion ideas with printed flyer templates for immediate neighborhood distribution.',
    plainLanguageSummary: 'Creates 3 simple marketing steps for local businesses using free word-of-mouth and community flyers.',
    targetAudience: 'Mom-and-pop shop owners, local artisans, home service providers.',
    nonTechScore: 94,
    measurableValueScore: 97,
    plainLanguageScore: 95,
    commonProblemScore: 98,
    tags: ['Small Business', 'Marketing', 'Low Budget'],
    beginnerPrompt: 'Act as a local business mentor. Give me 3 weekend promotional ideas for a [BUSINESS_TYPE] with $0 paid ad spend. Include a headline for a printed paper flyer.',
    advancedPrompt: 'Remember Me Profile: Business Name: [BIZ_NAME], Target Audience: [AUDIENCE]. Generate a 3-part campaign: 1. Neighborhood partnership proposal, 2. Printed flyer draft, 3. Social post script.'
  },
  {
    id: 'sol-3',
    title: 'Fixed-Income Grocery Inflation Optimizer',
    categoryId: 'productivity',
    categoryName: 'Personal Productivity',
    problem: 'Rising food costs make monthly grocery budgeting difficult for seniors and students.',
    solution: 'Snaps receipt or pantry photo to create a 4-category low-cost meal plan using items under $3.',
    plainLanguageSummary: 'Helps you stretch your food budget by turning what you already have in your kitchen into low-cost meals.',
    targetAudience: 'Seniors on fixed incomes, college students, budget-conscious families.',
    nonTechScore: 96,
    measurableValueScore: 98,
    plainLanguageScore: 97,
    commonProblemScore: 99,
    tags: ['Budgeting', 'Food', 'Seniors'],
    beginnerPrompt: 'Take a picture of my grocery store sales ad or pantry. Give me a 5-day dinner meal plan using ingredients under $3 each. Format as a simple printable checklist.',
    advancedPrompt: 'Remember Me Profile: Dietary: [DIET_RESTRICTIONS], Household Size: [FAMILY_SIZE]. Analyze attached store ad image. Build shopping list grouped by store aisle with target budget cap.'
  },
  {
    id: 'sol-4',
    title: 'Senior Router & Home Wi-Fi Tech Guide',
    categoryId: 'community',
    categoryName: 'Home & Planning',
    problem: 'Elderly users get frustrated trying to reconnect devices to Wi-Fi or fix TV connections.',
    solution: 'Translates technical network errors into physical button actions on their router box.',
    plainLanguageSummary: 'Tells seniors exactly which physical button to press on their Wi-Fi box without opening confusing phone settings menus.',
    targetAudience: 'Non-technical seniors living independently.',
    nonTechScore: 99,
    measurableValueScore: 94,
    plainLanguageScore: 98,
    commonProblemScore: 95,
    tags: ['Tech Support', 'Wi-Fi', 'Senior Friendly'],
    beginnerPrompt: 'My Wi-Fi stopped working. Look at this photo of my internet box router. Tell me which light is off and which button I should press for 10 seconds to reset it.',
    advancedPrompt: 'Remember Me Profile: Router Brand: [ROUTER_BRAND], ISP: [ISP_NAME]. Diagnose attached LED light status photo. Step-by-step physical recovery instructions in 3 steps.'
  },
  {
    id: 'sol-5',
    title: 'Theoretical Antigravity & Physics Explainer (Benchmark Scenario 9)',
    categoryId: 'education',
    categoryName: 'Education & Study',
    problem: 'Explaining complex theoretical physics (like levitation or quantum mechanics) without terrifying non-technical readers.',
    solution: 'Uses real-world physical analogies (like holding two repelling refrigerator magnets) to make friction-free conceptual bridges.',
    plainLanguageSummary: 'Explains complex science concepts using simple physical analogies anyone can feel in their own hands.',
    targetAudience: 'Non-tech seniors, students, and curious learners.',
    nonTechScore: 99,
    measurableValueScore: 96,
    plainLanguageScore: 100,
    commonProblemScore: 92,
    tags: ['Benchmark', 'Antigravity', 'Physics', 'Plain Language'],
    beginnerPrompt: 'OBJECTIVE: Explain magnetic levitation and antigravity concepts to an 81-year-old. CONSTRAINTS: 6th-grade reading level, maximum 150 words. Relate it to holding two refrigerator magnets pushing against each other.',
    advancedPrompt: 'Remember Me Profile: Learner Age 81, prefers physical analogies. Explain superconductor quantum locking in 3 bullet points using train track magnets.'
  }
];

export const INITIAL_PROMPT_LIBRARIES: PromptLibrary[] = [
  {
    id: 'lib-1',
    title: 'Library 1: Research Methods',
    keyword: '#RESEARCH',
    description: 'Deconstruct complex topics into plain-language bullet points and verifiable facts.',
    prompts: [
      {
        id: 'p-1',
        title: '6th-Grade Plain Language Explainer',
        libraryId: 'lib-1',
        tier: 'beginner',
        objective: 'Explain a complex concept using everyday analogies.',
        format: '1 sentence summary + 3 bullet points + 1 real-world example.',
        constraints: 'No words over 3 syllables. Maximum 120 words.',
        reasoningReq: false,
        compiledPrompt: 'OBJECTIVE: Explain [TOPIC] simply. FORMAT: 1-sentence summary, 3 short bullet points, 1 real-world example. CONSTRAINTS: No jargon, 6th-grade reading level, max 120 words.',
        variables: ['TOPIC'],
        difficulty: 'Easy'
      }
    ]
  },
  {
    id: 'lib-2',
    title: 'Library 2: Problem Solving Frameworks',
    keyword: '#SOLVE',
    description: 'Structured decision trees, root cause analysis, and 3-step action steps.',
    prompts: [
      {
        id: 'p-3',
        title: '3-Step Emergency Action Plan',
        libraryId: 'lib-2',
        tier: 'beginner',
        objective: 'Provide immediate prioritized steps for an urgent everyday problem.',
        format: 'Step 1 (Do Now), Step 2 (Do Next), Step 3 (Verify).',
        constraints: 'Action-oriented verbs only. Plain text.',
        reasoningReq: false,
        compiledPrompt: 'OBJECTIVE: Solve immediate issue: [PROBLEM]. FORMAT: Step 1 (Do Now), Step 2 (Do Next), Step 3 (Verify). CONSTRAINTS: Under 100 words total.',
        variables: ['PROBLEM'],
        difficulty: 'Easy'
      }
    ]
  }
];

// COMPLETE 8-BOOK SERIES INITIAL DATA
export const INITIAL_BOOKLET_TEMPLATES: BookletTemplate[] = [
  {
    id: 'bk-1',
    bookNumber: 1,
    title: 'Utensil Theories: Home & Planning',
    category: 'Home & Planning',
    coverGradient: 'linear-gradient(145deg, #0A1F5C 0%, #0044BB 60%, #0066FF 100%)',
    priceTag: '$2',
    tier: 'beginner',
    description: 'Book 1 of 8: Deep Ocean → Electric Blue. Home & Planning solutions for household bills, doctor notes, utility notices, and tech support.',
    sheetOrder: [8, 1, 4, 5, 7, 2, 3, 6],
    author: 'Utensil Theories Lab',
    printCount: 840,
    pages: [
      { pageNumber: 1, title: 'Home & Planning Companion', contentType: 'cover', bodyText: 'Your everyday guide to solving medications, bills, and tech questions in seconds.', tipBox: 'Scan QR or snap any page with your camera!' },
      { pageNumber: 2, title: 'Doctor Notes & Pill Bottle Reader', contentType: 'prompt', bodyText: 'Never struggle with tiny prescription labels or medical jargon again.', promptBox: 'Take a picture of this page + doctor note. List medicine names & exact daily times with food in large plain text.' },
      { pageNumber: 3, title: 'Utility Bill & Notice Explainer', contentType: 'prompt', bodyText: 'Confusing water, electric, or Medicare letters made simple.', promptBox: 'Read attached letter. Explain what I owe, due date, and if action is needed in 2 simple bullets.' },
      { pageNumber: 4, title: 'Senior Tech & Wi-Fi Helper', contentType: 'prompt', bodyText: 'Fix TV and router issues using physical buttons.', promptBox: 'Look at attached router photo. Tell me which button to hold for 10 seconds to reset.' },
      { pageNumber: 5, title: 'Anti-Scam Letter Checker', contentType: 'prompt', bodyText: 'Verify suspicious mail or bill demands before paying.', promptBox: 'Read attached letter photo. Is this an official bill or potential scam? Give 1 clear warning.' },
      { pageNumber: 6, title: 'Visual Folding Guide', contentType: 'visual_guide', bodyText: 'Fold paper in half twice. Cut central slit line. Pop open into 8-page booklet!', diagramType: 'zine_fold_diagram' },
      { pageNumber: 7, title: 'Voice Hotline Quick Guide', contentType: 'prompt', bodyText: 'Call 1-800-UTENSIL anytime for voice-assisted help.', tipBox: 'Speak passphrase "SUNSHINE" on phone.' },
      { pageNumber: 8, title: 'Official Senior ID Card', contentType: 'back_cover', bodyText: 'Utensil Theories Transfer Protocol #UTTP-BK1-2026. Licensed for community center distribution.', tipBox: 'Scan QR code to open Web Studio.' }
    ]
  },
  {
    id: 'bk-2',
    bookNumber: 2,
    title: 'Utensil Theories: Education & Study',
    category: 'Education & Study',
    coverGradient: 'linear-gradient(145deg, #7B3F00 0%, #D47A00 60%, #F5A623 100%)',
    priceTag: '$2',
    tier: 'beginner',
    description: 'Book 2 of 8: Warm Amber → Golden Yellow. Feynman micro-study guides, math summaries, and theoretical physics explainers.',
    sheetOrder: [8, 1, 4, 5, 7, 2, 3, 6],
    author: 'Utensil Theories Edu Team',
    printCount: 520,
    pages: [
      { pageNumber: 1, title: 'Education & Study Guide', contentType: 'cover', bodyText: 'Micro-study guides and plain-language summaries for complex subjects.', tipBox: 'Includes Feynman technique templates.' },
      { pageNumber: 2, title: 'Theoretical Physics & Antigravity', contentType: 'prompt', bodyText: 'Understand levitation and physics using magnet analogies.', promptBox: 'Explain magnetic levitation to an 81yo using refrigerator magnet analogies in 3 bullets.' },
      { pageNumber: 3, title: 'Feynman Micro-Study Sheet', contentType: 'prompt', bodyText: 'Deconstruct any textbook chapter in 3 steps.', promptBox: 'Teach [SUBJECT] using 1 core idea, 1 everyday analogy, and 2 quiz questions.' },
      { pageNumber: 4, title: 'Math & Formula Simplifier', contentType: 'prompt', bodyText: 'Turn confusing word problems into step-by-step algebra actions.', promptBox: 'Solve attached math problem photo. Show 3 plain language steps.' },
      { pageNumber: 5, title: 'Flashcard Generator', contentType: 'prompt', bodyText: 'Create 5 study flashcards for any topic.', promptBox: 'Generate 5 question & answer flashcards for [TOPIC].' },
      { pageNumber: 6, title: 'Visual Folding Guide', contentType: 'visual_guide', bodyText: 'Fold paper in half twice. Cut central slit line. Pop open into 8-page booklet!', diagramType: 'zine_fold_diagram' },
      { pageNumber: 7, title: 'Exam Anxiety Relief Prompt', contentType: 'prompt', bodyText: 'Quick 2-minute focus breathing technique.', promptBox: 'Give 3 calming steps before taking an exam.' },
      { pageNumber: 8, title: 'Utensil Edu Back Cover', contentType: 'back_cover', bodyText: 'Utensil Theories Protocol #UTTP-BK2-2026. Education Edition.', tipBox: 'Scan QR for digital flashcards.' }
    ]
  },
  {
    id: 'bk-3',
    bookNumber: 3,
    title: 'Utensil Theories: Entertainment & Games',
    category: 'Entertainment & Games',
    coverGradient: 'linear-gradient(145deg, #8B0000 0%, #CC2200 60%, #FF4500 100%)',
    priceTag: '$2',
    tier: 'beginner',
    description: 'Book 3 of 8: Coral Red → Bright Orange. Family game rules, interactive story generators, and trivia companions.',
    sheetOrder: [8, 1, 4, 5, 7, 2, 3, 6],
    author: 'Utensil Theories Fun Lab',
    printCount: 410,
    pages: [
      { pageNumber: 1, title: 'Entertainment & Games', contentType: 'cover', bodyText: 'Family board game rules, trivia games, and interactive story prompts.', tipBox: 'Fun for family game nights!' },
      { pageNumber: 2, title: 'Board Game Rule Summarizer', contentType: 'prompt', bodyText: 'Explain any board game setup in 60 seconds.', promptBox: 'Take a picture of board game box. List setup steps and win condition in 3 bullets.' },
      { pageNumber: 3, title: 'Family Trivia Master', contentType: 'prompt', bodyText: 'Generate 10 trivia questions for any era or theme.', promptBox: 'Generate 10 1970s pop culture trivia questions with hidden answers.' },
      { pageNumber: 4, title: 'Bedtime Story Generator', contentType: 'prompt', bodyText: 'Create a personalized 3-minute bedtime story.', promptBox: 'Tell a story about a friendly robot cat named [NAME] in 3 short paragraphs.' },
      { pageNumber: 5, title: 'Movie Night Picker', contentType: 'prompt', bodyText: 'Pick the perfect movie for 3 different tastes.', promptBox: 'Suggest 3 movies matching genres: [GENRE1] and [GENRE2].' },
      { pageNumber: 6, title: 'Visual Folding Guide', contentType: 'visual_guide', bodyText: 'Fold paper in half twice. Cut central slit line. Pop open into booklet!', diagramType: 'zine_fold_diagram' },
      { pageNumber: 7, title: 'Party Charades Prompt', contentType: 'prompt', bodyText: 'Instant charades word generator.', promptBox: 'List 10 funny charades words for all ages.' },
      { pageNumber: 8, title: 'Utensil Fun Back Cover', contentType: 'back_cover', bodyText: 'Utensil Theories Protocol #UTTP-BK3-2026. Entertainment Edition.', tipBox: 'Scan QR for online game master.' }
    ]
  },
  {
    id: 'bk-4',
    bookNumber: 4,
    title: 'Utensil Theories: Small Business',
    category: 'Small Business',
    coverGradient: 'linear-gradient(145deg, #1C1C1C 0%, #44505C 60%, #708090 100%)',
    priceTag: '$2',
    tier: 'advanced',
    description: 'Book 4 of 8: Charcoal → Steel Silver. Small business survival tools, $50 promos, physical paper flyers, and vendor scripts.',
    sheetOrder: [8, 1, 4, 5, 7, 2, 3, 6],
    author: 'Utensil Theories Biz Lab',
    printCount: 950,
    pages: [
      { pageNumber: 1, title: 'Small Business Survival', contentType: 'cover', bodyText: 'Turn AI into your 24/7 marketing manager. Advanced prompt frameworks with Remember Me context.', tipBox: 'Includes Remember Me context integration.' },
      { pageNumber: 2, title: 'Remember Me Profile Setup', contentType: 'prompt', bodyText: 'Stores business name, location, target customer profile, and monthly ad budget.', promptBox: 'Remember Me Context: Biz Name: [NAME], City: [CITY], Niche: [NICHE].' },
      { pageNumber: 3, title: 'Paper Flyer Engine', contentType: 'prompt', bodyText: 'High-conversion physical flyer copy for bulletin boards.', promptBox: 'Generate 1-page paper flyer headline & 3 value points for [BIZ_NAME].' },
      { pageNumber: 4, title: 'Customer Review Responder', contentType: 'prompt', bodyText: 'Reply to positive and negative Google reviews gracefully.', promptBox: 'Draft empathetic response to 3-star review regarding wait time.' },
      { pageNumber: 5, title: 'Supplier Pricing Negotiator', contentType: 'prompt', bodyText: 'Draft courteous emails asking vendors for bulk discounts.', promptBox: 'Write formal email asking vendor for 10% volume discount.' },
      { pageNumber: 6, title: 'Weekly Sales Plan', contentType: 'prompt', bodyText: 'Turn slow Tuesdays into high-traffic promotion days.', promptBox: 'Create 3 Tuesday-only bundle offers for local residents.' },
      { pageNumber: 7, title: 'Market Metrics Tracker', contentType: 'visual_guide', bodyText: 'Track booklets printed vs foot traffic gained using Step 4 analytics.', diagramType: 'analytics_chart' },
      { pageNumber: 8, title: 'Business Toolkit Back', contentType: 'back_cover', bodyText: 'Utensil Theories Protocol #UTTP-BK4-2026. Scalable local business tools.', tipBox: 'Print & distribute to local merchant associations.' }
    ]
  },
  {
    id: 'bk-5',
    bookNumber: 5,
    title: 'Utensil Theories: Personal Productivity',
    category: 'Personal Productivity',
    coverGradient: 'linear-gradient(145deg, #1A3A1A 0%, #2A7744 60%, #3CB371 100%)',
    priceTag: '$2',
    tier: 'beginner',
    description: 'Book 5 of 8: Forest Green → Mint. Grocery inflation optimizers, daily routine organizers, and task prioritization.',
    sheetOrder: [8, 1, 4, 5, 7, 2, 3, 6],
    author: 'Utensil Theories Productivity Lab',
    printCount: 480,
    pages: [
      { pageNumber: 1, title: 'Personal Productivity', contentType: 'cover', bodyText: 'Task prioritization, grocery inflation savings, and household routine planning.', tipBox: 'Maximize your daily momentum.' },
      { pageNumber: 2, title: 'Grocery Inflation Optimizer', contentType: 'prompt', bodyText: 'Turn pantry items into low-cost meals.', promptBox: 'Photo of store ad or pantry -> Give 5-day dinner meal plan using ingredients under $3 each.' },
      { pageNumber: 3, title: 'Daily Eisenhower Matrix', contentType: 'prompt', bodyText: 'Prioritize your to-do list into 4 quadrants.', promptBox: 'Group my list of tasks into Urgent/Important quadrants: [TASKS].' },
      { pageNumber: 4, title: 'Email Inbox Zero Assistant', contentType: 'prompt', bodyText: 'Draft quick 1-sentence polite email replies.', promptBox: 'Draft polite 1-sentence reply accepting invitation for [EVENT].' },
      { pageNumber: 5, title: 'Weekly Meal Prep Planner', contentType: 'prompt', bodyText: '30-minute Sunday prep plan.', promptBox: 'Generate 3 batch meal prep recipes for the week.' },
      { pageNumber: 6, title: 'Visual Folding Guide', contentType: 'visual_guide', bodyText: 'Fold paper in half twice. Cut central slit line. Pop open into booklet!', diagramType: 'zine_fold_diagram' },
      { pageNumber: 7, title: 'Habit Tracker Setup', contentType: 'prompt', bodyText: 'Track 3 daily habits effortlessly.', promptBox: 'Create 30-day habit grid for walking, reading, and water.' },
      { pageNumber: 8, title: 'Utensil Productivity Back', contentType: 'back_cover', bodyText: 'Utensil Theories Protocol #UTTP-BK5-2026. Productivity Edition.', tipBox: 'Scan QR for printable planner.' }
    ]
  },
  {
    id: 'bk-6',
    bookNumber: 6,
    title: 'Utensil Theories: Creative Hobbies',
    category: 'Creative Hobbies',
    coverGradient: 'linear-gradient(145deg, #2D0057 0%, #602588 60%, #9B59B6 100%)',
    priceTag: '$2',
    tier: 'beginner',
    description: 'Book 6 of 8: Deep Violet → Soft Lavender. Voice-assisted gardening, knitting, painting, and woodworking companions.',
    sheetOrder: [8, 1, 4, 5, 7, 2, 3, 6],
    author: 'Utensil Theories Craft Team',
    printCount: 360,
    pages: [
      { pageNumber: 1, title: 'Creative Hobbies', contentType: 'cover', bodyText: 'Voice-assisted gardening guides, knitting steps, and craft blueprints.', tipBox: 'Speak steps out loud while working!' },
      { pageNumber: 2, title: 'Voice Gardening Assistant', contentType: 'prompt', bodyText: 'Identify plant diseases and watering schedules hands-free.', promptBox: 'Take a photo of yellow plant leaf. Diagnose issue and give 2 care steps.' },
      { pageNumber: 3, title: 'Beginner Knitting & Crochet', contentType: 'prompt', bodyText: 'Step-by-step stitch guide with pause reminders.', promptBox: 'Guide single crochet stitch in 3 speakable steps.' },
      { pageNumber: 4, title: 'Color Palette Generator', contentType: 'prompt', bodyText: 'Generate harmonious color schemes for painting or decor.', promptBox: 'Give 4 complementary colors for a cozy living room.' },
      { pageNumber: 5, title: 'Woodworking Cut List', contentType: 'prompt', bodyText: 'Simple planter box cut dimensions.', promptBox: 'Generate cut list for a 2x4 wooden planter box.' },
      { pageNumber: 6, title: 'Visual Folding Guide', contentType: 'visual_guide', bodyText: 'Fold paper in half twice. Cut central slit line. Pop open into booklet!', diagramType: 'zine_fold_diagram' },
      { pageNumber: 7, title: 'Craft Project Planner', contentType: 'prompt', bodyText: 'Estimate materials & budget for DIY projects.', promptBox: 'List materials needed for DIY birdhouse.' },
      { pageNumber: 8, title: 'Utensil Hobbies Back', contentType: 'back_cover', bodyText: 'Utensil Theories Protocol #UTTP-BK6-2026. Hobbies Edition.', tipBox: 'Scan QR for voice craft helper.' }
    ]
  },
  {
    id: 'bk-7',
    bookNumber: 7,
    title: 'Utensil Theories: Family & Relationships',
    category: 'Family & Relationships',
    coverGradient: 'linear-gradient(145deg, #8B3A3A 0%, #C08070 60%, #F5CBA7 100%)',
    priceTag: '$2',
    tier: 'beginner',
    description: 'Book 7 of 8: Dusty Rose → Warm Cream. Caregiver guides, family elder care schedules, and meaningful conversation starters.',
    sheetOrder: [8, 1, 4, 5, 7, 2, 3, 6],
    author: 'Utensil Theories Family Lab',
    printCount: 430,
    pages: [
      { pageNumber: 1, title: 'Family & Relationships', contentType: 'cover', bodyText: 'Caregiver companions, elder care schedules, and meaningful conversation starters.', tipBox: 'Strengthen family connections.' },
      { pageNumber: 2, title: 'Caregiver Doctor Visit Prep', contentType: 'prompt', bodyText: 'Prepare 3 key questions before elder doctor visits.', promptBox: 'List top 3 questions for doctor regarding [CONDITION].' },
      { pageNumber: 3, title: 'Grandparent Conversation Starters', contentType: 'prompt', bodyText: '10 thoughtful storytelling questions for family dinners.', promptBox: 'List 5 heartwarming questions to ask grandparents about their childhood.' },
      { pageNumber: 4, title: 'Family Chore & Care Schedule', contentType: 'prompt', bodyText: 'Balance caregiving duties across family members.', promptBox: 'Create 1-week family care rotation schedule.' },
      { pageNumber: 5, title: 'Conflict Resolution Script', contentType: 'prompt', bodyText: 'Draft calm, respectful messages for family misunderstandings.', promptBox: 'Draft calm message opening conversation about [TOPIC].' },
      { pageNumber: 6, title: 'Visual Folding Guide', contentType: 'visual_guide', bodyText: 'Fold paper in half twice. Cut central slit line. Pop open into booklet!', diagramType: 'zine_fold_diagram' },
      { pageNumber: 7, title: 'Family Event Planner', contentType: 'prompt', bodyText: 'Plan a stress-free family reunion menu.', promptBox: 'Suggest easy buffet menu for 12 family members.' },
      { pageNumber: 8, title: 'Utensil Family Back', contentType: 'back_cover', bodyText: 'Utensil Theories Protocol #UTTP-BK7-2026. Family Edition.', tipBox: 'Scan QR for family audio book.' }
    ]
  },
  {
    id: 'bk-8',
    bookNumber: 8,
    title: 'Utensil Theories: Health & Wellness',
    category: 'Health & Wellness',
    coverGradient: 'linear-gradient(145deg, #004D4D 0%, #008B8B 60%, #00CED1 100%)',
    priceTag: '$2',
    tier: 'beginner',
    description: 'Book 8 of 8: Deep Teal → Aqua. Senior medication schedules, blood pressure logs, and gentle mobility exercise routines.',
    sheetOrder: [8, 1, 4, 5, 7, 2, 3, 6],
    author: 'Utensil Theories Health Team',
    printCount: 670,
    pages: [
      { pageNumber: 1, title: 'Health & Wellness', contentType: 'cover', bodyText: 'Medication schedules, blood pressure logs, and gentle mobility routines.', tipBox: 'Designed for daily patient clarity.' },
      { pageNumber: 2, title: 'Pill Bottle & Prescription Schedule', contentType: 'prompt', bodyText: 'Format tiny medicine labels into 3 large daily steps.', promptBox: 'Read attached pill bottle. List medicine name & exact times to take with food.' },
      { pageNumber: 3, title: 'Blood Pressure & Sugar Log', contentType: 'prompt', bodyText: 'Format daily health readings for doctor reviews.', promptBox: 'Organize blood pressure readings into 1-page table for doctor.' },
      { pageNumber: 4, title: 'Gentle Seated Mobility Routine', contentType: 'prompt', bodyText: '5-minute chair stretches for joint flexibility.', promptBox: 'Give 3 safe seated chair stretches for seniors.' },
      { pageNumber: 5, title: 'Hydration & Nutrition Tracker', contentType: 'prompt', bodyText: 'Track daily water intake and low-sodium meals.', promptBox: 'Create 1-day low-sodium meal plan with 8 water reminders.' },
      { pageNumber: 6, title: 'Visual Folding Guide', contentType: 'visual_guide', bodyText: 'Fold paper in half twice. Cut central slit line. Pop open into booklet!', diagramType: 'zine_fold_diagram' },
      { pageNumber: 7, title: 'Emergency Medical Summary', contentType: 'prompt', bodyText: 'Wallet-sized medical emergency summary.', promptBox: 'Format wallet emergency card with allergies and doctor contact.' },
      { pageNumber: 8, title: 'Utensil Health Back', contentType: 'back_cover', bodyText: 'Utensil Theories Protocol #UTTP-BK8-2026. Health Edition.', tipBox: 'Scan QR for emergency hotline.' }
    ]
  }
];

export const INITIAL_MARKET_METRICS: MarketMetric[] = [
  {
    id: 'm-1',
    bookletId: 'bk-1',
    bookletTitle: 'Utensil Theories: Home & Planning',
    producedCount: 150,
    distributedCount: 135,
    soldCount: 92,
    unitPrice: 2.00,
    totalRevenue: 184.00,
    productionTimeHours: 4.5,
    averageRating: 4.9,
    repeatInterestRate: 88,
    feedbackNotes: ['"My grandmother could finally understand how to use ChatGPT!"', '"The $2 price tag and 1-sheet zine folding guide was super clever."'],
    phase: 'market_testing',
    dateLogged: '2026-08-01'
  },
  {
    id: 'm-2',
    bookletId: 'bk-4',
    bookletTitle: 'Utensil Theories: Small Business',
    producedCount: 200,
    distributedCount: 180,
    soldCount: 145,
    unitPrice: 2.00,
    totalRevenue: 290.00,
    productionTimeHours: 6.0,
    averageRating: 4.8,
    repeatInterestRate: 82,
    feedbackNotes: ['"Printed 50 copies for our local farmers market vendors. Sold out in 2 hours!"'],
    phase: 'analysis',
    dateLogged: '2026-08-08'
  }
];

// COMPREHENSIVE SIMULATION BENCHMARK DATA ACROSS ALL 8 BOOKS & BOTTLENECK ANALYSIS
export const INITIAL_SIMULATIONS: SimulationResult[] = [
  {
    id: 'sim-1',
    scenarioTitle: '1. Senior Medication & Doctor Notes (Book 1 & 8)',
    difficultyArea: 'Health & Wellness',
    modelName: 'Google Gemini 1.5 Pro (Vision)',
    tier: 'beginner',
    promptText: 'OBJECTIVE: Extract doctor notes. FORMAT: 1. Medicine names in large font. 2. Exact times (Morning, Noon, Night) with food. CONSTRAINTS: 3 bullets, 6th-grade reading level.',
    rawOutput: '💊 YOUR DAILY MEDICATION SCHEDULE:\n\n• LISINOPRIL (10mg): Take 1 pill every morning with breakfast.\n• METFORMIN (500mg): Take 1 pill at noon with lunch and water.\n• ATORVASTATIN (20mg): Take 1 pill at night before sleep.',
    plainLanguageScore: 99,
    zeroTechScore: 98,
    executionTimeMs: 420,
    status: 'PASSED'
  },
  {
    id: 'sim-2',
    scenarioTitle: '2. Theoretical Physics & Antigravity (Book 2)',
    difficultyArea: 'Education & Study / Antigravity',
    modelName: 'Google Gemini 1.5 Flash',
    tier: 'beginner',
    promptText: 'OBJECTIVE: Explain theoretical antigravity and magnetic levitation to an 81-year-old using a walker. CONSTRAINTS: 6th-grade reading level, max 150 words. Relate it to holding two refrigerator magnets pushing against each other.',
    rawOutput: '🧲 HOW ANTIGRAVITY LEVITATION WORKS:\n\nImagine holding two refrigerator magnets in your hands. When you turn them so the same ends face each other, they push apart. You can feel an invisible force pushing back!\n\n• Antigravity levitation works the exact same way.\n• Powerful magnets push against a metal track to float a train in mid-air.\n• Because the train floats, there is no bumping or friction—it glides smoothly like ice!\n\nIt is not magic—just magnets pushing against each other to lift heavy weight weightlessly!',
    plainLanguageScore: 100,
    zeroTechScore: 99,
    executionTimeMs: 310,
    status: 'PASSED'
  },
  {
    id: 'sim-3',
    scenarioTitle: '3. Small Business $50 Marketing Promo (Book 4)',
    difficultyArea: 'Small Business',
    modelName: 'Microsoft Copilot / GPT-4o',
    tier: 'advanced',
    promptText: 'Remember Me Profile: Bakery, Downtown. OBJECTIVE: 3 weekend promotional ideas with $0 ad spend + 1 paper flyer headline.',
    rawOutput: '🥐 WEEKEND BAKERY BOOSTER:\n\n1. Free Coffee with Croissant 7am-9am.\n2. Neighborhood Partner Bulletin Swap.\n3. Printed Paper Flyer Headline: "Fresh Hot Cinnamon Rolls Baked at 8AM!"',
    plainLanguageScore: 96,
    zeroTechScore: 94,
    executionTimeMs: 510,
    status: 'PASSED'
  },
  {
    id: 'sim-4',
    scenarioTitle: '4. Board Game Rule Summarizer (Book 3)',
    difficultyArea: 'Entertainment & Games',
    modelName: 'Google Gemini 1.5 Flash (Vision)',
    tier: 'beginner',
    promptText: 'OBJECTIVE: Read board game box. FORMAT: 1. Setup in 2 steps. 2. How to win in 1 sentence. CONSTRAINTS: Under 80 words.',
    rawOutput: '🎲 GAME RULES SUMMARY:\n\nSetup: Deal 7 cards to each player and place remaining deck in center.\nWin Condition: Be the first player to play all your cards by matching colors or numbers!',
    plainLanguageScore: 98,
    zeroTechScore: 97,
    executionTimeMs: 380,
    status: 'PASSED'
  },
  {
    id: 'sim-5',
    scenarioTitle: '5. Grocery Inflation Pantry Meal Plan (Book 5)',
    difficultyArea: 'Personal Productivity',
    modelName: 'Google Gemini 1.5 Pro',
    tier: 'beginner',
    promptText: 'OBJECTIVE: Pantry photo -> 5 dinner meals using ingredients under $3 each. FORMAT: Simple printable checklist.',
    rawOutput: '🛒 $3 DINNER CHECKLIST:\n\n[ ] Mon: Black Bean & Cheese Quesadillas ($1.80/serving)\n[ ] Tue: Vegetable Rice Stir-fry ($2.10/serving)\n[ ] Wed: Tomato Basil Pasta ($1.90/serving)\n[ ] Thu: Egg & Potato Hash ($1.50/serving)\n[ ] Fri: Tuna Salad Wraps ($2.40/serving)',
    plainLanguageScore: 97,
    zeroTechScore: 96,
    executionTimeMs: 440,
    status: 'PASSED'
  },
  {
    id: 'sim-6',
    scenarioTitle: '6. Voice Gardening Plant Diagnosis (Book 6)',
    difficultyArea: 'Creative Hobbies',
    modelName: 'Google Gemini 1.5 Flash (Vision)',
    tier: 'beginner',
    promptText: 'OBJECTIVE: Yellow plant leaf photo -> Diagnose issue and give 2 spoken care steps.',
    rawOutput: '🌿 PLANT CARE DIAGNOSIS:\n\nIssue: Over-watering / Nitrogen deficiency.\nStep 1: Allow top 2 inches of soil to dry completely before watering again.\nStep 2: Add 1 teaspoon of organic liquid fertilizer during next morning watering.',
    plainLanguageScore: 96,
    zeroTechScore: 98,
    executionTimeMs: 350,
    status: 'PASSED'
  },
  {
    id: 'sim-7',
    scenarioTitle: '7. Caregiver Doctor Visit Question Prep (Book 7)',
    difficultyArea: 'Family & Relationships',
    modelName: 'Microsoft Copilot',
    tier: 'beginner',
    promptText: 'OBJECTIVE: Top 3 questions for elder doctor visit regarding arthritis pain medication.',
    rawOutput: '📋 DOCTOR VISIT QUESTIONS:\n\n1. Are there non-drowsy alternatives for arthritis pain?\n2. Should this medication be taken with breakfast or water?\n3. What physical therapy exercises can help joint mobility at home?',
    plainLanguageScore: 98,
    zeroTechScore: 97,
    executionTimeMs: 390,
    status: 'PASSED'
  },
  {
    id: 'sim-8',
    scenarioTitle: '8. Anti-Scam Mail & Demand Checker (Book 1)',
    difficultyArea: 'Home & Planning',
    modelName: 'Google Gemini 1.5 Pro (Vision)',
    tier: 'beginner',
    promptText: 'OBJECTIVE: Read letter photo. Determine if official bill or scam attempt. Give 1 clear warning.',
    rawOutput: '⚠️ MAIL SAFETY VERDICT:\n\nStatus: SUSPICIOUS / POTENTIAL SCAM.\nReason: The letter demands payment via gift card or wire transfer for an unlisted "domain renewal".\nAction: DO NOT PAY. Throw letter in trash or verify by calling official company number on your past bill.',
    plainLanguageScore: 100,
    zeroTechScore: 99,
    executionTimeMs: 480,
    status: 'PASSED'
  }
];

export const DEFAULT_SENIOR_USER: UserAccount = {
  id: 'usr-senior-1',
  name: 'Margaret Miller',
  email: 'margaret.miller@example.com',
  phone: '(555) 019-2834',
  role: 'senior',
  securityLevel: 'ultra_vault',
  blockLetterVerified: true,
  voiceVerified: true,
  registeredAt: '2026-08-01',
  recognizedDeviceIds: ['device-mobile-primary-991'],
  memoryContext: {
    age: 78,
    techLevel: 'Beginner (Prefers large fonts & voice instructions)',
    healthConditions: ['Mild Arthritis in hands', 'Takes Lisinopril 10mg'],
    mobilityNotes: 'Uses walking cane',
    preferredTone: 'Warm, direct, respectful, zero jargon',
    emergencyContact: 'Robert Miller (Son) - (555) 998-1122',
    securityPassphrase: 'SUNSHINE'
  }
};
