# Handoff: where the project stands

**Read this first in any new session, then `COMMUNICATION_GUIDE.md`, then `PLAN.md`.**
Branch: `ccr-1be0d913-1tlzao`. All code and results are in `experiments/` (write-ups in `experiments/README.md`).

## The project in one paragraph
The project owner's theory: an AI gains real *comprehension*, the ability to apply meaning to new situations rather than rote, from **rules plus the human errors that break them**. They also hold that **lessons taught as stories transfer further than lessons taught as rules**. We test this with tiny language models trained from scratch on chosen texts, scored on stories they have never seen. Every test has a chance level, a control, and pass/fail rules committed to git before results.

## What has been found (experiments 1–7, details in README.md)

| # | Test | Result |
|---|---|---|
| 1 | Can a text-only reader learn color, the way someone born blind does? | **Yes:** 10/14 object→color matches (chance 17%) |
| 2 | Three ways of reading the tokens | All similar; whole-verse reading best for right/wrong |
| 3 | Are the Bible's rules the secret? | **No:** rules alone were no better than other verses; stories teach right/wrong as well |
| 4 | Romans 7:7 ("I had not known lust, except the law…") | **Partly:** the law sharpens wrongness (e.g. covet) but isn't the only source |
| 5 | Predict consequences in 20 new stories (word-averaging model) | **Chance.** The gap is understanding a whole act, not knowing the rule |
| 6 | Same, with a tiny transformer on the Bible | **Chance.** Learned the language, not the consequences |
| 7 | The owner's **shifting word** (*velanok*): a running moral balance, reset to ±17, spelling changes with it | **68% vs 52% scrambled** on the 20 stories. Judging right/wrong 70%. First result above chance |
| 8 | Confirmation on 100 new pairs | **Consequences: not confirmed** (the 20-story result was luck). **Judging: 69% vs ~50%** for scrambled and no marker, all 3 runs |
| 10 | Shifting word vs the established method (plain good/bad label, as in Korbak et al. 2023) | **A tie on one-sentence stories** (~68–71% each). Labeling helps judging; the carry adds nothing *there* |
| 11 | **Long stories:** the act scrolls out of view, and only carried markers can remember it | **Everyday act: shifting word beats the plain label, CONFIRMED** (59, 56, 63 vs 54.5, 51, 54; p = 0.004). With an explicit verdict phrase, the label won |

## In progress / pending (update when done)
- **Experiment 8, the confirmation on 100 new story pairs: DONE.**
  - **Consequences:** NOT CONFIRMED (shifting 51/100, p = 0.46). The plain model did slightly better (61/100).
  - **Judging right vs wrong** (side measure): shifting **67, 72, 67**, vs scrambled 56, 42, 60 and no word 49, 60, 40. Pair by pair, shifting beat scrambled 57–25 (p = 0.0003).
  - Needs its own pre-registered confirmation with judging as the main measure.
- **Experiment 10, method comparison: DONE.** Judging averages: shifting word 68.7%, plain good/bad label 67.7%, 3-spelling carry 70.7%; no marker 49.7%; scrambled 52.7%.
  - **Q1** (shifting beats plain label): NOT CONFIRMED, a tie (20–18).
  - **Q2** (5 spellings beat 3): NOT CONFIRMED, a tie.
  - **Conclusion:** labeling the text helps judging (+15–20 points); the carry and graded spellings add nothing measurable on one-sentence stories.
- **Experiment 9, the Aesop moral transfer test** (`aesop_test.py`, version 3 after two adversarial pre-run reviews). Aesop is never in training; the model must match each fable to its true moral over a swapped one.
  - Training sets: world folk tales (9 cultures); the same tales with sentences shuffled within each story (control); novels (control); the Bible. Plus rules vs Bible narrative at small size.
  - 4 seeds each for stories, novels and the shuffled control.
  - Pass/fail rules P1, P2, P2b and P3 are in the docstring. Status: **QUEUED** behind the method comparison (about 3 hours).
- **Experiment 11, the long-story carry test: DONE.**
  - **L2 CONFIRMED:** when an everyday act must be remembered after it scrolls out of view, the shifting word beats the plain label: 59, 56, 63 vs 54.5, 51, 54 (43 pairs better, 21 worse, p = 0.004).
  - **L1 not confirmed:** with an explicit verdict phrase, the plain label won (73, 51, 97). The shifting word misjudges the verdict sentence when no marker comes before it.
  - An exploratory start-marker run is in `results_long_story_startmarker.json`.
- **Prior work:** see `PRIOR_WORK.md`. 25 verified citations, and what looks new.

## Files

| File | What it is |
|---|---|
| `resonance/resonance_engine.py` | First script: keyword "weight" detector with stances. Its "wavelength" is a text fingerprint, not a measurement |
| `experiments/bible_understanding.py` | Experiments 1–4 (word-meaning model on the KJV) |
| `experiments/consequences_test.py` | Experiment 5; the original 20 story pairs |
| `experiments/tiny_transformer.py` | Experiment 6; the tiny GPT used by everything after |
| `experiments/shifting_word.py` | Experiment 7; the owner's shifting word |
| `experiments/stories_v2.py`, `confirm.py` | Experiment 8; 100 new pairs and the confirmation |
| `experiments/world_stories.py` | Fetches 12 public-domain story collections from 9 cultures (GitHub mirror of Gutenberg) |
| `experiments/aesop_test.py` | Experiment 9 |
| `experiments/results_*.json/txt` | Raw results |
| `experiments/COMMUNICATION_GUIDE.md` | The owner's words and methods, translated |
| `experiments/PRIOR_WORK.md` | What already exists in research, and what looks new |
| `experiments/method_comparison.py` | Experiment 10: shifting word vs plain good/bad label vs 3-spelling carry |
| `experiments/long_story_test.py` | Experiment 11: carrying a judgment after the act scrolls out of view |

## How to run anything
```bash
pip install numpy scipy torch          # CPU is fine; each tiny model trains ~11 min on 4 cores
python experiments/bible_understanding.py
python experiments/confirm.py          # re-uses saved models in experiments/models/ if present
python experiments/aesop_test.py        # resumes from results_aesop.json
python experiments/method_comparison.py
python experiments/long_story_test.py   # add --start-marker for the exploratory version
```
Trained models are saved in `experiments/models/` (not committed, about 15 MB each). Every result file *is* committed, so analyses can be re-printed without retraining.
Data downloads automatically on first run (KJV and world stories from raw.githubusercontent.com, novels from the NLTK data mirror). In this sandbox only GitHub-hosted files could be downloaded; Gutenberg, Archive.org and Wikisource were blocked.

## Carried balance: open threads
In the spirit of the owner's "remaining" value, these are unresolved questions carried forward. Each has a lean based on evidence so far.

| Thread | Lean so far | What would settle it |
|---|---|---|
| Does the shifting word teach *judging* right vs wrong? | **Strongly for** (69% vs ~50%, 3 runs, 100 new pairs), but a side measure | Pre-registered judging test on fresh stories |
| Is that from the *carry* (the owner's idea) or labeling in general? | On short stories, labeling in general (experiment 10, a tie). On **long stories, the carry helps: L2 CONFIRMED** (experiment 11, +6 points over the label) | Bigger models, longer stories, and fixing the first-judgment weakness |
| Does it teach *predicting consequences*? | **Against** (not confirmed, 51/100); the plain model did better | A bigger model, or matching the ending format |
| Do stories transfer lessons better than rules? | Unclear: rules alone didn't win in experiment 3 | Aesop test (experiment 9) |
| Re-adding 17 at every appearance ("W1 = 17 + 4") | Untested | Switch `RECHARGE = True` in `shifting_word.py` and rerun |
| Do the numbers 32, 16, 34, 47 matter? | No reason yet, since only ratios matter | Try as reset sizes or spend rates in the long-story test |
| Why does the shifting word misjudge an explicit verdict sentence? | Likely: test stories start without a marker, unlike training | Exploratory start-marker run, then a pre-registered fix |
| Does the spelling (shared syllables) matter? | Untestable so far: the word-level tokenizer hides syllables | Sub-word tokenizer experiment (PLAN step 3) |
| A large AI as the reader (rules given as instructions) | Not run: needs an API key | Add an API key to the environment |
