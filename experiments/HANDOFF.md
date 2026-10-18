# Handoff: where the project stands

**Read this first in any new session, then `COMMUNICATION_GUIDE.md`, then `PLAN.md`.**

- **Branch:** `ccr-1be0d913-1tlzao`. These files are **not on `main`**.
- **Code and results:** everything for the experiments is in `experiments/`, with full write-ups in `experiments/README.md`. The early resonance engine and its tests are in `resonance/`. Everything else in the repo (`src/`, the book PDFs, `docs/`) belongs to the owner's separate zine project.
- **Versions:** results came from Python 3.13.16, torch 2.14.1 and numpy 2.5.3 on 4 CPU cores. Reproducing a seed exactly needs the same versions.

## In short
- **Works:** marking right and wrong in the training text makes a tiny model judge new stories better: about **69% vs about 50%** for no marking (experiments 8 and 10).
- **The owner's own idea, the *carried* balance:** it beat a plain good/bad label **only in long stories**, where the act has to be remembered after it has gone out of view. That's about **6 more right per 100**. Confirmed once (experiment 11); still small.
- **Didn't work:** predicting *consequences*. Chance every time (experiments 5, 6, 8).
- **Running at handoff:** the Aesop test (do stories teach lessons that transfer to a culture never seen?). Status is below.

## The project in one paragraph
The project owner's theory: an AI gains real *comprehension*, the ability to apply meaning to new situations rather than rote, from **rules plus the human errors that break them**. They also hold that **lessons taught as stories transfer further than lessons taught as rules**. We test this with tiny language models trained from scratch on chosen texts, scored on stories they have never seen. Every test beats a coin toss or it doesn't, has a control, and has pass/fail rules saved to git before any result is seen.

## What has been found (experiments 1–11; 9 still running; details in README.md)

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
| 9 | Aesop transfer: folk tales vs novels vs shuffled tales vs Bible | **Running** |
| 10 | Shifting word vs the established method (a plain per-verse good/bad label, as in Korbak et al. 2023) | **A tie on one-sentence stories** (about 68–71% each). Labeling helps judging; carrying the balance forward adds nothing in stories this short |
| 11 | **Long stories:** the act falls outside what the model can see (its last 64 tokens), so only carried markers can remember it | **CONFIRMED for everyday acts:** the shifting word beat the plain label in all 3 runs, about 59% vs 53% (p = 0.004). When the story states the verdict outright, the label won |

## Running, and latest results
- **Experiment 9, the Aesop transfer test** (`aesop_test.py`, version 3, after two checks for flaws before running). **RUNNING** since 03:40 UTC on 18 Oct.
  - **What it tests:** Aesop is never in training. The model must match each fable to its true moral over a swapped one.
  - **Size:** 67 fables (82 parsed; 8 excluded because versions appear in training; the rest lack a short final moral), giving 1,131 same-format pairs and 284 no-word-clue pairs.
  - **Training sets** (about 700k tokens each):
    - folk tales: 9 collections from 8 cultures, no Aesop;
    - the same tales with sentences shuffled inside each block of 10 paragraphs (control);
    - novels by Austen, Chesterton and Melville (control);
    - the Bible;
    - plus rules vs Bible narrative at small size.
  - **Runs:** 4 training runs each for stories, novels and the shuffled control; 16 models in all.
  - **Time:** about 20–30 minutes per model, roughly 6–8 hours in total.
  - **Pass/fail rules** P1, P2, P2b and P3 are in the script's docstring.
  - **Progress is saved:** each finished model's scores go into `results_aesop.json` (committed). If that file is missing, no model had finished at handoff.
  - **Before restarting**, check that it isn't already running: `pgrep -af aesop_test.py`. Two copies would both write the same file.
- **Experiment 11, long-story carry test: DONE.**
  - **L2 CONFIRMED:** everyday act, shifting word 59, 56, 63 vs plain label 54.5, 51, 54 (43 pairs better, 21 worse, p = 0.004).
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
| Does the *carry* (the owner's idea) add anything beyond labeling? | **For, in long stories** (experiment 11, L2, +6 points); a tie in short ones | A fresh long-story set at several distances |
| Why does the shifting word misjudge explicit verdicts? | It updates its marker too little: with a neutral start marker it never changed | First check whether greedy marker choice hides updates; then retrain with a stronger reset or faster spend |
| Does it teach *predicting consequences*? | **Against:** not confirmed (51/100); the plain model did better | A bigger model, or matching the ending format |
| Do stories transfer lessons better than rules? | Unclear: rules alone didn't win in experiment 3 | Aesop test (experiment 9) |
| Re-adding 17 at every appearance ("W1 = 17 + 4") | Untested. With it on, the balance pins at the ±51 cap | **New code needed:** train a separate model with its own file name, with RECHARGE on, without editing the shared settings in `shifting_word.py`. Cached results and model names don't record RECHARGE |
| Do the numbers 32, 16, 34, 47 matter? | No reason yet, since only ratios matter | Try them as RESET sizes, or as ratios (e.g. SPEND = 17/34 per word). A raw SPEND of 16–47 would erase the balance at once |
| Does the spelling (shared syllables) matter? | Untestable so far: the word-level tokenizer hides syllables | A sub-word tokenizer experiment |
| A large AI as the reader | Not run: needs an API key | Add an API key to the environment |
