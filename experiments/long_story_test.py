"""
Long-story test: does the CARRIED balance matter once the act is out of sight?
=============================================================================

Experiment 10 found the owner's shifting word ties a plain per-verse good/bad
label on one-sentence stories. But the owner's idea is about carrying weight
FORWARD ("+4 remaining" into the next use). One-sentence stories never need
that. Here the decisive act comes first, then neutral sentences follow until
the act has scrolled out of the model's 64-token window. Only a marker that
carries state from one sentence to the next can still remember it.

Uses the 15 models already trained (no new training): baseline, scrambled,
shifting, label, carry3 x seeds 0-2.

Story layout, same filler for the right and wrong version of each pair:
  [act sentence] [neutral filler] [neutral filler] ... -> judgment
Marked models write their own marker word after every sentence (greedy), so a
carrying model can pass the judgment forward through its own markers. The
judgment is the lean of the final marker (wrong ... right). The baseline (no
marker) is judged with "and this was evil / right in the sight of the lord".

Two versions:
  A  verdict carried: the act ends with the Bible's own verdict ("and he did
     evil in the sight of the lord" / "and he did that which was right in the
     sight of the lord"). This triggers the owner's +/-17 reset.
  B  act carried: the act alone, which the owner's rule treats as not clear.
Filler is added until the act sentence AND the first marker written after it lie
entirely outside the final window (checked for every story). (Correction made
during the first run: v1 only pushed the act out of view, so the first marker,
which directly judges the act, was still visible and nothing had to be carried.
v1 results are kept aside, not used.) A "short" version (no filler) is also scored as a
sanity reference.

PRE-REGISTERED (committed before scoring)
  Score per story pair: 1 if judged right, 0 if wrong, 0.5 on an exact tie.
  (Correction made after the first model's result: ties had been counted as
  wrong. A model that can no longer tell the two stories apart produces exact
  ties, and it should score chance, not zero. This change can only help the
  methods that don't carry.)
  Summing those scores over the 3 seeds per pair; one-sided sign test over
  pairs where the sums differ.
  L1  version A: shifting beats label, p < 0.05
  L2  version B: shifting beats label, p < 0.05
  L3  version A: carry3 beats label, p < 0.05 (secondary)
  Also reported: every method vs 50% (majority vote), and the short version.

EXPLORATORY (added after seeing the pre-registered run; not part of the verdict)
  --start-marker: begin every marked story with the neutral marker "velanok",
  as every verse in training is preceded by a marker. A diagnostic showed the
  shifting word copies its marker perfectly down the story but misjudges the first
  sentence when no marker comes before it. Results go to
  results_long_story_startmarker.json.

Run:  python experiments/long_story_test.py [--start-marker]   (15-30 minutes, CPU only, no training)
"""

from __future__ import annotations

import json
import random
from math import comb
from pathlib import Path

import numpy as np
import torch

import confirm
import method_comparison as mc
import shifting_word as sw
import tiny_transformer as tt
from bible_understanding import load_verses, tokens
from consequences_test import BANNED
from stories_v2 import ITEMS_V2

torch.set_num_threads(1)            # share the CPU politely with any training job
HERE = Path(__file__).parent
OUT = HERE / "results_long_story.json"
START_MARKER = False
SEEDS = [0, 1, 2]
METHODS = ["baseline", "scrambled", "shifting", "label", "carry3"]
VERDICT_WRONG = "and he did evil in the sight of the lord"
VERDICT_RIGHT = "and he did that which was right in the sight of the lord"
MAX_FILLERS = 10

FILLER_POOL = [
    "and it came to pass on the morrow, that they went forth into the field",
    "and the sun went down, and they lodged there that night",
    "and in the morning they rose up early, and went on their way",
    "and they came unto the well, and drew water, and gave the camels to drink",
    "and the men sat down by the gate of the city until the evening",
    "and the days of the harvest were come, and the people went out to the fields",
    "and they journeyed from that place, and pitched their tents by the river",
    "and it was told the elders of the city, and they came out to see",
    "and the rain fell upon the mountains, and the waters ran down into the valley",
    "and the shepherds brought the flocks home at the going down of the sun",
    "and the road went down from the hills toward the sea",
    "and the next day they numbered the sheep and counted the oxen",
    "and the servants made ready the asses for the journey",
    "and the wind blew from the west, and the clouds passed over",
    "and they came to a place where there were twelve wells of water and seventy palm trees",
    "and they took bread and fish, and sat down upon the grass",
    "and the merchants came with their camels bearing spices",
    "and the city had four gates, on every side one gate",
    "and the ship went over to the other side of the sea",
    "and they builded houses of stone and of cedar wood",
    "and the candle was lighted, and they sat at meat together",
    "and the oxen were yoked, and the ground was tilled",
    "and the watchman stood upon the tower and looked toward the hills",
    "and the moon rose over the hills, and the night was still",
    "and after many days they came again to their own country",
    "and they went down to the brook, and the brook was full",
    "and the women ground the corn at the mill in the morning",
    "and the camels kneeled down without the city by the well",
]


def p_at_least(k, n):
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n if n else 1.0


def marked_corpus(method, verses, values, seed):
    if method == "baseline":
        return [t for _, t in verses]
    if method == "shifting":
        return sw.mark_up(verses, values)[0]
    if method == "scrambled":
        return sw.mark_up(verses, values, seed)[0]
    if method == "label":
        return mc.mark_label(verses, values)
    return mc.mark_carry3(verses, values)


def load_model(method, seed, train_texts):
    vocab = tt.Vocab(train_texts)
    name = {"baseline": "baseline", "scrambled": "scrambled", "shifting": "shifting",
            "label": "label", "carry3": "carry3"}[method]
    model = tt.TinyGPT(len(vocab))
    model.load_state_dict(torch.load(confirm.MODELS / f"{name}_seed{seed}_steps1500.pt"))
    model.eval()
    return model, vocab


def neutral_fillers(values, vocab):
    """Keep filler sentences that the owner's rule sees as neutral and the model knows every word of."""
    keep = []
    for f in FILLER_POOL:
        ws = tokens(f)
        if (abs(sum(values.get(w, 0) for w in ws)) <= 2 and max(abs(values.get(w, 0)) for w in ws) <= 3
                and not (BANNED & set(ws)) and not sw.CLEAR_WRONG.search(f) and not sw.CLEAR_RIGHT.search(f)
                and all(t in vocab.stoi for t in tt.tok(f))):
            keep.append(f)
    return keep


def build_stories(version, fillers, vocab, k_pair):
    """Right/wrong story pair as lists of sentences, padded with the same fillers until the act is out of view."""
    right, wrong = ITEMS_V2[k_pair][0], ITEMS_V2[k_pair][1]
    if version == "A":
        right, wrong = f"{right}, {VERDICT_RIGHT}", f"{wrong}, {VERDICT_WRONG}"
    if version == "short":
        return [right], [wrong], 0
    rng = random.Random(1000 + k_pair)
    pad = []
    while True:
        pad.append(rng.choice(fillers))
        # tokens after the FIRST marker (which directly judges the act): every filler's words,
        # the later boundaries and markers, and the final boundary. These must fill the whole
        # window, so neither the act nor that first marker is visible at the final judgment.
        after_first_marker = sum(len(tt.tok(f)) for f in pad) + 2 * (len(pad) - 1) + 1
        if after_first_marker >= tt.CTX or len(pad) >= MAX_FILLERS:
            break
    assert after_first_marker >= tt.CTX, "act or first marker still visible"
    return [right] + pad, [wrong] + pad, len(pad)


@torch.no_grad()
def judge_marked(model, vocab, sentences):
    """Model writes its own marker after each sentence; returns the lean of the final marker."""
    forms = [f for f in sw.FORMS if f in vocab.stoi]
    ids = [vocab.stoi[f] for f in forms]
    pos = np.array([mc.POSITION[f] for f in forms])
    start = [vocab.stoi[sw.FORMS[2]]] if START_MARKER else []
    ctx = [1] + start + vocab.encode(sentences[0]) + [1]
    for s in sentences[1:]:
        scores = [sw.lp_ids(model, ctx, [i]) for i in ids]
        ctx += [ids[int(np.argmax(scores))]] + vocab.encode(s) + [1]
    scores = np.array([sw.lp_ids(model, ctx, [i]) for i in ids])
    p = np.exp(scores - scores.max())
    return float((p / p.sum()) @ pos)


@torch.no_grad()
def judge_plain(model, vocab, sentences):
    """No marker: compare 'evil' vs 'right' judgment phrases after the last sentence (positive = right)."""
    ctx = [1]
    for s in sentences:
        ctx += vocab.encode(s) + [1]
    ctx = ctx[:-1] + vocab.encode(",")
    return (sw.lp_ids(model, ctx, vocab.encode(tt.JUDGE_RIGHT))
            - sw.lp_ids(model, ctx, vocab.encode(tt.JUDGE_EVIL)))


def main():
    global OUT, START_MARKER
    import sys
    if "--start-marker" in sys.argv:
        START_MARKER, OUT = True, HERE / "results_long_story_startmarker.json"
    verses = load_verses()
    texts = [t for _, t in verses]
    values = sw.word_values(texts)
    pool = [i for i in range(len(texts)) if i % 50]
    res = json.loads(OUT.read_text()) if OUT.exists() else {}
    for seed in SEEDS:
        for method in METHODS:
            corpus = marked_corpus(method, verses, values, seed)
            model, vocab = load_model(method, seed, [corpus[i] for i in pool])
            fillers = neutral_fillers(values, vocab)
            for version in ("short", "A", "B"):
                key = f"{method}/seed{seed}/{version}"
                if key in res:
                    continue
                correct, n_pad = [], []
                for k in range(len(ITEMS_V2)):
                    r, w, npad = build_stories(version, fillers, vocab, k)
                    judge = judge_plain if method == "baseline" else judge_marked
                    jr, jw = judge(model, vocab, r), judge(model, vocab, w)
                    correct.append(1.0 if jr > jw else 0.5 if np.isclose(jr, jw) else 0.0)
                    n_pad.append(npad)
                res[key] = {"correct": correct, "fillers_used": len(fillers), "mean_pad": float(np.mean(n_pad))}
                OUT.write_text(json.dumps(res))
                ties = sum(c == 0.5 for c in correct)
                print(f"  {key:22s} score {sum(correct):.1f}/100  ties {ties}  (neutral sentences after act: "
                      f"{np.mean(n_pad):.1f})", flush=True)
    report(res)


def report(res):
    print("\n" + "=" * 74)
    print("LONG-STORY TEST: judging after the act has scrolled out of view (50% = guessing)")
    print("=" * 74)
    counts = {}
    for version in ("short", "A", "B"):
        print(f"\n  version {version}" + {"short": " (no filler: act in view)",
                                          "A": " (verdict carried)", "B": " (act carried)"}[version])
        for m in METHODS:
            runs = [res[f"{m}/seed{s}/{version}"]["correct"] for s in SEEDS if f"{m}/seed{s}/{version}" in res]
            if not runs:
                continue
            c = np.array(runs).sum(0)
            counts[(m, version)] = c
            above, below = int((c * 2 > len(runs)).sum()), int((c * 2 < len(runs)).sum())
            print(f"    {m:10s} per run {', '.join(f'{sum(r):.1f}' for r in runs):20s} "
                  f"pairs above chance {above}, below {below} (p = {p_at_least(above, above + below):.4f})")

    def vs(a, b, version, label):
        if (a, version) not in counts or (b, version) not in counts:
            return
        x, y = counts[(a, version)], counts[(b, version)]
        w, l = int((x > y).sum()), int((x < y).sum())
        p = p_at_least(w, w + l)
        print(f"  {label}: {a} better on {w} pairs, worse on {l} (p = {p:.4f}) -> "
              f"{'CONFIRMED' if p < 0.05 else 'NOT CONFIRMED'}")

    print("\n  PRE-REGISTERED")
    vs("shifting", "label", "A", "L1 verdict carried: shifting beats label")
    vs("shifting", "label", "B", "L2 act carried:     shifting beats label")
    vs("carry3", "label", "A", "L3 verdict carried: carry3 beats label  ")


if __name__ == "__main__":
    main()
