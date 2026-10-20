# Fact check and credit landscape (20 October 2026)

Published figures checked through web-search extracts of the primary pages (direct page fetching was blocked in the sandbox, so each caveat says how the figure was seen).


## What already exists, and what could still be the owner's credit

HOW THIS WAS CHECKED: every figure was confirmed through web-search extracts of the primary pages. Direct page fetching was blocked in this sandbox (WebFetch DNS failure; curl got a proxy 403), so the caveats mark anything seen only second-hand. Nothing was edited, committed or sent.

ALREADY EXISTS (the owner cannot claim these as new):
1. The core idea: understanding = prediction = compression, and the seed only needs to carry the 'surprise'. This is Shannon (1948/1951), arithmetic coding, Kolmogorov complexity (Solomonoff 1960/64, Kolmogorov 1965, Chaitin 1966/69), the Hutter Prize rationale (2006 onward), Delétang et al. 2023, and Huang et al. 2024 (r = −0.93 between compression and benchmark scores).
2. A 'data seed plus fixed shared grow instructions regrows exact data': this is model-based lossless compression. Prior art: Schmidhuber & Heil 1996, cmix, NNCP, LLMZip, ts_zip, and the 2026 Hutter record (fx2-cmix-T, 100,424,672 bytes, which uses an offline-pretrained 6M-parameter Transformer as a shared greenhouse). Procedural seeds (Minecraft, 2^64 worlds) are the same pattern for generated content.
3. The 'greenhouse' (shared prior knowledge): the Brotli 122,784-byte static dictionary, zstd trained dictionaries for small similar files, Shared Brotli RFC 9841, and LoRA-adapted LLM coders (Rinberg et al. 2026, 2× gain). The 'library factors' (strawberry/orange vs cucumber) are a shared codebook or dictionary.
4. The 'graph method' (find an expression whose 0/1 plot is the page): this is searching for a short program, i.e. Kolmogorov complexity. It is uncomputable in general, and the pigeonhole argument means it cannot shrink most pages. The 'it's all in there somewhere' version is the πfs joke, and inferencefs is the same joke with an LLM.
5. The weakness that the greenhouse must already be shared: the adjusted rate (14,008% when the 70B model must be shipped) is published.
6. Determinism as a requirement (LibNC, PyTorch docs, ts_zip, Thinking Machines 2025) is known.
7. Marker or conditioning tokens in training text: CTRL (2019) and MeCo (2025, 33% less data).

COULD STILL BE NEW AND CREDITABLE (honest, specific):
A. An empirical result about one particular training signal. Show that training a small LM with the owner's 'shifting word' (a carried right/wrong balance reset to ±17 and spent by the following words) makes the model a better lossless compressor of held-out plain narrative text it never saw (e.g. Aesop, other fables), measured in bits per character. Conditions for credibility:
   - Markers are removed at test time (MeCo-style), or their bits are counted if they stay in.
   - Same parameter count, compute and token budget as the controls.
   - Controls: plain text, a shuffled or random-value marker (same token count, to rule out a 'regularizer' effect), a per-verse plain label, carry3, and a MeCo-style prepended tag.
   - Several random seeds, with confidence intervals.
   - Exact decode check: actually arithmetic-code and decode the text byte-for-byte, deterministically on CPU.
   If the shifting word wins beyond noise, that is a new finding: a narrative-consequence or moral-state carry signal improves compression, and so measured understanding. Nothing found in this search covers that specific signal. If it does not win, publishing the honest null result is still a creditable contribution.
B. A 'seed bits as an understanding meter' teaching protocol. Measure how many bits a model needs to regrow a story exactly, before and after it is taught something (a moral, a rule). The drop in bits is 'understanding gained', in plain numbers. The idea that codelength measures learning is related to prequential/MDL work (e.g. Blier & Ollivier 2018, not verified in this pass), so the creditable part is the specific protocol, the dataset, and the child-friendly demo, not the principle.
C. The plain-language framing and teaching story. The soil, greenhouse, humidity and sun rotation (fixed shared rules plus determinism), air and microbes (checks), seed (only the surprise), and growing in stages map cleanly onto shared model, deterministic inference, verification and residual bits. Original explainers are creditable as authorship, though not as a scientific discovery. The AI-free seed_test.py is a good honest demo: seeds win on predictable data and lose on random data, as pigeonhole requires.

PRACTICAL NOTE ON CREDIT: the repository is public under MIT. Anyone may reuse the code and ideas; MIT only requires keeping the copyright notice on copies of the code. It does not protect ideas, and ideas cannot be patented as such. The owner's timestamped public commits establish when they published the write-ups and results, so the credit worth chasing is A (a measured, reproducible result with controls), plus B and C (protocol and pedagogy). The owner should not claim 'compression = understanding', 'regrowing exact data from a seed', or any method that shrinks all data.


## Verified facts


### 1a. Delétang et al. 2023 'Language Modeling Is Compression' (arXiv 2309.10668, ICLR 2024): abstract headline figures
- **Statement:** Abstract: Chinchilla 70B, "while trained primarily on text, compresses ImageNet patches to 43.4% and LibriSpeech samples to 16.4% of their raw size, beating domain-specific compressors like PNG (58.5%) or FLAC (30.3%), respectively." The abstract also says it "has long been established that predictive models can be transformed into lossless compressors and vice versa", and that the equivalence lets you "use any compressor (like gzip) to build a conditional generative model." Rate = compressed size / raw size (lower is better). First posted 19 Sep 2023; revised March 2024.
- **Source:** https://arxiv.org/abs/2309.10668
- **Verified:** yes
- **Caveat:** Checked through search-engine extracts of arxiv.org, the ICLR proceedings and the ar5iv render. Direct page fetches were blocked in this sandbox (WebFetch DNS failure; curl got a proxy 403). The paper's own Table 1 (ar5iv render) shows different raw figures for Chinchilla 70B at a 2048-byte context: ImageNet 48.0% and LibriSpeech 21.0%, not 43.4% and 16.4%. The search did not settle why (different setting, or a change between versions). Safest wording: 'the abstract reports 43.4% and 16.4%'.

### 1b. Delétang et al.: enwik9 rate, gzip, and raw vs adjusted rate (is the model's own size counted?)
- **Statement:** Table 1, Chinchilla 70B row (2048-byte context), raw compression rates: enwik9 8.3%, ImageNet 48.0%, LibriSpeech 21.0%, Random 100.8%. Adjusted rates, which add the model's parameter size to the compressed size: 14,008.3%, 14,048.0%, 14,021.0%, 14,100.8%. On enwik9, gzip gets 32.3% and LZMA2 23.0%. The adjusted rate is about 14,000% because the 70B model is about 140 GB in float16, set against 1 GB of data. So the model is a great compressor only when the decoder already has it (raw rate), and a terrible one if it must be shipped (adjusted rate). The paper also says dataset size puts a hard limit on model size for compression, and that model scaling is 'not a silver bullet'.
- **Source:** https://ar5iv.labs.arxiv.org/html/2309.10668
- **Verified:** yes
- **Caveat:** The Chinchilla row digits come from the ar5iv render quoted in search results. The gzip 32.3% and LZMA2 23.0% enwik9 figures come from a secondary summary (Lacuna), and the 140 GB explanation from an AlphaXiv summary. All agree with each other, but none were read from the PDF table directly. The '100.8' column header (Random) is inferred from layout, not seen.

### 2. LLMZip (Valmeekam et al. 2023, arXiv 2306.04050): bits per character on text8 with LLaMA-7B
- **Statement:** LLaMA-7B used as a next-token predictor with an arithmetic coder gives 0.7101 bits per character on a 1 MB section of text8, and 0.8426 bpc on a 100 KB section of another text. The authors say this beats BSC, ZPAQ and paq8h (those were run on the full 100 MB text8). The abstract presents a new upper-bound estimate of the entropy of English (about 0.709 bpc on text8 per a secondary summary), "significantly smaller" than the earlier estimates of Cover and King (1978) and Lutati et al. (2023).
- **Source:** https://arxiv.org/abs/2306.04050
- **Verified:** yes
- **Caveat:** The 0.7101 and 0.8426 figures come from a search extract of the arXiv HTML (arxiv.org/html/2306.04050), not a direct read. The 0.709 entropy figure is from Emergent Mind (secondary). The authors could not run LLaMA-7B on all 100 MB of text8, so the comparison is a 1 MB sample against full-file baselines, and they warn that results vary with the input text.

### 3a. Hutter Prize: current enwik9 record (as of Oct 2026)
- **Statement:** Current record: Vladimir Ivanov, 'fx2-cmix-T' (fx2-cmix-transformer). Total size 100,424,672 bytes (archive plus decompressor), submitted 24 July 2026. That is a 7.46% improvement, earning €37,300. It uses a 6M-parameter Transformer pretrained offline and runs on one CPU core (about 10 GB RAM, roughly 50 hours). It was the third 2026 win: cmix-lex (Ibrahim Marcouch & Kaido Orav, 26 Jun 2026, 109,671,639 bytes) and cmix-obias (David Freelan, 19 Jul 2026, 108,521,870 bytes) came first. The previous record was fx2-cmix (Kaido Orav & Byron Knoll, 3 Sep 2024, 110,793,128 bytes). Matt Mahoney's LTCB says the awards were made on 30 Sep 2026. Marcus Hutter called it the largest progress in the contest's 20-year history: three wins in one month, 'nearly 10%' total. Next claim threshold: about 99,420,425 bytes (1% better).
- **Source:** http://prize.hutter1.net/
- **Verified:** yes
- **Caveat:** These events are after my training data, so I verified them only through search extracts. Sources: the prize site, the LTCB page (mattmahoney.net/dc/text.html), a GitHub PR (tecunningham/ai-discovery-data #43), and Hutter's X post. I could not open the official table directly. The figures check out arithmetically: 1 − 100,424,672/108,521,870 = 7.46%; €500,000 × 7.46% ≈ €37,300; each earlier step is about 1%; total against 110,793,128 is 9.36%. Note that the 2026 record holder pretrained a small Transformer offline, which is the 'shared greenhouse' idea already in competition use. Older articles (2023 Saurabh Kumar ~114 MB; Orav 112,578,322 in Feb 2024) are outdated.

### 3b. Hutter Prize: stated rationale linking compression and intelligence
- **Statement:** The prize page says the contest "is motivated by the fact that being able to compress well is closely related to acting intelligently, thus reducing the slippery concept of intelligence to hard file size numbers." Supporting reasoning on the site: "In order to compress data, one has to find regularities in them, which is intrinsically difficult." Wikipedia's summary says the organizers believe text compression and AI are equivalent problems. Prize: €500,000 total, €5,000 per 1% improvement, on enwik9 (1 GB of Wikipedia).
- **Source:** https://hutter1.net/prize/index.htm
- **Verified:** yes
- **Caveat:** The phrase 'closely related to acting intelligently' and 'slippery concept of intelligence to hard file size numbers' matched hutter1.net in search results. I could not load the page to confirm every word, so check it before quoting in full. Critics (e.g. arXiv 1803.03407) argue that compression ignores goals and action, so 'compression = intelligence' is contested, not settled.

### 4. Shannon 1951, 'Prediction and Entropy of Printed English'
- **Statement:** Bell System Technical Journal, Vol. 30, No. 1, pp. 50–64 (1951). Using human subjects guessing the next letter, Shannon bounded the entropy of printed English between about 0.6 and 1.3 bits per letter when 100 letters of context are available (27-symbol alphabet; punctuation and case ignored). The Bell Labs abstract page says that with long-range statistics (up to 100 letters) the entropy falls to about 1 bit per letter, which implies roughly 75% redundancy. Cover & King (1978) later used a gambling method and got about 1.3 bits per symbol.
- **Source:** https://www.nokia.com/bell-labs/publications-and-media/publications/prediction-and-entropy-of-printed-english/
- **Verified:** yes
- **Caveat:** The 0.6–1.3 range is confirmed by secondary sources (arXiv 0911.2284, which states it explicitly, and a rare-book listing), not by reading the original BSTJ scan. Context for comparison: LLMZip's ~0.71 bpc on text8 is below Shannon's upper bound, but text8 is lowercase letters and spaces only, and the samples differ.

### 5a. Fabrice Bellard's ts_zip
- **Statement:** ts_zip compresses text files using a large language model (RWKV 169M v4, quantized to 8 bits per parameter, evaluated in BF16) as the predictor, feeding an arithmetic coder. On enwik9 it gets 1.084 bits per byte (135,443,237 bytes), against 1.707 bpb for xz. A GPU is needed for reasonable speed: up to about 1 MB/s on an RTX 4090. The page calls it experimental; it handles text only, and binary files barely compress. Bellard says the model is evaluated in a deterministic, reproducible way, so data compressed on one GPU or CPU can be decompressed on another. The model weights are not counted in the compressed size.
- **Source:** https://bellard.org/ts_zip/
- **Verified:** yes
- **Caveat:** Seen through search extracts of bellard.org/ts_zip and Bellard's encode.su announcement thread. The determinism statement was attributed to the forum post, not the main page. A Hacker News commenter suggested the model may have seen enwik-like data in training (contamination risk); that is unverified.

### 5b. Fabrice Bellard's NNCP
- **Statement:** NNCP is a lossless compressor that uses a neural network as the predictor for an arithmetic coder: an LSTM in v1 (May 2019), a Transformer in v2 (Jan/Feb 2021). The v2 paper says it achieves state-of-the-art results on enwik9 and beats cmix there with a much simpler model. On enwik8 it does not quite reach cmix (1.20 vs 1.19 bpb). The 2023-10-21 build lists enwik9 at 106,632,363 bytes compressed, or 107,261,318 bytes including the program. It is about as slow as cmix, roughly 1000× slower than xz -9, and the GPU build needs NVIDIA CUDA 11.x/12.x on an Ampere, Ada or Hopper GPU.
- **Source:** https://bellard.org/nncp/
- **Verified:** yes
- **Caveat:** From search extracts of bellard.org/nncp, nncp_v2.pdf and readme.txt. NNCP trains its model on the fly while compressing, so no pretrained weights are shipped. That point is from my background knowledge, not re-verified in this pass. I did not confirm its current Large Text Compression Benchmark rank.

### 6a. Brotli's built-in static dictionary
- **Statement:** Brotli (RFC 7932, J. Alakuijala & Z. Szabadka, July 2016) has a predefined static dictionary of 122,784 bytes (about 120 KiB), alongside its sliding window. It holds 13,504 common words and phrases in six languages, 4–24 characters long, drawn from a large text and HTML corpus. About 120 transforms (suffixes, prefixes, capitalization, truncation) expand it to 1,633,984 distinct matchable entries. RFC 9841 (Shared Brotli, Sept 2025) lets a custom shared dictionary replace or extend it.
- **Source:** https://www.rfc-editor.org/rfc/rfc7932
- **Verified:** yes
- **Caveat:** The byte count 122,784 comes from the reference implementation's dictionary.h, which says it 'matches the default RFC 7932 dictionary'. The word and transform counts are from a Cloudflare engineering blog post (blog.cloudflare.com/brotli-compression-using-a-reduced-dictionary/). I recall the RFC's transform table has 121 entries (IDs 0–120); check that if the exact count matters.

### 6b. Zstandard trained dictionaries (purpose: many small, similar files)
- **Statement:** The zstd README section 'The case for Small Data compression' says that "compression algorithms learn from past data how to compress future data. But at the beginning of a new data set, there is no 'past' to build upon." Zstd's training mode (`zstd --train samples/* -o dict`) builds a 'dictionary' from samples. The same dictionary must be loaded for both compression and decompression (`-D dict`), and it improves ratios on small data dramatically. The man page says typical gains range from 10% (at 64 KB) to 5× better (at under 1 KB), recommends more than 100 sample files, and sets a default maximum dictionary size of 112,640 bytes. Gains come mostly in the first few KB, and training only helps when the samples are correlated.
- **Source:** https://github.com/facebook/zstd
- **Verified:** yes
- **Caveat:** Read from mirrors of the README and man page (android.googlesource.com, Ubuntu manpages, Hackage), not the upstream page directly. Exact wording differs slightly between zstd versions.

### 7. πfs ('pi filesystem') joke project and why it saves no space
- **Statement:** philipl/pifs, 'πfs – the data-free filesystem!', jokingly 'stores your data in π' instead of on disk. It relies on the unproven conjecture that π is normal (contains every finite digit string). It looks up each byte separately in π using the Bailey–Borwein–Plouffe hex-digit formula and stores the offsets as metadata on disk. It saves no space: the position where a given string first appears in π is typically about as long as the string itself or longer (this is the counting argument again), and per-byte offsets cost more than the byte. Storing the offsets in π just needs offsets for the offsets. It is also extremely slow, and if the metadata is lost the files are gone. The same author later made 'inferencefs' ('The new data-free filesystem!'), a parody that 'infers' file contents from an LLM's latent space and stores only the filename.
- **Source:** https://github.com/philipl/pifs
- **Verified:** yes
- **Caveat:** The README's framing and the BBP per-byte lookup are confirmed. The 'index is as big as the data' explanation comes from commentary (Hacker News, man-page summaries) and from the pigeonhole argument, not a verbatim README sentence. inferencefs (github.com/philipl/inferencefs) is satire, not a working compressor. It mocks exactly the 'the model already holds your data' claim, so the owner should avoid sounding like it.

### 8. Minecraft world seeds
- **Statement:** A Minecraft world seed is a 64-bit (Java long) number, so there are 2^64 = 18,446,744,073,709,551,616 possible numeric seeds. Procedural generation grows the whole world, effectively without limit, from that seed plus the game's fixed generation code. Text seeds are turned into numbers with Java's String.hashCode(), which limits them to 2^32 = 4,294,967,296 worlds. Much generation uses java.util.Random, which uses only the lower 48 bits of the seed. Seeds in the signed 64-bit range give the same terrain and biomes in Java and Bedrock editions, though structures differ.
- **Source:** https://minecraft.fandom.com/wiki/Seed_(level_generation)
- **Verified:** yes
- **Caveat:** From search extracts of the Minecraft wiki (fandom/gamepedia). Whether randomly generated multiplayer seeds have only 2^48 effective values is disputed between sources. Teaching point: a seed regrows a world the generator chooses, not an arbitrary world you hand it. You cannot pick a 64-bit seed that reproduces a given hand-built map.

### 9a. Counting (pigeonhole) argument: no lossless method shrinks all files
- **Statement:** There are 2^n bit strings of length n, but only 2^n − 1 strings shorter than n (counting the empty string). A lossless compressor must be one-to-one, so it cannot map every length-n input to a shorter output. Any lossless method that shrinks some inputs must leave others the same size or larger, and most strings (random data in particular) cannot be compressed at all.
- **Source:** https://web.stanford.edu/class/archive/cs/cs103/cs103.1134/lectures/08/Small08.pdf
- **Verified:** yes
- **Caveat:** This is standard mathematics, confirmed in Stanford CS103 lecture notes and other course and industry sources (e.g. NCC Group, 'paradoxical compression'). It directly limits the owner's 'graph method': an expression that plots a page of binary can be short only for pages that have structure.

### 9b. Kolmogorov complexity origins (Solomonoff, Kolmogorov, Chaitin)
- **Statement:** The idea that a string's information content is the length of the shortest program that outputs it was developed independently by Ray Solomonoff (1960 report; fuller 1964 papers in Information and Control, as part of algorithmic probability and inductive inference), Andrey Kolmogorov (1965, Problems of Information Transmission) and Gregory Chaitin (papers published 1966 and 1969). Kolmogorov acknowledged Solomonoff's priority once he learned of it, so the measure is sometimes called Solomonoff–Kolmogorov–Chaitin complexity.
- **Source:** https://ethw.org/Ray_Solomonoff
- **Verified:** yes
- **Caveat:** Sources give slightly different dates (Kolmogorov says he reached the idea in 1963–64; Chaitin's first paper was submitted in Oct 1966). Kolmogorov complexity is uncomputable in general. That standard result is from my background knowledge and was not re-verified here; it means no procedure can always find the shortest 'seed'.

### 10. JavaScript Number.MAX_SAFE_INTEGER
- **Statement:** Number.MAX_SAFE_INTEGER is 9007199254740991, which equals 2^53 − 1. JavaScript numbers are IEEE 754 double-precision floats, so integers are exact and compare correctly only within ±(2^53 − 1). MDN's example: Number.MAX_SAFE_INTEGER + 1 === Number.MAX_SAFE_INTEGER + 2 evaluates to true, which is mathematically wrong. Use BigInt for larger integers.
- **Source:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER
- **Verified:** yes
- **Caveat:** Confirmed from MDN's Spanish, French and Portuguese versions of this page (the English URL is the canonical one). This matters for any seed or arithmetic-coding demo in a browser: big-integer arithmetic in plain Number silently loses precision.

### 11. Floating-point non-determinism and why neural/LLM compressors need deterministic inference
- **Statement:** (a) PyTorch docs define deterministic algorithms as ones that, given the same input "and when run on the same software and hardware, always produce the same output", and warn that "this setting alone is not always enough to make an application reproducible." (b) Bellard's LibNC docs: results are fully deterministic "for the same computation on the same system", but the CPU and GPU backends "do not provide the same exact results mainly due to the use of the NVidia Tensor Core which has a device dependent rounding behavior." (c) NNCP v1 (2019) used a custom library relying only on basic IEEE 754 32-bit operations (FMA, division, square root) to get the same results across CPUs and operating systems. (d) Thinking Machines (Horace He, Sept 2025, 'Defeating Nondeterminism in LLM Inference'): most LLM kernels are run-to-run deterministic. The main cause of endpoint nondeterminism is that kernels are not batch-invariant, so results change with server load and batch size, which works through floating-point non-associativity. (e) LLM-compression papers note that a tiny probability mismatch between encoder and decoder desynchronizes the arithmetic decoder, and the error spreads to every later token. So encoder and decoder need bit-identical probabilities: same weights, tokenizer, kernels, and batch shape.
- **Source:** https://bellard.org/libnc/libnc.html
- **Verified:** yes
- **Caveat:** (a)–(d) are confirmed by search extracts of the primary pages, except that the Thinking Machines post itself was seen only through secondary coverage (Simon Willison's blog and others). (e) comes from 2026 preprints (arXiv 2604.02343, 2601.10678, 2609.25624; CIDR 2026 Kipf et al.) seen only in snippets. One search summary said NNCP v2 used PyTorch's deterministic mode, guaranteed only on identical hardware and software. I could not confirm that, and it conflicts with NNCP being built on LibNC, so do not cite it.

### 12a. Prior neural arithmetic coding of text: Schmidhuber & Heil
- **Statement:** J. Schmidhuber and S. Heil, 'Sequential neural text compression', IEEE Transactions on Neural Networks 7(1):142–146, 1996. An earlier related paper is 'Predictive Coding with Neural Nets: Application to Text Compression', NIPS 1994. They combined predictive neural nets with statistical (arithmetic/Huffman-style) coding. On short newspaper articles they beat widely used Lempel-Ziv compressors, but ran about three orders of magnitude slower. Matt Mahoney's 'Fast Text Compression with Neural Networks' (c. 2000) followed up on this line.
- **Source:** https://mailman.srv.cs.cmu.edu/pipermail/connectionists/1996-February/016966.html
- **Verified:** yes
- **Caveat:** From the 1996 Connectionists announcement, the NeurIPS proceedings page and Mahoney's paper. I did not read the full IEEE paper.

### 12b. cmix and the neural-compressor lineage
- **Statement:** cmix (Byron Knoll, GPL) is a context-mixing compressor tuned for maximum compression ratio at very high CPU and memory cost (32 GB+ RAM recommended). It mixes thousands of specialized models, including an LSTM. The LTCB lists cmix v21 at 14,623,723 bytes on enwik8 and about 107.96 million bytes on enwik9. The Hutter Prize winners from 2024 to 2026 (fx2-cmix and its descendants) are built on cmix. The lineage is: Schmidhuber & Heil (1996) → Mahoney's neural/PAQ context mixing → cmix (LSTM mixing) → NNCP (LSTM, then Transformer) → LLM coders (LLMZip, ts_zip, Delétang et al. 2023) → 2026 Hutter record with a pretrained Transformer.
- **Source:** https://mattmahoney.net/dc/text.html
- **Verified:** yes
- **Caveat:** The cmix enwik9 figure was seen only in a search summary of LTCB, and numbers vary by cmix version and by whether the decompressor is counted. Quote the LTCB table directly if a precise number is needed.

### Extra: compression tracks measured intelligence (Huang et al. 2024)
- **Statement:** 'Compression Represents Intelligence Linearly' (Huang et al., arXiv 2404.09937, COLM 2024): across many open LLMs, average benchmark score correlates almost linearly with bits per character on held-out corpora (Common Crawl, GitHub, arXiv math), with Pearson r = −0.93. A follow-up (arXiv 2505.11441, 'Is Compression Really Linear with Code Intelligence?') argues the relationship for code is logarithmic rather than linear.
- **Source:** https://arxiv.org/abs/2404.09937
- **Verified:** yes
- **Caveat:** Seen through search extracts. This is the published version of the owner's framing that 'better understanding = smaller exact seed', so that framing is prior art.

### Extra: conditioning or marker tokens in training (closest prior art to the 'shifting word' marker)
- **Statement:** CTRL (Keskar et al., arXiv 1909.05858, 2019): a 1.63B-parameter LM trained on 'control codes' taken from structure that naturally comes with raw text, used to steer style, content and task. MeCo, 'Metadata Conditioning Accelerates Language Model Pre-training' (Gao et al., arXiv 2501.01956, ICML 2025): prepend metadata such as source URLs to training documents, then drop it in a final cooldown phase. A 1.6B model matched standard pretraining performance with 33% less data, and the metadata can steer the model at inference.
- **Source:** https://arxiv.org/abs/2501.01956
- **Verified:** yes
- **Caveat:** From search extracts of the arXiv and ICML pages. These are the baselines any 'shifting word' result must be compared against (inline marker vs. prepended metadata vs. a shuffled-marker control).

### Extra: shared-knowledge compression in 2026 ('Haiku to Opus in Just 10 bits')
- **Statement:** Rinberg, Carrell, Henniger, Carlini and Warr (arXiv 2604.02343; Harvard, Cambridge, Anthropic). Domain-specific LoRA adapters make LLM-based arithmetic coding about 2× better than the base model alone. Asking for a concise rewrite before coding gives lossy compression ratios of about 0.03. In a 'question-asking' protocol, a small model asks a large one 10 yes/no questions (10 bits), which recovers 23–72% of the capability gap on standard benchmarks and 7–38% on harder ones, at compression ratios of 0.0006–0.004.
- **Source:** https://arxiv.org/abs/2604.02343
- **Verified:** yes
- **Caveat:** Seen through search extracts of the arXiv and AlphaXiv pages. This is very close to the 'tiny seed plus a shared greenhouse' story, already published, including the idea that a better-adapted shared model halves the seed.