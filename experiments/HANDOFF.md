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
- **Understanding as compression (experiment 12):** the better a shared model predicts, the smaller the exact seed that regrows unseen text. The tiny Bible model needed 12.2 KB for 83.8 KB of held-out verses (85.4% smaller, exact), less than half of xz. **The shifting word did not help** on this measure (pre-registered, not confirmed: about 2% larger seeds).
- **Data seed / graph method (`SEED_TEST_2026-10-20/`):** built three ways and checked. It regrows exactly but only shrinks patterned data (99.99% on a repeating pattern, 6–19% on Bible text, 0% on random data).

## The project in one paragraph
The project owner's theory: an AI gains real *comprehension*, the ability to apply meaning to new situations rather than rote, from **rules plus the human errors that break them**. They also hold that **lessons taught as stories transfer further than lessons taught as rules**. We test this with tiny language models trained from scratch on chosen texts, scored on stories they have never seen. Every test beats a coin toss or it doesn't, has a control, and has pass/fail rules saved to git before any result is seen.

## What has been found (experiments 1–12; details in README.md)

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
| 12 | **Understanding as compression:** exact seeds that regrow 623 unseen verses, from no understanding up to the tiny transformers | **Understanding shrinks the seed:** raw 8.0 → zip 2.7 → xz 2.5 → word frequencies 1.9 → word pairs 1.4 → tiny transformer 1.17 bits per character, all regrown byte for byte. **Shifting word: not confirmed** (pre-registered); every marker method gave about 2% larger seeds, and no gain on the words even with the marker free |

## Running, and latest results
- **Experiment 12, understanding as compression: DONE** (`understanding_compression.py`; results in `results_understanding.json` and `.txt`; delivery folder `GROW_UNDERSTANDING_2026-10-20/`). The ladder is confirmed: each rung of shared understanding gives a smaller exact seed. The pre-registered shifting-word question was NOT CONFIRMED (+3.45 bits per verse vs the plain model). Exact regrowth needs the identical number setup: a 1-thread decoder fails on a 2-thread seed.
  - **Queued, owner-approved (20 Oct):**
    1. **The numbers test:** the owner's numbers 17, 32, 16, 34, 47 placed where 17 sits in "W1 = 17 + 4 Remaining" (the recharge/remaining rule), singly and in sequence. Script: `numbers_test.py` (being built).
    2. **Then the "2" test:** write the remaining value into the text as a number the model can read. The tokenizer `[a-z]+|[.,;:?!]` currently drops digits, so the model has never seen the number form of the owner's rule ("to / too / two / 2").
    3. **Then the +/- agent:** classify every input as + or - information, keep the balance with the owner's rule, and report only its placement on the line, never the exact number. The owner: "dont do this step yourself but make sure it happens."
       - **The owner's scoring rule (21 Oct), in their words:** "Positive inferences in a sentence are like, you know, moral high ground, telling the truth, or, you know, highly reasonable information ... Negative would be questionable morals, nonsense, you know, misspelling, stuff like that. Should always pull a negative. There should be a negative and a positive balance. There actually should almost be more negatives than positive, because the positives are actually higher numbers when they're there, and the negatives are lower numbers, but there are more negatives ... but it does balance."
       - **In short:** many small negatives, fewer but larger positives, every input pulls a little negative, and over ordinary text the two sides balance. Keep both sides as well as the net.
       - **Not yet tested.** Today's word values are symmetric (36.0% negative vs 37.4% positive valued words in the Bible text, average sizes 2.31 vs 2.27, net almost exactly 0), so this rule is a new shape. The exact sizes are still the owner's to choose.
       - **Related:** another AI's "ComprehensionSeed" blueprint (21 Oct) has the same add/subtract living memory. Its scoring functions are undefined, so it is an outline, not running code. Keep the personal name in one of its framework names out of the repository.
  - **Untested next candidates:**
    - the owner's own "W1 = 17 + 4" recharge rule (RECHARGE was switched off), as an "excess bank";
    - markers computed from text the model can see;
    - training on stories and scoring held-out stories.
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
