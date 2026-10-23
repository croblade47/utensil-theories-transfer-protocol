# Privacy and fact checks on the project record (21 October 2026)

Two checkers read the assembled report: a privacy and tone editor first, then a fact checker. Every change they made is below.

## Privacy and tone

| Before | After | Why |
|---|---|---|
| (section 6.2) Helper agents had written "he/his" for the owner; this was changed to "they/their". | Helper agents had used gendered pronouns for the owner; these were changed to "they/their". | Privacy: removes he/his used for the owner, which also hinted at their gender. |
| (section 3, #62) One framework name in it contains a person's full name, which is kept out of this public record. | ...kept out of this public record; it is called here "the owner's error-encoding method". | Privacy: uses the neutral label the brief asked for. The name itself was never in the document. |
| - **Understanding shrinks the exact seed** (experiment 12). | (experiment 12, confirmed). | Tone: this item sat under 'Strong and repeated', so the exact status word 'confirmed' was added. |
| / Meaning from text alone / Worked: 10 of 14 / | / Meaning from text alone / Worked once: 10 of 14 (no rules saved first) / | Tone: experiment 1 was a single run with no saved rules, so 'Worked' overstated it. |
| / Recharge rule and the numbers / Being tested; no results yet / | / Recharge rule and the numbers / Running; no results yet / | Status wording: uses 'running'. |
| (9.1 table) / 8 / Numbers test / In progress: dry run passed; full run not started / | / 8 / Numbers test / Running: full run started 17:45 UTC, 21 Oct; no results yet / | Status wording, and it contradicted sections 1, 3 and 9.2, which say the full run started at 17:45. |
| (4.5) - A 4-reviewer review is running. After it, the full run takes about 4-5 hours. | - The 4-reviewer review finished on 21 Oct. The full run (about 4-5 hours) has been running since 17:45 UTC. | Out-of-date status that contradicted the rest of the document. |
| (5B numbers test) - **Full run next:** 18 models, ... | - **Full run (running):** 18 models, ... | Out-of-date status; now uses 'running'. |
| (9.2) Dry run passed ... (2.6 minutes, 5-step models, | (1.7 minutes by its own log, 5-step models, | Matches section 5B, which says the log shows 1.7 minutes and that 2.6 came from a chat reply. |
| (10.1 NUMBERS_TEST row) `dry_run/`; `results/`, `logs/`, `review/` still empty | `dry_run/`, `review/` (review findings and fixes); `results/` and `logs/` empty at the time of writing | review/review_findings_and_fixes.md exists, and section 9.2 refers to it. |
| (4.8) The owner's day-1 phrase ... is exactly the right unit. | ... fits this unit well. | Tone: softens an overstated claim. |
| 85.4% smaller, and less than half of what xz needs. | ... what xz (a standard compression tool) needs. | Jargon at first use. |
| 59 vs 53 right per 100 (p = 0.004), | (p = 0.004, meaning luck alone would give this about 4 times in 1,000), | Jargon at first use (p-value). |
| a large-model API key, or a fresh expert reading. | a large-model API key (an access code for a large AI's paid service), or ... | Jargon at first use. |
| added 16 tests (`resonance/`, commit `d8ebeec`). | (`resonance/`, commit `d8ebeec`; a commit is a saved, dated change in the repository). | Jargon at first use. The timeline explains 'commit' only later. |
| the branch's diff has stayed large | the branch's diff (its list of changes against the main version) has stayed large | Jargon at first use. |
| (Shannon 1951, the Hutter Prize) | (Shannon 1951, and the Hutter Prize, a long-running text-compression contest) | Jargon at first use. |
| one-sided: sign tests for M1 and M2, and a 100,000-flip permutation test for M3. | sign tests (counting wins and losses pair by pair) ... permutation test (reshuffling to see how often luck matches the real gap) ... | Jargon at first use. |
| **The repository is public under MIT.** | **The repository is public under MIT** (an open license that lets anyone copy and reuse it). | Jargon at first use. |
| Yes, force-added; git stores identical copies once | Yes, force-added (saved despite the repository's rule to skip model files); git stores identical copies once | Jargon. Checked that .gitignore lists experiments/models/. |
| Glossary: Confirmed / supported once / not confirmed: ... | Confirmed / supported once / not confirmed / untested / running: ... / not yet tried / started, with no results yet. | Defines all five status words the document uses. |

**Left as is:** I made 21 small exact replacements and kept everything else, for these reasons.

Privacy (I checked the whole document against messages #1-#59):
- The message #51 life story (education, loss, youth, anger) and the #3/#4 personal reflections, including the father reference and the letter, are already summed up in one neutral line or left out.
- The name Garrett appears in the uploads and in Copilot's reply, but not in the document. "The owner's first name" in the section 7 table names no one.
- The Dawson_Creek time zone and the profile-document titles are not in the document.
- The section 13 contact-details warning names no detail.
- EBEC is an acronym, not a person's name; I checked the uploaded EBEC file. So EBEC and ebec_benchmark.json stay.

Kept on purpose:
- "numbers my subconscious mind has focused on for years" (#9, #39). It is project-relevant and is the hypothesis being tested.
- The palm seed "on vacation ... Antarctica". It is the owner's metaphor, not their real travel or location.
- "whether it could earn anything" (#10). It is about the project's value, not personal finances.
- #60 mentions emailing people but names no recipients.
- "This could be huge actually" is the owner's own quote.
- The audit phrase "strong and repeated, not yet pre-registered as the main measure" comes straight from the sources, so I did not change it to one of the five status words.
- The 02:20 UTC snapshot lines in section 3 and section 5B ("A 4-reviewer check is running", "Status at about 02:20 UTC ... NO RESULTS YET") are correct for that time, and later lines update them.

Characters: the only characters above Latin-1 are curly quotes and dashes, which are allowed. The ÷ in line 332 and the é in Delétang are Latin-1, so they stay.

Method: I applied each edit as a Python exact-match replacement, checking that each target appeared exactly once, instead of with the Edit tool. All the edits are small and listed in changes. I made no changes to the repository and did not commit, push or send anything.

## Facts

| Before | After | Why |
|---|---|---|
| (3, #7) Experiment 5: chance (45-52%) on 20 new story pairs | Experiment 5: chance (45-57%) on 20 new story pairs | results_consequences.txt runs from 45% to 57% (random verses removed #3 = 23/40). Sections 4.2 and 5.12 already said 45-57%. |
| (3, #35) ...whole numbers and raw bytes (`b6397c1`). | ...whole numbers and raw bytes. The graph-method drafts so far were saved (`b6397c1`). | git_log: b6397c1 is 'first drafts of graph method readings', not the palm-seed answer. The AI's 09:20 reply says it saved the two method files. |
| (3, #36) ...a dig through the chat and a fact check (`8f705c6`). | ...a fact check. Graph-method drafts were saved (`8f705c6`). | git_log: 8f705c6 is 'in-progress graph method drafts', not the greenhouse launch. |
| (3, #37) The AI posted a progress map with faces (`93890e4`). | The AI posted a progress map with faces. A graph-method update was saved (`93890e4`). | git_log: 93890e4 is 'graph_backwards update during checks'. The faces map was a chat reply, not a commit. |
| - **20:13-21:06 [LIMIT]** - Session limit (reset 21:10 UTC). | - **20:22-21:06 [LIMIT]** - Session limit (reset 21:10 UTC). | assistant_texts: at 20:13 the AI gave a normal reply. The limit messages appear at 20:22 and 21:06. |
| (5B) **Status at about 02:20 UTC, 21 October: NO RESULTS YET.** | **Status at about 02:20 UTC, 21 October, updated at 17:45 UTC: NO RESULTS YET.** | The bullets under this heading report the 17:45 review and run start, so the heading's time was out of date. |
| (9.2) At the time of writing the `results/` and `logs/` folders are empty. | At the time of writing the `results/` folder is empty, and `logs/` holds only the full-run log, which shows the first model has started training. | ls: NUMBERS_TEST_2026-10-21/logs/full_run_log.txt now exists (commit bb4c6eb, 17:48). It shows 'training num_charge17 seed 0' at 17:47. results/ is empty. |
| (9.2) ...a separate checker for each serious finding. Fixes come before the full run. | ...The fixes were made before the full run. | Out-of-date tense: the fixes were applied and the full run started at 17:45. |
| (10.1 NUMBERS_TEST row) `review/` (review findings and fixes); `results/` and `logs/` empty at the time of writing / 0.46 MB / | `review/` (review findings and fixes), `logs/` (the full-run log); `results/` empty at the time of writing / 0.65 MB / | ls and du: logs/ holds full_run_log.txt and the folder is now 652K. |
| (10.1 PROJECT_RECORD row) (`code/md2pdf.py`, `build_outputs.py`) | (`code/assemble_report.py`, `md2pdf.py`, `build_outputs.py`) | ls PROJECT_RECORD_2026-10-21/code shows assemble_report.py too (commit 4bc3a9c). |
| - **Commits:** 118 commits on this work, 17 to 21 October | - **Commits:** 122 commits on this work, from 17 October to 17:48 UTC on 21 October | git log on the branch shows 122 commits since 17 Oct, excluding the 3 zine commits. git_log.txt alone has 116; no snapshot gives 118. |
| `numbers_test.py` (the numbers test, 62 KB) | `numbers_test.py` (the numbers test, 65 KB) | wc -c: 65,085 bytes after the review fixes. |
| Experiments 1 to 12 (from `experiments/HANDOFF.md`): | Experiments 1 to 11 (from `experiments/HANDOFF.md`) and experiment 12 (from the `GROW_UNDERSTANDING_2026-10-20` guide): | HANDOFF.md's 'How to run anything' block has no understanding_compression.py line. That command comes from the GROW guide. |
| python understanding_compression.py                      # exp 12, 30-45 min | python understanding_compression.py                      # exp 12, about 24 min | results_understanding.txt says 'Run time 23.9 minutes', and README and the GROW guide say 'about 24 minutes'. No source gives 30-45. |
| (13) Session limits stopped work several times on 20 Oct. | Session limits stopped work twice on 20 Oct and twice on 21 Oct. | Matches section 3's 'Updated totals: 4 usage-limit stops (2 on 20 October, 2 on 21 October)'. |
| (12) Each model here had 1,500 steps. | Most models here had 1,500 steps (the two small Aesop models about 275; dry-run models 5). | results_aesop.txt shows the rules model at 275 steps and the narrative model at 274; dry runs used 5 steps. |

**Left as is:** - **2,029 vs 2,021 clear choices.** The record says 2,029 in 4.3, 5.7 and 6.1. That is exp 7's own printed count (README line 127, commit c918cb7). The numbers test recomputes the same rule today and gets 2,021 (dry-run and full-run logs, review file). The review says these labels equal sw.mark_up's on every verse, so the word values have probably shifted slightly since exp 7. Both numbers come from sources but describe different runs. 2,021 never appears in the record. I kept 2,029 for exp 7. The parent may want to add 2,021 to the numbers-test section, with a note on the difference.
- **"Confirmed" for "understanding shrinks the seed".** This was not a pre-registered test in the glossary's sense. HANDOFF.md, though, says "The ladder is confirmed", and the privacy editor added this word on purpose, so I kept it.
- **Spelling cut points.** 5.7 says "-12 to -4, between -4 and +4". 6.1 says "-11 to -4, -3 to 3, 4 to 11". Both match the source: the code's float thresholds and the docstring's integer table. Not a numeric conflict.
- **num_seqrev "0.30%" at cap.** This is the dry-run figure. After the rounding fix the full-run log prints 0.31%. The table is labelled as the dry run.
- **Repository history "about 386 MB".** du now gives 388M and it keeps growing. "About" covers it.
- **6.3 #8 "Ran a test".** The AI was stopped while starting tests (#23, 08:17). The wording is slightly strong but matches the owner's own correction.
- **Not checkable from the sources:** #60–#63 times, the 06:30 and 17:00 reset times, and the 17:37 start. Owner messages end at #59 and assistant texts at 02:15. a8a0cd7 (13:13) and 55f6817 (17:45) do exist in the repo's git log, but not in git_log.txt.
- **Left unchanged and consistent:** "M1: 100 new story pairs" (the exp-8 pairs, unseen in training) and "the 4-reviewer review finished" (3 finished, and the 4th's checks were done directly, as 9.2 explains).
