r"""
The numbers test: the owner's numbers 17, 32, 16, 34, 47 in the place of 17 in "W1 = 17 + 4 Remaining"
=======================================================================================================

The owner's words
-----------------
  Day 1: "[w1=17 -<Next word following it equal to (-13)> = +4 Remaining] next emergence of the word
         [W1=17+4 -<next 2 words following equaling (00)>= 0 Remaining] ... the word shifts interpretation
         and the token used to interpret it based a Remaining value from the previous use of it. This may
         continue on for long periods so it must reset to [w1=0] when a clear right or wrong choice exists.
         If wrong the sequence will begin with a value of (-17) and right a value of (+17) ...
         [Note:17,32,16,34,47 are numbers my subconscious mind has focused on for years, they may just be
         random noise or maybe useful i dont know"
  Today: "test the nunbers "17,32,16,34"=?0=-0=+0=00=["47,"="17+4"]"
  Clarification: "I dont know, I just know my sub conscious mind has had those numbers in that sequence and
         the stands for me the +4 was a way to direct you to a way to try testing the numbers where I feel
         like they belong"

PLAIN READING (verbatim from the final design)
----------------------------------------------
Two things are certain. Your numbers come in a fixed order, 17, 32, 16, 34, 47, and the "+4" points to where
they go: the place of 17 in your rule "W1 = 17 + 4 Remaining". That place is the charge the word gets each time
it appears, with whatever was left over last time carried on top. So in this test the word gets a fresh charge
every time it appears. In the plain version the charge is 17 every time. In your sequence version the charges
take turns: 17, 32, 16, 34, 47, 17, 32, and so on. A clear right or wrong restarts the run at +17 or -17, as
your day-1 rule says. The words of each verse use up most of the charge, and the word is spelled from what is
left, as you wrote ("based a Remaining value from the previous use of it"). How fast the words use up the
charge was my choice, not yours. I set it so that in ordinary text the plain rule settles at exactly your
"17 + 4": each verse uses 17 and leaves 4. That choice is what keeps the word from getting stuck at the top,
which is why your original rule was switched off before. Nobody knows what ?0, -0, +0 and 00 mean, so they are
not tested. Reading "47 = 17+4" as "47 also goes in that slot" is a guess, and one model tests it by giving 47
every time.

THE SIX CONFIGURATIONS (verbatim from the final design)
-------------------------------------------------------
num_charge17
  rule: SHARED RULE for all six configs, CHARGE(CH). It goes in a new script, experiments/numbers_test.py,
  which imports shifting_word (word_values, tokens, CLEAR_WRONG, CLEAR_RIGHT, CLEAR_PCT, FORMS, form_for) and
  changes nothing in it.

  Constants, fixed now: RESET = 17, CAP = 51, NBAR = 10.9043 (the mean number of tokens w with w in values per
  TRAINING verse, i % 50 != 0), DRAIN = 1 - (4/21)**(1/NBAR) = 0.141073 (assert this to 6 decimals). Clear
  choices are found exactly as in sw.mark_up: the verdict regex, or the top or bottom 3% of verse sums.

  Go through the verses in order:
  (0) At each book start: R = 0.0, s = 0, k = 0.
  (1) form = form_for(R). The word is spelled from the Remaining before the charge, with the same 5 spellings
      and cuts.
  (2) If s != 0: W = R + s*CH[k % len(CH)] and k += 1. Otherwise W = R.
  (3) Write 'form text'.
  (4) If the verse is a clear choice c = ±1: R = 17*c, s = c, k = 0, and the verse's own words are not read
      (as now). Otherwise x = W; for each token w of the verse with w in values: x += values[w];
      x *= (1 - DRAIN). Then R = clip(x, -51, 51).

  Training: TinyGPT on the training verses (i % 50 != 0), vocab = tt.Vocab(train_texts), CTX 64, 1500 steps,
  seeds 0, 1 and 2. Save as models/num_<name>_seed{s}_steps1500.pt.

  For num_charge17: CH = (17,), a charge of 17 at every appearance after a clear choice.
  owner basis: Day 1: "[w1=17 -<next word (-13)> = +4 Remaining] next emergence of the word [W1=17+4 ...]";
  "the token used to interpret it based a Remaining value from the previous use of it"; "reset to [w1=0] when
  a clear right or wrong choice exists. If wrong the sequence will begin with a value of (-17) and right a
  value of (+17)". In neutral text this rule settles at exactly W = 17 + 4 = 21, leaving 4 Remaining
  (checked).
  why included: The task requires it: the owner's plain recharge rule, never tested before, with N = 17. It
  separates the rule itself from the effect of the numbers. On the Bible markup, with no training: spellings
  10.8/23.1/32.0/20.1/13.9%, 0.03% of verses at the cap, and 55.0% of markers differ from the current
  shifting word.

num_seq
  rule: Same as num_charge17, except CH = (32, 16, 34, 47, 17). After each clear choice the values therefore
  run 17 (the reset) → 32 → 16 → 34 → 47 → 17 → 32 → ... in the direction of that choice. The run cycles
  until the next clear choice, and every clear choice restarts it at 17.
  owner basis: Today: "17,32,16,34 ... [47, = 17+4]". The clarification: "those numbers in that sequence",
  and the +4 shows where they belong, in the 17 slot. Day 1: "syllables rotation sequence" and "This may
  continue on for long periods" (so it cycles rather than stops). The owner's list begins with 17, the same
  value as the day-1 reset.
  why included: The owner's literal numbers, in his order, as N. It does not pin (simulated: spellings
  19.1/20.4/22.2/16.7/21.6%, 0.27% of verses at the cap). Its marker differs from num_charge17 on 28.1% of
  verses.

num_seqrev
  rule: Same as num_charge17, except CH = (47, 34, 16, 32, 17). The values run 17 (the reset) → 47 → 34 →
  16 → 32 → 17 → ...: the same five numbers, the same mean, the same restart at 17, with the cycle reversed.
  owner basis: A control for the one claim the owner is sure of: that the numbers belong "in that sequence".
  why included: The order control. It changes 4 of the 5 charge positions. Its marker differs from num_seq on
  22.3% of verses, the most of the orders checked (the ascending, "logical" order differs on 21.0%).

num_const29
  rule: Same as num_charge17, except CH = (29.2,): the mean of 17, 32, 16, 34 and 47, given at every
  appearance.
  owner basis: Not an owner rule. It is the control that matches the owner's sequence in average size but has
  no variation. It also stands for the single numbers 32 and 34, whose markups differ from it on only 5.5% and
  9.1% of verses.
  why included: It separates 'the owner's sequence' from 'a bigger average charge'. Its marker differs from
  num_seq on 13.5% of verses and from num_charge17 on 30.9%.

num_charge47
  rule: Same as num_charge17, except CH = (47,): a charge of 47 at every appearance. The reset stays at 17.
  owner basis: Today: ["47," = "17+4"]: 47 is written in the place of "17+4". This is the 'singly' half of
  the queued HANDOFF test. Single 16 needs no model of its own: its markup differs from num_charge17 on only
  3.2% of verses.
  why included: It tests the owner's largest number on its own in the slot. Simulated: spellings
  29.0/15.3/13.5/12.2/30.0%, 1.23% at the cap. Its marker differs from num_charge17 on 52.9% of verses.

num_drain0
  rule: Same as num_charge17, except CH = (0,): no charge at all. It keeps the proportional drain, the
  spelling from R, and the ±17 on a clear choice.
  owner basis: Not an owner rule. It is the mechanism control: compared with the current shifting word, the
  new rule changes two things, the drain (my choice) and the recharge (the owner's rule). This control
  isolates the drain.
  why included: It keeps my drain change from taking credit for the owner's rule. Simulated: spellings
  4.4/17.7/52.8/19.8/5.3%. It forgets a verdict fast: the verdict's sign survives 5 verses later only 33% of
  the time, against 65% for num_charge17 and 63% for the current shifting word.

CONTROLS (verbatim from the final design)
-----------------------------------------
These models are reused and not retrained. Each has seeds 0, 1 and 2 at 1500 steps, stored in
experiments/models/{method}_seed{s}_steps1500.pt:
- shifting (RESET 17, the current rule): the main comparator.
- baseline (no marker): the second comparator.
- label, carry3 and scrambled: reported for description only.

Their stored per-item scores are reused unchanged: results_methods.json v2_judge (M1), results_long_story.json
version B 'correct' (M2), and results_understanding.json R6/R7 per_verse_total (M3).

The 18 new models are scored with the same unchanged code paths: method_comparison.score on ITEMS_V2;
long_story_test build_stories and judge_marked for version B with START_MARKER = False;
understanding_compression code_one with each config's own held-out markers.

PRE-REGISTRATION (verbatim from the final design; fixed before any of the 18 models is trained)
-----------------------------------------------------------------------------------------------
This is fixed before any of the 18 models is trained. Nothing is tuned on stories_v2 or on the held-out verses.

0. MANIPULATION CHECK (Bible markup only, before training)
A config passes if at most 5% of verses sit at the ±51 cap and every spelling covers at least 3% of verses. A
config that fails is still trained, but it is labelled 'degenerate' and its results are descriptive only.
Expected values, from the judge's scratch simulation
/tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/judge_numbers/sim_rules.py:
all six pass. The constants are frozen: NBAR 10.9043, DRAIN 0.141073, CAP 51, RESET 17, the CH lists as given,
word_values, SCALE 30, the verdict regexes, CLEAR_PCT 3, FORMS and the cut points.

1. MEASURES (per config, seeds 0, 1, 2)
- M1 (PRIMARY): judging on the 100 stories_v2 pairs, as in exp 10, using method_comparison.score → v2_judge.
  For each pair, the score is the number of seeds that judged it correctly (0-3).
- M2: long-story version B (the everyday act pushed out of the 64-token view, no start marker), as in exp 11.
  For each pair and seed the score is 1, 0.5 for an exact tie, or 0. For each pair, the score is the sum over
  seeds (0-3).
- M3: exact-seed TOTAL bits, as in exp 12. For each of the 623 held-out verses (i % 50 == 0), the TOTAL code
  length (marker + words + verse end), averaged over the 3 seeds. Seed 0 of each config is decoded and must
  regrow H exactly; if it does not, M3 is void for that config.
- Version A and the short version are reported for description only.

2. TESTS (all one-sided, in the direction 'new is better')
- M1 and M2: exact sign test over the pairs whose per-pair sums differ. Ties are dropped.
  p = P(Bin(n, ½) ≥ wins).
- M3: paired sign-flip permutation test on the mean of d_v = new_v − comparator_v. It uses 100,000 flips with
  numpy default_rng(0), and p = (#{permuted mean ≤ observed} + 1) / 100,001. 'Better' means a mean d_v below
  0. The one-sided sign test over verses is reported alongside, and any disagreement between the two tests is
  reported.

3. FAMILIES (Holm correction, alpha 0.05, applied separately within each measure)
- F1: each of the 6 new configs vs shifting.
- F2: each of the 6 new configs vs baseline. On M2 the baseline scores a constant 1.5 per pair, so F2 there
  means 'beats chance'.
- F3, the owner's numbers (4 tests):
  - N1: num_seq > num_charge17
  - N2: num_seq > num_seqrev
  - N3: num_seq > num_const29
  - N4: num_charge47 > num_charge17
- F4, mechanism: R1 num_charge17 > num_drain0. This is a single test at alpha 0.05.

4. VERDICTS (decided on M1)
- 'The owner's numbers matter' = N1 passes on M1: his sequence beats a plain 17 in the same rule.
- 'The sequence itself matters' = N1, N2 and N3 all pass on M1.
- '47 in the 17 slot helps' = N4 passes on M1.
- 'The owner's recharge rule helps' = num_charge17 passes F1 on M1. It is credited to the recharge, and not to
  the AI's drain, only if R1 also passes on M1.
- 'Useful for the project' = any config passes F1 on M1.
- M2 and M3 are judged by the same rules. A pass on M2 or M3 alone is reported as a 'secondary sign', never as
  a confirmation.
- Every other outcome is reported as 'not shown at this scale', never as 'disproved'.
- Effect sizes are reported for every comparison, even when not significant, because the owner counts any
  improvement: mean % correct per seed, wins/losses, and mean bits per verse. label, carry3 and scrambled are
  included for description.
- Expectation, which is not part of the verdict: ties with shifting on M1, as all marker methods have tied so
  far, and num_seq ≈ num_seqrev.

5. LIMITS
Tiny model, 3 seeds, 100 pairs. Only large effects can be detected. word_values were computed on all verses,
including the held-out ones; this is kept as before for comparability and flagged for M3.

DROPPED (verbatim from the final design)
----------------------------------------
- The coded RECHARGE switch (re-add 17·sign at each appearance, spell after the charge, linear SPEND 0.5, cap
  ±51). It pins at the cap, and swapping in 16, 32, 34, 47 or the cycling sequence gives the same marked text,
  so it cannot test the numbers.
- The numbers as successive RESET sizes. That is not the slot the owner pointed to, and only 9.8% of markers
  would change.
- The numbers as SPEND ratios. 17/34 = 16/32 = 0.5, which is the existing model.
- A linear spend calibrated to 17 (reader 3's recharge17spent and seqcyclespent). The owner's numbers (mean
  29.2) then overcharge it, unless SPEND is changed for each config, which would confound size with spend.
- Reader 1's directional bank (signed spend, cap R ≤ N, direction only from verdicts, heavy form at R ≥ 4). It
  adds more invented rules, and under its spend the owner's own example 17 − 13 gives 0 instead of 4.
- Rescaled 'normalized' charges. These are not the owner's numbers as N. The proportional drain makes
  rescaling unnecessary, because the rule never pins for any N.
- seqchoice (a run that stops after 47, with a ±146 cap). Day 1 says the rule 'may continue on for long
  periods', which favours cycling, and the hint from the zero symbols is weak.
- Single 16, 32 and 34. Their markups differ from num_charge17, num_const29 and num_const29 on only 3.2%, 5.5%
  and 9.1% of verses, so those configs cover them.
- The ascending ('logical') order control. The reversed order changes more markers (22.3% vs 21.0%).
- The zero states ?0, -0, +0, 00. The owner has no meaning for them, and testing them would need new invented
  spellings plus a change to the POSITION map in score().
- Numerology (47 = 51 − 4, 21 + 47 = 68, the mirror pattern x, 2y, y, 2x, mod-17 patterns). None of it makes a
  testable claim.
- The start-marker version of M2. It stays exploratory, as in exp 11.

IMPLEMENTATION NOTES (how this script carries out the design; nothing here changes it)
--------------------------------------------------------------------------------------
* shifting_word.py and every other existing file are imported, never edited. The rule is a new class,
  ChargeWord, written from steps (0)-(4) above. The clear choices are computed exactly as in sw.mark_up.
* Spellings: no new spellings. Every config uses the same five words as the current shifting word, with the
  same cuts on the balance it is spelled from (R, the Remaining before the charge):
      R <= -12 anoksha (-2, heavy wrong)   -11..-4 oksharu (-1)   -3..3 velanok (0, unresolved)
      4..11 sharuvel (+1)                  R >= 12 ruvelan (+2, heavy right)
  The numbers in brackets are the wrong..right positions used by scoring (method_comparison.POSITION).
* How each config's marker is used at test time is exactly how the shifting model's is:
    M1  the model writes its OWN marker after each story (method_comparison.score); no rule is applied.
    M2  the model writes its own marker after every sentence (long_story_test.judge_marked, START_MARKER False).
    M3  every held-out verse carries the marker the config's own rule gave it in the full-Bible markup
        (the same marked text the training verses came from), and the marker is paid for in the seed.
* Model files: models/{config}_seed{s}_steps1500.pt, e.g. models/num_seq_seed0_steps1500.pt ("num_<name>" in the
  design is the config name itself). A saved model is never retrained: the run is resumable. Scores already in
  results_numbers.json are not recomputed.
* CPU threads match the earlier experiments: training 4 (tiny_transformer), M1 4 (confirm / method_comparison),
  M2 1 (long_story_test), M3 2 (understanding_compression).
* M3: every seed of every new config is encoded AND fully decoded and compared byte for byte with H (the design
  requires seed 0; seeds 1 and 2 are an extra check, and any mismatch there is reported plainly).
* Holm: within each family and measure; a test passes if its Holm-adjusted p < 0.05. The family size stays as
  pre-registered: a test that cannot be computed (missing models, a void M3, a 'degenerate' config) enters Holm
  with p = 1 and cannot pass.
* Control reproduction check (extra, before training): the stored control scores are reused unchanged, but this
  script also re-scores the saved shifting seed-0 model (and baseline seed 0 on M1) with the same code paths
  and reports whether it reproduces the stored numbers exactly. This checks that the setup matches.
* --dry-run: all six configs at 5 training steps, seed 0 only, 8 story pairs (M1), 4 long-story pairs (M2) and
  the 40 TRAINING verses exp 12 used for its own --dev check (M3, so no held-out verse is touched). It writes
  ONLY to its scratch folder (--scratch, or $NUMBERS_DRY_DIR, or the system temp folder). Its numbers mean
  nothing; it checks the machinery end to end.

Run (from experiments/):
  python numbers_test.py                # full run: 18 models (about 10 min each) + scoring; resumable
  python numbers_test.py --report-only  # rebuild the tables from results_numbers.json, no training
  python numbers_test.py --dry-run --scratch /some/scratch/folder
Writes results_numbers.json (after every step) and results_numbers.txt (final tables).
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True          # the dry run must write only to its scratch folder

import argparse
import hashlib
import json
import os
import tempfile
import time
from collections import Counter
from math import comb
from pathlib import Path

import numpy as np
import torch

import confirm
import long_story_test as lst
import method_comparison as mc
import shifting_word as sw
import tiny_transformer as tt
import understanding_compression as uc
from bible_understanding import load_verses, tokens
from consequences_test import ITEMS as ITEMS_V1
from shifting_word import CLEAR_PCT, CLEAR_RIGHT, CLEAR_WRONG, FORMS, form_for, word_values
from stories_v2 import ITEMS_V2

HERE = Path(__file__).parent
MODELS = HERE / "models"
OUT_JSON = HERE / "results_numbers.json"
OUT_TXT = HERE / "results_numbers.txt"

# ---------------------------------------------------------------------------
# Frozen constants (pre-registered)
# ---------------------------------------------------------------------------

RESET = 17
CAP = 51
NBAR_FROZEN = 10.9043
DRAIN_FROZEN = 0.141073
LEFT_SHARE = 4 / 21              # in neutral text the plain rule settles at W = 21 and leaves 4
STEPS = 1500
SEEDS = [0, 1, 2]
ALPHA = 0.05
MAX_CAP_PCT = 5.0                # manipulation check: at most 5% of verses at the +/-51 cap
MIN_SPELLING_PCT = 3.0           # manipulation check: every spelling on at least 3% of verses

CONFIGS = {
    "num_charge17": (17,),
    "num_seq": (32, 16, 34, 47, 17),
    "num_seqrev": (47, 34, 16, 32, 17),
    "num_const29": (29.2,),
    "num_charge47": (47,),
    "num_drain0": (0,),
}
NEW = list(CONFIGS)
CONTROLS = ["shifting", "baseline", "label", "carry3", "scrambled"]
ALL = NEW + CONTROLS
THREADS = {"train": 4, "M1": 4, "M2": 1, "M3": 2}
POSITION = mc.POSITION                                    # anoksha -2 ... ruvelan +2 (unchanged)

FAMILIES = {
    "F1": [(f"{c} > shifting", c, "shifting") for c in NEW],
    "F2": [(f"{c} > baseline", c, "baseline") for c in NEW],
    "F3": [("N1 num_seq > num_charge17", "num_seq", "num_charge17"),
           ("N2 num_seq > num_seqrev", "num_seq", "num_seqrev"),
           ("N3 num_seq > num_const29", "num_seq", "num_const29"),
           ("N4 num_charge47 > num_charge17", "num_charge47", "num_charge17")],
    "F4": [("R1 num_charge17 > num_drain0", "num_charge17", "num_drain0")],
}

# The judge's scratch simulation (sim_rules.py), printed for comparison with this script's own markup.
JUDGE_EXPECTED = {
    "num_charge17": {"shares": [10.8, 23.1, 32.0, 20.1, 13.9], "cap": 0.03},
    "num_seq":      {"shares": [19.1, 20.4, 22.2, 16.7, 21.6], "cap": 0.27},
    "num_seqrev":   {"shares": [19.7, 19.8, 22.1, 16.5, 21.9], "cap": 0.31},
    "num_const29":  {"shares": [19.4, 20.8, 21.1, 16.7, 22.0], "cap": 0.26},
    "num_charge47": {"shares": [29.0, 15.3, 13.5, 12.2, 30.0], "cap": 1.23},
    "num_drain0":   {"shares": [4.4, 17.7, 52.8, 19.8, 5.3], "cap": 0.00},
}
JUDGE_DIFFERS = {("num_charge17", "shifting"): 55.0, ("num_seq", "num_charge17"): 28.1,
                 ("num_seqrev", "num_seq"): 22.3, ("num_const29", "num_seq"): 13.5,
                 ("num_const29", "num_charge17"): 30.9, ("num_charge47", "num_charge17"): 52.9}

TRACE_BOOK, TRACE_START, TRACE_LEN = "II Kings", "In the twelfth year of Ahaz", 15

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

LOG_LINES: list[str] = []


def log(s=""):
    print(s, flush=True)
    LOG_LINES.append(s)


def stamp():
    return time.strftime("%H:%M:%S")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _jsonable(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(f"not JSON serialisable: {type(o)}")


def atomic_write(path: Path, text: str):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def p_at_least(k, n):
    """P(Bin(n, 1/2) >= k); 1.0 when n == 0."""
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else 1.0


def holm(pvals):
    """Holm step-down adjusted p-values (same order as given)."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj, running = [1.0] * m, 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvals[i]))
        adj[i] = running
    return adj

# ---------------------------------------------------------------------------
# The rule: CHARGE(CH)
# ---------------------------------------------------------------------------

def clear_choices(verses, values):
    """Exactly as in sw.mark_up: verdict phrases, or the top/bottom CLEAR_PCT% of verse sums."""
    sums = np.array([sum(values.get(w, 0) for w in tokens(t)) for _, t in verses])
    lo, hi = np.percentile(sums, [CLEAR_PCT, 100 - CLEAR_PCT])
    clear = np.array([(-1 if CLEAR_WRONG.search(t) or s <= lo else
                       1 if CLEAR_RIGHT.search(t) or s >= hi else 0)
                      for (_, t), s in zip(verses, sums)])
    return clear, sums


def drain_constants(verses, values):
    texts = [t for _, t in verses]
    nval = np.array([sum(w in values for w in tokens(t)) for t in texts])
    nbar = float(nval[[i for i in range(len(texts)) if i % 50]].mean())
    drain = 1 - LEFT_SHARE ** (1 / nbar)
    return nbar, drain


class ChargeWord:
    """The owner's "W1 = N + Remaining": a fresh charge N (taken in turn from CH, in the direction of the last
    clear choice) is added to what was left last time; the verse's words spend it (proportional drain);
    the word is spelled from the Remaining before the charge."""

    def __init__(self, values, CH, drain):
        self.values, self.CH, self.drain = values, tuple(CH), drain
        self.new_book()

    def new_book(self):                                   # step (0)
        self.R, self.s, self.k = 0.0, 0, 0

    def emerge(self):
        form = form_for(self.R)                           # step (1)
        if self.s != 0:                                   # step (2)
            self.charge = self.s * self.CH[self.k % len(self.CH)]
            self.k += 1
        else:
            self.charge = 0
        self.W = self.R + self.charge
        return form

    def read(self, text, clear):                          # step (4)
        if clear:
            self.R, self.s, self.k = float(RESET * clear), int(clear), 0
            self.x = None
            return
        x = self.W
        for w in tokens(text):
            if w in self.values:
                x += self.values[w]
                x *= (1 - self.drain)
        self.x = x
        self.R = float(np.clip(x, -CAP, CAP))


def mark_charge(verses, values, CH, drain, clear):
    """Insert the config's word at the start of every verse. Returns the marked texts and a per-verse record."""
    cw, out, prev_book = ChargeWord(values, CH, drain), [], None
    rec = {"R_spell": [], "form": [], "charge": [], "W": [], "R_after": [], "at_cap_after": []}
    for (book, text), c in zip(verses, clear):
        if book != prev_book:
            cw.new_book()
            prev_book = book
        rec["R_spell"].append(cw.R)
        form = cw.emerge()
        out.append(f"{form} {text}")                       # step (3)
        rec["form"].append(FORMS.index(form))
        rec["charge"].append(cw.charge)
        rec["W"].append(cw.W)
        cw.read(text, int(c))
        rec["R_after"].append(cw.R)
        rec["at_cap_after"].append(cw.x is not None and abs(cw.x) >= CAP)
    return out, {k: np.array(v) for k, v in rec.items()}

# ---------------------------------------------------------------------------
# Manipulation check, spelling counts and trace (Bible markup only, no model)
# ---------------------------------------------------------------------------

def retention(form_idx, clear, books, L):
    """Share of verdicts whose sign the marker still shows L verses later (same book, no newer verdict)."""
    pos = form_idx - 2
    ok = n = 0
    for i in np.where(clear != 0)[0]:
        j = i + L
        if j >= len(books) or books[j] != books[i] or np.any(clear[i + 1:j] != 0):
            continue
        n += 1
        ok += np.sign(pos[j]) == clear[i]
    return 100 * ok / n if n else float("nan")


def manipulation(verses, marked, recs, current_forms, clear, pool):
    books = [b for b, _ in verses]
    n = len(verses)
    man = {}
    for name in NEW:
        f = recs[name]["form"]
        shares = 100 * np.bincount(f, minlength=5) / n
        cap_after = 100 * recs[name]["at_cap_after"].mean()
        cap_spell = 100 * np.mean(np.abs(recs[name]["R_spell"]) >= CAP)
        cap_pct = max(cap_after, cap_spell)
        passes = bool(cap_pct <= MAX_CAP_PCT and shares.min() >= MIN_SPELLING_PCT)
        train_counts = Counter(marked[name][i].split(" ", 1)[0] for i in pool)
        exp = JUDGE_EXPECTED[name]
        man[name] = {
            "CH": list(CONFIGS[name]), "passes": passes, "label": "ok" if passes else "degenerate",
            "shares_all_pct": shares.round(2).tolist(),
            "train_counts": {fm: train_counts[fm] for fm in FORMS},
            "cap_pct_after_reading": round(cap_after, 3), "cap_pct_spelled_from": round(cap_spell, 3),
            "cap_pct_checked": round(cap_pct, 3),
            "mean_abs_R": round(float(np.mean(np.abs(recs[name]["R_spell"]))), 2),
            "verdict_sign_kept_pct": {str(L): round(retention(f, clear, books, L), 1) for L in (1, 3, 5, 10)},
            "judge_sim_shares": exp["shares"], "judge_sim_cap": exp["cap"],
            "max_share_diff_vs_judge": round(float(np.max(np.abs(shares - np.array(exp["shares"])))), 3),
        }
    allf = {name: recs[name]["form"] for name in NEW}
    allf["shifting"] = current_forms
    differs = {a: {b: round(100 * float(np.mean(allf[a] != allf[b])), 1) for b in allf} for a in allf}
    cur = {"shares_all_pct": (100 * np.bincount(current_forms, minlength=5) / n).round(2).tolist(),
           "verdict_sign_kept_pct": {str(L): round(retention(current_forms, clear, books, L), 1)
                                     for L in (1, 3, 5, 10)}}
    return man, differs, cur


def trace(verses, recs, current_forms, clear, name, start=None, length=TRACE_LEN):
    if start is None:
        start = next(k for k, (b, t) in enumerate(verses) if b == TRACE_BOOK and t.startswith(TRACE_START))
    r = recs[name]
    lines = [f"  {name}  CH = {CONFIGS[name]}   ({verses[start][0]}, {length} verses in a row)",
             f"    {'#':>5s} {'R (spelled from)':>16s} {'spelling':9s} {'charge':>7s} {'W=R+charge':>10s} "
             f"{'clear?':6s} {'R left':>7s}  {'now':8s}  verse"]
    for i in range(start, start + length):
        c = {-1: "WRONG", 1: "RIGHT", 0: "-"}[int(clear[i])]
        ch = r["charge"][i]
        lines.append(f"    {i:5d} {r['R_spell'][i]:+16.1f} {FORMS[r['form'][i]]:9s} {ch:+7.1f} {r['W'][i]:+10.1f} "
                     f"{c:6s} {r['R_after'][i]:+7.1f}  {FORMS[current_forms[i]]:8s}  {verses[i][1][:58]}")
    lines.append("    (R left = the Remaining after the verse, which spells the NEXT verse's word; a clear choice "
                 "sets it to +/-17 and restarts the run; 'now' = the current shifting word)")
    return lines

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def get_model(name, seed, train_texts, steps, models_dir, train_ok=True):
    vocab = tt.Vocab(train_texts)
    path = models_dir / f"{name}_seed{seed}_steps{steps}.pt"
    model = tt.TinyGPT(len(vocab))
    if path.exists():
        model.load_state_dict(torch.load(path, map_location="cpu"))
        model.eval()
        log(f"  [{stamp()}] loaded {path.name}")
        return model, vocab, False
    if not train_ok:
        raise FileNotFoundError(path)
    torch.set_num_threads(THREADS["train"])
    log(f"\n== [{stamp()}] training {name} seed {seed} ({steps} steps, {len(train_texts):,} verses, "
        f"vocab {len(vocab):,})")
    t0 = time.time()
    model = tt.train(vocab, train_texts, steps, seed)
    models_dir.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    torch.save(model.state_dict(), tmp)
    os.replace(tmp, path)
    log(f"  [{stamp()}] saved {path}  ({time.time() - t0:.0f}s)")
    return model, vocab, True

# ---------------------------------------------------------------------------
# Measures (the unchanged code paths of experiments 10, 11 and 12)
# ---------------------------------------------------------------------------

def run_m1(model, vocab, n_v2, n_v1, plain=False):
    torch.set_num_threads(THREADS["M1"])
    scorer = confirm.score_baseline if plain else mc.score
    v1s, v1j = scorer(model, vocab, ITEMS_V1[:n_v1])
    v2s, v2j = scorer(model, vocab, ITEMS_V2[:n_v2])
    return {"v1_shift": v1s, "v1_judge": v1j, "v2_shift": v2s, "v2_judge": v2j}


def run_m2(model, vocab, values, version, n_pairs, plain=False):
    torch.set_num_threads(THREADS["M2"])
    assert lst.START_MARKER is False
    fillers = lst.neutral_fillers(values, vocab)
    judge = lst.judge_plain if plain else lst.judge_marked
    correct, n_pad = [], []
    for k in range(n_pairs):
        r, w, npad = lst.build_stories(version, fillers, vocab, k)
        jr, jw = judge(model, vocab, r), judge(model, vocab, w)
        correct.append(1.0 if jr > jw else 0.5 if np.isclose(jr, jw) else 0.0)
        n_pad.append(npad)
    return {"correct": correct, "fillers_used": len(fillers), "mean_pad": float(np.mean(n_pad))}


def run_m3(key, model, vocab, held_norm, H, markers, decode):
    torch.set_num_threads(THREADS["M3"])
    res = uc.code_one(key, uc.Neural(model), held_norm, vocab, markers, H, decode, log)
    res["vocab_size"] = len(vocab)
    res["threads"] = torch.get_num_threads()
    return res

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def gather(results, stored, seeds, n_m1, n_m2):
    """Per method: M1 array (seeds x pairs), M2 array (seeds x pairs) for B (and A, short), M3 per-verse mean."""
    M1, M2, M2A, M2S, M3, M3_seed0_exact, M3_bytes = {}, {}, {}, {}, {}, {}, {}
    M1_shift = {}
    for m in ALL:
        if m in CONFIGS:
            src1 = [results["M1"].get(f"{m}/seed{s}") for s in seeds]
            src2 = {v: [results["M2"].get(f"{m}/seed{s}/{v}") for s in seeds] for v in ("B", "A", "short")}
            src3 = [results["M3"].get(f"{m}/seed{s}") for s in seeds]
        else:
            src1 = [stored["M1"].get(f"{m}/seed{s}") for s in seeds]
            src2 = {v: [stored["M2"].get(f"{m}/seed{s}/{v}") for s in seeds] for v in ("B", "A", "short")}
            src3 = [stored["M3"].get(f"{m}/seed{s}") for s in seeds]
        if all(x is not None for x in src1):
            M1[m] = np.array([x["v2_judge"][:n_m1] for x in src1], float)
            M1_shift[m] = np.array([x["v2_shift"][:n_m1] for x in src1], float)
        for v, dst in (("B", M2), ("A", M2A), ("short", M2S)):
            if all(x is not None for x in src2[v]):
                dst[m] = np.array([x["correct"][:n_m2] for x in src2[v]], float)
        if all(x is not None for x in src3):
            M3[m] = np.mean([x["per_verse_total"] for x in src3], 0)
            M3_bytes[m] = [x["seed_bytes"] for x in src3]
            first = src3[0]
            M3_seed0_exact[m] = bool(first.get("exact")) if first.get("decoded") else None
    return {"M1": M1, "M1_shift": M1_shift, "M2": M2, "M2A": M2A, "M2S": M2S, "M3": M3,
            "M3_seed0_exact": M3_seed0_exact, "M3_bytes": M3_bytes}


def pair_test(a, b):
    """a, b: (seeds x pairs) score arrays. Sign test over pairs whose per-pair sums differ."""
    x, y = a.sum(0), b.sum(0)
    w, l = int((x > y).sum()), int((x < y).sum())
    return {"wins": w, "losses": l, "ties": int(len(x) - w - l), "p": p_at_least(w, w + l),
            "mean_pct_new": 100 * float(a.mean()), "mean_pct_comp": 100 * float(b.mean())}


def run_tests(data, man, dry):
    """All pre-registered tests, Holm within each family and measure."""
    tests = {}
    for measure in ("M1", "M2", "M3"):
        tests[measure] = {}
        for fam, rows in FAMILIES.items():
            recs = []
            for label, a, b in rows:
                r = {"label": label, "new": a, "comparator": b, "valid": True, "why_not": ""}
                if a not in data[measure] or b not in data[measure]:
                    r.update(valid=False, why_not="models missing")
                elif measure == "M3" and any(data["M3_seed0_exact"].get(c) is not True
                                             for c in (a, b) if c in CONFIGS):
                    r.update(valid=False, why_not="void: seed 0 did not regrow H exactly")
                if r["valid"] or r["why_not"] != "models missing":
                    if measure == "M3":
                        t = uc.compare(data["M3"][a], data["M3"][b])
                        r.update({"mean_diff_bits_per_verse": t["mean_diff_bits_per_verse"],
                                  "verses_smaller": t["verses_smaller"], "verses_larger": t["verses_larger"],
                                  "ties": t["ties"], "p": t["perm_p_one_sided"],
                                  "sign_p": t["sign_p_one_sided"], "perm_p_two_sided": t["perm_p_two_sided"]})
                    else:
                        r.update(pair_test(data[measure][a], data[measure][b]))
                degenerate = [c for c in (a, b) if c in man and not man[c]["passes"]]
                if degenerate:
                    r["degenerate"] = degenerate
                recs.append(r)
            # Holm: family size fixed as pre-registered; an invalid or degenerate test enters with p = 1
            p_for_holm = [r["p"] if (r["valid"] and not r.get("degenerate")) else 1.0 for r in recs]
            adj = holm(p_for_holm)
            for r, pa in zip(recs, adj):
                r["p_holm"] = pa
                r["pass"] = bool(r["valid"] and not r.get("degenerate") and pa < ALPHA)
            if measure == "M3":
                adj_s = holm([r["sign_p"] if (r["valid"] and not r.get("degenerate") and "sign_p" in r) else 1.0
                              for r in recs])
                for r, pa in zip(recs, adj_s):
                    r["sign_p_holm"] = pa
                    r["sign_pass"] = bool(r["valid"] and not r.get("degenerate") and pa < ALPHA)
                    r["tests_disagree"] = r["sign_pass"] != r["pass"]
            tests[measure][fam] = recs
    return tests


def find(tests, measure, fam, label_start):
    return next(r for r in tests[measure][fam] if r["label"].startswith(label_start))


def verdicts(tests):
    def status(fn):
        on = {m: fn(m) for m in ("M1", "M2", "M3")}
        if on["M1"]:
            s = "SHOWN on the primary measure M1"
            extra = [m for m in ("M2", "M3") if on[m]]
            if extra:
                s += " (also passes on " + ", ".join(extra) + ")"
        elif on["M2"] or on["M3"]:
            s = "secondary sign only (passes on " + ", ".join(m for m in ("M2", "M3") if on[m]) + \
                ", not on M1): not a confirmation"
        else:
            s = "not shown at this scale"
        return s, on

    out = {}
    out["The owner's numbers matter (N1)"] = status(lambda m: find(tests, m, "F3", "N1")["pass"])
    out["The sequence itself matters (N1, N2 and N3)"] = status(
        lambda m: all(find(tests, m, "F3", n)["pass"] for n in ("N1", "N2", "N3")))
    out["47 in the 17 slot helps (N4)"] = status(lambda m: find(tests, m, "F3", "N4")["pass"])
    s, on = status(lambda m: find(tests, m, "F1", "num_charge17")["pass"])
    r1 = {m: find(tests, m, "F4", "R1")["pass"] for m in ("M1", "M2", "M3")}
    if on["M1"]:
        s += ("; credited to the owner's recharge (R1 passes on M1)" if r1["M1"] else
              "; NOT credited to the recharge alone: R1 does not pass on M1, so the AI's drain may account for it")
    out["The owner's recharge rule helps (num_charge17 in F1; R1 decides the credit)"] = (s, on)
    s, on = status(lambda m: any(r["pass"] for r in tests[m]["F1"]))
    which = {m: [r["new"] for r in tests[m]["F1"] if r["pass"]] for m in ("M1", "M2", "M3")}
    if any(which.values()):
        s += "; configs passing F1: " + "; ".join(f"{m}: {', '.join(w)}" for m, w in which.items() if w)
    out["Useful for the project (any config passes F1)"] = (s, on)
    return {k: {"status": v[0], "passes": v[1], **({"R1": r1} if "recharge" in k else {})} for k, v in out.items()}

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def report(results, stored, seeds, n_m1, n_m2, dry):
    lines = []

    def out(s=""):
        lines.append(s)

    man = results["manipulation"]
    data = gather(results, stored, seeds, n_m1, n_m2)
    n_new_models = sum(f"{c}/seed{s}" in results["M1"] for c in NEW for s in seeds)
    complete = n_new_models == len(NEW) * len(seeds) and all(
        f"{c}/seed{s}" in results["M3"] and f"{c}/seed{s}/B" in results["M2"] for c in NEW for s in seeds)

    out("THE NUMBERS TEST: the owner's numbers 17, 32, 16, 34, 47 in the place of 17 in \"W1 = 17 + 4 Remaining\"")
    out("=" * 104)
    if dry:
        out("DRY RUN: 5 training steps, seed 0 only, small subsets. A machinery check; THE NUMBERS BELOW MEAN NOTHING.")
    if not complete:
        out(f"PROVISIONAL: {n_new_models} of {len(NEW) * len(seeds)} new models scored so far.")
    m = results["meta"]
    out(f"Frozen constants: RESET {RESET}, CAP {CAP}, NBAR {m['NBAR']:.4f}, DRAIN {m['DRAIN']:.6f}, "
        f"SCALE {sw.SCALE}, CLEAR_PCT {CLEAR_PCT}, spellings {', '.join(FORMS)}")
    out(f"Seeds {seeds}, {m['steps']} training steps. Script SHA-256 {m['script_sha256'][:16]}...")
    out()

    out("TABLE 0  MANIPULATION CHECK (Bible markup only, no model). Pass: <= 5% of verses at the +/-51 cap and")
    out(f"         every spelling on >= 3% of verses. Shares over all {m['n_verses']:,} verses; the judge's simulation"
        " below each row.")
    out(f"  {'config':13s} {'CH':22s} {'anoksha':>8s} {'oksharu':>8s} {'velanok':>8s} {'sharuvel':>8s} "
        f"{'ruvelan':>8s} {'at cap':>7s}  {'kept 1/3/5/10':14s} result")
    for c in NEW:
        r = man[c]
        sh = " ".join(f"{x:8.1f}" for x in r["shares_all_pct"])
        kept = "/".join(f"{r['verdict_sign_kept_pct'][str(L)]:.0f}" for L in (1, 3, 5, 10))
        out(f"  {c:13s} {str(tuple(r['CH'])):22s} {sh} {r['cap_pct_checked']:6.2f}%  {kept:14s} "
            f"{'PASS' if r['passes'] else 'FAIL -> degenerate (descriptive only)'}")
        out(f"  {'':13s} {'(judge sim)':22s} " + " ".join(f"{x:8.1f}" for x in r["judge_sim_shares"])
            + f" {r['judge_sim_cap']:6.2f}%   max share diff {r['max_share_diff_vs_judge']:.2f} points")
    cur = results["current_shifting"]
    out(f"  {'shifting now':13s} {'(RESET 17, SPEND 0.5)':22s} " + " ".join(f"{x:8.1f}" for x in cur["shares_all_pct"])
        + f" {'':7s}  " + "/".join(f"{cur['verdict_sign_kept_pct'][str(L)]:.0f}" for L in (1, 3, 5, 10)))
    out("  ('kept 1/3/5/10' = % of clear choices whose sign the word still shows 1, 3, 5 and 10 verses later)")
    out()
    d = results["differs_pct"]
    names = NEW + ["shifting"]
    out("  % of verses whose word differs between two rules:")
    out("  " + " " * 13 + "".join(f"{n.replace('num_', '')[:9]:>10s}" for n in names))
    for a in names:
        out(f"  {a.replace('num_', ''):13s}" + "".join(f"{d[a][b]:10.1f}" for b in names))
    out("  judge's figures for the same pairs: " + ", ".join(
        f"{a.replace('num_', '')} vs {b.replace('num_', '')} {v} (here {d[a][b]})" for (a, b), v in JUDGE_DIFFERS.items()))
    out()

    out("SPELLING COUNTS over the training Bible (the verses the models learn from)")
    for c in NEW:
        tc = man[c]["train_counts"]
        out(f"  {c:13s} " + "  ".join(f"{fm} {tc[fm]:,}" for fm in FORMS))
    out()
    out("TRACE: the rule at work, verse by verse")
    for c in NEW:
        lines.extend(results["traces"][c])
        out()

    # ---- M1 ----
    out("=" * 104)
    out(f"TABLE 1  M1 (PRIMARY): judging right vs wrong on {n_m1} new story pairs (50% = guessing)")
    out(f"  {'method':13s} {'correct per seed':18s} {'mean %':>7s} {'majority':>9s} {'p vs 50%':>9s}   "
        f"consequence per seed (descriptive)")
    for mth in ALL:
        if mth not in data["M1"]:
            out(f"  {mth:13s} (not scored yet)")
            continue
        J = data["M1"][mth]
        maj = int((J.sum(0) * 2 > len(seeds)).sum())
        tag = "" if mth in CONFIGS else "  [stored]"
        out(f"  {mth:13s} {', '.join(str(int(x)) for x in J.sum(1)):18s} {100 * J.mean():7.1f} {maj:>5d}/{n_m1:<3d} "
            f"{p_at_least(maj, n_m1):9.4f}   {', '.join(str(int(x)) for x in data['M1_shift'][mth].sum(1))}{tag}")
    out()

    # ---- M2 ----
    out(f"TABLE 2  M2: long stories, version B (the act pushed out of the 64-token view), {n_m2} pairs (50% = guessing)")
    out(f"  {'method':13s} {'B score per seed':22s} {'B mean %':>8s} {'ties':>6s}   "
        f"{'A mean % (descr.)':>17s} {'short mean % (descr.)':>21s}")
    for mth in ALL:
        if mth not in data["M2"]:
            out(f"  {mth:13s} (not scored yet)")
            continue
        B = data["M2"][mth]
        a = f"{100 * data['M2A'][mth].mean():17.1f}" if mth in data["M2A"] else f"{'-':>17s}"
        s = f"{100 * data['M2S'][mth].mean():21.1f}" if mth in data["M2S"] else f"{'-':>21s}"
        out(f"  {mth:13s} {', '.join(f'{x:.1f}' for x in B.sum(1)):22s} {100 * B.mean():8.1f} {int((B == 0.5).sum()):6d}   {a} {s}"
            + ("" if mth in CONFIGS else "  [stored]"))
    out()

    # ---- M3 ----
    nv = len(next(iter(data["M3"].values()))) if data["M3"] else 0
    out(f"TABLE 3  M3: exact-seed TOTAL bits per verse ({nv} verses; marker + words + verse end; lower = better)")
    out(f"  {'method':13s} {'mean bits/verse':>15s} {'vs baseline':>11s} {'seed bytes per seed':>28s}  seed 0 regrown exactly?")
    base = data["M3"].get("baseline")
    for mth in ALL:
        if mth not in data["M3"]:
            out(f"  {mth:13s} (not scored yet)")
            continue
        v = data["M3"][mth]
        vb = f"{100 * (v.mean() / base.mean() - 1):+10.2f}%" if base is not None else f"{'-':>11s}"
        ex = data["M3_seed0_exact"].get(mth)
        exs = "yes (decoded)" if ex else ("NO - M3 VOID" if ex is False else "not decoded")
        out(f"  {mth:13s} {v.mean():15.3f} {vb} {', '.join(f'{b:,}' for b in data['M3_bytes'][mth]):>28s}  {exs}"
            + ("" if mth in CONFIGS else "  [stored]"))
    other = [(k, r) for k, r in results["M3"].items() if r.get("decoded") and not r.get("exact")]
    if other:
        out("  DECODE MISMATCH on: " + ", ".join(k for k, _ in other))
    out()

    # ---- tests ----
    tests = run_tests(data, man, dry)
    out("=" * 104)
    out("TABLE 4  PRE-REGISTERED TESTS (one-sided, 'new is better'; Holm within each family and measure; pass = Holm p < 0.05)")
    fam_names = {"F1": "F1  each new config vs shifting", "F2": "F2  each new config vs baseline (on M2: vs chance)",
                 "F3": "F3  the owner's numbers", "F4": "F4  mechanism (single test)"}
    for measure in ("M1", "M2", "M3"):
        out(f"\n  {measure}" + {"M1": "  judging on story pairs (sign test over pairs)",
                                "M2": "  long stories, version B (sign test over pairs)",
                                "M3": "  TOTAL bits per verse (sign-flip permutation test; sign test alongside)"}[measure])
        for fam in FAMILIES:
            out(f"    {fam_names[fam]}")
            for r in tests[measure][fam]:
                if "p" not in r:
                    out(f"      {r['label']:34s} {r['why_not']}")
                    continue
                flag = "PASS" if r["pass"] else "-"
                if not r["valid"]:
                    flag = r["why_not"]
                elif r.get("degenerate"):
                    flag = "descriptive only (degenerate: " + ", ".join(r["degenerate"]) + ")"
                if measure == "M3":
                    dis = "  TESTS DISAGREE" if r.get("tests_disagree") else ""
                    out(f"      {r['label']:34s} mean diff {r['mean_diff_bits_per_verse']:+7.3f} bits/verse  "
                        f"smaller/larger {r['verses_smaller']:>3d}/{r['verses_larger']:<3d}  perm p {r['p']:.5f} "
                        f"(Holm {r['p_holm']:.4f})  sign p {r['sign_p']:.4f} (Holm {r['sign_p_holm']:.4f})  {flag}{dis}")
                else:
                    out(f"      {r['label']:34s} {r['mean_pct_new']:5.1f}% vs {r['mean_pct_comp']:5.1f}%  "
                        f"better on {r['wins']:>3d}, worse on {r['losses']:>3d}, tied {r['ties']:>3d}  "
                        f"p {r['p']:.4f} (Holm {r['p_holm']:.4f})  {flag}")
    out()

    # descriptive comparisons for the controls
    out("  Descriptive only (not part of any verdict): label, carry3 and scrambled vs shifting and vs baseline")
    for measure in ("M1", "M2", "M3"):
        for c in ("label", "carry3", "scrambled"):
            for b in ("shifting", "baseline"):
                if c not in data[measure] or b not in data[measure]:
                    continue
                if measure == "M3":
                    t = uc.compare(data["M3"][c], data["M3"][b])
                    out(f"    {measure} {c:9s} vs {b:8s}  mean diff {t['mean_diff_bits_per_verse']:+7.3f} bits/verse, "
                        f"perm p {t['perm_p_one_sided']:.5f}")
                else:
                    t = pair_test(data[measure][c], data[measure][b])
                    out(f"    {measure} {c:9s} vs {b:8s}  {t['mean_pct_new']:5.1f}% vs {t['mean_pct_comp']:5.1f}%, "
                        f"better on {t['wins']}, worse on {t['losses']}, p {t['p']:.4f}")
    out()

    # ---- verdicts ----
    v = verdicts(tests)
    out("=" * 104)
    out("PRE-REGISTERED VERDICTS (decided on M1; a pass on M2 or M3 alone is a 'secondary sign', never a confirmation;")
    out("every other outcome is 'not shown at this scale', never 'disproved')")
    if dry:
        out("  [DRY RUN: verdict machinery only; these verdicts mean nothing]")
    elif not complete:
        out("  [PROVISIONAL: not all 18 models are scored yet]")
    for k, r in v.items():
        out(f"  {k}:")
        out(f"      {r['status']}")
    out()
    out("  Expectation written before the run (not part of the verdict): ties with shifting on M1, as all marker")
    out("  methods have tied so far, and num_seq about equal to num_seqrev.")
    out()
    out("LIMITS: tiny model, 3 seeds, 100 pairs; only large effects can be detected. word_values were computed on all")
    out("verses, held-out ones included (kept as before for comparability; flagged for M3).")
    if results.get("repro"):
        out()
        out("CONTROL REPRODUCTION CHECK (the stored control scores are reused unchanged; this re-scores saved control")
        out("models with the same code paths to check the setup matches)")
        for k, r in results["repro"].items():
            out(f"  {k:28s} {'REPRODUCED EXACTLY' if r['identical'] else 'DIFFERS'}  {r.get('note', '')}")
    return lines, {"tests": tests, "verdicts": v, "complete": complete, "n_new_models_scored": n_new_models}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_stored(seeds, n_m1, n_m2):
    """Reused control scores, read-only and unchanged."""
    meth = json.loads(mc.OUT.read_text())
    longs = json.loads(lst.OUT.read_text())
    under = json.loads((HERE / "results_understanding.json").read_text())
    st = {"M1": {}, "M2": {}, "M3": {}}
    for m in CONTROLS:
        for s in seeds:
            if f"{m}/seed{s}" in meth:
                st["M1"][f"{m}/seed{s}"] = meth[f"{m}/seed{s}"]
            for v in ("B", "A", "short"):
                if f"{m}/seed{s}/{v}" in longs:
                    st["M2"][f"{m}/seed{s}/{v}"] = longs[f"{m}/seed{s}/{v}"]
            k = f"{'R6' if m == 'baseline' else 'R7'}_{m}_seed{s}"
            if k in under["rungs"]:
                st["M3"][f"{m}/seed{s}"] = under["rungs"][k]
    return st, under


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="5 steps, seed 0, small subsets, scratch folder only")
    ap.add_argument("--scratch", default=None, help="dry-run output folder")
    ap.add_argument("--report-only", action="store_true", help="rebuild tables from results_numbers.json")
    args = ap.parse_args()
    dry = args.dry_run
    T0 = time.time()

    if dry:
        base = Path(args.scratch or os.environ.get("NUMBERS_DRY_DIR") or tempfile.gettempdir()).resolve()
        repo = HERE.parent.resolve()
        if base == repo or repo in base.parents:
            raise SystemExit("the dry run must write outside the repository (use --scratch)")
        scratch = base / "numbers_test_dry"
        models_dir, out_json, out_txt = scratch / "models", scratch / "results_numbers_dry.json", \
            scratch / "results_numbers_dry.txt"
        # start fresh, removing only the files an earlier dry run made
        for f in [out_json, out_txt] + sorted(models_dir.glob("num_*_seed0_steps5.pt")):
            f.unlink(missing_ok=True)
        models_dir.mkdir(parents=True, exist_ok=True)
        seeds, steps, n_m1, n_v1, n_m2 = [0], 5, 8, 4, 4
    else:
        models_dir, out_json, out_txt = MODELS, OUT_JSON, OUT_TXT
        seeds, steps, n_m1, n_v1, n_m2 = SEEDS, STEPS, len(ITEMS_V2), len(ITEMS_V1), len(ITEMS_V2)

    log(f"[{stamp()}] numbers_test.py {'DRY RUN' if dry else 'FULL RUN'}  -> {out_json}")
    verses = load_verses()
    texts = [t for _, t in verses]
    pool = [i for i in range(len(texts)) if i % 50]
    held_idx = list(range(0, len(texts), 50))
    if dry:                                    # exp 12's --dev verses: TRAINING verses, no held-out verse touched
        held_idx = [i for i in range(1, len(texts), 50)][:40]
    held_norm = [uc.norm(texts[i]) for i in held_idx]
    H = "\n".join(held_norm)

    t0 = time.time()
    values = word_values(texts)
    log(f"[{stamp()}] word values: {len(values):,} words ({time.time() - t0:.0f}s)")
    nbar, drain = drain_constants(verses, values)
    assert round(nbar, 4) == NBAR_FROZEN, nbar
    assert round(drain, 6) == DRAIN_FROZEN, drain
    log(f"  NBAR = {nbar:.4f}, DRAIN = {drain:.6f} (frozen {NBAR_FROZEN}, {DRAIN_FROZEN}): OK")
    # neutral steady state of the plain rule: W = 21, R = 4
    R = 0.0
    for _ in range(60):
        W = R + 17
        R = W * (1 - drain) ** nbar
    log(f"  neutral text, plain rule: settles at W = {W:.3f}, Remaining = {R:.3f} (the owner's 17 + 4)")

    clear, _ = clear_choices(verses, values)
    marked, recs = {}, {}
    for c, CH in CONFIGS.items():
        marked[c], recs[c] = mark_charge(verses, values, CH, drain, clear)
    current, n_clear_sw = sw.mark_up(verses, values)
    current_forms = np.array([FORMS.index(x.split(" ", 1)[0]) for x in current])
    assert int((clear != 0).sum()) == n_clear_sw            # the same clear choices as sw.mark_up

    frozen = {"RESET": RESET, "CAP": CAP, "NBAR": NBAR_FROZEN, "DRAIN": DRAIN_FROZEN, "CONFIGS": CONFIGS,
              "SCALE": sw.SCALE, "CLEAR_PCT": CLEAR_PCT, "FORMS": FORMS, "steps": steps, "seeds": seeds,
              "values_sha256": sha(json.dumps(values, sort_keys=True).encode()),
              "marked_sha256": {c: sha("\n".join(marked[c]).encode()) for c in CONFIGS},
              "H_sha256": sha(H.encode()), "n_m1": n_m1, "n_m2": n_m2}
    frozen = json.loads(json.dumps(frozen, default=_jsonable))
    results = json.loads(out_json.read_text()) if out_json.exists() else {}
    if results and results["meta"]["frozen"] != frozen:
        raise SystemExit(f"{out_json} was made with different frozen settings; refusing to mix results")
    script_sha = sha(Path(__file__).read_bytes())
    results.setdefault("meta", {}).update(
        frozen=frozen, NBAR=nbar, DRAIN=drain, steps=steps, seeds=seeds, dry_run=dry,
        script_sha256=script_sha, n_clear=int((clear != 0).sum()), held_verse_index=held_idx,
        n_verses=len(verses),
        torch=torch.__version__, numpy=np.__version__, python=sys.version.split()[0], threads=THREADS)
    results["meta"].setdefault("started_utc", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    for k in ("M1", "M2", "M3", "repro", "timings_s"):
        results.setdefault(k, {})

    def save():
        atomic_write(out_json, json.dumps(results, default=_jsonable))

    # ---- manipulation check, spelling counts, traces ----
    man, differs, cur = manipulation(verses, marked, recs, current_forms, clear, pool)
    results["manipulation"], results["differs_pct"], results["current_shifting"] = man, differs, cur
    results["traces"] = {c: trace(verses, recs, current_forms, clear, c) for c in NEW}
    results["meta"]["clear_choices"] = int((clear != 0).sum())
    save()
    log(f"\n[{stamp()}] MANIPULATION CHECK ({int((clear != 0).sum()):,} clear choices of {len(verses):,} verses)")
    for c in NEW:
        r = man[c]
        log(f"  {c:13s} shares {' '.join(f'{x:5.1f}' for x in r['shares_all_pct'])}  at cap {r['cap_pct_checked']:.2f}%  "
            f"-> {'PASS' if r['passes'] else 'FAIL (degenerate)'}   (judge sim max diff {r['max_share_diff_vs_judge']:.2f} pts)")
        log(f"  {'':13s} training Bible: " + ", ".join(f"{fm} {r['train_counts'][fm]:,}" for fm in FORMS))
    log()
    for c in NEW:
        for line in results["traces"][c]:
            log(line)
        log()

    stored, under = load_stored(seeds, n_m1, n_m2)

    if args.report_only:
        lines, ana = report(results, stored, seeds, n_m1, n_m2, dry)
        results["analysis"] = ana
        save()
        atomic_write(out_txt, "\n".join(lines) + "\n")
        print("\n".join(lines))
        return

    # ---- control reproduction check (extra) ----
    def repro(key, fn, stored_val, note=""):
        if key in results["repro"]:
            return
        t = time.time()
        got = fn()
        results["repro"][key] = {"identical": got == stored_val, "note": note, "seconds": round(time.time() - t, 1)}
        save()
        log(f"  [{stamp()}] repro {key}: {'REPRODUCED EXACTLY' if got == stored_val else 'DIFFERS'} "
            f"({time.time() - t:.0f}s) {note}")

    log(f"[{stamp()}] CONTROL REPRODUCTION CHECK")
    ctrl = {}
    for m in ("shifting", "baseline"):
        corpus = lst.marked_corpus(m, verses, values, 0)
        ctrl[m] = get_model(m, 0, [corpus[i] for i in pool], STEPS, MODELS, train_ok=False)[:2]
    sm, sv = ctrl["shifting"]
    bm, bv = ctrl["baseline"]
    repro("M1/shifting/seed0", lambda: run_m1(sm, sv, n_m1, 0)["v2_judge"],
          stored["M1"]["shifting/seed0"]["v2_judge"][:n_m1], "method_comparison.score vs stored v2_judge")
    repro("M1/baseline/seed0", lambda: run_m1(bm, bv, n_m1, 0, plain=True)["v2_judge"],
          stored["M1"]["baseline/seed0"]["v2_judge"][:n_m1], "confirm.score_baseline vs stored v2_judge")
    repro("M2/shifting/seed0/B", lambda: run_m2(sm, sv, values, "B", n_m2)["correct"],
          stored["M2"]["shifting/seed0/B"]["correct"][:n_m2], "judge_marked, version B")
    if not dry:
        shifting_marked = lst.marked_corpus("shifting", verses, values, 0)
        repro("M3/shifting/seed0", lambda: run_m3("repro_shifting_seed0", sm, sv, held_norm, H,
                                                  [shifting_marked[i].split(" ", 1)[0] for i in held_idx],
                                                  False)["per_verse_total"],
              stored["M3"]["shifting/seed0"]["per_verse_total"], "per-verse TOTAL bits, 2 threads")
    else:
        # dev verses are not the stored held-out verses: compute the M3 comparators fresh (encode only)
        stored["M3"] = {}
        for m, (mod, voc) in ctrl.items():
            corpus = lst.marked_corpus(m, verses, values, 0)
            mk = None if m == "baseline" else [corpus[i].split(" ", 1)[0] for i in held_idx]
            stored["M3"][f"{m}/seed0"] = run_m3(f"dry_{m}_seed0", mod, voc, held_norm, H, mk, False)
    del ctrl, sm, bm
    log()

    # ---- the 18 new models: train if needed, then M1, M2, M3 ----
    for s in seeds:
        for c in NEW:
            k1 = k3 = f"{c}/seed{s}"
            todo_m2 = [v for v in ("B", "A", "short") if f"{c}/seed{s}/{v}" not in results["M2"]]
            if k1 in results["M1"] and not todo_m2 and k3 in results["M3"]:
                log(f"[{stamp()}] {c} seed {s}: already scored")
                continue
            train_texts = [marked[c][i] for i in pool]
            t = time.time()
            model, vocab, trained = get_model(c, s, train_texts, steps, models_dir)
            if trained:
                results["timings_s"][f"train/{c}/seed{s}"] = round(time.time() - t, 1)
            assert all(fm in vocab.stoi for fm in FORMS), "a spelling is missing from the vocabulary"
            if k1 not in results["M1"]:
                t = time.time()
                results["M1"][k1] = run_m1(model, vocab, n_m1, n_v1)
                results["timings_s"][f"M1/{c}/seed{s}"] = round(time.time() - t, 1)
                save()
                r = results["M1"][k1]
                log(f"  [{stamp()}] M1 {k1}: judge {sum(r['v2_judge'])}/{n_m1}, consequence "
                    f"{sum(r['v2_shift'])}/{n_m1}  ({time.time() - t:.0f}s)")
            for v in todo_m2:
                t = time.time()
                results["M2"][f"{c}/seed{s}/{v}"] = run_m2(model, vocab, values, v, n_m2)
                results["timings_s"][f"M2/{c}/seed{s}/{v}"] = round(time.time() - t, 1)
                save()
                r = results["M2"][f"{c}/seed{s}/{v}"]
                log(f"  [{stamp()}] M2 {c}/seed{s}/{v}: score {sum(r['correct']):.1f}/{n_m2}, ties "
                    f"{sum(x == 0.5 for x in r['correct'])}  ({time.time() - t:.0f}s)")
            if k3 not in results["M3"]:
                t = time.time()
                mk = [marked[c][i].split(" ", 1)[0] for i in held_idx]
                res = run_m3(f"{c}_seed{s}", model, vocab, held_norm, H, mk, decode=True)
                results["M3"][k3] = res
                results["timings_s"][f"M3/{c}/seed{s}"] = round(time.time() - t, 1)
                save()
                if not res["exact"]:
                    log(f"  !!! {c} seed {s}: the decoded text does NOT match H"
                        + (" -> M3 VOID for this config" if s == 0 else " (seed 0 decides validity)"))
            del model

    lines, ana = report(results, stored, seeds, n_m1, n_m2, dry)
    results["analysis"] = ana
    results["meta"]["runtime_s_this_session"] = round(time.time() - T0, 1)
    results["meta"]["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    save()
    atomic_write(out_txt, "\n".join(lines) + "\n")
    log("\n".join(lines))
    log(f"\n[{stamp()}] done in {(time.time() - T0) / 60:.1f} minutes. Wrote {out_json} and {out_txt}")


if __name__ == "__main__":
    main()
