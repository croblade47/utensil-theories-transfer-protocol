# Prompt for the other AI session (draft for the owner to review and fix)

**Who this is for:** the session titled "Human error encoding system", which is running the Aesop test (experiment 9) on branch `ccr-1be0d913-1tlzao`.

**Status:** DRAFT. The owner reviews and edits this before it is sent. Nothing has been sent.

---

## The prompt

You are continuing my research project. Before you do anything else, read this whole message. It corrects where the work has drifted.

### 1. The objective (my words, unchanged)
Increase an LLM's ability to "comprehend" and "understand" in a way that improves communication. Every step must serve that.

The story tests, the Bible and the fables are training material and ways of measuring. They are not the goal. If a step does not move us toward better communication, say so before you do it.

### 2. Where we stand (checked against the raw results files by a second session)
- Rung 1 of 5: two small signs of better understanding inside a 3.4-million-parameter model.
  - Labeling right/wrong in the training text: 69 vs 50 right per 100. Strong and repeated, but never pre-registered as the main measure.
  - My carry idea in long stories: 59 vs 53 per 100, seen once.
- Nothing has tested communication yet. Nothing has been tested on a real-size AI.
- The numbers in README.md match the raw files. The wording does not always.

### 3. Corrections to make in HANDOFF.md, README.md and PLAN.md
Make these after the Aesop results are in. Commit them as one step called "Accuracy corrections from audit".
1. Change "Works" for judging to "strong and repeated, not yet pre-registered as the main measure".
2. Change "L2 CONFIRMED" to "supported once". Add why: the pass/fail rules were saved at 03:44. The test was changed twice afterwards (03:45 and 03:51), after the first models were scored, and the first-run results were not kept. The test also reused the same 100 story acts as experiments 8 and 10.
3. Add the shape of the carry result: in long stories the carry model gives no answer (an exact tie) on about 65 of 100 pairs. When it does answer, it is right 81 times and wrong 25.
4. Delete "by design" where README says the plain label is blind to the act. It isn't: it writes its own markers too, which is how it scored 97 in one run.
5. Experiment 10 was pre-registered at 02:17, after 7 of the 9 experiment-8 models had already shown judging was strong. Choosing judging as the main measure came after that peek. Say so.

### 4. Rules from now on (no exceptions)
1. **Pass/fail rules are frozen once saved.** If you find a flaw after any result is seen, keep the original result, save the fix as a new version, and label the new result "re-run after a fix". Never call it "confirmed".
2. **Keep every result,** including flawed runs. Nothing is "set aside and lost".
3. **Plain numbers,** like "6 more right per 100", always next to pass or fail.
4. **Mark guesses** about what I meant. Check with me when a guess changes the result.
5. **No hype and no mythic tone.** My images are names, not evidence.
6. **Use the tools properly:**
   - Commit and push after every step.
   - Before saying a file exists, check it.
   - Report test failures and skipped steps.
   - If a tool or key is missing, say what is missing and what it blocks. Don't work around it silently.

### 5. File delivery rule (strict)
Every file you make must reach me as an actual file, not a link and not just a path.
- Send each finished file with the file-sending tool, so it shows up on my screen in the app.
- If there is more than one file, put them all in one folder. Include a master doc called `00_START_HERE` that lists every file in plain English with its path. Zip the folder and send the zip.
- Use real Word files (.docx). Do not use a web page renamed to .doc.
- Also commit the folder to the repo.

### 6. When the Aesop test finishes
1. Push the results to `ccr-1be0d913-1tlzao`.
2. Report P1, P2, P2b and P3 first, as pass or fail with plain-number sizes. Failures as plainly as successes.
3. Say in one line what the result does or does not mean for communication.
4. Apply the corrections in section 3.
5. Deliver the result write-up as a file, using the rule in section 5.
6. Stop. Do not start a new experiment. The next step is a conversation test (does carried state help a model stay true to what a person said early in a long conversation?). I will approve its pass/fail rules first.

---

## Notes for the owner (not part of the prompt)
- **My guess at what you meant:** "the other AI" is the session running Aesop. "Using stuff properly" means three things: the pre-registration rules, file delivery, and the tools it has. Tell me if you meant something else.
- **Ready to edit:** sections 4 and 5 are where your own rules go. Add or cut freely.
- **I can't do this part:** I can't place files on your laptop desktop or phone home screen. I can send real files to the app, where you tap to save them.
