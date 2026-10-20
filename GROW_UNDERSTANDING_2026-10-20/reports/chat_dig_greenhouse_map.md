# Brute-force dig through the chat: the greenhouse pieces and the final piece (20 October 2026)

Every message the owner typed in this conversation (34 messages) was read in order. Each piece the owner gave was matched to the project mechanism it became, and to what it means for seeds and compression. Only the owner's words about the method and ideas are quoted. 'L' numbers are line positions in the chat log.


## The synthesis

Read in order, the 34 owner messages describe one thing grown in stages. Day 1 laid the soil: text alone, read the way a blind person learns color, with human error as the signal ("a mistake is the calibration point"). It built the greenhouse: a tiny model trained on the Bible. On the evening of day 1 the owner set the humidity and the sun's rotation: a carried "remaining" balance, reset to ±17 on clear events and faded by following words, written as rotating spellings so as to "shift the coin toss". Day 2 checked the air and the bugs: pre-registered rules, scrambled controls, a drift guard, and reviewers who caught real bugs. Today came the seed: the expression [+2×y(...)÷(...)yx2]. The owner then refined how it grows, step by step: no AI needed, only add, subtract, multiply, restart or work backwards; a graph of 0/1 points stacked into a fixed page of binary; a shared library where strawberry and orange are expected and the cucumber is the odd one out; and a palm seed that must grow by the same instructions in any igloo. The piece that joins them is that the owner's "coin toss" is the unit of the page of binary. A greenhouse that understands tilts each toss toward what really comes next, and the seed only has to record the surprises. That is arithmetic coding, and its seed size equals the model's loss, so understanding and compression are literally one number. That number has been in this chat since day 1: the tiny model's held-out loss of about 5 bits per word, against 13 for a bare word list, predicts an exact seed about 2.3 times smaller than xz on held-out verses. The ladder now running should confirm or refute that. The library half explains the owner's own 98.9%/100% results: with the Bible already on the shared shelf, naming a verse costs about 1.9 bytes against 132.5, which is 98.6% smaller and exact. The limit is that this only works for what is already on the shelf. Two more findings sharpen the picture. The seed expression is an exact mirror around its ÷ sign, so "worked backwards" is built into it: grow is plant run in reverse, and the mirror check is the exactness check. The shifting word is computed only from earlier text, so a grower can recompute it for free, and the bits a model spends predicting its own marker are a direct gauge of whether it has learned the carried state. Arithmetic coding, library pointers and Burrows-Wheeler already exist, so they cannot be the owner's credit. A measured drop in exact-seed size on unseen text from the owner's carried-balance marker, or from the owner's untested "W1 = 17 + 4" excess-bank rule, would be the owner's own. So would the communication version: a shared codebook that lets fewer words land an exact meaning between a person and an AI, testable through the owner-explanation test.


## Every greenhouse piece


### Soil (the base material both sides already hold)
- **The owner's words:** do a read of the Bible testing a few various ways of interpretation of tokens and words (L103, Oct 17); Lessons taught through story have more transferable data and relation vectors to give further understanding of things (L655)
- **What it is in the project:** KJV corpus via load_verses() (31,102 verses, 4.1 MB, fetched by URL from scrollmapper); world_stories.py (12 collections); NLTK novels; word tokenizer tiny_transformer.tok; held-out set = every 50th verse (623 verses).
- **What it means for seeds and compression:** The shared base both sides fetch for free, so it costs 0 seed bytes. A greenhouse can only be built from soil both sides have. Anything already in the soil regrows from a call number: one KJV verse = log2(31,102) = 14.9 bits, about 98.6% smaller, exact. The held-out verses test growth on ground the greenhouse never saw.

### Building the greenhouse
- **The owner's words:** yes try the tiny transformer next (L228); instructions to find the soil needed and to build a greenhouse (L3129)
- **What it is in the project:** tiny_transformer.py TinyGPT (4 layers, width 192, 4 heads, window CTX=64, 1500 steps, seeds 0-2); saved models in experiments/models/{baseline,scrambled,shifting,label,carry3}_seed{s}_steps1500.pt
- **What it means for seeds and compression:** The shared predictor. Its logged held-out loss of 3.46 nats/word is about 5.0 bits/word ('1 in 32'), against 13.1 bits/word for a bare word list of 8,658 words. That implies roughly an 11.7 KB seed for the 83.8 KB normalized held-out text. xz gives 26.4 KB and zlib 28.6 KB. This is an estimate from the loss, still to be measured with a real coder.

### Humidity (the setting that keeps growth alive without drowning it)
- **The owner's words:** it must reset to [w1=0] when a clear right or wrong choice exists. If wrong the sequence will begin with a value of (-17) and right a value of (+17) (L334); The rules are the secret of understanding (L103)
- **What it is in the project:** shifting_word.py: RESET=17 (watering on clear verdicts, via the CLEAR_WRONG/CLEAR_RIGHT regexes and the top/bottom CLEAR_PCT=3% of verses) vs SPEND=0.5 per valued word (evaporation), cap ±51 = 3×17. Known defect: 'carries perfectly but updates poorly'.
- **What it means for seeds and compression:** The adaptation rate of a context model: how fast old evidence fades vs how hard decisive events overwrite the state. Tuned well, it minimizes bits. If the air is too stagnant (the state never updates), predictions go stale and the seed grows.

### Rotation of the sun (a fixed cycle both sides follow in lockstep)
- **The owner's words:** The idea is based on a syllables rotation sequence rather than a logical one (L334)
- **What it is in the project:** The five spellings are rotations of sha-ru-vel-an-ok (anoksha, oksharu, velanok, sharuvel, ruvelan), with cut points at -12, -4, +4 and +12. The balance runs a day/night cycle: reset to ±17, then fade toward 0. The 64-token window slides forward, so the act 'sets' out of view, and the carried marker is the warmth left after sunset (experiment 11).
- **What it means for seeds and compression:** A deterministic schedule costs nothing to send if both sides run it. Verified in code: mark_up() calls emerge() before read(), so each marker depends only on earlier verses. The grower can recompute it, so it is free side information. Related known transform: sorting all rotations (Burrows-Wheeler, bzip2), which is inverted exactly by walking backwards.

### Checking the air inside
- **The owner's words:** ensure that yiur drifting does not pass to the next llm (L2428); Let's confirm the result (L506)
- **What it is in the project:** Pre-registered pass/fail rules, scrambled and shuffled controls, confirm.py on 100 new pairs, the drift guard in HANDOFF.md, and the audit session. seed_test.py grows each seed in a separate process inside an empty folder and checks exactness with SHA-256.
- **What it means for seeds and compression:** Clean air means no leakage: the grower never sees the original, the grow instructions are the same for every seed and counted once, and exactness is proven by fingerprint. The first script's SHA-256 'wavelength' (a 12-hex fingerprint that cannot regrow anything) returns as the exactness check.

### Microbes and bugs thriving (the small living ecosystem)
- **The owner's words:** The things  we do wrong naturally and have to be told not to do them is something ai must mimic to grasp reality as a human does (L103); pasted code: Maps human deviation (sins, mistakes, burdens) into calculable vectors (L2)
- **What it is in the project:** The many small checkers that found real bugs: ties counted as wrong, the carry3 KeyError, Aesop leakage and the punctuation shortcut. The controls. The <unk> escape for unknown words. The small statistics rungs (word list, word frequencies, word pairs = ladder R3-R5).
- **What it means for seeds and compression:** A healthy greenhouse handles the odd bits instead of killing them. The surprise/residual stream (unknown words spelled letter by letter, the 'cucumber') must be coded exactly. Human error is the residual the seed carries, and also what calibrates the greenhouse.

### The seed
- **The owner's words:** [+2×y(27/5.2+t=y/?)÷(?\y=t+2.5\72)yx2] ... (Seed=algebraic expression) (L2879, Oct 20)
- **What it is in the project:** The SEED block in the technical report (GOAL × METHOD × DATA × MODEL × MARKER); plant()/grow() in seed_test.py; methods/graph_fit.py, graph_locate.py and graph_backwards.py (drafts, checks pending).
- **What it means for seeds and compression:** The seed is only what the greenhouse cannot predict. New, verified fact: the expression is a mirror image around ÷. Reverse the left half and mirror each glyph (/→\, (→), ×→x) and you get the right half exactly; only the leading + has no partner. So 'worked backwards' is built into it, and half of it plus a mirror rule regrows the whole.

### Slowly more in-depth instructions as you built (growing shared context)
- **The owner's words:** Slowly I gave you more in depth instructions as you built (L3129); stopping at points to pull out more algebraic expressions to solve the simple (L2879)
- **What it is in the project:** Today's chain of instructions: data seed → electricity/security → no LLM ('add/subtract/multiply, restarted or worked backwards') → graph → page of 0/1 points + library → palm tree/OS → greenhouse. COMMUNICATION_GUIDE.md glossary, NEXT_SESSION_PROMPT.md, and the report's 10 grow steps with checkpoints.
- **What it means for seeds and compression:** The conversation is an adaptive compressor. As shared context grows, each later message needs fewer words ('Use a graph system lol' is 22 characters). The glossary is a codebook, and the checkpoints are where new sub-seeds are pulled out.

### Water and sunlight (grow instructions everyone already knows)
- **The owner's words:** Some already known like plants need water  and sunlight for example (L2879)
- **What it is in the project:** Public-domain texts fetched by URL; generic priors (word list, word frequencies); a built-in dictionary, as in the browser compressor Brotli or the zlib zdict (ladder R2).
- **What it means for seeds and compression:** Priors both sides get for free. The seed only pays for what the priors miss.

### Library factors: strawberry and orange versus cucumber
- **The owner's words:** library style factors called strawberry and orange verse cucumber (L2963)
- **What it is in the project:** Placeholder libraries in the three graph_*.py methods; ladder R2 (zlib with a shared 32 KB dictionary); the Bible's own book:chapter:verse numbering.
- **What it means for seeds and compression:** Items on the shared shelf (the fruit) cost a short call number or a high probability; the odd one out (the cucumber) is spelled out with an escape. Measured: with the KJV shelved in the greenhouse, a verse costs about 1.9 bytes against 132.5 bytes on average, 98.6% smaller and exact.

### The coin toss
- **The owner's words:** shift the "coin toss" towards the desired outcome (L334)
- **What it is in the project:** The chance level in every test; judging 69 vs 50 per 100 with marked training text.
- **What it means for seeds and compression:** Each 0/1 point on the page of binary is a coin toss. A fair coin costs 1 bit. Tilting it toward what really happens costs -log2(p) bits. The seed is the sum of the surprises, so 'shifting the coin toss' is exactly what makes a seed small.

### Palm tree seed taken to an igloo in Antarctica
- **The owner's words:** Imagine I buy a palm tree seed while on vacation and I get a set of instructions ... I must still follow given instructions ... What do you think happens between differing os and data transfer? (L3105)
- **What it is in the project:** The reply: integer-only arithmetic, raw bytes, and the same instructions for every seed. HANDOFF pins torch 2.14.1 / numpy 2.5.3. The ladder spec quantizes probabilities (freq = floor(p·2^20)).
- **What it means for seeds and compression:** The receiver must rebuild an identical greenhouse on any machine. With a neural greenhouse, tiny float differences across CPUs or threads can desync an arithmetic decoder and kill the seed by accident.

### Dead seed if intercepted
- **The owner's words:** ensure the 2 devices both have the grow instructions so they only send seeds and any interception will yield a dead seed (L2917)
- **What it is in the project:** The reply: compress, then encrypt with standard methods and pad the length; Kerckhoffs's principle.
- **What it means for seeds and compression:** A seed is meaningless without its greenhouse, but the greenhouse is not a secret key. Security has to come from real encryption on top.

### A child that grows and learns to grow food
- **The owner's words:** Its like watching a child grow and nurturing it while it learns to grow food (L3129)
- **What it is in the project:** The trained tiny model used as a generator/decoder.
- **What it means for seeds and compression:** Decoding is generation steered by the seed. A model normally writes by tossing weighted coins; feed it the seed's bits instead and it writes the exact message. The predictor nurtured in this chat becomes the grower.

### Grain of rice to a farm; solar calculator
- **The owner's words:** we can take a seed the size of a grain of rice and grow into a farm that could feed  the earth we just need a simple set of grow instructions (L2879); Essentially a calculator running on solar power (L2928)
- **What it is in the project:** seed_test.py: standard library only, runs on any old laptop. The energy caveat in the reply.
- **What it means for seeds and compression:** A tiny seed grows a huge output only when the rules, not the seed, hold the knowledge. Grow compute costs energy, so the saving is real where sending data is expensive.

### The blind person and color (understanding through relations)
- **The owner's words:** can still be done by the blind but in a different way (L103)
- **What it is in the project:** Experiment 1: a PPMI+SVD word model matched colors 10/14 from text alone.
- **What it means for seeds and compression:** Relations between words are predictive structure, and predictive structure is exactly what a greenhouse stores and what shrinks the seed.


## Candidates for the final piece (strongest first)


### [strong] The coin toss is the unit. Each 0/1 point on the 'page of binary' is a coin toss. The greenhouse (the tiny model trained in this chat) tilts each toss toward what really comes next, and the seed only records the surprises. This is arithmetic coding, and the seed size equals the model's loss, so understanding (lower loss) and compression (smaller exact seed) are literally one number.
- **Evidence:** "shift the \"coin toss\" towards the desired outcome" (L334, Oct 17). "The graph existing plot points if only \"0\" or\"1\" stacked from the work of solving an expression generates a page of binary rapidly and it doesn't change. The correct method is key." (L2963). "just needs a few numbers and symbols to added and subtracted and multipled to different points and restarted or worked backwards" (L2928). "can I grow understanding and compression?" (L3129). From the README (exp 6): the model "narrows each next word to about 1 in 32 out of 8,658" (held-out loss 3.46).
- **Why it could be the final piece:** It joins all three parts. The seed is the bitstream. The grow instructions are the fixed coder plus the shared model. Understanding is the loss. Every verb the owner used matches a range-coder step: multiply the range by the probability, add an offset, subtract, renormalize (restart), decode (work backwards). It was already in the chat on day 1: 3.46 nats is about 5.0 bits/word, against 13.1 bits/word for a bare word list.
- **How to test it:** The ladder experiment: an exact integer range coder over the saved models, with byte-for-byte decoding of the held-out verses, checking that seed bits ≈ Σ -log2 p within a few bytes. The logged loss predicts about 11.7 KB for the 83.8 KB held-out text (about 86% smaller), against xz 26.4 KB and zlib 28.6 KB. Random bytes must still give about 0%. Pre-register the prediction.

### [strong] Library call numbers ('strawberry and orange versus cucumber'). Items already on the shared shelf cost only their call number; the odd one out is spelled out. The Bible has the oldest such system (book:chapter:verse). This explains the owner's reported 98.9% / 100% results and the 'huge files' flaw: the library is the huge file.
- **Evidence:** "library style factors called strawberry and orange verse cucumber" (L2963). "100% reconstruction accuracy and 98.9% data reduction" and "It required huge files" (L2928). "Some already known like plants need water  and sunlight for example" (L2879). Measured here: with the KJV shelved, naming one verse takes log2(31,102) = 14.9 bits ≈ 1.9 bytes, against 132.5 bytes on average, which is 98.6% smaller and exact. The 623 held-out verses (80,798 bytes) shrink to about 1,162 bytes (98.56%).
- **Why it could be the final piece:** It reproduces the owner's own number almost exactly, with 100% exact regrowth. It is the likely mechanism behind successful tests in other AI chats, where the AI or its context already holds the text. It also marks the boundary: pointer seeds work only for data already in the library, while understanding seeds (candidate 1) work on unseen data. The complete greenhouse is a hybrid: copy from the shelf when the item is there, predict when it isn't, and spell out the cucumber.
- **How to test it:** Add a 'library pointer' method to seed_test.py with the KJV as the shared library, and count the library once as grow instructions. Report seed bytes for (a) held-out KJV verses (expect about 98.6%), (b) a novel paragraph and random bytes (expect about 0% or worse), and (c) a hybrid: pointer if found, model-coded if not, escape for the rest.

### [strong] The greenhouse is the shared context grown in this conversation: a codebook for the owner's language. It lets very short messages carry exact meaning. This is compression of communication, the owner's actual objective.
- **Evidence:** "Slowly I gave you more in depth instructions as you built" (L3129). "build a further understanding a d comprehension within our communication" (L753). "actual deconstruction of the knowledge sent as a tiny seed of information and the grow instruction so it can be grown back to this state exactly" (L2879). Late messages are tiny but carry big instructions: "Use a graph system lol" (L2947), "Run it. Your close" (L3003).
- **Why it could be the final piece:** It is the human-scale version of the seed: COMMUNICATION_GUIDE.md maps short owner phrases ('remaining', 'coin toss', '±17', 'seed and grow') to full mechanisms. NEXT_SESSION_PROMPT.md and the technical report are literal seeds that regrow a working session from the repo greenhouse. Better understanding means fewer words are needed to land an exact meaning.
- **How to test it:** The owner-explanation test (PLAN 1b): give a fresh model the owner's real short explanations ([w1=17 -<next word (-13)> = +4 Remaining], 'page of binary', 'strawberry vs cucumber') with vs without the guide, and score mechanism mapping against a pre-registered key. Also count how many words are needed before the restatement is correct. Optionally, measure the bits of the owner's next message under a model given the guide vs not.

### [medium] The shifting word as free side information, with marker surprisal as a gauge of understanding. The marker is computed only from earlier text, so the grower can recompute it at zero seed cost. Whatever it saves on the following words is pure gain, and the bits a model spends predicting its own marker show whether it has learned the carried state.
- **Evidence:** "the idea is the word shifts interpretation and the token used to interpret it based a Remaining value from the previous use of it" (L334). "shift the \"coin toss\" towards the desired outcome" (L334). Verified in code: shifting_word.mark_up() calls emerge() before read(), and method_comparison.mark_label() uses only the verse before.
- **Why it could be the final piece:** It turns the owner's own invention into a compression lever without changing the coder. It also gives a no-retraining diagnosis of 'carries perfectly but updates poorly': compare marker surprisal right after resets with surprisal on carried verses.
- **How to test it:** Ladder R7: (a) total bits vs (b) words-only bits, paired verse by verse against the baseline. Add per-position marker surprisal at reset vs carry points. Caveats to fix first: word_values() and the 3% clear cut-offs (and the label quantile edges) are computed from ALL verses, including held-out ones, so recompute them from training verses only. The receiver must also hold the preceding training verses, because the marker of held-out verse i depends on verse i-1. Prior art: hand-built context models in context-mixing compressors, and memory tokens. Credit would only come from a measured drop in bits on unseen text.

### [medium] 'Remaining' = the Excess Bank: keep the leftover and never throw it away. The owner's exact rule (W1 = 17 + 4, re-add at each emergence) was never tested. The AI switched it off (RECHARGE=False) and clips the balance at ±51, which discards the excess the way modulo does.
- **Evidence:** "[w1=17 -<Next word following it equal to (-13)> = +4 Remaining]" and "[W1=17+4 -<next 2 words following equaling (00)>= 0 Remaining]" (L334). The uploaded EBEC notes (technical, paraphrased) use a subtraction rule instead of modulo, with an 'excess bank' holding what modulo would discard.
- **Why it could be the final piece:** It is the same principle that makes arithmetic coding exact: the leftover range carries forward into the next step. The owner stated it twice, in two different projects (shifting word and EBEC), and the built system deviates from it at exactly that point.
- **How to test it:** New code under new model names, without editing the shared settings: RECHARGE on, plus an excess bank. The spelling comes from the capped part, and the overflow is banked and released as SPEND drains it. Compare held-out bits (ladder) and long-story judging against the current shifting word and the plain label. Pre-register.

### [medium] The seed expression is a mirror image, and 'worked backwards' is built into it. Reverse the left half of [+2×y(27/5.2+t=y/?)÷(?\y=t+2.5\72)yx2] and mirror each glyph (/→\, (→), ×→x) and you get the right half exactly; only the leading + has no partner. 27↔72, 5.2↔2.5, t=y↔y=t, +2×y↔yx2. This was never noticed in the chat.
- **Evidence:** The seed (L2879). "its not tge answer you're looking for but instead its the \"show your work\"" (L2879). "restarted or worked backwards" (L2928).
- **Why it could be the final piece:** The seed encodes 'grow = plant run in reverse'. Forward ÷ mirrored equals 1 exactly when the round trip is lossless. It is also its own demonstration: 18 of its 37 characters plus the rule 'mirror it' regrow the whole, about 50% smaller.
- **How to test it:** (1) The string check is done (Python): exact apart from the leading '+'. (2) In the arithmetic coder, write decode as the step-for-step mirror of encode and require SHA-256 equality on every test file; that equality is the '÷ = 1'. The mirror fact is certain; the interpretation is a hypothesis.

### [medium] The child that learns to grow food: decoding is generation steered by the seed. A language model writes by tossing weighted coins. Feed it the seed's bits instead of random coins and it writes the exact message.
- **Evidence:** "Its like watching a child grow and nurturing it while it learns to grow food" (L3129). "Its actually so simply children could technically do it but it would take for ever" (L2928). The coin toss (L334).
- **Why it could be the final piece:** It explains in one story why the same trained model is both the understanding (predictor) and the grower (generator). The model nurtured in this chat is that child.
- **How to test it:** Run the tiny model as an arithmetic decoder twice: with random bits (it grows new Bible-like text, the 'food') and with the encoded seed (it regrows the held-out verse exactly). Show both side by side. This is a known technique, so its value is as an explanation, not as credit.

### [medium] The palm seed in Antarctica: the greenhouse must regrow identically on any machine. Integer-only, quantized probabilities and pinned versions are part of the grow instructions.
- **Evidence:** "The part that differs is grow instructions" ... "I must still follow given instructions" ... "What do you think happens between differing os and data transfer?" (L3105).
- **Why it could be the final piece:** It is the practical piece that makes a neural greenhouse usable. A one-unit floating-point difference across CPUs, thread counts or torch versions can flip one arithmetic-decoding step and kill the seed.
- **How to test it:** Encode with torch using 4 threads, decode with 1 thread in a fresh process, and check exactness. If it fails, quantize logits or probabilities more coarsely, or use the float-free n-gram rungs. Record the versions in the seed header.

### [medium] Human error is the residual. What a predictive seed carries is the deviation from what the greenhouse expected, and that same deviation is what trains the greenhouse ('the calibration point'). Spelling variants and typos are cheap when they are predicted.
- **Evidence:** Pasted code (L2): "Maps human deviation (sins, mistakes, burdens) into calculable vectors", with the attribute "resonance_shift": "static_compression" for a carried burden. Pasted text the owner shared: "A mistake is not a defeat; it is the calibration point" (L79/L89). "The things  we do wrong naturally and have to be told not to do them is something ai must mimic" (L103). "to", "too", "two" ... "2" (L334).
- **Why it could be the final piece:** It closes the circle from the first message of the chat to the last: error is both the learning signal (understanding) and the payload (compression). The owner's earlier uploaded notes describe a 'human error encoding' compression method.
- **How to test it:** Inject controlled typos or spelling variants into held-out text. Compare bits for raw coding vs a model coding 'expected word + small edit'. On the ladder, confirm that training loss and seed size track each other across models.

### [weak] Syllable rotation ↔ the Burrows-Wheeler transform: sort all rotations like books on a library shelf, then invert exactly by walking backwards.
- **Evidence:** "syllables rotation sequence rather than a logical one" (L334); "library style factors" (L2963); "worked backwards" (L2928).
- **Why it could be the final piece:** It is a known exact seed-and-grow transform (1994, used in bzip2) whose parts match three of the owner's words: rotation, library ordering, and backwards regrowth.
- **How to test it:** Add bz2 as a method or rung in seed_test.py and the ladder, and compare it with zlib, xz and the model-based coder on the same files.

### [weak] The owner's numbers as cycle parameters. 17 and 47 are coprime to 16 and 32, so stepping by 17 or 47 around a 32-slot page visits every slot before repeating. 34 covers only 16 slots, and 16 and 32 don't rotate at all. Also 17 = 16+1 and 34 = 32+2.
- **Evidence:** "Note:17,32,16,34,47 are numbers my subconscious mind has focused on for years , they may just be random noise or maybe useful i dont know" (L334). Coincidences worth noting but not trusting: the tiny model's perplexity is about 31.8 ('1 in 32'), and a bare word list costs about 13.08 bits/word (the '-13').
- **Why it could be the final piece:** It would give the numbers a mechanical role in a page generator or hash. The owner's EBEC notes use +17 as a collision shift, and graph_locate.py already uses 17/32/16/34/47 as page parameters.
- **How to test it:** Run the PLAN step-1 settings (RESET 32/16/34/47, or SPEND ratios such as 17/34 and 16/32) under new model names. For the page generators, compare period and coverage with steps of 17 or 47 vs other coprime steps. Expect no advantage beyond coprimality.


## Every number and rule the owner gave, and where it was used

THE SHIFTING WORD (L334, Oct 17 23:00 UTC):
- Rule 1: "[w1=17 -<Next word following it equal to (-13)> = +4 Remaining]".
- Rule 2: "[W1=17+4 -<next 2 words following equaling (00)>= 0 Remaining]". The "(00)" was never explained; one reading is two 0/1 points.
- Continuation: "{w1=17-<next......>".
- Resets: "reset to [w1=0] when a clear right or wrong choice exists"; wrong starts at (-17), right at (+17).
- Spellings: "to", "too", "two", and "2" for computing.
- Rotation: "a syllables rotation sequence rather than a logical one".
- Purpose: "shift the \"coin toss\" towards the desired outcome".
- Numbers: "17,32,16,34,47 are numbers my subconscious mind has focused on for years".

Where the shifting word was used (experiments/shifting_word.py):
- RESET = 17; the cap is ±51 = 3×17.
- RECHARGE = False. The owner's "17+4" re-add was switched off by the AI and has never been tested; it is in PLAN step 1 and needs new model names.
- SPEND = 0.5 per valued word (an AI addition, so the balance fades). SCALE = 30. CLEAR_PCT = 3%.
- Clear verdicts come from the CLEAR_WRONG and CLEAR_RIGHT regexes. The balance resets to 0 at each book.
- Five spellings, rotations of sha-ru-vel-an-ok, with cut points at -12, -4, +4 and +12.
- 32, 16, 34 and 47 are untested. PLAN suggests trying them as RESET sizes or as SPEND ratios (17/34, 16/32).
- graph_locate.py (a draft) uses 17, 32, 16, 34, 47, 27 and 72 as placeholder page parameters.
- Related, from the owner's uploaded EBEC notes (technical only):
  - +17 prime shift for collisions;
  - H = Σ ord(c)·31^pos mod 46656 (36^3), base-36 3-character codes;
  - a subtraction rule instead of modulo, with an "Excess Bank";
  - "S = H × 26", a 4th-iteration correction trigger, a Levenshtein failsafe.
  - EBEC was rebuilt in TECHNICAL_REPORT_2026-10-20/2_Code/new_reference/ebec_reference.py and has not been run, at the owner's request.

THE SEED (L2879, Oct 20 08:35):
- "[+2×y(27/5.2+t=y/?)÷(?\y=t+2.5\72)yx2]", described as "the \"show your work\"" and "Seed=algebraic expression".
- Rule: "can be scaled exactly if stopping at points to pull out more algebraic expressions to solve the simple".
- Also: "a seed the size of a grain of rice and grow into a farm"; "plants need water  and sunlight".
- Where used:
  - it modelled the report's SEED block and its 10 grow steps with checkpoints;
  - graph_locate's page rule y ← (y×2×TIMES + 27t + 72 − MINUS) mod 2,147,483,647 echoes it;
  - graph_backwards' '?' unknowns come from it.
- New finding: it is a near-perfect mirror palindrome around ÷.

THE DATA SEED (L2917, L2928, L2947, L2958, L2963):
- Goals: "lower the amount of electricity"; "interception will yield a dead seed".
- Reported results: "100% reconstruction accuracy and 98.9% data reduction"; 99.8% "but it was flawed ... It required huge files".
- Method: "doesn't require an LLM ... numbers and symbols to added and subtracted and multipled to different points and restarted or worked backwards"; "a calculator running on solar power".
- Graph: "Use a graph system"; "plot points if only \"0\" or\"1\" stacked ... page of binary ... doesn't change. The correct method is key"; "library style factors called strawberry and orange verse cucumber".
- Where used:
  - SEED_TEST_2026-10-20/seed_test.py (fair harness: raw byte counts, SHA-256, a separate process in an empty folder, random-bytes case);
  - three draft readings in methods/: graph_fit, graph_locate, graph_backwards (Berlekamp-Massey, run backwards); all are placeholders until the owner shares the real factors.
- Benchmark: a pointer into the shared KJV gives 98.6% exact per verse (computed here).

PALM TREE (L3105): "The part that differs is grow instructions"; "I must still follow given instructions"; "differing os and data transfer". This led to the integer-only, raw-bytes, same-instructions-for-every-seed rule.

GREENHOUSE (L3129): soil, greenhouse, humidity, rotation of the sun, air, microbes and bugs, seed, then step-by-step instructions; "improve AI compression and understanding"; "grow more than a data seed".

STANDING RULES:
- "for A.I. not about people" (L96).
- Objective: "increase LLM ability to \"Comprehend\" and \"Understand\" in a way that improves communication" (L2428).
- "ensure that yiur drifting does not pass to the next llm" (L2428).
- "The moral aspect was merely training data that you drifted with" (L2670).
- "Any improvement is notable to me" (L944); "even if its .5% improvement" (L1088).
- "Separate the task being done in the chat i am sharing from the idea" (L79).
- "have faith and give it a try. If it doesn't work we will try something else" (L103).
- "I didn't say run tests? Did I?" (L2879): do only what is asked.
- Plain-language and copyable text (L2670).
- A .doc rebuild kit that regrows the project from a fresh chat (L2879).

NUMBERS COMPUTED HERE FOR CONTEXT:
- Held-out loss 3.46 nats ≈ 4.99 bits/word (perplexity 31.8); log2(8,658) = 13.08 bits/word.
- Held-out normalized text: 83,757 bytes / 18,674 tokens. zlib 28,565 B; xz 26,420 B. The model implies about 11.7 KB (estimate).

WORKING FILES: extraction scripts and outputs are in /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/final_piece_discovery/:
- owner.txt: all 34 owner messages in order;
- asst.txt: all assistant replies;
- extract2.py, extract_asst.py.

My first extract.py was written to the scratchpad root before I moved it, so it may have replaced an earlier extract.py of the parent's if one existed. No repo files were edited.


## Note added after the ladder finished
The dig was written before the ladder results came in. Since then:
- The tiny-model prediction it made from the logged loss (about 11.7 KB) was measured at 12.2 KB with a real coder, with exact regrowth.
- The shifting-word marker did NOT reduce the seed. That candidate ("free side information") was tested and did not pay off in this layout.
- The mirror fact about the seed expression was re-checked independently and is exact (apart from the leading '+').
