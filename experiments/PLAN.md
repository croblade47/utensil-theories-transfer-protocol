# Plan: next steps

Work top to bottom. Mark each step done, with its result, in `HANDOFF.md`.

## 1. Finish what's running
- [ ] **Experiment 8 verdict:** run `python experiments/confirm.py`. It reuses saved models and prints the pre-registered verdict. Write it up in README.md.
- [ ] **Experiment 9, the Aesop test:** run `python experiments/aesop_test.py` (about 1.5 hours). Report P1 and P2 first, then S1–S3.

## 2. Strengthen the shifting word, where it showed signal (judging right vs wrong)
- [ ] **Make judging a main test.** Write a new held-out story set and pre-register *judging* as the primary measure, since experiment 8 used it only as a side measure.
- [ ] **Try the owner's original rule:** set `RECHARGE = True` in `shifting_word.py`, which re-adds 17 at each appearance. Compare against the current version.
- [ ] **Try the owner's numbers (32, 16, 34, 47)** as reset sizes and thresholds. Report honestly, including no effect.
- [ ] **Shifting word on world stories:** the Bible's judgment phrases don't exist there, so mark clear right/wrong with the strongest-worded paragraphs. Then rerun the Aesop test.

## 3. Bigger readers
- [ ] **A large AI as the reader:** give it the same story tests with and without the Bible's rules, or the shifting-word convention, as instructions. Needs an API key in the environment.
- [ ] **A larger tiny model** (more layers, more steps) if a GPU becomes available.

## 4. If anything holds up
- [ ] **Write a short public report:** the idea (credited to the owner), the method (built with an AI), every result including failures, and the code.
- [ ] **Compare with prior work** found by the research review (see `HANDOFF.md`).
