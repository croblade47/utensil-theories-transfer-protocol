# START HERE: Integrated Handoff (21 October 2026)

Garrett C. Gauthier is the owner and sole author of this project and its ideas. This guide was put together with Claude (Anthropic) in Claude Code, a tool used by the owner.

## What this folder is
Everything from every work session on this project, combined into one place, so a new session (or you) can pick up without searching. The owner asked for it on 21 October: "Integrate all session data to strengthen the data and start a new instance."

It contains:
- this guide: where things stand, every session, branch and folder, every result, what is still missing, and the decisions waiting on you;
- the prompt given to the new session;
- up-to-date copies of the four working notes and the standing rules;
- a copy of the start-here guide from every delivery folder, so all the master docs sit together.

## Where things stand (short version)
- **Goal:** help an AI understand people better, so it communicates better.
- **Progress:** about rung 1 of 5. In a tiny model:
  - labeling right and wrong in the training text helps judging (69 vs 50 right per 100);
  - your carry idea helps remember an act in long stories (59 vs 53 per 100, seen once).
- **Clear failures:**
  - predicting consequences (chance);
  - the Aesop test (stories didn't transfer better);
  - carry with stated verdicts;
  - carry in the compression test.
- **Communication itself is still untested.** The next step is the conversation test with a large AI as the reader. It needs an API key.
- **Your last instruction to the old session:** "Stop everything except API". So nothing is running. The numbers test is paused at 3 of 18 models.

## Every work session

| Session (title) | When (UTC) | What it did | Where its work is | Status |
|---|---|---|---|---|
| Shared room simulation | 11 Oct | Added a skill for running role-play rooms between AI copies | branch `ccr-e9b75f5f-6rquhp` | Finished |
| Print-ready prototype pages | 14 Oct | Zine prototype: two starter books with a launch script | **Not in the repository**: delivered only in the app as a zip | Finished |
| Human error encoding system (the research session) | 17 Oct 21:41 to 21 Oct 21:50 | Experiments 1-12, Aesop test, seed test, technical report, project record, similar-work check, GitHub inventory, numbers test | branch `ccr-1be0d913-1tlzao` | Stopped by you; asked to push its last unsaved files, then stand down |
| Code session | 18 Oct 02:46-02:52 | "Master patent-ready theory" file for the zine project | branch `ccr-4507ebbb-bfz236`; real Word copy in `AUDIT_PACK_2026-10-18/5_Other_Master_Files/` | Finished |
| Comprehension research: continuation (the audit session) | 18 Oct 05:47 to 21 Oct | Audit of the research, prompt to the research session, your file rules, Aesop check, this combined handoff | merged into `ccr-1be0d913-1tlzao` | Hands over to the new session |
| New session | from 21 Oct | Takes over the research | `ccr-1be0d913-1tlzao` | Started with the prompt in this folder |

## Every branch on GitHub

| Branch | What it holds | Use it? |
|---|---|---|
| `ccr-1be0d913-1tlzao` | **Everything:** research, results, saved models, all delivery folders, the audit, standing rules | **Yes, this is the working branch** |
| `ccr-1be0d913-audit-pack` | The audit folder; fully merged into the working branch | No (older copy) |
| `research` | An older duplicate of the working branch (21 Oct 17:56). Checked: nothing on it is missing from the working branch | No. Deleting it is your call |
| `ccr-4507ebbb-bfz236` | Zine "master patent-ready theory" file | Zine project |
| `ccr-e9b75f5f-6rquhp` | Shared-room simulation skill | Separate |
| `main` | Zine project release v1.0.0-rc1 (August) | Zine project |

## Every delivery folder (all on the working branch, top level)

| Folder | What it is |
|---|---|
| `AESOP_RESULTS_2026-10-18/` | Aesop test (experiment 9) results and write-up |
| `AUDIT_PACK_2026-10-18/` | The audit: timeline, what went wrong, re-checked numbers, all files as of 18 Oct |
| `TECHNICAL_REPORT_2026-10-20/` | "Seed and grow" rebuild kit: how to rebuild the whole project from scratch |
| `SEED_TEST_2026-10-20/` | Fair test of your "data seed" idea (no AI needed) |
| `GROW_UNDERSTANDING_2026-10-20/` | Experiment 12: understanding as compression |
| `NUMBERS_TEST_2026-10-21/` | Your numbers 17, 32, 16, 34, 47 in the "W1 = 17 + 4" rule. Paused at 3 of 18 models |
| `PROJECT_RECORD_2026-10-21/` | Full record of 17-21 Oct. **The report itself is missing from GitHub** (see below) |
| `SIMILAR_WORK_CHECK_2026-10-21/` | Search of news, YouTube and papers for similar work |
| `GITHUB_INVENTORY_2026-10-21/` | What is findable under your name, and a list of your projects and personas |
| `INTEGRATED_HANDOFF_2026-10-21/` | This folder |

The start-here guide from each folder is copied into `3_All_Start_Here_Guides/` here.

## Every result, in plain numbers (50 = guessing, unless noted)

| # | Test | Result | Verdict |
|---|---|---|---|
| 1 | Color learned from text only | 10 of 14 objects matched (guessing: about 2) | Worked |
| 3 | Are the Bible's rules the key? | Rules alone no better than other verses | No |
| 5, 6, 8 | Predict consequences of new stories | 51 per 100 | Failed |
| 7 | Shifting word, 20 stories | 68 vs 52; later shown to be luck (test 8) | Not confirmed |
| 8, 10 | Labeling right/wrong in training text, then judging new stories | 69 vs 50 per 100, all 3 runs | Strong, not yet pre-registered as the main measure |
| 10 | Your carry vs plain label, short stories | 68.7 vs 67.7 | Tie |
| 11 | Your carry vs plain label, long stories (everyday acts) | 59 vs 53 per 100; the recovered first run showed the same gap | Supported once |
| 11 | Same, with the verdict stated in the story | Label won 74 pairs, carry 11 | Failed for the carry |
| 9 | Aesop: do folk tales teach morals that transfer? | Folk tales 52.3, novels 54.1, shuffled 53.1, Bible 43.6 | Failed (all 4 checks) |
| 12 | Understanding as compression | Exact seeds shrink with understanding: 8.0 → 1.17 bits per character | Worked |
| 12 | Does your carry make compression better? | About 2% worse | Failed |
| Seed test | Your "data seed" idea | Regrows data exactly; shrinks only patterned data (99.99% on a pattern, 6-19% on Bible text, 0% on random) | Works as described, with that limit |
| Numbers | Your numbers in the full "W1 = 17 + 4" rule | 3 of 18 models done | No verdict yet |

Scale caveat: every result comes from a model of about 3.4 million parameters. None of it changes how a large AI like Claude understands anyone.

## Timeline, 17-21 October (UTC)
- **17 Oct, evening:** research session starts. Experiments 1-7.
- **18 Oct:**
  - experiments 8-11 and the Aesop test;
  - the audit (05:47 onward) found wording stronger than the evidence and one test changed after a peek;
  - corrections applied at 07:35; Aesop failed at 07:34.
- **20 Oct:**
  - technical rebuild kit;
  - seed test;
  - experiment 12 (compression);
  - the 15 trained models and the Bible text saved to GitHub;
  - your numbers test queued.
- **21 Oct:**
  - numbers test built, dry-run and reviewed;
  - project record written;
  - your +/- scoring rule recorded;
  - authorship rule added;
  - similar-work check and GitHub inventory;
  - numbers test started 17:45, stopped at your request at 21:50 ("Stop everything except API");
  - this combined handoff, and a new session started.

## Still missing or unresolved
1. **Project record report:** the folder's guide lists the report (PDF, Word, text, email parts, checks), but only the guide and build scripts are on GitHub. The old session was asked on 21 Oct to push the rest.
2. **Numbers-test models:** the 3 finished models were saved only on the old session's machine. They were requested the same way. Without them, those 3 must be retrained (about 30 minutes) when the test resumes.
3. **Zine prototype zip (14 Oct session):** never put in the repository. If you have it, it can be added.
4. **Your messages:** the project record collects your 59 messages up to 21 Oct 02:15. Later ones exist only in the session transcripts. The key ones are quoted in `experiments/HANDOFF.md` and in this guide.

## Decisions waiting on you
1. **API key:** if you added `ANTHROPIC_API_KEY`, the new session will confirm it works. If not: environment menu → Edit → Network secrets (or an environment variable). Never paste it into chat.
2. **Conversation test:** the new session will draft the pass/fail rules for your yes before anything runs.
3. **Numbers test:** resume (about 4 hours) or leave paused.
4. **Repository visibility:** it is public (MIT license); anyone can read it. Change it in GitHub settings if you want.
5. **Google Drive sharing to your three accounts:** blocked by a safety check on 18 Oct; it needs your explicit approval to retry.
6. **Old `research` branch:** keep or delete.

## Your standing rules (full text in `CLAUDE.md`)
1. **Files:** real files saved into a dated folder as they are made, sent to your screen, with a start-here guide and a zip; never links only.
2. **Nothing locked or permission-blocked.**
3. **Authorship:** you are the sole author; AI is credited only as a tool; no AI co-author lines.

## Every file in this folder

| File (path inside this folder) | What it is | Where the original lives |
|---|---|---|
| `00_START_HERE_Integrated_Handoff.docx` / `.md` | This guide (Word, plus a text copy) | here |
| `1_New_Session_Prompt.docx` / `.md` / `.txt` | The exact first message given to the new session | `experiments/NEXT_SESSION_PROMPT.md` |
| `2_Current_Notes/HANDOFF` (`.docx`, `.md`) | Where the project stands, with the new "Start here" box | `experiments/HANDOFF.md` |
| `2_Current_Notes/PLAN` (`.docx`, `.md`) | Next steps in order (step 0: API key, conversation test) | `experiments/PLAN.md` |
| `2_Current_Notes/COMMUNICATION_GUIDE` (`.docx`, `.md`) | How you communicate, with the new lessons | `experiments/COMMUNICATION_GUIDE.md` |
| `2_Current_Notes/CLAUDE` (`.docx`, `.md`) | Your standing rules | `CLAUDE.md` (repository top) |
| `3_All_Start_Here_Guides/<FOLDER>__00_START_HERE...` | The start-here guide of each of the 9 other delivery folders, in Word and text | each folder on the working branch |
| `INTEGRATED_HANDOFF_2026-10-21.zip` (next to this folder) | This whole folder as a plain zip | repository top level |

## Things outside this folder's control
- **Public repository:** anyone can read these files on GitHub. Changing that is your decision.
- **Your devices:** a cloud session can't place files on your devices. The files are sent to you in the app to save.
- **The old session:** whether it pushes its last files depends on it running again. If it doesn't, the items in "Still missing" stay missing.
