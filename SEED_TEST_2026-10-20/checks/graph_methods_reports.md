# Graph methods: builder reports and independent checks (20 October 2026)

Each method was written by one builder and then checked by a separate checker that tried to break it. These are their full reports, copied as returned.


---

## graph_fit

**Checker verdict: PASS** (checker re-ran the builder's numbers: matched). Fix stage needed: no.


### How it works

Every byte is 8 binary points stacked in a column, so a file is a page of 0/1 points 8 rows tall. The planting side looks through the whole page for stretches that a small expression regrows exactly. An expression is a few starting numbers plus a fixed step rule that adds, subtracts and multiplies earlier points, mod 256. Examples are a repeating cycle, a constant run, a straight line, a curve, several lines taking turns, or multiply-and-add. A shortest-path search then picks the mix of expression stretches and leftover gaps that makes the seed smallest. The leftover gaps (cucumber) are written row by row. A row that is a flat line, or a flat line with a few points off it ("dents"), costs one point plus about one byte per dent. Rows that are neither are stored as they are. The receiver needs only the seed and the fixed rules in the method file: it reads the records one by one and solves each expression step by step to regrow the exact bytes. The planting side regrows the seed itself before sending, as a proof that the round trip is exact.


### The library (strawberry / orange / cucumber, placeholder names)

These are placeholder names (stated in the file's docstring) until the owner shares their own factors. ORANGE means round, repeating expressions: a constant run (the same number again and again) and a cycle (a motif of 2 to 256 numbers going round). Step rule: next = the number one round back, factors (1). STRAWBERRY means straight-line and steady-step expressions: a line adds the same step each time, factors (2, -1). A curve's step grows steadily, factors (3, -3, 1). Woven lines/curves are 2 to 32 lines (or 2 to 8 curves) taking turns, for example counters stored as 2- or 4-byte numbers. Multiply-add means next = previous × m + c. Library rule: an expression must keep working for at least one full round past its starting numbers, so a cycle must go round at least twice. CUCUMBER is the odd one out: a stretch no fruit expression fits, stored as it is. The bit-level plot is part of cucumber: within a cucumber piece, a row of the 0/1 page that is a flat line (all 0 or all 1), or a flat line with a few dents, is given as the line plus the dent positions instead of point by point. The file defines 9 record kinds: cucumber, cucumber with flat rows, cucumber with line rows plus dents, orange constant, orange cycle, strawberry line, curve, woven and multiply-add.


### What the seed contains

Empty input gives an empty seed (0 bytes). Otherwise the seed is a plain sequence of records, with no global header, file name or total length; grow() reads records until the seed ends.

Every record starts with 1 byte: the top 4 bits are the kind (0 to 8), the bottom 4 bits are a length field. Values 0 to 14 are used directly; 15 means a varint follows (7 bits per byte, high bit = more bytes) holding field-15. The field is the stretch length minus the entry's minimum length: L-1 for the cucumber kinds, L-2 for constant, L-2p for a cycle, L-3 for a line, L-4 for a curve, L-(k+1)p for woven, L-4 for multiply.

What follows depends on the kind:
- 0, cucumber: the L bytes as they are.
- 1, flat rows: 1 mask byte (which rows are perfectly flat). Then a bitstream: the m flat-row values (top row first), then for each byte its 8-m other row points (top first), zero-padded to whole bytes.
- 8, line rows: a 2-byte row plan (2 bits per row, row 7 in the top bits; 00 = stored, 01 = line at 0, 10 = line at 1). Then for each line row (top first): a varint dent count followed by varint gaps between dents. Then the stored rows' points packed per byte, zero-padded.
- 2, constant: 1 byte (the value).
- 3, cycle: varint(p-2), then the p motif bytes.
- 4, line: 2 starting bytes.
- 5, curve: 3 starting bytes.
- 6, woven: varint((p-2)*2 + (k-2)), then k*p starting bytes.
- 7, multiply-add: 3 bytes (start, m, c).

Examples measured:
- "ABC123"×20000 gives an 11-byte seed: header byte + 3-byte varint length + 1 setting byte (p-2 = 4) + "ABC123".
- 100,000 random bytes give a 100,004-byte seed: header byte + 3-byte varint + the raw bytes.


### Builder's test results

```
Methods: graph_fit
Test files: random bytes (no pattern at all) (100,000 bytes), repeating pattern (120,000 bytes), short ordinary text (267 bytes), kjv_first_100k.txt (100,000 bytes), sample_word_file.docx (11,110 bytes)

=== Method: graph_fit ===
Cuts the data into stretches: a stretch that a small add/subtract/multiply expression regrows exactly (strawberry lines and curves, orange cycles) is stored as that expression, rows of the 0/1 page that are flat lines are stored as a line plus its dents, and the rest is stored as it is (cucumber).
test file                           original      seed reduction  exact?  plant s  grow s   xz size
random bytes (no pattern at all)     100,000   100,004     -0.0%     YES     1.96    0.06   100,064
repeating pattern                    120,000        11    100.0%     YES     2.22    0.04       160
short ordinary text                      267        95     64.4%     YES     0.01    0.05       152
kjv_first_100k.txt                   100,000    80,677     19.3%     YES     4.57    0.07    26,940
sample_word_file.docx                 11,110    10,945      1.5%     YES     0.43    0.05    10,060
Grow instructions (the test script + this method's file) are 40,698 bytes; they are shared once, not sent with each seed.

=== Summary: total seed bytes vs total original bytes, and exact regrowth ===
graph_fit              seeds     191,732 of 331,377 bytes  ( 42.1% smaller)   exact: 5/5 files
```


### Why each file got its result

Random bytes (-0.0%, seed 100,004): random data has no shape, so no expression fits. It is one cucumber record, and the 4-byte header makes the seed slightly bigger than the data. Zip is also bigger (100,041).

Repeating pattern (shown as 100.0%; really 99.99%, 11 bytes): "ABC123" repeated is exactly an orange cycle of length 6. The seed is the header, the cycle length and "ABC123". This is the only file near the claimed 98.9%, and it is trivial; zip gets 99.8% (204 bytes).

Short text (64.4%, 95 bytes): each of its two sentences is repeated 3 times back-to-back, so each is an orange cycle. The seed stores each 45- and 44-byte sentence once, plus about 3 bytes each. Zip gets 66.3% (90 bytes), because it also gives frequent letters shorter codes.

KJV (19.3%, 80,677 bytes): words are not lines, curves or cycles, so almost the whole file is cucumber. The gain comes from two rows of the 0/1 page:
- The top row (128s) is 0 except at 330 non-ASCII bytes. It costs about 0.4 KB as dents instead of 12.5 KB stored.
- The 32s row is 1 except at 5,156 capitals, brackets and line breaks. It costs about 5.2 KB as dents instead of 12.5 KB.
- The other 6 rows are stored as they are: 75,000 bytes.

Only 2 tiny cycles (62 bytes) were used. Zip gets 70.2% by copying repeated phrases and giving frequent letters shorter codes; neither is part of the graph idea, so this method does not do them.

DOCX (1.5%, 10,945 bytes): a .docx is a zip of already-compressed XML, so its bytes look random. Only the small plain-ASCII header and file-name parts (907 bytes) shrink, through flat rows. Zip gets 9.9% mainly by copying the repeated file names and headers.

Summary line (42.1% smaller): this total is dominated by the 120,000-byte repeating-pattern file. Without that file, graph_fit is 191,721 of 211,377 bytes, 9.3% smaller. Zip on the same four files is 139,955 of 211,377, 33.8% smaller.

Fairness decisions that lowered numbers:
- I made "an expression must go round at least once more than its starting numbers" a library rule. In an earlier version, 284 of the 287 "cycles" found in the KJV were really repeated phrases seen about 1.15 times, which is zip's copy trick in disguise. Removing them cost about 0.7 points on the KJV (84,230 vs 84,961 bytes in that version).
- I did not tune the split-penalty setting to the test files (other values changed results by ±0.1%).

Changes that raised numbers, both within the bit-level-plot idea:
- An exact-quality cut-point search for the flat-row pieces.
- "Line rows with dents". This took the KJV from 84,961 to 80,677 bytes.

No zlib/lzma/bz2 or other compressor is used. The method imports only re, bisect and collections.


### Builder's own exactness tests

Round trips (grow(plant(x)) == x), run in-process: 881 cases, 0 failures, 0 self-check fallbacks.
- Edge cases: empty bytes, every one of the 256 single-byte inputs, and 1,000 os.urandom bytes.
- Lengths 2–39, 127–129, 142–144, 255–257, 511–513, 1000, 4096, 16399–16401 and 70000 for each of 12 data families: random, text-like, sparse-caps ASCII, constant, line, curve, multiply-add, 16-bit and 32-bit counters, random-motif cycles, and mostly-constant with rare dents.
- A 17,775-byte mixture of all of these.
- The harness short text, KJV, docx, ABC123×20000, 100k os.urandom, and the harness's own .py source.

Timings in the suite: slowest plant 4.77 s (KJV), slowest grow 0.04 s. The harness run (grow in a separate `python -I` process in an empty folder) was exact on 5/5 files.

Determinism: planting each harness input twice gave identical seeds.

The search that cuts cucumber gaps into flat-row pieces was checked against a brute-force exact search on 2,500-byte samples. It matched within 1 byte: 2087 vs 2087, 2110 vs 2109, 2502 vs 2502.

The test scripts are in /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/graph_fit_agent/ (gf_roundtrip.py, gf_explain.py, gf_tune.py). Other agents (graph_backwards, graph_locate) share that scratchpad and once overwrote my rt.py, so I moved to this private subfolder. That did not affect any reported number.

Nothing else was edited, and nothing was committed, pushed or sent.


### Checker's issues

- **minor**: The docstring says "Every step rule here can also be run backwards". That is false for multiply-add when m is even. The finder accepts even m (it only needs the first step difference to be odd), and next = previous x m + c is not reversible mod 256 when m is even.  
  Evidence: plant(bytes([0,1,3,7,15,31,63,127,255,255,255])) gives seed 77000201, one multiply-add record with m = 2. Going backwards from 255 is ambiguous: both 127 and 255 lead to 255. The round trip is still exact; only the 'worked backwards' claim in the docstring is wrong.
- **minor**: The docstring says longer lengths spill into "1 to 3 more bytes". For a stretch longer than about 2,097,167 bytes the varint needs 4 bytes. The code handles this correctly; only the text is off.  
  Evidence: 2,500,000 zero bytes planted to a 6-byte seed starting 2f 8fcb9801 (header byte plus a 4-byte varint) and regrew exactly.
- **minor**: Plant time grows with file size at roughly 50 s per MB. It is well inside the limit at the test sizes, but a multi-MB file such as a photo would take minutes. Even trivial data pays for the whole-file cucumber pass, which always runs first.  
  Evidence: The first 2.3 MB of KJV.txt: plant 115.8 s, grow 0.43 s, exact. 2.5 MB of zeros: plant 30.9 s (6-byte seed). At 120 KB the worst adversarial input took 13.0 s with 8 runs in parallel, and grow was at most 0.10 s.


### Checker's fresh-file results

```
python3 seed_test.py --method graph_fit <fresh files>   (zip_example on the same files, run the same way, shown in [brackets])
test file                           original      seed reduction  exact?  plant s  grow s   xz size
random bytes (no pattern at all)     100,000   100,004     -0.0%     YES     1.85    0.05   100,064   [zip 100,041, -0.0%]
repeating pattern                    120,000        11    100.0%     YES     2.07    0.06       160   [zip 204, 99.8%]
short ordinary text                      267        95     64.4%     YES     0.01    0.06       152   [zip 90, 66.3%]
fresh_random_sha256_50k.bin           50,000    50,004     -0.0%     YES     0.84    0.05    50,060   [zip 50,026, -0.1%]
fresh_kjv_middle_60k.txt              60,000    48,221     19.6%     YES     2.37    0.06    19,148   [zip 20,932, 65.1%]
fresh_stories_v2_first20k.py          20,000    15,408     23.0%     YES     0.45    0.06     5,800   [zip 6,091, 69.5%]
fresh_tech_report_first20k.md         20,000    16,118     19.4%     YES     0.87    0.05     8,808   [zip 9,141, 54.3%]
Summary: graph_fit seeds 229,861 of 370,267 bytes (37.9% smaller), exact 7/7. zip_example: 186,525 (49.6% smaller), exact 7/7.
The fresh files:
- 50,000 bytes from a SHA-256 counter stream (not os.urandom).
- 60,000 bytes from the middle of experiments/data/KJV.txt (offset len/2+12345, Psalm 71 onward).
- The first 20,000 bytes of experiments/stories_v2.py.
- An extra file: the first 20,000 bytes of TECHNICAL_REPORT_2026-10-20/1_Seed_and_Grow_Technical_Report.md.
The method generalises the way the builder described: about 19–23% on text and code, and -0.0% on random data.
```

### Checker's notes

I re-ran the builder's command and it matched their table byte for byte, random file included: 100,004 / 11 / 95 / 80,677 / 10,945, 191,732 of 331,377 (42.1%), exact 5/5. Plant on KJV took 4.17 s here.

1. Exactness. grow(plant(x)) == x on all of these, with 0 failures and 0 self-check fallbacks:
- 513 directed cases: empty, all 256 single bytes, 120 random inputs of length 1–5000, zeros and 0xFF up to 70,001 bytes, alternating patterns, Unicode text, the owner's seed expression, KJV middle slices from 1 to 120,000 bytes, seed_test.py and graph_fit.py source, lines, curves, multiply-add, cycles, u16/u32 counters, float32, sparse dents, high-bit text, 0/1 byte pages, and random and text inputs at every header-length boundary.
- 4,500 fuzz mixtures of small-alphabet, line, curve, multiply, constant, cycle and woven segments, built to stress overlapping fits in the DP.
- 8 adversarial 120 KB inputs and 2 inputs over 2 MB.
- A separate `python -I` process in an empty folder, given only the seed, grew 12 chosen cases exactly.
- Planting the same input twice gives the same seed.
The plant-side "send raw if self-check fails" safety net never fired, so it is not hiding encoder bugs.

2. Fairness. The only imports are re, bisect and collections. There is no open/os/sys/time/random/hash, no zlib/lzma/bz2, and no data-specific literals (no ABC123, Bible words or docx/PK bytes). The only byte literals are b"", b"\x00" and b"\x01" regex patterns. grow() reads only the seed and fixed constants. The only module state is a deterministic row-table cache keyed by mask and the plant-only counter SELF_CHECK_FALLBACKS, which grow never reads. Every length, kind, mask, plan, dent count and setting is written into the seed and counted. The seed has no total length and does not need one. The "line rows with dents" coding is a general bit-plane technique (a row is a flat line plus listed exceptions), labelled as part of the bit-level-plot idea. It is not a hidden general compressor, but it is where nearly all of the text gain comes from.

3. Speed. At 120 KB the worst plant was 13 s and the worst grow 0.1 s, against limits of 60 s and 10 s.

4. Builder claims verified with explain():
- KJV is 3 line-row cucumber records, 2 tiny cycles (62 bytes) and 6 raw bytes.
- 330 bytes are 128 or above; 5,156 bytes have the 32s bit at 0.
- In the docx, 907 bytes go through flat rows.
- Zip on the four non-pattern files is 139,955.
- ABC123×20000 gives an 11-byte seed.
- 'Grow instructions 40,698 bytes' = 6,442 + 34,256.
Placeholder fruit names are clearly labelled in the docstring.

Context for the owner, not a defect: the method is honest and exact, but on every real file it is far from the claimed 98.9% and well behind ordinary zip (KJV 19.3% vs zip 70.2%; fresh KJV 19.6% vs 65.1%; Python 23.0% vs 69.5%; Markdown 19.4% vs 54.3%). Only the trivial repeating pattern gets near 98.9%.

I edited, committed and pushed nothing in the repository. methods/graph_fit.py has the same md5 before and after (bb49b23d…), and git status is clean. The harness's own `python -I` grow step writes .pyc files into methods/__pycache__, which .gitignore ignores. My scripts and outputs are in /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/gfcheck_LDnh/ (roundtrip.py, fuzz.py, speed.py, claims.py, fresh/, fresh_graph_fit.txt, fresh_zip.txt, builder_rerun.txt).


---

## graph_locate

**Checker verdict: PASS** (checker re-ran the builder's numbers: matched). Fix stage needed: no.


### How it works

Both sides keep a small library of fixed expressions. Each one is solved step by step with whole numbers only (multiply, add, subtract, keep the remainder), and after every step one point is plotted, a 0 or a 1. Stacking those points gives a long page of binary that is always the same, and any computer can regrow it in under a second. To plant a file, its bits are cut into 16-bit chunks. For each chunk we find the first spot on the page where that exact pattern appears (its plot point), and the seed is the list of those plot points plus a small header. To grow, the receiver regrows the same page and reads the 16 bits at each plot point. The catch is that a 16-bit chunk can be any of 65,536 patterns. To point at any of them you need 65,536 different spots, and naming one spot out of 65,536 takes 16 bits, which is exactly the size of the chunk. So the seed comes out the same size as the file, or a few bytes bigger. That held for every file tested.


### The library (strawberry / orange / cucumber, placeholder names)

These are PLACEHOLDER names, labelled as such in the code, until the owner shares their own factors. They are three library pages. Each is the expression y <- (y x 2 x TIMES + 27 x t + 72 - MINUS) mod 2,147,483,647, then t <- t+1, and the plotted point is one binary digit of y. The pages use different factors built from the owner's numbers: strawberry: start 17, TIMES = 17x32x16x34x47 (13,908,992), MINUS = 16x34 (544), plots digit 16. orange: start 32, TIMES = 47x34x27x72+1 (3,106,513), MINUS = 17x47 (799), plots digit 15. cucumber: start 47, TIMES = 17x16x47x27x72 (24,852,096), MINUS = 34x47 (1,598), plots digit 14. Each page runs until all 65,536 16-bit patterns have appeared, with a cap of 2,000,000 steps: strawberry needs 923,081 steps, orange 825,371 and cucumber 637,940. The library also fixes the chunk size at 16 bits and the 2,000,000-step cap. plant() tries all 3 pages and both ways of numbering plot points, and keeps the smallest seed.


### What the seed contains

An empty file gives an empty seed (0 bytes). Otherwise the seed contains:
- Byte 0, a settings byte: bits 0-1 say which page (0 strawberry, 1 orange, 2 cucumber). Bit 2 says the numbering style: 0 is the plain position on the page, 1 is the compact number ("the n-th new pattern seen on the page", 0..65,535). Bit 3 is set if some chunks were not on the page and are stored as they are. Bits 4-7 are 0.
- Byte 1: W, the number of bits used per plot point in this seed.
- Next: the original length in bytes, written 7 bits per byte (1-3 bytes).
- Next: one W-bit plot point per 16-bit chunk. If bit 3 is set, code 0 means "16 raw bits follow" and any other code is the plot point plus 1.
- Last: the final odd byte (when the length is odd), stored as it is, then 0-bits padding up to a whole byte.
Nothing else is needed. grow() regrows the page from the constants in the file.


### Builder's test results

```
Methods: graph_locate
Test files: random bytes (no pattern at all) (100,000 bytes), repeating pattern (120,000 bytes), short ordinary text (267 bytes), kjv_first_100k.txt (100,000 bytes), sample_word_file.docx (11,110 bytes)

=== Method: graph_locate ===
A fixed page of 0/1 plot points grows from a library expression; the seed lists, for each 16-bit chunk, the plot point where that chunk sits on the page.
test file                           original      seed reduction  exact?  plant s  grow s   xz size
random bytes (no pattern at all)     100,000   100,005     -0.0%     YES     2.87    0.79   100,064
repeating pattern                    120,000   120,005     -0.0%     YES     2.18    0.80       160
short ordinary text                      267       271     -1.5%     YES     2.02    0.69       152
kjv_first_100k.txt                   100,000   100,005     -0.0%     YES     1.82    0.70    26,940
sample_word_file.docx                 11,110    11,114     -0.0%     YES     2.10    0.73    10,060
Grow instructions (the test script + this method's file) are 21,922 bytes; they are shared once, not sent with each seed.

=== Summary: total seed bytes vs total original bytes, and exact regrowth ===
graph_locate           seeds     331,400 of 331,377 bytes  ( -0.0% smaller)   exact: 5/5 files
```


### Why each file got its result

The key comparison is bits needed to store one plot point against the 16 bits in a chunk, measured per file. All 65,536 patterns appear on every page, so every chunk was found.
- Random 100k: plain positions average 15.66-15.67 binary digits, but a fixed-width column needs 20 bits. Compact numbering needs 16. Seed 100,005 = 100,000 + 5 header bytes.
- KJV: plain positions average 15.10-15.52 digits and need 19-20 bits fixed width. Compact needs 16. Seed 100,005.
- docx: plain positions average 15.68-15.72 digits and need 20 bits. Compact needs 16. Seed 11,114.
- Short text (267 bytes, 133 chunks plus 1 odd byte): plain positions average 15.11-16.01 digits and need 18-19 bits. Compact needs 16. Seed 271 = 2 + 2 + 266 + 1, which is -1.5%.
- Repeating pattern ABC123: only 3 different chunks appear. Plain needs 17 bits on all three pages, compact needs 16. Seed 120,005. The page cannot see that the file repeats. It only knows where each chunk sits, so 60,000 repeats still cost 60,000 plot points. zlib gets 99.8% on this file because it spots repetition, which is a separate technique I deliberately did not add, so the result reflects the owner's idea alone.

Why "average digits" is below 16 but still can't be used: a list of numbers of different lengths needs some way to show where each number ends. The best variable-length code I measured in exploration cost 16.67-17.74 bits per 16-bit chunk, and a fixed width costs 17-20 bits.

Why compact numbering is exactly 16: the page has exactly 65,536 useful spots (one first sighting per pattern), and naming one of 65,536 takes 16 bits.

Other chunk sizes, from exploration on the same files:
- 8 bits: plain 10-11 bits vs compact 8.
- 12 bits: plain 14-15 vs compact 12.
- 20 bits: only about 97-98% of chunks were on a 4M-step page; plain cost about 23.5 bits and compact about 21.5 per 20-bit chunk.
- 24 bits: only about 20-23% found; worse than storing as-is.

More pages don't help either. Taking the earliest of 3 pages saved about 1.58 bits of position, which is exactly what it costs to say which page (log2 3 = 1.58).

Conclusion from the measurements: with a fixed page, a plot point never costs fewer bits than the chunk it points to. The seed is the file's size plus a few header bytes. Small gains appear only by luck, as with 5,000 zero bytes -> 4,692. This is a counting (pigeonhole) limit, not a tuning problem. Nothing like the claimed 98.9% appeared in any test.


### Builder's own exactness tests

All round trips ran in-process with grow(plant(data)) == data, and all were exact: 25/25.
- Inputs: empty (seed 0 bytes), 1 byte 0x00 and 1 byte 0xFF (4 bytes each), 2 bytes (5), 3 bytes (6), 1,000 random bytes (1,004), and every byte value 0-255 (260).
- Random lengths 4, 5, 15, 16, 17, 31, 32, 33, 255, 256, 257, 4095, 4097 and 65537: each seed came out 3-5 bytes bigger than the input.
- KJV 100,000 -> 100,005 and docx 11,110 -> 11,114.
- 5,000 zero bytes -> 4,692 (cucumber page, compact numbering, W=15) and 777 0xFF bytes -> 684 (cucumber page, plain position, W=14). These two gains are luck: each file has a single repeated pattern that happened to sit early on one page.
- Forced "not on the page" path: the page was cut to 30,000 steps so many patterns were missing. 5/5 were still exact, using the stored-as-is flag. The seeds got much bigger: KJV 100,000 -> 144,435, docx 11,110 -> 17,500, 1,000 random -> 1,576.
- Timing here: plant took about 1.6-2.9 s and grow about 0.5-0.9 s per file, far inside the 60 s / 10 s limits.
- The harness ran grow in a separate, isolated process: 5/5 exact.


### Checker's issues

- **minor**: Small 'gains' only appear on files made of one repeated 16-bit pattern, and they are luck. The pattern happens to sit early on one page, so a smaller fixed width W fits. The builder already reports this honestly. Nothing like 98.9% appears on any real file.  
  Evidence: My round trips: zeros_5000 -> 4,692, ffs_5000 -> 4,379, alternating 00 01 x3001 -> 1,880 (W=10), alternating aa x3001 -> 2,443. Every random, text, KJV, Python and docx input came out 3-5 bytes larger than the original.
- **minor**: The page cannot see repetition. 'ABC123' x 20,000 only has 3 distinct chunks, yet it still costs 16 bits per chunk (0.0% reduction), while zlib gets 99.8%. This is a limit of the interpretation, not a bug, and the builder says so.  
  Evidence: Harness row: repeating pattern 120,000 -> 120,005.
- **minor**: grow() trusts the seed. A malformed seed, for example one with page bits = 3, would raise IndexError on LIBRARY[3]. Valid seeds are never affected.  
  Evidence: graph_locate.py line 255: page_number = seed[0] & 0b11, then LIBRARY[page_number] in grow_page.
- **minor**: When the 'not on page' flag is on, each missing chunk costs W+16 bits. This never happens with the shipped library, because all 3 pages contain all 65,536 patterns. It only matters if the owner's real factors give a shorter page.  
  Evidence: Forced cap of 30,000 steps on both sides: still exact, but KJV 9,999 -> 14,697 and allpat 131,072 -> 205,723.


### Checker's fresh-file results

```
Command: cd /home/user/utensil-theories-transfer-protocol/SEED_TEST_2026-10-20 && python3 seed_test.py --method graph_locate <3 fresh files>. The fresh files are in /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/check_graph_locate_tzNt/fresh/

test file                           original      seed reduction  exact?  plant s  grow s   xz size
random bytes (no pattern at all)     100,000   100,005     -0.0%     YES     2.18    0.71   100,064
repeating pattern                    120,000   120,005     -0.0%     YES     1.91    0.90       160
short ordinary text                      267       271     -1.5%     YES     1.73    0.71       152
fresh_random_50000.bin                50,000    50,005     -0.0%     YES     1.78    0.67    50,060
fresh_kjv_middle_60000.txt            60,000    60,005     -0.0%     YES     1.77    0.79    18,336
fresh_stories_v2_20000.py             20,000    20,005     -0.0%     YES     1.92    0.57     5,800
Summary: graph_locate seeds 350,296 of 350,267 bytes (-0.0% smaller), exact: 6/6 files.

Where the fresh files came from:
- 50,000 random bytes from `openssl rand`, a different source from os.urandom.
- 60,000 bytes of KJV.txt starting at len/2 + 54,321 (Psalm 91 area).
- The first 20,000 bytes of experiments/stories_v2.py.

zlib on the same fresh files: random -0.1%, KJV 66.6%, Python 69.5%.
```

### Checker's notes

Verdict: PASS. The method is correct and fair, and its result is honest: it gives no compression.

1. Exactness: 334 out of 334 inputs regrew exactly, using the method file exactly as written (no memo or cache). The inputs were:
   - the empty file;
   - all 256 single bytes;
   - 40 random lengths from 1 to 5,000 (seeded generator);
   - 13 os.urandom inputs at the length boundaries 2/3/4/5/127/128/129/255/256/257/4096/4097/5000;
   - all-zero and all-0xFF files of lengths 2, 3, 1000, 4999 and 5000;
   - 6 alternating patterns;
   - short text;
   - 30,001 bytes from the middle of KJV.txt;
   - seed_test.py itself;
   - every 16-bit pattern once (131,072 bytes, which forces the largest codes), and the same reversed plus an odd byte;
   - 16,383 and 16,384 bytes (a length-field boundary);
   - 120,000 random bytes.
   The largest overhead was 5 bytes. I also ran grow through the harness's own `--grow` mode in a separate `python -I` process, in an empty folder, with a varied PYTHONHASHSEED: 6 out of 6 exact, and the folder held only seed.bin. Finally I forced the "not on page" path by patching MAX_PAGE_STEPS to 20, 1,000, 30,000 and 300,000 on both sides: 32 out of 32 exact.

2. Fairness:
   - The plant/grow path imports nothing. The only import is `import sys` under `__main__`.
   - No file, environment, clock or randomness access. No zlib, lzma or bz2.
   - plant fills no module state; LIBRARY is never mutated.
   - grow uses only the seed plus the constants in the file.
   - I checked that the pages are deterministic: each page grown twice gave an identical result. Strawberry is 923,081 steps, orange 825,371 and cucumber 637,940, and each holds all 65,536 patterns, as the builder stated.
   - The library constants check out (13,908,992 / 3,106,513 / 24,852,096) and contain nothing tied to the test files: no ABC123, no Bible words, no docx bytes.
   - The seed counts everything it needs: page and style bits, flag, W byte, a varint length, padding and the odd last byte.

3. Speed: plant takes 1.6-2.8 s for every size, because it grows 3 pages each time. grow takes 1.12 s at most. Both are far inside the 60 s / 10 s limits.

4. Bits per plot point compared with the 16-bit chunk (I measured this independently with measure()):
   - KJV slice: plain positions average 15.15-15.52 binary digits, but a fixed width needs 19 bits. Compact numbering needs 16.
   - 777 random bytes: average 15.71-15.76 digits, fixed width 19, compact 16.
   This matches the builder's pigeonhole explanation. First-sighting spots are a one-to-one relabelling of the 65,536 patterns, so naming one of them always costs 16 bits.

5. I re-ran the builder's command and got identical seed sizes on all 5 files (331,400 of 331,377 bytes, 5/5 exact). Timings were similar.

Housekeeping:
- I edited no repository files. I ran the harness with PYTHONDONTWRITEBYTECODE=1.
- During my run, git status showed SEED_TEST_2026-10-20/methods/graph_backwards.py modified, and graph_fit.py's earlier modification gone. Other sessions did that, not me.
- My scripts and outputs are in /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/check_graph_locate_tzNt/: roundtrip.py, sep_and_missing.py, roundtrip_out.txt, sep_and_missing_out.txt, fresh_harness_out.txt, builder_cmd_out.txt and fresh/.
- I did not copy them into a dated delivery folder or send them to the owner. CLAUDE.md asks for that, but this task said not to touch the repository, so the orchestrating session should do it if wanted.


---

## graph_backwards

**Checker verdict: PASS** (checker re-ran the builder's numbers: matched). Fix stage needed: no.


### How it works

The file treats any data as a long page of 0/1 points, 8 per byte. An "expression" is a step rule built from add, subtract, multiply and mod, plus a few unknowns (the "?" in the owner's example). Solving the rule step by step always grows the same page of points. To make a seed, the sender works BACKWARDS from the data to those unknowns at every place in the file, using real algebra rather than guessing: the Berlekamp-Massey method for the 0/1-point rule, and remainder arithmetic with a precomputed answer table for the number rule. Each rule found is run forward to see how far it keeps matching the data exactly; a strawberry rule can also be run backwards to start a block earlier. A planner then picks the set of cuts that makes the whole seed smallest, keeping a block only where writing down its expression costs less than the bytes it regrows. Every other byte is stored as it is. The receiver reads only the seed and the fixed rules in the file, solves each expression forward, and gets the data back exactly.


### The library (strawberry / orange / cucumber, placeholder names)

These are PLACEHOLDER names. The owner has not shared their own factors, and the file says so at the top. STRAWBERRY is a rule for the points themselves: next point = (c1·point 1 back + … + cL·point L back) mod 2. Its unknowns are L, the factors c1..cL (each 0 or 1) and the first L points. It is solved backwards exactly by Berlekamp-Massey, which returns the shortest such rule. ORANGE is a rule for whole numbers 0 to 255, each plotted as 8 points: next number = (a·the number k steps back + c) mod 256, with k from 1 to 255. Its unknowns are k, a, c and the first k numbers. It is solved backwards from the data's step differences: a × (difference then) = (difference now) mod 256, using a precomputed answer table, then c follows. CUCUMBER is the raw fallback: bytes no expression fits, stored as they are with a flag. Nothing in the library is specific to the test files. The owner's numbers (17, 32, 16, 34, 47) are not hard-coded; any constant a block needs is found by the backwards search.


### What the seed contains

The seed is a series of records, nothing else: no global header, no file name, no hidden table. An empty input gives a 0-byte seed. Each record starts with a varint (7 bits per byte, low bits first, top bit means "more follows") holding length_in_bytes×4 + kind, where kind 0 = cucumber, 1 = strawberry, 2 = orange.
- Cucumber: then `length` raw bytes.
- Strawberry: then a varint L, then ceil(2L/8) bytes read as one little-endian number. Its low L bits are the factors (bit i-1 = ci). The next L bits are the block's first L points (bit j = point j; points are taken from each byte biggest place first).
- Orange: then a varint k×4 + form. Form 0 means a=1, c=0 and nothing more is written. Form 1 means a=1 and is followed by 1 byte, c. Form 2 is followed by 2 bytes, a then c. After that come k bytes: the first k numbers.
The receiver needs only these bytes plus the constants in the method file.


### Builder's test results

```
Methods: graph_backwards
Test files: random bytes (no pattern at all) (100,000 bytes), repeating pattern (120,000 bytes), short ordinary text (267 bytes), kjv_first_100k.txt (100,000 bytes), sample_word_file.docx (11,110 bytes)

=== Method: graph_backwards ===
Works backwards from the data to small add/multiply/mod expressions whose page of 0/1 points equals a stretch exactly (strawberry: a 0/1 point rule solved by Berlekamp-Massey; orange: a number rule solved by remainder arithmetic), and stores stretches no expression fits as they are (cucumber).
test file                           original      seed reduction  exact?  plant s  grow s   xz size
random bytes (no pattern at all)     100,000   100,003     -0.0%     YES     4.74    0.04   100,064
repeating pattern                    120,000        10    100.0%     YES     0.60    0.06       160
short ordinary text                      267        97     63.7%     YES     0.03    0.04       152
kjv_first_100k.txt                   100,000    93,800      6.2%     YES     4.19    0.04    26,940
sample_word_file.docx                 11,110    10,897      1.9%     YES     0.49    0.04    10,060
Grow instructions (the test script + this method's file) are 37,646 bytes; they are shared once, not sent with each seed.

=== Summary: total seed bytes vs total original bytes, and exact regrowth ===
graph_backwards        seeds     204,807 of 331,377 bytes  ( 38.2% smaller)   exact: 5/5 files
```


### Why each file got its result

Blocks found by working backwards, per file (counted from each file's seed; random from my own 100 KB os.urandom run):
- **Random bytes: −0.0% (3 bytes bigger).** 1 block, 0 found (0%). No rule cheaper than the bytes themselves exists for random data, so it is one cucumber record plus its 3-byte header.
- **Repeating pattern: 100.0% (10 bytes).** 1 block, found (100%). It is the single orange rule y[t] = 1·y[t-6] + 0 with first numbers "ABC123", run for 120,000 bytes. The rule itself grows 119,994 of those bytes.
- **Short text: 63.7% (97 bytes).** 2 of 2 blocks found (100%): orange "repeat 45 back" for the first sentence ×3 and "repeat 44 back" for the second ×3. Only 66.7% of the bytes are grown by rule steps; the rest are the stored first sentence of each pair. Zip gets 66.3%.
- **KJV: 6.2%.** 1,851 blocks, of which 1,010 (54.6%) were found by working backwards, every one an orange "repeat k back" (a=1, c=0). Strawberry found 0. The found blocks hold 66.7% of the bytes, but the rules themselves grow only 10.5%. The rest is the stored first-k numbers inside each block, which is raw text. Text has no add/multiply rule. The only exact regularity is short phrases repeating nearby, and "repeat k back" is the same trick zip uses, without zip's ability to copy from anywhere earlier. Zip gets 70.2%.
- **Docx: 1.9%.** 36 blocks, 22 found (61.1%): 14 orange repeats and 8 full (a, c) rules, all in zip headers such as the repeated "PK\x03\x04…" structures. Rules grow only 2.8% of the bytes. The rest of a .docx is already-compressed data that looks random. Zip gets 9.9%.

Overall the method is 38.2% smaller, but nearly all of that comes from the 120 KB repeating-pattern file. Only that file reaches the claimed 98.9%. On real text and Word files, this is far below both the claim and ordinary zip.

Two more checks:
- **Reach-back limit.** Before the cut planner was added, greedy cutting got worse as k reached further (KJV 3.4% at 64, 2.8% at 255, 1.4% at 1024). With the planner it is 3.8% at 64, 6.2% at 255 and 6.4% at 1024 (docx 1.6%, 1.9%, 2.3%). I kept 255 so k stays a one-byte "small constant".
- **A limit of this library.** A 16-bit counter (00 00 00 01 00 02 …) is not captured (−0.0%), because orange works on 1-byte numbers. A wider-number orange could catch it, but none of the test files needs it.

No zlib, lzma, bz2 or gzip is used, and grow() uses only the seed plus the constants in the file. I wrote only graph_backwards.py; nothing was committed, pushed or sent.


### Builder's own exactness tests

Every round trip below gave grow(plant(data)) == data. There were 0 failures in all of these:
- Fixed cases (227): empty input (0-byte seed), 1 byte (0x00 and 0xFF, 2-byte seed each), 2 and 3 bytes, and random data of 4, 5, 7, 8, 9, 15, 16, 17, 31, 64, 100, 255, 256, 1000 and 4097 bytes (each seed is 1–3 bytes bigger than the input). Also structured cases: 5,000 zeros → 4 bytes; a 0..255 counter → 5; an LFSR bit sequence → 11 (strawberry found p[t]=p[t-28]+p[t-31]); the 17x+32 mod 256 sequence → 5; an affine sequence → 70; a mix of random, ABC123, counter and LFSR → 414; the short text → 97. Plus 200 random fuzz cases.
- 1,500 extra fuzz inputs mixing random runs, constant runs, random affine orange sequences, periodic patterns, random strawberry sequences, two-letter text and repeated phrases.
- Stress runs at 120,000 bytes, all exact. Plant times: two-letter random text 17.5 s; sparse 0/1/255 bytes 17.4 s; four-letter text 12.0 s; zeros 0.9 s; LFSR 1.5 s; LFSR with noise 4.2 s; two-byte counter 10.4 s. Every grow took 0.4 s or less. A per-place budget of 48 checked rules was added after the first stress runs, which had taken 48–52 s; seed sizes were identical before and after.
- The harness run above: 5/5 exact, with grow in a separate `python -I` process in an empty folder.
plant() also checks its own seed with grow(); if that ever failed it would store the whole file as cucumber. The found blocks reported for the harness files show this fallback did not fire there.


### Checker's issues

- **minor**: On real data it shrinks files far less than the owner's 98.9% claim and far less than ordinary zip. The builder said so honestly. Only exact repeating patterns come close to the claim.  
  Evidence: Builder files: KJV 6.2% (zip 70.2%), docx 1.9% (zip 9.9%). Fresh files: KJV middle 60k 4.0% (zip 65.1%), stories_v2.py 20k 13.8% (zip 69.5%), tech report .md 20k 4.0% (zip 54.3%), SHA-256 random -0.0%. The 38.2% overall figure comes almost entirely from the 120 KB ABC123 file.
- **minor**: Repeats more than 255 bytes back are never caught. Orange can only look back k ≤ 255 numbers, and strawberry can only find rules up to 480 points long. Data that zip shrinks almost to nothing gets no saving.  
  Evidence: 300 random bytes repeated to 120,000 bytes gives 120,003 bytes (-0.0%). 256 random bytes repeated 40 times gives 10,243 of 10,240 (-0.0%). A 16-bit counter gives -0.0%; the builder already disclosed that one.
- **minor**: Saying '54% of blocks found by working backwards' on text could mislead the owner. Every block found in text is 'repeat the numbers k back' (the same trick zip uses). The starting numbers stored inside each block are raw text, so rules actually regrow only 8–19% of the bytes. The builder disclosed this.  
  Evidence: describe(): KJV 1,010 of 1,851 blocks found, all of them repeats; found bytes 66.7%, rule-grown bytes 10.5%. Fresh KJV: 576 of 1,061 found, rule-grown 8.4%. Fresh .py: 204 of 380 found, rule-grown 19.1%. Strawberry found 0 blocks in every text file.
- **minor**: Planting is within the 60 s limit, but data from a two-value alphabet leaves less headroom on a slow machine.  
  Evidence: Adversarial 120 KB inputs run one at a time: random {0,128} bytes 24.3 s, {0,64,128,192} 20.0 s, random 'ab' 17.5 s. The same inputs run 4 at a time on this already loaded 4-core machine (load average about 7) took up to 59.1 s. All other adversarial inputs took 8–46 s under that contention. Every grow took 0.6 s or less.
- **minor**: grow() does not check that a seed is intact. A truncated seed quietly returns shorter, wrong data, and some malformed seeds crash it. This only matters for seeds that plant() did not make.  
  Evidence: grow(seed[:-3]) returned b'hello world, plain cucumber t' without any error. grow(b'\x0a\x00') (orange with k=0) raises ZeroDivisionError. grow(b'\x80') raises IndexError.
- **minor**: Small inaccuracy in the docstring: it says each record header is '1 to 3 bytes', but a single record longer than 524,287 bytes needs a 4-byte varint. The decoder handles that correctly.  
  Evidence: _varint(length*4+kind) uses 4 bytes once length*4 ≥ 2^21. The text is in docstring section 4.


### Checker's fresh-file results

```
cd SEED_TEST_2026-10-20 && python3 seed_test.py --method graph_backwards <fresh files>   (fresh files are in /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/check_WfB4/fresh/)
test file                           original      seed reduction  exact?  plant s  grow s   xz size
random bytes (no pattern at all)     100,000   100,003     -0.0%     YES     4.06    0.04   100,064
repeating pattern                    120,000        10    100.0%     YES     0.37    0.05       160
short ordinary text                      267        97     63.7%     YES     0.03    0.05       152
fresh_random_sha256_50k.bin           50,000    50,003     -0.0%     YES     2.06    0.04    50,060
fresh_kjv_middle_60k.txt              60,000    57,573      4.0%     YES     2.28    0.05    19,148
fresh_stories_v2_20k.py               20,000    17,236     13.8%     YES     1.35    0.05     5,800
fresh_tech_report_20k.md              20,000    19,199      4.0%     YES     0.83    0.04     8,808
Summary: seeds 244,121 of 370,267 bytes (34.1% smaller), exact: 7/7 files.
zlib on the same fresh files for comparison: SHA random -0.1%, KJV middle 65.1%, .py 69.5%, .md 54.3%.
Blocks found by working backwards: SHA random 0/1, KJV middle 576/1,061 (54.3%, all repeats, 8.4% of bytes grown by rules), .py 204/380 (53.7%: 200 repeats, 4 full a,c rules; 19.1% rule-grown), .md 156/289 (54.0%; 7.5% rule-grown).
```

### Checker's notes

I re-ran the builder's command and every seed size matches exactly: random 100,003, pattern 10, short text 97, KJV 93,800, docx 10,897. Total is 204,807 of 331,377 bytes (38.2%), with 5/5 exact. Plant times were 0.04–4.5 s and grow times 0.04–0.06 s. Using describe(), I confirmed the builder's block counts exactly: KJV 1,851 blocks, 1,010 found (54.6%); docx 36 blocks, 22 found (14 repeats, 8 full rules); short text 2/2 found; ABC123 is the single rule y[t]=1·y[t-6]+0.

Exactness:
- 469 fixed cases all round-tripped exactly. They covered empty input, all 256 single bytes, 120 random inputs of 1–5000 bytes, zeros and 0xFF up to 120 KB, alternating patterns, short and Unicode text, slices from the middle of KJV.txt, seed_test.py, graph_locate.py, an LFSR, affine sequences, a 16-bit counter, period-256 and period-300 data, mixes, and two-value alphabets.
- Another 1,200 fuzz inputs, each mixing up to 12 segment types (affine with k up to 300, misaligned LFSRs, copies from any distance, KJV slices, random), also round-tripped exactly with 0 failures.
- I patched grow inside plant() to watch its built-in safety net. The safety net never fired, so the planner's own seeds were correct every time; exactness does not depend on the fallback.
- 9 seeds were also regrown in a separate python -I process with an empty environment, in an empty folder. All were exact.
- The worst size increase on random data was 3 bytes.

Fairness, from reading the code:
- grow() uses only the seed and module constants. The only module state is _AFFINE_CACHE, which is a pure x→(a·x+c) mod 256 table and is empty in the separate process.
- There are no imports outside the __main__ block: no zlib, lzma, bz2, gzip, os, time or random, and no file or environment access.
- Nothing is special-cased for the test files. 'ABC123' appears only in docstrings, and there are no Bible or PK/docx byte literals.
- Every needed byte is inside the seed: per-record varint length×4+kind, L, k and form, a/c, the starting numbers and points. There is no global header, and an empty input gives a 0-byte seed.

Speed: plant stays under 60 s per 120 KB file. Run one at a time, the worst adversarial input took 24 s; most inputs take 0.4–20 s. Grow takes 0.6 s or less.

I edited no repository file. The method file's sha256 (2b13bb64…) was unchanged before and after, and git status is clean. I ran the harness with PYTHONDONTWRITEBYTECODE=1.

My scratch files are outside the repository, in /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/check_WfB4/:
- roundtrip.py, speed.py, fuzz.py and fuzz_out.txt
- fresh/ (the 4 fresh input files)
- fresh_harness.txt and builder_harness_rerun.txt

Under the repo's CLAUDE.md, the parent session should copy any of these it wants into the delivery folder. I did not do that because the task said not to touch the repository.
