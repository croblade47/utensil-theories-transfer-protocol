# Plan: next steps

Work top to bottom. Record each result in `HANDOFF.md` and `README.md`. Pre-register pass/fail rules (commit them) before any run.

## 0. Finish what's running
- [x] **Experiment 9, the Aesop transfer test:** DONE, not confirmed (see README experiment 9).
- [x] **Exploratory start-marker run:** done (stopped early). It made things worse: the shifting word copied "unresolved" down the whole story. It **carries perfectly but updates poorly**.

## 1. Confirm the owner's carry idea properly (experiment 11 found L2)
- [ ] **A fresh long-story set, pre-registered**, with the shifting word vs the plain label as the main test.
  - New everyday acts, so not the stories_v2 acts.
  - 3–5 seeds.
  - Distances of 1, 3, 5 and 8 neutral sentences.
  - Expected if the idea holds: the gap grows with distance.
- [ ] **Balance carry vs update.**
  - First check whether greedy marker choice (argmax in `long_story_test.judge_marked`) is hiding updates. Re-score the existing models with the full spelling distribution carried forward, or with sampled markers. That's exploratory and needs no training.
  - Then retrain the shifting word so markers respond more to new sentences (stronger reset or faster `SPEND`), **under new model file names**, and rerun the long-story test.
- [ ] **Try the owner's original rule** ("W1 = 17 + 4"). Needs new code: train a separate model with RECHARGE on, under its own file name, without editing the shared settings in `shifting_word.py`. Cached keys and model names don't record it, so flipping the setting would silently reuse or overwrite old models. With it on, the balance pins at ±51, so also try a smaller cap.
- [ ] **Try the owner's numbers** (32, 16, 34, 47) as RESET sizes with SPEND and word values fixed, or as ratios (e.g. SPEND = 17/34 or 16/32 per word). A raw SPEND of 16–47 per word would erase the balance immediately. Use new model names, in the long-story setting. Report effect sizes even if small: the owner considers any improvement notable.

## 1b. Bring it back to communication (closest to the objective)
- [ ] **Conversation-carry test:** the communication version of experiment 11. In a long dialogue, the owner states an intent or a key fact early, followed by enough ordinary turns that it scrolls out of view. Does a carried marker help the model answer later turns consistently with that early intent? Shifting word vs plain label vs no marker, pre-registered. This tests whether carried state improves *understanding a person over a conversation*, which is the owner's actual goal.
- [ ] **Owner-explanation test:** take the owner's real metaphor-and-math explanations (for example `[w1=17 −<next word (−13)> = +4 Remaining]`) and check whether a reader maps them to the right mechanism. Turn `COMMUNICATION_GUIDE.md` into checkable examples.

## 2. Confirm the judging gain with its own pre-registration
- [ ] **Also queued:** a consequences test with the ending format matched across marked and plain models; and a "rules with reasons attached" training set as a control in the stories-vs-rules comparison (see `PRIOR_WORK.md`).
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
