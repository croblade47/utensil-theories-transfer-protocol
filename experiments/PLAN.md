# Plan: next steps

Work top to bottom. Record each result in `HANDOFF.md` and `README.md`. Pre-register pass/fail rules (commit them) before any run.

## 0. Finish what's running
- [ ] **Experiment 9, the Aesop transfer test.** Run `python experiments/aesop_test.py`. It resumes: finished runs are read from `results_aesop.json`, and saved models from `experiments/models/` (if the machine still has them). About 15–25 minutes per model on 4 CPU cores, 16 models. Report P1, P2, P2b and P3 first.
- [x] **Exploratory start-marker run:** done (stopped early). It made things worse: the shifting word copied "unresolved" down the whole story. It **carries perfectly but updates poorly**.

## 1. Confirm the owner's carry idea properly (experiment 11 found L2)
- [ ] **A fresh long-story set, pre-registered**, with the shifting word vs the plain label as the main test.
  - New everyday acts, so not the stories_v2 acts.
  - 3–5 seeds.
  - Distances of 1, 3, 5 and 8 neutral sentences.
  - Expected if the idea holds: the gap grows with distance.
- [ ] **Balance carry vs update:** retrain the shifting word so markers respond more to new sentences (stronger reset, faster `SPEND`, or the owner's numbers as settings). Then rerun the long-story test.
- [ ] **Try the owner's original rule** (`RECHARGE = True`, "W1 = 17 + 4"). The long-story test is where re-adding 17 could matter, so retrain the shifting word with it and compare.
- [ ] **Try the owner's numbers** (32, 16, 34, 47) as reset sizes or `SPEND` rates in the long-story setting. Report effect sizes even if small: the owner considers any improvement notable.

## 2. Confirm the judging gain with its own pre-registration
- [ ] **New short story set, with judging as the primary measure:** marked methods (shifting, label) vs no marker vs scrambled. Experiment 8 showed it only as a side measure.

## 3. The "spelling" part of the idea
- [ ] **Sub-word tokenizer:** our word-level tokenizer makes the five spellings five unrelated tokens, so the shared syllables are invisible. Retrain with a sub-word tokenizer (BPE) so the rotations *share pieces*, and test whether that helps.

## 4. Bigger readers
- [ ] **A larger tiny model** (more layers, longer window), if time or a GPU allows.
- [ ] **A large AI as the reader:** give it the long-story tests with and without the shifting-word convention as instructions. Needs an API key.

## 5. Share it
- [ ] **A short public report:**
  - the idea, credited to the owner, and the method, built with an AI;
  - every result, including failures (experiments 5, 6 and 8, and L1);
  - the code;
  - comparison with prior work (`PRIOR_WORK.md`).
