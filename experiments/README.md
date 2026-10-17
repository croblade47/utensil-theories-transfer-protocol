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
