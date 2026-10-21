# Prompt to start a new session

This is the exact first message given to the new session on 21 October 2026. To start another session later, open a new Claude Code session on this repository and paste everything in the box below.

```
You're continuing my research project. You are taking
over from two earlier sessions, which have stood down.

Objective (my words): increase an LLM's ability to
"comprehend" and "understand" in a way that improves
communication. Every step must serve that.

Branch: ccr-1be0d913-1tlzao. Everything is on it.
Don't use the old branches (research,
ccr-1be0d913-audit-pack): they are older copies.

Read, in order:
1. CLAUDE.md (my standing rules: files, nothing
   locked, authorship). Follow them in every step.
2. INTEGRATED_HANDOFF_2026-10-21/00_START_HERE_
   Integrated_Handoff.md (every session, branch,
   folder and result, and what is still missing)
3. experiments/HANDOFF.md ("Start here" box and the
   drift guard)
4. experiments/COMMUNICATION_GUIDE.md (how I talk;
   follow its working rules)
5. experiments/PLAN.md (step 0 is what's next)
6. experiments/README.md and PRIOR_WORK.md as needed

My last instruction to the old session was "Stop
everything except API". So:
- Don't resume the numbers test or start any
  training unless I ask.
- Check that nothing is running (pgrep -af python).
- Check whether ANTHROPIC_API_KEY is set. Never
  print it or ask me to paste it.
  - If it's set: make one tiny test call to confirm
    it works (say the cost), then draft the
    conversation test's pass/fail rules (PLAN 0b)
    for my approval. Don't run the test until I say
    yes.
  - If it's not set: tell me in one line where to
    add it, and wait.

Drift check: spot-check two or three key claims in
the handoff against the raw results files and the
git history. Tell me plainly if anything is
overstated, missing, or has drifted from the
objective.

How to work with me:
- I explain with pictures and rough math. Turn them
  into plain rules, mark your guesses, and check
  with me when a guess changes the result.
- Every idea gets a fair test: beat chance, use a
  control, and commit the pass/fail rules before
  running. Never change them after a result is
  seen; save a fix as a new version.
- Report failures as plainly as successes, in plain
  numbers ("6 more right per 100").
- No flattery and no mythic tone. My images are
  names, not evidence. Tiny-model results don't
  change how a large AI understands anyone.
- I read on my phone: outcome first, short, plain
  words. My messages may have typos; if one could
  change what you do, ask.
- Commit and push after every step. No AI
  co-author lines.

First reply, phone-friendly:
1. The objective, in 2 lines.
2. Where things stand, in 5 lines.
3. Drift or overstatement found, if any.
4. API key: set or not, and what you did.
5. What you propose next, and how long it takes.
```
