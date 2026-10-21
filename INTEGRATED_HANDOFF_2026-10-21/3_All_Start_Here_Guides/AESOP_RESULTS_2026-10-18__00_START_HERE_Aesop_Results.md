# START HERE: Aesop Test Results (18 October 2026)

## What this folder is
The finished results of the Aesop test (experiment 9): do lessons taught through stories transfer to fables from a culture the model never saw? It also records the accuracy corrections from the audit session.

**The answer:** not confirmed. Details are in `1_Aesop_Result_Writeup.docx`.

## Timeline (UTC, 18 Oct 2026)
- **00:52** Confirmation test (experiment 8) pre-registered. **02:35** Written up: consequences not confirmed; judging strong.
- **02:17** Method comparison (experiment 10) pre-registered. **03:41** Written up: the plain label ties the shifting word.
- **03:40** The Aesop test starts: 16 small models, trained one after another.
- **03:44** Long-story test (experiment 11) pre-registered. Two fixes during run 1 (03:45, 03:51). **04:04** Written up; now worded "supported once".
- **05:47** A new session ("Comprehension research: continuation") is launched for an independent audit.
- **07:32** The Aesop test finishes. All four pre-registered tests fail. **07:33** Results pushed.
- **07:35** Audit corrections applied ("Accuracy corrections from audit"). Flawed first-run long-story results kept in the repo. This folder made.

## Technical details
- **Models:** tiny GPT-style models, 4 layers and about 3–5 million parameters (the word list differs per training set), trained from scratch on CPU. Each sees 128 tokens at a time and trains for 1,500 steps.
- **Test:** 67 Aesop fables, 1,131 same-format pairs and 284 no-word-clue pairs. Score: the share of pairs where the true fable→moral matching beats the swapped one.
- **Statistics:**
  - each set vs guessing: a permutation test;
  - set vs set: a fable-level paired permutation test, plus a model-level test across 4 vs 4 training runs.
- **Raw numbers:** `2_Raw_Results/results_aesop.json` holds every score matrix; `results_aesop.txt` is the full printout.

## Every file in this folder

| File | What it is | Original location (branch `ccr-1be0d913-1tlzao`) |
|---|---|---|
| `00_START_HERE_Aesop_Results.docx` (and `.md`) | This guide | This folder |
| `1_Aesop_Result_Writeup.docx` (and `.md`) | The results in plain English: verdicts, numbers, and what they mean for communication | Summary of `experiments/README.md`, experiment 9 |
| `2_Raw_Results/results_aesop.json` | Every model's score matrix and settings | `experiments/results_aesop.json` |
| `2_Raw_Results/results_aesop.txt` | Full printout of the test and its verdict | `experiments/results_aesop.txt` |
| `3_Code/aesop_test.py` | The test itself, with its pre-registered pass/fail rules at the top | `experiments/aesop_test.py` |
| `3_Code/world_stories.py` | Downloads the 12 story collections | `experiments/world_stories.py` |
| `3_Code/tiny_transformer.py` | The tiny model used | `experiments/tiny_transformer.py` |
| `AESOP_RESULTS_2026-10-18.zip` (next to this folder) | Everything above in one plain zip | Repository top level |

## Good to know
- **The repository is public on GitHub** (MIT license), so anyone can read these files. Changing that is your decision, in GitHub settings.
- **Nothing here is locked:** no passwords, and the zip is plain.
