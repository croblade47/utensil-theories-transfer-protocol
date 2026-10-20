# Greenhouse ladder: builder report and independent check (20 October 2026)

The builder wrote and ran `understanding_compression.py`. A separate checker then tried to break it. Both reports are copied here as returned.


## Checker verdict: PASS (no fix stage was needed)


### Checker's issues (all minor)

- **minor**: Exact regrowth only works if the decoder repeats the encoder's float path exactly, and that already breaks on this same machine with a different thread count. The builder lists this caveat as 'not tested'. It should now say it was tested and fails: the greenhouse has to include the exact numeric setup (2 threads, these torch/numpy versions, this CPU). R3 and R4 use only integers, so they are portable.  
  Evidence: Fresh process, builder's own code, baseline seed 0 on full H. With 2 threads: seed 12,252 B, SHA identical to the JSON, decode == H. With 1 thread: the encoder writes 12,253 B with a different SHA. Decoding the 2-thread seed with 1 thread does not equal H (547 of 623 verses right, the rest garbled after the coder loses sync).
- **minor**: The TOTAL comparison is structurally tilted against the marker models, and the caveat 'this is the same for every rung' understates that. Each held-out verse's marker sums up the real preceding verses, which are training verses and not in the window. The window holds the previous held-out verse, 50 verses back. So the marker is nearly unpredictable by design (2–3 bits per verse). The pre-registered answer is valid as specified. But 'paying for the marker makes the seed ~2% bigger' should be tied to this layout. The conclusion still stands, because WORDS ONLY shows no gain either.  
  Evidence: The marker for verse v comes from sw.mark_up: emerge() runs before read(text), using the balance from verses < v in the same book. The layout puts only held-out verses in the context. Marker cost: shifting 3.02, label 2.60, scrambled 2.34, carry3 1.95 bits per verse.
- **minor**: The TXT summary line 'Fully decoded token by token ...: 24 runs; 24 of 24' counts R8_baseline_seed0_k64, which is a copy of the R6_baseline_seed0 result, not a separate decode. There are 23 distinct decodes. The builder's prose report discloses this; the TXT line does not.  
  Evidence: In understanding_compression.py lines 662–667, R[key] = dict(R['R6_baseline_seed0']) for k == 64. meta.fully_decoded lists 24 keys, including R8_baseline_seed0_k64.
- **minor**: The greenhouse-size line is labelled 'R6-R8 tiny transformer: 3,439,680 numbers', but n_params comes from the last model loaded in the loop (shifting seed 2, vocab 8,581). The baseline R6/R8 model has 3,438,720.  
  Evidence: tt.TinyGPT(8576) has 3,438,720 parameters; tt.TinyGPT(8581) has 3,439,680. n_params is set inside the baseline/shifting loop at lines 652–654.
- **minor**: A few small wording points. (1) 'words slightly dearer for shifting and carry3' leaves out scrambled, which is also dearer (+0.400 bits/verse, two-sided p ≈ 0.01) by about as much as shifting, and shifting vs scrambled WORDS ONLY is a tie. (2) The explanation for context growth ('part of the reason is ... 50 verses back') is an untested guess. (3) The dev-mode header still says 'held-out verses ... no model saw them' next to the DEV tag (scratch output only). (4) The pre-registration was not committed to git (the builder discloses this). The script SHA in the JSON matches the file on disk, and the prototypes proto.py/proto2.py only measured H's size and unknown-word count plus model speed; they never ran a model on H.  
  Evidence: Table 3 scrambled WORDS ONLY: +0.400, 280/343, two-sided sign p 0.0129, permutation p 0.0093. sha256sum of understanding_compression.py = 52cbb153d57d08b3..., the same as meta.script_sha256.


### What the checker re-ran or recomputed

All of this was run in a fresh scratch folder: /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/verify_uc_xtlS (scripts indep.py, repro.py, cross.py, stats.py). No repository file was edited.
1) TARGET AND SPLIT. I rebuilt H with my own regex: SHA-256 80d0ffa0... matches, 83,757 characters. The held indices in the JSON equal range(0, N, 50), the same as tiny_transformer.py's held-out split, and the pool is disjoint from them. The training-only vocab has 8,576 words (a vocab from all verses would have 8,658), so there is no vocab leak. H has 156 unknown words (1,119 letters); they are spelled inside the seed.
2) R1/R2. zlib9 28,565 B, xz 26,420 B and zlib+zdict 27,625 B all reproduce exactly. The zdict is the last 32 KB of the normalised training text only, and no held-out line appears in it.
3) R3–R5. I recomputed per-verse code lengths with my own uniform, add-one unigram and Witten-Bell bigram code: 31,257.3 / 19,768.5 / 14,859.4 bytes, equal to the builder's ideal bits, with the largest per-verse difference 5e-5 (JSON rounding).
4) TRANSFORMERS. All 15 state dicts load strictly with the reproduced vocabs (8,576 / 8,581 / 8,579). Using the model's standard forward (batch 1, my own softmax), per-verse bits for the first 50 held-out verses match the JSON for baseline s0 (8,157.2 bits), shifting s0 (8,373.4) and carry3 s1 (8,352.1); largest difference 0.0000. Baseline s0 held-out loss from tt.held_out_loss is 3.445 nats/token, against 3.46 for the project's earlier full/seed0 model, so the models are plausible.
5) EXACTNESS, INDEPENDENT CODER. I wrote an exact big-integer interval arithmetic coder of a different design. From the bits plus the greenhouse alone, it encoded and then decoded token by token the first 50 held-out verses for R4, R5, baseline s0, shifting s0 (markers coded and decoded) and carry3 s1: all byte-for-byte equal to H's first 50 lines.
6) EXACTNESS, BUILDER CODE, FULL H, FRESH PROCESS. Baseline s0 (12,252 B) and shifting s1 (12,411 B) seeds are SHA-identical to the JSON. Decoding baseline s0 gives exactly H. Flipping one bit of the seed breaks regrowth, so the seed really carries the information and nothing peeks. Reading run_coder's decode path confirms it uses only the header N, the seed bits and the predictor. The 1-thread decode fails (see issue 1).
7) ACCOUNTING. Seed = 4-byte header + coder bytes. coder_bits − ideal is 0.4–2 bits, and the padding is under 1 byte. Unknown-word letters (log2 27 each, plus an end mark), every verse end (token 1, including the last one in each group) and the markers in TOTAL are all coded. The only free side information is the fixed rules (12 groups, quantiser) and the greenhouse.
8) STATISTICS. I recomputed all 12 comparisons from the JSON per-verse arrays with scipy binomtest and my own 200,000-flip permutation (different RNG): every mean, win/loss count and p-value matches. The main test is one-sided in the right direction: mean +3.454 bits/verse, 127/496, one-sided p = 1.0, so NOT CONFIRMED is correct. The per-seed differences are also positive (+3.49, +3.31, +3.57), and a paired t-test agrees. The '~2% bigger' claim checks out: 2.21% / 1.76% / 1.99% / 1.75%.

### Checker's notes

The core results hold up. Every number I re-ran or recomputed matches, my separate coder regrows H exactly, there is no leakage in the greenhouses, the models and vocabs are right, and the pre-registered statistics are correct and one-sided as stated. The main fix to pass on is to the caveats: exact regrowth depends on the thread count (a 1-thread decoder fails on the 2-thread seed), so the shared greenhouse must include the exact software and hardware setup. Also say that the TOTAL marker cost is partly built into the layout, because each marker depends on true neighbouring verses that are not in the window.


---

## Builder's report


### The script

/home/user/utensil-theories-transfer-protocol/experiments/understanding_compression.py (new file, about 820 lines; no other repo file edited; nothing committed or pushed). The plain-English docstring maps the greenhouse metaphor onto each rung: soil = training verses, plant = H, humidity and sun = fixed shared grow instructions, greenhouse = shared knowledge (not counted in the seed), seed = bitstream, checking the air = real decode plus byte-for-byte or SHA-256 check. The pre-registration is in the docstring and was written before any rung ran on H.

How it works:
- Exact integer arithmetic coder: Witten-Neal-Cleary style, 62-bit registers, Python big ints.
- Probability rounding: freq = max(1, floor(p*2^20)), from float64 numpy softmax of the float32 logits.
- H is split into 12 fixed contiguous verse groups that advance together. Each step makes one batched model call on the 12 windows (the last 64 tokens or fewer, the training layout: <v> before each verse, marker first for marker models, a final <v> closing each group). The decoder makes the identical call on identical windows, so its probabilities are bit-identical.
- Unknown words are coded as <unk> by the model, then spelled with a 27-symbol uniform letter coder (counted in the seed).
- Seed = 4-byte header (N verses) + coder bytes.
- R4 uses exact add-one integer counts. R5 is a Witten-Bell bigram (no tuning).
- `--dev` mode self-tests on 40 TRAINING verses and writes only to the scratchpad. It ran first: 24/24 exact.


### Printed results

```
TABLE 1  THE LADDER: exact seeds that regrow H byte for byte
  raw H = 83,757 bytes = 670,056 bits.  bpc = seed bits / characters.  Greenhouse = shared in advance, NOT in the seed.
  rung                         seed bytes     bpc  smaller  regrown exactly?  
  R0_raw                           83,757   8.000     0.0%  yes (decompressed)
  R1_zlib9                         28,565   2.728    65.9%  yes (decompressed)
  R1_xz9e                          26,420   2.523    68.5%  yes (decompressed)
  R2_zlib9_library32KB             27,625   2.639    67.0%  yes (decompressed)
  R3_word_list                     31,262   2.986    62.7%  yes (decoded)
  R4_word_freq                     19,773   1.889    76.4%  yes (decoded)
  R5_word_pairs                    14,864   1.420    82.3%  yes (decoded)
  R6_baseline_seed0                12,252   1.170    85.4%  yes (decoded)
  R6_baseline_seed1                12,153   1.161    85.5%  yes (decoded)
  R6_baseline_seed2                12,189   1.164    85.4%  yes (decoded)
  R7_shifting_seed0                12,524   1.196    85.0%  yes (decoded)
  R7_shifting_seed1                12,411   1.185    85.2%  yes (decoded)
  R7_shifting_seed2                12,467   1.191    85.1%  yes (decoded)
  R7_label_seed0                   12,441   1.188    85.1%  yes (decoded)
  R7_label_seed1                   12,388   1.183    85.2%  yes (decoded)
  R7_label_seed2                   12,409   1.185    85.2%  yes (decoded)
  R7_carry3_seed0                  12,383   1.183    85.2%  yes (decoded)
  R7_carry3_seed1                  12,468   1.191    85.1%  yes (decoded)
  R7_carry3_seed2                  12,471   1.191    85.1%  yes (decoded)
  R7_scrambled_seed0               12,437   1.188    85.2%  yes (decoded)
  R7_scrambled_seed1               12,359   1.180    85.2%  yes (decoded)
  R7_scrambled_seed2               12,438   1.188    85.1%  yes (decoded)
  R8_baseline_seed0_k1             15,111   1.443    82.0%  yes (decoded)
  R8_baseline_seed0_k2             13,800   1.318    83.5%  yes (decoded)
  R8_baseline_seed0_k4             13,020   1.244    84.5%  yes (decoded)
  R8_baseline_seed0_k8             12,508   1.195    85.1%  yes (decoded)
  R8_baseline_seed0_k16            12,278   1.173    85.3%  yes (decoded)
  R8_baseline_seed0_k64            12,252   1.170    85.4%  yes (decoded)

TABLE 2  TINY TRANSFORMERS, mean of 3 seeds (TOTAL = real decoded seed; WORDS ONLY = markers not paid)
  method     TOTAL seed B TOTAL bpc               per seed (B) marker bits/verse TOTAL ideal bpc WORDS ONLY bpc
  baseline         12,198    1.1651     12,252, 12,153, 12,189              0.00          1.1647         1.1647
  shifting         12,467    1.1908     12,524, 12,411, 12,467              3.02          1.1904         1.1679
  label            12,413    1.1856     12,441, 12,388, 12,409              2.60          1.1851         1.1658
  carry3           12,441    1.1883     12,383, 12,468, 12,471              1.95          1.1878         1.1733
  scrambled        12,411    1.1855     12,437, 12,359, 12,438              2.34          1.1850         1.1676

TABLE 3  EACH METHOD vs BASELINE, paired verse by verse (3-seed average per verse)
  diff = method minus baseline, bits per verse (negative = smaller seed = better).
  p one-sided tests 'method smaller'; two-sided in brackets. Permutation: 100,000 sign flips.
  comparison                 measure    mean diff  smaller/larger           sign p      permutation p
  shifting vs baseline       TOTAL         +3.454     127/496      1.0000 (0.0000)  1.00000 (0.00001)
  shifting vs baseline       WORDS ONLY    +0.436     279/344      0.9959 (0.0103)  0.99841 (0.00342)
  label vs baseline          TOTAL         +2.752     132/491      1.0000 (0.0000)  1.00000 (0.00001)
  label vs baseline          WORDS ONLY    +0.148     301/322      0.8109 (0.4230)  0.83529 (0.32887)
  carry3 vs baseline         TOTAL         +3.111     137/486      1.0000 (0.0000)  1.00000 (0.00001)
  carry3 vs baseline         WORDS ONLY    +1.159     233/390      1.0000 (0.0000)  1.00000 (0.00001)
  scrambled vs baseline      TOTAL         +2.736     146/477      1.0000 (0.0000)  1.00000 (0.00001)
  scrambled vs baseline      WORDS ONLY    +0.400     280/343      0.9949 (0.0129)  0.99524 (0.00934)
  shifting vs scrambled      TOTAL         +0.718     284/339      0.9876 (0.0304)  1.00000 (0.00001)
  shifting vs scrambled      WORDS ONLY    +0.035     317/306      0.3444 (0.6887)  0.61827 (0.76428)
  shifting vs label          TOTAL         +0.702     261/362      1.0000 (0.0001)  0.99999 (0.00003)
  shifting vs label          WORDS ONLY    +0.288     288/335      0.9728 (0.0652)  0.99585 (0.00853)

PRE-REGISTERED VERDICT
  Does the shifting-word model regrow the held-out verses with a smaller TOTAL seed than baseline?
  mean difference +3.454 bits per verse (+269 bytes over all of H);  permutation p = 1.00000;  sign test p = 1.0000
  -> NOT CONFIRMED

TABLE 4  THE GREENHOUSE BUILT GRADUALLY: baseline seed 0 given the last k tokens
  k tokens seen seed bytes     bpc  smaller than raw
              1     15,111   1.443             82.0%
              2     13,800   1.318             83.5%
              4     13,020   1.244             84.5%
              8     12,508   1.195             85.1%
             16     12,278   1.173             85.3%
             64     12,252   1.170             85.4%

EXACT REGROWTH
  Fully decoded token by token from seed bytes + greenhouse: 24 runs; byte-for-byte identical to H: 24 of 24.
  Encoded only (seed size real, not decoded): none
  R0-R2 were decompressed and compared byte for byte.

SIZE OF THE GREENHOUSES (shared in advance, NOT in any seed)
  R2 library: 32,768 bytes of training text.  R3-R5 word list: 8,576 entries (R4/R5 add counts; R5 knows 132,894 word pairs).
  R6-R8 tiny transformer: 3,439,680 numbers (about 13.8 MB as float32), far larger than H (84 KB).
  A greenhouse pays off only when it is reused for many messages, like a dictionary both people own.
```


### Exact regrowth

Everything was fully regrown and matched H byte for byte, with no exceptions and nothing left as encode-only.
- 24 of 24 coder runs were decoded token by token from the seed bytes plus the shared greenhouse:
  - R3, R4, R5;
  - all 15 transformers: baseline, shifting, label, carry3 and scrambled, seeds 0, 1 and 2, TOTAL seeds with the markers decoded too;
  - R8 at k = 1, 2, 4, 8 and 16.
- Every regrown SHA-256 equals H's SHA-256 (80d0ffa084f89746...).
- R8 at k = 64 is the same computation as R6 baseline seed 0 and reuses that decode.
- R0 is the identity. R1 (zlib, xz) and R2 (zlib with the library) were decompressed and compared byte for byte: all exact.
- The earlier dev self-test on 40 training verses also decoded 24 of 24 exactly.
- Each real seed equals the ideal code length plus about 4–5 bytes (the 4-byte header and the coder flush).


### The owner's ideas vs the plain model

Pre-registered main question: does the shifting-word model regrow H with a smaller TOTAL seed than baseline? **NOT CONFIRMED.** It goes the opposite way.

**(a) TOTAL seed bytes per seed (markers paid for):**
- baseline: 12,252 / 12,153 / 12,189 (mean 12,198, 1.1651 bpc)
- shifting: 12,524 / 12,411 / 12,467 (mean 12,467, 1.1908 bpc)
- label: 12,441 / 12,388 / 12,409 (mean 12,413)
- carry3: 12,383 / 12,468 / 12,471 (mean 12,441)
- scrambled: 12,437 / 12,359 / 12,438 (mean 12,411)

Every marker-model seed is larger than every baseline seed.

**Paired by verse (n = 623, 3-seed average, method minus baseline, bits per verse):**
- shifting +3.454: smaller on 127 verses, larger on 496. One-sided p: sign 1.0000, permutation 1.00000. Two-sided p: sign below 0.0001, permutation 0.00001.
- label +2.752: 132 smaller, 491 larger. One-sided p = 1.0. Two-sided p: sign below 0.0001, permutation 0.00001.
- carry3 +3.111: 137 smaller, 486 larger. Same p-values.
- scrambled +2.736: 146 smaller, 477 larger. Same p-values.

The markers cost about 2–3 bits per verse to code (shifting 3.02, label 2.60, scrambled 2.34, carry3 1.95).

**(b) WORDS ONLY (markers given free; accounting only, not a stand-alone seed):**
- shifting +0.436 bits/verse: 279 smaller, 344 larger. One-sided p: sign 0.9959, permutation 0.99841. Two-sided p: sign 0.0103, permutation 0.0034. So the words cost slightly more even when the marker is free.
- label +0.148: 301 smaller, 322 larger. One-sided p: sign 0.8109, permutation 0.835. Two-sided p: 0.42 / 0.33. No clear difference.
- carry3 +1.159: 233 smaller, 390 larger. Two-sided p about 0.00001 (worse).
- scrambled +0.400: 280 smaller, 343 larger. Two-sided p: sign 0.0129, permutation 0.0093.

**Descriptive extras:**
- shifting vs scrambled: TOTAL +0.718 (two-sided permutation p 0.00001, sign p 0.0304); WORDS ONLY +0.035 (two-sided p 0.69 / 0.76), a tie.
- shifting vs label: TOTAL +0.702 (two-sided p 0.00003); WORDS ONLY +0.288 (two-sided permutation p 0.0085, sign p 0.065).

**Plainly:** under this compression measure, none of the marker methods helped the tiny model predict held-out Bible text. Paying for the marker makes the seed about 2% bigger. Even with the marker given free, the words are no cheaper, and slightly dearer for shifting and carry3. This measures plain next-word prediction of verses, not the right/wrong judging where the markers helped in earlier experiments.


### The greenhouse built step by step (context)

R8, baseline seed 0, bits per character as the model is allowed to see more context (k tokens; at 1–2 KB each, the bigger numbers here are in tokens):

| k (tokens seen) | bpc | seed bytes |
|---|---|---|
| 1 | 1.443 | 15,111 |
| 2 | 1.318 | 13,800 |
| 4 | 1.244 | 13,020 |
| 8 | 1.195 | 12,508 |
| 16 | 1.173 | 12,278 |
| 64 | 1.170 | 12,252 |

- About 90% of the total gain from k = 1 to k = 64 is in place by k = 8; 16 to 64 adds only 0.003 bpc. Part of the reason is that each held-out verse's context is the previous held-out verse, 50 verses back, not its true neighbour.
- With one token of context the transformer (1.443) is slightly worse than the word-pair statistics (R5, 1.420).

Full ladder in bpc: raw 8.000 → word list 2.986 → zip 2.728 → zip with library 2.639 → xz 2.523 → word frequencies 1.889 → word pairs 1.420 → tiny transformer 1.161–1.170 (85.4% smaller than raw). The plain word list is worse than zip; word frequencies and anything above beat every classic compressor.


### Caveats

- **The greenhouse is not counted in any seed.** The transformer is 3.44M numbers (about 13.8 MB) against H of 84 KB. These are seeds given a shared greenhouse, worth it only when the greenhouse is reused for many messages.
- **Exactness depends on the identical float path.** Decoding was done on the same machine, process and settings (2 threads, torch 2.14.1, numpy 2.5.3, Python 3.13.16). A decoder on other hardware, thread count or versions might compute slightly different floats and fail. That was not tested.
- **Pre-registration was not committed to git before the run.** It sits in the docstring, written before any rung ran on H. The JSON records the script SHA-256 (52cbb153...) and start time 16:25:35 UTC. Before the full run, a dev self-test on 40 TRAINING verses ran to check the machinery. After it I added one display column to Table 2 and the held-verse indices to the JSON; no test, setting or analysis changed. In the dev run the marker models were also larger than baseline, but on training verses.
- **Marker word values include held-out verses.** The project's word values that pick the markers (shifting_word.word_values) were computed from all verses, held-out included. I kept them unchanged because the models were trained with them. This affects only WORDS ONLY; TOTAL pays for every marker. WORDS ONLY is an accounting number, not a decodable seed.
- **Context is the previous held-out verse, not the true neighbour.** Each held-out verse is coded with the earlier held-out verses (50 verses back) as context. H is coded as 12 fixed groups, so context restarts 12 times. This is the same for every model rung.
- **Normalisation drops detail for every rung alike:** capitals, verse numbers, apostrophes and hyphens are gone; only lowercase words and . , ; : ? ! remain.
- **Accounting details.** Per-verse bits are ideal code lengths of the same rounded probabilities the coder uses; the real seed is about 4–5 bytes more than their sum. xz's size includes its container header (about 60 bytes).
- **Scale honesty:** these are tiny models; the results do not say how a large AI understands.
- **What I did not deliver:** the seed bitstreams were not saved as files, only their SHA-256 and sizes. The models are not in git. Nothing was committed, pushed, zipped or sent; that is left for the main session.


### Run time

Full run took 23.9 minutes (1,432 s) on 2 threads. Each transformer took about 42 s to encode plus 42 s to decode; R8 took 7–16 s per direction; R3–R5 1–2 s; setup (marking, SVD word values) about 1 minute. The dev self-test took 2.2 minutes.


### Results files

/home/user/utensil-theories-transfer-protocol/experiments/results_understanding.json (441 KB). It holds:
- every rung's seed bytes, bpc, % smaller than raw, exact flag, seed SHA-256 and regrown SHA-256;
- per-verse TOTAL and WORDS ONLY bits for every model;
- the paired tests, method summary, context growth and pre-registered verdict;
- meta: script SHA-256 52cbb153d57d08b3..., H SHA-256 80d0ffa0..., held verse indices, versions.

/home/user/utensil-theories-transfer-protocol/experiments/results_understanding.txt (the printed tables).

Dev self-test output (scratch only, not part of the delivery): /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/results_understanding_dev.txt and .json. Full run log: /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/full_run.log
