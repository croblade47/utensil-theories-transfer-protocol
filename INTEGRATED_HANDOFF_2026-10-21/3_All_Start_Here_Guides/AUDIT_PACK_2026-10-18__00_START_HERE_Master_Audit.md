Audit Pack: Comprehension Research

Built 18 October 2026 by a Claude Code session (a second AI checking the
first). Ideas and direction: Garrett Gauthier. Code and experiments:
built with Claude.

**Start here.** This folder holds actual copies of every file, not
links. Everything a reviewer (you or another AI) needs is inside it.

1\. The short answer

- **Goal:** make an AI understand people better, so it communicates
  better.

- **How close:** about rung 1 of 5. Two small signs of better
  understanding inside a very small model. Communication has not been
  tested, and nothing has been tried on a real-size AI.

- **Aesop test (finished 07:34):** all four checks failed. In this small
  model, folk tales did not teach morals that carry over to fables it
  had never seen.

- **Numbers:** all headline numbers match the raw results files.

- **Problems:** some wording is stronger than the evidence. One test was
  changed after a peek. The work drifted toward the measuring tool and
  away from the goal.

2\. Timeline (UTC; rows shaded red are problems)

Commit codes (like 6fc220d) can be looked up in the repository to see
exactly what changed and when.

<table>
<colgroup>
<col style="width: 14%" />
<col style="width: 44%" />
<col style="width: 19%" />
<col style="width: 21%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>When</strong></th>
<th><strong>What happened</strong></th>
<th><strong>File / commit</strong></th>
<th><strong>Verdict</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>17 Oct 21:41</td>
<td>Previous session ("Human error encoding system") starts.</td>
<td>-</td>
<td></td>
</tr>
<tr class="even">
<td>17 Oct 21:43</td>
<td>First script: a keyword detector that reads people's emotional
"weight". Later dropped: the goal is the AI's understanding, not reading
people.</td>
<td><p>d8ebeec</p>
<p>resonance/</p></td>
<td>Off-goal start, corrected</td>
</tr>
<tr class="odd">
<td>17 Oct 22:08</td>
<td>Experiments 1-4: a word-meaning model of the Bible. Color learned 10
of 14 (chance 17%). Rules alone were no better than stories.</td>
<td><p>ec22991</p>
<p>bible_understanding.py</p></td>
<td>No pass/fail rules saved first; can't be checked from git</td>
</tr>
<tr class="even">
<td>17 Oct 22:16</td>
<td>Experiment 5: predict consequences in 20 new stories. Chance.</td>
<td>939d60f</td>
<td>Failure, reported plainly</td>
</tr>
<tr class="odd">
<td>17 Oct 22:42</td>
<td>Experiment 6: tiny transformer on the Bible. Learned the language,
chance on consequences.</td>
<td><p>1a4dfac</p>
<p>tiny_transformer.py</p></td>
<td>Failure, reported plainly</td>
</tr>
<tr class="even">
<td>17 Oct 23:03-23:46</td>
<td>Experiment 7: the owner's shifting word (velanok). 68% vs 52%
scrambled, on the same 20 pairs, 2 runs. Called "the first result above
chance".</td>
<td><p>f676eed-c918cb7</p>
<p>shifting_word.py</p></td>
<td>PROBLEM: no pass/fail rules first; 20 pairs only. Later shown to be
luck</td>
</tr>
<tr class="odd">
<td>18 Oct 00:52</td>
<td>Pass/fail rules saved for experiment 8 (100 new story pairs). Good
practice starts here.</td>
<td><p>5538b46</p>
<p>confirm.py</p></td>
<td></td>
</tr>
<tr class="even">
<td>18 Oct 01:03-02:21</td>
<td>Experiment 8 models score one by one. Judging is visibly strong in
the early results.</td>
<td>results_confirm.json</td>
<td></td>
</tr>
<tr class="odd">
<td>18 Oct 01:57-02:37</td>
<td>Aesop test rules drafted, then fixed twice, all before any
training.</td>
<td>87cccf9, 194fc7c, 910e9cb</td>
<td>Done right</td>
</tr>
<tr class="even">
<td>18 Oct 01:58-02:02</td>
<td>Communication guide, first handoff and plan written.</td>
<td>b58b583, cde3dac, 6143fa8</td>
<td></td>
</tr>
<tr class="odd">
<td>18 Oct 02:17</td>
<td>Pass/fail rules saved for experiment 10, with judging as the main
measure.</td>
<td><p>6e365ef</p>
<p>method_comparison.py</p></td>
<td>PROBLEM: 7 of 9 experiment-8 models had already shown judging was
strong. Measure chosen after a peek</td>
</tr>
<tr class="even">
<td>18 Oct 02:35</td>
<td>Experiment 8 written up: consequences NOT confirmed (51/100;
experiment 7 was luck). Judging 69 vs ~50, but only a side measure.</td>
<td>a5f1a6b</td>
<td>Honest result</td>
</tr>
<tr class="odd">
<td>18 Oct 02:58</td>
<td>Scoring fix for the 3-spelling method, after the first experiment-10
model had scored.</td>
<td>ca1f8c9</td>
<td>Minor: the write-up says results for the 5-spelling methods were
unchanged</td>
</tr>
<tr class="even">
<td>18 Oct 03:40</td>
<td>Aesop test (experiment 9) starts on the other machine. 16 models,
about 6-8 hours.</td>
<td>aesop_test.py</td>
<td>Finished 07:34 (see below)</td>
</tr>
<tr class="odd">
<td>18 Oct 03:41</td>
<td>Experiment 10 written up: carry and plain label tie on short stories
(68.7 vs 67.7).</td>
<td>9c6fb86</td>
<td>Honest result</td>
</tr>
<tr class="even">
<td>18 Oct 03:44</td>
<td>Pass/fail rules saved for experiment 11 (long stories).</td>
<td><p>99622d3</p>
<p>long_story_test.py</p></td>
<td></td>
</tr>
<tr class="odd">
<td>18 Oct 03:45</td>
<td>Scoring changed: exact ties count as half right. Found after the
first model scored 0/100.</td>
<td>c93f383</td>
<td>PROBLEM (mild): change after a result was seen</td>
</tr>
<tr class="even">
<td>18 Oct 03:51</td>
<td>Test design changed during run 1: stories made longer so the first
marker is also out of view. First-run results were not kept.</td>
<td>6fc220d</td>
<td>PROBLEM: design changed after peeking. First-run results recovered
later (see 07:35)</td>
</tr>
<tr class="odd">
<td>18 Oct 04:04</td>
<td>Experiment 11 written up: "L2 CONFIRMED". Carry 59 vs label 53 per
100, all 3 runs.</td>
<td>01b9050</td>
<td>OVERSTATED: should be "supported once"</td>
</tr>
<tr class="even">
<td>18 Oct 04:10</td>
<td>Exploratory start-marker run: the carry model "carries perfectly but
updates poorly".</td>
<td>11982b6</td>
<td>Exploratory, labeled as such</td>
</tr>
<tr class="odd">
<td>18 Oct 04:16</td>
<td>Accuracy pass by three review agents.</td>
<td>226f68c</td>
<td>PROBLEM: missed the 03:45 / 03:51 changes</td>
</tr>
<tr class="even">
<td>18 Oct 04:17-05:4x</td>
<td>Aesop partial results pushed (7 of 16 models).</td>
<td>results_aesop.json</td>
<td></td>
</tr>
<tr class="odd">
<td>18 Oct 05:47</td>
<td>Objective and "drift guard" added to the handoff. The owner restates
the goal: communication.</td>
<td><p>2b3d28e</p>
<p>HANDOFF.md</p></td>
<td>Drift admitted, not yet acted on</td>
</tr>
<tr class="even">
<td>18 Oct 05:47-06:40</td>
<td>New session (this audit) re-checks every headline number against the
raw files. Numbers match. Wording and timing problems found.</td>
<td>this folder</td>
<td></td>
</tr>
<tr class="odd">
<td>18 Oct 06:52</td>
<td>Audit prompt, approved by the owner, sent to the test session. It
re-checked the audit numbers, found them correct, and agreed to the
steps.</td>
<td><p>send_message</p>
<p>1_Prompt_for_Other_AI</p></td>
<td></td>
</tr>
<tr class="even">
<td>18 Oct 07:33-07:34</td>
<td>Aesop test finished (16 models). All four pre-registered checks NOT
CONFIRMED: folk tales 52.3, novels 54.1, shuffled tales 53.1, Bible 43.6
right per 100 (50 = chance).</td>
<td><p>7fdad39, 29a94aa</p>
<p>results_aesop.txt</p></td>
<td>Failure, reported plainly</td>
</tr>
<tr class="odd">
<td>18 Oct 07:35</td>
<td>Audit corrections applied to HANDOFF, README and PLAN (two commits;
one item was missed on the first pass).</td>
<td>2a58b61, 6bfa507</td>
<td>Done</td>
</tr>
<tr class="even">
<td>18 Oct 07:35</td>
<td>The first long-story runs, thought lost, were found and saved.
Before the 03:51 design change, run 1 already showed shifting 59 vs
label 54.5 on everyday acts: the same as the final result.</td>
<td>results_long_story_v1_flawed_run1.json, _run2.json</td>
<td>Good news: the 03:51 change did not create the L2 result</td>
</tr>
<tr class="odd">
<td>18 Oct 07:36</td>
<td>Aesop results folder delivered to the owner. Standing rules
(CLAUDE.md) copied onto the research branch.</td>
<td><p>d93b6f7, df59cfc, 49e10f0</p>
<p>AESOP_RESULTS_2026-10-18/</p></td>
<td>Done</td>
</tr>
<tr class="even">
<td>18 Oct 07:40</td>
<td>This audit merged with the research branch, so everything is in one
place.</td>
<td>branch ccr-1be0d913-1tlzao</td>
<td></td>
</tr>
<tr class="odd">
<td>Separate project, 18 Oct 02:51</td>
<td>A "Master Patent-Ready Theory" file for the zine project, made in
another session.</td>
<td>f6f4c6e on branch ccr-4507ebbb-bfz236</td>
<td>PROBLEM: named .doc but is a web page, so many phone apps can't open
it. Real .docx copy made here</td>
</tr>
</tbody>
</table>

3\. What went wrong, and the fix

| **Problem**                               | **What happened**                                                                                                                                                                                                        | **Evidence**                                                       | **Fix**                                                                                                                                                                                                                                         |
|-------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Drift from the goal                       | All 11 experiments measure moral judging of Bible-style sentences in a 3.4-million-parameter model. None measures communication, and none uses a real-size AI.                                                           | HANDOFF.md, "Objective and drift guard"                            | Next step: a conversation test (does carried state keep a model true to what a person said early on?), with a large AI as the reader.                                                                                                           |
| Claim before proof (exp 7)                | 68% on 20 pairs was announced as the first result above chance, with no pass/fail rules saved first. On 100 new pairs it was 51%: luck.                                                                                  | c918cb7, a5f1a6b, results_shifting_word.json, results_confirm.json | Already corrected in README. Rule: no headline without saved pass/fail rules.                                                                                                                                                                   |
| Main measure chosen after a peek (exp 10) | Judging became the main measure at 02:17, after most experiment-8 models had shown judging was strong.                                                                                                                   | 6e365ef vs commits 01:03-02:08                                     | Say so in README. The judging claim needs a fresh test with judging as the main measure from the start.                                                                                                                                         |
| Test changed mid-run (exp 11)             | Two changes at 03:45 and 03:51, after the first scores, and the first-run results were not kept at the time (recovered at 07:35). "Confirmed" is too strong.                                                             | c93f383, 6fc220d, 01b9050                                          | Call it "supported once" (done at 07:35). Update: the recovered run 1 shows the same gap before the change (59 vs 54.5), so the change did not create the result. It is still one set of stories: repeat on fresh stories at several distances. |
| Same stories reused                       | Experiment 11 reused the same 100 story acts as experiments 8 and 10.                                                                                                                                                    | long_story_test.py (ITEMS_V2)                                      | The fresh-story re-test fixes this.                                                                                                                                                                                                             |
| Hidden shape of the effect                | "+6 per 100" hides that the carry model gives no answer on about 65 of 100 pairs. When it answers, it is right 81 times, wrong 25.                                                                                       | results_long_story.json; 6_Number_Check output                     | Report both numbers.                                                                                                                                                                                                                            |
| Wrong wording                             | README says the plain label is blind to the act "by design". It isn't: it writes its own markers too, which is how it scored 97 in one run.                                                                              | README.md exp 11; long_story_test.py judge_marked()                | Delete "by design" and explain.                                                                                                                                                                                                                 |
| Headline without its caveat               | HANDOFF opens with "Works:" for judging, but judging was never pre-registered as the main measure.                                                                                                                       | HANDOFF.md "In short"                                              | Change to "strong and repeated, not yet pre-registered".                                                                                                                                                                                        |
| Lost evidence                             | Marker diagnostics were never saved. The first experiment-11 runs were thought lost, but were recovered at 07:35. Trained models and data aren't in git, so a fresh machine must retrain (about 2.5 hours for exp 8/10). | README exp 11; HANDOFF "Files"                                     | Save every run, flawed ones included. Consider storing models outside git.                                                                                                                                                                      |
| Files hard to find or open                | Results live on a side branch, not main. The zine master file is a web page named .doc. Nothing was sent as a downloadable file.                                                                                         | branches; 5_Other_Master_Files                                     | This folder. Strict file rule added to CLAUDE.md.                                                                                                                                                                                               |
| Missing tools                             | No API key, so the large-AI test was never run. Gutenberg and Archive.org were blocked. A new container has no torch or saved models.                                                                                    | HANDOFF "How to run"                                               | Add an API key, or use helper AI copies as readers with blind, rule-based scoring.                                                                                                                                                              |
| Public repository                         | The repository is public, with an MIT license. Everything in it, including the zine "patent-ready" file with your email address, is readable by anyone. This audit first said "private", which was wrong.                | GitHub repository settings (visibility: public)                    | Your decision. If you plan a patent, ask a patent attorney before anything more is made public. To change: GitHub, Settings, Danger Zone, Change visibility.                                                                                    |
| Review missed things                      | Three review agents (04:16) did not catch the mid-run test changes.                                                                                                                                                      | 226f68c                                                            | Reviewers should be given the git timeline, not just the write-ups.                                                                                                                                                                             |

4\. What held up (re-checked from raw files)

<table>
<colgroup>
<col style="width: 24%" />
<col style="width: 36%" />
<col style="width: 39%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Test</strong></th>
<th><strong>Raw numbers (per 100 pairs)</strong></th>
<th><strong>Plain meaning</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Judging, short stories (exp 8/10)</td>
<td><p>Shifting word 67, 72, 67 (avg 68.7)</p>
<p>Plain label 71, 69, 63 (67.7)</p>
<p>3-spelling carry 66, 72, 74 (70.7)</p>
<p>No marker 49, 60, 40 (49.7)</p>
<p>Scrambled 56, 42, 60 (52.7)</p></td>
<td>Labeling right/wrong in training text: about 19 more right per 100
than plain text. Strong, repeated, not pre-registered as main
measure.</td>
</tr>
<tr class="even">
<td>Shifting vs plain label, short (exp 10)</td>
<td>20 better, 18 worse pairs (p = 0.44)</td>
<td>Tie. Matches the write-up.</td>
</tr>
<tr class="odd">
<td>Shifting vs no marker / scrambled</td>
<td>54-26 (p = 0.001) / 57-25 (p = 0.0003)</td>
<td>Matches the write-up.</td>
</tr>
<tr class="even">
<td>Long story, everyday act (exp 11, L2)</td>
<td><p>Shifting 59, 56, 63 vs label 54.5, 51, 54</p>
<p>43 better, 21 worse (p = 0.004)</p></td>
<td>About 6 more right per 100. Supported once, not confirmed (see
timeline).</td>
</tr>
<tr class="odd">
<td>Long story, verdict stated (L1)</td>
<td>Label won 74 pairs, shifting 11</td>
<td>Failure for the carry idea. Reported plainly.</td>
</tr>
<tr class="even">
<td>Consequences (exp 5, 6, 8)</td>
<td>51 per 100 in exp 8</td>
<td>Chance. Failure.</td>
</tr>
<tr class="odd">
<td>Aesop (exp 9): do folk tales teach morals that transfer to fables
never seen?</td>
<td><p>Folk tales 52.3, novels 54.1, shuffled tales 53.1, Bible 43.6 (4,
4, 4 and 2 runs)</p>
<p>No-word-clue pairs: folk tales 60.2 (p = 0.065)</p>
<p>A simple word-overlap count, no model, gets 76.1</p></td>
<td>All four checks NOT CONFIRMED. Stories did not beat novels or
shuffled stories, and every model did worse than plain word matching.
Failure, reported plainly. Checked against results_aesop.txt.</td>
</tr>
</tbody>
</table>

Scale caveat: these are results in a 3.4-million-parameter model trained
on one book. They do not change how a large AI like Claude understands
anyone.

5\. Technical details for reviewers

| **Item**                                | **Detail**                                                                                                                                                                                                                                                                                                                                       |
|-----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Repository                              | github.com/croblade47/utensil-theories-transfer-protocol. Owner: croblade47 (Garrett Gauthier's GitHub account, sole admin). PUBLIC: anyone on the internet can read it. MIT license: anyone may reuse the code.                                                                                                                                 |
| Research branch                         | ccr-1be0d913-1tlzao (NOT on main). Now holds everything: research, Aesop results, this audit folder and the standing rules. Research commits run 17 Oct 21:43 to 18 Oct 07:36 UTC, plus "partial results" commits.                                                                                                                               |
| This folder in the repo                 | AUDIT_PACK_2026-10-18/ at the top of the research branch ccr-1be0d913-1tlzao. The same copy is also on branch ccr-1be0d913-audit-pack.                                                                                                                                                                                                           |
| Software (reported by previous session) | Python 3.13.16, torch 2.14.1, numpy 2.5.3, 4 CPU cores. Exact seed reproduction needs these versions.                                                                                                                                                                                                                                            |
| Model                                   | Small GPT-style transformer trained from scratch: 4 layers, 4 heads, width 192, window 64 tokens (Aesop: 128), dropout 0.1, tied embeddings, AdamW (weight decay 0.1) with one-cycle schedule, 1,500 steps. About 3.4 million parameters. Word-level tokenizer.                                                                                  |
| Training text                           | King James Bible: 31,102 verses, about 793,000 words. Every 50th verse held out to check language learning.                                                                                                                                                                                                                                      |
| Shifting word settings                  | RESET = 17 on a clear right/wrong; SPEND = 0.5 per word toward zero; cap ±51; RECHARGE off. Five spellings: anoksha, oksharu, velanok (unresolved), sharuvel, ruvelan. Clear choices = Bible verdict phrases plus the 3% most strongly worded verses at each end (2,029 verses). Word values from a good/evil direction in a word-meaning model. |
| Methods compared                        | baseline (no marker), scrambled (random spelling), shifting (carry, 5 spellings), label (per-verse only, no carry), carry3 (carry, 3 spellings). Seeds 0, 1, 2.                                                                                                                                                                                  |
| Judging score                           | Marked models: the model writes its own marker after the story; the score is the probability-weighted lean of that marker. No-marker model: log-probability of the "right" phrase minus the "evil" phrase.                                                                                                                                       |
| Long-story setup (exp 11)               | Act, then neutral filler sentences (max 10) until both the act and the first marker are outside the 64-token window. The model writes a marker after each sentence (greedy choice). Exact ties count as 0.5.                                                                                                                                     |
| Statistics                              | Pair-by-pair one-sided sign test (binomial), 3 runs summed per pair.                                                                                                                                                                                                                                                                             |
| Aesop test (exp 9)                      | 67 fables (none in training), 1,131 same-format pairs, 284 no-word-clue pairs. Training sets of about 700k tokens: folk tales (9 collections, 8 cultures), shuffled folk tales, novels (Austen, Chesterton, Melville), Bible. Pass/fail rules P1, P2, P2b, P3 in the aesop_test.py docstring.                                                    |
| Not saved anywhere                      | experiments/data/ (re-downloads automatically) and experiments/models/ (must be retrained).                                                                                                                                                                                                                                                      |
| Re-check the numbers                    | Run: python3 6_Number_Check/check_numbers.py. It reads the copies in 4_Raw_Results and should print exactly 6_Number_Check/check_numbers_output.txt.                                                                                                                                                                                             |

6\. Every file in this folder

Paths are relative to the AUDIT_PACK_2026-10-18 folder. The same folder
is at the top of the research branch ccr-1be0d913-1tlzao (and on
ccr-1be0d913-audit-pack).

| **File (path in this folder)**                       | **What it is**                                                                                                                                                                                                                    |
|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 00_START_HERE_Master_Audit.docx                      | This document.                                                                                                                                                                                                                    |
| 1_Prompt_for_Other_AI.docx / .md / .txt              | Draft prompt to bring the running session back on track. For you to review and edit before sending. Same text in three formats.                                                                                                   |
| 2_Research_Notes/HANDOFF (.docx, .md)                | Summary of where things stand (with the audit corrections applied at 07:35).                                                                                                                                                      |
| 2_Research_Notes/as_audited_before_corrections/      | All six research notes exactly as they were when audited, before the corrections. Compare with the corrected versions one level up.                                                                                               |
| 2_Research_Notes/COMMUNICATION_GUIDE (.docx, .md)    | How you explain things, and how an AI should translate them.                                                                                                                                                                      |
| 2_Research_Notes/PLAN (.docx, .md)                   | Planned next steps.                                                                                                                                                                                                               |
| 2_Research_Notes/README (.docx, .md)                 | Full write-up of every experiment.                                                                                                                                                                                                |
| 2_Research_Notes/PRIOR_WORK (.docx, .md)             | Related published research, and what looks new.                                                                                                                                                                                   |
| 2_Research_Notes/NEXT_SESSION_PROMPT (.docx, .md)    | Prompt used to start new sessions.                                                                                                                                                                                                |
| 3_Code/\*.py                                         | All experiment scripts (experiments 1-11), plus the early resonance engine in 3_Code/resonance/.                                                                                                                                  |
| 4_Raw_Results/results\_\*.json, \*.txt               | Raw scores every claim is based on. Includes the final Aesop results (results_aesop.json, results_aesop.txt) and the recovered first long-story runs (results_long_story_v1_flawed_run1.json, \_run2.json).                       |
| 5_Other_Master_Files/MASTER_PATENT_READY_THEORY.docx | Zine project master file, converted to a real Word file so it opens anywhere.                                                                                                                                                     |
| 5_Other_Master_Files/...\_original_webpage.doc       | The original file as made (a web page with a .doc name). Kept for the record.                                                                                                                                                     |
| 7_Strict_File_Rules (.docx, .md)                     | Your standing rules for every AI session: real files saved into the folder as they are made, never links, nothing locked or permission-blocked. Same text as CLAUDE.md at the top of the repo, which sessions read automatically. |
| 9_Aesop_Results_copy/                                | Full copy of the Aesop results folder made by the test session (its own start-here guide, write-up in Word, raw results, code). The original is AESOP_RESULTS_2026-10-18/ at the top of the research branch.                      |
| 8_Build_Scripts/build_master_doc.js                  | The script that builds this master doc (run: node build_master_doc.js out.docx). Kept so anyone can rebuild or check it.                                                                                                          |
| 6_Number_Check/check_numbers.py + output             | Script that recomputes the headline numbers from the raw results, and what it printed.                                                                                                                                            |

Where the originals live

- **Research files:** branch ccr-1be0d913-1tlzao, folders experiments/
  and resonance/.

- **Zine master file:** branch ccr-4507ebbb-bfz236, file
  MASTER_PATENT_READY_THEORY.doc.

- **Where this pack was built:**
  /home/user/utensil-theories-transfer-protocol/AUDIT_PACK_2026-10-18 in
  a temporary cloud machine. That machine is deleted later, so the
  repository and your downloaded copy are the lasting ones.

7\. Questions to give another AI reviewer

1.  Do the headline numbers in README.md match the raw files in
    4_Raw_Results? (Run 6_Number_Check.)

2.  Compare the git timeline above with each claim. Was any pass/fail
    rule changed after results were seen, beyond the ones listed?

3.  Is "supported once" the right label for experiment 11, L2? Would you
    go weaker or stronger?

4.  Does the long-story test leak information other than the carried
    markers (for example story length, or the label model's own
    markers)?

5.  Which single next experiment would move closest to the real goal:
    better communication by a real-size AI?

6.  Is anything in the write-ups stated more strongly than the numbers
    allow?

Give the reviewer the whole folder, and ask it to cite file names and
commit codes for every claim it makes.
