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

## In progress / pending (update when done)
- **Experiment 8, the confirmation on 100 new story pairs: DONE.**
  - **Consequences:** NOT CONFIRMED (shifting 51/100, p = 0.46). The plain model did slightly better (61/100).
  - **Judging right vs wrong** (side measure): shifting **67, 72, 67**, vs scrambled 56, 42, 60 and no word 49, 60, 40. Pair by pair, shifting beat scrambled 57–25 (p = 0.0003).
  - Needs its own pre-registered confirmation with judging as the main measure.
- **Experiment 10, method comparison** (`method_comparison.py`): shifting word vs the plain good/bad label (the established conditional-training method) vs carried balance with 3 spellings. Judging is the main measure. Status: **RUNNING**
- **Experiment 9 — Aesop moral transfer test** (`aesop_test.py`). Aesop is never in training; the model must match each fable to its true moral over a swapped one. Training sets of equal size: world folk tales (9 cultures), Bible, and novels as a control; plus rules vs stories at small size. Pass/fail rules P1, P2, S1–S3 are in the file's docstring. Status: **PENDING**, waiting for the CPU and a pre-run review.

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

## How to run anything
```bash
pip install numpy scipy torch          # CPU is fine; each tiny model trains ~11 min on 4 cores
python experiments/bible_understanding.py
python experiments/confirm.py          # re-uses saved models in experiments/models/ if present
python experiments/aesop_test.py
```
Data downloads automatically on first run (KJV and world stories from raw.githubusercontent.com, novels from the NLTK data mirror). In this sandbox only GitHub-hosted files could be downloaded; Gutenberg, Archive.org and Wikisource were blocked.

## Carried balance: open threads
In the spirit of the owner's "remaining" value, these are unresolved questions carried forward. Each has a lean based on evidence so far.

| Thread | Lean so far | What would settle it |
|---|---|---|
| Does the shifting word teach *judging* right vs wrong? | **Strongly for** (69% vs ~50%, 3 runs, 100 new pairs), but a side measure | Pre-registered judging test on fresh stories |
| Is that from the *carry* (the owner's idea) or labeling in general? | Unknown | Experiment 10 (shifting vs plain label) |
| Does it teach *predicting consequences*? | **Against** (not confirmed, 51/100); the plain model did better | A bigger model, or matching the ending format |
| Do stories transfer lessons better than rules? | Unclear: rules alone didn't win in experiment 3 | Aesop test (experiment 9) |
| Re-adding 17 at every appearance ("W1 = 17 + 4") | Untested | Switch `RECHARGE = True` in `shifting_word.py` and rerun |
| Do the numbers 32, 16, 34, 47 matter? | No reason yet, since only ratios matter | Try as reset sizes or thresholds |
| A large AI as the reader (rules given as instructions) | Not run: needs an API key | Add an API key to the environment |
