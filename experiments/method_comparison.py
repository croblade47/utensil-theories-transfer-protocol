"""
Method comparison: the shifting word vs the closest established method
=====================================================================

Same tiny transformer, same Bible, same 1,500 training steps, same 100 new
test story pairs (stories_v2.py). Only the way the training text is marked
changes. Each method is trained with 3 seeds.

Methods
  baseline     plain Bible, no marker                         (from confirm.py)
  scrambled    marker word with random spelling (control)     (from confirm.py)
  shifting     the owner's shifting word: a carried balance,
               reset to +/-17 on clear right/wrong, spent by
               following words, 5 spellings                   (from confirm.py)
  label        PLAIN GOOD/BAD LABEL, the established approach
               (like conditional training with good/bad tokens):
               same 5 spellings, same position, but each one
               judges ONLY the verse right before it. No carry,
               no reset, no fading. Uses the same verdict phrases
               ("did evil in the sight of the Lord" ...) and the
               same word values. Cut-offs chosen so each spelling
               appears about as often as in "shifting".
  carry3       carried balance like "shifting" but only 3
               spellings (wrong / unresolved / right): tests
               whether the graded spelling matters.

PRE-REGISTERED (committed before label/carry3 were trained)
  Main measure: JUDGING right vs wrong on the 100 new pairs (the measure where
  the shifting word showed signal; it is the same score for every method).
  Q1  shifting vs label:  per pair, count correct runs (0-3) for each;
      one-sided sign test over pairs where counts differ.  p < 0.05 = shifting
      beats the established method.
  Q2  shifting vs carry3: same test.  p < 0.05 = graded spelling helps.
  Also reported: each method vs chance (majority vote, sign test) and the
  consequence ("shift") score. No method was tuned on stories_v2.

Run:  python experiments/method_comparison.py   (about 66 minutes; reuses saved models)
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path

import numpy as np
import torch

import confirm
import shifting_word as sw
import tiny_transformer as tt
from bible_understanding import load_verses, tokens
from consequences_test import ITEMS as ITEMS_V1
from stories_v2 import ITEMS_V2

HERE = Path(__file__).parent
OUT = HERE / "results_methods.json"
SEEDS = [0, 1, 2]
STEPS = 1500
NEW = ["label", "carry3"]
ALL = ["baseline", "scrambled", "shifting", "label", "carry3"]


def p_at_least(k, n):
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else 1.0


def mark_label(verses, values):
    """Each verse is preceded by a spelling that judges ONLY the verse before it."""
    shifting, _ = sw.mark_up(verses, values)
    share = np.array([sum(m.split(" ", 1)[0] == f for m in shifting) for f in sw.FORMS], float)
    cuts = np.cumsum(share / share.sum())[:-1]          # same frequency of each spelling
    scores = np.array([sum(values.get(w, 0) for w in tokens(t)) for _, t in verses], float)
    edges = np.quantile(scores, cuts)
    out, prev_book = [], None
    for k, (book, text) in enumerate(verses):
        if book != prev_book or k == 0:
            form = sw.FORMS[2]                            # unresolved at the start of a book
            prev_book = book
        else:
            prev = verses[k - 1][1]
            if sw.CLEAR_WRONG.search(prev):          # same verdict phrases the shifting word uses
                form = sw.FORMS[0]
            elif sw.CLEAR_RIGHT.search(prev):
                form = sw.FORMS[4]
            else:
                form = sw.FORMS[int(np.searchsorted(edges, scores[k - 1], side="right"))]
        out.append(f"{form} {text}")
    return out


def mark_carry3(verses, values):
    """Same carried balance as the shifting word, but only three spellings."""
    shifting, _ = sw.mark_up(verses, values)
    three = {sw.FORMS[0]: sw.FORMS[0], sw.FORMS[1]: sw.FORMS[0], sw.FORMS[2]: sw.FORMS[2],
             sw.FORMS[3]: sw.FORMS[4], sw.FORMS[4]: sw.FORMS[4]}
    return [three[m.split(" ", 1)[0]] + " " + m.split(" ", 1)[1] for m in shifting]


def main():
    verses = load_verses()
    texts = [t for _, t in verses]
    values = sw.word_values(texts)
    pool = [i for i in range(len(texts)) if i % 50]
    res = json.loads(OUT.read_text()) if OUT.exists() else {}

    # Existing methods: copy their per-pair scores from the confirmation run.
    conf = json.loads(confirm.OUT.read_text())
    for m in ("baseline", "scrambled", "shifting"):
        for s in SEEDS:
            k = f"{m}/seed{s}"
            if k in conf:
                res[k] = conf[k]

    marked = {"label": mark_label(verses, values), "carry3": mark_carry3(verses, values)}
    for m in NEW:
        dist = {f: sum(x.split(" ", 1)[0] == f for x in marked[m]) for f in sw.FORMS}
        print(f"{m} spelling counts: {dist}")

    for s in SEEDS:
        for m in NEW:
            key = f"{m}/seed{s}"
            if key in res:
                continue
            train_texts = [marked[m][i] for i in pool]
            vocab = tt.Vocab(train_texts)
            path = confirm.MODELS / f"{m}_seed{s}_steps{STEPS}.pt"
            model = tt.TinyGPT(len(vocab))
            if path.exists():
                model.load_state_dict(torch.load(path))
                model.eval()
            else:
                print(f"\n== training {m} seed {s}", flush=True)
                model = tt.train(vocab, train_texts, STEPS, s)
                confirm.MODELS.mkdir(exist_ok=True)
                torch.save(model.state_dict(), path)
            v1s, v1j = confirm.score_word_model(model, vocab, ITEMS_V1)
            v2s, v2j = confirm.score_word_model(model, vocab, ITEMS_V2)
            res[key] = {"v1_shift": v1s, "v1_judge": v1j, "v2_shift": v2s, "v2_judge": v2j}
            OUT.write_text(json.dumps(res))
            print(f"  {key}: judge {sum(v2j)}/100, consequence {sum(v2s)}/100", flush=True)

    report(res)


def report(res):
    n = len(ITEMS_V2)
    counts = {}
    print("\n" + "=" * 72)
    print("METHOD COMPARISON on 100 new story pairs (50% = guessing)")
    print("=" * 72)
    print(f"  {'method':10s} {'judging, per run':20s} {'avg':>5s} {'majority':>9s} {'p':>8s}   consequence per run")
    for m in ALL:
        runs = [res[f"{m}/seed{s}"] for s in SEEDS if f"{m}/seed{s}" in res]
        if not runs:
            continue
        J = np.array([r["v2_judge"] for r in runs])
        S = np.array([r["v2_shift"] for r in runs])
        counts[m] = J.sum(0)
        maj = int((J.sum(0) * 2 > len(runs)).sum())
        print(f"  {m:10s} {', '.join(str(int(x)) for x in J.sum(1)):20s} {J.mean() * 100:5.1f} "
              f"{maj:>6d}/{n} {p_at_least(maj, n):8.4f}   {', '.join(str(int(x)) for x in S.sum(1))}")

    def vs(a, b, label):
        if a not in counts or b not in counts:
            return
        w, l = int((counts[a] > counts[b]).sum()), int((counts[a] < counts[b]).sum())
        p = p_at_least(w, w + l)
        print(f"  {label}: {a} better on {w} pairs, worse on {l}  (p = {p:.4f})  "
              f"-> {'CONFIRMED' if p < 0.05 else 'NOT CONFIRMED'}")

    print("\n  PRE-REGISTERED")
    vs("shifting", "label", "Q1 shifting beats plain good/bad label")
    vs("shifting", "carry3", "Q2 graded spelling beats 3 spellings ")
    print("\n  Descriptive")
    vs("shifting", "baseline", "   shifting vs no marker            ")
    vs("shifting", "scrambled", "   shifting vs scrambled            ")
    vs("label", "baseline", "   plain label vs no marker         ")


if __name__ == "__main__":
    main()
