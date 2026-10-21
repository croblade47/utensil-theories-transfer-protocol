# Numbers test: independent review before the full run

Four reviewers were set to check `numbers_test.py`, each from a different angle, before 18 models were trained. Each was told to find anything that would waste the run or make a result untrustworthy. They were not allowed to change any repository file.

- **Result:** three reviewers finished (21 October, about 02:20-02:40 UTC and 13:10-13:30 UTC; the session hit its usage limit twice in between). **All three said "ready". They found no blocking problem, only minor notes.**
- **The fourth reviewer (engineering and run safety)** was cut off twice by the usage limit. Its checks were done by the main session at 17:40 UTC instead. The dry run was re-run after the fixes, with fingerprints of the repository taken before and after. The repository and the models folder were unchanged, every exact seed regrew byte for byte, and the stored control scores reproduced exactly. A provisional report was tested and left the results file untouched.

## Every finding, and what was done

| Finding | Severity | What it said (short) | What was done |
|---|---|---|---|
| rule-1 (The rule arithmetic) | minor | The check that numbers_test uses the same clear choices as sw.mark_up compares only the COUNT of clear verses, not the label of each verse. The docstring (line 219) and design claim the clear choices are 'computed exactly as in sw.mark_up'. I checked independently and the per-verse labels ARE identi... | Applied: the script now refuses to run unless the clear choices are exactly 1,033 right and 988 wrong (together with the pinned word values, this fixes every per-verse label). |
| rule-2 (The rule arithmetic) | minor | Nothing pins the frozen word_values NUMBERS to the version the judge checked. The NBAR and DRAIN asserts depend only on which words are in `values` (nval counts `w in values`), not on their values. A change in the numbers (for example scipy svds or BLAS rounding flipping a borderline word's round(le... | Applied: the word values and all six markups are pinned to the verified fingerprints; the run stops if any differs. |
| rule-3 (The rule arithmetic) | minor | Design comment. 'In neutral text this rule settles at exactly W = 17 + 4 = 21, leaving 4 Remaining (checked)' is exact only for a hypothetical verse with exactly NBAR = 10.9043 valued words of value 0. Real verses have integer counts (0 to 40, median 10). Because the drain is convex in the count (Je... | Wording fixed in the START HERE guide ("a verse with the average number of valued words settles at 17 + 4"). The frozen DRAIN is unchanged. |
| rule-4 (The rule arithmetic) | minor | Cosmetic. The trace prints a charge and W on clear-choice verses. Step (2) computes them, then step (4) discards them, which matches the design literally. A reader can still take them as applied. Example: verse 9985 is a WRONG verdict, yet its row shows charge +17 and W +16.8. | Applied: the trace shows "(reset)" instead of a charge on clear-choice verses. |
| rule-5 (The rule arithmetic) | minor | Cosmetic double rounding. cap_pct_checked is stored after round(...,3), then printed with :.2f. For num_seqrev the true 0.3054% becomes 0.305, which prints as '0.30%'. The judge's figure beside it is 0.31. | Applied: cap percentages are stored to 4 decimals, so 0.3054% now prints as 0.31%. |
| design-m3-marker-entropy (Test-time consistency and stored controls) | minor | Design comment. M3 TOTAL includes the cost of sending each held-out marker, and that cost follows how spread out a config's spellings are, whatever the model understands. The exp 12 checker already noted that held-out markers are hard to predict from the visible context. Configs whose spellings are ... | Applied as a descriptive column: Table 3 now shows words-only bits next to the TOTAL. Not part of any verdict. |
| design-m1-carry-vs-content (Test-time consistency and stored controls) | minor | Design comment. M1 stories are one sentence with no marker in front, the same as exp 10 did for shifting, so it is consistent. Under the charge rules, though, the marker after a verse depends more on the run state carried from before (the sign of the last verdict) and less on the verse's own words. ... | Noted for the write-up; no code change (frozen design). |
| repro-informational-only (Test-time consistency and stored controls) | minor | The control reproduction check only reports. If it prints DIFFERS, for example because M3 runs on a different torch build or thread setup, the F1/F2 tests still run against the stored controls with nothing flagged in Table 4. It also covers only seed 0, and the M3 part runs only in the full run, nev... | Applied: the report prints a warning above Table 4 if any control fails to reproduce. |
| stats-1 (Statistics and pre-registration fidelity) | minor | Running `--report-only` for a provisional report while the full run is going can overwrite results_numbers.json with an older copy. The --report-only process loads the JSON at line 1000 and saves its in-memory copy at lines 1021 and 1039. Any save the main run makes in between is lost on disk until ... | Applied: --report-only never writes results_numbers.json; it writes results_numbers_provisional.txt instead (tested). |
| stats-2 (Statistics and pre-registration fidelity) | minor | Design comment / reporting gap. Pre-registration section 4 says 'M2 and M3 are judged by the same rules'. But when num_charge17 passes F1 only on M2 or M3, the printed 'recharge' verdict never states the R1 credit. The R1-credit sentence is added only when the M1 pass holds. The R1 result for every ... | Applied: a secondary-sign recharge verdict now states whether R1 passes on that measure. |
| stats-3 (Statistics and pre-registration fidelity) | minor | Design comment. The M3 'disagreement' flag compares the Holm-adjusted pass/fail of the permutation test with a Holm-adjusted sign test. The pre-registration only says the one-sided sign test 'is reported alongside' and 'any disagreement between the two tests is reported'. It does not say whether the... | Applied: M3 rows flag disagreement both after Holm and before Holm. |
| stats-4 (Statistics and pre-registration fidelity) | minor | Cosmetic, dry run only. In the dry report's Table 3, the shifting/baseline comparators are tagged '[stored]', but they were freshly encoded on the 40 dev verses. label/carry3/scrambled show '(not scored yet)'. This does not affect the full run, where load_stored supplies all five controls from resul... | No change needed (dry run only). |

## Checks each reviewer ran (their own words)

### The rule arithmetic (verdict: ready)

All scratch work is in <scratch>/tmp.nGTb6dUGZQ (t1_hand.py, t2_real.py, t3_fuzz.py, builder_copy.py), run with PYTHONDONTWRITEBYTECODE=1. No training, no repo writes: git status is clean, and the only __pycache__ files are pre-existing, gitignored ones dated Oct 17-20. The reviewed numbers_test.py has SHA 85ca6105…, the same as the dry run's meta.script_sha256. The only change since 12f2051 is in the docstring.

PASS: hand-made sequences (t1_hand.py). Drain 0.5 so the expected values are exact; expected R, W, charge, form and marked text worked out by hand; all compared verse by verse with mark_charge. All 9 groups pass:
(A) Two books with CH=(17,). Book start resets R, s and k. No charge before the book's first clear choice: verse 8 in Beta with R=-4 still gets charge 0. A clear verse's own words ('bad bad bad' on a RIGHT verse) are not read. After the reset the run goes R=17 then W=34. The charge sign follows the last clear choice even after R turns positive (v12: R=+7.96, charge -17, R -> -4.5185546875). Unvalued words cost nothing. R_spell equals the previous R_after, and is 0 at a book start.
(B, B') num_seq charges go 32,16,34,47,17,32,16 after a reset (the run 17 -> CH[0] -> CH[1] ...); num_seqrev goes 47,34,16,32,17,47. k restarts at every clear choice, including two clear choices in a row and sign flips.
(C, C') Clip at ±51 after reading, with CH 47 and drain 0. The cap flag is set when |x| >= 51, including x exactly 51. A negative clip works too.
(D) Float charge ±29.2 with the real DRAIN.
(E) The drain is applied after each valued word, including zero-valued words.
(F) form_for cut points -12/-4/4/12.
(G) The spelling comes from R BEFORE the charge.

PASS: random fuzz (t3_fuzz.py). 3,000 random multi-book sequences: random values, clear choices (including at book starts and in a row), CH of length 1-6 including 29.2, 3.7 and 0, drain in {0, 0.141, 0.5, 1, random}. Zero mismatches against my own implementation of steps (0)-(4).

PASS: real corpus (t2_real.py), 31,102 verses.
- The 66 book names form 66 contiguous runs.
- word_values(texts) equals the judge's values.json (6,836 words). The values sha d128a7fb… equals the dry run's.
- NBAR 10.904261950851406 and DRAIN 0.1410731824082132 equal my own computation and the judge's D. Both frozen asserts hold.
- (1-d)^NBAR = 0.19047619 (4/21). Fixed point R=4.000, W=21.000. The script's 60-step loop gives W 21.0, R 3.999999999999999.
- clear_choices labels equal sw.mark_up's labels on every verse (monkeypatched read): 2021 clear, 1033 right, 988 wrong. lst.marked_corpus('shifting') equals sw.mark_up.
- My independent implementation matches mark_charge exactly (np.array_equal) for all six configs on form, R_spell, R_after, W, charge, the cap flag and the marked text. The judge's sim mark() matches form and R_spell exactly, and the cap % agrees to 4 decimals (0.0289/0.2669/0.3054/0.2604/1.2282/0.0000).
- All six marked_sha256 equal the dry run's.

PASS: builder's comparison. A copy of builder_check_markup_matches_judge.py, re-run: forms and R identical for all six configs, DRAIN equal to the judge's D. The repo copies of sim_rules.py, values.json, sim_judge.py and sim_extra.py are byte-identical to the old scratch copies (cmp).

PASS: manipulation-check computations.
- My own shares, cap after reading, cap spelled from, min share, pass/fail, training-pool counts and retention (counted explicitly per verdict, n = 2005/1539/1236/827 for L = 1/3/5/10) all equal nt.manipulation for every config.
- All six configs pass: max cap 1.23% (num_charge47), min share 4.40% (num_drain0 anoksha).
- Retention at L=5: charge17 64.6, drain0 33.2, current shifting 62.9, matching the design's 65/33/63.
- 'Differs' figures: 55.0/28.1/22.3/13.5/30.9/52.9, matching JUDGE_DIFFERS. Shares are within 0.05 points of JUDGE_EXPECTED.

PASS (extra, outside my lens): p_at_least matches scipy binomtest(greater) for every n<60 and k; holm() matches a reference step-down implementation on 2,000 random vectors.

PASS: run_full.sh uses the same python and environment as the dry run and sets no thread variables, so the markup inputs are the same.

Issues are all minor. No blocking problem in the rule arithmetic.

### Test-time consistency and stored controls (verdict: ready)

All checks were read-only and ran from scratch folder <scratch>/tmp.R90K4b1xdQ with PYTHONDONTWRITEBYTECODE=1. Nothing was trained. Scripts: chk_stored.py, chk_vocab.py, chk_repro.py, chk_threads.py, chk_carry.py. The repo was untouched: the experiments/__pycache__ listing was identical before and after, and git status showed only another session's PROJECT_RECORD_2026-10-21/. The SHA-256 of experiments/numbers_test.py, 85ca6105..., is the same as the dry run's script_sha256 and the same as NUMBERS_TEST_2026-10-21/code/numbers_test.py.

PASS 1, how shifting was scored before and how num_* is scored now. Exp 10 stored shifting's M1 from confirm.score_word_model (copied into results_methods.json). numbers_test uses mc.score. Both make the model write its own marker after the story: ctx = [1] + story + [1], lean = softmax over the 5 spellings @ positions -2..2. No rule is applied to the stories. Exp 11 used lst.judge_marked with START_MARKER False, and run_m2 calls the same function and asserts START_MARKER is False (line 581). Exp 12 used uc.code_one with Neural(model) and held markers from the full-Bible markup, and run_m3 calls the same function with marked[c][i].split()[0] for i in held_idx (line 1116). Threads match each original run: M1 4 (tt sets 4, confirm/mc keep it), M2 1 (set by lst), M3 2 (set by uc; exp 12 meta threads = 2).

PASS 2, no dependence on names or globals. mc.score, lst.judge_marked, lst.neutral_fillers, lst.build_stories and uc.code_one/layout/run_coder/compare depend only on sw.FORMS, mc.POSITION, sw.lp_ids, sw.CLEAR_*, lst.START_MARKER and the vocab. None depends on a method name. The hard-coded method lists (lst.marked_corpus, lst.load_model, uc.METHODS, mc.ALL) are used only for shifting and baseline. A grep for assignments to sw./lst./mc./uc./confirm./tt. attributes, or for 'global', in numbers_test.py found none.

PASS 3, positions and direction. POSITION is {anoksha -2, oksharu -1, velanok 0, sharuvel 1, ruvelan 2}, the same as sw.FORMS order. For all six configs, every rec['form'] equals FORMS.index(form_for(R_spell)). After every clear RIGHT the next verse in the same book is spelled ruvelan (+2), and after every clear WRONG it is spelled anoksha (-2) (dir_after_clear_ok = True). Every marked text is 'form' + ' ' + the original verse.

PASS 4, vocab. For all six configs, tt.Vocab of the training texts has the same itos as the shifting model's, in the same words and order (8,581; symmetric difference empty). neutral_fillers returns the same 12 fillers as for shifting. The baseline vocab is 8,576, i.e. shifting minus the 5 spellings. The dry run JSON shows fillers_used 12, vocab_size 8581 and threads 2 for every config.

PASS 5, M3 setup. The H recomputed with uc.norm has the same SHA-256 as the results_understanding.json meta H_sha256. held_idx equals the stored held_verse_index (623). Torch, numpy and python versions match the exp 12 meta (2.14.1+cu130 / 2.5.3 / 3.13.16).

PASS 6, stored M1. results_methods.json has all 15 control keys (shifting, baseline, label, carry3, scrambled × seeds 0-2), each with v2_judge of length 100. shifting, baseline and scrambled are identical to results_confirm.json. stories_v2.py and consequences_test.py are unchanged since before exp 8. Re-scoring with numbers_test.run_m1 (4 threads, all 100 v2 + 20 v1 pairs) reproduced every per-pair v2_judge, v2_shift and v1 value exactly for shifting seeds 0, 1, 2 and baseline seeds 0, 1, 2.

PASS 7, stored M2. results_long_story.json has all 45 keys (5 controls × 3 seeds × B/A/short), each with 100 'correct', fillers_used 12, mean_pad 4.88. It comes from the final fixed run: the file was deleted in commit 6fc220d (the 03:51 fix that pushes the first marker out of view) and rebuilt from scratch. The flawed v1 files have mean_pad 4.78 and are separate. The startmarker run is a separate file. The only later change to long_story_test.py (226f68c) is a skip-if-cached. Re-scoring version B with numbers_test.run_m2 (1 thread, 100 pairs) reproduced 'correct' per pair exactly for shifting seeds 0, 1 and 2 (59.0 / 56.0 / 63.0). The baseline's B is 100 ties per seed (1.5 per pair), as the design states.

PASS 8, stored M3. All 15 keys exist: R6_baseline_seed{0,1,2} and R7_{shifting,label,carry3,scrambled}_seed{0,1,2}. Each has 623 per_verse_total values and was decoded with exact = True. numbers_test.run_m3 (2 threads) on shifting seed 0 with sw.mark_up held markers, and on baseline seed 0 with no markers, reproduced per_verse_total exactly (max abs diff 0.000000) and the same seed SHA-256 (12,524 B and 12,252 B). It stayed exact after the full run's sequence of thread switches (4 → 4 → 1 → 2) in one process. The marker is coded in the seed the same way as R7: kind 'm' first in each verse, counted in per_verse_total.

PASS 9, analysis use of stored data. gather() takes v2_judge[:100], B 'correct'[:100] and per_verse_total (mean over seeds) for the controls through load_stored. The keys match the stored files. run_tests only checks M3 seed-0 exactness for the new configs, and the stored controls are all decoded and exact. No output path overwrites a stored results file: only results_numbers.json/.txt and models/num_*_seed{s}_steps1500.pt are written, and no such model exists yet.

PASS 10, dry run log and outputs. All six configs pass the manipulation check, and their shares are within 0.05 points of the judge simulation. The three repro checks reproduced exactly. All six M3 dev decodes are exact. The dry run wrote only to its scratch folder.

Design comments (minor, not blocking): M3 marker entropy differs by config (drain0 1.89 bits up to seqrev 2.31), and the charge rules tie the marker more to the carried run state than to the verse itself, which matters for one-sentence M1 stories. Details are in the issues.

### Statistics and pre-registration fidelity (verdict: ready)

All scratch work is in <scratch>/tmp.mDVpDjpSTG (t_stats.py, t_m3.py, t_tests.py, t_report.py, t_report2.py, t_m2close.py, t_holm2.py, chk_stored.py). Nothing was trained. `git status --porcelain` was empty before and after, and no new __pycache__ appeared in the repo.

PASS — the dry run tested the current script: its SHA-256 85ca6105… equals `sha256sum experiments/numbers_test.py`.

PASS — the pre-registration text in the docstring (lines 130-189) matches interpretations_and_design.md lines 267-307 clause by clause (only the simulation path differs).

PASS — p_at_least(k,n) equals scipy binom.sf(k-1,n,.5) for every n ≤ 60 and every k (0 mismatches). It returns 1.0 at n=0.

PASS — holm() was checked two ways:
- Against a reference implementation over 5,000 random families, including ties and p=1 entries: 0 mismatches.
- Its 'adjusted p < 0.05' decisions against the textbook step-down rule (p_(i) ≤ α/(m−i+1)) over 60,000 families of size 1, 4 and 6: 0 mismatches.
- It is monotone and stays within [p, 1]. holm([0.04]) = [0.04], so F4 is a plain α = 0.05 test.
- The '<' versus '≤' choice cannot matter: no sign-test p (n ≤ 100) times 1-6, and no perm p (le+1)/100001 times 1-6, equals 0.05 exactly.

PASS — pair_test on hand-made arrays:
- It sums over seeds per pair and drops ties. Sums 3,1,1,3,0 vs 1,1,2,2,2 gave wins 2, losses 2, ties 1, p = 11/16.
- Direction is 'new is better': all-correct new gives p = 1/32; all-worse gives 1.0.
- M2 halves: against a constant 0.5 per seed, sums 2.0, 2.5, 0.5, 1.5 vs 1.5 gave wins 2, losses 1, tie 1, p = 0.5.

PASS — uc.compare / perm_test / sign_test match the pre-registration exactly:
- d = new − comparator; N_PERM = 100000; a fresh default_rng(0) for each test; p = (#{perm ≤ obs} + 1)/100001.
- An independent single-draw reference gave the same perm p to 5 decimals in 4 scenarios. The 10k-chunked draws equal one 100k draw (array_equal True).
- The sign test is one-sided for 'smaller', ties dropped, and matches the reference. All-zero d gives p = 1.

PASS — FAMILIES: F1 6 tests, F2 6, F3 4 (N1-N4 with the right new/comparator order), F4 1 (R1 num_charge17 > num_drain0).

PASS — run_tests, synthetic scenarios:
- An invalid test ('models missing', or M3 void because seed 0 did not decode exactly) or a degenerate config enters Holm with p = 1 and cannot pass; family size stays fixed.
- Void M3 tests still show their effect sizes.
- The M3 void check looks only at the new configs' seed-0 'exact'.

PASS — verdicts, synthetic scenarios:
- N1 on M1 gives 'owner's numbers matter'. N1+N2+N3 give 'sequence'. N4 gives '47'.
- num_charge17 in F1 plus R1 gives 'credited'; without R1 it gives 'NOT credited…drain'.
- Any F1 pass on M1 gives 'useful', listing which configs passed.
- An M3-only pass gives 'secondary sign only…not a confirmation'. Otherwise 'not shown at this scale'.

PASS — stored controls:
- results_methods.json has v2_judge for 100 pairs for all 5 controls × 3 seeds (ITEMS_V2 = 100, ITEMS_V1 = 20).
- results_long_story.json has B/A/short 'correct' for 100 pairs each.
- Baseline B is 0.5 in all 300 seed×pair cells (uniq [0.5]), so every pair sums to 1.5 and F2 on M2 means 'beats chance', as stated.
- results_understanding.json R6_baseline / R7_{shifting,label,carry3,scrambled} seeds 0-2: 623 per-verse totals each, all decoded and exact, threads 2, same torch/numpy/python versions.
- Stored summaries match README exps 10/11 (shifting M1 67, 72, 67; B 59, 56, 63; carry3 B 59, 63.5, 59; label A 73, 51, 97).
- M2 scoring in run_m2 is identical to long_story_test.main (same `1.0 if jr>jw else 0.5 if isclose else 0`).
- The filler pool is the same size (12) for stored and new runs, and every new vocab is 8,581.

PASS — near-ties (np.isclose versus 'exact tie'): re-judging version B with the stored shifting seed-0 model on 100 pairs (31 s, 1 thread) gave 70 exact ties, 0 near-ties that isclose would wrongly call ties, and a smallest nonzero |jr − jw| of 1.49. The asymmetry is harmless.

PASS — report() in the full-run shape (seeds 0-2, 100/100 pairs, real load_stored) never crashed:
- no new models;
- one model with M1 only;
- one config with M1+B only;
- two configs complete;
- all 18 complete;
- all 18 with a seed-0 decode mismatch (shows 'NO - M3 VOID', 'DECODE MISMATCH', and void flags in Table 4).

PROVISIONAL and complete are flagged correctly, and the analysis dict is JSON-serialisable.

PASS — the dry-run report <scratch>/dry_main/numbers_test_dry/results_numbers_dry.txt (313 lines) is complete:
- Table 0: all six PASS, within 0.05 points of the judge's shares; differs % equals all of the judge's figures; kept-5 is 33 for drain0, 65 for charge17 and 63 for shifting, as the docstring says.
- Spelling counts and all six traces are there.
- Tables 1-4 and the descriptive control comparisons are there.
- Verdicts: the M3-only passes are correctly called 'secondary sign only'.
- Expectation, limits, and three repro lines all REPRODUCED EXACTLY.
- The log has no warnings or NaN. The 5-step models' numbers are meaningless, as labelled.
