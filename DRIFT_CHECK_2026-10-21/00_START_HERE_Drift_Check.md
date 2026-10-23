# START HERE: Drift Check (21 October 2026)

Garrett C. Gauthier is the owner and sole author of this project and its ideas. This folder was put together with Claude (Anthropic) in Claude Code, a tool used by the owner.

## What this folder is
The new session's first step: a check of the integrated handoff against the raw results and git history, plus a status check (nothing running, API key not set).

## Timeline (21 Oct, UTC)
- Read CLAUDE.md, the integrated handoff, HANDOFF, COMMUNICATION_GUIDE and PLAN.
- Checked for running jobs: none.
- Checked ANTHROPIC_API_KEY: **not set**. No API call made; cost $0.
- Recomputed key results from `experiments/results_confirm.json` and `experiments/results_long_story.json`; checked commit times in the full git history.
- Wrote the drift check (this folder).

## Main findings, short
- The numbers in the handoff match the raw files.
- The long-story carry gain (59 vs 53) comes from the carry answering more often. Where both models answered, they tied (13 right each, out of 16).
- Commit 01b9050 still says "L2 confirmed". The notes say "supported once", which is correct.
- Communication is still untested. The conversation test is the right next step and needs the API key.

## Files
| File (path in this folder) | What it is | Original |
|---|---|---|
| `00_START_HERE_Drift_Check.docx` / `.md` | This guide | here (branch `ccr-1be0d913-1tlzao`) |
| `1_Drift_Check.docx` / `.md` | The full check, with tables | here |
| `DRIFT_CHECK_2026-10-21.zip` (next to the folder) | Plain zip of this folder | repository top level |

## Outside this folder's control
- The repository is public (MIT): anyone can read it.
- I can't place files on your devices; they're sent to you in the app.
