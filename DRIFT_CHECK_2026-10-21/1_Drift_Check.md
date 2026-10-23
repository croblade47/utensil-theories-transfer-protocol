# Drift check of the handoff (21 October 2026)

Garrett C. Gauthier is the owner and sole author of this project and its ideas. This check was done with Claude (Anthropic) in Claude Code, a tool used by the owner.

## Outcome
The handoff's numbers match the raw results files and the git history. One result reads stronger than it is (the long-story carry), and one old commit message still says "confirmed". The project has not drifted in its notes, but most work since 18 Oct has been side work, and communication itself is still untested.

## What was checked
| Claim in the handoff | Raw source | Matches? |
|---|---|---|
| Labeling right/wrong: judging about 69 vs 50 per 100, all 3 runs | `experiments/results_confirm.json` (`v2_judge`) | **Yes.** Shifting word 67, 72, 67 (average 68.7). No marker 49, 60, 40 (49.7). Scrambled 56, 42, 60 (52.7) |
| Long stories (everyday act): carry 59 vs label 53 | `experiments/results_long_story.json` (condition B) | **Numbers yes.** Carry 59, 56, 63 (59.3); label 54.5, 51, 54 (53.2) |
| Stated verdict: label won (73, 51, 97) | same file (condition A) | **Yes.** Carry 45, 57, 62.5 |
| Long-story rules saved 03:44, changed 03:45 and 03:51 | git history, 18 Oct | **Yes.** Commits 99622d3 (03:44), c93f383 (03:45), 6fc220d (03:51) |
| Experiment 10 pre-registered at 02:17 | git history | **Yes.** Commit 6e365ef |

## Overstated or missing
1. **The long-story carry gain is about answering more often, not judging better.** Over the 3 runs (300 pairs):
   - the plain label gave an answer on only 31 pairs (right on 25);
   - the carry gave an answer on 106 pairs (right on 81);
   - on the 16 pairs where both answered, they were right equally often (13 each).
   So "6 more right per 100" is real, but it comes from the carry still having a signal after the act is out of view, while the label has almost none. That is what the carry idea predicts, so it is not a failure. But it should not be read as "the carry judges acts better". It means "the carry still has something to go on". Measured on answered pairs only, neither method was better.
2. **An old commit message overstates.** Commit 01b9050 (18 Oct 04:04) says "L2 confirmed". The written notes were corrected to "supported once (re-run after a fix)". The commit message can't be changed without rewriting history, so this note records it.
3. **A third condition is left out of the summary.** "carry3" (the carry with 3 spellings instead of 5) scored 59, 63.5, 59 on the everyday-act stories, about the same as the 5-spelling carry. It is a second carry variant, so it is consistent, but it isn't an independent test.

## Drift from the objective
The objective: increase an LLM's ability to comprehend and understand in a way that improves communication.
- The notes still state it and the drift guard is intact.
- Since 18 Oct, most work was side work: the seed test, the compression ladder, the numbers test, the project record, the similar-work check and the GitHub inventory. Only the compression ladder measures understanding, and none of it measures communication.
- All 12 experiments use a 3.4-million-parameter model. None of them tests communication with a person, or says anything about how a large AI understands anyone.
- The conversation test (PLAN step 0b) is the first test aimed directly at the objective. It is the right next step.

## How the check was done
I recomputed the scores from the raw per-pair lists in the JSON files with a short Python script, and read the commit times from the full git history. I trained and ran no models.
