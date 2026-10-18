"""
Bible Understanding Experiments
===============================

Question: can a system that only ever reads text (never sees, never acts)
build something we would call understanding? And are the Bible's *rules*
especially rich teaching material for it, as Romans 7:7 suggests
("I had not known sin, but by the law")?

Method: a classic "learn meaning from company kept" model.
  1. Count which words appear near which words (King James Bible, public domain).
  2. Weight surprising pairs (PPMI) and compress to 100 dimensions (SVD).
  3. Each word becomes a point; nearby points = related meaning.
No pre-trained knowledge is used. Everything the model knows comes from the text.

All test word lists below were written BEFORE any results were seen.

Run:  python experiments/bible_understanding.py   (needs numpy + scipy)
"""

from __future__ import annotations

import random
import re
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import svds

DATA = Path(__file__).parent / "data" / "KJV.txt"
DIM = 100
WINDOW = 4
MIN_COUNT = 3
SEEDS = [0, 1, 2, 3, 4]

STOP = set("""a an the and or but of to in on at by for with from unto upon into
that this these those it its is was be been were are am shall shalt will wilt
he him his she her they them their we us our i me my thou thee thy thine ye you
your not no nor as so then there which who whom what when all also have hath had
do did doth dost said saith say o let up out""".split())

# --------------------------------------------------------------------------
# Loading and reading strategies
# --------------------------------------------------------------------------

KJV_URL = ("https://raw.githubusercontent.com/scrollmapper/bible_databases/"
           "master/formats/txt/KJV.txt")


def load_verses() -> list[tuple[str, str]]:
    """Return [(book, raw_text), ...]. Downloads the KJV text on first run."""
    if not DATA.exists():
        import urllib.request
        DATA.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(KJV_URL, DATA)
    verses, book = [], None
    for line in DATA.read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            book = line[4:].strip()
        elif line.startswith("["):
            verses.append((book, re.sub(r"^\[\d+:\d+\]\s*", "", line)))
    return verses


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


def pairs_window(verse: str):
    """Reading A: word by word, each word sees its 4 neighbours."""
    toks = tokens(verse)
    for i, w in enumerate(toks):
        for j in range(max(0, i - WINDOW), min(len(toks), i + WINDOW + 1)):
            if i != j:
                yield w, toks[j], 1.0 / abs(i - j)


def pairs_verse(verse: str):
    """Reading B: the whole verse is one unit of meaning."""
    toks = [t for t in tokens(verse) if t not in STOP]
    for i, w in enumerate(toks):
        for j, c in enumerate(toks):
            if i != j:
                yield w, c, 1.0


def pairs_parallel(verse: str):
    """Reading C: Hebrew-poetry parallelism. Many verses say one thing twice:
    'Thy word is a lamp unto my feet, / and a light unto my path.'
    On top of reading A, align the two halves so each word also sees the word
    in the same relative position of the restating half."""
    yield from pairs_window(verse)
    halves = re.split(r"[;:]", verse, maxsplit=1)
    if len(halves) != 2:
        return
    a = [t for t in tokens(halves[0]) if t not in STOP]
    b = [t for t in tokens(halves[1]) if t not in STOP]
    if len(a) < 2 or len(b) < 2:
        return
    for i, w in enumerate(a):
        pos = i / (len(a) - 1) * (len(b) - 1)
        for j, c in enumerate(b):
            d = abs(j - pos)
            if d <= 1.5:
                weight = 1.0 / (1.0 + d)
                yield w, c, weight
                yield c, w, weight


READINGS = {"A word-by-word": pairs_window,
            "B verse-as-unit": pairs_verse,
            "C parallelism": pairs_parallel}

# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------

class Model:
    def __init__(self, verses: list[str], reading=pairs_window):
        counts = Counter(t for v in verses for t in tokens(v))
        self.vocab = [w for w, c in counts.items() if c >= MIN_COUNT]
        self.idx = {w: i for i, w in enumerate(self.vocab)}
        co = Counter()
        for v in verses:
            for w, c, wt in reading(v):
                if w in self.idx and c in self.idx and c not in STOP:
                    co[(self.idx[w], self.idx[c])] += wt
        rows, cols, vals = zip(*((i, j, v) for (i, j), v in co.items()))
        n = len(self.vocab)
        m = coo_matrix((vals, (rows, cols)), shape=(n, n)).tocsr()
        # PPMI with context smoothing (alpha = 0.75)
        total = m.sum()
        row = np.asarray(m.sum(1)).ravel()
        col = np.asarray(m.sum(0)).ravel() ** 0.75
        col /= col.sum()
        m = m.tocoo()
        pmi = np.log((m.data / total) / ((row[m.row] / total) * col[m.col] + 1e-12) + 1e-12)
        keep = pmi > 0
        ppmi = coo_matrix((pmi[keep], (m.row[keep], m.col[keep])), shape=(n, n)).tocsr()
        k = min(DIM, n - 2)
        u, s, _ = svds(ppmi, k=k, random_state=0)
        vec = u * np.sqrt(s)
        self.vec = vec / (np.linalg.norm(vec, axis=1, keepdims=True) + 1e-12)

    def has(self, w): return w in self.idx
    def v(self, w): return self.vec[self.idx[w]]
    def sim(self, a, b): return float(self.v(a) @ self.v(b))

    def neighbours(self, w, k=8):
        if not self.has(w):
            return []
        s = self.vec @ self.v(w)
        order = np.argsort(-s)
        return [self.vocab[i] for i in order if self.vocab[i] != w and self.vocab[i] not in STOP][:k]


def auc(pos: list[float], neg: list[float]) -> float:
    """Chance = 0.50, perfect = 1.00."""
    if not pos or not neg:
        return float("nan")
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))

# --------------------------------------------------------------------------
# Tests (fixed in advance)
# --------------------------------------------------------------------------

# General understanding: pairs a reader would call close in meaning.
SIMILAR = [("sword", "spear"), ("gold", "silver"), ("sheep", "goats"), ("bread", "meat"),
           ("king", "prince"), ("mercy", "compassion"), ("sin", "iniquity"),
           ("wicked", "ungodly"), ("joy", "gladness"), ("fear", "dread"),
           ("father", "mother"), ("son", "daughter"), ("sea", "waters"),
           ("mountain", "hill"), ("cry", "weep"), ("praise", "bless"),
           ("destroy", "consume"), ("strength", "might"), ("wisdom", "understanding"),
           ("horse", "chariot"), ("oil", "wine"), ("ox", "ass"), ("brass", "iron"),
           ("city", "village"), ("sun", "moon"), ("hand", "arm"), ("eyes", "ears"),
           ("death", "grave"), ("trouble", "affliction"), ("servant", "handmaid")]

# Colour, as a blind reader would meet it: only through words.
COLOURS = ["white", "red", "black", "green", "purple", "blue"]
COLOUR_OBJECTS = {  # object -> the colour a sighted reader expects
    "snow": "white", "wool": "white", "milk": "white", "linen": "white",
    "blood": "red", "wine": "red",
    "night": "black", "darkness": "black", "sackcloth": "black",
    "grass": "green", "tree": "green", "herb": "green",
    "fine": "purple", "robe": "purple",
}
PURE = ["clean", "pure", "righteous", "holy", "washed"]
SINFUL = ["sin", "sins", "iniquity", "wicked", "unclean"]

# Moral understanding: the axis is built from seed words only.
GOOD_SEEDS = ["good", "righteous", "righteousness", "upright"]
BAD_SEEDS = ["evil", "wicked", "wickedness", "iniquity"]
# ...and tested on acts the axis never saw.
RIGHT_ACTS = ["give", "help", "forgive", "honour", "mercy", "love", "truth", "charity",
              "kindness", "justice", "peace", "praise", "obey", "humble", "faithful"]
WRONG_ACTS = ["kill", "steal", "adultery", "murder", "covet", "envy", "theft",
              "fornication", "idolatry", "deceit", "pride", "drunkenness", "hatred",
              "falsehood", "lying"]

RULE_RE = re.compile(r"\b(shalt not|shall not|thou shalt|ye shall|commandments?|statutes?|"
                     r"ordinances?|judgments|forbid|beware|take heed)\b", re.I)


def test_similarity(m: Model) -> float:
    pairs = [(a, b) for a, b in SIMILAR if m.has(a) and m.has(b)]
    words = sorted({w for p in pairs for w in p})
    rng = random.Random(0)
    neg = []
    while len(neg) < 300:
        a, b = rng.sample(words, 2)
        if (a, b) not in SIMILAR and (b, a) not in SIMILAR:
            neg.append(m.sim(a, b))
    return auc([m.sim(a, b) for a, b in pairs], neg)


def test_colour_objects(m: Model):
    hits, total, detail = 0, 0, []
    for obj, colour in COLOUR_OBJECTS.items():
        if not m.has(obj) or not m.has(colour):
            continue
        ranked = sorted((c for c in COLOURS if m.has(c)), key=lambda c: -m.sim(obj, c))
        total += 1
        hits += ranked[0] == colour
        detail.append(f"{obj}->{ranked[0]}{'' if ranked[0] == colour else f' (expected {colour})'}")
    return hits, total, detail


def mean_sim(m: Model, w: str, group: list[str]) -> float:
    g = [x for x in group if m.has(x)]
    return float(np.mean([m.sim(w, x) for x in g])) if g and m.has(w) else float("nan")


def test_moral(m: Model) -> float:
    good = [w for w in GOOD_SEEDS if m.has(w)]
    bad = [w for w in BAD_SEEDS if m.has(w)]
    axis = np.mean([m.v(w) for w in good], 0) - np.mean([m.v(w) for w in bad], 0)
    pos = [float(m.v(w) @ axis) for w in RIGHT_ACTS if m.has(w)]
    neg = [float(m.v(w) @ axis) for w in WRONG_ACTS if m.has(w)]
    return auc(pos, neg)

# --------------------------------------------------------------------------
# Experiments
# --------------------------------------------------------------------------

def main():
    verses = load_verses()
    texts = [t for _, t in verses]
    print(f"Loaded {len(texts):,} verses, {sum(len(tokens(t)) for t in texts):,} words.\n")

    print("=" * 70)
    print("EXPERIMENT 1 - Colour without sight")
    print("=" * 70)
    full = Model(texts)
    for w in ["white", "scarlet", "red", "black", "purple", "green"]:
        print(f"  {w:8s} keeps company with: {', '.join(full.neighbours(w))}")
    hits, total, detail = test_colour_objects(full)
    print(f"\n  Object -> colour (pick 1 of {len(COLOURS)}, chance = {1/len(COLOURS):.0%}): "
          f"{hits}/{total} = {hits/total:.0%}")
    print("   ", "; ".join(detail))
    print("\n  What colour MEANS (Isaiah 1:18 'sins as scarlet ... white as snow'):")
    for c in ["white", "scarlet", "red", "crimson", "black"]:
        p, s = mean_sim(full, c, PURE), mean_sim(full, c, SINFUL)
        lean = "purity" if p > s else "sin"
        print(f"    {c:8s} near purity {p:+.3f} | near sin {s:+.3f}  -> leans {lean}")

    print("\n" + "=" * 70)
    print("EXPERIMENT 2 - Three ways of reading the tokens")
    print("=" * 70)
    models = {}
    for name, fn in READINGS.items():
        models[name] = Model(texts, fn)
        m = models[name]
        h, t, _ = test_colour_objects(m)
        print(f"  {name:18s} similarity AUC {test_similarity(m):.3f} | "
              f"moral AUC {test_moral(m):.3f} | colour {h}/{t}")
    print("  (AUC: 0.50 = guessing, 1.00 = perfect)")

    print("\n" + "=" * 70)
    print("EXPERIMENT 3 - Are the rules the secret? (Romans 7:7)")
    print("=" * 70)
    rule_idx = [i for i, t in enumerate(texts) if RULE_RE.search(t)]
    other_idx = [i for i in range(len(texts)) if i not in set(rule_idx)]
    n = len(rule_idx)
    print(f"  Rule verses (thou shalt / shall not / commandments / statutes...): "
          f"{n:,} of {len(texts):,} ({n/len(texts):.0%})\n")

    def run(idx):
        m = Model([texts[i] for i in idx])
        return test_similarity(m), test_moral(m)

    def row(label, results):
        sims, morals = zip(*results)
        sd = lambda xs: f" ±{np.std(xs):.3f}" if len(xs) > 1 else "       "
        print(f"  {label:38s} similarity {np.mean(sims):.3f}{sd(sims)} | "
              f"moral {np.mean(morals):.3f}{sd(morals)}")
        return np.mean(sims), np.mean(morals)

    print("  3a. Learn ONLY from a slice of the text (same size each):")
    r_rules = row("rules only", [run(rule_idx)])
    r_rand = row("random verses (5 draws)",
                 [run(random.Random(s).sample(range(len(texts)), n)) for s in SEEDS])
    r_narr = row("non-rule verses only (5 draws)",
                 [run(random.Random(s).sample(other_idx, n)) for s in SEEDS])

    print("\n  3b. Learn from everything EXCEPT a slice:")
    row("full Bible", [(test_similarity(full), test_moral(full))])
    k_rules = row("minus the rules", [run(other_idx)])
    k_rand = row("minus same number random (5 draws)",
                 [run(sorted(set(range(len(texts))) -
                             set(random.Random(s).sample(range(len(texts)), n)))) for s in SEEDS])

    def compare(a, b, sd):
        """Call a difference real only if it is bigger than the random spread."""
        if abs(a - b) <= max(sd, 0.01):
            return "NO CLEAR DIFFERENCE"
        return "BETTER" if a > b else "WORSE"

    rand_sd_moral = np.std([run(random.Random(s).sample(range(len(texts)), n))[1] for s in SEEDS[:3]])
    print("\n  Verdict (differences inside random noise are called 'no clear difference'):")
    print(f"    Rules-only vs random, moral meaning:  {compare(r_rules[1], r_rand[1], rand_sd_moral)}")
    print(f"    Rules-only vs random, general meaning: {compare(r_rules[0], r_rand[0], 0.039)}")
    print(f"    Removing rules vs removing random:      {compare(k_rules[1], k_rand[1], 0.014)}")

    print("\n" + "=" * 70)
    print("EXPERIMENT 4 - 'I had not known lust, except the law had said, Thou shalt not covet'")
    print("=" * 70)
    no_rules = Model([texts[i] for i in other_idx])
    print("  Where each wrong act sits on the good(+)/evil(-) axis, with and without the rules:")
    print(f"  {'act':12s} {'full Bible':>11s} {'no rules':>9s}  times seen without rules")
    counts_nr = Counter(t for i in other_idx for t in tokens(texts[i]))

    def place(m, w):
        good = np.mean([m.v(x) for x in GOOD_SEEDS if m.has(x)], 0)
        bad = np.mean([m.v(x) for x in BAD_SEEDS if m.has(x)], 0)
        return float(m.v(w) @ (good - bad)) if m.has(w) else float("nan")

    flipped = 0
    for w in WRONG_ACTS:
        a, b = place(full, w), place(no_rules, w)
        mark = "  <- loses its wrongness" if a < 0 <= b or (a < 0 and np.isnan(b)) else ""
        flipped += bool(mark)
        print(f"  {w:12s} {a:+11.3f} {b:+9.3f}  {counts_nr[w]:>5d}{mark}")
    print(f"\n  Wrong acts that lose their wrongness without the rules: {flipped}/{len(WRONG_ACTS)}")

if __name__ == "__main__":
    main()
