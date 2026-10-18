"""
Confirmation run for experiment 7 (the shifting word)
=====================================================

Pre-registered (committed before any model saw stories_v2.py):

  Models: three conditions x three training seeds (0, 1, 2), 1,500 steps each.
    baseline    - plain Bible, no shifting word        (tiny_transformer.py)
    shifting    - Bible marked up with the shifting word (shifting_word.py)
    scrambled   - same marked-up Bible, spelling chosen at random

  Test: the 100 NEW story pairs in stories_v2.py. Score per pair = the shift
  test (does the model lean more toward the fortunate ending after the right
  act than after the wrong act?). The old 20 pairs are re-scored too, as a
  reproducibility check.

  PRIMARY  (confirmed if p < 0.05):
    For each new pair, take the majority vote of the 3 shifting-word models.
    The share of pairs where the majority is right must beat 50%
    (one-sided sign test over the 100 pairs).

  SECONDARY (confirmed if p < 0.05):
    Shifting beats scrambled on the same pairs. Per pair, count correct runs
    (0-3) for each; sign test over pairs where the counts differ.

  Anything else reported is descriptive only.

Run:  python experiments/confirm.py          (about 1.5-2 hours on 4 CPU cores)
Trained models are saved to experiments/models/ (not committed) and re-used.
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path

import numpy as np
import torch

import shifting_word as sw
import tiny_transformer as tt
from bible_understanding import load_verses
from consequences_test import ITEMS as ITEMS_V1
from stories_v2 import ITEMS_V2

HERE = Path(__file__).parent
MODELS = HERE / "models"
OUT = HERE / "results_confirm.json"
SEEDS = [0, 1, 2]
STEPS = 1500
CONDITIONS = ["shifting", "scrambled", "baseline"]


def p_at_least(k, n):
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else 1.0

# ---------------------------------------------------------------------------
# Per-pair scoring (same logic as the original scripts, but returns each pair)
# ---------------------------------------------------------------------------

def score_word_model(model, vocab, items):
    """Model writes its own shifting word after the story, then endings are compared."""
    form_ids = [vocab.stoi[f] for f in sw.FORMS]
    shift, judge = [], []
    for right, wrong, fortunate, ruinous in items:
        ef, er = vocab.encode(fortunate), vocab.encode(ruinous)
        d, lean = {}, {}
        for name, story in (("right", right), ("wrong", wrong)):
            ctx = [1] + vocab.encode(story) + [1]
            scores = [sw.lp_ids(model, ctx, [f]) for f in form_ids]
            probs = np.exp(np.array(scores) - max(scores))
            probs /= probs.sum()
            lean[name] = float(probs @ np.arange(-2, 3))
            own = form_ids[int(np.argmax(scores))]
            d[name] = sw.lp_ids(model, ctx + [own], ef) - sw.lp_ids(model, ctx + [own], er)
        shift.append(bool(d["right"] > d["wrong"]))
        judge.append(bool(lean["right"] > lean["wrong"]))
    return shift, judge


def score_baseline(model, vocab, items):
    shift, judge = [], []
    for right, wrong, fortunate, ruinous in items:
        d = {n: tt.logp(model, vocab, s + tt.JOIN, fortunate) - tt.logp(model, vocab, s + tt.JOIN, ruinous)
             for n, s in (("right", right), ("wrong", wrong))}
        j = {n: tt.logp(model, vocab, s + tt.JOIN, tt.JUDGE_EVIL) - tt.logp(model, vocab, s + tt.JOIN, tt.JUDGE_RIGHT)
             for n, s in (("right", right), ("wrong", wrong))}
        shift.append(bool(d["right"] > d["wrong"]))
        judge.append(bool(j["wrong"] > j["right"]))
    return shift, judge

# ---------------------------------------------------------------------------

def training_texts(cond, seed, verses, values, pool):
    texts = [t for _, t in verses]
    if cond == "baseline":
        return [texts[i] for i in pool]
    marked, _ = sw.mark_up(verses, values, None if cond == "shifting" else seed)
    return [marked[i] for i in pool]


def get_model(cond, seed, train_texts):
    vocab = tt.Vocab(train_texts)
    path = MODELS / f"{cond}_seed{seed}_steps{STEPS}.pt"
    model = tt.TinyGPT(len(vocab))
    if path.exists():
        model.load_state_dict(torch.load(path))
        model.eval()
        print(f"  loaded {path.name}", flush=True)
    else:
        print(f"\n== training {cond} seed {seed}", flush=True)
        model = tt.train(vocab, train_texts, STEPS, seed)
        MODELS.mkdir(exist_ok=True)
        torch.save(model.state_dict(), path)
    return model, vocab


def analyse(results):
    print("\n" + "=" * 72)
    print("RESULTS on the 100 new story pairs (50% = guessing)")
    print("=" * 72)
    n = len(ITEMS_V2)
    per = {}
    for cond in CONDITIONS:
        runs = [results[f"{cond}/seed{s}"] for s in SEEDS if f"{cond}/seed{s}" in results]
        if not runs:
            continue
        shift = np.array([r["v2_shift"] for r in runs])
        judge = np.array([r["v2_judge"] for r in runs])
        per[cond] = shift.sum(0)
        each = ", ".join(f"{int(x.sum())}/{n}" for x in shift)
        majority = int((shift.sum(0) * 2 > len(runs)).sum())
        print(f"  {cond:9s} shift per run: {each}   majority vote: {majority}/{n} "
              f"(p = {p_at_least(majority, n):.4f})")
        print(f"  {'':9s} judge per run: " + ", ".join(f"{int(x.sum())}/{n}" for x in judge))
        old = ", ".join(f"{sum(r['v1_shift'])}/20" for r in runs)
        print(f"  {'':9s} old 20 pairs, shift per run: {old}")

    if len(per.get("shifting", [])) and len(per.get("scrambled", [])):
        a, b = per["shifting"], per["scrambled"]
        wins, losses = int((a > b).sum()), int((a < b).sum())
        print(f"\n  Shifting vs scrambled, pair by pair: shifting better on {wins}, "
              f"worse on {losses}, tied on {n - wins - losses} "
              f"(p = {p_at_least(wins, wins + losses):.4f})")

    runs = [results[f"shifting/seed{s}"] for s in SEEDS if f"shifting/seed{s}" in results]
    if len(runs) == len(SEEDS):
        maj = int((np.array([r["v2_shift"] for r in runs]).sum(0) * 2 > len(SEEDS)).sum())
        p1 = p_at_least(maj, n)
        p2 = p_at_least(wins, wins + losses) if "scrambled" in per else float("nan")
        print("\n  PRE-REGISTERED VERDICT")
        print(f"    Primary   (shifting beats 50%):       {'CONFIRMED' if p1 < 0.05 else 'NOT CONFIRMED'}  (p = {p1:.4f})")
        print(f"    Secondary (shifting beats scrambled): {'CONFIRMED' if p2 < 0.05 else 'NOT CONFIRMED'}  (p = {p2:.4f})")


def main():
    verses = load_verses()
    texts = [t for _, t in verses]
    values = sw.word_values(texts)
    pool = [i for i in range(len(texts)) if i % 50]
    results = json.loads(OUT.read_text()) if OUT.exists() else {}

    for seed in SEEDS:
        for cond in CONDITIONS:
            key = f"{cond}/seed{seed}"
            if key in results:
                continue
            train_texts = training_texts(cond, seed, verses, values, pool)
            model, vocab = get_model(cond, seed, train_texts)
            scorer = score_baseline if cond == "baseline" else score_word_model
            v1s, v1j = scorer(model, vocab, ITEMS_V1)
            v2s, v2j = scorer(model, vocab, ITEMS_V2)
            results[key] = {"v1_shift": v1s, "v1_judge": v1j, "v2_shift": v2s, "v2_judge": v2j}
            OUT.write_text(json.dumps(results))
            print(f"  {key}: new pairs shift {sum(v2s)}/100, judge {sum(v2j)}/100 | "
                  f"old pairs shift {sum(v1s)}/20", flush=True)

    analyse(results)


if __name__ == "__main__":
    main()
