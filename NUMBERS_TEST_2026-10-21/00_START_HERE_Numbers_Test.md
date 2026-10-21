# START HERE: The Numbers Test (21 October 2026)

## What this folder is
The test of the owner's numbers **17, 32, 16, 34, 47**, placed where the owner pointed: the place of 17 in their own day-1 rule **"W1 = 17 + 4 Remaining"**.

In that rule, each time the shifting word appears it gets a fresh **charge**, and whatever was **left over** last time is carried on top. The words of the verse then use up most of the charge, and the word is spelled from what is left. This "recharge" part of the owner's rule was switched off in every earlier experiment, so **this is the first time the owner's full rule is tested.**

**Status: running.** This guide is updated at each step.

## What is being tested, in plain words
Six new versions of the shifting word, each trained 3 times (18 small models):

| Name | The charge each time the word appears | Why it is here |
|---|---|---|
| `num_charge17` | 17 every time | The owner's plain recharge rule. In ordinary text it settles at exactly 17 + 4: each verse uses 17 and leaves 4 |
| `num_seq` | 17 (at a clear right/wrong), then 32, 16, 34, 47, 17, 32 ... in turn | **The owner's numbers, in the owner's order** |
| `num_seqrev` | 17, then 47, 34, 16, 32, 17 ... | The same numbers in reverse order: does the order matter? |
| `num_const29` | 29.2 every time (the average of the five numbers) | Same average size, no turn-taking: is it the sequence or just a bigger charge? |
| `num_charge47` | 47 every time | The owner wrote "47" in the place of "17+4" |
| `num_drain0` | 0 (no charge) | A check on the AI's own choice (how fast words use up the charge), so that choice can't take credit for the owner's rule |

A clear right or wrong verse always restarts the run at +17 or -17, as the owner's day-1 rule says.

Each model is compared with the earlier models (already trained, reused unchanged): the current shifting word, the plain Bible model with no marker, and three others.

**Three measures:**
1. **Judging (the main one):** 100 new story pairs, one right and one wrong. Does the model tell which is which?
2. **Long stories:** the act scrolls out of the model's view, so only the carried word can remember it.
3. **Exact seed size:** how many bits it takes to regrow 623 unseen verses exactly (the greenhouse measure from experiment 12).

The pass/fail rules were written before any of the 18 models was trained. They are in `code/numbers_test.py` (top of the file) and in `design/interpretations_and_design.md`.

## The verdict
*Not yet: the models are being trained.*

## Timeline of what was done
1. **20 October, evening.** The owner asked to test the numbers, then clarified: *"I just know my sub conscious mind has had those numbers in that sequence ... the +4 was a way to direct you to a way to try testing the numbers where I feel like they belong."*
2. **Three independent readers** (AI agents) read the owner's notation from three angles: the owner's own rules, the numbers themselves, and test design. **A judge** chose the final six versions and wrote the pass/fail rules. Their full write-ups are in `design/interpretations_and_design.md`.
3. **The test script was built** (`code/numbers_test.py`). The builder checked that its marking matches the judge's simulation verse for verse, for all six versions.
4. **Paused** at the owner's request, then a full project review.
5. **21 October, 02:06 UTC: dry run.** Every part of the test was run end to end with tiny 5-step models, writing only to a scratch folder:
   - all six versions pass the pre-registered check (no spelling stuck, at most 1.23% of verses at the cap);
   - the saved shifting and plain models reproduce their stored scores exactly through the new script;
   - the exact-seed coder regrows the text byte for byte.

## Technical details
- **The rule, step by step** (for each verse, in order):
  1. At each book start: Remaining R = 0, no direction yet.
  2. The word for this verse is spelled from R, with the same five spellings as before: anoksha (heavy wrong, R ≤ -12), oksharu (-11 to -4), velanok (unresolved, -3 to 3), sharuvel (4 to 11), ruvelan (heavy right, R ≥ 12).
  3. If a direction exists, the next charge from the list is added: W = R + charge (in the direction of the last clear choice).
  4. If the verse is a clear right or wrong: R = +17 or -17, the direction is set, and the list restarts.
     Otherwise each valued word in the verse adds its value to W, then W shrinks by 14.1% (the "drain"). What is left is the new R, capped at ±51.
- **The drain (14.1% per valued word)** was the AI's choice, not the owner's. It was set so that the owner's plain rule settles at exactly W = 17 + 4 = 21 in ordinary text, leaving 4. That is what keeps the word from getting stuck at the top, which is why the recharge was switched off before.
- **Frozen constants:** RESET 17, CAP 51, NBAR 10.9043 valued words per training verse, DRAIN 0.141073.
- **Models:** the same tiny transformer as experiments 6–12 (64 words of view, 1,500 training steps), seeds 0, 1 and 2.
- **Tests:** one-sided sign tests over story pairs (measures 1 and 2) and a paired permutation test over verses (measure 3), with Holm correction within each group of comparisons.

## Every file in this folder

| File (path inside this folder) | What it is | Where the original lives |
|---|---|---|
| `00_START_HERE_Numbers_Test.docx` / `.md` | This guide (Word file, plus a text copy) | branch `ccr-1be0d913-1tlzao`, `NUMBERS_TEST_2026-10-21/` |
| `code/numbers_test.py` | The test: the six rules, training, the three measures, the pre-registered tests | `experiments/numbers_test.py` (same branch) |
| `code/md2docx.py` | The small converter that makes the Word copy of this guide | made in this session; only here |
| `design/interpretations_and_design.md` | The three readings of the owner's notation and the judge's final design and pass/fail rules, word for word | made from this session's work; only here |
| `design/judge_simulation/sim_rules.py`, `sim_judge.py`, `sim_extra.py`, `values.json` | The judge's simulation of the six rules on the Bible (no training), and the word values it used | made in this session; only here |
| `design/builder_check_markup_matches_judge.py` | The builder's check that the script marks every verse exactly as the judge's simulation does | made in this session; only here |

## Things outside this folder's control
- **The repository is public** on GitHub (MIT license): anyone can read these files. Changing that is the owner's decision, in GitHub settings.
- **A cloud session can't place files on your devices.** The files are sent to you in the app to save.
- **Scale:** these are tiny models. A result here does not change how a large AI like Claude understands anyone.
