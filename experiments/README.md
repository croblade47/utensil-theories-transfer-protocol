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
