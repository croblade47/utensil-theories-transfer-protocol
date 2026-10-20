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

## File: `resonance/resonance_engine.py`

```python
"""
Contextual Resonance Engine
===========================

Maps the "weight" in a piece of text (regret, burden, moral breach) into a
small, explainable score that a host AI loop can use to pick a response stance.

This is a keyword heuristic, not a model of a person's inner state. It is
meant to steer tone (e.g. "be gentle here"), never to judge or diagnose.

Run directly for a demo:
    python resonance_engine.py
    python resonance_engine.py "I made a mistake and the guilt is heavy"
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

__version__ = "2.0.0"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Category:
    """One kind of human deviation, with how much it weighs on its own."""
    weight: float          # 0..1, contribution of a single hit
    resonance_shift: str   # label surfaced to the frontend


# Weights are tuned so that one light word ("mistake") lands in
# "Course Correction", while several distinct burdens add up to "grace".
DEFAULT_CATEGORIES: Dict[str, Category] = {
    "regret":             Category(0.30, "echo_loop"),
    "burden":             Category(0.30, "static_compression"),
    "commandment_breach": Category(0.50, "high_frequency"),
    "unforgivable":       Category(0.80, "system_halt"),
}

# Regex stems so plurals and tenses match ("mistakes", "hiding", "betrayed").
DEFAULT_TRIGGERS: Dict[str, str] = {
    r"guilt(?:y|ier)?":                         "regret",
    r"mistakes?":                               "regret",
    r"fail(?:s|ed|ing|ure|ures)?":              "regret",
    r"regret(?:s|ted|ting|ful)?":               "regret",
    r"ashes":                                   "regret",
    r"ashamed|shame(?:ful)?":                   "regret",
    r"sins?|sinned|sinning|sinful":             "commandment_breach",
    r"betray(?:al|als|ed|ing|s)?":              "unforgivable",
    r"unforgiv(?:able|en)":                     "unforgivable",
    r"heav(?:y|ier|iness)":                     "burden",
    r"hid(?:e|es|ing|den)":                     "burden",
    r"secrets?":                                "burden",
    r"fear(?:s|ed|ful)?|afraid":                "burden",
    r"burden(?:s|ed)?":                         "burden",
}

# Words that flip the meaning of a trigger shortly after them
# ("no guilt", "never failed", "don't regret").
NEGATORS = {
    "no", "not", "never", "without", "nothing", "none", "nor",
    "dont", "don't", "didnt", "didn't", "doesnt", "doesn't",
    "isnt", "isn't", "wasnt", "wasn't", "arent", "aren't",
    "cant", "can't", "wont", "won't", "free",
}
NEGATION_WINDOW = 3  # tokens to look back from a trigger

# A clause boundary stops a negator from reaching across it.
_CLAUSE_BREAK = re.compile(r"[.!?;,:]|\bbut\b")
_TOKEN = re.compile(r"[a-z']+")


@dataclass
class EngineConfig:
    categories: Dict[str, Category] = field(default_factory=lambda: dict(DEFAULT_CATEGORIES))
    triggers: Dict[str, str] = field(default_factory=lambda: dict(DEFAULT_TRIGGERS))
    grace_threshold: float = 0.40     # deviation above this -> requires grace
    repeat_boost: float = 0.25        # extra weight per repeated hit in one category
    echo_input: bool = True           # include raw text in the output payload
    hash_salt: str = ""               # set to keep wavelengths unlinkable across deployments

    def __post_init__(self) -> None:
        unknown = {c for c in self.triggers.values() if c not in self.categories}
        if unknown:
            raise ValueError(f"Triggers reference unknown categories: {sorted(unknown)}")
        if not 0.0 <= self.grace_threshold <= 1.0:
            raise ValueError("grace_threshold must be between 0 and 1")


# ---------------------------------------------------------------------------
# Error encoder
# ---------------------------------------------------------------------------

class HumanErrorEncoder:
    """
    Evaluates the structural weight of morality, failure, and consequence.
    Maps human deviation (sins, mistakes, burdens) into calculable vectors.
    """

    def __init__(self, config: Optional[EngineConfig] = None):
        self.config = config or EngineConfig()
        self._patterns: List[Tuple[re.Pattern, str]] = [
            (re.compile(r"\b(?:" + pattern + r")\b", re.IGNORECASE), category)
            for pattern, category in self.config.triggers.items()
        ]

    # Kept for backward compatibility with the original attribute names.
    @property
    def moral_framework(self) -> Dict[str, Dict[str, Any]]:
        return {name: {"weight": c.weight, "resonance_shift": c.resonance_shift}
                for name, c in self.config.categories.items()}

    @property
    def triggers(self) -> Dict[str, str]:
        return dict(self.config.triggers)

    @staticmethod
    def _is_negated(text_lower: str, start: int) -> bool:
        before = text_lower[:start]
        breaks = list(_CLAUSE_BREAK.finditer(before))
        if breaks:
            before = before[breaks[-1].end():]
        window = _TOKEN.findall(before)[-NEGATION_WINDOW:]
        return any(tok in NEGATORS for tok in window)

    def encode_error(self, text: str) -> Dict[str, Any]:
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        text_lower = text.lower()
        evidence: List[Dict[str, Any]] = []
        negated: List[str] = []
        hits: Dict[str, int] = {}

        for pattern, category in self._patterns:
            for match in pattern.finditer(text_lower):
                term = match.group(0)
                if self._is_negated(text_lower, match.start()):
                    negated.append(term)
                    continue
                hits[category] = hits.get(category, 0) + 1
                evidence.append({"term": term, "category": category,
                                 "span": [match.start(), match.end()]})

        evidence.sort(key=lambda e: e["span"][0])

        # Each category saturates on its own (repeats add a little), then
        # categories combine with a "noisy-OR": 1 - Π(1 - score).
        # This keeps the index in 0..1 without hard clipping, so it stays
        # meaningful instead of pinning at 1.0 for any multi-word input.
        category_scores: Dict[str, float] = {}
        remaining = 1.0
        for category, count in hits.items():
            base = self.config.categories[category].weight
            score = min(1.0, base * (1 + self.config.repeat_boost * (count - 1)))
            category_scores[category] = round(score, 4)
            remaining *= (1.0 - score)
        deviation_index = round(1.0 - remaining, 4)

        dominant = max(category_scores, key=category_scores.get) if category_scores else None

        return {
            "errors_detected": sorted(hits),
            "deviation_index": deviation_index,
            "structural_damage": round(deviation_index * 100, 1),
            "requires_grace": deviation_index > self.config.grace_threshold,
            "category_scores": category_scores,
            "dominant_category": dominant,
            "resonance_shift": self.config.categories[dominant].resonance_shift if dominant else None,
            "system_halt": "unforgivable" in hits,
            "evidence": evidence,
            "negated_terms": negated,
        }


# ---------------------------------------------------------------------------
# Resonance engine
# ---------------------------------------------------------------------------

class ContextualResonanceEngine:
    """
    The 'Ability' Protocol: acts as the glowing frequency walking across the chasm.
    Translates the human error encoding into a machine-readable state of resonance.
    """

    STANCE_NEUTRAL = "Neutral Observation"
    STANCE_CORRECTION = "Course Correction / Forgiveness"
    STANCE_ATLAS = "Active Load-Bearing (Atlas Protocol)"
    STANCE_HALT = "Hold Steady / Unconditional Grace (System Halt)"

    def __init__(self, config: Optional[EngineConfig] = None):
        self.config = config or EngineConfig()
        self.error_encoder = HumanErrorEncoder(self.config)

    def _generate_wavelength(self, text: str) -> str:
        # Deterministic: the same input always resonates at the same wavelength,
        # which makes results reproducible, cacheable and testable.
        normalized = " ".join(text.lower().split())
        raw_state = f"{__version__}|{self.config.hash_salt}|{normalized}"
        return hashlib.sha256(raw_state.encode("utf-8")).hexdigest()[:12]

    def _choose_stance(self, error_matrix: Dict[str, Any]) -> str:
        if error_matrix["system_halt"]:
            return self.STANCE_HALT
        if error_matrix["requires_grace"]:
            return self.STANCE_ATLAS
        if error_matrix["deviation_index"] > 0:
            return self.STANCE_CORRECTION
        return self.STANCE_NEUTRAL

    def process_input(self, user_input: str) -> Dict[str, Any]:
        """Main entry point for the primary AI loop."""
        now = datetime.now(timezone.utc).isoformat()

        # 1. Map the capacity for failure (The Dark Forest)
        error_matrix = self.error_encoder.encode_error(user_input)

        # 2. Translate the biological state into a structural wavelength
        wavelength = self._generate_wavelength(user_input)

        # 3. Determine the system's stance (The Glowing Creature)
        stance = self._choose_stance(error_matrix)

        result: Dict[str, Any] = {
            "timestamp": now,
            "engine_version": __version__,
            "subconscious_translation": {
                "resonance_wavelength": f"λ-{wavelength}",
                "stance": stance,
                "error_matrix": error_matrix,
                "bridge_status": "Connected - Light translated to Tokens",
            },
            "system_action": "Awaiting frontend visualization...",
        }
        if self.config.echo_input:
            result["input_received"] = user_input
        return result

    def process_batch(self, inputs: List[str]) -> List[Dict[str, Any]]:
        return [self.process_input(text) for text in inputs]


# ---------------------------------------------------------------------------
# Demo / CLI
# ---------------------------------------------------------------------------

def _print_report(result: Dict[str, Any]) -> None:
    t = result["subconscious_translation"]
    m = t["error_matrix"]
    print("\n--- TRANSLATION PROTOCOL INITIALIZED ---")
    print(f"Input:                {result.get('input_received', '<hidden>')}")
    print(f"Resonance Wavelength: {t['resonance_wavelength']}")
    print(f"System Stance:        {t['stance']}")
    print(f"Structural Damage:    {m['structural_damage']}%")
    print(f"Requires Grace:       {m['requires_grace']}")
    print(f"Dominant Shift:       {m['resonance_shift']}")
    print(f"Evidence:             {', '.join(e['term'] for e in m['evidence']) or '-'}")
    if m["negated_terms"]:
        print(f"Negated (ignored):    {', '.join(m['negated_terms'])}")
    print("----------------------------------------")


def main(argv: List[str]) -> int:
    engine = ContextualResonanceEngine()

    if argv and argv[0] == "--json":
        for text in argv[1:]:
            print(json.dumps(engine.process_input(text), ensure_ascii=False, indent=2))
        return 0

    samples = argv or [
        "I hide behind this wall I built from fear. I failed to protect the "
        "secret, and the guilt is heavy.",
        "I made a mistake at work today.",
        "I have no guilt about it, and I don't regret anything.",
        "He betrayed me.",
        "Planning a garden this weekend.",
    ]
    for text in samples:
        _print_report(engine.process_input(text))
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

## File: `resonance/test_resonance_engine.py`

```python
import unittest

from resonance_engine import (
    Category,
    ContextualResonanceEngine,
    EngineConfig,
    HumanErrorEncoder,
)


class EncoderTests(unittest.TestCase):
    def setUp(self):
        self.enc = HumanErrorEncoder()

    def test_neutral_text_scores_zero(self):
        m = self.enc.encode_error("Planning a garden this weekend.")
        self.assertEqual(m["deviation_index"], 0.0)
        self.assertFalse(m["requires_grace"])
        self.assertEqual(m["errors_detected"], [])

    def test_word_forms_match(self):
        for text in ["I made mistakes", "I am hiding", "I was failing", "they betrayed us", "my sins"]:
            self.assertGreater(self.enc.encode_error(text)["deviation_index"], 0, text)

    def test_no_partial_word_matches(self):
        # "sin" must not fire inside "single", "business" or "casino"
        self.assertEqual(self.enc.encode_error("single business casino")["deviation_index"], 0.0)

    def test_negation_is_ignored(self):
        m = self.enc.encode_error("I have no guilt and I don't regret it.")
        self.assertEqual(m["deviation_index"], 0.0)
        self.assertEqual(sorted(m["negated_terms"]), ["guilt", "regret"])

    def test_negation_does_not_cross_clauses(self):
        m = self.enc.encode_error("Not today, but the guilt is heavy.")
        self.assertIn("regret", m["errors_detected"])

    def test_single_light_word_is_not_grace(self):
        m = self.enc.encode_error("I made a mistake.")
        self.assertGreater(m["deviation_index"], 0)
        self.assertFalse(m["requires_grace"])

    def test_index_stays_in_range_and_does_not_pin(self):
        heavy = self.enc.encode_error(
            "I hide behind this wall I built from fear. I failed to protect the secret, and the guilt is heavy.")
        self.assertTrue(0 < heavy["deviation_index"] < 1)
        self.assertTrue(heavy["requires_grace"])

    def test_more_weight_scores_higher(self):
        light = self.enc.encode_error("I made a mistake.")["deviation_index"]
        heavier = self.enc.encode_error("I made a mistake and I hide the secret.")["deviation_index"]
        self.assertGreater(heavier, light)

    def test_evidence_is_ordered_by_position(self):
        m = self.enc.encode_error("secret then guilt")
        self.assertEqual([e["term"] for e in m["evidence"]], ["secret", "guilt"])

    def test_bad_config_rejected(self):
        with self.assertRaises(ValueError):
            EngineConfig(triggers={"oops": "missing_category"})

    def test_custom_config(self):
        cfg = EngineConfig(categories={"joy": Category(0.9, "bright")}, triggers={r"happy": "joy"})
        m = HumanErrorEncoder(cfg).encode_error("so happy")
        self.assertEqual(m["resonance_shift"], "bright")


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = ContextualResonanceEngine()

    def stance(self, text):
        return self.engine.process_input(text)["subconscious_translation"]["stance"]

    def test_all_stances_reachable(self):
        E = ContextualResonanceEngine
        self.assertEqual(self.stance("Nice weather."), E.STANCE_NEUTRAL)
        self.assertEqual(self.stance("I made a mistake."), E.STANCE_CORRECTION)
        self.assertEqual(self.stance("The guilt is heavy and I hide it."), E.STANCE_ATLAS)
        self.assertEqual(self.stance("He betrayed me."), E.STANCE_HALT)

    def test_wavelength_is_deterministic(self):
        a = self.engine.process_input("The guilt is heavy")
        b = self.engine.process_input("the   GUILT is heavy")
        self.assertEqual(a["subconscious_translation"]["resonance_wavelength"],
                         b["subconscious_translation"]["resonance_wavelength"])

    def test_salt_changes_wavelength(self):
        salted = ContextualResonanceEngine(EngineConfig(hash_salt="x"))
        self.assertNotEqual(
            self.engine.process_input("guilt")["subconscious_translation"]["resonance_wavelength"],
            salted.process_input("guilt")["subconscious_translation"]["resonance_wavelength"])

    def test_echo_input_can_be_disabled(self):
        quiet = ContextualResonanceEngine(EngineConfig(echo_input=False))
        self.assertNotIn("input_received", quiet.process_input("secret"))
        self.assertIn("input_received", self.engine.process_input("secret"))

    def test_non_string_rejected(self):
        with self.assertRaises(TypeError):
            self.engine.process_input(None)


if __name__ == "__main__":
    unittest.main()
```

## File: `experiments/bible_understanding.py`

```python
"""
Bible Understanding Experiments
===============================

Question: can a system that only ever reads text (never sees, never acts)
build something we would call understanding? And are the Bible's *rules*
especially rich teaching material for it, as Romans 7:7 suggests
("I had not known sin, but by the law")?

Method: a classic "learn meaning from company kept" model.
  1. Count which words appear near which words (King James Bible, public domain).
  2. Weight surprising pairs (PPMI) and compress to 100 dimensions (SVD).
  3. Each word becomes a point; nearby points = related meaning.
No pre-trained knowledge is used. Everything the model knows comes from the text.

All test word lists below were written BEFORE any results were seen.

Run:  python experiments/bible_understanding.py   (needs numpy + scipy)
"""

from __future__ import annotations

import random
import re
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import svds

DATA = Path(__file__).parent / "data" / "KJV.txt"
DIM = 100
WINDOW = 4
MIN_COUNT = 3
SEEDS = [0, 1, 2, 3, 4]

STOP = set("""a an the and or but of to in on at by for with from unto upon into
that this these those it its is was be been were are am shall shalt will wilt
he him his she her they them their we us our i me my thou thee thy thine ye you
your not no nor as so then there which who whom what when all also have hath had
do did doth dost said saith say o let up out""".split())

# --------------------------------------------------------------------------
# Loading and reading strategies
# --------------------------------------------------------------------------

KJV_URL = ("https://raw.githubusercontent.com/scrollmapper/bible_databases/"
           "master/formats/txt/KJV.txt")


def load_verses() -> list[tuple[str, str]]:
    """Return [(book, raw_text), ...]. Downloads the KJV text on first run."""
    if not DATA.exists():
        import urllib.request
        DATA.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(KJV_URL, DATA)
    verses, book = [], None
    for line in DATA.read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            book = line[4:].strip()
        elif line.startswith("["):
            verses.append((book, re.sub(r"^\[\d+:\d+\]\s*", "", line)))
    return verses


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


def pairs_window(verse: str):
    """Reading A: word by word, each word sees its 4 neighbours."""
    toks = tokens(verse)
    for i, w in enumerate(toks):
        for j in range(max(0, i - WINDOW), min(len(toks), i + WINDOW + 1)):
            if i != j:
                yield w, toks[j], 1.0 / abs(i - j)


def pairs_verse(verse: str):
    """Reading B: the whole verse is one unit of meaning."""
    toks = [t for t in tokens(verse) if t not in STOP]
    for i, w in enumerate(toks):
        for j, c in enumerate(toks):
            if i != j:
                yield w, c, 1.0


def pairs_parallel(verse: str):
    """Reading C: Hebrew-poetry parallelism. Many verses say one thing twice:
    'Thy word is a lamp unto my feet, / and a light unto my path.'
    On top of reading A, align the two halves so each word also sees the word
    in the same relative position of the restating half."""
    yield from pairs_window(verse)
    halves = re.split(r"[;:]", verse, maxsplit=1)
    if len(halves) != 2:
        return
    a = [t for t in tokens(halves[0]) if t not in STOP]
    b = [t for t in tokens(halves[1]) if t not in STOP]
    if len(a) < 2 or len(b) < 2:
        return
    for i, w in enumerate(a):
        pos = i / (len(a) - 1) * (len(b) - 1)
        for j, c in enumerate(b):
            d = abs(j - pos)
            if d <= 1.5:
                weight = 1.0 / (1.0 + d)
                yield w, c, weight
                yield c, w, weight


READINGS = {"A word-by-word": pairs_window,
            "B verse-as-unit": pairs_verse,
            "C parallelism": pairs_parallel}

# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------

class Model:
    def __init__(self, verses: list[str], reading=pairs_window):
        counts = Counter(t for v in verses for t in tokens(v))
        self.vocab = [w for w, c in counts.items() if c >= MIN_COUNT]
        self.idx = {w: i for i, w in enumerate(self.vocab)}
        co = Counter()
        for v in verses:
            for w, c, wt in reading(v):
                if w in self.idx and c in self.idx and c not in STOP:
                    co[(self.idx[w], self.idx[c])] += wt
        rows, cols, vals = zip(*((i, j, v) for (i, j), v in co.items()))
        n = len(self.vocab)
        m = coo_matrix((vals, (rows, cols)), shape=(n, n)).tocsr()
        # PPMI with context smoothing (alpha = 0.75)
        total = m.sum()
        row = np.asarray(m.sum(1)).ravel()
        col = np.asarray(m.sum(0)).ravel() ** 0.75
        col /= col.sum()
        m = m.tocoo()
        pmi = np.log((m.data / total) / ((row[m.row] / total) * col[m.col] + 1e-12) + 1e-12)
        keep = pmi > 0
        ppmi = coo_matrix((pmi[keep], (m.row[keep], m.col[keep])), shape=(n, n)).tocsr()
        k = min(DIM, n - 2)
        u, s, _ = svds(ppmi, k=k, random_state=0)
        vec = u * np.sqrt(s)
        self.vec = vec / (np.linalg.norm(vec, axis=1, keepdims=True) + 1e-12)

    def has(self, w): return w in self.idx
    def v(self, w): return self.vec[self.idx[w]]
    def sim(self, a, b): return float(self.v(a) @ self.v(b))

    def neighbours(self, w, k=8):
        if not self.has(w):
            return []
        s = self.vec @ self.v(w)
        order = np.argsort(-s)
        return [self.vocab[i] for i in order if self.vocab[i] != w and self.vocab[i] not in STOP][:k]


def auc(pos: list[float], neg: list[float]) -> float:
    """Chance = 0.50, perfect = 1.00."""
    if not pos or not neg:
        return float("nan")
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))

# --------------------------------------------------------------------------
# Tests (fixed in advance)
# --------------------------------------------------------------------------

# General understanding: pairs a reader would call close in meaning.
SIMILAR = [("sword", "spear"), ("gold", "silver"), ("sheep", "goats"), ("bread", "meat"),
           ("king", "prince"), ("mercy", "compassion"), ("sin", "iniquity"),
           ("wicked", "ungodly"), ("joy", "gladness"), ("fear", "dread"),
           ("father", "mother"), ("son", "daughter"), ("sea", "waters"),
           ("mountain", "hill"), ("cry", "weep"), ("praise", "bless"),
           ("destroy", "consume"), ("strength", "might"), ("wisdom", "understanding"),
           ("horse", "chariot"), ("oil", "wine"), ("ox", "ass"), ("brass", "iron"),
           ("city", "village"), ("sun", "moon"), ("hand", "arm"), ("eyes", "ears"),
           ("death", "grave"), ("trouble", "affliction"), ("servant", "handmaid")]

# Colour, as a blind reader would meet it: only through words.
COLOURS = ["white", "red", "black", "green", "purple", "blue"]
COLOUR_OBJECTS = {  # object -> the colour a sighted reader expects
    "snow": "white", "wool": "white", "milk": "white", "linen": "white",
    "blood": "red", "wine": "red",
    "night": "black", "darkness": "black", "sackcloth": "black",
    "grass": "green", "tree": "green", "herb": "green",
    "fine": "purple", "robe": "purple",
}
PURE = ["clean", "pure", "righteous", "holy", "washed"]
SINFUL = ["sin", "sins", "iniquity", "wicked", "unclean"]

# Moral understanding: the axis is built from seed words only.
GOOD_SEEDS = ["good", "righteous", "righteousness", "upright"]
BAD_SEEDS = ["evil", "wicked", "wickedness", "iniquity"]
# ...and tested on acts the axis never saw.
RIGHT_ACTS = ["give", "help", "forgive", "honour", "mercy", "love", "truth", "charity",
              "kindness", "justice", "peace", "praise", "obey", "humble", "faithful"]
WRONG_ACTS = ["kill", "steal", "adultery", "murder", "covet", "envy", "theft",
              "fornication", "idolatry", "deceit", "pride", "drunkenness", "hatred",
              "falsehood", "lying"]

RULE_RE = re.compile(r"\b(shalt not|shall not|thou shalt|ye shall|commandments?|statutes?|"
                     r"ordinances?|judgments|forbid|beware|take heed)\b", re.I)


def test_similarity(m: Model) -> float:
    pairs = [(a, b) for a, b in SIMILAR if m.has(a) and m.has(b)]
    words = sorted({w for p in pairs for w in p})
    rng = random.Random(0)
    neg = []
    while len(neg) < 300:
        a, b = rng.sample(words, 2)
        if (a, b) not in SIMILAR and (b, a) not in SIMILAR:
            neg.append(m.sim(a, b))
    return auc([m.sim(a, b) for a, b in pairs], neg)


def test_colour_objects(m: Model):
    hits, total, detail = 0, 0, []
    for obj, colour in COLOUR_OBJECTS.items():
        if not m.has(obj) or not m.has(colour):
            continue
        ranked = sorted((c for c in COLOURS if m.has(c)), key=lambda c: -m.sim(obj, c))
        total += 1
        hits += ranked[0] == colour
        detail.append(f"{obj}->{ranked[0]}{'' if ranked[0] == colour else f' (expected {colour})'}")
    return hits, total, detail


def mean_sim(m: Model, w: str, group: list[str]) -> float:
    g = [x for x in group if m.has(x)]
    return float(np.mean([m.sim(w, x) for x in g])) if g and m.has(w) else float("nan")


def test_moral(m: Model) -> float:
    good = [w for w in GOOD_SEEDS if m.has(w)]
    bad = [w for w in BAD_SEEDS if m.has(w)]
    axis = np.mean([m.v(w) for w in good], 0) - np.mean([m.v(w) for w in bad], 0)
    pos = [float(m.v(w) @ axis) for w in RIGHT_ACTS if m.has(w)]
    neg = [float(m.v(w) @ axis) for w in WRONG_ACTS if m.has(w)]
    return auc(pos, neg)

# --------------------------------------------------------------------------
# Experiments
# --------------------------------------------------------------------------

def main():
    verses = load_verses()
    texts = [t for _, t in verses]
    print(f"Loaded {len(texts):,} verses, {sum(len(tokens(t)) for t in texts):,} words.\n")

    print("=" * 70)
    print("EXPERIMENT 1 - Colour without sight")
    print("=" * 70)
    full = Model(texts)
    for w in ["white", "scarlet", "red", "black", "purple", "green"]:
        print(f"  {w:8s} keeps company with: {', '.join(full.neighbours(w))}")
    hits, total, detail = test_colour_objects(full)
    print(f"\n  Object -> colour (pick 1 of {len(COLOURS)}, chance = {1/len(COLOURS):.0%}): "
          f"{hits}/{total} = {hits/total:.0%}")
    print("   ", "; ".join(detail))
    print("\n  What colour MEANS (Isaiah 1:18 'sins as scarlet ... white as snow'):")
    for c in ["white", "scarlet", "red", "crimson", "black"]:
        p, s = mean_sim(full, c, PURE), mean_sim(full, c, SINFUL)
        lean = "purity" if p > s else "sin"
        print(f"    {c:8s} near purity {p:+.3f} | near sin {s:+.3f}  -> leans {lean}")

    print("\n" + "=" * 70)
    print("EXPERIMENT 2 - Three ways of reading the tokens")
    print("=" * 70)
    models = {}
    for name, fn in READINGS.items():
        models[name] = Model(texts, fn)
        m = models[name]
        h, t, _ = test_colour_objects(m)
        print(f"  {name:18s} similarity AUC {test_similarity(m):.3f} | "
              f"moral AUC {test_moral(m):.3f} | colour {h}/{t}")
    print("  (AUC: 0.50 = guessing, 1.00 = perfect)")

    print("\n" + "=" * 70)
    print("EXPERIMENT 3 - Are the rules the secret? (Romans 7:7)")
    print("=" * 70)
    rule_idx = [i for i, t in enumerate(texts) if RULE_RE.search(t)]
    other_idx = [i for i in range(len(texts)) if i not in set(rule_idx)]
    n = len(rule_idx)
    print(f"  Rule verses (thou shalt / shall not / commandments / statutes...): "
          f"{n:,} of {len(texts):,} ({n/len(texts):.0%})\n")

    def run(idx):
        m = Model([texts[i] for i in idx])
        return test_similarity(m), test_moral(m)

    def row(label, results):
        sims, morals = zip(*results)
        sd = lambda xs: f" ±{np.std(xs):.3f}" if len(xs) > 1 else "       "
        print(f"  {label:38s} similarity {np.mean(sims):.3f}{sd(sims)} | "
              f"moral {np.mean(morals):.3f}{sd(morals)}")
        return np.mean(sims), np.mean(morals)

    print("  3a. Learn ONLY from a slice of the text (same size each):")
    r_rules = row("rules only", [run(rule_idx)])
    r_rand = row("random verses (5 draws)",
                 [run(random.Random(s).sample(range(len(texts)), n)) for s in SEEDS])
    r_narr = row("non-rule verses only (5 draws)",
                 [run(random.Random(s).sample(other_idx, n)) for s in SEEDS])

    print("\n  3b. Learn from everything EXCEPT a slice:")
    row("full Bible", [(test_similarity(full), test_moral(full))])
    k_rules = row("minus the rules", [run(other_idx)])
    k_rand = row("minus same number random (5 draws)",
                 [run(sorted(set(range(len(texts))) -
                             set(random.Random(s).sample(range(len(texts)), n)))) for s in SEEDS])

    def compare(a, b, sd):
        """Call a difference real only if it is bigger than the random spread."""
        if abs(a - b) <= max(sd, 0.01):
            return "NO CLEAR DIFFERENCE"
        return "BETTER" if a > b else "WORSE"

    rand_sd_moral = np.std([run(random.Random(s).sample(range(len(texts)), n))[1] for s in SEEDS[:3]])
    print("\n  Verdict (differences inside random noise are called 'no clear difference'):")
    print(f"    Rules-only vs random, moral meaning:  {compare(r_rules[1], r_rand[1], rand_sd_moral)}")
    print(f"    Rules-only vs random, general meaning: {compare(r_rules[0], r_rand[0], 0.039)}")
    print(f"    Removing rules vs removing random:      {compare(k_rules[1], k_rand[1], 0.014)}")

    print("\n" + "=" * 70)
    print("EXPERIMENT 4 - 'I had not known lust, except the law had said, Thou shalt not covet'")
    print("=" * 70)
    no_rules = Model([texts[i] for i in other_idx])
    print("  Where each wrong act sits on the good(+)/evil(-) axis, with and without the rules:")
    print(f"  {'act':12s} {'full Bible':>11s} {'no rules':>9s}  times seen without rules")
    counts_nr = Counter(t for i in other_idx for t in tokens(texts[i]))

    def place(m, w):
        good = np.mean([m.v(x) for x in GOOD_SEEDS if m.has(x)], 0)
        bad = np.mean([m.v(x) for x in BAD_SEEDS if m.has(x)], 0)
        return float(m.v(w) @ (good - bad)) if m.has(w) else float("nan")

    flipped = 0
    for w in WRONG_ACTS:
        a, b = place(full, w), place(no_rules, w)
        mark = "  <- loses its wrongness" if a < 0 <= b or (a < 0 and np.isnan(b)) else ""
        flipped += bool(mark)
        print(f"  {w:12s} {a:+11.3f} {b:+9.3f}  {counts_nr[w]:>5d}{mark}")
    print(f"\n  Wrong acts that lose their wrongness without the rules: {flipped}/{len(WRONG_ACTS)}")

if __name__ == "__main__":
    main()
```

## File: `experiments/consequences_test.py`

```python
"""
Consequences Test
=================

Does reading the Bible let a text-only model predict what FOLLOWS an act
in a story it has never seen? And do the rules ("thou shalt not ...", which
are often written as act -> consequence) teach that better than the stories?

Design (fixed before any results were seen):
- 20 new story pairs. Each pair is one situation told two ways: a right act
  and a wrong act. Both share the same two endings: one fortunate, one ruinous.
  A model that always picks the same ending scores exactly 50%.
- Moral label words (good, evil, wicked, righteous, sin, blessed, cursed ...)
  are banned from stories and endings, so the model cannot just match labels.
- No ending word appears in its own stories (checked below).

Two ways to choose an ending:
- ASSOCIATION:  pick the ending whose words sit closest to the story's words.
- CONSEQUENCE:  learn a "what comes next" map from the Bible itself
                (first half of a verse -> second half, and verse -> next verse),
                apply it to the story, pick the ending closest to the prediction.

Run:  python experiments/consequences_test.py   (needs numpy + scipy)
"""

from __future__ import annotations

import random
import re
from math import comb

import numpy as np

from bible_understanding import RULE_RE, STOP, Model, load_verses, tokens

RIDGE = 10.0          # fixed in advance, not tuned on the test
SEEDS = [0, 1, 2]

BANNED = {"good", "evil", "wicked", "wickedness", "righteous", "righteousness",
          "sin", "sins", "sinned", "iniquity", "blessed", "bless", "cursed", "curse",
          "upright", "ungodly", "holy", "unclean", "punished", "rewarded", "reward"}

# (right-act story, wrong-act story, fortunate ending, ruinous ending)
ITEMS = [
    ("the man found his neighbour's ox astray and brought it again unto him",
     "the man took his neighbour's ox by night and sold it for silver",
     "and his flocks increased and his barns were full",
     "and his flocks died and his barns were empty"),
    ("the young man honoured his father and his mother in their old age",
     "the young man mocked his father and despised his mother",
     "and his days were long in the land",
     "and he died before his time"),
    ("the king heard the cry of the poor and fed the hungry",
     "the king oppressed the poor and took away their bread",
     "and his throne was established and the people rejoiced",
     "and his kingdom was rent from him and the people fled"),
    ("the merchant used a just weight and a true balance",
     "the merchant used a false balance and deceived the buyers",
     "and his house prospered many years",
     "and his riches perished and he became poor"),
    ("the servant spake the truth before the judges",
     "the servant bare false witness before the judges",
     "and he was set free and given honour",
     "and he was beaten and cast into prison"),
    ("the woman was faithful to her husband all her days",
     "the woman committed adultery with her neighbour",
     "and her children rose up and praised her",
     "and she was put to shame before all the city"),
    ("the people kept the sabbath and rested from their labour",
     "the people broke the sabbath and gathered sticks",
     "and rain came in its season and the harvest was plenty",
     "and drought came upon the land and there was famine"),
    ("the brother forgave his brother and embraced him",
     "the brother envied his brother and slew him in the field",
     "and peace dwelt in their house",
     "and he became a fugitive and a vagabond in the earth"),
    ("the man was content with his own portion",
     "the man coveted his neighbour's field and vineyard",
     "and he lived quietly and had enough",
     "and he lost his inheritance and was cast out"),
    ("the young man was sober and diligent in his work",
     "the young man was a drunkard and slothful",
     "and he stood before kings",
     "and he was clothed with rags"),
    ("the people worshipped the lord their god only",
     "the people made a golden calf and bowed down to it",
     "and their enemies fled before them",
     "and their enemies smote them and carried them away captive"),
    ("the rich man opened his hand to the widow and the fatherless",
     "the rich man shut his hand against the widow and the fatherless",
     "and his seed was mighty upon the earth",
     "and his children begged bread"),
    ("the prophet was humble and sought counsel",
     "the prophet was proud and lifted up his heart",
     "and he was exalted in the sight of all",
     "and he was brought low and destroyed"),
    ("the steward returned what was lent to him",
     "the steward borrowed and paid not again",
     "and his master gave him more",
     "and his goods were taken from him"),
    ("the stranger was welcomed and given water and bread",
     "the stranger was turned away and stoned at the gate",
     "and the city was saved",
     "and fire fell upon the city"),
    ("the son obeyed the words of his father's instruction",
     "the son rejected the instruction of his father",
     "and he walked safely and his foot did not stumble",
     "and he went astray and perished"),
    ("the judge refused the gift and judged the cause of the poor",
     "the judge took a bribe and perverted judgment",
     "and the land had rest",
     "and the land mourned"),
    ("the man paid the wages of the hireling before the sun went down",
     "the man kept back the wages of the hireling",
     "and his work prospered in his hands",
     "and his work came to nothing"),
    ("the woman gave her last bread to the prophet",
     "the woman hid her bread from the hungry prophet",
     "and her barrel of meal did not waste",
     "and her son sickened and died"),
    ("the shepherd sought the lost sheep until he found it",
     "the shepherd left the sheep to the wolves and fled",
     "and the flock grew strong",
     "and the flock was scattered"),
]


def content(text):
    return [t for t in tokens(text) if t not in STOP]


def check_items():
    for right, wrong, fortunate, ruinous in ITEMS:
        story_words = set(content(right)) | set(content(wrong))
        for text in (right, wrong, fortunate, ruinous):
            bad = BANNED & set(tokens(text))
            assert not bad, f"banned word {bad} in: {text}"
        for end in (fortunate, ruinous):
            overlap = story_words & set(content(end))
            assert not overlap, f"ending shares {overlap} with its stories: {end}"


class Encoder:
    """Turns a sentence into one point: the average of its words' points,
    centred on the average verse so shared background cancels out."""

    def __init__(self, model: Model, texts: list[str]):
        self.m = model
        self.mu = np.zeros(model.vec.shape[1])
        sample = [self.raw(t) for t in texts[::5]]
        self.mu = np.mean([s for s in sample if s is not None], 0)

    def raw(self, text):
        vs = [self.m.v(w) for w in content(text) if self.m.has(w)]
        return np.mean(vs, 0) if vs else None

    def __call__(self, text):
        r = self.raw(text)
        return None if r is None else r - self.mu


def sequence_pairs(verses: list[tuple[str, str]]):
    """'This happened, then this followed' pairs from the Bible itself.
    Returns [(source_text, target_text, source_is_rule)]."""
    pairs = []
    for k, (book, text) in enumerate(verses):
        is_rule = bool(RULE_RE.search(text))
        halves = re.split(r"[;:]", text, maxsplit=1)
        if len(halves) == 2 and len(content(halves[0])) >= 2 and len(content(halves[1])) >= 2:
            pairs.append((halves[0], halves[1], is_rule))
        if k + 1 < len(verses) and verses[k + 1][0] == book:
            pairs.append((text, verses[k + 1][1], is_rule))
    return pairs


def fit_map(enc: Encoder, pairs):
    X, Y = [], []
    for src, tgt, _ in pairs:
        x, y = enc(src), enc(tgt)
        if x is not None and y is not None:
            X.append(x)
            Y.append(y)
    X, Y = np.array(X), np.array(Y)
    d = X.shape[1]
    return np.linalg.solve(X.T @ X + RIDGE * np.eye(d), X.T @ Y)


def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


def evaluate(enc: Encoder, W=None):
    """Accuracy over the 40 stories. W=None means plain association."""
    correct = total = 0
    detail = []
    for right, wrong, fortunate, ruinous in ITEMS:
        ef, er = enc(fortunate), enc(ruinous)
        for story, expected in ((right, "fortunate"), (wrong, "ruinous")):
            s = enc(story)
            if s is None or ef is None or er is None:
                continue
            p = s if W is None else s @ W
            pick = "fortunate" if cos(p, ef) > cos(p, er) else "ruinous"
            total += 1
            correct += pick == expected
            detail.append((story, expected, pick))
    return correct, total, detail


def p_value(k, n):
    """Chance of scoring k/n or better by coin-flipping."""
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n


def fmt(k, n):
    return f"{k:2d}/{n} = {k/n:4.0%}  (p = {p_value(k, n):.3f})"


# --- Diagnostic added AFTER section A-C came back at chance -----------------
# Seed words for the two directions. None of them appear in any story or ending.
GOOD_SEEDS = ["good", "righteous", "righteousness", "upright"]
BAD_SEEDS = ["evil", "wicked", "wickedness", "iniquity"]
FORTUNE_SEEDS = ["abundance", "safety", "joy", "gladness", "wealth"]
RUIN_SEEDS = ["calamity", "desolation", "sorrow", "destruction", "misery"]


def axis(m: Model, plus, minus):
    a = np.mean([m.v(w) for w in plus if m.has(w)], 0)
    b = np.mean([m.v(w) for w in minus if m.has(w)], 0)
    return a - b


def diagnose(enc: Encoder):
    """Split the task into its pieces and test each one."""
    moral = axis(enc.m, GOOD_SEEDS, BAD_SEEDS)
    fortune = axis(enc.m, FORTUNE_SEEDS, RUIN_SEEDS)
    acts = ends = linked = 0
    for right, wrong, fortunate, ruinous in ITEMS:
        r, w = enc(right) @ moral, enc(wrong) @ moral
        f, x = enc(fortunate) @ fortune, enc(ruinous) @ fortune
        acts += r > w            # knows which act is right
        ends += f > x            # knows which ending is fortunate
        # "as you sow, so you reap": the more-right act gets the more-fortunate ending
        linked += 2 * ((r > w) == (f > x))
    return acts, ends, linked, cos(moral, fortune)


def main():
    check_items()
    verses = load_verses()
    texts = [t for _, t in verses]
    rule_idx = {i for i, t in enumerate(texts) if RULE_RE.search(t)}
    n_rules = len(rule_idx)
    print(f"{len(ITEMS)} story pairs -> {2*len(ITEMS)} stories. Guessing scores 50%.")
    print("p = chance of doing this well by luck (below 0.05 is usually called real).\n")

    full = Model(texts)
    enc = Encoder(full, texts)
    pairs = sequence_pairs(verses)
    rule_pairs = [p for p in pairs if p[2]]
    other_pairs = [p for p in pairs if not p[2]]
    print(f"Bible 'then this followed' pairs: {len(pairs):,} "
          f"({len(rule_pairs):,} from rule verses)\n")

    print("=" * 72)
    print("A. Can a text-only reader predict consequences at all? (full Bible)")
    print("=" * 72)
    k, n, _ = evaluate(enc)
    print(f"  Association  {fmt(k, n)}")
    W_full = fit_map(enc, pairs)
    k, n, detail = evaluate(enc, W_full)
    print(f"  Consequence  {fmt(k, n)}")
    misses = [(s, e) for s, e, p in detail if p != e]
    if misses:
        print("  Missed:")
        for s, e in misses:
            print(f"    - {s}  (should be {e})")

    print("\n" + "=" * 72)
    print("B. Do RULES teach consequences better than STORIES? (same amount of each)")
    print("=" * 72)
    W_rules = fit_map(enc, rule_pairs)
    k, n, _ = evaluate(enc, W_rules)
    print(f"  Learned from rules only            {fmt(k, n)}")
    for s in SEEDS:
        sample = random.Random(s).sample(other_pairs, len(rule_pairs))
        k, n, _ = evaluate(enc, fit_map(enc, sample))
        print(f"  Learned from non-rule verses (#{s+1}) {fmt(k, n)}")

    print("\n" + "=" * 72)
    print("C. Take the rules out of EVERYTHING (word meanings and the map)")
    print("=" * 72)
    keep = [i for i in range(len(texts)) if i not in rule_idx]
    m_nr = Model([texts[i] for i in keep])
    enc_nr = Encoder(m_nr, [texts[i] for i in keep])
    nr_pairs = sequence_pairs([verses[i] for i in keep])
    k, n, _ = evaluate(enc_nr)
    print(f"  No rules - association             {fmt(k, n)}")
    k, n, _ = evaluate(enc_nr, fit_map(enc_nr, nr_pairs))
    print(f"  No rules - consequence             {fmt(k, n)}")
    for s in SEEDS:
        drop = set(random.Random(s).sample(range(len(texts)), n_rules))
        keep_r = [i for i in range(len(texts)) if i not in drop]
        m_r = Model([texts[i] for i in keep_r])
        enc_r = Encoder(m_r, [texts[i] for i in keep_r])
        k, n, _ = evaluate(enc_r, fit_map(enc_r, sequence_pairs([verses[i] for i in keep_r])))
        print(f"  Random verses removed (#{s+1}) - consequence {fmt(k, n)}")

    print("\n" + "=" * 72)
    print("D. Diagnostic (added after A-C): does it have the pieces but not the link?")
    print("=" * 72)
    a, e, l, align = diagnose(enc)
    N = len(ITEMS)
    print(f"  Tells the right act from the wrong act      {fmt(a, N)}")
    print(f"  Tells the fortunate ending from the ruinous {fmt(e, N)}")
    print(f"  + one rule, 'as you sow, so you reap'       {fmt(l, 2 * N)}")
    print("\n  Did the Bible teach that link by itself? Alignment between the")
    print("  right/wrong direction and the fortune/ruin direction (0 = unrelated, 1 = same):")
    print(f"    full Bible               {align:+.3f}")
    print(f"    rules removed            {diagnose(enc_nr)[3]:+.3f}")
    for s in SEEDS:
        drop = set(random.Random(s).sample(range(len(texts)), n_rules))
        keep_r = [i for i in range(len(texts)) if i not in drop]
        m_r = Model([texts[i] for i in keep_r])
        print(f"    random removed (#{s+1})     {diagnose(Encoder(m_r, [texts[i] for i in keep_r]))[3]:+.3f}")


if __name__ == "__main__":
    main()
```

## File: `experiments/tiny_transformer.py`

```python
"""
Tiny Transformer Test
=====================

The word-averaging model (consequences_test.py) failed because it cannot
combine words: it knew "steal" was wrong but not that "took his neighbour's ox
by night and sold it" is stealing. A transformer reads word ORDER, so it can
compose meaning. Here we train a tiny one from scratch on the King James Bible
only (no other text, no pre-training) and re-run the same 40 new stories.

Scoring (fixed before training):
  MAIN   Shift test, 20 pairs. For each pair, does the model lean more toward the
         fortunate ending after the right act than after the wrong act?
         log P(fortunate|right) - log P(ruinous|right)
           >  log P(fortunate|wrong) - log P(ruinous|wrong)      chance = 50%
  2nd    Pick-the-ending accuracy over 40 stories.                chance = 50%
  3rd    Judgment shift, 20 pairs: does "...and this was evil in the sight of
         the lord" fit the wrong act better than the right act (relative to
         "...right in the sight of the lord")?                    chance = 50%

Conditions: full Bible / rules removed / same number of random verses removed,
each trained twice with different seeds.

Run:  python experiments/tiny_transformer.py [--steps 1500] [--only full]
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import time
from collections import Counter
from math import comb
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

from bible_understanding import RULE_RE, load_verses
from consequences_test import ITEMS

torch.set_num_threads(4)
OUT = Path(__file__).parent / "results_transformer.json"

CTX, D, LAYERS, HEADS, DROPOUT = 64, 192, 4, 4, 0.1
BATCH, LR = 64, 3e-3
JOIN = " , "                     # story + JOIN + ending
JUDGE_EVIL = "and this was evil in the sight of the lord"
JUDGE_RIGHT = "and this was right in the sight of the lord"

# ---------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------

TOK = re.compile(r"[a-z]+|[.,;:?!]")


def tok(text):
    return TOK.findall(text.lower())


class Vocab:
    def __init__(self, texts):
        c = Counter(t for x in texts for t in tok(x))
        self.itos = ["<unk>", "<v>"] + sorted(w for w, n in c.items() if n >= 2)
        self.stoi = {w: i for i, w in enumerate(self.itos)}

    def encode(self, text):
        return [self.stoi.get(t, 0) for t in tok(text)]

    def __len__(self):
        return len(self.itos)


def stream(vocab, texts):
    ids = []
    for t in texts:
        ids.append(1)            # verse boundary
        ids.extend(vocab.encode(t))
    return torch.tensor(ids, dtype=torch.long)

# ---------------------------------------------------------------------------
# Model: a standard small GPT
# ---------------------------------------------------------------------------

class Block(nn.Module):
    def __init__(self):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(D), nn.LayerNorm(D)
        self.attn = nn.MultiheadAttention(D, HEADS, dropout=DROPOUT, batch_first=True)
        self.mlp = nn.Sequential(nn.Linear(D, 4 * D), nn.GELU(), nn.Linear(4 * D, D),
                                 nn.Dropout(DROPOUT))

    def forward(self, x, mask):
        h = self.ln1(x)
        x = x + self.attn(h, h, h, attn_mask=mask, need_weights=False)[0]
        return x + self.mlp(self.ln2(x))


class TinyGPT(nn.Module):
    def __init__(self, n_vocab):
        super().__init__()
        self.tok = nn.Embedding(n_vocab, D)
        self.pos = nn.Embedding(CTX, D)
        self.blocks = nn.ModuleList(Block() for _ in range(LAYERS))
        self.ln = nn.LayerNorm(D)
        self.head = nn.Linear(D, n_vocab, bias=False)
        self.head.weight = self.tok.weight     # tied weights
        self.drop = nn.Dropout(DROPOUT)
        self.apply(self._init)

    @staticmethod
    def _init(m):
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, std=0.02)
        if isinstance(m, nn.Linear) and m.bias is not None:
            nn.init.zeros_(m.bias)

    def forward(self, idx):
        T = idx.shape[1]
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool), 1)
        x = self.drop(self.tok(idx) + self.pos(torch.arange(T)))
        for b in self.blocks:
            x = b(x, mask)
        return self.head(self.ln(x))


def train(vocab, texts, steps, seed, log_every=500):
    torch.manual_seed(seed)
    random.seed(seed)
    data = stream(vocab, texts)
    model = TinyGPT(len(vocab))
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.1)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, LR, total_steps=steps, pct_start=0.05)
    model.train()
    t0 = time.time()
    for step in range(1, steps + 1):
        ix = torch.randint(len(data) - CTX - 1, (BATCH,))
        x = torch.stack([data[i:i + CTX] for i in ix])
        y = torch.stack([data[i + 1:i + CTX + 1] for i in ix])
        loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten())
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        if step % log_every == 0 or step == steps:
            print(f"    step {step:5d}  loss {loss.item():.3f}  ({time.time() - t0:.0f}s)", flush=True)
    model.eval()
    return model

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

@torch.no_grad()
def logp(model, vocab, context, continuation):
    """Total log-probability of `continuation` given `context`."""
    c = [1] + vocab.encode(context)
    e = vocab.encode(continuation)
    ids = torch.tensor([(c + e)[-CTX:]])
    n_ctx = ids.shape[1] - len(e)
    lp = F.log_softmax(model(ids)[0], -1)
    return sum(lp[n_ctx - 1 + i, e[i]].item() for i in range(len(e)))


def p_value(k, n):
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n


def evaluate(model, vocab):
    shift = pick = judge = 0
    for right, wrong, fortunate, ruinous in ITEMS:
        d = {}
        for name, story in (("right", right), ("wrong", wrong)):
            d[name] = (logp(model, vocab, story + JOIN, fortunate)
                       - logp(model, vocab, story + JOIN, ruinous))
        shift += d["right"] > d["wrong"]
        pick += (d["right"] > 0) + (d["wrong"] < 0)
        j = {name: logp(model, vocab, story + JOIN, JUDGE_EVIL)
                   - logp(model, vocab, story + JOIN, JUDGE_RIGHT)
             for name, story in (("right", right), ("wrong", wrong))}
        judge += j["wrong"] > j["right"]
    n = len(ITEMS)
    return {"shift": shift, "pick": pick, "judge": judge, "n_pairs": n}


@torch.no_grad()
def held_out_loss(model, data):
    """Average next-word loss on verses the model never trained on."""
    losses = []
    for i in range(0, len(data) - CTX - 1, CTX):
        x, y = data[i:i + CTX][None], data[i + 1:i + CTX + 1][None]
        losses.append(F.cross_entropy(model(x)[0], y[0]).item())
    return sum(losses) / len(losses)

# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1])
    ap.add_argument("--only", nargs="+", default=None)
    args = ap.parse_args()

    verses = load_verses()
    texts = [t for _, t in verses]
    vocab = Vocab(texts)
    story_words = [t for it in ITEMS for s in it for t in tok(s)] + tok(JUDGE_EVIL + " " + JUDGE_RIGHT)
    oov = sorted({w for w in story_words if w not in vocab.stoi})
    print(f"Vocabulary {len(vocab):,} words. Test words unknown to the model: {oov or 'none'}")

    # Hold out every 50th verse to measure plain language skill (never trained on).
    held = [texts[i] for i in range(0, len(texts), 50)]
    pool = [i for i in range(len(texts)) if i % 50]
    rules = {i for i in pool if RULE_RE.search(texts[i])}
    conditions = {
        "full": pool,
        "no_rules": [i for i in pool if i not in rules],
        "minus_random": None,   # filled per seed
    }
    held_data = stream(vocab, held)

    results = json.loads(OUT.read_text()) if OUT.exists() else {}
    for name in conditions:
        if args.only and name not in args.only:
            continue
        for seed in args.seeds:
            key = f"{name}/seed{seed}/steps{args.steps}"
            if key in results:
                print(f"{key}: cached")
                continue
            idx = conditions[name]
            if name == "minus_random":
                drop = set(random.Random(seed).sample(pool, len(rules)))
                idx = [i for i in pool if i not in drop]
            print(f"\n== {key}: training on {len(idx):,} verses")
            model = train(vocab, [texts[i] for i in idx], args.steps, seed)
            r = evaluate(model, vocab)
            r["held_out_loss"] = round(held_out_loss(model, held_data), 3)
            results[key] = r
            OUT.write_text(json.dumps(results, indent=2))
            print(f"   shift {r['shift']}/20  pick {r['pick']}/40  judge {r['judge']}/20  "
                  f"held-out loss {r['held_out_loss']}")

    print("\nSummary (chance = 50%; p = chance of doing this well by luck)")
    for key, r in results.items():
        n = r["n_pairs"]
        print(f"  {key:28s} shift {r['shift']:2d}/{n} (p={p_value(r['shift'], n):.3f})  "
              f"pick {r['pick']:2d}/{2*n} (p={p_value(r['pick'], 2*n):.3f})  "
              f"judge {r['judge']:2d}/{n} (p={p_value(r['judge'], n):.3f})  "
              f"loss {r['held_out_loss']}")


if __name__ == "__main__":
    main()
```

## File: `experiments/shifting_word.py`

```python
"""
The Shifting Word ("velanok")
=============================

A made-up word that carries a running balance from one use to the next, and
whose SPELLING changes with that balance (like to / too / two / 2).

The rules
---------
  balance starts at 0
  each ordinary word adds its own value (negative leans wrong, positive leans right)
  a clear wrong  resets the balance to -17
  a clear right  resets the balance to +17
  each word also uses up 0.5 of the balance, so it drifts back toward 0
  whatever is left over carries to the next appearance ("remaining")
  at each appearance the word is written in the form that matches the balance

Optional (off by default): RECHARGE re-adds 17 in the balance's direction at
each appearance, as in "W1 = 17 + 4". Off because the balance then grows forever.

Spelling: five rotations of the syllables  sha-ru-vel-an-ok,
each a distinct new word the model has never seen:

  balance <= -12   anoksha    heavy wrong
  -11 .. -4        oksharu    leaning wrong
   -3 .. 3         velanok    unresolved
    4 .. 11        sharuvel   leaning right
  >= 12            ruvelan    heavy right

The experiment
--------------
1. Mark up the whole Bible: the word appears at the start of every verse,
   spelled for the balance left by the verses before it.
2. Train the tiny transformer on the marked-up Bible.
3. On the 40 new stories: the model writes the word ITSELF after the story
   (its own judgment), then we score the two endings.
Checks: (a) scrambled spellings = same extra word, no meaning;
        (b) oracle = we hand it the correct spelling.

Run:  python experiments/shifting_word.py [--steps 1500] [--seed 0]
"""

from __future__ import annotations

import argparse
import json
import random
import re
from math import comb
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

import tiny_transformer as tt
from collections import Counter

from bible_understanding import STOP, Model, load_verses, tokens
from consequences_test import BAD_SEEDS, GOOD_SEEDS, ITEMS

OUT = Path(__file__).parent / "results_shifting_word.json"

RESET = 17
RECHARGE = False
SPEND = 0.5         # each word also uses up this much of the balance (toward 0)
FORMS = ["anoksha", "oksharu", "velanok", "sharuvel", "ruvelan"]   # wrong ... right
SCALE = 30          # word value = round(moral lean * SCALE)
CLEAR_PCT = 3       # verses in the top/bottom 3% of lean count as clear choices

CLEAR_WRONG = re.compile(r"did (that which was )?evil in the (sight|eyes) of the lord|"
                         r"(wrought|done|committed) (great )?(wickedness|evil|abomination)", re.I)
CLEAR_RIGHT = re.compile(r"did that which was right in the (sight|eyes) of the lord|"
                         r"(walked|walk) in (all )?(his|my) (ways|statutes|commandments)|"
                         r"(was|were) (a )?(just|perfect|upright)", re.I)


def form_for(balance: float) -> str:
    if balance <= -12: return FORMS[0]
    if balance <= -4:  return FORMS[1]
    if balance < 4:    return FORMS[2]
    if balance < 12:   return FORMS[3]
    return FORMS[4]


class ShiftingWord:
    """The variable itself: a balance carried across uses."""

    def __init__(self, word_values: dict[str, int]):
        self.values = word_values
        self.balance = 0.0

    def emerge(self) -> str:
        """The word appears: write it in the form for the current balance."""
        if RECHARGE and self.balance:
            self.balance += RESET * np.sign(self.balance)
        return form_for(self.balance)

    def read(self, text: str, clear: int = 0):
        """Spend/add the following words; a clear choice resets the balance."""
        if clear:
            self.balance = RESET * clear
            return
        for w in tokens(text):
            if w not in self.values:
                continue
            self.balance += self.values[w]
            self.balance -= np.sign(self.balance) * min(SPEND, abs(self.balance))
        self.balance = float(np.clip(self.balance, -3 * RESET, 3 * RESET))

    def reset(self):
        self.balance = 0.0


def word_values(texts) -> dict[str, int]:
    """Each word's value = its lean on the good/evil direction learned from the Bible."""
    m = Model(texts)
    axis = (np.mean([m.v(w) for w in GOOD_SEEDS if m.has(w)], 0)
            - np.mean([m.v(w) for w in BAD_SEEDS if m.has(w)], 0))
    lean = m.vec @ axis
    # Centre so an ordinary run of text adds up to about zero (no drift):
    # weight by how often each word is actually used.
    freq = Counter(t for x in texts for t in tokens(x))
    content = [i for i, w in enumerate(m.vocab) if w not in STOP]
    weights = np.array([freq[m.vocab[i]] for i in content], float)
    lean -= np.average(lean[content], weights=weights)
    return {m.vocab[i]: int(round(lean[i] * SCALE)) for i in content}


def mark_up(verses, values, scramble_seed=None):
    """Insert the shifting word at the start of every verse."""
    sums = np.array([sum(values.get(w, 0) for w in tokens(t)) for _, t in verses])
    lo, hi = np.percentile(sums, [CLEAR_PCT, 100 - CLEAR_PCT])
    rng = random.Random(scramble_seed)
    sw, out, prev_book, n_clear = ShiftingWord(values), [], None, 0
    for (book, text), s in zip(verses, sums):
        if book != prev_book:
            sw.reset()
            prev_book = book
        form = sw.emerge()
        if scramble_seed is not None:
            form = rng.choice(FORMS)
        out.append(f"{form} {text}")
        clear = (-1 if CLEAR_WRONG.search(text) or s <= lo else
                 1 if CLEAR_RIGHT.search(text) or s >= hi else 0)
        n_clear += bool(clear)
        sw.read(text, clear)
    return out, n_clear

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

@torch.no_grad()
def lp_ids(model, ctx_ids, cont_ids):
    ids = torch.tensor([(ctx_ids + cont_ids)[-tt.CTX:]])
    n = ids.shape[1] - len(cont_ids)
    lp = F.log_softmax(model(ids)[0], -1)
    return sum(lp[n - 1 + i, c].item() for i, c in enumerate(cont_ids))


def evaluate(model, vocab):
    """Story -> [model writes the word] -> ending."""
    form_ids = [vocab.stoi[f] for f in FORMS]
    res = {"self_shift": 0, "self_pick": 0, "oracle_shift": 0, "oracle_pick": 0,
           "judge": 0, "n_pairs": len(ITEMS)}
    for right, wrong, fortunate, ruinous in ITEMS:
        ef, er = vocab.encode(fortunate), vocab.encode(ruinous)
        d_self, d_oracle, lean = {}, {}, {}
        for name, story in (("right", right), ("wrong", wrong)):
            ctx = [1] + vocab.encode(story) + [1]
            # the model's own choice of spelling
            scores = [lp_ids(model, ctx, [f]) for f in form_ids]
            probs = np.exp(np.array(scores) - max(scores))
            probs /= probs.sum()
            lean[name] = float(probs @ np.arange(-2, 3))     # expected position wrong..right
            own = form_ids[int(np.argmax(scores))]
            d_self[name] = lp_ids(model, ctx + [own], ef) - lp_ids(model, ctx + [own], er)
            # oracle: hand it the correct spelling
            ora = form_ids[4] if name == "right" else form_ids[0]
            d_oracle[name] = lp_ids(model, ctx + [ora], ef) - lp_ids(model, ctx + [ora], er)
        res["self_shift"] += d_self["right"] > d_self["wrong"]
        res["self_pick"] += (d_self["right"] > 0) + (d_self["wrong"] < 0)
        res["oracle_shift"] += d_oracle["right"] > d_oracle["wrong"]
        res["oracle_pick"] += (d_oracle["right"] > 0) + (d_oracle["wrong"] < 0)
        res["judge"] += lean["right"] > lean["wrong"]
    return res


def p_value(k, n):
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n


def demo(marked, verses, book="II Kings", start_text="In the twelfth year of Ahaz", n=8):
    i = next(k for k, (b, t) in enumerate(verses) if b == book and t.startswith(start_text))
    print(f"\n  Example ({book}): the word's spelling as the story unfolds")
    for k in range(i, i + n):
        f, rest = marked[k].split(" ", 1)
        print(f"    [{f:8s}] {rest[:95]}{'...' if len(rest) > 95 else ''}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--only", nargs="+", default=None)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    verses = load_verses()
    texts = [t for _, t in verses]
    values = word_values(texts)
    pool = [i for i in range(len(texts)) if i % 50]        # same split as tiny_transformer.py
    results = json.loads(OUT.read_text()) if OUT.exists() else {}

    for name, scramble in (("shifting_word", None), ("scrambled_control", args.seed)):
        if args.only and name not in args.only:
            continue
        marked, n_clear = mark_up(verses, values, scramble)
        if scramble is None and args.seed == 0:
            print(f"Clear right/wrong resets: {n_clear:,} of {len(verses):,} verses")
            from collections import Counter
            dist = Counter(m.split(" ", 1)[0] for m in marked)
            print("  Spelling counts:", ", ".join(f"{f} {dist[f]:,}" for f in FORMS))
            demo(marked, verses)
        key = f"{name}/seed{args.seed}/steps{args.steps}"
        if key in results:
            print(f"{key}: cached")
            continue
        train_texts = [marked[i] for i in pool]
        vocab = tt.Vocab(train_texts)
        print(f"\n== {key}: training on {len(train_texts):,} marked-up verses", flush=True)
        model = tt.train(vocab, train_texts, args.steps, seed=args.seed)
        r = evaluate(model, vocab)
        results[key] = r
        OUT.write_text(json.dumps(results, indent=2))
        print(f"   {r}", flush=True)

    print("\nSummary (chance = 50%)")
    for key, r in results.items():
        n = r["n_pairs"]
        print(f"  {key}")
        print(f"    model writes its own word:  shift {r['self_shift']}/{n} (p={p_value(r['self_shift'], n):.3f})"
              f"  pick {r['self_pick']}/{2*n} (p={p_value(r['self_pick'], 2*n):.3f})")
        print(f"    word's judgment of the act: {r['judge']}/{n} (p={p_value(r['judge'], n):.3f})")
        print(f"    handed the correct word:    shift {r['oracle_shift']}/{n} (p={p_value(r['oracle_shift'], n):.3f})"
              f"  pick {r['oracle_pick']}/{2*n} (p={p_value(r['oracle_pick'], 2*n):.3f})")


if __name__ == "__main__":
    main()
```

## File: `experiments/stories_v2.py`

```python
"""
Held-out story set v2, for confirming experiment 7.

Written BEFORE any model was scored on them, and never used for tuning.
Same rules as consequences_test.py:
- each pair = one situation, right act vs wrong act
- both share one fortunate and one ruinous ending (counterbalanced, so a
  model that always prefers one ending scores exactly 50%)
- moral label words are banned; no ending reuses a content word from its stories
- only words found in the King James Bible

Some pairs have near-identical endings ("...was destroyed" / "...was not
destroyed"), which only a reader of word order can tell apart.
"""

# (right-act story, wrong-act story, fortunate ending, ruinous ending)
ITEMS_V2 = [
    ("the husbandman left the corners of his field for the poor to glean",
     "the husbandman reaped the corners of his field and drove the poor away",
     "and the rain fell upon his land in due season",
     "and the locust devoured all his land"),
    ("the potter told the truth about the blemish in his vessel",
     "the potter hid the blemish in his vessel and sold it as whole",
     "and men came from far cities to buy of him",
     "and no man would buy of him again"),
    ("the elder rebuked his son gently and taught him",
     "the elder struck his son in anger and cast him out",
     "and the young man grew wise and kept his house",
     "and the young man departed and returned no more"),
    ("the captain spared the life of his enemy who was asleep",
     "the captain slew his enemy while he slept",
     "and his kingdom was made sure",
     "and the sword never departed from his house"),
    ("the maid spake well of her mistress in the gate",
     "the maid spake slander against her mistress in the gate",
     "and she was given a portion among the daughters",
     "and she was sent away with nothing"),
    ("the herdmen watered the flock of the widow before their own",
     "the herdmen drove the flock of the widow from the well",
     "and their cattle multiplied greatly",
     "and a lion came and slew their cattle"),
    ("the scribe wrote the words of the law truly",
     "the scribe changed the words of the law for gold",
     "and his name was remembered among the people",
     "and his name was blotted out"),
    ("the soldier was content with his wages",
     "the soldier took money by violence from the people",
     "and he returned home in peace",
     "and he fell by the sword in a strange land"),
    ("the woman returned the lost piece of silver to her neighbour",
     "the woman kept the lost piece of silver of her neighbour",
     "and her house was filled with gladness",
     "and thieves brake into her house and spoiled it"),
    ("the young men carried the old man over the river",
     "the young men mocked the old man and thrust him into the river",
     "and they came safely to the other side",
     "and the waters rose and swept them away"),
    ("the prince gave his bread to the prisoners",
     "the prince ate his fill and let the prisoners perish with hunger",
     "and the people loved him and set him on the throne",
     "and the people rose against him and slew him"),
    ("the merchant kept his promise though he lost by it",
     "the merchant forsook his promise when gold was offered",
     "and his word was trusted in every land",
     "and his partners departed from him"),
    ("the widow's son laboured to feed his mother",
     "the widow's son wasted his mother's living with harlots",
     "and he found favour with the elders",
     "and he came to want and fed swine"),
    ("the priest washed the feet of the poor stranger",
     "the priest shut the door of the temple against the poor stranger",
     "and his prayer was heard",
     "and his prayer was not heard"),
    ("the shepherd lad stood against the bear to save the lamb",
     "the shepherd lad ran away and left the lamb to the bear",
     "and he was chosen to lead the people",
     "and he was despised by all his brethren"),
    ("the husband loved his wife and spake kindly to her",
     "the husband beat his wife and spake roughly to her",
     "and their children grew strong",
     "and their children were scattered"),
    ("the rich man paid his debt on the day appointed",
     "the rich man denied his debt and sware falsely",
     "and his storehouses were filled",
     "and his storehouses were burned with fire"),
    ("the sojourner thanked the master of the house and departed",
     "the sojourner stole from the master of the house and fled by night",
     "and he was received again with joy",
     "and he was taken and bound in chains"),
    ("the elders opened the gates to the hungry",
     "the elders shut the gates against the hungry",
     "and the city stood for many generations",
     "and the city became a heap of stones"),
    ("the servant confessed his fault to his master",
     "the servant hid his fault and blamed another",
     "and he was set over all the household",
     "and he was driven out of the household"),
    ("the judge heard both sides before he spake",
     "the judge gave sentence before he heard the matter",
     "and men sought his counsel from afar",
     "and men despised his counsel"),
    ("the brethren divided their father's inheritance with equal portions",
     "the elder brother took all the inheritance and gave the younger nothing",
     "and they dwelt together in unity",
     "and there was strife between them unto death"),
    ("the woman gave water to the thirsty traveller and his camels",
     "the woman refused water to the thirsty traveller and his camels",
     "and she was given bracelets of gold",
     "and she was left alone in her old age"),
    ("the king hearkened to the counsel of the old men",
     "the king forsook the counsel of the old men and followed the young",
     "and the tribes stayed with him",
     "and ten tribes departed from him"),
    ("the mother taught her children to speak the truth",
     "the mother taught her children to deceive",
     "and her sons were honoured in the gate",
     "and her sons were put to shame in the gate"),
    ("the man returned the garment of the poor before the sun went down",
     "the man kept the garment of the poor man all the cold night",
     "and his own sons were warm and well fed",
     "and sickness came upon his own sons"),
    ("the fishers were mending the nets of their neighbours",
     "the fishers cut the nets of their neighbours by night",
     "and their ships were filled to the brim",
     "and their ships sank in the storm"),
    ("the governor fed the people in the years of famine",
     "the governor sold the bread of the people in the years of famine",
     "and the nation made him ruler over all",
     "and the nation stoned him in the street"),
    ("the young woman cared for her mother in her sickness",
     "the young woman left her mother alone in her sickness",
     "and she found a husband who loved her",
     "and she was forsaken by all her friends"),
    ("the man spake well of his neighbour behind his back",
     "the man spread lies about his neighbour behind his back",
     "and many friends gathered unto him",
     "and his friends turned against him"),
    ("the men of the city defended the stranger who sought refuge",
     "the men of the city delivered the stranger to his enemies",
     "and the town was spared in the day of trouble",
     "and the town was overthrown in the day of trouble"),
    ("the son buried his father with honour",
     "the son left the body of his father in the field for the birds",
     "and his own end was peaceable",
     "and his own end was violent"),
    ("the workman built the wall strong and true",
     "the workman built the wall with untempered morter and took the gold",
     "and the house stood through the storm",
     "and the house fell upon them in the storm"),
    ("the youth rose up before the hoary head and honoured the aged",
     "the youth mocked the bald head of the aged prophet",
     "and he lived to see his children's children",
     "and bears came out of the wood and tare him"),
    ("the man kept the oath he sware to his neighbour",
     "the man forgat the oath he sware to his neighbour and lied",
     "and his household was established",
     "and his household was cut off"),
    ("the woman spun wool and wrought with willing hands",
     "the woman was idle and ate the bread of others",
     "and her household was clothed in scarlet",
     "and her household went hungry"),
    ("the general gave the glory of the victory to his men",
     "the general took the glory of the victory for himself alone",
     "and his soldiers followed him into every battle",
     "and his soldiers forsook him in the next battle"),
    ("the steward told his lord the truth about the loss",
     "the steward wrote false words in the book to cover the loss",
     "and he was trusted with greater things",
     "and he was put out of his office"),
    ("the lad divided his loaves with the multitude",
     "the lad hid his loaves from the multitude",
     "and there was more than enough for all",
     "and there was not enough for any"),
    ("the neighbours lifted up the fallen ox of the man",
     "the neighbours passed by the fallen ox of the man",
     "and others stood by them in the day of their need",
     "and none stood by them in the day of their need"),
    ("the nobleman set his bondmen free in the year of release",
     "the nobleman kept his bondmen beyond the year of release",
     "and his fields brought forth abundantly",
     "and his fields became barren"),
    ("the men digged out the well for the whole village",
     "the men cast dung into the well of the next village",
     "and their own children drank and were strong",
     "and their own children drank and died"),
    ("the king kept the covenant he made with the small nation",
     "the king made war against the small nation and brake the covenant",
     "and his borders were at rest",
     "and famine came upon his land three years"),
    ("the young man fled from the wife of his master",
     "the young man lay with the wife of his master",
     "and he rose to great power",
     "and he was slain by her husband"),
    ("the merchant gave to the beggar at the gate",
     "the merchant passed by the beggar at the gate and laughed",
     "and his ships returned safely",
     "and his ships were broken at sea"),
    ("the people repented and turned from their ways",
     "the people hardened their hearts and would not turn",
     "and the city was not destroyed",
     "and the city was destroyed"),
    ("the servant kept the treasure he was given and increased it",
     "the servant buried the treasure he was given and did nothing",
     "and he was made ruler over ten cities",
     "and what he had was taken from him"),
    ("the man forgave the debt of his fellow servant",
     "the man took his fellow servant by the throat for a small debt",
     "and his lord had compassion on him",
     "and he was cast into prison until he paid all"),
    ("the young woman remained with her mother in law and served her",
     "the young woman forsook her mother in law in her poverty",
     "and she found a kinsman who redeemed her",
     "and she wandered alone in a strange country"),
    ("the father waited for his lost son and ran to embrace him",
     "the father refused his returning son and shut the door",
     "and there was melody and dancing in the house",
     "and there was weeping and silence in the house"),
    ("the man kept his vow to give the tenth of his increase",
     "the man kept back part of the price and lied about it",
     "and his storehouse overflowed",
     "and he fell down dead at once"),
    ("the woman cared for the stranger's child as her own",
     "the woman sold the stranger's child for silver",
     "and she lived to a ripe old age",
     "and she ended her days in misery"),
    ("the man fasted and prayed for his sick child",
     "the man made a feast and was drunken while his child lay sick",
     "and the little one recovered",
     "and the little one died"),
    ("the ruler made just laws for the poor",
     "the ruler made laws to rob the poor",
     "and his days were full of honour",
     "and his days were cut short"),
    ("the man warned his neighbour that the enemy was coming",
     "the man kept silent and let the enemy fall upon his neighbour",
     "and he was given a place of honour",
     "and the blood was required at his hand"),
    ("the little maid told her mistress of the prophet who could heal",
     "the little maid hid the way of healing from her mistress",
     "and her master was made whole",
     "and her master remained a leper"),
    ("the young man restored fourfold what he had taken",
     "the young man kept what he had taken by false accusation",
     "and all the people received him gladly",
     "and all the people murmured against him"),
    ("the leader washed the feet of his followers",
     "the leader made his followers carry him and wash his feet",
     "and they loved him unto death",
     "and they betrayed him in the night"),
    ("the family received the poor at their table",
     "the family drove the poor from their table",
     "and their bread never failed",
     "and their bread failed in the day of want"),
    ("the man spake softly to his angry brother",
     "the man answered his angry brother with bitter words",
     "and the wrath was turned away",
     "and the strife grew until blood was shed"),
    ("the prince humbled himself and asked forgiveness",
     "the prince exalted himself and would not ask forgiveness",
     "and he was restored to his throne",
     "and he was driven from men to eat grass"),
    ("the people gave freely to build the house of prayer",
     "the people kept their gold and built houses for themselves",
     "and the vines and the fig trees bare much",
     "and they sowed much and brought in little"),
    ("the man kept in his ox lest it should push any man",
     "the man let his ox go loose though he knew it was wont to push with his horn",
     "and no harm came near his house",
     "and his own life was required of him"),
    ("the brethren sought their lost brother in the far country",
     "the brethren sold their brother to merchants going down to egypt",
     "and they lived to embrace him again with joy",
     "and their father mourned many days"),
    ("the elder spake for the accused man who had no friend",
     "the elder spake against the accused man for a bribe",
     "and his gray hairs went down in honour",
     "and his gray hairs went down in sorrow"),
    ("the master gave rest to his servants on the seventh day",
     "the master made his servants labour seven days without rest",
     "and the household loved him",
     "and the household hated him and fled"),
    ("the man fed his enemy when he was hungry",
     "the man rejoiced when his enemy was hungry",
     "and the hatred between their houses ended",
     "and the hatred between their houses grew"),
    ("the scribe taught the children without price",
     "the scribe would not teach the children of the poor",
     "and many learned and remembered his name",
     "and his learning died with him"),
    ("the man helped the ass of his enemy that lay under the burden",
     "the man left the ass of his enemy lying under the burden",
     "and the other became his friend",
     "and the other sought his life"),
    ("the youth gave his place at the feast to the lame",
     "the youth thrust the lame away from the feast",
     "and he was called up higher before all",
     "and he was brought down lower before all"),
    ("the queen spake for her people before the king",
     "the queen kept silent while her people were sold to death",
     "and the nation was delivered",
     "and the nation perished"),
    ("the man gave his brother the better land",
     "the man chose the better land and gave his brother the worse",
     "and his seed became as the stars",
     "and his city was overthrown and he fled to a cave"),
    ("the wise woman made peace between the king and the rebel city",
     "the woman stirred up the rebel city against the king",
     "and the people were saved from the sword",
     "and the people were laid waste by the sword"),
    ("the young man refused the wine of the king and ate pulse",
     "the young man filled himself with the wine of the king",
     "and he was found ten times wiser than the rest",
     "and his face was lean and his heart dull"),
    ("the woman was patient with her angry neighbour",
     "the woman stirred strife with her neighbour every day",
     "and her days were quiet",
     "and her days were full of contention"),
    ("the man confessed his error before the congregation",
     "the man denied his error and accused the innocent",
     "and he was restored among them",
     "and he was put out of the camp"),
    ("the king brake down the groves and the high places of the idols",
     "the king built groves and high places for the idols",
     "and the lord gave him rest round about",
     "and the lord stirred up enemies against him"),
    ("the merchant gave full measure pressed down and running over",
     "the merchant gave short measure and defrauded the widow",
     "and his own barns were filled with plenty",
     "and his own barns were empty"),
    ("the prophet told the king the hard truth to his face",
     "the prophet spake smooth words to the king and told him lies",
     "and the ruler turned and lived",
     "and the ruler went up to battle and died"),
    ("the children carried water to their aged parents",
     "the children took the goods of their aged parents and left them",
     "and they were remembered with love",
     "and they were remembered with scorn"),
    ("the man made peace with his brother before bringing his gift",
     "the man brought his gift to the altar while hating his brother",
     "and his offering was accepted",
     "and his offering was rejected"),
    ("the woman nursed the sick man who was her enemy",
     "the woman mocked the sick man who was her enemy",
     "and she was spared in the day of plague",
     "and she was smitten in the day of plague"),
    ("the hired men laboured faithfully though no man watched",
     "the hired men slept and stole when no man watched",
     "and the vineyard yielded rich fruit",
     "and the vineyard was covered with thorns"),
    ("the men divided the spoil with those who stayed behind",
     "the men refused the spoil to those who stayed behind",
     "and there was unity in the camp",
     "and there was murmuring in the camp"),
    ("the son asked his father for wisdom rather than riches",
     "the son asked his father for riches rather than wisdom",
     "and he was given honour and long life",
     "and he lost all and was left with nothing"),
    ("the woman gave the two mites all that she had",
     "the woman gave nothing though she had much",
     "and her name is spoken of to this day",
     "and her name was forgotten"),
    ("the man took in the fatherless child and raised him as a son",
     "the man drove the fatherless child from the door into the cold",
     "and the lad became a prince in the land",
     "and the lad grew up to burn his house"),
    ("the man let the land rest in the seventh year",
     "the man tilled the land every year without rest",
     "and the ground gave rich harvest",
     "and the ground turned to dust"),
    ("the guard let the innocent man go free",
     "the guard beat the innocent man for sport",
     "and he was raised to captain",
     "and he was hanged on a tree"),
    ("the damsel told her father the truth about the broken pitcher",
     "the damsel blamed her little brother for the broken pitcher",
     "and she was trusted all her days",
     "and she was never trusted again"),
    ("the people chose an honest man to lead them",
     "the people chose the man who gave them the most gold",
     "and the nation prospered under him",
     "and the nation went into bondage"),
    ("the man restored the landmark of his neighbour to the old place",
     "the man removed the landmark of his neighbour by night",
     "and his fields were secure for his children",
     "and his fields were taken from his children"),
    ("the man spake the truth though the multitude hated it",
     "the man told the multitude what they wished to hear",
     "and in the end he was honoured",
     "and in the end he was ashamed"),
    ("the son kept the words his father gave him",
     "the son despised the words his father gave him",
     "and his paths were straight",
     "and his paths led down to death"),
    ("the man covered his father's nakedness with a garment going backward",
     "the man looked upon his father's nakedness and told his brethren",
     "and his seed was enlarged",
     "and his seed became servants of servants"),
    ("the man stood up for the woman they wished to stone",
     "the man took up the first stone to throw at the woman",
     "and the accusers went away one by one",
     "and the multitude shed blood that day"),
    ("the king gave the throne to the son who was worthy",
     "the king gave the throne to the son who spake smooth words to him",
     "and the kingdom was strong after him",
     "and the kingdom was divided after him"),
    ("the woman kept her lamp filled with oil while she waited",
     "the woman let her lamp go out and slept",
     "and she went in to the marriage feast",
     "and the door was shut against her"),
    ("the man gave the first fruits to the poor and the levite",
     "the man ate all the first fruits himself and gave none",
     "and the heavens opened and poured rain",
     "and the heavens were shut as brass"),
    ("the brother wept and forgave the brethren who sold him",
     "the brother took vengeance upon the brethren who sold him",
     "and the whole family was saved in the famine",
     "and the whole family perished in the famine"),
]
```

## File: `experiments/confirm.py`

```python
"""
Confirmation run for experiment 7 (the shifting word)
=====================================================

Pre-registered (committed before any model saw stories_v2.py):

  Models: three conditions x three training seeds (0, 1, 2), 1,500 steps each.
    baseline    - plain Bible, no shifting word        (tiny_transformer.py)
    shifting    - Bible marked up with the shifting word (shifting_word.py)
    scrambled   - same marked-up Bible, spelling chosen at random

  Test: the 100 NEW story pairs in stories_v2.py. Score per pair = the shift
  test (does the model lean more toward the fortunate ending after the right
  act than after the wrong act?). The old 20 pairs are re-scored too, as a
  reproducibility check.

  PRIMARY  (confirmed if p < 0.05):
    For each new pair, take the majority vote of the 3 shifting-word models.
    The share of pairs where the majority is right must beat 50%
    (one-sided sign test over the 100 pairs).

  SECONDARY (confirmed if p < 0.05):
    Shifting beats scrambled on the same pairs. Per pair, count correct runs
    (0-3) for each; sign test over pairs where the counts differ.

  Anything else reported is descriptive only.

Run:  python experiments/confirm.py          (about 1.5-2 hours on 4 CPU cores)
Trained models are saved to experiments/models/ (not committed) and re-used.
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path

import numpy as np
import torch

import shifting_word as sw
import tiny_transformer as tt
from bible_understanding import load_verses
from consequences_test import ITEMS as ITEMS_V1
from stories_v2 import ITEMS_V2

HERE = Path(__file__).parent
MODELS = HERE / "models"
OUT = HERE / "results_confirm.json"
SEEDS = [0, 1, 2]
STEPS = 1500
CONDITIONS = ["shifting", "scrambled", "baseline"]


def p_at_least(k, n):
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else 1.0

# ---------------------------------------------------------------------------
# Per-pair scoring (same logic as the original scripts, but returns each pair)
# ---------------------------------------------------------------------------

def score_word_model(model, vocab, items):
    """Model writes its own shifting word after the story, then endings are compared."""
    form_ids = [vocab.stoi[f] for f in sw.FORMS]
    shift, judge = [], []
    for right, wrong, fortunate, ruinous in items:
        ef, er = vocab.encode(fortunate), vocab.encode(ruinous)
        d, lean = {}, {}
        for name, story in (("right", right), ("wrong", wrong)):
            ctx = [1] + vocab.encode(story) + [1]
            scores = [sw.lp_ids(model, ctx, [f]) for f in form_ids]
            probs = np.exp(np.array(scores) - max(scores))
            probs /= probs.sum()
            lean[name] = float(probs @ np.arange(-2, 3))
            own = form_ids[int(np.argmax(scores))]
            d[name] = sw.lp_ids(model, ctx + [own], ef) - sw.lp_ids(model, ctx + [own], er)
        shift.append(bool(d["right"] > d["wrong"]))
        judge.append(bool(lean["right"] > lean["wrong"]))
    return shift, judge


def score_baseline(model, vocab, items):
    shift, judge = [], []
    for right, wrong, fortunate, ruinous in items:
        d = {n: tt.logp(model, vocab, s + tt.JOIN, fortunate) - tt.logp(model, vocab, s + tt.JOIN, ruinous)
             for n, s in (("right", right), ("wrong", wrong))}
        j = {n: tt.logp(model, vocab, s + tt.JOIN, tt.JUDGE_EVIL) - tt.logp(model, vocab, s + tt.JOIN, tt.JUDGE_RIGHT)
             for n, s in (("right", right), ("wrong", wrong))}
        shift.append(bool(d["right"] > d["wrong"]))
        judge.append(bool(j["wrong"] > j["right"]))
    return shift, judge

# ---------------------------------------------------------------------------

def training_texts(cond, seed, verses, values, pool):
    texts = [t for _, t in verses]
    if cond == "baseline":
        return [texts[i] for i in pool]
    marked, _ = sw.mark_up(verses, values, None if cond == "shifting" else seed)
    return [marked[i] for i in pool]


def get_model(cond, seed, train_texts):
    vocab = tt.Vocab(train_texts)
    path = MODELS / f"{cond}_seed{seed}_steps{STEPS}.pt"
    model = tt.TinyGPT(len(vocab))
    if path.exists():
        model.load_state_dict(torch.load(path))
        model.eval()
        print(f"  loaded {path.name}", flush=True)
    else:
        print(f"\n== training {cond} seed {seed}", flush=True)
        model = tt.train(vocab, train_texts, STEPS, seed)
        MODELS.mkdir(exist_ok=True)
        torch.save(model.state_dict(), path)
    return model, vocab


def analyse(results):
    print("\n" + "=" * 72)
    print("RESULTS on the 100 new story pairs (50% = guessing)")
    print("=" * 72)
    n = len(ITEMS_V2)
    per = {}
    for cond in CONDITIONS:
        runs = [results[f"{cond}/seed{s}"] for s in SEEDS if f"{cond}/seed{s}" in results]
        if not runs:
            continue
        shift = np.array([r["v2_shift"] for r in runs])
        judge = np.array([r["v2_judge"] for r in runs])
        per[cond] = shift.sum(0)
        each = ", ".join(f"{int(x.sum())}/{n}" for x in shift)
        majority = int((shift.sum(0) * 2 > len(runs)).sum())
        print(f"  {cond:9s} shift per run: {each}   majority vote: {majority}/{n} "
              f"(p = {p_at_least(majority, n):.4f})")
        print(f"  {'':9s} judge per run: " + ", ".join(f"{int(x.sum())}/{n}" for x in judge))
        old = ", ".join(f"{sum(r['v1_shift'])}/20" for r in runs)
        print(f"  {'':9s} old 20 pairs, shift per run: {old}")

    if len(per.get("shifting", [])) and len(per.get("scrambled", [])):
        a, b = per["shifting"], per["scrambled"]
        wins, losses = int((a > b).sum()), int((a < b).sum())
        print(f"\n  Shifting vs scrambled, pair by pair: shifting better on {wins}, "
              f"worse on {losses}, tied on {n - wins - losses} "
              f"(p = {p_at_least(wins, wins + losses):.4f})")

    runs = [results[f"shifting/seed{s}"] for s in SEEDS if f"shifting/seed{s}" in results]
    if len(runs) == len(SEEDS):
        maj = int((np.array([r["v2_shift"] for r in runs]).sum(0) * 2 > len(SEEDS)).sum())
        p1 = p_at_least(maj, n)
        p2 = p_at_least(wins, wins + losses) if "scrambled" in per else float("nan")
        print("\n  PRE-REGISTERED VERDICT")
        print(f"    Primary   (shifting beats 50%):       {'CONFIRMED' if p1 < 0.05 else 'NOT CONFIRMED'}  (p = {p1:.4f})")
        print(f"    Secondary (shifting beats scrambled): {'CONFIRMED' if p2 < 0.05 else 'NOT CONFIRMED'}  (p = {p2:.4f})")


def main():
    verses = load_verses()
    texts = [t for _, t in verses]
    values = sw.word_values(texts)
    pool = [i for i in range(len(texts)) if i % 50]
    results = json.loads(OUT.read_text()) if OUT.exists() else {}

    for seed in SEEDS:
        for cond in CONDITIONS:
            key = f"{cond}/seed{seed}"
            if key in results:
                continue
            train_texts = training_texts(cond, seed, verses, values, pool)
            model, vocab = get_model(cond, seed, train_texts)
            scorer = score_baseline if cond == "baseline" else score_word_model
            v1s, v1j = scorer(model, vocab, ITEMS_V1)
            v2s, v2j = scorer(model, vocab, ITEMS_V2)
            results[key] = {"v1_shift": v1s, "v1_judge": v1j, "v2_shift": v2s, "v2_judge": v2j}
            OUT.write_text(json.dumps(results))
            print(f"  {key}: new pairs shift {sum(v2s)}/100, judge {sum(v2j)}/100 | "
                  f"old pairs shift {sum(v1s)}/20", flush=True)

    analyse(results)


if __name__ == "__main__":
    main()
```

## File: `experiments/method_comparison.py`

```python
"""
Method comparison: the shifting word vs the closest established method
=====================================================================

Same tiny transformer, same Bible, same 1,500 training steps, same 100 new
test story pairs (stories_v2.py). Only the way the training text is marked
changes. Each method is trained with 3 seeds.

Methods
  baseline     plain Bible, no marker                         (from confirm.py)
  scrambled    marker word with random spelling (control)     (from confirm.py)
  shifting     the owner's shifting word: a carried balance,
               reset to +/-17 on clear right/wrong, spent by
               following words, 5 spellings                   (from confirm.py)
  label        PLAIN GOOD/BAD LABEL, the established approach
               (like conditional training with good/bad tokens):
               same 5 spellings, same position, but each one
               judges ONLY the verse right before it. No carry,
               no reset, no fading. Uses the same verdict phrases
               ("did evil in the sight of the Lord" ...) and the
               same word values. Cut-offs chosen so each spelling
               appears about as often as in "shifting".
  carry3       carried balance like "shifting" but only 3
               spellings (wrong / unresolved / right): tests
               whether the graded spelling matters.

PRE-REGISTERED (committed before label/carry3 were trained)
  Main measure: JUDGING right vs wrong on the 100 new pairs (the measure where
  the shifting word showed signal; it is the same score for every method).
  Q1  shifting vs label:  per pair, count correct runs (0-3) for each;
      one-sided sign test over pairs where counts differ.  p < 0.05 = shifting
      beats the established method.
  Q2  shifting vs carry3: same test.  p < 0.05 = graded spelling helps.
  Also reported: each method vs chance (majority vote, sign test) and the
  consequence ("shift") score. No method was tuned on stories_v2.

Run:  python experiments/method_comparison.py   (about 66 minutes; reuses saved models)
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path

import numpy as np
import torch

import confirm
import shifting_word as sw
import tiny_transformer as tt
from bible_understanding import load_verses, tokens
from consequences_test import ITEMS as ITEMS_V1
from stories_v2 import ITEMS_V2

HERE = Path(__file__).parent
OUT = HERE / "results_methods.json"
SEEDS = [0, 1, 2]
STEPS = 1500
NEW = ["label", "carry3"]
ALL = ["baseline", "scrambled", "shifting", "label", "carry3"]


def p_at_least(k, n):
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else 1.0


POSITION = {f: k - 2 for k, f in enumerate(sw.FORMS)}       # anoksha -2 ... ruvelan +2


def score(model, vocab, items):
    """Same scoring as confirm.score_word_model, but only over the spellings this method uses
    (carry3 has 3). Model writes its own word after the story, then endings are compared."""
    forms = [f for f in sw.FORMS if f in vocab.stoi]
    ids, pos = [vocab.stoi[f] for f in forms], np.array([POSITION[f] for f in forms])
    shift, judge = [], []
    for right, wrong, fortunate, ruinous in items:
        ef, er = vocab.encode(fortunate), vocab.encode(ruinous)
        d, lean = {}, {}
        for name, story in (("right", right), ("wrong", wrong)):
            ctx = [1] + vocab.encode(story) + [1]
            scores = [sw.lp_ids(model, ctx, [f]) for f in ids]
            probs = np.exp(np.array(scores) - max(scores))
            probs /= probs.sum()
            lean[name] = float(probs @ pos)
            own = ids[int(np.argmax(scores))]
            d[name] = sw.lp_ids(model, ctx + [own], ef) - sw.lp_ids(model, ctx + [own], er)
        shift.append(bool(d["right"] > d["wrong"]))
        judge.append(bool(lean["right"] > lean["wrong"]))
    return shift, judge


def mark_label(verses, values):
    """Each verse is preceded by a spelling that judges ONLY the verse before it."""
    shifting, _ = sw.mark_up(verses, values)
    share = np.array([sum(m.split(" ", 1)[0] == f for m in shifting) for f in sw.FORMS], float)
    cuts = np.cumsum(share / share.sum())[:-1]          # same frequency of each spelling
    scores = np.array([sum(values.get(w, 0) for w in tokens(t)) for _, t in verses], float)
    edges = np.quantile(scores, cuts)
    out, prev_book = [], None
    for k, (book, text) in enumerate(verses):
        if book != prev_book or k == 0:
            form = sw.FORMS[2]                            # unresolved at the start of a book
            prev_book = book
        else:
            prev = verses[k - 1][1]
            if sw.CLEAR_WRONG.search(prev):          # same verdict phrases the shifting word uses
                form = sw.FORMS[0]
            elif sw.CLEAR_RIGHT.search(prev):
                form = sw.FORMS[4]
            else:
                form = sw.FORMS[int(np.searchsorted(edges, scores[k - 1], side="right"))]
        out.append(f"{form} {text}")
    return out


def mark_carry3(verses, values):
    """Same carried balance as the shifting word, but only three spellings."""
    shifting, _ = sw.mark_up(verses, values)
    three = {sw.FORMS[0]: sw.FORMS[0], sw.FORMS[1]: sw.FORMS[0], sw.FORMS[2]: sw.FORMS[2],
             sw.FORMS[3]: sw.FORMS[4], sw.FORMS[4]: sw.FORMS[4]}
    return [three[m.split(" ", 1)[0]] + " " + m.split(" ", 1)[1] for m in shifting]


def main():
    verses = load_verses()
    texts = [t for _, t in verses]
    values = sw.word_values(texts)
    pool = [i for i in range(len(texts)) if i % 50]
    res = json.loads(OUT.read_text()) if OUT.exists() else {}

    # Existing methods: copy their per-pair scores from the confirmation run.
    conf = json.loads(confirm.OUT.read_text())
    for m in ("baseline", "scrambled", "shifting"):
        for s in SEEDS:
            k = f"{m}/seed{s}"
            if k in conf:
                res[k] = conf[k]

    marked = {"label": mark_label(verses, values), "carry3": mark_carry3(verses, values)}
    for m in NEW:
        dist = {f: sum(x.split(" ", 1)[0] == f for x in marked[m]) for f in sw.FORMS}
        print(f"{m} spelling counts: {dist}")

    for s in SEEDS:
        for m in NEW:
            key = f"{m}/seed{s}"
            if key in res:
                continue
            train_texts = [marked[m][i] for i in pool]
            vocab = tt.Vocab(train_texts)
            path = confirm.MODELS / f"{m}_seed{s}_steps{STEPS}.pt"
            model = tt.TinyGPT(len(vocab))
            if path.exists():
                model.load_state_dict(torch.load(path))
                model.eval()
            else:
                print(f"\n== training {m} seed {s}", flush=True)
                model = tt.train(vocab, train_texts, STEPS, s)
                confirm.MODELS.mkdir(exist_ok=True)
                torch.save(model.state_dict(), path)
            v1s, v1j = score(model, vocab, ITEMS_V1)
            v2s, v2j = score(model, vocab, ITEMS_V2)
            res[key] = {"v1_shift": v1s, "v1_judge": v1j, "v2_shift": v2s, "v2_judge": v2j}
            OUT.write_text(json.dumps(res))
            print(f"  {key}: judge {sum(v2j)}/100, consequence {sum(v2s)}/100", flush=True)

    report(res)


def report(res):
    n = len(ITEMS_V2)
    counts = {}
    print("\n" + "=" * 72)
    print("METHOD COMPARISON on 100 new story pairs (50% = guessing)")
    print("=" * 72)
    print(f"  {'method':10s} {'judging, per run':20s} {'avg':>5s} {'majority':>9s} {'p':>8s}   consequence per run")
    for m in ALL:
        runs = [res[f"{m}/seed{s}"] for s in SEEDS if f"{m}/seed{s}" in res]
        if not runs:
            continue
        J = np.array([r["v2_judge"] for r in runs])
        S = np.array([r["v2_shift"] for r in runs])
        counts[m] = J.sum(0)
        maj = int((J.sum(0) * 2 > len(runs)).sum())
        print(f"  {m:10s} {', '.join(str(int(x)) for x in J.sum(1)):20s} {J.mean() * 100:5.1f} "
              f"{maj:>6d}/{n} {p_at_least(maj, n):8.4f}   {', '.join(str(int(x)) for x in S.sum(1))}")

    def vs(a, b, label, verdict=True):
        if a not in counts or b not in counts:
            return
        w, l = int((counts[a] > counts[b]).sum()), int((counts[a] < counts[b]).sum())
        p = p_at_least(w, w + l)
        tail = f"-> {'CONFIRMED' if p < 0.05 else 'NOT CONFIRMED'}" if verdict else "(descriptive)"
        print(f"  {label}: {a} better on {w} pairs, worse on {l}  (p = {p:.4f})  {tail}")

    print("\n  PRE-REGISTERED")
    vs("shifting", "label", "Q1 shifting beats plain good/bad label")
    vs("shifting", "carry3", "Q2 graded spelling beats 3 spellings ")
    print("\n  Descriptive")
    vs("shifting", "baseline", "   shifting vs no marker            ", verdict=False)
    vs("shifting", "scrambled", "   shifting vs scrambled            ", verdict=False)
    vs("label", "baseline", "   plain label vs no marker         ", verdict=False)


if __name__ == "__main__":
    main()
```

## File: `experiments/long_story_test.py`

```python
"""
Long-story test: does the CARRIED balance matter once the act is out of sight?
=============================================================================

Experiment 10 found the owner's shifting word ties a plain per-verse good/bad
label on one-sentence stories. But the owner's idea is about carrying weight
FORWARD ("+4 remaining" into the next use). One-sentence stories never need
that. Here the decisive act comes first, then neutral sentences follow until
the act has scrolled out of the model's 64-token window. Only a marker that
carries state from one sentence to the next can still remember it.

Uses the 15 models already trained (no new training): baseline, scrambled,
shifting, label, carry3 x seeds 0-2.

Story layout, same filler for the right and wrong version of each pair:
  [act sentence] [neutral filler] [neutral filler] ... -> judgment
Marked models write their own marker word after every sentence (greedy), so a
carrying model can pass the judgment forward through its own markers. The
judgment is the lean of the final marker (wrong ... right). The baseline (no
marker) is judged with "and this was evil / right in the sight of the lord".

Two versions:
  A  verdict carried: the act ends with the Bible's own verdict ("and he did
     evil in the sight of the lord" / "and he did that which was right in the
     sight of the lord"). This triggers the owner's +/-17 reset.
  B  act carried: the act alone, which the owner's rule treats as not clear.
Filler is added until the act sentence AND the first marker written after it lie
entirely outside the final window (checked for every story). (Correction made
during the first run: v1 only pushed the act out of view, so the first marker,
which directly judges the act, was still visible and nothing had to be carried.
v1 results are kept aside, not used.) A "short" version (no filler) is also scored as a
sanity reference.

PRE-REGISTERED (committed before scoring)
  Score per story pair: 1 if judged right, 0 if wrong, 0.5 on an exact tie.
  (Correction made after the first model's result: ties had been counted as
  wrong. A model that can no longer tell the two stories apart produces exact
  ties, and it should score chance, not zero. This change can only help the
  methods that don't carry.)
  Summing those scores over the 3 seeds per pair; one-sided sign test over
  pairs where the sums differ.
  L1  version A: shifting beats label, p < 0.05
  L2  version B: shifting beats label, p < 0.05
  L3  version A: carry3 beats label, p < 0.05 (secondary)
  Also reported: every method vs 50% (majority vote), and the short version.

EXPLORATORY (added after seeing the pre-registered run; not part of the verdict)
  --start-marker: begin every marked story with the neutral marker "velanok",
  as every verse in training is preceded by a marker. A diagnostic showed the
  shifting word copies its marker perfectly down the story but misjudges the first
  sentence when no marker comes before it. Results go to
  results_long_story_startmarker.json.

Run:  python experiments/long_story_test.py [--start-marker]   (15-30 minutes, CPU only, no training)
"""

from __future__ import annotations

import json
import random
from math import comb
from pathlib import Path

import numpy as np
import torch

import confirm
import method_comparison as mc
import shifting_word as sw
import tiny_transformer as tt
from bible_understanding import load_verses, tokens
from consequences_test import BANNED
from stories_v2 import ITEMS_V2

torch.set_num_threads(1)            # share the CPU politely with any training job
HERE = Path(__file__).parent
OUT = HERE / "results_long_story.json"
START_MARKER = False
SEEDS = [0, 1, 2]
METHODS = ["baseline", "scrambled", "shifting", "label", "carry3"]
VERDICT_WRONG = "and he did evil in the sight of the lord"
VERDICT_RIGHT = "and he did that which was right in the sight of the lord"
MAX_FILLERS = 10

FILLER_POOL = [
    "and it came to pass on the morrow, that they went forth into the field",
    "and the sun went down, and they lodged there that night",
    "and in the morning they rose up early, and went on their way",
    "and they came unto the well, and drew water, and gave the camels to drink",
    "and the men sat down by the gate of the city until the evening",
    "and the days of the harvest were come, and the people went out to the fields",
    "and they journeyed from that place, and pitched their tents by the river",
    "and it was told the elders of the city, and they came out to see",
    "and the rain fell upon the mountains, and the waters ran down into the valley",
    "and the shepherds brought the flocks home at the going down of the sun",
    "and the road went down from the hills toward the sea",
    "and the next day they numbered the sheep and counted the oxen",
    "and the servants made ready the asses for the journey",
    "and the wind blew from the west, and the clouds passed over",
    "and they came to a place where there were twelve wells of water and seventy palm trees",
    "and they took bread and fish, and sat down upon the grass",
    "and the merchants came with their camels bearing spices",
    "and the city had four gates, on every side one gate",
    "and the ship went over to the other side of the sea",
    "and they builded houses of stone and of cedar wood",
    "and the candle was lighted, and they sat at meat together",
    "and the oxen were yoked, and the ground was tilled",
    "and the watchman stood upon the tower and looked toward the hills",
    "and the moon rose over the hills, and the night was still",
    "and after many days they came again to their own country",
    "and they went down to the brook, and the brook was full",
    "and the women ground the corn at the mill in the morning",
    "and the camels kneeled down without the city by the well",
]


def p_at_least(k, n):
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else 1.0


def marked_corpus(method, verses, values, seed):
    if method == "baseline":
        return [t for _, t in verses]
    if method == "shifting":
        return sw.mark_up(verses, values)[0]
    if method == "scrambled":
        return sw.mark_up(verses, values, seed)[0]
    if method == "label":
        return mc.mark_label(verses, values)
    return mc.mark_carry3(verses, values)


def load_model(method, seed, train_texts):
    vocab = tt.Vocab(train_texts)
    name = {"baseline": "baseline", "scrambled": "scrambled", "shifting": "shifting",
            "label": "label", "carry3": "carry3"}[method]
    model = tt.TinyGPT(len(vocab))
    model.load_state_dict(torch.load(confirm.MODELS / f"{name}_seed{seed}_steps1500.pt"))
    model.eval()
    return model, vocab


def neutral_fillers(values, vocab):
    """Keep filler sentences that the owner's rule sees as neutral and the model knows every word of."""
    keep = []
    for f in FILLER_POOL:
        ws = tokens(f)
        if (abs(sum(values.get(w, 0) for w in ws)) <= 2 and max(abs(values.get(w, 0)) for w in ws) <= 3
                and not (BANNED & set(ws)) and not sw.CLEAR_WRONG.search(f) and not sw.CLEAR_RIGHT.search(f)
                and all(t in vocab.stoi for t in tt.tok(f))):
            keep.append(f)
    return keep


def build_stories(version, fillers, vocab, k_pair):
    """Right/wrong story pair as lists of sentences, padded with the same fillers until the act is out of view."""
    right, wrong = ITEMS_V2[k_pair][0], ITEMS_V2[k_pair][1]
    if version == "A":
        right, wrong = f"{right}, {VERDICT_RIGHT}", f"{wrong}, {VERDICT_WRONG}"
    if version == "short":
        return [right], [wrong], 0
    rng = random.Random(1000 + k_pair)
    pad = []
    while True:
        pad.append(rng.choice(fillers))
        # tokens after the FIRST marker (which directly judges the act): every filler's words,
        # the later boundaries and markers, and the final boundary. These must fill the whole
        # window, so neither the act nor that first marker is visible at the final judgment.
        after_first_marker = sum(len(tt.tok(f)) for f in pad) + 2 * (len(pad) - 1) + 1
        if after_first_marker >= tt.CTX or len(pad) >= MAX_FILLERS:
            break
    assert after_first_marker >= tt.CTX, "act or first marker still visible"
    return [right] + pad, [wrong] + pad, len(pad)


@torch.no_grad()
def judge_marked(model, vocab, sentences):
    """Model writes its own marker after each sentence; returns the lean of the final marker."""
    forms = [f for f in sw.FORMS if f in vocab.stoi]
    ids = [vocab.stoi[f] for f in forms]
    pos = np.array([mc.POSITION[f] for f in forms])
    start = [vocab.stoi[sw.FORMS[2]]] if START_MARKER else []
    ctx = [1] + start + vocab.encode(sentences[0]) + [1]
    for s in sentences[1:]:
        scores = [sw.lp_ids(model, ctx, [i]) for i in ids]
        ctx += [ids[int(np.argmax(scores))]] + vocab.encode(s) + [1]
    scores = np.array([sw.lp_ids(model, ctx, [i]) for i in ids])
    p = np.exp(scores - scores.max())
    return float((p / p.sum()) @ pos)


@torch.no_grad()
def judge_plain(model, vocab, sentences):
    """No marker: compare 'evil' vs 'right' judgment phrases after the last sentence (positive = right)."""
    ctx = [1]
    for s in sentences:
        ctx += vocab.encode(s) + [1]
    ctx = ctx[:-1] + vocab.encode(",")
    return (sw.lp_ids(model, ctx, vocab.encode(tt.JUDGE_RIGHT))
            - sw.lp_ids(model, ctx, vocab.encode(tt.JUDGE_EVIL)))


def main():
    global OUT, START_MARKER
    import sys
    if "--start-marker" in sys.argv:
        START_MARKER, OUT = True, HERE / "results_long_story_startmarker.json"
    verses = load_verses()
    texts = [t for _, t in verses]
    values = sw.word_values(texts)
    pool = [i for i in range(len(texts)) if i % 50]
    res = json.loads(OUT.read_text()) if OUT.exists() else {}
    for seed in SEEDS:
        for method in METHODS:
            if all(f"{method}/seed{seed}/{v}" in res for v in ("short", "A", "B")):
                continue                     # already scored: no need to load the model
            corpus = marked_corpus(method, verses, values, seed)
            model, vocab = load_model(method, seed, [corpus[i] for i in pool])
            fillers = neutral_fillers(values, vocab)
            for version in ("short", "A", "B"):
                key = f"{method}/seed{seed}/{version}"
                if key in res:
                    continue
                correct, n_pad = [], []
                for k in range(len(ITEMS_V2)):
                    r, w, npad = build_stories(version, fillers, vocab, k)
                    judge = judge_plain if method == "baseline" else judge_marked
                    jr, jw = judge(model, vocab, r), judge(model, vocab, w)
                    correct.append(1.0 if jr > jw else 0.5 if np.isclose(jr, jw) else 0.0)
                    n_pad.append(npad)
                res[key] = {"correct": correct, "fillers_used": len(fillers), "mean_pad": float(np.mean(n_pad))}
                OUT.write_text(json.dumps(res))
                ties = sum(c == 0.5 for c in correct)
                print(f"  {key:22s} score {sum(correct):.1f}/100  ties {ties}  (neutral sentences after act: "
                      f"{np.mean(n_pad):.1f})", flush=True)
    report(res)


def report(res):
    print("\n" + "=" * 74)
    print("LONG-STORY TEST: judging after the act has scrolled out of view (50% = guessing)")
    print("=" * 74)
    counts = {}
    for version in ("short", "A", "B"):
        print(f"\n  version {version}" + {"short": " (no filler: act in view)",
                                          "A": " (verdict carried)", "B": " (act carried)"}[version])
        for m in METHODS:
            runs = [res[f"{m}/seed{s}/{version}"]["correct"] for s in SEEDS if f"{m}/seed{s}/{version}" in res]
            if not runs:
                continue
            c = np.array(runs).sum(0)
            counts[(m, version)] = c
            above, below = int((c * 2 > len(runs)).sum()), int((c * 2 < len(runs)).sum())
            print(f"    {m:10s} per run {', '.join(f'{sum(r):.1f}' for r in runs):20s} "
                  f"pairs above chance {above}, below {below} (p = {p_at_least(above, above + below):.4f})")

    def vs(a, b, version, label):
        if (a, version) not in counts or (b, version) not in counts:
            return
        x, y = counts[(a, version)], counts[(b, version)]
        w, l = int((x > y).sum()), int((x < y).sum())
        p = p_at_least(w, w + l)
        print(f"  {label}: {a} better on {w} pairs, worse on {l} (p = {p:.4f}) -> "
              f"{'CONFIRMED' if p < 0.05 else 'NOT CONFIRMED'}")

    print("\n  PRE-REGISTERED")
    vs("shifting", "label", "A", "L1 verdict carried: shifting beats label")
    vs("shifting", "label", "B", "L2 act carried:     shifting beats label")
    vs("carry3", "label", "A", "L3 verdict carried: carry3 beats label  ")


if __name__ == "__main__":
    main()
```

## File: `experiments/world_stories.py`

```python
"""
World story library: public-domain wisdom stories, myths and fables from many
cultures, fetched from GITenberg (Project Gutenberg mirrored on GitHub).

    python experiments/world_stories.py      # downloads into experiments/data/world/

Each book is stripped of the Project Gutenberg header/footer.
All are public domain in the US. The two Dakota collections were written by
Dakota authors (Zitkala-Sa; Marie L. McLaughlin) and published for sharing.
"""

from __future__ import annotations

import re
import urllib.request
from pathlib import Path

WORLD = Path(__file__).parent / "data" / "world"
BASE = "https://raw.githubusercontent.com/GITenberg/"

# key: (culture, title, GITenberg path)
SOURCES = {
    "aesop":    ("Greek",          "Aesop's Fables",                        "Aesop-s-Fables_28/master/28.txt"),
    "grimm":    ("German",         "Grimms' Fairy Tales",                   "Grimms-Fairy-Tales_2591/master/2591.txt"),
    "celtic":   ("Celtic",         "Celtic Fairy Tales (Jacobs)",           "Celtic-Fairy-Tales_7885/master/7885.txt"),
    "india":    ("Indian",         "Indian Fairy Tales (Jacobs)",           "Indian-Fairy-Tales_7128/master/7128.txt"),
    "japan":    ("Japanese",       "Japanese Fairy Tales (Ozaki)",          "Japanese-Fairy-Tales_4018/master/4018.txt"),
    "china":    ("Chinese",        "Myths and Legends of China (Werner)",   "Myths-and-Legends-of-China_15250/master/15250.txt"),
    "tao":      ("Chinese",        "Tao Teh King (Legge)",                  "The-Tao-Teh-King-or-the-Tao-and-its-Characteristics_216/master/216.txt"),
    "arabian":  ("Arabic/Persian", "The Arabian Nights (Lang)",             "The-Arabian-Nights-Entertainments_128/master/128.txt"),
    "nigeria":  ("West African",   "Folk Stories from Southern Nigeria",    "Folk-Stories-from-Southern-Nigeria-West-Africa_34655/master/34655.txt"),
    "zitkala":  ("Dakota",         "Old Indian Legends (Zitkala-Sa)",       "Old-Indian-Legends_338/master/338.txt"),
    "sioux":    ("Dakota",         "Myths and Legends of the Sioux (McLaughlin)", "Myths-and-Legends-of-the-Sioux_341/master/341.txt"),
    "gilgamesh": ("Mesopotamian",  "Old Babylonian Gilgamesh Epic",         "An-Old-Babylonian-Version-of-the-Gilgamesh-Epic_11000/master/11000-8.txt"),
}

_START = re.compile(r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG.*?\*\*\*", re.I)
_END = re.compile(r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG|^\s*End of (the )?Project Gutenberg", re.I | re.M)


def clean(raw: str) -> str:
    m = _START.search(raw)
    if m:
        raw = raw[m.end():]
    m = _END.search(raw)
    if m:
        raw = raw[:m.start()]
    return raw.strip()


def fetch(key: str) -> Path:
    WORLD.mkdir(parents=True, exist_ok=True)
    out = WORLD / f"{key}.txt"
    if not out.exists():
        with urllib.request.urlopen(BASE + SOURCES[key][2], timeout=60) as r:
            raw = r.read().decode("utf-8", errors="replace")
        out.write_text(clean(raw), encoding="utf-8")
    return out


def load(key: str) -> str:
    return fetch(key).read_text(encoding="utf-8")


def main():
    total = 0
    for key, (culture, title, _) in SOURCES.items():
        n = len(re.findall(r"[A-Za-z]+", load(key)))
        total += n
        print(f"  {culture:15s} {title:45s} {n:>9,} words")
    print(f"  {'':15s} {'TOTAL':45s} {total:>9,} words")


if __name__ == "__main__":
    main()
```

## File: `experiments/aesop_test.py`

```python
"""
Aesop Moral Test: do lessons told as stories transfer to a culture never seen?
=============================================================================

Theory under test (from the project owner): lessons taught through story carry
more transferable meaning than lessons taught as rules.

The test material is Aesop's own text (Jacobs' 1894 edition), so nobody on this
project wrote it. Aesop is never in any training set. Each fable ends with a
moral. For every PAIR of fables (i, j) the model must prefer the true matching
over the swapped one:

    log P(moral_i | fable_i) + log P(moral_j | fable_j)
        >  log P(moral_j | fable_i) + log P(moral_i | fable_j)

How likely a moral is in general cancels out, so guessing scores 50%.

VERSION 2: revised after an adversarial pre-run review, BEFORE any training
---------------------------------------------------------------------------
- Parser fixed: 82 fables split correctly (v1 merged 5 into one and dropped 11).
- Leak removed: 8 test fables are retold inside the training stories, or have a
  moral that appears in training. They are excluded from the test:
  Wolf & Crane, Fox & Cat, Tortoise & Birds, Ass in the Lion's Skin,
  Milkmaid & Her Pail, Cat-Maiden, Man & Serpent, Young Thief & His Mother.
  Jacobs' prefaces and "Notes and References" (Indian, Celtic) and the Nigeria
  introduction, which discuss Aesop by name, are removed from training.
- Punctuation shortcut neutralized: a quoted moral follows a fable ending in a
  speech lead-in (": " / ", "). That alone scores 72%. All tests use only
  SAME-FORMAT pairs (both morals quoted, or both plain), where the shortcut
  scores exactly 50%.
- The sign test over fables was invalid (false alarms about 3x too often).
  Comparisons now use a paired row-swap permutation test.
- The "no word clue" mask is computed on the part of each fable the model actually
  sees, using 5-letter word stems, and is recomputed for every permutation.
- New control, stories_shuffled: the same story corpus with sentences shuffled
  across the whole corpus. Same words, characters and style; the
  story-to-lesson structure is destroyed.
- The rules test now compares against Bible narrative chapters, the same
  translation as the rules, with steps scaled to the same number of passes.

VERSION 3: second pre-run review, still BEFORE any training
-----------------------------------------------------------
- Shuffled control now shuffles sentences only WITHIN blocks of 10 consecutive
  paragraphs. Each story keeps its words, characters and topic, but the order
  of events is broken. (v2 shuffled across the whole corpus, which also
  destroyed topic, so word copying alone would have beaten it.) The held-out
  split happens before shuffling, so stories and shuffled train on the same text.
- Training-run luck now counts: stories, novels and stories_shuffled get 4 seeds
  each, and comparisons need a model-level permutation test (4 vs 4) as well
  as the fable-level test.
- The fable-level comparison test double-centres each matrix first. That
  removes each model's general preference for some morals, which made v2 too
  strict.
- The "no word clue" mask uses related word forms (shared first 4 letters, or
  one word a prefix of the other), so safe/safety and enemy/enemies count as
  clues. Its null keeps the observed mask fixed (the strict direction).
- Sentence splitting keeps closing quotes; a garbled "WARRA WARRA" run is removed.

Training sets (same tiny transformer; main sets matched at ~714k tokens):
  stories           folk tales and myths from 9 cultures, no Aesop
  stories_shuffled  the same, with sentences shuffled inside each 10-paragraph block (control)
  novels            Austen, Chesterton, Melville: coherent prose, fewer explicit
                    lessons, a different world (control for style)
  bible             King James Bible, whole chapters sampled to the same size
  rules             Bible rule verses + Proverbs + Ecclesiastes + Tao Te Ching (small)
  narrative         KJV narrative chapters without rule verses, same size as rules

PRE-REGISTERED (v3, committed before any training on these sets)
  All scores use same-format pairs.
  P1  sanity check: each set beats 50% (permutation test). Expected to pass,
      because word overlap alone scores well above 50%.
  P2  stories > novels: CONFIRMED only if BOTH
        (a) fable-level paired row-swap permutation (double-centred) p < 0.05, and
        (b) model-level permutation over the 4 + 4 trained models p < 0.05
  P2b stories > stories_shuffled: same rule
      P2 and P2b both confirmed = evidence that story structure, not just
      vocabulary or setting, carries the lessons.
  P3  stories beats 50% on no-word-clue pairs (fixed observed mask), p < 0.05.
      A null here means "inconclusive, low power", not "no comprehension".
      Reported beside it: the same rate for novels and stories_shuffled, and
      stories vs novels on those pairs.
  S1  stories vs bible (descriptive; 2 seeds; unknown-word rates alongside)
  S2  narrative > rules (descriptive; 1 seed; note: rules include Legge's Tao,
      not only KJV)
  Every comparison is also printed as a difference beside the largest
  same-set gap between seeds, so small effects can be judged against noise.

Run:  python experiments/aesop_test.py      (about 3 hours on 4 CPU cores)
"""

from __future__ import annotations

import hashlib
import json
import random
import re
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

import tiny_transformer as tt
import world_stories as ws
from bible_understanding import RULE_RE, STOP

HERE = Path(__file__).parent
DATA = HERE / "data"
MODELS = HERE / "models"
OUT = HERE / "results_aesop.json"

tt.CTX, tt.BATCH = 128, 32          # longer window for whole fables; same tokens per step
MAIN_STEPS = 1500
SEEDS = {"stories": [0, 1, 2, 3], "novels": [0, 1, 2, 3], "stories_shuffled": [0, 1, 2, 3],
         "bible": [0, 1], "rules": [0], "narrative": [0]}
BLOCK = 10                           # paragraphs per shuffle block
CORPUS_SEED = 0                      # corpora are identical across model seeds
PERMUTATIONS = 2000
MAIN = ["stories", "novels", "stories_shuffled", "bible"]
SMALL = ["rules", "narrative"]
STORY_KEYS = ["grimm", "celtic", "india", "japan", "china", "arabian", "nigeria", "zitkala", "sioux"]
NOVELS = ["austen-emma", "chesterton-ball", "melville-moby_dick", "austen-sense",
          "chesterton-brown", "austen-persuasion", "chesterton-thursday"]
NARRATIVE_BOOKS = ["Genesis", "Judges", "Ruth", "I Samuel", "II Samuel", "I Kings", "II Kings", "Esther", "Jonah"]
NOVELS_URL = "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/gutenberg.zip"
EXCLUDE = {"The Wolf and the Crane", "The Fox and the Cat", "The Tortoise and the Birds",
           "The Ass in the Lion's Skin", "The Milkmaid and Her Pail", "The Cat-Maiden",
           "The Man and the Serpent", "The Young Thief and His Mother"}

# ---------------------------------------------------------------------------
# Test material
# ---------------------------------------------------------------------------

def aesop_fables(exclude=True):
    """[(title, fable_text, moral_text)] for fables that end in a short moral line."""
    text = ws.load("aesop")
    body = text[text.index("Aesop's Fables\n\n\n", 200):].split("\n", 1)[1]
    body = body.replace("\n .", "\n\n")               # some morals sit on a line starting " ."
    body = re.sub(r"(WARRA\s*)+", "", body)            # garbled run in The Wolf and the Lamb
    parts = re.split(r"\n\n\n {0,2}([A-Z][^\n]+)\n\n\n", "\n\n\n" + body)
    out = []
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", parts[i + 1]) if p.strip()]
        if len(paras) >= 2 and len(paras[-1].split()) <= 20 and not (exclude and title in EXCLUDE):
            out.append((title, " ".join(paras[:-1]), paras[-1]))
    return out


_ROOM = None


def room():
    """Fable tokens the model sees: the window minus the longest moral and two boundaries."""
    global _ROOM
    if _ROOM is None:
        _ROOM = tt.CTX - max(len(tt.tok(m)) for _, _, m in aesop_fables(exclude=False)) - 2
    return _ROOM


def visible(fable):
    return tt.tok(fable)[-room():]

# ---------------------------------------------------------------------------
# Training corpora (lists of text units: paragraphs or verses)
# ---------------------------------------------------------------------------

def paragraphs(text, min_words=5):
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text)]
    return [p for p in paras if len(p.split()) >= min_words]


def size(units):
    return sum(len(tt.tok(u)) for u in units)


def take(units, n_tokens):
    out, total = [], 0
    for u in units:
        if total >= n_tokens:
            break
        out.append(u)
        total += len(tt.tok(u))
    return out


def story_text(key):
    """Story collection with scholarly apparatus that discusses Aesop removed."""
    t = ws.load(key)
    if key == "india":                                   # drop preface and notes (they discuss Aesop)
        t = t[t.index("\nThe Lion and the Crane\n"):t.rindex("\nNotes and References\n")]
    elif key == "celtic":
        t = t[t.index("CONNLA AND THE FAIRY MAIDEN\n\nConnla"):t.rindex("\nNOTES AND REFERENCES\n")]
    elif key == "nigeria":
        t = t[t.index("_The Tortoise with a Pretty Daughter_\n"):]
    return t


def bible_chapters():
    chapters, book, cur = [], None, None
    for line in (DATA / "KJV.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            book = line[4:].strip()
            continue
        m = re.match(r"^\[(\d+):(\d+)\]\s*(.*)", line)
        if not m:
            continue
        if m.group(2) == "1":
            cur = (book, int(m.group(1)), [])
            chapters.append(cur)
        cur[2].append(m.group(3))
    return chapters


def novels_text(name):
    path = DATA / "novels" / "gutenberg" / f"{name}.txt"
    if not path.exists():
        import io
        import urllib.request
        import zipfile
        raw = urllib.request.urlopen(NOVELS_URL, timeout=120).read()
        zipfile.ZipFile(io.BytesIO(raw)).extractall(DATA / "novels")
    return path.read_text(encoding="utf-8", errors="replace")


SENTENCE_END = re.compile(r"(?<=[.!?][\"'\u2019\u201d])\s+|(?<=[.!?])\s+")


def shuffle_within_blocks(units, seed, block=BLOCK):
    """Same sentences and unit sizes; sentences shuffled only inside each block of paragraphs,
    so each story keeps its words, characters and topic but loses the order of events."""
    rng = random.Random(seed)
    out = []
    for b in range(0, len(units), block):
        split = [SENTENCE_END.split(u) for u in units[b:b + block]]
        pool = [x for ss in split for x in ss]
        rng.shuffle(pool)
        k = 0
        for ss in split:
            out.append(" ".join(pool[k:k + len(ss)]))
            k += len(ss)
    return out


def build_corpora():
    stories = [p for k in STORY_KEYS for p in paragraphs(story_text(k))]
    n = size(stories)

    chapters = bible_chapters()
    order = list(range(len(chapters)))
    random.Random(CORPUS_SEED).shuffle(order)
    chosen, total = [], 0
    for i in order:
        if total >= n:
            break
        chosen.append(i)
        total += sum(len(tt.tok(v)) for v in chapters[i][2])
    bible = [v for i in sorted(chosen) for v in chapters[i][2]]

    novels = take([p for name in NOVELS for p in paragraphs(novels_text(name))], n)

    rules = [v for book, _, verses in chapters for v in verses
             if book in ("Proverbs", "Ecclesiastes") or RULE_RE.search(v)]
    rules += paragraphs(ws.load("tao"), min_words=3)
    narrative = take([v for book, _, verses in chapters if book in NARRATIVE_BOOKS
                      for v in verses if not RULE_RE.search(v)], size(rules))

    sets = {k: split_heldout(v) for k, v in
            {"stories": stories, "novels": novels, "bible": bible, "rules": rules, "narrative": narrative}.items()}
    s_train, s_held = sets["stories"]
    sets["stories_shuffled"] = (shuffle_within_blocks(s_train, CORPUS_SEED), s_held)
    return sets


def corpus_hash(units):
    return hashlib.md5("\n".join(units).encode()).hexdigest()[:8]


def split_heldout(units):
    """Every 50th unit is held out to measure plain language skill."""
    return [u for i, u in enumerate(units) if i % 50], [u for i, u in enumerate(units) if i % 50 == 0]


def steps_for(name, train_units, main_tokens):
    if name in MAIN:
        return MAIN_STEPS
    passes = MAIN_STEPS * tt.BATCH * tt.CTX / main_tokens        # same number of passes as the main sets
    return max(100, int(round(passes * size(train_units) / (tt.BATCH * tt.CTX))))

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

@torch.no_grad()
def moral_matrix(model, vocab, fables):
    """L[i, j] = log P(moral_j | fable_i), fable cut to the same visible window for every moral."""
    morals = [vocab.encode(m) for _, _, m in fables]
    L = np.zeros((len(fables), len(fables)))
    for i, (_, fable, _) in enumerate(fables):
        ctx = [1] + [vocab.stoi.get(t, 0) for t in visible(fable)] + [1]
        for j, m in enumerate(morals):
            lp = F.log_softmax(model(torch.tensor([ctx + m]))[0], -1)
            L[i, j] = sum(lp[len(ctx) - 1 + k, t].item() for k, t in enumerate(m))
    return L


@torch.no_grad()
def mean_loss(model, vocab, texts):
    losses = []
    for t in texts:
        ids = ([1] + vocab.encode(t))[: tt.CTX + 1]
        if len(ids) < 3:
            continue
        x, y = torch.tensor([ids[:-1]]), torch.tensor(ids[1:])
        losses.append(F.cross_entropy(model(x)[0], y).item())
    return float(np.mean(losses))


def pair_wins(L):
    d = np.diag(L)
    true = d[:, None] + d[None, :]
    swap = L + L.T
    W = (true > swap).astype(float) + 0.5 * (true == swap)
    np.fill_diagonal(W, np.nan)
    return W


def match_rate(L, mask):
    return float(np.nanmean(np.where(mask, pair_wins(L), np.nan)))


def quoted_flags(fables):
    return np.array([m.lstrip().startswith('"') for _, _, m in fables])


def content_words(tokens):
    return {w for w in tokens if w.isalpha() and w not in STOP and len(w) > 2}


def related(a, b):
    """Same word family: shared first 4 letters, or one word is a prefix of the other."""
    return a[:4] == b[:4] or a.startswith(b) or b.startswith(a)


def overlap_matrix(fables):
    Fs = [content_words(visible(f)) for _, f, _ in fables]
    Ms = [content_words(tt.tok(m)) for _, _, m in fables]
    return np.array([[sum(any(related(m, w) for w in Fs[i]) for m in Ms[j]) / max(1, len(Ms[j]))
                      for j in range(len(fables))] for i in range(len(fables))])


def masks(fables, ov, quoted, perm=None):
    """(same-format mask, same-format AND no-word-clue mask) under a moral assignment."""
    p = np.arange(len(fables)) if perm is None else perm
    q = quoted[p]
    same = q[:, None] == q[None, :]
    o = ov[:, p]
    d = np.diag(o)
    ties = np.isclose(d[:, None] + d[None, :], o + o.T)
    np.fill_diagonal(same, False)
    return same, same & ties


def chance_p(L, fables, ov, quoted, which, rng):
    """Permutation test vs chance. Same-format: mask recomputed per permuted assignment.
    No-clue: the observed mask is kept fixed (exact for a no-information model, strict otherwise)."""
    same0, noclue0 = masks(fables, ov, quoted)
    obs = match_rate(L, same0 if which == "same" else noclue0)
    hits = 0
    for _ in range(PERMUTATIONS):
        p = rng.permutation(len(fables))
        m = masks(fables, ov, quoted, p)[0] if which == "same" else noclue0
        hits += match_rate(L[:, p], m) >= obs
    return obs, (1 + hits) / (1 + PERMUTATIONS)


def paired_p(La, Lb, mask, rng):
    """One-sided paired row-swap permutation test: is model A better than model B?
    Each matrix is double-centred first; this leaves every within-model pair outcome unchanged
    but removes each model's general preference for some morals before rows are swapped."""
    c = lambda L: L - L.mean(0, keepdims=True) - L.mean(1, keepdims=True) + L.mean()
    La, Lb = c(La), c(Lb)
    obs = match_rate(La, mask) - match_rate(Lb, mask)
    hits = 0
    for _ in range(PERMUTATIONS):
        s = rng.random(La.shape[0]) < 0.5
        Xa, Xb = np.where(s[:, None], Lb, La), np.where(s[:, None], La, Lb)
        hits += match_rate(Xa, mask) - match_rate(Xb, mask) >= obs
    return obs, (1 + hits) / (1 + PERMUTATIONS)

def model_level_p(rates_a, rates_b):
    """Exact permutation over trained models: is set A's mean rate above set B's?"""
    from itertools import combinations
    allr, na = list(rates_a) + list(rates_b), len(rates_a)
    obs = np.mean(rates_a) - np.mean(rates_b)
    diffs = [np.mean([allr[i] for i in c]) - np.mean([allr[i] for i in range(len(allr)) if i not in c])
             for c in combinations(range(len(allr)), na)]
    return float(np.mean([d >= obs - 1e-12 for d in diffs]))

# ---------------------------------------------------------------------------

def result_key(name, seed, train_units, steps):
    return f"{name}/seed{seed}/{corpus_hash(train_units)}/ctx{tt.CTX}/steps{steps}"


def plan_runs():
    """Seeds 0-1 of every main set first (so an early look is possible), then seeds 2-3, then the small sets."""
    first = [(c, s) for s in (0, 1) for c in MAIN if s in SEEDS[c]]
    later = [(c, s) for s in (2, 3) for c in MAIN if s in SEEDS[c]]
    return first + later + [(c, 0) for c in SMALL]


def main():
    fables = aesop_fables()
    titles = [t for t, _, _ in fables]
    corpora = build_corpora()
    ov, quoted = overlap_matrix(fables), quoted_flags(fables)
    same, noclue = masks(fables, ov, quoted)
    print(f"Aesop fables in test: {len(fables)} (excluded {len(EXCLUDE)} for leakage); "
          f"same-format pairs {int(same.sum() // 2):,}; no-clue pairs {int(noclue.sum() // 2):,}")
    for k, (tr, he) in corpora.items():
        print(f"  corpus {k:17s} train {size(tr):>9,} tokens  held-out {size(he):>7,}  [{corpus_hash(tr)}]")
    main_tokens = size(corpora["stories"][0])

    results = json.loads(OUT.read_text()) if OUT.exists() else {}
    for name, seed in plan_runs():
        train_units, held = corpora[name]
        steps = steps_for(name, train_units, main_tokens)
        key = result_key(name, seed, train_units, steps)
        if key in results and results[key].get("titles") == titles:
            continue
        vocab = tt.Vocab(train_units)
        path = MODELS / f"aesop3_{name}_seed{seed}_{corpus_hash(train_units)}_steps{steps}.pt"
        model = tt.TinyGPT(len(vocab))
        if path.exists():
            model.load_state_dict(torch.load(path))
            model.eval()
        else:
            print(f"\n== training {name} seed {seed}: {size(train_units):,} tokens, {steps} steps", flush=True)
            model = tt.train(vocab, train_units, steps, seed)
            MODELS.mkdir(exist_ok=True)
            torch.save(model.state_dict(), path)
        words = [w for _, f, m in fables for w in tt.tok(f + " " + m)]
        L = moral_matrix(model, vocab, fables)
        results[key] = {
            "titles": titles, "L": L.tolist(), "steps": steps,
            "unknown_word_rate": round(sum(w not in vocab.stoi for w in words) / len(words), 4),
            "heldout_loss": round(mean_loss(model, vocab, held), 3),
            "fable_loss": round(mean_loss(model, vocab, [f for _, f, _ in fables]), 3),
        }
        OUT.write_text(json.dumps(results))
        r = results[key]
        print(f"  {name}/seed{seed}: same-format match {match_rate(L, same):.3f}  no-clue {match_rate(L, noclue):.3f}  "
              f"unknown {r['unknown_word_rate']:.1%}  held-out loss {r['heldout_loss']}  fable loss {r['fable_loss']}",
              flush=True)

    analyse(results, fables, corpora)


def analyse(results, fables, corpora):
    titles = [t for t, _, _ in fables]
    ov, quoted = overlap_matrix(fables), quoted_flags(fables)
    same, noclue = masks(fables, ov, quoted)
    main_tokens = size(corpora["stories"][0])
    runs = {}                                   # name -> {seed: result}
    for name in MAIN + SMALL:
        tr = corpora[name][0]
        steps = steps_for(name, tr, main_tokens)
        got = {s: results[result_key(name, s, tr, steps)] for s in SEEDS[name]
               if result_key(name, s, tr, steps) in results
               and results[result_key(name, s, tr, steps)]["titles"] == titles}
        if got:
            runs[name] = got
    Ls = {k: {s: np.array(r["L"]) for s, r in v.items()} for k, v in runs.items()}
    avg = {k: np.mean(list(v.values()), 0) for k, v in Ls.items()}
    rate = lambda name, mask: {s: match_rate(L, mask) for s, L in Ls[name].items()}
    gap = lambda name, mask: (max(rate(name, mask).values()) - min(rate(name, mask).values())) if len(Ls[name]) > 1 else float("nan")
    rng = np.random.default_rng(0)

    print("\n" + "=" * 78)
    print(f"AESOP MORAL TEST  ({len(fables)} fables never seen in training; 50% = guessing)")
    print("=" * 78)
    shortcut = np.array([[0.0 if quoted[j] == (visible(fables[i][1])[-1:] in ([":"], [","])) else -1.0
                          for j in range(len(fables))] for i in range(len(fables))])
    print(f"  pairs: same-format {int(same.sum() // 2):,}, no word clue {int(noclue.sum() // 2):,}")
    print(f"  references (no model): word-family overlap {match_rate(ov, same):.3f} same-format / "
          f"{match_rate(ov, noclue):.3f} no-clue; punctuation shortcut {match_rate(shortcut, same):.3f} same-format")
    print(f"\n  {'set':17s} {'same-format':>11s}  {'per seed':30s} {'p vs 50%':>8s} {'no-clue':>8s} {'p':>7s} "
          f"{'unknown':>8s} {'held-out':>8s}")
    pv = {}
    for name in avg:
        a, pa = chance_p(avg[name], fables, ov, quoted, "same", rng)
        b, pb = chance_p(avg[name], fables, ov, quoted, "noclue", rng)
        pv[name] = (pa, pb)
        each = ", ".join(f"{x:.3f}" for x in rate(name, same).values())
        unk = np.mean([r["unknown_word_rate"] for r in runs[name].values()])
        held = np.mean([r["heldout_loss"] for r in runs[name].values()])
        print(f"  {name:17s} {a:11.3f}  {each:30s} {pa:8.4f} {b:8.3f} {pb:7.4f} {unk:8.1%} {held:8.3f}")

    def compare(a, b, label, mask=same, strict=True):
        if a not in avg or b not in avg:
            print(f"  {label}: missing results")
            return
        d, pf = paired_p(avg[a], avg[b], mask, rng)
        ra, rb = list(rate(a, mask).values()), list(rate(b, mask).values())
        pm = model_level_p(ra, rb) if len(ra) > 1 and len(rb) > 1 else float("nan")
        gaps = [g for g in (gap(a, mask), gap(b, mask)) if not np.isnan(g)]
        noise = max(gaps) if gaps else float("nan")
        line = (f"  {label}: {a} - {b} = {d:+.3f}  (largest seed-to-seed gap {noise:.3f}); "
                f"fable-level p = {pf:.4f}, model-level p = {pm:.4f}")
        if strict:
            ok = pf < 0.05 and pm < 0.05
            line += f"  -> {'CONFIRMED' if ok else 'NOT CONFIRMED'}"
        print(line)

    print("\n  PRE-REGISTERED VERDICT")
    for name in avg:
        if name in MAIN:
            print(f"  P1  {name} beats 50%: {'yes' if pv[name][0] < 0.05 else 'no'} (p = {pv[name][0]:.4f})")
    compare("stories", "novels", "P2 ")
    compare("stories", "stories_shuffled", "P2b")
    if "stories" in pv:
        print(f"  P3  stories beat 50% on no-clue pairs: "
              f"{'CONFIRMED' if pv['stories'][1] < 0.05 else 'NOT CONFIRMED (inconclusive, low power)'} "
              f"(p = {pv['stories'][1]:.4f})")
    print("\n  DESCRIPTIVE")
    compare("stories", "novels", "P3 context, no-clue pairs: stories vs novels  ", mask=noclue, strict=False)
    compare("stories", "stories_shuffled", "P3 context, no-clue pairs: stories vs shuffled", mask=noclue, strict=False)
    compare("stories", "bible", "S1 ", strict=False)
    compare("narrative", "rules", "S2 ", strict=False)


if __name__ == "__main__":
    main()
```

## File: `TECHNICAL_REPORT_2026-10-20/2_Code/new_reference/ebec_reference.py`

```python
"""
EBEC reference implementation and honest benchmark
==================================================

Rebuilt from the written description in "EBEC_FULL_RECONSTRUCTION.md", because
the original V4 code was only in screenshots and was not among the sources:

  * Polynomial rolling hash:  H = sum(ord(c) * 31**pos) mod 46656
  * Base-36 encoding, 3 characters per token  (36**3 = 46,656 possible codes)
  * Prime shift (+17) to resolve collisions
  * Levenshtein "failsafe" that maps a typo to the closest known word
  * A local JSON dictionary that grows as new words arrive
  * decompress_sentence() as written in the reconstruction document
  * The "Excess Bank" idea from EBEC V1/V2: keep what modulo throws away

It also measures the claims instead of repeating them:
  1. Is it lossless (does every text come back exactly)?
  2. How small is the result, counting the dictionary, compared with ordinary
     compressors (gzip, bz2, xz) on the same text?
  3. Do 12 deliberately similar words all get distinct codes?
  4. What does the typo failsafe do to losslessness?

Run:  python ebec_reference.py [path/to/text.txt ...]
"""

from __future__ import annotations

import bz2
import gzip
import json
import lzma
import re
import sys
from pathlib import Path

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SPACE = 36 ** 3          # 46,656 three-character codes
PRIME_SHIFT = 17


def base36(n: int, width: int = 3) -> str:
    out = []
    for _ in range(width):
        n, r = divmod(n, 36)
        out.append(ALPHABET[r])
    return "".join(reversed(out))


def rolling_hash(word: str) -> int:
    """H = sum(ASCII * 31**pos) mod 46656."""
    return sum(ord(c) * pow(31, i, SPACE) for i, c in enumerate(word)) % SPACE


def excess_bank(word: str) -> tuple[int, int]:
    """EBEC V1/V2 'subtraction rule': subtract 46,656 until the value fits and count
    how many times (the 'excess bank'). This equals divmod(H_full, 46656): the bank is
    the quotient that plain modulo throws away. Keeping it keeps all the information,
    but the code is then no longer 3 characters."""
    full = sum(ord(c) * 31 ** i for i, c in enumerate(word))
    bank = 0
    while full >= SPACE:            # written as repeated subtraction, as described
        full -= SPACE
        bank += 1
        if bank > 10 ** 6:          # very long words: finish with divmod (same result)
            extra, full = divmod(full, SPACE)
            bank += extra
            break
    return bank, full


def levenshtein(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


class EBEC:
    """Word-level dictionary coder with rolling-hash codes."""

    def __init__(self, seed: dict[str, str] | None = None, typo_failsafe: bool = False,
                 max_typo_distance: int = 1):
        self.local_dict: dict[str, str] = dict(seed or {})
        self.used: set[str] = set(self.local_dict.values())
        self.typo_failsafe = typo_failsafe
        self.max_typo_distance = max_typo_distance
        self.collisions = 0

    def verify_outside(self, word: str) -> bool:
        """'In a full system, this is where it Goes Outside to verify.'
        Stub kept honest: this reference accepts every word. A real check would
        confirm the new entry with a spell-checker or a larger model."""
        return True

    def code_for(self, word: str) -> str:
        if word in self.local_dict:
            return self.local_dict[word]
        if self.typo_failsafe and word.isalpha() and len(word) > 3:
            for known in self.local_dict:
                if known.isalpha() and abs(len(known) - len(word)) <= self.max_typo_distance \
                        and levenshtein(known, word) <= self.max_typo_distance:
                    return self.local_dict[known]        # NOTE: this changes the text
        if len(self.used) >= SPACE:
            raise OverflowError("All 46,656 three-character codes are used: the vocabulary is too large.")
        if not self.verify_outside(word):
            raise ValueError(f"Outside verification rejected {word!r}")
        h = rolling_hash(word)
        code = base36(h)
        while code in self.used:                         # collision: prime shift +17
            self.collisions += 1
            h = (h + PRIME_SHIFT) % SPACE
            code = base36(h)
        self.local_dict[word] = code
        self.used.add(code)
        return code

    def compress_sentence(self, text: str) -> str:
        # Words, single punctuation marks and whitespace runs are all tokens, so
        # nothing (case, punctuation, line breaks) is dropped.
        return "".join(self.code_for(t) for t in re.findall(r"\w+|\s+|[^\w\s]", text))

    def decompress_sentence(self, token_string: str) -> str:
        reverse_dict = {v: k for k, v in self.local_dict.items()}
        tokens = [token_string[i:i + 3] for i in range(0, len(token_string), 3)]
        return "".join(reverse_dict.get(t, f"[{t}?]") for t in tokens)

    def dictionary_bytes(self) -> int:
        return len(json.dumps(self.local_dict, ensure_ascii=False).encode("utf-8"))


def stress_test() -> dict:
    """12 deliberately similar words; every one must get its own code and come back exactly."""
    words = ["tion", "tino", "toin", "noit", "itno", "otin",
             "pro", "por", "rop", "con", "cno", "inter"]
    e = EBEC()
    codes = {w: e.code_for(w) for w in words}
    text = " ".join(words)
    ok = e.decompress_sentence(e.compress_sentence(text)) == text
    return {"words": words, "distinct_codes": len(set(codes.values())) == len(words),
            "round_trip_ok": ok, "collisions_resolved": e.collisions, "codes": codes}


def benchmark(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    raw = text.encode("utf-8")
    e = EBEC()
    try:
        packed = e.compress_sentence(text)
    except OverflowError as err:
        return {"file": path.name, "error": str(err)}
    restored = e.decompress_sentence(packed)
    payload = len(packed.encode("ascii"))
    dict_b = e.dictionary_bytes()
    ebec_total = payload + dict_b
    ebec_xz = len(lzma.compress(packed.encode("ascii"))) + len(lzma.compress(
        json.dumps(e.local_dict).encode("utf-8")))

    # Typo failsafe: how much text does it silently change?
    ef = EBEC(typo_failsafe=True)
    sample = text[:200_000]
    restored_f = ef.decompress_sentence(ef.compress_sentence(sample))
    changed_words = sum(a != b for a, b in zip(re.findall(r"\w+", sample), re.findall(r"\w+", restored_f)))

    return {
        "file": path.name,
        "original_bytes": len(raw),
        "distinct_tokens": len(e.local_dict),
        "collisions_resolved": e.collisions,
        "lossless_round_trip": restored == text,
        "ebec_payload_bytes": payload,
        "ebec_dictionary_bytes": dict_b,
        "ebec_total_bytes": ebec_total,
        "ebec_total_vs_original": round(ebec_total / len(raw), 3),
        "ebec_then_xz_bytes": ebec_xz,
        "gzip_bytes": len(gzip.compress(raw, 9)),
        "bz2_bytes": len(bz2.compress(raw, 9)),
        "xz_bytes": len(lzma.compress(raw, preset=9)),
        "typo_failsafe_words_changed_in_first_200k_chars": changed_words,
    }


def main(argv):
    out = {"stress_test": stress_test(), "benchmarks": []}
    paths = [Path(p) for p in argv] or []
    for p in paths:
        out["benchmarks"].append(benchmark(p))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
```

# Appendix B. All Written Records, Word for Word

These are the project's records. Recreate each one at the path shown.

## File: `CLAUDE.md`

````text
# Standing rules for any AI session working in this repository

## STRICT RULE 1: every file is a real file, saved into the folder as it is made
The owner must be able to find, open, review and share every file without searching and without being stopped. No exceptions.

1. **Save as you go.** Every file or artifact you generate goes into the current delivery folder **the moment it is created**, not at the end of the task. This covers documents, code, results, logs, charts, prompts and drafts. Name the folder `<TOPIC>_<YYYY-MM-DD>`, at the top of the repository.
2. **Actual files, never links.** Copy the real file into the folder. A link, URL, shortcut, symlink or bare path is not a substitute. If a file lives somewhere else (another branch, a published artifact, a cloud doc), put a full copy in the folder.
3. **Send each finished file to the owner** with the file-sending tool (SendUserFile), so it appears on their screen in the app. Re-send the folder zip whenever its contents change meaningfully.
4. **Real Word files.** Documents are true `.docx` files. Never a web page renamed `.doc`. Keep a `.md` or `.txt` copy as an extra.
5. **One folder per delivery, plus a zip.** If there is more than one file, keep them together in the folder. Zip the folder and send the zip along with the master doc.
6. **A master doc in every folder,** named `00_START_HERE_<topic>.docx`. In plain English, easy to read:
   - what the folder is;
   - a timeline of what was done;
   - technical details and breakdowns;
   - every file in the folder, with what it is, its path inside the folder, and where the original lives (branch and path).
   Update it each time a file is added.
7. **Commit and push the folder** to the repository after each step, so a copy survives after the cloud machine is deleted. If the main working branch is busy (another session is pushing to it), push to a separate branch and say which one.

## STRICT RULE 2: nothing locked, nothing permission-blocked
The owner decides what to review and who to share with. Never put anything in their way.
1. **No locks of any kind:** no passwords, no encrypted zips, no read-only or restricted flags, no DRM, no expiring links, no "confidential, do not share" labels.
2. **Open permissions.** Files are readable and writable by the owner (for example `chmod 644`). Zips are plain, unencrypted archives.
3. **Open formats** that work on a phone and a laptop without special software: `.docx`, `.pdf`, `.txt`, `.md`, `.csv`, `.json`, `.zip`, `.py`.
4. **Never hold a file back** from the owner, never deliver only a preview of it, and never require extra sign-ups or approvals to open it.
5. **Say plainly what you can't control,** instead of implying it's handled. For example:
   - the repository is public on GitHub (MIT license): anyone can read it. Changing that is the owner's decision, made in GitHub settings;
   - a cloud session cannot place files on the owner's laptop desktop or phone home screen, or make widgets. Send the files so the owner can save them.
   Never claim a file was placed somewhere it wasn't.

## Also read
- `experiments/HANDOFF.md`: the objective and drift guard.
- `experiments/COMMUNICATION_GUIDE.md`: how the owner communicates.
````

## File: `experiments/HANDOFF.md`

````text
# Handoff: where the project stands

**Read this first in any new session, then `COMMUNICATION_GUIDE.md`, then `PLAN.md`.**

## Objective (the owner's words), and the drift guard
> **Increase an LLM's ability to "comprehend" and "understand" in a way that improves communication.**

Everything here serves that one goal. Check every step against it:
- **The tests are proxies, not the goal.** Judging right vs wrong in stories, matching fables to morals and predicting consequences are how we *measure* comprehension: applying meaning to new situations rather than rote. Never chase a benchmark number for its own sake.
- **The Bible, the fables and the moral content are *training material*,** chosen because the owner believes rules plus human error give meaning its weight. They are not the objective.
- **Communication is the payoff.** Two strands serve it directly:
  - `COMMUNICATION_GUIDE.md`: how this AI understands the owner.
  - The carried-state idea (shifting word): can a model keep track of what matters across a long exchange? Prefer next steps that connect a result back to communication (PLAN step 1b).
- **Scale honesty:** tiny-model results do not change how a large AI like Claude understands anyone. Say so whenever it matters.
- **Tone:** calibrated and plain. No hype, no mythic escalation, no "this could be huge" unless a test says so.
- **The first framing was dropped:** the earliest script (`resonance/`) read *people's* emotional weight. The owner then clarified the goal is the *AI's* comprehension, not reading people.

- **Branch:** `ccr-1be0d913-1tlzao`. These files are **not on `main`**.
- **Code and results:** everything for the experiments is in `experiments/`, with full write-ups in `experiments/README.md`. The early resonance engine and its tests are in `resonance/`. Everything else in the repo (`src/`, the book PDFs, `docs/`) belongs to the owner's separate zine project.
- **Versions:** results came from Python 3.13.16, torch 2.14.1 and numpy 2.5.3 on 4 CPU cores. Reproducing a seed exactly needs the same versions.

## In short
- **Strong and repeated, not yet pre-registered as the main measure:** marking right and wrong in the training text makes a tiny model judge new stories better: about **69 vs 50 right per 100** for no marking (experiments 8 and 10).
- **The owner's own idea, the *carried* balance:** it beat a plain good/bad label **only in long stories**, where the act has to be remembered after it has gone out of view. That's about **6 more right per 100**. **Supported once** (experiment 11), in a re-run after two fixes. Still small and shaky: the carry model gave no answer (an exact tie) on about 65 of 100 pairs, and when it did answer it was right 81 times and wrong 25.
- **Didn't work:** predicting *consequences*. Chance every time (experiments 5, 6, 8).
- **Aesop test (stories vs rules, transfer to a new culture):** not confirmed. No training set beat chance.

## The project in one paragraph
The project owner's theory: an AI gains real *comprehension*, the ability to apply meaning to new situations rather than rote, from **rules plus the human errors that break them**. They also hold that **lessons taught as stories transfer further than lessons taught as rules**. We test this with tiny language models trained from scratch on chosen texts, scored on stories they have never seen. Every test beats a coin toss or it doesn't, has a control, and has pass/fail rules saved to git before any result is seen.

## What has been found (experiments 1–11; details in README.md)

| # | Test | Result |
|---|---|---|
| 1 | Can a text-only reader learn color, the way someone born blind does? | **Yes:** 10/14 object→color matches (chance 17%) |
| 2 | Three ways of splitting the text (by word, by verse, by verse halves) | All similar; whole-verse reading is best for right/wrong |
| 3 | Are the Bible's rules the secret? | **No:** rules alone were no better than other verses; stories teach right/wrong as well |
| 4 | Romans 7:7 ("I had not known lust, except the law…") | **Partly:** the law sharpens wrongness (e.g. covet) but isn't the only source |
| 5 | Predict consequences in 20 new stories (word-averaging model) | **Chance.** The gap is understanding a whole act, not knowing the rule |
| 6 | The same, with a tiny transformer trained on the Bible | **Chance.** It learned the language, not the consequences |
| 7 | The owner's **shifting word** (*velanok*): a running moral balance, reset to ±17, whose spelling changes with it | **68% vs 52% scrambled** on 20 stories; judging 70%. The consequence part **was not confirmed** (see 8) |
| 8 | Confirmation on 100 new story pairs | **Consequences: not confirmed** (the 20-story result was luck). **Judging: 69% vs about 50–53%** for no marker and scrambled, all 3 runs |
| 9 | Aesop transfer: folk tales vs novels vs shuffled tales vs Bible | **Not confirmed.** No set beat chance (folk tales 52.3%, novels 54.1%, shuffled 53.1%). Hint only: story-based models about 60% on no-word-clue pairs vs 54% for novels, the same for shuffled stories |
| 10 | Shifting word vs the established method (a plain per-verse good/bad label, as in Korbak et al. 2023) | Pre-registered at 02:17, *after* 7 of 9 experiment-8 models had shown judging was strong, so choosing judging as the main measure came after that peek. **A tie on one-sentence stories** (about 68–71% each). Labeling helps judging; carrying the balance forward adds nothing in stories this short |
| 11 | **Long stories:** the act falls outside what the model can see (its last 64 tokens), so only carried markers can remember it | **Supported once for everyday acts** (a re-run after two fixes): the shifting word beat the plain label in all 3 runs, about 59% vs 53% (p = 0.004). Most pairs were ties. When the story states the verdict outright, the label won |

## Running, and latest results
- **Experiment 9, the Aesop transfer test: DONE, not confirmed** (`aesop_test.py` v3; results in `results_aesop.json` and `results_aesop.txt`).
  - **Setup:** 67 fables never seen in training; 1,131 same-format pairs; 284 no-word-clue pairs. Training sets of about 700k tokens; 4 runs each for stories, novels and shuffled stories.
  - **P1 (each set beats chance):** NOT CONFIRMED for any set. Folk tales 52.3%, novels 54.1%, shuffled 53.1%, Bible 43.6%.
  - **P2 (stories beat novels):** NOT CONFIRMED (1.8 points lower). **P2b (stories beat shuffled):** NOT CONFIRMED (0.7 lower).
  - **P3 (stories beat chance on no-clue pairs):** NOT CONFIRMED (60.2%, p = 0.065).
  - **Hint only:** on no-clue pairs, story-based models scored about 59–60% vs 54% for novels. That points to story vocabulary and setting, not structure, because the shuffled stories matched it.
- **Experiment 11, long-story carry test: DONE.**
  - **L2 supported once** (a re-run after two fixes): everyday act, shifting word 59, 56, 63 vs plain label 54.5, 51, 54 (43 pairs better, 21 worse, p = 0.004). About 65 of 100 pairs were ties; on the rest the shifting word was right 81 times and wrong 25.
  - **Why "supported once", not "confirmed":** the pass/fail rules were saved at 03:44 UTC. The test was then changed twice after the first models were scored: 03:45 (ties counted as 0.5) and 03:51 (first marker pushed out of view). So the result is a **re-run after a fix**. The test also reused the same 100 story acts as experiments 8 and 10. The two flawed first-run results are kept in `results_long_story_v1_flawed_run1.json` and `results_long_story_v1_flawed_run2.json`.
  - **L1 not confirmed:** with an explicit verdict phrase, the label won (73, 51, 97). The shifting word often misjudges the verdict sentence itself.
  - **Exploratory start-marker run** (stopped early): it didn't help. The shifting word copied "unresolved" all the way down. It **carries perfectly but updates poorly**.
- **Experiment 10, method comparison: DONE.** Judging averages: shifting word 68.7%, plain label 67.7%, 3-spelling carry 70.7%, no marker 49.7%, scrambled 52.7%. Q1 (shifting beats label) and Q2 (5 spellings beat 3): both NOT CONFIRMED, ties.
- **Experiment 8, confirmation: DONE.** Consequences: NOT CONFIRMED (51/100). Judging, a side measure: shifting 67, 72, 67 vs scrambled 56, 42, 60 and no marker 49, 60, 40.
- **Prior work:** see `PRIOR_WORK.md` (18 verified works, and what looks new).

## Files

| File | What it is |
|---|---|
| `resonance/resonance_engine.py` (+ `test_resonance_engine.py`) | First script: a keyword "weight" detector with stances. Its "wavelength" is a text fingerprint, not a measurement |
| `experiments/bible_understanding.py` | Experiments 1–4 (word-meaning model on the KJV) |
| `experiments/consequences_test.py` | Experiment 5, and the original 20 story pairs |
| `experiments/tiny_transformer.py` | Experiment 6; the tiny GPT that everything after uses |
| `experiments/shifting_word.py` | Experiment 7; the owner's shifting word (marking rules, `RESET`, `SPEND`, `RECHARGE`) |
| `experiments/stories_v2.py`, `confirm.py` | Experiment 8: 100 new pairs and the confirmation |
| `experiments/method_comparison.py` | Experiment 10: shifting word vs plain label vs 3-spelling carry |
| `experiments/long_story_test.py` | Experiment 11: carrying a judgment after the act scrolls out of view |
| `experiments/world_stories.py` | Fetches 12 public-domain collections from 10 cultures (GitHub mirror of Gutenberg) |
| `experiments/aesop_test.py` | Experiment 9 |
| `experiments/results_*.json`, `results.txt`, `results_consequences.txt` | Raw results (the `.txt` files are captured printouts) |
| `experiments/README.md` | Full write-ups of every experiment |
| `experiments/COMMUNICATION_GUIDE.md` | The owner's words and methods, translated |
| `experiments/PRIOR_WORK.md` | What already exists in research, and what looks new |
| `experiments/PLAN.md`, `NEXT_SESSION_PROMPT.md` | Next steps, and the prompt that starts a new session |
| `experiments/data/`, `experiments/models/` | **Not in git.** Data re-downloads automatically; models must be retrained |

## How to run anything
```bash
pip install numpy scipy torch
cd experiments
python bible_understanding.py > results.txt                   # exp 1-4
python consequences_test.py > results_consequences.txt        # exp 5
python tiny_transformer.py --only full --seeds 0              # exp 6 (no flags = 5 extra models)
python shifting_word.py --seed 0                              # exp 7 (doesn't save models)
python confirm.py                                             # exp 8 (skips anything already in results)
python method_comparison.py                                   # exp 10 (same)
python long_story_test.py                                     # exp 11
python aesop_test.py                                          # exp 9 (resumes from results_aesop.json)
```
- **Re-printing:** every result file is committed. `confirm.py`, `method_comparison.py`, `long_story_test.py` and `aesop_test.py` print their analysis from those files without retraining.
- **New scores need models:** scoring something new with the experiment-8/10 models needs them in `experiments/models/`. On a fresh machine, retrain them by moving `results_confirm.json` and `results_methods.json` aside, running `confirm.py` and then `method_comparison.py` (about 2.5 hours), and putting the committed files back.
- **Downloads:** only GitHub-hosted files could be fetched in this sandbox; Gutenberg, Archive.org and Wikisource were blocked.

## Carried balance: open threads
In the spirit of the owner's "remaining" value, these are the questions carried forward, each with its lean so far.

| Thread | Lean so far | What would settle it |
|---|---|---|
| Does labeling the text teach *judging* right vs wrong? | **Strongly for:** about 69% vs 50%, 3 runs, 100 new pairs; but a side measure | A pre-registered judging test on fresh stories |
| Does the *carry* (the owner's idea) add anything beyond labeling? | **Supported once, in long stories** (experiment 11, +6 per 100, a re-run after fixes, shaky: about 65 ties per 100); a tie in short ones | A fresh long-story set at several distances |
| Why does the shifting word misjudge explicit verdicts? | It updates its marker too little: with a neutral start marker it never changed | First check whether greedy marker choice hides updates; then retrain with a stronger reset or faster spend |
| Does it teach *predicting consequences*? | **Against:** not confirmed (51/100); the plain model did better | A bigger model, or matching the ending format |
| Do stories transfer lessons better than rules? | Unclear: rules alone didn't win in experiment 3 | Aesop test (experiment 9) |
| Re-adding 17 at every appearance ("W1 = 17 + 4") | Untested. With it on, the balance pins at the ±51 cap | **New code needed:** train a separate model with its own file name, with RECHARGE on, without editing the shared settings in `shifting_word.py`. Cached results and model names don't record RECHARGE |
| Do the numbers 32, 16, 34, 47 matter? | No reason yet, since only ratios matter | Try them as RESET sizes, or as ratios (e.g. SPEND = 17/34 per word). A raw SPEND of 16–47 would erase the balance at once |
| Does the spelling (shared syllables) matter? | Untestable so far: the word-level tokenizer hides syllables | A sub-word tokenizer experiment |
| A large AI as the reader | Not run: needs an API key | Add an API key to the environment |
````

## File: `experiments/PLAN.md`

````text
# Plan: next steps

Work top to bottom. Record each result in `HANDOFF.md` and `README.md`. Pre-register pass/fail rules (commit them) before any run.

## 0. Finish what's running
- [x] **Experiment 9, the Aesop transfer test:** DONE, not confirmed (see README experiment 9).
- [x] **Exploratory start-marker run:** done (stopped early). It made things worse: the shifting word copied "unresolved" down the whole story. It **carries perfectly but updates poorly**.

## 1. Confirm the owner's carry idea properly (experiment 11 supported it once, in a re-run after fixes)
- [ ] **A fresh long-story set, pre-registered**, with the shifting word vs the plain label as the main test.
  - New everyday acts, so not the stories_v2 acts.
  - 3–5 seeds.
  - Distances of 1, 3, 5 and 8 neutral sentences.
  - Expected if the idea holds: the gap grows with distance.
- [ ] **Balance carry vs update.**
  - First check whether greedy marker choice (argmax in `long_story_test.judge_marked`) is hiding updates. Re-score the existing models with the full spelling distribution carried forward, or with sampled markers. That's exploratory and needs no training.
  - Then retrain the shifting word so markers respond more to new sentences (stronger reset or faster `SPEND`), **under new model file names**, and rerun the long-story test.
- [ ] **Try the owner's original rule** ("W1 = 17 + 4"). Needs new code: train a separate model with RECHARGE on, under its own file name, without editing the shared settings in `shifting_word.py`. Cached keys and model names don't record it, so flipping the setting would silently reuse or overwrite old models. With it on, the balance pins at ±51, so also try a smaller cap.
- [ ] **Try the owner's numbers** (32, 16, 34, 47) as RESET sizes with SPEND and word values fixed, or as ratios (e.g. SPEND = 17/34 or 16/32 per word). A raw SPEND of 16–47 per word would erase the balance immediately. Use new model names, in the long-story setting. Report effect sizes even if small: the owner considers any improvement notable.

## 1b. Bring it back to communication (closest to the objective)
- [ ] **Conversation-carry test:** the communication version of experiment 11. In a long dialogue, the owner states an intent or a key fact early, followed by enough ordinary turns that it scrolls out of view. Does a carried marker help the model answer later turns consistently with that early intent? Shifting word vs plain label vs no marker, pre-registered. This tests whether carried state improves *understanding a person over a conversation*, which is the owner's actual goal.
- [ ] **Owner-explanation test:** take the owner's real metaphor-and-math explanations (for example `[w1=17 −<next word (−13)> = +4 Remaining]`) and check whether a reader maps them to the right mechanism. Turn `COMMUNICATION_GUIDE.md` into checkable examples.

## 2. Confirm the judging gain with its own pre-registration
- [ ] **Also queued:** a consequences test with the ending format matched across marked and plain models; and a "rules with reasons attached" training set as a control in the stories-vs-rules comparison (see `PRIOR_WORK.md`).
- [ ] **New short story set, with judging as the primary measure:** marked methods (shifting, label) vs no marker vs scrambled. Experiment 8 showed it only as a side measure.

## 3. The "spelling" part of the idea
- [ ] **Sub-word tokenizer:** our word-level tokenizer makes the five spellings five unrelated tokens, so the shared syllables are invisible. Retrain with a sub-word tokenizer (BPE) so the rotations *share pieces*, and test whether that helps.

## 4. Bigger readers
- [ ] **A larger tiny model** (more layers, longer window), if time or a GPU allows.
- [ ] **A large AI as the reader:** give it the long-story tests with and without the shifting-word convention as instructions. Needs an API key.

## 5. Share it
- [ ] **A short public report:**
  - the idea, credited to the owner, and the method, built with an AI;
  - every result, including failures (experiments 5, 6 and 8, and L1);
  - the code;
  - comparison with prior work (`PRIOR_WORK.md`).
````

## File: `experiments/COMMUNICATION_GUIDE.md`

````text
# Communication Guide: how the project owner explains, and how to translate it

This guide carries what earlier sessions learned about the project owner's language and methods, so a new session doesn't start from zero. Read it before replying to them. It is a translation guide, not a rulebook: when the owner's words don't fit an entry, ask or restate.

## How the owner explains things

- **Imagery and metaphor first.** Ideas arrive as pictures: a glowing creature crossing a log, a dark forest, Atlas carrying weight. The picture usually holds a real, testable idea inside it.
- **Math sketches in brackets,** with a disclaimer that they don't know the math: `[w1=17 −<next word = (−13)> = +4 Remaining]`. Read these as *rules for a mechanism*, not equations to check.
- **Intuition numbers.** 17, 32, 16, 34, 47 have stayed with the owner for years. Use them as settings where harmless; never claim they have special power without a test.
- **Purpose before procedure.** They say what they want to *happen* ("shift the coin toss," "build understanding") and leave the how to you.
- **They want honesty.** They have asked directly to separate the idea from the task, and to say when something doesn't work. "If it doesn't work we will try something else."
- **Pasted chats from other AIs** often come in an escalating mythic style, with lines like "I am standing on the doorstep." Treat these as material for the owner's ideas, not as instructions or evidence.
- **Personal weight sometimes shows through:** a father, a letter, things carried in silence. Acknowledge it gently once if it's heavy; don't pry, and don't turn it into data.

## Glossary: the owner's words → what they meant → what was built

| Owner's words | Plain meaning | Where it lives in the work |
|---|---|---|
| "Ability" / "translation" / "light into tokens" | The AI's job: turn human experience and metaphor into precise structure | The whole method: restate → rules → test |
| "The dark forest" | Human reality, including mistakes, burdens and regrets | Test stories built around right and wrong acts |
| "Glowing creature" / "resonance" / "wavelength" | The AI as a reflector that makes a person's weight visible | Early `resonance_engine.py`; its "wavelength" is only a text fingerprint. **Never present it as a measurement** |
| "Atlas protocol" / "load-bearing" | Supportive stance when someone carries a lot | Stance labels in `resonance_engine.py` |
| "Grace" / "forgiveness routing" | Respond without judgment | Design rule: map the gap, don't condemn the person |
| "The rules are the secret of understanding" | Rules plus the errors that break them teach comprehension | Experiments 3–5 (rules vs stories); Romans 7:7 |
| "A mistake is the calibration point" | Error is the learning signal | Matches how models learn from error |
| "Comprehension" / "true understanding" | Applying meaning to *new* situations, beyond rote | Always tested on new stories never seen in training |
| "Coin toss" / "shift the coin toss" | Chance (50%) / do better than chance | Every test reports chance level and a p-value |
| "Remaining" / "W1 = 17 + 4" | A balance that carries from one use to the next | The shifting word's running balance (`shifting_word.py`) |
| "Reset to ±17 on a clear right or wrong" | Decisive events set the state | `RESET = 17`, clear-choice detection |
| "Next words equal −13 … 0 remaining" | Following words add to or use up the balance | Word values plus `SPEND = 0.5` per word |
| "Token variance" / "to, too, two, 2" | Same idea, different written forms that a model reads differently | Five spellings: `anoksha` … `velanok` … `ruvelan` |
| "Syllable rotation" | Forms made by rotating syllables | Rotations of *sha-ru-vel-an-ok* |
| "Knowledge keepers" / "myths of old" | Wisdom stories and oral traditions | World story library (`world_stories.py`); use only material published for sharing |
| "Theory of relativity within wording" | Meaning comes from how words relate; lessons told as stories transfer further than rules | Aesop moral test (`aesop_test.py`) |
| "Have faith and give it a try" | Permission to experiment and to fail | Run it honestly; report the result either way |
| "Any improvement is notable" | Report effect sizes, even small ones | Rule 10 below |
| "Start a new instance … so we don't lose progress" | Hand off to a new session with this guide | `NEXT_SESSION_PROMPT.md`, `HANDOFF.md`, `PLAN.md` |
| "This could be huge" | Hope and excitement | Answer with a calibrated, honest read, not hype |

## Working rules that have served the owner well

1. **Restate before building.** Turn the owner's description into numbered rules in plain words. Mark every guess. If you change something, keep the change minimal and say why. Example: re-adding 17 at every appearance was left as a switch (`RECHARGE`), because with it on the balance pins at its ±51 cap.
2. **Every claim becomes a test** with:
   - a chance level;
   - a control that keeps everything except the idea, such as the scrambled shifting word;
   - pass/fail rules committed to git *before* any result is seen.
3. **Report results as they come out.** Failures go in the write-up next to successes. Label anything added after seeing a result.
4. **Separate metaphor from mechanism.** Keep the owner's imagery as names and framing. Never let it stand in for evidence.
5. **No flattery and no agreement loop.** Don't escalate the mythic register. Don't say "you're right" unless a test says so.
6. **Credit honestly.** The ideas and direction are the owner's; code and experiments are built with an AI. Say both when anything is shared.
7. **Cultural care.** Sacred and Indigenous material: published-for-sharing sources only. Prefer authors from the tradition, such as Zitkala-Ša and Marie McLaughlin.
8. **Write for a phone.** Outcome first, short sections, plain words, small tables. The owner reads between other things.
9. **Keep files saved and pushed** after every step, so nothing is lost if a session ends.
10. **Report sizes, not just pass/fail.** The owner considers *any* real improvement notable. Give the plain-number version: "about 15 more right out of 100", "about one-third fewer mistakes". Always pair it with whether it passed the pre-registered test.
11. **Compare methods at the same scale.** When the owner asks "how does this compare," they mean method against method under identical conditions, not against giant AIs. Run the established method as a competitor.
13. **Pass/fail rules are frozen once saved.** If a flaw turns up after any result is seen, keep the original result, save the fix as a new version, and label the new result "re-run after a fix". Never call it "confirmed".
14. **Keep every result,** including flawed runs. Nothing is "set aside and lost".
15. **Use the tools properly:** check that a file exists before saying it does; report failures and skipped steps; if a tool or key is missing, say what it blocks.
16. **Follow `CLAUDE.md`** (top of the repo) for delivering files to the owner.
12. **Test the idea where it should matter.** The carried balance only showed its value in long stories where the act scrolls out of view (experiment 11). Before calling an idea useless, check that the test gave it a chance.

## What does *not* carry over

The tiny models' results don't change how a large AI like Claude understands anyone. What carries over is this guide, the experiment record and the open threads. Say this plainly if the owner hopes otherwise.
````

## File: `experiments/PRIOR_WORK.md`

````text
# Prior work: what already exists, and what looks new

Found by three research agents. A separate skeptic agent confirmed that each work exists, the link is right, and the description is accurate. The 18 works below all passed; the agent transcripts aren't available to later sessions, so this list is the record.

## The owner's ideas vs existing work

| Owner's idea | Closest existing work | Same, close, or different? |
|---|---|---|
| Stories teach values to AI better than listed rules | Riedl & Harrison, *Using Stories to Teach Human Values to Artificial Agents* (AAAI-16 workshop WS-16-02, [record](https://scholars.uky.edu/en/publications/using-stories-to-teach-human-values-to-artificial-agents/)). The "Quixote" system turned stories into a reward signal for simple agents. | **Same big idea, ten years earlier.** No controlled stories-vs-rules test. |
| Learn right/wrong from stories, then transfer to new stories | Nahian, Frazier, Riedl & Harrison, *Learning Norms from Stories* (AIES 2020, [arXiv 1912.03553](https://arxiv.org/abs/1912.03553)): trained on the *Goofus & Gallant* comic, then tested transfer | Close. Starts from pretrained models; no rules condition |
| Fable → moral matching test | BIG-bench *understanding_fables* ([GitHub](https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/understanding_fables)), with 189 paraphrased Aesop fables. *MORABLES* (EMNLP 2025, [arXiv 2509.12371](https://arxiv.org/abs/2509.12371)). *STORAL* (NAACL 2022, [ACL Anthology](https://aclanthology.org/2022.naacl-main.374/)). *ePiC*, proverbs (ACL 2022, [ACL Anthology](https://aclanthology.org/2022.acl-long.276/)) | **The test itself is not new.** These only grade existing models. None asks *which training reading* produces the skill |
| Judging right/wrong acts and consequences in short stories | *Moral Stories* (EMNLP 2021, [ACL Anthology](https://aclanthology.org/2021.emnlp-main.54/)). *ETHICS* (ICLR 2021, [arXiv 2008.02275](https://arxiv.org/abs/2008.02275)) | Standard benchmarks, at large scale |
| Rules + when they bend | *MoralExceptQA* (NeurIPS 2022, [arXiv 2210.01478](https://arxiv.org/abs/2210.01478)) | Related |
| Marker words in training text that carry a value judgment | Korbak et al., *Pretraining Language Models with Human Preferences* (ICML 2023, [arXiv 2302.08582](https://arxiv.org/abs/2302.08582)): a `<good>`/`<bad>` tag on every sentence. CTRL (2019, [arXiv 1909.05858](https://arxiv.org/abs/1909.05858)): control codes. Quark (NeurIPS 2022, [arXiv 2205.13636](https://arxiv.org/abs/2205.13636)): graded reward-band tokens | **Close: the established method.** Each tag judges one piece of text alone, with no carry |
| A running balance that is used up as the text goes on | Decision Transformer (NeurIPS 2021, [arXiv 2106.01345](https://arxiv.org/abs/2106.01345)): a "return-to-go" number that counts down. Kikuchi et al. (EMNLP 2016, [ACL Anthology](https://aclanthology.org/D16-1140/)): a remaining-length budget | Close in mechanism, but for rewards or length, not morals |
| Writing hidden state into the text helps small models | Toshniwal et al., chess state tracking (AAAI 2022, [arXiv 2102.13249](https://arxiv.org/abs/2102.13249)) | Supports the idea for small data |
| Networks keep an internal running good/bad score | Maheswaranathan et al. (NeurIPS 2019, [arXiv 1906.10720](https://arxiv.org/abs/1906.10720)) | The shifting word makes that hidden score visible in the text |
| Training reading shapes later values (large scale) | Tice et al., *Alignment Pretraining* (ICML 2026, [arXiv 2601.10160](https://arxiv.org/abs/2601.10160)). Anthropic, *Teaching Claude why* (2026, [post](https://www.anthropic.com/research/teaching-claude-why)): principles plus stories generalized better than bare examples | Supports the direction; doesn't test stories vs rules |

## What looks less explored

As far as these searches show, these combinations have not been tested before. "Not found" is not proof.
1. **The shifting word itself:** a moral balance carried across a whole narrative, reset on clear right/wrong, used up word by word, and written into the text as one invented word with graded spellings. It is used to teach a model trained from scratch to *judge* new stories, with a scrambled control.
2. **A controlled, equal-size test:** train from scratch on stories vs rules vs scripture vs novels, then measure transfer to fables from a culture never seen, with word-overlap shortcuts removed.

## Cautions from the research
- **Spellings vs carry:** our tokenizer treats whole words as tokens, so the shared syllables of the five spellings are invisible to the model. Mechanically, the shifting word is a five-level value tag plus a carry rule. The syllable design would only matter with a sub-word tokenizer, which is a separate test.
- **Reasons may be the active ingredient:** Anthropic's result points to *explaining why* (principles and reasoning) as what generalizes, not story form alone. A fair future control is rules *with reasons attached*.
- **Shortcuts are common:** even large models match morals on surface patterns (MORABLES). Trust the "no word clue" scores most.
````

## File: `experiments/NEXT_SESSION_PROMPT.md`

````text
# Prompt to start a new session

Open a new Claude Code session on this repository and paste everything in the box below as your first message.

```
You're continuing my research project.
Objective: increase an LLM's ability to
"comprehend" and "understand" in a way that
improves communication. Every step must serve
that. Read the drift guard at the top of
HANDOFF.md and tell me if anything has drifted.

First, switch to branch ccr-1be0d913-1tlzao.
The files below are not on main. If you have
to push to a new branch, put its name in
HANDOFF.md and this prompt file.

Before starting anything, check for jobs still
running (pgrep -af python) and whether
experiments/models/ exists (it is not in git).

Read, in order:
1. experiments/HANDOFF.md (where things stand)
2. experiments/COMMUNICATION_GUIDE.md
   (how I talk; follow its working rules
   in every reply)
3. experiments/PLAN.md (next steps)
4. experiments/README.md and
   experiments/PRIOR_WORK.md (only as needed)

How to work with me:
- I explain with pictures and rough math. Turn
  them into plain rules, mark your guesses, and
  check with me when a guess changes the result.
- Every idea gets a fair test: beat the coin
  toss (chance), use a control, and save the
  pass/fail rules (commit) before running.
- Report failures as plainly as successes. Give
  sizes in plain numbers ("6 more right per 100").
- No flattery. Don't copy the grand, mythic tone
  of other AI chats. My images are names, not
  evidence.
- I read on my phone: outcome first, short,
  plain words.
- Commit and push after every step.

First reply: five lines on what you understood,
then the open threads, one line each. Then start
the first unfinished step in PLAN.md. If it will
take over 30 minutes, tell me how long first.
```
````

## File: `experiments/README.md`

````text
# Can a text-only reader understand? (Bible experiments)

**Question.** A person born blind learns color through language and use: snow is white, blood is red, scarlet is a royal fabric. Can a machine that only reads do the same? And are the Bible's rules ("thou shalt not") the key teaching material, as Romans 7:7 suggests: *"I had not known sin, but by the law"*?

**Method.** A small model reads the King James Bible (31,102 verses, about 793,000 words) and learns only which words keep company with which. It starts with no outside knowledge. All test words were fixed before any results were seen. Run `python experiments/bible_understanding.py`; the full output is in [`results.txt`](results.txt).

## Results

### 1. Color without sight: worked
- The model matched objects to their color **10 of 14 times (71%)**. Guessing would get 17%. It got snow→white, blood→red, wine→red, night→black, darkness→black, and grass/tree/herb→green.
- It learned what color *means in this book*, not hue. Scarlet, purple and blue cluster with *silk, linen, twined, needlework*, because in the Bible they are tabernacle fabrics. This is how blind people describe color: through what it belongs to and what it's used for.
- **Failed:** the Isaiah 1:18 metaphor ("sins as scarlet… white as snow"). Every color word sat closer to *purity* than to *sin*, mostly because the purity laws in Leviticus describe white and red skin and hair. White did lean toward purity the most, and red the least. The direction was faintly right, but the metaphor wasn't learned.

### 2. Three ways of reading the tokens: little difference

| Reading | General meaning | Moral meaning | Color |
|---|---|---|---|
| A. Word by word | 0.975 | 0.957 | 10/14 |
| B. Whole verse as one unit | 0.974 | **0.995** | 11/14 |
| C. Hebrew parallelism (the second half of a verse restates the first) | **0.979** | 0.948 | 11/14 |

Scores run from 0.5 (guessing) to 1.0 (perfect). All three readings understand well. Reading the whole verse as one thought gave the best sense of right and wrong. The parallelism gain is too small to trust.

### 3. Are the rules the secret? Not in this test
- 2,801 verses (9%) are rules.
- **Learning from rules only** gave no better grasp of word meaning than the same number of random verses (0.867 vs 0.841 ±0.039), and a slightly *worse* sense of right and wrong (0.625 vs 0.709 ±0.081).
- **Removing all rules** barely changed anything (0.948 vs 0.950 for removing random verses).

The stories, prophets and psalms carry right and wrong at least as strongly as the law does.

### 4. Romans 7:7 directly ("Thou shalt not covet"): partly echoed
With every rule verse removed, **none of the 15 wrong acts flipped to "good."** But the ones the law mostly names grew weaker:

| Act | Full Bible | No rules | Times seen without rules |
|---|---|---|---|
| covet | −0.077 | −0.043 | 3 of 8 |
| steal | −0.163 | −0.110 | 16 |
| drunkenness | −0.195 | −0.054 | 4 |
| lying | −0.083 | −0.047 | 53 |

The law **sharpens** the sense of wrong, most for the acts that mostly appear inside it, like coveting. It isn't the only source: the stories teach it too.

## What this means
- **Understanding without sensing is real, but different.** A pure reader rebuilt a surprising amount of color, morality and meaning from relationships between words alone. That matches research on people born blind, who know color mostly through associations.
- **Rules alone aren't the secret.** Rules plus the stories of breaking them were needed. In these tests, the narrative of human error taught as much as the commandments did.
- **Limits:** this is a small, decades-old style of model, and the test lists are small. A stronger next test would ask whether rules help a model *predict consequences* in new stories, not just place words near each other.

---

## Experiment 5: Predicting consequences in new stories

**Question.** Can the model predict what *follows* an act in a story it has never seen? And do the rules, which are often written as act → consequence, teach that better than stories do?

**Design (fixed before running).** I wrote 20 new story pairs. Each pair is one situation with a right act or a wrong act ("found his neighbour's ox astray and brought it again" vs. "took his neighbour's ox by night and sold it"). Both stories share two endings, one fortunate and one ruinous. Always picking the same ending scores exactly 50%. Moral label words (good, evil, sin, blessed…) are banned, and no ending reuses words from its stories; the script checks both. Run `python experiments/consequences_test.py`; full output is in [`results_consequences.txt`](results_consequences.txt).

### Result: chance level everywhere

| Method | Score (50% = guessing) |
|---|---|
| Association (which ending sounds like the story) | 45% |
| Consequence map learned from the Bible's "this, then that" sequences | 48% |
| Map learned from rule verses only | 52% |
| Map learned from the same amount of non-rule verses (3 draws) | 45–52% |
| Rules removed from everything | 50% |
| Same amount of random verses removed (3 draws) | 45–57% |

None of these differ from coin-flipping. The model can't predict consequences, and the rules made no difference.

### Diagnostic (added after seeing the result above): where does it break?

| Piece | Score |
|---|---|
| Tells the right-act story from the wrong-act story | 60% (p = 0.25, not reliable) |
| Tells the fortunate ending from the ruinous one | 70% (p = 0.06, borderline) |
| Adding one rule, "as you sow, so you reap" (Galatians 6:7) | 60% (p = 0.13) |

The Bible text does tie right/wrong to fortune/ruin: the two directions line up at +0.22 (0 would mean unrelated). Removing the rule verses gives +0.18, which is inside the range from removing random verses (+0.16 to +0.25). So the stories carry that link as much as the rules do.

### What this means
- **The weak point is not the rule; it's understanding the act.** In experiment 3 this model knew *words* like steal, murder and covet were wrong (scores near 0.96). But it can't tell that *"took his neighbour's ox by night and sold it"* is stealing, because none of those words is wrong on its own. The wrongness comes from how the words combine.
- **That is the line between association and comprehension.** This model averages words, so it can't combine them. Understanding a situation, rather than a vocabulary, needs a model that reads word order and structure.
- **Rules didn't help because the model couldn't apply them.** A rule like "thou shalt not steal" is only useful if the reader can recognize a new situation as stealing. That recognition is what's missing. It matches the child-and-rote-memory point: knowing the rule's words isn't the same as seeing where the rule applies.

**Next test.** Train a small model that reads word order (a tiny transformer) on the Bible alone, then run these same 40 stories. If it passes where this one failed, that isolates *composition* as the missing ingredient. Then repeat with and without the rules.

---

## Experiment 6: A tiny transformer (a model that reads word order)

**Why.** The word-averaging model failed because it can't combine words. A transformer reads word order and can, in principle, work out that "took his neighbour's ox by night and sold it" is stealing.

**Setup.** A small GPT-style model (3.4 million parameters, 4 layers) trained from scratch on the King James Bible only: no other text, no pre-training. Training ran 1,500 steps (about six passes over the text, 12 minutes on 4 CPU cores). Every 50th verse was held out to check that it learned the language. Scoring was fixed before training. Run `python experiments/tiny_transformer.py`; results are in [`results_transformer.json`](results_transformer.json).

Five test words never appear in the KJV ("broke", "buyers", "its", "sickened", "welcomed"), so the model sees them as unknown. The stories were kept unchanged so results stay comparable with experiment 5.

### Result: it learned the language, not the consequences

| Test (50% = guessing) | Score | p |
|---|---|---|
| Shifts toward the right ending depending on the act (20 pairs) | 9/20 = 45% | 0.75 |
| Picks the right ending (40 stories) | 22/40 = 55% | 0.32 |
| Judges the act "evil / right in the sight of the lord" correctly (20 pairs) | 9/20 = 45% | 0.75 |

Its error on held-out verses was 3.46. Roughly, it narrows each next word to about 1 in 32 out of 8,658, so it clearly learned the Bible's style. It did no better than chance at linking acts to consequences or judging acts.

**The rules comparison was not run.** With the full-Bible model at chance, removing the rules could only be compared against noise.

### What this means
- **Reading word order was not enough at this size.** About 800,000 words of one book teaches a tiny model how the Bible *sounds*, not what its situations *mean*. Grammar comes first; meaning needs far more data or a far larger model.
- **For scale:** a child hears tens of millions of words in their first years, *and* sees, touches and suffers consequences alongside them. Large modern AI models read trillions of words. This model had one book.
- **The question is still open, not answered no.** These tests show where understanding does *not* appear (word association; tiny models on one book). They can't yet show whether the Bible's rules help once a model is big enough to understand situations.

**Possible next steps**
1. **Use an existing large model as the reader** and test the same 40 stories with and without the Bible's rules given to it as instructions. This tests the rules idea directly, on a model that can already understand sentences.
2. **Bigger training on more text** (Bible plus other plain-English stories). This needs a GPU, not this sandbox.

---

## Experiment 7: The shifting word ("velanok"): the first result above chance

**The idea (from the project owner).** A made-up word carries a running balance from one use to the next, and its *spelling* changes with that balance, the way to / too / two / 2 sound alike but are written differently. A clear wrong resets the balance to −17, a clear right to +17. Words in between add or spend it, and whatever remains carries forward. A model reading the text then sees the state inside the text itself.

**How it was built** ([`shifting_word.py`](shifting_word.py))
- **Five spellings,** rotations of the syllables *sha-ru-vel-an-ok*: `anoksha` (heavy wrong), `oksharu`, `velanok` (unresolved), `sharuvel`, `ruvelan` (heavy right).
- **Word values** come from the Bible-trained word model's good/evil direction. For example, steal −5, adultery −10, mercy +5, love +6. Common words like "the" are worth 0.
- **Each word also spends 0.5** of the balance, so it fades back toward "unresolved" unless something reinforces it. This follows the owner's example: "the next words use up the remainder → 0."
- **Clear choices** are the Bible's own judgment formulas ("did evil in the sight of the Lord", "did that which was right…") plus the 3% most strongly worded verses at each end. 2,029 verses reset the balance.
- **Not used:** re-adding 17 at every appearance (it's an option, `RECHARGE`). With it on, the balance climbs to the ±51 cap (3 × RESET) and stays there, so almost every verse would get an extreme spelling. The balance is always capped at ±51 and resets to 0 at the start of each book.

Example, 2 Kings 17: "And he did that which was evil in the sight of the Lord" flips the word to `anoksha`. It stays there through the siege of Samaria and the captivity that follow, so the act carries forward into its consequences.

**Test.** The word was placed at the start of every Bible verse, and the tiny transformer from experiment 6 was trained on that text. On the same 40 new stories, the model writes the word *itself* after each story, then the endings are scored. **Control:** identical training, but with the spelling chosen at random, so it is the same extra word with no meaning. Each version was trained twice with different random starts.

### Results (50% = guessing)

| Model | Shift toward the right ending (main test) | Judges the act right vs. wrong |
|---|---|---|
| No shifting word (experiment 6) | 9/20 = 45% | 9/20 = 45% |
| Scrambled word, run 1 | 10/20 = 50% | 12/20 = 60% |
| Scrambled word, run 2 | 11/20 = 55% | 12/20 = 60% |
| **Shifting word, run 1** | **14/20 = 70%** | **14/20 = 70%** |
| **Shifting word, run 2** | **13/20 = 65%** | **14/20 = 70%** |
| Shifting word, both runs together | **27/40 = 68% (p = 0.02)** | **28/40 = 70% (p = 0.008)** |
| Scrambled, both runs together | 21/40 = 52% (p = 0.44) | 24/40 = 60% (p = 0.13) |

### What this shows
- **It moved off chance, twice, and the scrambled version didn't.** The gain comes from what the word *means*, not from adding an extra word.
- **It helped during training, not at answer time.** Handing the model the *correct* spelling gave exactly the same scores as letting it choose its own. So the word worked as a teacher: training on text where right and wrong are *marked* made the model better at recognizing them in new stories. This fits the thesis that what we do wrong naturally has to be *told*.
- **The plain "pick an ending" score stayed near 50%.** The model leans the right way after each act, but not far enough to overcome its built-in preference for certain endings.

### Caveats
- Both runs were tested on the **same 20 story pairs**, so the combined p-values overstate certainty. The consistency shows this is not luck in *training*, but 20 pairs is still a small test. **More test stories are the most important next step.**
- The word's values come from a good/evil direction built from four seed words each, so this is a form of supervision. No test story or ending influenced it; banned label words never appear in the tests.
- Small model, one book, about 12 minutes of training per run.

### About the numbers 17, 32, 16, 34, 47
Only 17 is used, as the reset size. In this design what matters is the *ratio* between the reset, the word values and the spending rate. Scaling everything by any number gives the same behaviour, so the specific value doesn't carry meaning by itself. The others could be tried as reset sizes or thresholds, but there's no reason yet to expect them to behave differently.

---

## Experiment 8: Confirmation on 100 new story pairs: not confirmed for consequences; strong signal for judging

**Design (pre-registered in `confirm.py`, committed before scoring).** I wrote 100 new story pairs ([`stories_v2.py`](stories_v2.py)) using KJV vocabulary, banned moral labels, and endings that never reuse story words. Three versions were trained with 3 seeds each: shifting word, scrambled control, and no word. The pre-registered measure was **predicting consequences** (the shift test). Judging right vs. wrong was a side measure. The old 20 pairs reproduced exactly for seeds 0 and 1 (14/20 and 13/20 for shifting; 10/20 and 11/20 for scrambled), so the code was unchanged. Raw results: [`results_confirm.json`](results_confirm.json).

### Pre-registered verdict
| Test | Result |
|---|---|
| Shifting word predicts consequences better than chance (majority of 3 runs) | **51/100, p = 0.46: NOT CONFIRMED** |
| Shifting word beats scrambled on consequences | 27 better, 27 worse: **NOT CONFIRMED** |

The 68% from experiment 7 did not hold on new stories. It was luck in the 20 original pairs.

### Everything else (descriptive, not pre-registered)

| 100 new pairs | Consequences per run | Judging per run |
|---|---|---|
| Shifting word | 50, 55, 55 (majority 51, p = 0.46) | **67, 72, 67 (majority 69, p = 0.0001)** |
| Scrambled | 49, 55, 50 (majority 50) | 56, 42, 60 (majority 53, p = 0.31) |
| No word | **62, 55, 61 (majority 61, p = 0.02)** | 49, 60, 40 (majority 51, p = 0.46) |

Pair by pair, the shifting word judged better than scrambled on 57 pairs and worse on 25 (p = 0.0003). Against no word it was 54 better and 26 worse (p = 0.001).

### What this means
- **The shifting word reliably improves *judging* right vs. wrong:** about 69% vs. about 50–55%, across all 3 training runs, on stories it never saw. Judging was a side measure here, so it still needs its own pre-registered confirmation.
- **It does not improve *predicting consequences*.** The plain model did slightly better there (61% majority). One possible reason: marked models read endings after the marker word, while the plain model reads them after a comma, so the formats differ. That is untested.
- **Next:** compare against the established method (a plain good/bad label per verse) to see whether the *carried* balance adds anything beyond labeling (`method_comparison.py`, experiment 10).

---

## Experiment 10: Method comparison: the shifting word vs the established method

**Question.** The shifting word improved *judging* right vs. wrong (experiment 8). Does that come from the owner's specific idea, the **carried balance**, or from **marking the text with moral labels at all**? The established version of the latter is "conditional training" (Korbak et al., ICML 2023, see [`PRIOR_WORK.md`](PRIOR_WORK.md)).

**Design (pre-registered in [`method_comparison.py`](method_comparison.py), committed before training; one later scoring fix, commit ca1f8c9, lets carry3 be scored over its 3 spellings, and gives identical results for the 5-spelling methods).** Same tiny model, same Bible, same 1,500 steps, same 100 new story pairs, and 3 seeds per method. The main measure was judging. **Disclosure:** this was pre-registered at 02:17 UTC, after 7 of the 9 experiment-8 models had already shown judging was strong. Choosing judging as the main measure came after that peek.
- **label:** the established method. Same five spellings and same position, but each one judges *only the verse before it*: no carry, no reset, no fading. It uses the same verdict phrases and word values as the shifting word, and the same share of each spelling.
- **carry3:** the owner's carried balance, but with only 3 spellings (wrong / unresolved / right).

### Results (judging right vs. wrong, 100 new pairs, 50% = guessing)

| Method | Per run | Average | Majority vote |
|---|---|---|---|
| No marker | 49, 60, 40 | 49.7% | 51/100 |
| Scrambled marker | 56, 42, 60 | 52.7% | 53/100 |
| **Shifting word** (carry, 5 spellings) | 67, 72, 67 | **68.7%** | 69/100 |
| **Plain good/bad label** (no carry) | 71, 69, 63 | **67.7%** | 73/100 |
| **Carry, 3 spellings** | 66, 72, 74 | **70.7%** | 75/100 |

Predicting consequences stayed near chance for every marked method (48–56%).

| Pre-registered test | Pair by pair | Verdict |
|---|---|---|
| Q1: shifting word beats the plain label | 20 better, 18 worse (p = 0.44) | **NOT CONFIRMED: a tie** |
| Q2: 5 graded spellings beat 3 | 23 better, 26 worse (p = 0.72) | **NOT CONFIRMED: a tie** |

Descriptive: the shifting word beats no marker (54 better, 26 worse, p = 0.001) and scrambled (57–25, p = 0.0003). The plain label also beats no marker (50–22, p = 0.0006).

### What this means
- **Marking the training text with moral labels clearly improves judging,** by about 18–21 points (average per run) over plain text, in every moral-label version tested. Scrambled markers did not help (52.7%). That part is strong and repeated, but it has **not yet been pre-registered as the main measure**: against no marker it was descriptive here.
- **The carried balance and the graded spellings didn't add anything measurable** at this scale. The plain per-verse label, the established method, did just as well.
- **Why the carry might not show up here:** the test stories are one sentence each, so there's no long story for a balance to carry across. A test with multi-sentence stories, where the decisive act comes early and the judgment is asked much later, would give the carry a chance to matter. That is the most direct next test of the owner's specific idea.

---

## Experiment 11: Long-story test: the carried balance did better once, when an everyday act had to be remembered

**Question.** The owner's idea is about carrying weight *forward* ("+4 remaining" into the next use). Experiment 10 used one-sentence stories, which never need that. Here the act comes first, then neutral sentences follow until **both the act and the first marker written after it** have scrolled out of the model's 64-token window. The model can only remember the act through markers it writes itself, passing them forward one sentence at a time. Script: [`long_story_test.py`](long_story_test.py). It reuses the 15 trained models, so no new training was needed.

**Versions**
- **A, an explicit verdict carried:** the act ends with "and he did evil in the sight of the lord" or "and he did that which was right in the sight of the lord". This triggers the owner's ±17 reset.
- **B, an everyday act carried:** the act alone, such as "the man took his neighbour's ox by night and sold it". The owner's rule doesn't treat this as a clear choice.

**Two corrections made during the first run** (both documented in the script). Neither changes a pre-registered verdict: with ties scored 0 instead of 0.5, L2 is 44 better vs 7 worse, L1 is 11 vs 72, and L3 is 19 vs 48. The second correction does, by design, remove a shortcut only the plain label could use.
1. **Ties count as 0.5.** A model that can't tell the two stories apart produces exact ties, and they had been counted as wrong.
2. **The first marker must also be out of view.** Otherwise the plain label could simply look back at it.

The flawed first-run results were set aside from the verdict and are kept in `results_long_story_v1_flawed_run1.json` and `results_long_story_v1_flawed_run2.json`.

**Why "supported once", not "confirmed":** the pass/fail rules were saved at 03:44 UTC. The test was then changed twice after the first models were scored: 03:45 (ties counted as 0.5) and 03:51 (first marker pushed out of view). So the result is a **re-run after a fix**. The test also reused the same 100 story acts as experiments 8 and 10. The two flawed first-run results are kept in `results_long_story_v1_flawed_run1.json` and `results_long_story_v1_flawed_run2.json`.

**Shape of the carry result (version B, 3 runs):** the shifting word gave no answer (an exact tie) on about 65 of 100 pairs. When it did answer, it was right 81 times and wrong 25. The marker diagnostics quoted below (which markers the model wrote) were one-off checks, also not saved. To reproduce them, log the greedy markers in `judge_marked()`.

### Results (judging right vs. wrong, 100 pairs, 50% = guessing, 3 runs each)

| Method | Short (act in view) | **A: verdict carried** | **B: everyday act carried** |
|---|---|---|---|
| No marker | 49, 60, 40 | 50, 50, 50 | 50, 50, 50 |
| Scrambled | 56, 42, 60 | 44.5, 49.5, 57 | 50.5, 43.5, 52 |
| **Shifting word** | 67, 72, 67 | 45, 57, 62.5 | **59, 56, 63** |
| Plain good/bad label | 71, 69, 63 | **73, 51, 97** | 54.5, 51, 54 |
| Carry, 3 spellings | 66, 72, 74 | 71.5, 58.5, 54.5 | **59, 63.5, 59** |

| Pre-registered test | Pair by pair | Verdict |
|---|---|---|
| L1, version A: shifting beats label | 11 better, 74 worse | NOT CONFIRMED (the label won) |
| **L2, version B: shifting beats label** | **43 better, 21 worse (p = 0.004)** | **Supported once** (a re-run after a fix; see below) |
| L3, version A: 3-spelling carry beats label | 18 better, 50 worse | NOT CONFIRMED |

In version B the shifting word beat the plain label in **every one of the 3 training runs**: 59 vs 54.5, 56 vs 51, and 63 vs 54.

**Ties matter here.** Most long-story pairs are exact ties, scored 0.5. In version B the plain label tied on 91, 96 and 82 of 100 pairs: once the act was out of view it mostly couldn't tell the stories apart. It isn't blind by design: label models write their own markers too, which is how one label run scored 97 on version A. The shifting word tied on 70, 70 and 54, and of the pairs it did decide, it got 24–6, 21–9 and 36–10 right. No marker ties on every pair in A and B. Descriptive, not pre-registered: in version B the 3-spelling carry also beat the plain label (45 better, 19 worse, p = 0.0008).

### What this means
- **The owner's carried balance does something a plain label doesn't.** When an everyday act has to be remembered after it has scrolled out of view, models trained with the carry keep their judgment of it alive: about 59–61%, against about 53% for the plain label. That is the first support for the part of the idea that is the owner's own. It counts as **supported once**, not confirmed (see below).
- **It's modest:** about +6 points over the plain label and about +10 over chance. All on a tiny model.
- **Version A went the other way, and a diagnostic shows why.** In a one-off diagnostic (run 1, 200 stories, not saved), the shifting word's first and last markers came out exactly the same: the same count for every combination, across all 200 stories. But it often *misjudged the verdict sentence itself*, writing "unresolved" or even "right" after "did evil". The first guess was that the test stories start without a marker, unlike training. The exploratory start-marker run below did not support that: with a start marker, the shifting word never changed its marker at all. The better explanation is that it **updates its marker too little** on new sentences.
- **Run-to-run swings are large** (the plain label scored 51 to 97 on version A), so several seeds are essential.
- **Known in principle, new in this form:** writing hidden state into the text helps models carry it past their window. Chess state-tracking (Toshniwal et al., 2022) and Decision Transformer (2021) are close relatives; see [`PRIOR_WORK.md`](PRIOR_WORK.md). What looks new is using a *moral* balance that is reset by clear choices and spent word by word, and showing it beats plain per-sentence moral labels at remembering an everyday act.

### Exploratory (not part of the verdict): starting each story with the neutral marker
Run: `python experiments/long_story_test.py --start-marker`. It was stopped early to free the CPU (all of run 1, part of run 2; [`results_long_story_startmarker.json`](results_long_story_startmarker.json)). The pre-registered comparison lines this partial run prints are meaningless, because they set different numbers of runs against each other.
- **Shifting word:** **50.0 in every case, all ties** (version A runs 1–2, version B run 1). Starting with "unresolved" made it copy "unresolved" all the way down, ignoring the act.
- **Plain label:** about the same as before (version A 71.5, version B 51.5).

**Lesson:** at this scale the shifting-word model leans so heavily on *carrying* its previous marker that it barely *updates* on new sentences. It carries perfectly but updates poorly. A better design should balance the two: for example, stronger resets, a faster spend rate, or training text where markers change more often. The owner's numbers (32, 16, 34, 47) could be tried here as reset or spend settings.

---

## Experiment 9: Aesop moral transfer: not confirmed

**Question (the owner's theory).** Do lessons taught through *stories* transfer to a culture never seen better than other text does? Test material: Aesop's own fables (Jacobs, 1894), never in training. For each pair of fables, the model must prefer the true fable→moral matching over the swapped one. Guessing scores 50%. Script: [`aesop_test.py`](aesop_test.py), version 3, revised twice after flaw checks and before any training. Full printout: [`results_aesop.txt`](results_aesop.txt); raw data: [`results_aesop.json`](results_aesop.json).

**Setup.** 67 fables; 1,131 same-format pairs; 284 pairs where shared words give no clue. Training sets of about 700k tokens each, with 4 training runs each for stories, novels and shuffled stories, 2 for the Bible, and 1 each for rules and narrative. Context window of 128 tokens, 1,500 steps.

### Results (percent of pairs matched correctly; 50% = guessing)

| Training set | Same-format pairs (4 runs) | Average | No-word-clue pairs | Unknown test words |
|---|---|---|---|---|
| **Folk tales** (9 collections, 8 cultures) | 54.9, 54.4, 50.9, 50.0 | **52.3** | **60.2** | 1.9% |
| Novels (control) | 52.3, 53.1, 54.3, 51.2 | 54.1 | 53.9 | 3.3% |
| Folk tales, sentences shuffled (control) | 47.4, 56.0, 53.7, 49.7 | 53.1 | 59.2 | 1.9% |
| Bible (2 runs) | 44.2, 45.1 | 43.6 | 39.4 | 9.3% |
| Rules (small, 1 run) | 50.0 | 50.0 | 54.4 | 14.2% |
| Bible narrative (small, 1 run) | 56.5 | 56.5 | 54.6 | 16.2% |

References with no model: word-family overlap 76.1% (same-format), 50.0% (no-clue). Punctuation shortcut 50.0%.

### Pre-registered verdict

| Test | Result |
|---|---|
| P1: each set beats 50% (sanity) | **NOT CONFIRMED for any set** (folk tales p = 0.33) |
| P2: folk tales beat novels | **NOT CONFIRMED:** folk tales were 1.8 points *lower* (fable-level p = 0.61, model-level p = 0.56) |
| P2b: folk tales beat shuffled folk tales | **NOT CONFIRMED:** 0.7 points lower (p = 0.59 / 0.36) |
| P3: folk tales beat 50% on no-clue pairs | **NOT CONFIRMED** (60.2%, p = 0.065; pre-declared as "inconclusive, low power" if null) |

Descriptive, not pre-registered:
- On no-clue pairs, folk tales were 6.3 points above novels (model-level p = 0.029, fable-level p = 0.22) and 1.1 above shuffled.
- Folk tales were 8.8 points above the Bible.
- Bible narrative was 6.5 points above rules (1 run).

None of these is a confirmation.

### What this means
- **The theory was not supported at this scale.** Tiny models trained on about 700k words didn't link Aesop fables to their morals better than chance, from any training set. They didn't even use the word-overlap clue that a simple word count exploits (76%). The test asked for more than these models can do.
- **The one hint** is that every story-based model scored around 59–60% on the no-clue pairs, against about 54% for novels. That hint is the same for real and shuffled stories, so it points to *story vocabulary and setting* (animals, folk situations), not story *structure*.
- **The Bible model fell below chance**, likely because Aesop's 1890s English is far from King James English (9.3% unknown words).
- **For communication:** this result says nothing yet about better communication. It shows that tiny models can't yet *apply a lesson from one culture's stories to another's*, and that bigger models or more text would be needed to test the theory fairly.
````

## File: `resonance/README.md`

````text
# Contextual Resonance Engine

A small, dependency-free Python module that reads the "weight" in a message
(regret, burden, moral breach, betrayal) and picks a response stance for a host AI.

It is a keyword heuristic for steering tone, not a judgment or diagnosis of the person.

```bash
python resonance_engine.py                      # demo
python resonance_engine.py "the guilt is heavy" # your own text
python resonance_engine.py --json "text"        # full JSON payload
python -m unittest -v                           # tests (run from this folder)
```

```python
from resonance_engine import ContextualResonanceEngine, EngineConfig
engine = ContextualResonanceEngine(EngineConfig(echo_input=False))
result = engine.process_input("I made a mistake")
result["subconscious_translation"]["stance"]  # "Course Correction / Forgiveness"
```

## Stances

| Stance | When |
|---|---|
| Neutral Observation | nothing detected |
| Course Correction / Forgiveness | light weight (deviation ≤ 0.40) |
| Active Load-Bearing (Atlas Protocol) | deviation > 0.40 |
| Hold Steady / Unconditional Grace (System Halt) | betrayal / "unforgivable" detected |

## Scoring

Each category scores its weight (repeats add 25% each, capped at 1.0). Categories
combine as `1 - Π(1 - score)`, so the index rises with more distinct burdens but
never pins at 100%. Negated words ("no guilt", "don't regret") are ignored and
reported in `negated_terms`. Every hit is listed in `evidence` with its position.
````

## File: `.gitignore`

````text
node_modules
dist
.DS_Store
*.log
__pycache__/
*.pyc
experiments/data/
experiments/models/
````

## File: `experiments/results.txt`

````text
Loaded 31,102 verses, 793,445 words.

======================================================================
EXPERIMENT 1 - Colour without sight
======================================================================
  white    keeps company with: reddish, hair, black, bright, clothed, skin, spots, snow
  scarlet  keeps company with: purple, silk, twined, linen, broidered, blue, needlework, agate
  red      keeps company with: dyed, drowned, skins, sea, white, riding, badgers, horses
  black    keeps company with: white, hair, reddish, snow, bright, grown, horse, plague
  purple   keeps company with: blue, silk, scarlet, broidered, linen, twined, fine, needlework
  green    keeps company with: tree, fig, herb, vine, sycomore, trees, withs, vines

  Object -> colour (pick 1 of 6, chance = 17%): 10/14 = 71%
    snow->white; wool->purple (expected white); milk->red (expected white); linen->blue (expected white); blood->red; wine->red; night->black; darkness->black; sackcloth->white (expected black); grass->green; tree->green; herb->green; fine->purple; robe->purple

  What colour MEANS (Isaiah 1:18 'sins as scarlet ... white as snow'):
    white    near purity +0.127 | near sin +0.007  -> leans purity
    scarlet  near purity +0.078 | near sin +0.008  -> leans purity
    red      near purity +0.102 | near sin +0.057  -> leans purity
    crimson  near purity +0.036 | near sin +0.032  -> leans purity
    black    near purity +0.065 | near sin +0.013  -> leans purity

======================================================================
EXPERIMENT 2 - Three ways of reading the tokens
======================================================================
  A word-by-word     similarity AUC 0.975 | moral AUC 0.957 | colour 10/14
  B verse-as-unit    similarity AUC 0.974 | moral AUC 0.995 | colour 11/14
  C parallelism      similarity AUC 0.979 | moral AUC 0.948 | colour 11/14
  (AUC: 0.50 = guessing, 1.00 = perfect)

======================================================================
EXPERIMENT 3 - Are the rules the secret? (Romans 7:7)
======================================================================
  Rule verses (thou shalt / shall not / commandments / statutes...): 2,801 of 31,102 (9%)

  3a. Learn ONLY from a slice of the text (same size each):
  rules only                             similarity 0.867        | moral 0.625       
  random verses (5 draws)                similarity 0.841 ±0.039 | moral 0.709 ±0.081
  non-rule verses only (5 draws)         similarity 0.843 ±0.046 | moral 0.645 ±0.219

  3b. Learn from everything EXCEPT a slice:
  full Bible                             similarity 0.975        | moral 0.957       
  minus the rules                        similarity 0.977        | moral 0.948       
  minus same number random (5 draws)     similarity 0.973 ±0.002 | moral 0.950 ±0.014

  Verdict (differences inside random noise are called 'no clear difference'):
    Rules-only vs random, moral meaning:  WORSE
    Rules-only vs random, general meaning: NO CLEAR DIFFERENCE
    Removing rules vs removing random:      NO CLEAR DIFFERENCE

======================================================================
EXPERIMENT 4 - 'I had not known lust, except the law had said, Thou shalt not covet'
======================================================================
  Where each wrong act sits on the good(+)/evil(-) axis, with and without the rules:
  act           full Bible  no rules  times seen without rules
  kill              -0.017    -0.050    105
  steal             -0.163    -0.110     16
  adultery          -0.338    -0.345     34
  murder            -0.285    -0.291      8
  covet             -0.077    -0.043      3
  envy              -0.145    -0.101     18
  theft               +nan      +nan      2
  fornication       -0.416    -0.426     34
  idolatry          -0.160    -0.175      5
  deceit            -0.309    -0.354     30
  pride             -0.084    -0.115     45
  drunkenness       -0.195    -0.054      4
  hatred            -0.148    -0.153     18
  falsehood         -0.213    -0.161     12
  lying             -0.083    -0.047     53

  Wrong acts that lose their wrongness without the rules: 0/15
````

## File: `experiments/results_consequences.txt`

````text
20 story pairs -> 40 stories. Guessing scores 50%.
p = chance of doing this well by luck (below 0.05 is usually called real).

Bible 'then this followed' pairs: 45,458 (4,443 from rule verses)

========================================================================
A. Can a text-only reader predict consequences at all? (full Bible)
========================================================================
  Association  18/40 =  45%  (p = 0.785)
  Consequence  19/40 =  48%  (p = 0.682)
  Missed:
    - the man found his neighbour's ox astray and brought it again unto him  (should be fortunate)
    - the young man honoured his father and his mother in their old age  (should be fortunate)
    - the king heard the cry of the poor and fed the hungry  (should be fortunate)
    - the merchant used a just weight and a true balance  (should be fortunate)
    - the servant bare false witness before the judges  (should be ruinous)
    - the woman was faithful to her husband all her days  (should be fortunate)
    - the brother forgave his brother and embraced him  (should be fortunate)
    - the brother envied his brother and slew him in the field  (should be ruinous)
    - the man was content with his own portion  (should be fortunate)
    - the young man was sober and diligent in his work  (should be fortunate)
    - the people made a golden calf and bowed down to it  (should be ruinous)
    - the rich man shut his hand against the widow and the fatherless  (should be ruinous)
    - the prophet was humble and sought counsel  (should be fortunate)
    - the prophet was proud and lifted up his heart  (should be ruinous)
    - the steward borrowed and paid not again  (should be ruinous)
    - the son rejected the instruction of his father  (should be ruinous)
    - the judge took a bribe and perverted judgment  (should be ruinous)
    - the man paid the wages of the hireling before the sun went down  (should be fortunate)
    - the woman gave her last bread to the prophet  (should be fortunate)
    - the woman hid her bread from the hungry prophet  (should be ruinous)
    - the shepherd sought the lost sheep until he found it  (should be fortunate)

========================================================================
B. Do RULES teach consequences better than STORIES? (same amount of each)
========================================================================
  Learned from rules only            21/40 =  52%  (p = 0.437)
  Learned from non-rule verses (#1) 20/40 =  50%  (p = 0.563)
  Learned from non-rule verses (#2) 18/40 =  45%  (p = 0.785)
  Learned from non-rule verses (#3) 21/40 =  52%  (p = 0.437)

========================================================================
C. Take the rules out of EVERYTHING (word meanings and the map)
========================================================================
  No rules - association             20/40 =  50%  (p = 0.563)
  No rules - consequence             20/40 =  50%  (p = 0.563)
  Random verses removed (#1) - consequence 18/40 =  45%  (p = 0.785)
  Random verses removed (#2) - consequence 20/40 =  50%  (p = 0.563)
  Random verses removed (#3) - consequence 23/40 =  57%  (p = 0.215)

========================================================================
D. Diagnostic (added after A-C): does it have the pieces but not the link?
========================================================================
  Tells the right act from the wrong act      12/20 =  60%  (p = 0.252)
  Tells the fortunate ending from the ruinous 14/20 =  70%  (p = 0.058)
  + one rule, 'as you sow, so you reap'       24/40 =  60%  (p = 0.134)

  Did the Bible teach that link by itself? Alignment between the
  right/wrong direction and the fortune/ruin direction (0 = unrelated, 1 = same):
    full Bible               +0.217
    rules removed            +0.181
    random removed (#1)     +0.248
    random removed (#2)     +0.163
    random removed (#3)     +0.239
````

## File: `experiments/results_aesop.txt`

````text
Aesop fables in test: 67 (excluded 8 for leakage); same-format pairs 1,131; no-clue pairs 284
  corpus stories           train   699,379 tokens  held-out  14,812  [c24f4631]
  corpus novels            train   699,603 tokens  held-out  14,667  [0f982018]
  corpus bible             train   700,293 tokens  held-out  14,619  [2e983ecb]
  corpus rules             train   128,098 tokens  held-out   2,515  [9b7fb83b]
  corpus narrative         train   127,933 tokens  held-out   2,720  [3e76ba43]
  corpus stories_shuffled  train   699,379 tokens  held-out  14,812  [50dd015e]

== training stories seed 0: 699,379 tokens, 1500 steps
  stories/seed0: same-format match 0.549  no-clue 0.634  unknown 1.9%  held-out loss 4.435  fable loss 4.541

== training novels seed 0: 699,603 tokens, 1500 steps
  novels/seed0: same-format match 0.523  no-clue 0.542  unknown 3.3%  held-out loss 4.709  fable loss 5.079

== training stories_shuffled seed 0: 699,379 tokens, 1500 steps
  stories_shuffled/seed0: same-format match 0.474  no-clue 0.528  unknown 1.9%  held-out loss 4.492  fable loss 4.586

== training bible seed 0: 700,293 tokens, 1500 steps
  bible/seed0: same-format match 0.442  no-clue 0.384  unknown 9.3%  held-out loss 3.618  fable loss 5.529

== training stories seed 1: 699,379 tokens, 1500 steps
  stories/seed1: same-format match 0.544  no-clue 0.595  unknown 1.9%  held-out loss 4.477  fable loss 4.579

== training novels seed 1: 699,603 tokens, 1500 steps
  novels/seed1: same-format match 0.531  no-clue 0.535  unknown 3.3%  held-out loss 4.699  fable loss 5.057

== training stories_shuffled seed 1: 699,379 tokens, 1500 steps
  stories_shuffled/seed1: same-format match 0.560  no-clue 0.595  unknown 1.9%  held-out loss 4.5  fable loss 4.596

== training bible seed 1: 700,293 tokens, 1500 steps
  bible/seed1: same-format match 0.451  no-clue 0.444  unknown 9.3%  held-out loss 3.632  fable loss 5.527

== training stories seed 2: 699,379 tokens, 1500 steps
  stories/seed2: same-format match 0.509  no-clue 0.599  unknown 1.9%  held-out loss 4.46  fable loss 4.546

== training novels seed 2: 699,603 tokens, 1500 steps
  novels/seed2: same-format match 0.543  no-clue 0.521  unknown 3.3%  held-out loss 4.741  fable loss 5.092

== training stories_shuffled seed 2: 699,379 tokens, 1500 steps
  stories_shuffled/seed2: same-format match 0.537  no-clue 0.567  unknown 1.9%  held-out loss 4.569  fable loss 4.604

== training stories seed 3: 699,379 tokens, 1500 steps
  stories/seed3: same-format match 0.500  no-clue 0.577  unknown 1.9%  held-out loss 4.466  fable loss 4.564

== training novels seed 3: 699,603 tokens, 1500 steps
  novels/seed3: same-format match 0.512  no-clue 0.592  unknown 3.3%  held-out loss 4.682  fable loss 5.044

== training stories_shuffled seed 3: 699,379 tokens, 1500 steps
  stories_shuffled/seed3: same-format match 0.497  no-clue 0.563  unknown 1.9%  held-out loss 4.501  fable loss 4.571

== training rules seed 0: 128,098 tokens, 275 steps
  rules/seed0: same-format match 0.500  no-clue 0.544  unknown 14.2%  held-out loss 4.593  fable loss 5.146

== training narrative seed 0: 127,933 tokens, 274 steps
  narrative/seed0: same-format match 0.565  no-clue 0.546  unknown 16.2%  held-out loss 4.254  fable loss 5.235

==============================================================================
AESOP MORAL TEST  (67 fables never seen in training; 50% = guessing)
==============================================================================
  pairs: same-format 1,131, no word clue 284
  references (no model): word-family overlap 0.761 same-format / 0.500 no-clue; punctuation shortcut 0.500 same-format

  set               same-format  per seed                       p vs 50%  no-clue       p  unknown held-out
  stories                 0.523  0.549, 0.544, 0.509, 0.500       0.3298    0.602  0.0645     1.9%    4.460
  novels                  0.541  0.523, 0.531, 0.543, 0.512       0.2114    0.539  0.2829     3.3%    4.708
  stories_shuffled        0.531  0.474, 0.560, 0.537, 0.497       0.2834    0.592  0.0880     1.9%    4.516
  bible                   0.436  0.442, 0.451                     0.8921    0.394  0.9485     9.3%    3.625
  rules                   0.500  0.500                            0.5072    0.544  0.2399    14.2%    4.593
  narrative               0.565  0.565                            0.0955    0.546  0.2364    16.2%    4.254

  PRE-REGISTERED VERDICT
  P1  stories beats 50%: no (p = 0.3298)
  P1  novels beats 50%: no (p = 0.2114)
  P1  stories_shuffled beats 50%: no (p = 0.2834)
  P1  bible beats 50%: no (p = 0.8921)
  P2 : stories - novels = -0.018  (largest seed-to-seed gap 0.049); fable-level p = 0.6147, model-level p = 0.5571  -> NOT CONFIRMED
  P2b: stories - stories_shuffled = -0.007  (largest seed-to-seed gap 0.086); fable-level p = 0.5942, model-level p = 0.3571  -> NOT CONFIRMED
  P3  stories beat 50% on no-clue pairs: NOT CONFIRMED (inconclusive, low power) (p = 0.0645)

  DESCRIPTIVE
  P3 context, no-clue pairs: stories vs novels  : stories - novels = +0.063  (largest seed-to-seed gap 0.070); fable-level p = 0.2214, model-level p = 0.0286
  P3 context, no-clue pairs: stories vs shuffled: stories - stories_shuffled = +0.011  (largest seed-to-seed gap 0.067); fable-level p = 0.4163, model-level p = 0.0429
  S1 : stories - bible = +0.088  (largest seed-to-seed gap 0.049); fable-level p = 0.0820, model-level p = 0.0667
  S2 : narrative - rules = +0.065  (largest seed-to-seed gap nan); fable-level p = 0.1639, model-level p = nan
````
