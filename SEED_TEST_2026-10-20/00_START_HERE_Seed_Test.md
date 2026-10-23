# START HERE: Seed Test (20 October 2026)

## What this folder is
A fair test of the owner's "data seed" idea: a tiny seed plus fixed, shared grow instructions should regrow the exact original data. It needs no AI, only Python on any computer.

This folder also holds the owner's **graph method**, built three ways (the three closest readings of the owner's description), and the results of running each one through the fair test.

## The verdict so far

**Every method regrew every file exactly (5 of 5 files each), and independent checkers passed all three graph methods as fair.**

| Test file | Zip (for comparison) | Graph: fit the shape | Graph: work backwards | Graph: find it on a fixed page |
|---|---|---|---|---|
| Repeating pattern, 120,000 bytes | 99.8% smaller | **99.99%** (11 bytes) | **99.99%** (10 bytes) | 0% |
| Short text, 267 bytes | 66.3% | 64.4% | 63.7% | -1.5% |
| Bible text, 100,000 bytes | 70.2% | 19.3% | 6.2% | 0% |
| Word file, 11,110 bytes | 9.9% | 1.5% | 1.9% | 0% |
| Random bytes, 100,000 | 0% | 0% | 0% | 0% |

What it means, in plain words:
- **The seed works where the data is a pattern.** A repeating pattern shrinks to 10 or 11 bytes, beating zip. That is where the owner's 98.9% shows up.
- **It does not work on everyday text or files.** Words are not shaped like lines, curves or cycles, so the graph method keeps most of the text as it is (the "cucumber"). Zip does better on text.
- **Random data never shrinks, with any method.** This is the counting limit: there are more possible files than short seeds.
- **Finding data on a fixed page never saves space.** Naming a spot on the page costs as many 0s and 1s as the piece found there. The checkers confirmed this on fresh files too.
- **Strawberry, orange and cucumber are placeholder names** in the code. The owner has not yet shared their own factors. If the owner's real factors work differently, they can be dropped into a new method file and tested the same way.

## Timeline of what was done
1. **Seed test made (morning).** A fair, AI-free test with an example method (ordinary zip).
2. **Test upgraded.** It now runs several methods side by side, and grows each seed in a separate program inside an empty folder, so the grower cannot peek at the original.
3. **Graph method built three ways.** One builder for each reading of the owner's description:
   - **Fit the shape** (`graph_fit`): the expression is the shape of the data.
   - **Work backwards** (`graph_backwards`): solve back from the data to the expression's unknowns.
   - **Find it on a fixed page** (`graph_locate`): one expression grows an unchanging page of 0/1, and the seed lists positions on that page.
4. **Each method independently checked.** A separate checker tried to break each one. Checks covered:
   - hundreds of round trips;
   - fresh files the builder never saw;
   - fairness: no peeking, no hidden zip, nothing tailored to the test files.

   All three passed. Only minor notes were found, listed in `checks/graph_methods_reports.md`.
5. **All methods re-run together** on the final files. The numbers matched the checkers' numbers (`results_graph_methods.txt`).
6. **Next (running now):** the "greenhouse" test. It measures whether shared understanding (a model trained on the Bible) lets a much smaller seed regrow text exactly. It also measures whether the owner's shifting word makes the model a better grower. This will be added here when it finishes.

## Technical details
- **The four methods.** Each one is a file in `methods/` with two functions: `plant(data) -> seed` and `grow(seed) -> data`.
- **Separate grower.** Each seed is grown by a separate `python -I` process, started in an empty temporary folder holding only `seed.bin`.
- **Exactness check.** The regrown bytes are compared with the original by SHA-256 fingerprint.
- **What counts as seed size.** Every byte the grower needs (lengths, flags, settings) is inside the seed. The grow instructions (the test script plus the method file) are counted once and are the same for every file.
- **No hidden tools.** The graph methods use no zip or other compressor, only adding, subtracting, multiplying and remainders.

## How to run it yourself
1. Run `python seed_test.py` to test every method on the built-in test files.
2. Run `python seed_test.py --method graph_fit photo.jpg letter.txt` to test one method on your own files.
3. To try your own rules, copy any file in `methods/`, rename it, and change `plant()` and `grow()`.

## Every file in this folder

| File (path inside this folder) | What it is | Where the original lives |
|---|---|---|
| `00_START_HERE_Seed_Test.docx` / `.md` | This guide (Word file, plus a text copy) | branch `ccr-1be0d913-1tlzao`, `SEED_TEST_2026-10-20/` |
| `seed_test.py` | The fair test. Runs every method, grows in a separate process, checks exactness | same branch and folder |
| `methods/graph_fit.py` | Graph method, "fit the shape" | same branch, `SEED_TEST_2026-10-20/methods/` |
| `methods/graph_backwards.py` | Graph method, "work backwards" | same |
| `methods/graph_locate.py` | Graph method, "find it on a fixed page" | same |
| `results_graph_methods.txt` | Output of the full run of all four methods | same folder |
| `checks/graph_methods_reports.md` | Full builder reports and independent checker reports for each method | same branch, `SEED_TEST_2026-10-20/checks/` |
| `test_inputs/kjv_first_100k.txt` | First 100,000 bytes of the King James Bible (public domain), used as a text test | made from `experiments/data/KJV.txt` (not in git) |
| `test_inputs/sample_word_file.docx` | An 11 KB Word file, used as a document test | copy of `TECHNICAL_REPORT_2026-10-20/00_START_HERE_Technical_Report.docx` |
| `SEED_TEST_2026-10-20.zip` (next to the folder) | This whole folder as a plain zip | repository top level |

## Things outside this folder's control
- **The repository is public** on GitHub (MIT license): anyone can read these files. Changing that is the owner's decision, in GitHub settings.
- **A cloud session can't place files on your devices.** It cannot put files on your laptop or phone directly; the files are sent to you in the app to save.
