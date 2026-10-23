---
title: "Seed and Grow: Full Technical Report and Rebuild Kit"
subtitle: "LLM Comprehension and Communication Research, state as of 20 October 2026"
---

# How to use this document

This one file holds everything needed to rebuild the project from nothing:

- **The seed:** the whole project in one compact expression.
- **The grow instructions:** steps in order. Each ends with a checkpoint result, so you can confirm the rebuild matches before going on.
- **All the code, word for word** (Appendix A), plus every written record (Appendix B).

**To regrow it:** start a new chat with Claude (Claude Code is best, because it can run code), attach this file, and paste:

> Rebuild this project exactly from the attached Seed-and-Grow document. Recreate every file in Appendix A and Appendix B with exactly the paths and contents shown. Then follow the Grow Instructions in order, check each checkpoint, and stop and tell me if any result differs. Follow the Communication Rules in Section 4 in every reply.

**Online copy of everything:** <https://github.com/croblade47/utensil-theories-transfer-protocol/tree/ccr-1be0d913-1tlzao>

- **Experiments folder:** <https://github.com/croblade47/utensil-theories-transfer-protocol/tree/ccr-1be0d913-1tlzao/experiments>
- **Audit pack (other branch):** <https://github.com/croblade47/utensil-theories-transfer-protocol/tree/ccr-1be0d913-audit-pack>
- The repository is public (MIT license).

# 1. The Seed

The seed works the way the owner described: a short expression that is "the show your work". Applying the grow rules unfolds it, step by step, into the full project.

```
SEED =
  GOAL[ comprehension -> better communication ]
  x METHOD[ idea -> plain rules -> fair test( beat chance, control, rules saved first ) -> honest report ]
  x DATA[ KJV Bible + 12 public-domain story books + 3 novel sets, all fetched by URL ]
  x MODEL[ tiny GPT: 4 layers, width 192, 4 heads, window 64, 1500 steps, seeds {0,1,2} ]
  x MARKER[ b = 0 ; clear wrong -> b = -17 ; clear right -> b = +17 ;
            each valued word w -> b += v(w), then b moves 0.5 toward 0 ;
            b capped at +/-51 ; spelling = bucket(b) in {anoksha, oksharu, velanok, sharuvel, ruvelan}
            cut at -12, -4, +4, +12 ]
  = { Exp1 ... Exp11 results in Section 6 }
```

Plain words: the goal is better communication. The method is "turn every idea into a fair test." The data and model are small and fully reproducible. The marker is the owner's carried-balance idea, written into the text.

**Grow rules** (they apply at every step):
1. Restate the idea as plain numbered rules, and mark guesses.
2. Build the smallest version that can test it.
3. Write the pass/fail rules down and save them **before** running.
4. Compare against chance (a coin toss) and against a control that removes only the idea being tested.
5. Report the result in plain numbers ("6 more right per 100"), including failures.
6. If a flaw turns up after results are seen, keep the old result and label the new one "re-run after a fix."
7. Every result becomes the starting point (the next "seed") for the next question.

# 2. The Objective and Drift Guard

**Objective, in the owner's words:** *Increase an LLM's ability to "comprehend" and "understand" in a way that improves communication.*

- **Comprehension means one testable thing:** applying meaning to a new situation the model has never seen, not repeating memorized text.
- **The moral stories are practice material only.** The Bible, fables and right-or-wrong labels are training data and measuring sticks. They are not the goal.
- **Scale honesty:** results from tiny models do not change how a large AI like Claude understands anyone. Nothing has been tested yet on a large AI or in a real conversation.
- **Tone:** plain and calibrated. No hype, and no grand or mythic language.

# 3. Where the Project Stands Now (20 October 2026)

**Branch:** `ccr-1be0d913-1tlzao`. All experiment code is in `experiments/`; the first script is in `resonance/`.

**Confirmed or strong**
- **Meaning from word relationships alone works:** 10 of 14 color matches (chance about 2 or 3).
- **Marking the training text with a state word improves judging new situations:** about 69 right per 100 vs about 50 with no marking. This held in all 3 runs, but it was not yet pre-registered as the main test.

**Supported once, not yet confirmed**
- **The carried balance (the owner's "remaining" idea)** beat a plain per-sentence label when the act had scrolled out of view: about 59 vs 53 per 100 (p = 0.004).
  - It came from a re-run after two fixes.
  - About 65 of every 100 pairs were ties. On the rest it was right 81 times and wrong 25.

**Did not work**
- **Predicting consequences:** chance (51 per 100).
- **Transferring lessons from folk tales to Aesop's fables:** no training set beat chance.
- **Rules alone** were not "the secret": rules sharpened some judgments, and the stories carried the rest.

**Known weakness:** the carried marker **carries perfectly but updates poorly.** Once it writes a state, it tends to keep it.

**Next steps, in order**
1. **Conversation-carry test:** does a carried state help a model stay true to what a person said early in a long conversation? The owner approves its pass/fail rules first.
2. **Owner-explanation test:** does an AI map the owner's picture-and-math explanations to the right mechanism?
3. **Confirm the labeling gain** with pre-registered rules.
4. **A fresh long-story set at several distances** (1, 3, 5 and 8 neutral sentences).
5. **Balance carrying against updating.** First check whether greedy marker choice is hiding updates, then retrain with a stronger reset or a faster fade.
6. **Try the owner's rule "W1 = 17 + 4"** (RECHARGE) and the owner's numbers (32, 16, 34, 47) as reset sizes or ratios.
7. **A sub-word tokenizer test,** so the shared syllables of the spellings become visible to the model.
8. **A large AI as the reader:** needs an API key, which only the owner can add.

# 4. Communication Rules (how to work with the owner)

**How the owner explains**
- The owner explains with pictures, metaphors and rough math in brackets, for example `[w1=17 −<next word (−13)> = +4 Remaining]`.
- Read those as **rules for a mechanism**, not equations to check.
- Keep the image as a name. Never treat it as evidence.

**The working rules**
1. Restate before building. Mark guesses. Ask when a guess changes the result.
2. Every claim gets a chance level, a control, and pass/fail rules saved first.
3. Report failures as plainly as successes, with plain-number sizes.
4. No flattery and no mythic tone.
5. Credit: the ideas are the owner's; the code was built with an AI.
6. Cultural care: use only material published for sharing.
7. Write for a phone: outcome first, short, plain words.
8. Save and push every file. Deliver real Word files. Nothing locked.
9. Test an idea where it should matter before calling it useless.

**Glossary: the owner's words and what they mean**

| Owner's words | Meaning |
|---|---|
| "remaining" | A balance carried forward to the next step |
| "reset to ±17" | A clear right or wrong sets the balance |
| "coin toss" | Chance level |
| "to / too / two / 2" | Different spellings for different states |
| "dark forest" | Human reality, including mistakes |
| "Atlas" | Supportive stance |
| "seed and grow" | A compact expression, plus rules that unfold it exactly |

# 5. Grow Instructions (rebuild step by step, with checkpoints)

**Environment**
- Python 3.13, `pip install numpy scipy torch python-docx pypdf`, 4 CPU cores. No GPU needed.
- The results came from torch 2.14.1, numpy 2.5.3 and scipy 1.18.1. Exact seed reproduction needs the same versions.
- Data downloads automatically from these addresses:
  - KJV Bible: `https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/txt/KJV.txt`
  - World stories: GITenberg mirrors listed in `world_stories.py`
  - Novels: the NLTK Gutenberg zip, `https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/gutenberg.zip`

**Step 1. The first script.** Recreate `resonance/resonance_engine.py` and its tests.
- Run `python -m unittest` from `resonance/`.
- **Checkpoint:** 16 tests pass.
- What it does: a keyword detector for "weight" in text (regret, burden), with stances.

**Step 2. Experiments 1–4** (`experiments/bible_understanding.py`, a word-meaning model).
- **Checkpoint:**
  - color 10/14 = 71%;
  - judging right and wrong (moral) AUC 0.957 (word by word), 0.995 (whole verse), 0.948 (parallelism);
  - rules-only moral score 0.625 vs random verses 0.709;
  - 0 of 15 wrong acts flip without rules (theft unmeasurable, so really 0 of 14);
  - covet −0.077 → −0.043.

**Step 3. Experiment 5** (`consequences_test.py`, 20 story pairs, no training).
- **Checkpoint:** all methods at chance: association 45%, consequence map 48%.

**Step 4. Experiment 6** (`tiny_transformer.py --only full --seeds 0`).
- **Checkpoint:** consequences 9/20, picking the ending 22/40, judging 9/20. Held-out loss about 3.46.

**Step 5. Experiment 7** (`shifting_word.py --seed 0`, then `--seed 1`).
- **Checkpoint:** shifting word 14/20 and 13/20 on consequences; scrambled control 10/20 and 11/20.

**Step 6. Experiment 8** (`confirm.py`, 100 new pairs from `stories_v2.py`, 9 models).
- **Checkpoint, consequences:** shifting 50, 55, 55 → **not confirmed** (majority 51).
- **Checkpoint, judging:** shifting 67, 72, 67; scrambled 56, 42, 60; no marker 49, 60, 40.

**Step 7. Experiment 10** (`method_comparison.py`).
- **Checkpoint, judging:** plain label 71, 69, 63; three spellings 66, 72, 74.
- Q1 (shifting beats plain label) and Q2 (5 spellings beat 3): both ties.

**Step 8. Experiment 11** (`long_story_test.py`).
- **Checkpoint, version B (everyday act):** shifting 59, 56, 63 vs label 54.5, 51, 54. Pair by pair 43 better, 21 worse, p = 0.004.
- **Checkpoint, version A (explicit verdict):** label 73, 51, 97 vs shifting 45, 57, 62.5.

**Step 9. Experiment 9** (`world_stories.py`, then `aesop_test.py`, 16 models, about 6–8 hours).
- **Checkpoint:** stories 52.3, novels 54.1, shuffled 53.1, Bible 43.6, rules 50.0, narrative 56.5. P1, P2, P2b and P3 all **not confirmed**.

**Step 10. Records.** Recreate the records from Appendix B: HANDOFF, PLAN, COMMUNICATION_GUIDE, PRIOR_WORK, README and CLAUDE.md. You are now back at this point.

# 6. Results Table (everything measured so far)

| # | Test | Result | Status |
|---|---|---|---|
| 1 | Color from text only | 10/14 (chance 17%) | Worked |
| 2 | Three ways of splitting text | All similar; whole verse best for judging (0.995) | Descriptive |
| 3 | Rules as "the secret" | Rules-only 0.625 vs random 0.709 | Not supported |
| 4 | Remove the rules | 0 of 14 measurable acts flip; 6 weaker, 3 stronger | Mixed |
| 5 | Consequences (word model) | 45–52% | Chance |
| 6 | Consequences (tiny GPT) | 9/20 | Chance |
| 7 | Shifting word, 20 pairs | 68% vs 52% scrambled | Later shown to be luck |
| 8 | 100 new pairs | Consequences 51/100; judging 69 vs 50 | Consequences failed; judging strong |
| 9 | Aesop transfer | All at about chance | Not confirmed |
| 10 | vs plain label (short stories) | Tie (about 68–71) | Not confirmed |
| 11 | Long stories, everyday act | 59 vs 53 (p = 0.004) | Supported once |

# 7. How This Improves Systems

**Now** (works today with any AI chat; ideas from this work, not yet tested on large AIs)
1. **Keep a running state note** at the top of long chats: Goal, What my words mean, Decided, Still open, Changed. This is the "remaining" idea applied to conversation.
2. **Mark decisive moments** with "DECIDED:" or "REJECTED:". They reset the note, like the ±17 reset.
3. **Ordinary details adjust the note but don't overwrite it.** Items not mentioned for a while fade into "Still open".
4. **Have the AI explain back in plain numbered rules,** with guesses marked, before it does the work.
5. **Give one right example and one wrong example** when the AI misunderstands.
6. **Check understanding on a new case,** not a repeat.
7. **Ask for plain-number sizes** for every claimed improvement.
8. **Restart long chats with a handoff note,** like this document.

**After further research** (if the planned tests hold up)
- **Training text with carried state markers** could help models keep track of intent across long conversations, beyond what they can see at once.
- **A tuned balance between carrying and updating** could give AI assistants a reliable "memory of what matters".
- **A user-visible, correctable model of the person** (see Section 8) could make AI communication transparent and accurate.
- **A sub-word tokenizer** could test whether the shared syllables in spelling variants carry meaning.

# 8. Evaluation of the 11 Uploaded Sources (technical content only)

Some sources include private life details and named people. Those are left out on purpose, because this document and the repository are public. Only the technical content is evaluated.

**1. Gemini code report v1.1.** Useful structure, but it has errors:
- "73% vs 97%" were the *plain label's* runs; the shifting word scored 45, 57 and 62.5.
- "Validated" and "verified" overstate: the carry result is "supported once", and the labeling gain was not pre-registered.
- SPEND applies per *valued word*, not per token.
- Greedy marker choice is a suspected cause to check, not a fix.
- The trinary engine is not implemented anywhere in this repo.

**2. EBEC full reconstruction.**
- **The rolling hash, base-36 codes and dictionary** are standard dictionary coding. Sound engineering, but not new.
- **The 99.9% figure** compares a 3-byte token with a 3,072-byte *embedding*, which is a different thing. Normal AI token IDs are already 2–4 bytes. The fair comparison is against zip-style compressors on the same text, including the dictionary's size.
- **"Lossless"** holds only if the dictionary is kept and the typo failsafe is off. The failsafe changes words.
- **The "Excess Bank"** equals the quotient that modulo discards. Keeping it keeps all the information, but then the code is no longer 3 characters.
- **The CCG "syllable attractors" claim** needs a control: frequent syllables appear at the top of almost any mapping simply because they are frequent. Test it against a frequency-matched random formula, and across several languages.
- **The original V4 code was not supplied** (it was in screenshots). A reference version was rebuilt from the description: `2_Code/new_reference/ebec_reference.py`, in Appendix A. It is written but **not yet run**.
- **The reconstruction's own snippet:**

```python
def decompress_sentence(self, token_string):
    reverse_dict = {v: k for k, v in self.local_dict.items()}
    tokens = token_string.split()
    words = [reverse_dict.get(t, f"[{t}?]") for t in tokens]
    return " ".join(words)
```

**3. Echo Key data collection and transparency framework** (two Gemini Gem prompts)
- **Useful:** Gem 2, the transparency companion. Letting the person see, challenge and correct the AI's model of them directly serves the communication goal. It is the same idea as the state note.
- **Problem 1, consent:** Gem 1 logs people *silently* ("Do not reveal logging operations"). Collect data openly and with consent instead.
- **Problem 2, invented numbers:** a chat model cannot silently keep a JSON log between turns or truly compute "baseline deviation" scores. Asked for an audit, it will produce plausible-looking numbers it made up. Keep any real log visibly in the chat or in an external file.
- **The logging schema** it proposed:

```json
{ "turn_index": 0, "baseline_deviation_score": 0.0,
  "tone_variance_vector": {"warmth": 0.0, "directness": 0.0, "neutrality": 0.0},
  "active_archetype": "", "observed_defense_trigger": "" }
```

**4–5. Echo Key project tracker and project notebook** (the same content as a .md file and a PDF). Useful design principles:
- **"The Magic School Bus Rule":** content is the key, not the lesson. That is exactly the drift guard: the moral data was the key.
- **The trinary Yes / No / Maybe:** this matches the shifting word's middle "unresolved" state and the state note's "Still open".
- **The Mentor Paradox:** the AI guides; it doesn't do the work.
- **The Semantic Compass:** a distance between the current state and the goal state.
- Personal timeline details are omitted.

**6. Alara psychological-technical architecture**
- **Missing code:** it refers to JSON triggers, a SQL ALTER TABLE command and a base prompt, but none of them is in the file. They were in a Gemini Canvas that did not export, so they cannot be included.
- **Overclaim:** a text app cannot "manage the neuro-biological state" of a user.

**7. AI's Conceptual Mapping Upgrade** (Echoes of Alara v5, a React prototype)
- **It is a simulation:** the detected concept is hard-coded to `'trapped'`.
- **Bug, crashes:** `trapped`'s antonym `freedom` is missing from `CONCEPT_MAP`, so `endPoint` is undefined and the code crashes. `growth`, `connection` and `chaos` are missing too.
- **Misleading or unfinished interface:**
  - an "ENCRYPTED" label with no encryption;
  - crisis-help icons imported but no crisis handling;
  - the chat box isn't wired up;
  - the Big Five numbers are mock data.
- **Not real embeddings:** hand-placed 2-D points are not embeddings. Real embeddings have hundreds of learned dimensions.
- **Unsupported:** the "90% less database load" figure.
- **The fix for the crash:**

```javascript
// add the missing goal states so every antonym exists
'freedom':    { x: 70,  y: -90, cluster: 'Freedom',    antonym: 'trapped', color: 'text-cyan-300' },
'growth':     { x: 60,  y: -70, cluster: 'Growth',     antonym: 'fire',    color: 'text-lime-400' },
'connection': { x: -70, y: -60, cluster: 'Connection', antonym: 'void',    color: 'text-teal-400' },
'chaos':      { x: 75,  y: 75,  cluster: 'Chaos',      antonym: 'root',    color: 'text-rose-400' },
```

- **Core logic of the prototype** (excerpt, as written):

```javascript
const runVectorAnalysis = (file) => {
  setIsAnalyzing(true);
  setTimeout(() => {
    const detectedConcept = 'trapped';               // simulated
    const startPoint = CONCEPT_MAP[detectedConcept];
    const endPoint = CONCEPT_MAP[startPoint.antonym];
    const newVectorResult = {
      start: startPoint, end: endPoint,
      distance: Math.sqrt(Math.pow(endPoint.x - startPoint.x, 2) +
                          Math.pow(endPoint.y - startPoint.y, 2)).toFixed(0),
      theme: `From ${startPoint.cluster} to ${endPoint.cluster.toUpperCase()}`
    };
    setVectorData(newVectorResult); setIsAnalyzing(false);
  }, 2500);
};
```

**8. AI Helper Mini Booklets** (grocery, home tasks, gifts)
- **Good, plain prompt templates:** fill-in blanks, plus "if you can't find it, let me know."
- **Improvement:** add one line: "First repeat back what you understood in a short list, then answer."

**9. Adult Engine recalibrated for 18–35** (a PowerShell script)
- **Risky:** it deletes files with `-Force` and keeps no backup. Use version control (git) instead.
- **Broken:** `[cite: N]` markers pasted inside the code make it invalid.
- **Placeholder only:** the "sentiment engine" returns fixed values.
- **The drift the guide warns about:** its theatrical tone ("I hear the thunder in your voice").
- The script, as written:

```powershell
$ProjectRoot = "projects/echoes-of-alara"
$OldFiles = @("GRADES_3_5_FRAMEWORK.md", "grade-configs.ts")
foreach ($file in $OldFiles) {
  if (Test-Path "$ProjectRoot/docs/$file") { Remove-Item "$ProjectRoot/docs/$file" -Force } }
# writes src/core/AlaraPrimeEngine.ts whose analyzeAdultTheme() returns a fixed object:
# { theme: "Internal Conflict", shadowPotential: "Untapped Assertiveness",
#   somaticClue: "Coiled energy in the chest" }
```

**10–11. AI profiling logs** (Echo Key 1 and Echo Key 2)
- **Personal psychological profiles that name third parties.** None of their content is reproduced here.
- **Technical notes only:**
  - an AI-written profile is not a clinical assessment;
  - mapping other people's dynamics needs their consent;
  - these files must stay private and not be published.

# 9. Code Guide (what each file does and what it means)

**`resonance/resonance_engine.py`**
- **What it does:** finds weighted words with word-form matching and skips negated ones ("no guilt"). It combines scores (noisy-OR), picks a stance and produces a stable fingerprint of the text.
- **What it means:** the first, keyword-level attempt at "reading weight". Superseded by the experiments.

**`experiments/bible_understanding.py`**
- **What it does:** builds word meanings from co-occurrence (PPMI + SVD).
- **What it means:** tests 1–4. Understanding through relationships alone.

**`experiments/consequences_test.py`**
- **What it does:** holds the 20 test story pairs and a "this follows that" map.
- **What it means:** a word-averaging model can't understand an act made of several words.

**`experiments/tiny_transformer.py`**
- **What it does:** a small GPT trained from scratch (4 layers, window 64).
- **What it means:** the model that reads word order, used in every later test.

**`experiments/shifting_word.py`**
- **What it does:** the owner's carried balance, written into training text as an invented word with 5 spellings. It resets on clear verdicts, words nudge the balance, and it fades by 0.5 per valued word.
- **What it means:** the core idea of the project.

**`experiments/stories_v2.py`**
- **What it does:** holds 100 new right/wrong story pairs in KJV vocabulary.
- **What it means:** the fair confirmation set.

**`experiments/confirm.py`**
- **What it does:** trains and scores 9 models: shifting word, scrambled control, no marker.
- **What it means:** experiment 8.

**`experiments/method_comparison.py`**
- **What it does:** compares the plain per-verse label (the established method) and the 3-spelling carry.
- **What it means:** experiment 10. Labeling helps; the carry adds nothing on short stories.

**`experiments/long_story_test.py`**
- **What it does:** pads stories with neutral sentences until the act scrolls out of view. The model writes its own markers forward.
- **What it means:** experiment 11. Where the carry helped.

**`experiments/world_stories.py`**
- **What it does:** fetches 12 public-domain story books.
- **What it means:** the training library for the Aesop test.

**`experiments/aesop_test.py`**
- **What it does:** pairwise fable-to-moral matching, with controls for word clues and punctuation shortcuts, and permutation statistics.
- **What it means:** experiment 9. Stories vs novels vs shuffled stories.

**`2_Code/new_reference/ebec_reference.py`**
- **What it does:** a reference rebuild of EBEC V4 (rolling hash, base-36, +17 shift, Excess Bank, typo failsafe, decompress, outside-verify stub), with a stress test and benchmark functions.
- **What it means:** lets the EBEC claims be measured. Written, **not yet run**.

# Appendix A. All Code, Word for Word

Every file is shown with its exact path. Recreate each one exactly.
