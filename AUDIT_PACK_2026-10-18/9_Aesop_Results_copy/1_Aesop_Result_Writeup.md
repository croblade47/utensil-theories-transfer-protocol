# Aesop Test Results: Do Stories Teach Lessons That Transfer?

18 October 2026 · Experiment 9 · Branch `ccr-1be0d913-1tlzao`

## The answer in one line
**Not confirmed.** Tiny models trained on folk tales did not match Aesop's fables to their morals better than chance, and did no better than models trained on novels or on shuffled stories.

## What this means for communication
This result says nothing yet about better communication. It shows that tiny models can't apply a lesson from one culture's stories to another culture's fables. Testing the theory fairly needs bigger models or much more text.

## The question
The owner's theory: lessons taught through **stories** carry more transferable meaning than lessons taught as rules or plain prose.

## How it was tested
- **Test material:** Aesop's own fables (1894 edition). No model ever saw them in training.
- **The task:** take two fables and their two morals. The model must prefer the true matching over the swapped one. Guessing scores 50 out of 100.
- **Size:** 67 fables, giving 1,131 fair pairs and 284 "no word clue" pairs, where no shared word gives the answer away.
- **Training sets,** about 700,000 words each:
  - folk tales from 9 collections and 8 cultures: German, Celtic, Indian, Japanese, Chinese, Arabian, West African, and two Dakota collections written by Dakota authors;
  - the same folk tales with sentences shuffled inside each story block (control);
  - novels by Austen, Chesterton and Melville (control);
  - the King James Bible;
  - plus a small rules-only set and a small Bible-stories set.
- **Training runs:** 4 per set for folk tales, novels and shuffled folk tales.
- **Pass/fail rules** were saved to git before any training. The test was checked for flaws twice before it ran.

## Results (right per 100 pairs; 50 = guessing)

| Training set | Fair pairs | No word clue |
|---|---|---|
| Folk tales | 52 | 60 |
| Novels | 54 | 54 |
| Shuffled folk tales | 53 | 59 |
| Bible | 44 | 39 |
| Rules only (small) | 50 | 54 |
| Bible stories (small) | 57 | 55 |

## Pass/fail verdict (all decided in advance)

| Test | Result | Size |
|---|---|---|
| P1: each set beats guessing | **Fail** for every set | folk tales 52 vs 50 |
| P2: folk tales beat novels | **Fail** | folk tales about 2 fewer right per 100 |
| P2b: folk tales beat shuffled folk tales | **Fail** | about 1 fewer per 100 |
| P3: folk tales beat guessing on no-clue pairs | **Fail** (inconclusive, low power) | 60 vs 50, p = 0.065 |

## The one hint (not a confirmation)
- **On no-clue pairs,** every story-based model scored about 59–60, against about 54 for novels.
- **But the shuffled stories scored just as well.** So the hint points to story vocabulary and setting (animals, folk situations), not story *structure*.
- **The Bible model scored below guessing.** A likely reason: Aesop's 1890s English is far from King James English (9 in 100 test words unknown to it).

## Where the whole project stands
- **Strong and repeated, not yet pre-registered as the main measure:** marking right and wrong in the training text makes a tiny model judge new stories better, about 69 vs 50 right per 100.
- **The owner's carry idea:** supported once in long stories, about 6 more right per 100 than a plain good/bad label. That came from a re-run after two fixes. It's shaky: about 65 of 100 pairs were ties, and on the rest it was right 81 times and wrong 25.
- **Did not work:** predicting consequences, and now story-to-moral transfer across cultures.
- **Not yet tested:** communication itself, and anything on a full-size AI.

## Next step (waiting for the owner's approval)
**A conversation test.** Does a carried marker help a model stay true to what a person said early in a long conversation? The owner approves its pass/fail rules first.
