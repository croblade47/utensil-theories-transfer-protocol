# Can a text-only reader understand? (Bible experiments)

**Question.** A person born blind learns color through language and use: snow is white, blood is red, scarlet is a royal fabric. Can a machine that only reads do the same? And are the Bible's rules ("thou shalt not") the key teaching material, as Romans 7:7 suggests: *"I had not known sin, but by the law"*?

**Method.** A small model reads the King James Bible (31,102 verses, about 793,000 words) and learns only which words keep company with which. It starts with no outside knowledge. All test words were fixed before any results were seen. Run `python experiments/bible_understanding.py`; the full output is in [`results.txt`](results.txt).

## Results

### 1. Color without sight: worked
- The model matched objects to their color **10 of 14 times (71%)**. Guessing would get 17%. It got snow→white, blood→red, wine→red, night→black, darkness→black, and grass/tree/herb→green.
- It learned what color *means in this book*, not hue. Scarlet, purple and blue cluster with *silk, linen, twined, needlework*, because in the Bible they are tabernacle fabrics. This is how blind people describe color: through what it belongs to and what it's used for.
- **Failed:** the Isaiah 1:18 metaphor ("sins as scarlet… white as snow"). Every color word sat closer to *purity* than to *sin*, mostly because the purity laws in Leviticus describe white and red skin and hair. White did lean toward purity the most, and red the least. The direction was faintly right, but the metaphor wasn't learned.

### 2. Three ways of reading the tokens: little difference

| Reading | General meaning | Moral meaning | Color |
|---|---|---|---|
| A. Word by word | 0.975 | 0.957 | 10/14 |
| B. Whole verse as one unit | 0.974 | **0.995** | 11/14 |
| C. Hebrew parallelism (the second half of a verse restates the first) | **0.979** | 0.948 | 11/14 |

Scores run from 0.5 (guessing) to 1.0 (perfect). All three readings understand well. Reading the whole verse as one thought gave the best sense of right and wrong. The parallelism gain is too small to trust.

### 3. Are the rules the secret? Not in this test
- 2,801 verses (9%) are rules.
- **Learning from rules only** gave no better grasp of word meaning than the same number of random verses (0.867 vs 0.841 ±0.039), and a slightly *worse* sense of right and wrong (0.625 vs 0.709 ±0.081).
- **Removing all rules** barely changed anything (0.948 vs 0.950 for removing random verses).

The stories, prophets and psalms carry right and wrong at least as strongly as the law does.

### 4. Romans 7:7 directly ("Thou shalt not covet"): partly echoed
With every rule verse removed, **none of the 15 wrong acts flipped to "good."** But the ones the law mostly names grew weaker:

| Act | Full Bible | No rules | Times seen without rules |
|---|---|---|---|
| covet | −0.077 | −0.043 | 3 of 8 |
| steal | −0.163 | −0.110 | 16 |
| drunkenness | −0.195 | −0.054 | 4 |
| lying | −0.083 | −0.047 | 53 |

The law **sharpens** the sense of wrong, most for the acts that mostly appear inside it, like coveting. It isn't the only source: the stories teach it too.

## What this means
- **Understanding without sensing is real, but different.** A pure reader rebuilt a surprising amount of color, morality and meaning from relationships between words alone. That matches research on people born blind, who know color mostly through associations.
- **Rules alone aren't the secret.** Rules plus the stories of breaking them were needed. In these tests, the narrative of human error taught as much as the commandments did.
- **Limits:** this is a small, decades-old style of model, and the test lists are small. A stronger next test would ask whether rules help a model *predict consequences* in new stories, not just place words near each other.

---

## Experiment 5: Predicting consequences in new stories

**Question.** Can the model predict what *follows* an act in a story it has never seen? And do the rules, which are often written as act → consequence, teach that better than stories do?

**Design (fixed before running).** I wrote 20 new story pairs. Each pair is one situation with a right act or a wrong act ("found his neighbour's ox astray and brought it again" vs. "took his neighbour's ox by night and sold it"). Both stories share two endings, one fortunate and one ruinous. Always picking the same ending scores exactly 50%. Moral label words (good, evil, sin, blessed…) are banned, and no ending reuses words from its stories; the script checks both. Run `python experiments/consequences_test.py`; full output is in [`results_consequences.txt`](results_consequences.txt).

### Result: chance level everywhere

| Method | Score (50% = guessing) |
|---|---|
| Association (which ending sounds like the story) | 45% |
| Consequence map learned from the Bible's "this, then that" sequences | 48% |
| Map learned from rule verses only | 52% |
| Map learned from the same amount of non-rule verses (3 draws) | 45–52% |
| Rules removed from everything | 50% |
| Same amount of random verses removed (3 draws) | 45–57% |

None of these differ from coin-flipping. The model can't predict consequences, and the rules made no difference.

### Diagnostic (added after seeing the result above): where does it break?

| Piece | Score |
|---|---|
| Tells the right-act story from the wrong-act story | 60% (p = 0.25, not reliable) |
| Tells the fortunate ending from the ruinous one | 70% (p = 0.06, borderline) |
| Adding one rule, "as you sow, so you reap" (Galatians 6:7) | 60% (p = 0.13) |

The Bible text does tie right/wrong to fortune/ruin: the two directions line up at +0.22 (0 would mean unrelated). Removing the rule verses gives +0.18, which is inside the range from removing random verses (+0.16 to +0.25). So the stories carry that link as much as the rules do.

### What this means
- **The weak point is not the rule; it's understanding the act.** In experiment 3 this model knew *words* like steal, murder and covet were wrong (scores near 0.96). But it can't tell that *"took his neighbour's ox by night and sold it"* is stealing, because none of those words is wrong on its own. The wrongness comes from how the words combine.
- **That is the line between association and comprehension.** This model averages words, so it can't combine them. Understanding a situation, rather than a vocabulary, needs a model that reads word order and structure.
- **Rules didn't help because the model couldn't apply them.** A rule like "thou shalt not steal" is only useful if the reader can recognize a new situation as stealing. That recognition is what's missing. It matches the child-and-rote-memory point: knowing the rule's words isn't the same as seeing where the rule applies.

**Next test.** Train a small model that reads word order (a tiny transformer) on the Bible alone, then run these same 40 stories. If it passes where this one failed, that isolates *composition* as the missing ingredient. Then repeat with and without the rules.

---

## Experiment 6: A tiny transformer (a model that reads word order)

**Why.** The word-averaging model failed because it can't combine words. A transformer reads word order and can, in principle, work out that "took his neighbour's ox by night and sold it" is stealing.

**Setup.** A small GPT-style model (3.4 million parameters, 4 layers) trained from scratch on the King James Bible only: no other text, no pre-training. Training ran 1,500 steps (about six passes over the text, 12 minutes on 4 CPU cores). Every 50th verse was held out to check that it learned the language. Scoring was fixed before training. Run `python experiments/tiny_transformer.py`; results are in [`results_transformer.json`](results_transformer.json).

Five test words never appear in the KJV ("broke", "buyers", "its", "sickened", "welcomed"), so the model sees them as unknown. The stories were kept unchanged so results stay comparable with experiment 5.

### Result: it learned the language, not the consequences

| Test (50% = guessing) | Score | p |
|---|---|---|
| Shifts toward the right ending depending on the act (20 pairs) | 9/20 = 45% | 0.75 |
| Picks the right ending (40 stories) | 22/40 = 55% | 0.32 |
| Judges the act "evil / right in the sight of the lord" correctly (20 pairs) | 9/20 = 45% | 0.75 |

Its error on held-out verses was 3.46. Roughly, it narrows each next word to about 1 in 32 out of 8,658, so it clearly learned the Bible's style. It did no better than chance at linking acts to consequences or judging acts.

**The rules comparison was not run.** With the full-Bible model at chance, removing the rules could only be compared against noise.

### What this means
- **Reading word order was not enough at this size.** About 800,000 words of one book teaches a tiny model how the Bible *sounds*, not what its situations *mean*. Grammar comes first; meaning needs far more data or a far larger model.
- **For scale:** a child hears tens of millions of words in their first years, *and* sees, touches and suffers consequences alongside them. Large modern AI models read trillions of words. This model had one book.
- **The question is still open, not answered no.** These tests show where understanding does *not* appear (word association; tiny models on one book). They can't yet show whether the Bible's rules help once a model is big enough to understand situations.

**Possible next steps**
1. **Use an existing large model as the reader** and test the same 40 stories with and without the Bible's rules given to it as instructions. This tests the rules idea directly, on a model that can already understand sentences.
2. **Bigger training on more text** (Bible plus other plain-English stories). This needs a GPU, not this sandbox.

---

## Experiment 7: The shifting word ("velanok"): the first result above chance

**The idea (from the project owner).** A made-up word carries a running balance from one use to the next, and its *spelling* changes with that balance, the way to / too / two / 2 sound alike but are written differently. A clear wrong resets the balance to −17, a clear right to +17. Words in between add or spend it, and whatever remains carries forward. A model reading the text then sees the state inside the text itself.

**How it was built** ([`shifting_word.py`](shifting_word.py))
- **Five spellings,** rotations of the syllables *sha-ru-vel-an-ok*: `anoksha` (heavy wrong), `oksharu`, `velanok` (unresolved), `sharuvel`, `ruvelan` (heavy right).
- **Word values** come from the Bible-trained word model's good/evil direction. For example, steal −5, adultery −10, mercy +5, love +6. Common words like "the" are worth 0.
- **Each word also spends 0.5** of the balance, so it fades back toward "unresolved" unless something reinforces it. This follows the owner's example: "the next words use up the remainder → 0."
- **Clear choices** are the Bible's own judgment formulas ("did evil in the sight of the Lord", "did that which was right…") plus the 3% most strongly worded verses at each end. 2,029 verses reset the balance.
- **Not used:** re-adding 17 at every appearance (it's an option, `RECHARGE`). With it on, the balance climbs to the ±51 cap (3 × RESET) and stays there, so almost every verse would get an extreme spelling. The balance is always capped at ±51 and resets to 0 at the start of each book.

Example, 2 Kings 17: "And he did that which was evil in the sight of the Lord" flips the word to `anoksha`. It stays there through the siege of Samaria and the captivity that follow, so the act carries forward into its consequences.

**Test.** The word was placed at the start of every Bible verse, and the tiny transformer from experiment 6 was trained on that text. On the same 40 new stories, the model writes the word *itself* after each story, then the endings are scored. **Control:** identical training, but with the spelling chosen at random, so it is the same extra word with no meaning. Each version was trained twice with different random starts.

### Results (50% = guessing)

| Model | Shift toward the right ending (main test) | Judges the act right vs. wrong |
|---|---|---|
| No shifting word (experiment 6) | 9/20 = 45% | 9/20 = 45% |
| Scrambled word, run 1 | 10/20 = 50% | 12/20 = 60% |
| Scrambled word, run 2 | 11/20 = 55% | 12/20 = 60% |
| **Shifting word, run 1** | **14/20 = 70%** | **14/20 = 70%** |
| **Shifting word, run 2** | **13/20 = 65%** | **14/20 = 70%** |
| Shifting word, both runs together | **27/40 = 68% (p = 0.02)** | **28/40 = 70% (p = 0.008)** |
| Scrambled, both runs together | 21/40 = 52% (p = 0.44) | 24/40 = 60% (p = 0.13) |

### What this shows
- **It moved off chance, twice, and the scrambled version didn't.** The gain comes from what the word *means*, not from adding an extra word.
- **It helped during training, not at answer time.** Handing the model the *correct* spelling gave exactly the same scores as letting it choose its own. So the word worked as a teacher: training on text where right and wrong are *marked* made the model better at recognizing them in new stories. This fits the thesis that what we do wrong naturally has to be *told*.
- **The plain "pick an ending" score stayed near 50%.** The model leans the right way after each act, but not far enough to overcome its built-in preference for certain endings.

### Caveats
- Both runs were tested on the **same 20 story pairs**, so the combined p-values overstate certainty. The consistency shows this is not luck in *training*, but 20 pairs is still a small test. **More test stories are the most important next step.**
- The word's values come from a good/evil direction built from four seed words each, so this is a form of supervision. No test story or ending influenced it; banned label words never appear in the tests.
- Small model, one book, about 12 minutes of training per run.

### About the numbers 17, 32, 16, 34, 47
Only 17 is used, as the reset size. In this design what matters is the *ratio* between the reset, the word values and the spending rate. Scaling everything by any number gives the same behaviour, so the specific value doesn't carry meaning by itself. The others could be tried as reset sizes or thresholds, but there's no reason yet to expect them to behave differently.

---

## Experiment 8: Confirmation on 100 new story pairs: not confirmed for consequences; strong signal for judging

**Design (pre-registered in `confirm.py`, committed before scoring).** I wrote 100 new story pairs ([`stories_v2.py`](stories_v2.py)) using KJV vocabulary, banned moral labels, and endings that never reuse story words. Three versions were trained with 3 seeds each: shifting word, scrambled control, and no word. The pre-registered measure was **predicting consequences** (the shift test). Judging right vs. wrong was a side measure. The old 20 pairs reproduced exactly for seeds 0 and 1 (14/20 and 13/20 for shifting; 10/20 and 11/20 for scrambled), so the code was unchanged. Raw results: [`results_confirm.json`](results_confirm.json).

### Pre-registered verdict
| Test | Result |
|---|---|
| Shifting word predicts consequences better than chance (majority of 3 runs) | **51/100, p = 0.46: NOT CONFIRMED** |
| Shifting word beats scrambled on consequences | 27 better, 27 worse: **NOT CONFIRMED** |

The 68% from experiment 7 did not hold on new stories. It was luck in the 20 original pairs.

### Everything else (descriptive, not pre-registered)

| 100 new pairs | Consequences per run | Judging per run |
|---|---|---|
| Shifting word | 50, 55, 55 (majority 51, p = 0.46) | **67, 72, 67 (majority 69, p = 0.0001)** |
| Scrambled | 49, 55, 50 (majority 50) | 56, 42, 60 (majority 53, p = 0.31) |
| No word | **62, 55, 61 (majority 61, p = 0.02)** | 49, 60, 40 (majority 51, p = 0.46) |

Pair by pair, the shifting word judged better than scrambled on 57 pairs and worse on 25 (p = 0.0003). Against no word it was 54 better and 26 worse (p = 0.001).

### What this means
- **The shifting word reliably improves *judging* right vs. wrong:** about 69% vs. about 50–55%, across all 3 training runs, on stories it never saw. Judging was a side measure here, so it still needs its own pre-registered confirmation.
- **It does not improve *predicting consequences*.** The plain model did slightly better there (61% majority). One possible reason: marked models read endings after the marker word, while the plain model reads them after a comma, so the formats differ. That is untested.
- **Next:** compare against the established method (a plain good/bad label per verse) to see whether the *carried* balance adds anything beyond labeling (`method_comparison.py`, experiment 10).

---

## Experiment 10: Method comparison: the shifting word vs the established method

**Question.** The shifting word improved *judging* right vs. wrong (experiment 8). Does that come from the owner's specific idea, the **carried balance**, or from **marking the text with moral labels at all**? The established version of the latter is "conditional training" (Korbak et al., ICML 2023, see [`PRIOR_WORK.md`](PRIOR_WORK.md)).

**Design (pre-registered in [`method_comparison.py`](method_comparison.py), committed before training; one later scoring fix, commit ca1f8c9, lets carry3 be scored over its 3 spellings, and gives identical results for the 5-spelling methods).** Same tiny model, same Bible, same 1,500 steps, same 100 new story pairs, and 3 seeds per method. The main measure was judging.
- **label:** the established method. Same five spellings and same position, but each one judges *only the verse before it*: no carry, no reset, no fading. It uses the same verdict phrases and word values as the shifting word, and the same share of each spelling.
- **carry3:** the owner's carried balance, but with only 3 spellings (wrong / unresolved / right).

### Results (judging right vs. wrong, 100 new pairs, 50% = guessing)

| Method | Per run | Average | Majority vote |
|---|---|---|---|
| No marker | 49, 60, 40 | 49.7% | 51/100 |
| Scrambled marker | 56, 42, 60 | 52.7% | 53/100 |
| **Shifting word** (carry, 5 spellings) | 67, 72, 67 | **68.7%** | 69/100 |
| **Plain good/bad label** (no carry) | 71, 69, 63 | **67.7%** | 73/100 |
| **Carry, 3 spellings** | 66, 72, 74 | **70.7%** | 75/100 |

Predicting consequences stayed near chance for every marked method (48–56%).

| Pre-registered test | Pair by pair | Verdict |
|---|---|---|
| Q1: shifting word beats the plain label | 20 better, 18 worse (p = 0.44) | **NOT CONFIRMED: a tie** |
| Q2: 5 graded spellings beat 3 | 23 better, 26 worse (p = 0.72) | **NOT CONFIRMED: a tie** |

Descriptive: the shifting word beats no marker (54 better, 26 worse, p = 0.001) and scrambled (57–25, p = 0.0003). The plain label also beats no marker (50–22, p = 0.0006).

### What this means
- **Marking the training text with moral labels clearly improves judging,** by about 18–21 points (average per run) over plain text, in every moral-label version tested. Scrambled markers did not help (52.7%). That part is real and repeatable.
- **The carried balance and the graded spellings didn't add anything measurable** at this scale. The plain per-verse label, the established method, did just as well.
- **Why the carry might not show up here:** the test stories are one sentence each, so there's no long story for a balance to carry across. A test with multi-sentence stories, where the decisive act comes early and the judgment is asked much later, would give the carry a chance to matter. That is the most direct next test of the owner's specific idea.

---

## Experiment 11: Long-story test: the carried balance works when an everyday act must be remembered

**Question.** The owner's idea is about carrying weight *forward* ("+4 remaining" into the next use). Experiment 10 used one-sentence stories, which never need that. Here the act comes first, then neutral sentences follow until **both the act and the first marker written after it** have scrolled out of the model's 64-token window. The model can only remember the act through markers it writes itself, passing them forward one sentence at a time. Script: [`long_story_test.py`](long_story_test.py). It reuses the 15 trained models, so no new training was needed.

**Versions**
- **A, an explicit verdict carried:** the act ends with "and he did evil in the sight of the lord" or "and he did that which was right in the sight of the lord". This triggers the owner's ±17 reset.
- **B, an everyday act carried:** the act alone, such as "the man took his neighbour's ox by night and sold it". The owner's rule doesn't treat this as a clear choice.

**Two corrections made during the first run** (both documented in the script). Neither changes a pre-registered verdict: with ties scored 0 instead of 0.5, L2 is 44 better vs 7 worse, L1 is 11 vs 72, and L3 is 19 vs 48. The second correction does, by design, remove a shortcut only the plain label could use.
1. **Ties count as 0.5.** A model that can't tell the two stories apart produces exact ties, and they had been counted as wrong.
2. **The first marker must also be out of view.** Otherwise the plain label could simply look back at it.

The flawed first-run results were set aside, not used. They were not committed and are lost with the session. The marker diagnostics quoted below (which markers the model wrote) were one-off checks, also not saved. To reproduce them, log the greedy markers in `judge_marked()`.

### Results (judging right vs. wrong, 100 pairs, 50% = guessing, 3 runs each)

| Method | Short (act in view) | **A: verdict carried** | **B: everyday act carried** |
|---|---|---|---|
| No marker | 49, 60, 40 | 50, 50, 50 | 50, 50, 50 |
| Scrambled | 56, 42, 60 | 44.5, 49.5, 57 | 50.5, 43.5, 52 |
| **Shifting word** | 67, 72, 67 | 45, 57, 62.5 | **59, 56, 63** |
| Plain good/bad label | 71, 69, 63 | **73, 51, 97** | 54.5, 51, 54 |
| Carry, 3 spellings | 66, 72, 74 | 71.5, 58.5, 54.5 | **59, 63.5, 59** |

| Pre-registered test | Pair by pair | Verdict |
|---|---|---|
| L1, version A: shifting beats label | 11 better, 74 worse | NOT CONFIRMED (the label won) |
| **L2, version B: shifting beats label** | **43 better, 21 worse (p = 0.004)** | **CONFIRMED** |
| L3, version A: 3-spelling carry beats label | 18 better, 50 worse | NOT CONFIRMED |

In version B the shifting word beat the plain label in **every one of the 3 training runs**: 59 vs 54.5, 56 vs 51, and 63 vs 54.

**Ties matter here.** Most long-story pairs are exact ties, scored 0.5. In version B the plain label tied on 91, 96 and 82 of 100 pairs: once the act is out of view it can't tell the stories apart, so it sits near 50% by design. The shifting word tied on 70, 70 and 54, and of the pairs it did decide, it got 24–6, 21–9 and 36–10 right. No marker ties on every pair in A and B. Descriptive, not pre-registered: in version B the 3-spelling carry also beat the plain label (45 better, 19 worse, p = 0.0008).

### What this means
- **The owner's carried balance does something a plain label doesn't.** When an everyday act has to be remembered after it has scrolled out of view, models trained with the carry keep their judgment of it alive: about 59–61%, against about 53% for the plain label. That is the first pre-registered support for the part of the idea that is the owner's own.
- **It's modest:** about +6 points over the plain label and about +10 over chance. All on a tiny model.
- **Version A went the other way, and a diagnostic shows why.** In a one-off diagnostic (run 1, 200 stories, not saved), the shifting word's first and last markers came out exactly the same: the same count for every combination, across all 200 stories. But it often *misjudged the verdict sentence itself*, writing "unresolved" or even "right" after "did evil". The first guess was that the test stories start without a marker, unlike training. The exploratory start-marker run below did not support that: with a start marker, the shifting word never changed its marker at all. The better explanation is that it **updates its marker too little** on new sentences.
- **Run-to-run swings are large** (the plain label scored 51 to 97 on version A), so several seeds are essential.
- **Known in principle, new in this form:** writing hidden state into the text helps models carry it past their window. Chess state-tracking (Toshniwal et al., 2022) and Decision Transformer (2021) are close relatives; see [`PRIOR_WORK.md`](PRIOR_WORK.md). What looks new is using a *moral* balance that is reset by clear choices and spent word by word, and showing it beats plain per-sentence moral labels at remembering an everyday act.

### Exploratory (not part of the verdict): starting each story with the neutral marker
Run: `python experiments/long_story_test.py --start-marker`. It was stopped early to free the CPU (all of run 1, part of run 2; [`results_long_story_startmarker.json`](results_long_story_startmarker.json)). The pre-registered comparison lines this partial run prints are meaningless, because they set different numbers of runs against each other.
- **Shifting word:** **50.0 in every case, all ties** (version A runs 1–2, version B run 1). Starting with "unresolved" made it copy "unresolved" all the way down, ignoring the act.
- **Plain label:** about the same as before (version A 71.5, version B 51.5).

**Lesson:** at this scale the shifting-word model leans so heavily on *carrying* its previous marker that it barely *updates* on new sentences. It carries perfectly but updates poorly. A better design should balance the two: for example, stronger resets, a faster spend rate, or training text where markers change more often. The owner's numbers (32, 16, 34, 47) could be tried here as reset or spend settings.

---

## Experiment 9: Aesop moral transfer: not confirmed

**Question (the owner's theory).** Do lessons taught through *stories* transfer to a culture never seen better than other text does? Test material: Aesop's own fables (Jacobs, 1894), never in training. For each pair of fables, the model must prefer the true fable→moral matching over the swapped one. Guessing scores 50%. Script: [`aesop_test.py`](aesop_test.py), version 3, revised twice after flaw checks and before any training. Full printout: [`results_aesop.txt`](results_aesop.txt); raw data: [`results_aesop.json`](results_aesop.json).

**Setup.** 67 fables; 1,131 same-format pairs; 284 pairs where shared words give no clue. Training sets of about 700k tokens each, with 4 training runs each for stories, novels and shuffled stories, 2 for the Bible, and 1 each for rules and narrative. Context window of 128 tokens, 1,500 steps.

### Results (percent of pairs matched correctly; 50% = guessing)

| Training set | Same-format pairs (4 runs) | Average | No-word-clue pairs | Unknown test words |
|---|---|---|---|---|
| **Folk tales** (9 collections, 8 cultures) | 54.9, 54.4, 50.9, 50.0 | **52.3** | **60.2** | 1.9% |
| Novels (control) | 52.3, 53.1, 54.3, 51.2 | 54.1 | 53.9 | 3.3% |
| Folk tales, sentences shuffled (control) | 47.4, 56.0, 53.7, 49.7 | 53.1 | 59.2 | 1.9% |
| Bible (2 runs) | 44.2, 45.1 | 43.6 | 39.4 | 9.3% |
| Rules (small, 1 run) | 50.0 | 50.0 | 54.4 | 14.2% |
| Bible narrative (small, 1 run) | 56.5 | 56.5 | 54.6 | 16.2% |

References with no model: word-family overlap 76.1% (same-format), 50.0% (no-clue). Punctuation shortcut 50.0%.

### Pre-registered verdict

| Test | Result |
|---|---|
| P1: each set beats 50% (sanity) | **NOT CONFIRMED for any set** (folk tales p = 0.33) |
| P2: folk tales beat novels | **NOT CONFIRMED:** folk tales were 1.8 points *lower* (fable-level p = 0.61, model-level p = 0.56) |
| P2b: folk tales beat shuffled folk tales | **NOT CONFIRMED:** 0.7 points lower (p = 0.59 / 0.36) |
| P3: folk tales beat 50% on no-clue pairs | **NOT CONFIRMED** (60.2%, p = 0.065; pre-declared as "inconclusive, low power" if null) |

Descriptive, not pre-registered:
- On no-clue pairs, folk tales were 6.3 points above novels (model-level p = 0.029, fable-level p = 0.22) and 1.1 above shuffled.
- Folk tales were 8.8 points above the Bible.
- Bible narrative was 6.5 points above rules (1 run).

None of these is a confirmation.

### What this means
- **The theory was not supported at this scale.** Tiny models trained on about 700k words didn't link Aesop fables to their morals better than chance, from any training set. They didn't even use the word-overlap clue that a simple word count exploits (76%). The test asked for more than these models can do.
- **The one hint** is that every story-based model scored around 59–60% on the no-clue pairs, against about 54% for novels. That hint is the same for real and shuffled stories, so it points to *story vocabulary and setting* (animals, folk situations), not story *structure*.
- **The Bible model fell below chance**, likely because Aesop's 1890s English is far from King James English (9.3% unknown words).
- **For communication:** this result says nothing yet about better communication. It shows that tiny models can't yet *apply a lesson from one culture's stories to another's*, and that bigger models or more text would be needed to test the theory fairly.
