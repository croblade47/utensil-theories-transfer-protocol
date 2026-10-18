# Prompt to start a new session

Open a new Claude Code session on this repository and paste everything in the box below as your first message.

```
You're continuing my research project.
Objective: increase an LLM's ability to
"comprehend" and "understand" in a way that
improves communication. Every step must serve
that. Read the drift guard at the top of
HANDOFF.md and tell me if anything has drifted.

First, switch to branch ccr-1be0d913-1tlzao.
The files below are not on main. If you have
to push to a new branch, put its name in
HANDOFF.md and this prompt file.

Before starting anything, check for jobs still
running (pgrep -af python) and whether
experiments/models/ exists (it is not in git).

Read, in order:
1. experiments/HANDOFF.md (where things stand)
2. experiments/COMMUNICATION_GUIDE.md
   (how I talk; follow its working rules
   in every reply)
3. experiments/PLAN.md (next steps)
4. experiments/README.md and
   experiments/PRIOR_WORK.md (only as needed)

How to work with me:
- I explain with pictures and rough math. Turn
  them into plain rules, mark your guesses, and
  check with me when a guess changes the result.
- Every idea gets a fair test: beat the coin
  toss (chance), use a control, and save the
  pass/fail rules (commit) before running.
- Report failures as plainly as successes. Give
  sizes in plain numbers ("6 more right per 100").
- No flattery. Don't copy the grand, mythic tone
  of other AI chats. My images are names, not
  evidence.
- I read on my phone: outcome first, short,
  plain words.
- Commit and push after every step.

First reply: five lines on what you understood,
then the open threads, one line each. Then start
the first unfinished step in PLAN.md. If it will
take over 30 minutes, tell me how long first.
```
