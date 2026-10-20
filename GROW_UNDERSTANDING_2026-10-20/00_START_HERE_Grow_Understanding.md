# START HERE: Growing Understanding (20 October 2026)

## What this folder is
The test of the owner's question: *"Can I grow understanding and compression?"*

The idea: two sides share a **greenhouse**, knowledge both already have. The **seed** only has to carry what the greenhouse cannot already predict. If that's right, a greenhouse that understands more needs a smaller seed to regrow the exact message.

This folder holds four things:
- the experiment that measured this (the "greenhouse ladder");
- an independent check of it;
- a brute-force dig through the whole chat for the owner's greenhouse pieces;
- a fact check of the published work, and where the owner's credit could come from.

## The verdict

1. **Yes: understanding shrinks the seed, and it regrows exactly.**
   - The tiny model trained on the Bible regrew 623 verses it had never seen from a 12.2 KB seed, against 83.8 KB of text: **85.4% smaller, byte for byte exact.**
   - That is **less than half** the size xz needs (26.4 KB) and well under zip (28.6 KB).
   - Every rung of shared understanding gave a smaller exact seed.
2. **The shifting word did not make the model a better grower** (pre-registered test, not confirmed).
   - With the markers paid for, seeds were about 2% bigger.
   - Even with the markers given for free, the words were no cheaper.
   - The shifting word tied the scrambled control. Its earlier gains were in *judging right and wrong*, not in *predicting what comes next*.
3. **The palm seed in Antarctica, measured.** Decoding with 1 thread instead of 2 broke the regrowth after 547 of 623 verses. A greenhouse made of decimal numbers must be rebuilt identically on the receiving side, or the seed dies partway through. The whole-number rungs don't have this problem.
4. **The principle itself is already published,** so it can't be the owner's credit: understanding = prediction = compression (Shannon 1951, the Hutter Prize, Delétang et al. 2023, Huang et al. 2024). Where credit could still come from is listed below.

## The ladder (same 83,757-character text, every seed regrown exactly)

| Greenhouse (more understanding further down) | Seed | Smaller than raw |
|---|---|---|
| None: raw text | 83,757 bytes | 0% |
| A shared word list, every word equally likely | 31,262 | 62.7% |
| Zip | 28,565 | 65.9% |
| Zip with a shared 32 KB library ("strawberry and orange" in plainest form) | 27,625 | 67.0% |
| xz | 26,420 | 68.5% |
| Word frequencies | 19,773 | 76.4% |
| Word pairs | 14,864 | 82.3% |
| **Tiny Bible model (3 runs)** | **12,153–12,252** | **85.4%** |
| Tiny model + shifting word (markers paid for) | 12,411–12,524 | 85.1% |

**The greenhouse built step by step.** Letting the model see more of what came before shrinks the seed:

| Words the model can see | Seed |
|---|---|
| 1 | 15,111 bytes |
| 2 | 13,800 |
| 4 | 13,020 |
| 8 | 12,508 |
| 64 | 12,252 |

Each instruction given makes the next one cheaper to send. That's what happened in this chat.

## The story version (for explaining it to others)
- **The soil** is the text both sides already have: the Bible, the stories.
- **The greenhouse** is what was built from the soil: a word list, then word habits, then a small model that has read the Bible. Both sides build the same one in advance.
- **Humidity and the turning sun** are the fixed rules both sides follow in lockstep. If one side's sun turns a little differently (1 thread instead of 2), the plant dies partway.
- **The coin toss** is every word. A fair coin costs 1 bit. A greenhouse that understands tilts the coin toward what really comes next, so a likely word costs a fraction of a bit. *"Shift the coin toss towards the desired outcome"* was the owner's own phrase on day 1. It's exactly the right unit.
- **The seed** is only the surprises: the tosses that landed against the tilt, plus spelled-out words the greenhouse has never met (the cucumber).
- **Checking the air and the bugs** means proving the plant is the same plant: every regrown text is fingerprinted against the original.
- **The child learning to grow food:** the same model that understands (predicts) is the one that grows (writes). Feed it random coin tosses and it writes new Bible-like text. Feed it the seed and it writes back the exact message.

## The final piece: what the dig through the chat found
The owner said the final piece was already in this chat. The strongest candidates, in order:

1. **The coin toss is the unit.**
   - Every 0/1 point on the "page of binary" is a coin toss. The greenhouse tilts each toss, and the seed records only the surprises.
   - That is arithmetic coding: seed size equals how surprised the model is, so understanding and compression are one number.
   - The number was in the chat from day 1: the model's held-out loss predicted about 11.7 KB. The real coder measured 12.2 KB.
2. **The library (strawberry and orange vs cucumber).** Items already on the shared shelf cost only a call number.
   - With the Bible on the shelf, naming one verse costs about 1.9 bytes against 132.5 bytes: **98.6% smaller and exact**. That is almost exactly the owner's 98.9%.
   - It may explain the earlier results in other AI chats, and why those needed "huge files": the library is the huge file. This is a likely explanation, not a proven one.
   - The limit: it only works for what is already on the shelf. Understanding (piece 1) is what works on new text.
3. **The conversation itself is a growing greenhouse.** Shared context let late messages like "Use a graph system lol" carry big instructions. That is compression of communication, the owner's original objective.
4. **The seed expression is a mirror image.**
   - Reverse the left half of `[+2×y(27/5.2+t=y/?)÷(?\y=t+2.5\72)yx2]` and mirror each sign (/ to \, ( to ), × to x), and you get the right half exactly. Only the leading + has no partner. This was re-checked by computer and is exact.
   - "Worked backwards" is built into the seed: growing is planting run in reverse.
5. **"Remaining" as an excess bank.** The owner's rule [w1 = 17 − 13 = +4 Remaining] and "W1 = 17 + 4" carries the leftover forward. That is the same principle that makes arithmetic coding exact. The project switched this part off (RECHARGE = False), so the owner's exact rule **has never been tested.**

The full dig, with every piece and quote, is `reports/chat_dig_greenhouse_map.md`.

## Where the owner's credit could come from
- **Already exists** (not claimable):
  - understanding = compression;
  - regrowing exact data from a seed plus a shared model;
  - shared dictionaries, like Brotli's built-in 122,784-byte one;
  - finding data on a fixed page (the πfs joke);
  - marker tokens in training (CTRL 2019, MeCo 2025).
- **Could still be new:**
  1. **A measured result for a specific training idea.** A carried right/wrong balance that makes a small model a better exact compressor of stories it never saw would count. The shifting word in its current form did not do this. The owner's untested "17 + 4" recharge rule is the next candidate. An honest negative result is also publishable.
  2. **"Seed bits as an understanding meter":** a teaching protocol. Measure how many bits a model needs to regrow a story exactly, before and after it is taught a lesson. The drop is understanding gained, in plain numbers.
  3. **The plain-language greenhouse story** as a way to teach this to people. That's authorship credit, not discovery credit.

## Timeline of what was done
1. **Morning:** the seed test and graph method (folder `SEED_TEST_2026-10-20/`). The graph method regrows exactly but only shrinks patterned data.
2. **The owner's greenhouse message.** "Use some brute force discovery… can I grow understanding and compression?"
3. **Discovery run in parallel:**
   - a dig through all 34 of the owner's messages;
   - a fact check of 21 published results (web-search extracts; direct page fetches were blocked in this sandbox).
4. **First ladder attempt stopped** when the session hit its usage limit. Restarted after the reset, reusing the finished dig and fact check.
5. **The ladder built and run** (`understanding_compression.py`, about 24 minutes):
   - 24 exact seeds;
   - 23 distinct full decodes, all byte for byte equal to the original.

   The pre-registered question was written into the script before it ran on the held-out verses.
6. **Independent check: PASS.**
   - The checker rebuilt the text and the split, and found no leakage.
   - They recomputed the simple rungs with their own code.
   - They regrew 50 verses with a coder of a different design.
   - They reproduced the seed fingerprints and recomputed every statistic.
   - They found the thread-count fragility (point 3 of the verdict).
7. **Records updated:** experiment 12 written into `experiments/README.md` and `experiments/HANDOFF.md`.

## Technical details
- **Text regrown.** The held-out verses: every 50th verse, which no model trained on. That is 623 verses and 83,757 characters, normalized to lowercase words and . , ; : ? ! for every rung alike. Capitals and verse numbers were dropped for every rung.
- **Coder.**
  - An exact integer arithmetic coder.
  - Probabilities are rounded to whole numbers the same way on both sides (frequency = max(1, floor(p × 2^20))).
  - Unknown words are spelled out letter by letter inside the seed.
  - Each seed is a 4-byte header plus the coded bits.
- **Greenhouses** were built only from training verses:
  - word list: 8,576 words;
  - word pairs: 132,894 pairs;
  - tiny transformer: about 3.4 million numbers, about 13.8 MB.

  The greenhouse is shared once in advance and not counted in any seed. It pays off only when reused for many messages.
- **Statistics.** Paired verse by verse, sign test and permutation test (100,000 flips).
  - Shifting word vs plain model: +3.45 bits per verse; larger on 496 of 623 verses. One-sided p = 1.0, so not confirmed.
  - Words only: +0.44 bits per verse.
  - Shifting word vs scrambled control, words only: +0.04 bits per verse, p = 0.69 (a tie).
- **Checker's minor notes, corrected here:**
  1. **Decode count.** "24 of 24 decodes" in the printed results is 23 distinct decodes; the k = 64 row reuses the plain-model run.
  2. **Greenhouse size.** The size printed (3,439,680 numbers) is the shifting model's. The plain model has 3,438,720.
  3. **Number setup.** Exactness needs the identical software and thread settings. It was tested, and it fails with a different thread count.
  4. **Marker layout.** In this layout each held-out marker depends on neighbouring training verses that are not in view, which makes markers harder to predict. The words-only measure shows no gain either, so the conclusion stands.
- **Versions.** Python 3.13.16, torch 2.14.1, numpy 2.5.3, 2 threads, 4-core machine.
- **To run it:** `cd experiments && python understanding_compression.py`. It needs the saved models in `experiments/models/` and the Bible text in `experiments/data/`; both are kept out of git because of their size. The Bible text downloads itself on the first run, from the same public source the other experiments use. The models are rebuilt by the project's training scripts (`confirm.py`, `method_comparison.py`).

## Every file in this folder

| File (path inside this folder) | What it is | Where the original lives |
|---|---|---|
| `00_START_HERE_Grow_Understanding.docx` / `.md` | This guide (Word file, plus a text copy) | branch `ccr-1be0d913-1tlzao`, `GROW_UNDERSTANDING_2026-10-20/` |
| `code/understanding_compression.py` | The ladder experiment: exact arithmetic coder, every rung, statistics | `experiments/understanding_compression.py` (same branch) |
| `results/results_understanding.txt` | The printed result tables | `experiments/results_understanding.txt` |
| `results/results_understanding.json` | Every number: seed sizes, fingerprints, per-verse bits, tests | `experiments/results_understanding.json` |
| `reports/ladder_build_and_check.md` | The builder's full report and the independent checker's report | made from this session's work; only here |
| `reports/chat_dig_greenhouse_map.md` | Every greenhouse piece from the chat, the final-piece candidates, the owner's numbers | made from this session's work; only here |
| `reports/fact_check_and_credit.md` | 21 published facts with sources, and what is or isn't claimable | made from this session's work; only here |
| `GROW_UNDERSTANDING_2026-10-20.zip` (next to the folder) | This whole folder as a plain zip | repository top level |

Related folder: `SEED_TEST_2026-10-20/` holds the data-seed test and the graph method, with its own guide and zip.

## Things outside this folder's control
- **The repository is public** on GitHub (MIT license): anyone can read these files. Changing that is the owner's decision, in GitHub settings.
- **A cloud session can't place files on your devices.** It cannot put files on your laptop or phone directly; the files are sent to you in the app to save.
- **The trained models and the Bible text are not in git** (about 430 MB of models; the 15 used here are about 210 MB). They live only on this cloud machine, which is deleted after the session. The training scripts can rebuild them, which takes several hours. Without the identical models, the seeds can't be regrown, because the models are the greenhouse.
