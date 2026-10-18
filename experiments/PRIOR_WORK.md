# Prior work: what already exists, and what looks new

Found by three research agents. A separate skeptic agent confirmed that each work exists, the link is right, and the description is accurate. The 18 works below all passed; the agent transcripts aren't available to later sessions, so this list is the record.

## The owner's ideas vs existing work

| Owner's idea | Closest existing work | Same, close, or different? |
|---|---|---|
| Stories teach values to AI better than listed rules | Riedl & Harrison, *Using Stories to Teach Human Values to Artificial Agents* (AAAI-16 workshop WS-16-02, [record](https://scholars.uky.edu/en/publications/using-stories-to-teach-human-values-to-artificial-agents/)). The "Quixote" system turned stories into a reward signal for simple agents. | **Same big idea, ten years earlier.** No controlled stories-vs-rules test. |
| Learn right/wrong from stories, then transfer to new stories | Nahian, Frazier, Riedl & Harrison, *Learning Norms from Stories* (AIES 2020, [arXiv 1912.03553](https://arxiv.org/abs/1912.03553)): trained on the *Goofus & Gallant* comic, then tested transfer | Close. Starts from pretrained models; no rules condition |
| Fable → moral matching test | BIG-bench *understanding_fables* ([GitHub](https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/understanding_fables)), with 189 paraphrased Aesop fables. *MORABLES* (EMNLP 2025, [arXiv 2509.12371](https://arxiv.org/abs/2509.12371)). *STORAL* (NAACL 2022, [ACL Anthology](https://aclanthology.org/2022.naacl-main.374/)). *ePiC*, proverbs (ACL 2022, [ACL Anthology](https://aclanthology.org/2022.acl-long.276/)) | **The test itself is not new.** These only grade existing models. None asks *which training reading* produces the skill |
| Judging right/wrong acts and consequences in short stories | *Moral Stories* (EMNLP 2021, [ACL Anthology](https://aclanthology.org/2021.emnlp-main.54/)). *ETHICS* (ICLR 2021, [arXiv 2008.02275](https://arxiv.org/abs/2008.02275)) | Standard benchmarks, at large scale |
| Rules + when they bend | *MoralExceptQA* (NeurIPS 2022, [arXiv 2210.01478](https://arxiv.org/abs/2210.01478)) | Related |
| Marker words in training text that carry a value judgment | Korbak et al., *Pretraining Language Models with Human Preferences* (ICML 2023, [arXiv 2302.08582](https://arxiv.org/abs/2302.08582)): a `<good>`/`<bad>` tag on every sentence. CTRL (2019, [arXiv 1909.05858](https://arxiv.org/abs/1909.05858)): control codes. Quark (NeurIPS 2022, [arXiv 2205.13636](https://arxiv.org/abs/2205.13636)): graded reward-band tokens | **Close: the established method.** Each tag judges one piece of text alone, with no carry |
| A running balance that is used up as the text goes on | Decision Transformer (NeurIPS 2021, [arXiv 2106.01345](https://arxiv.org/abs/2106.01345)): a "return-to-go" number that counts down. Kikuchi et al. (EMNLP 2016, [ACL Anthology](https://aclanthology.org/D16-1140/)): a remaining-length budget | Close in mechanism, but for rewards or length, not morals |
| Writing hidden state into the text helps small models | Toshniwal et al., chess state tracking (AAAI 2022, [arXiv 2102.13249](https://arxiv.org/abs/2102.13249)) | Supports the idea for small data |
| Networks keep an internal running good/bad score | Maheswaranathan et al. (NeurIPS 2019, [arXiv 1906.10720](https://arxiv.org/abs/1906.10720)) | The shifting word makes that hidden score visible in the text |
| Training reading shapes later values (large scale) | Tice et al., *Alignment Pretraining* (ICML 2026, [arXiv 2601.10160](https://arxiv.org/abs/2601.10160)). Anthropic, *Teaching Claude why* (2026, [post](https://www.anthropic.com/research/teaching-claude-why)): principles plus stories generalized better than bare examples | Supports the direction; doesn't test stories vs rules |

## What looks less explored

As far as these searches show, these combinations have not been tested before. "Not found" is not proof.
1. **The shifting word itself:** a moral balance carried across a whole narrative, reset on clear right/wrong, used up word by word, and written into the text as one invented word with graded spellings. It is used to teach a model trained from scratch to *judge* new stories, with a scrambled control.
2. **A controlled, equal-size test:** train from scratch on stories vs rules vs scripture vs novels, then measure transfer to fables from a culture never seen, with word-overlap shortcuts removed.

## Cautions from the research
- **Spellings vs carry:** our tokenizer treats whole words as tokens, so the shared syllables of the five spellings are invisible to the model. Mechanically, the shifting word is a five-level value tag plus a carry rule. The syllable design would only matter with a sub-word tokenizer, which is a separate test.
- **Reasons may be the active ingredient:** Anthropic's result points to *explaining why* (principles and reasoning) as what generalizes, not story form alone. A fair future control is rules *with reasons attached*.
- **Shortcuts are common:** even large models match morals on surface patterns (MORABLES). Trust the "no word clue" scores most.
