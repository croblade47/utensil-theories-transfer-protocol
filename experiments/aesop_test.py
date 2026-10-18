"""
Aesop Moral Test: do lessons told as stories transfer to a culture never seen?
=============================================================================

Theory under test (from the project owner): lessons taught through story carry
more transferable meaning than lessons taught as rules.

Test material is Aesop's own text, so nobody on this project wrote it.
Aesop is NEVER in any training set.

Each Aesop fable ends with a one-line moral. For every PAIR of fables (i, j)
the model must prefer the true matching over the swapped one:

    log P(moral_i | fable_i) + log P(moral_j | fable_j)
        >  log P(moral_j | fable_i) + log P(moral_i | fable_j)

How likely a moral is in general cancels out, so guessing scores 50%.

Training sets (same number of tokens, same tiny transformer, same steps):
  stories   folk tales and myths from 9 cultures (Grimm, Celtic, Indian,
            Japanese, Chinese, Arabian Nights, Southern Nigeria, and two
            Dakota collections written by Dakota authors), no Aesop
  bible     King James Bible, whole chapters sampled to the same size
  novels    Austen, Chesterton, Melville: prose of the same era with no
            built-in lessons (controls for vocabulary and writing style)
Secondary, smaller size:
  rules     Bible rule verses + Proverbs + Ecclesiastes + Tao Te Ching
  stories_small   story paragraphs sampled to the same size as rules

PRE-REGISTERED (written and committed before any model was trained on these sets)
  P1  stories model (2 seeds, averaged) beats 50%:  permutation test p < 0.05
  P2  stories beats novels:  per-fable scores, sign test over fables, p < 0.05
  S1  stories vs bible       (same test, secondary)
  S2  rules vs stories_small (same test, 1 seed, secondary)
  S3  "no word clue" pairs: the same scores counted only on pairs where plain
      word overlap between fable and moral is tied (gives no hint), so a
      model can only win them by something beyond matching words
  Descriptive only: word-overlap reference score, unknown-word rates.

Run:  python experiments/aesop_test.py      (about 1.5 hours on 4 CPU cores)
"""

from __future__ import annotations

import json
import random
import re
from math import comb
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

import tiny_transformer as tt
import world_stories as ws
from bible_understanding import RULE_RE, STOP

HERE = Path(__file__).parent
DATA = HERE / "data"
MODELS = HERE / "models"
OUT = HERE / "results_aesop.json"

tt.CTX, tt.BATCH = 128, 32          # longer window for whole fables; same tokens per step
STEPS = 1500
MAIN_SEEDS = [0, 1]
CORPUS_SEED = 0                      # corpora are identical across model seeds
PERMUTATIONS = 2000
STORY_KEYS = ["grimm", "celtic", "india", "japan", "china", "arabian", "nigeria", "zitkala", "sioux"]
NOVELS = ["austen-emma", "chesterton-ball", "melville-moby_dick", "austen-sense",
          "chesterton-brown", "austen-persuasion", "chesterton-thursday"]
NOVELS_URL = "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/gutenberg.zip"

# ---------------------------------------------------------------------------
# Test material
# ---------------------------------------------------------------------------

def aesop_fables():
    """[(title, fable_text, moral)] for fables that end in a short moral line."""
    text = ws.load("aesop")
    body = text[text.index("Aesop's Fables\n\n\n", 200):].split("\n", 1)[1]
    parts = re.split(r"\n\n\n  ([A-Z][^\n]+)\n\n\n", "\n\n\n" + body)
    out = []
    for i in range(1, len(parts), 2):
        paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", parts[i + 1]) if p.strip()]
        if len(paras) >= 2 and len(paras[-1].split()) <= 20:
            out.append((parts[i].strip(), " ".join(paras[:-1]), paras[-1]))
    return out

# ---------------------------------------------------------------------------
# Training corpora (lists of text units; each unit is a paragraph or verse)
# ---------------------------------------------------------------------------

def paragraphs(text, min_words=5):
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text)]
    return [p for p in paras if len(p.split()) >= min_words]


def size(units):
    return sum(len(tt.tok(u)) for u in units)


def take(units, n_tokens):
    out, total = [], 0
    for u in units:
        if total >= n_tokens:
            break
        out.append(u)
        total += len(tt.tok(u))
    return out


def bible_chapters():
    chapters, book, cur = [], None, None
    for line in (DATA / "KJV.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            book = line[4:].strip()
            continue
        m = re.match(r"^\[(\d+):(\d+)\]\s*(.*)", line)
        if not m:
            continue
        if m.group(2) == "1":
            cur = (book, int(m.group(1)), [])
            chapters.append(cur)
        cur[2].append(m.group(3))
    return chapters


def novels_text(name):
    path = DATA / "novels" / "gutenberg" / f"{name}.txt"
    if not path.exists():
        import io
        import urllib.request
        import zipfile
        raw = urllib.request.urlopen(NOVELS_URL, timeout=120).read()
        zipfile.ZipFile(io.BytesIO(raw)).extractall(DATA / "novels")
    return path.read_text(encoding="utf-8", errors="replace")


def build_corpora():
    stories = [p for k in STORY_KEYS for p in paragraphs(ws.load(k))]
    n = size(stories)

    chapters = bible_chapters()
    order = list(range(len(chapters)))
    random.Random(CORPUS_SEED).shuffle(order)
    chosen, total = [], 0
    for i in order:
        if total >= n:
            break
        chosen.append(i)
        total += sum(len(tt.tok(v)) for v in chapters[i][2])
    bible = [v for i in sorted(chosen) for v in chapters[i][2]]

    novels = take([p for name in NOVELS for p in paragraphs(novels_text(name))], n)

    rules = []
    for book, _, verses in chapters:
        for v in verses:
            if book in ("Proverbs", "Ecclesiastes") or RULE_RE.search(v):
                rules.append(v)
    rules += paragraphs(ws.load("tao"), min_words=3)
    shuffled = stories[:]
    random.Random(CORPUS_SEED).shuffle(shuffled)
    stories_small = take(shuffled, size(rules))

    return {"stories": stories, "bible": bible, "novels": novels,
            "rules": rules, "stories_small": stories_small}

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

@torch.no_grad()
def moral_matrix(model, vocab, fables):
    """L[i, j] = log P(moral_j | fable_i)."""
    morals = [vocab.encode(m) for _, _, m in fables]
    room = tt.CTX - max(len(m) for m in morals) - 2
    L = np.zeros((len(fables), len(fables)))
    for i, (_, fable, _) in enumerate(fables):
        ctx = [1] + vocab.encode(fable)[-room:] + [1]
        for j, m in enumerate(morals):
            ids = torch.tensor([ctx + m])
            lp = F.log_softmax(model(ids)[0], -1)
            L[i, j] = sum(lp[len(ctx) - 1 + k, t].item() for k, t in enumerate(m))
    return L


def pair_wins(L):
    """W[i, j] = 1 if the true matching beats the swap for pair (i, j); 0.5 on ties."""
    d = np.diag(L)
    true = d[:, None] + d[None, :]
    swap = L + L.T
    W = (true > swap).astype(float) + 0.5 * (true == swap)
    np.fill_diagonal(W, np.nan)
    return W


def match_rate(L, mask=None):
    W = pair_wins(L)
    return float(np.nanmean(W if mask is None else np.where(mask, W, np.nan)))


def no_clue_mask(fables):
    """Pairs where word overlap gives exactly the same score to the true and swapped matching."""
    ov = overlap_matrix(fables)
    d = np.diag(ov)
    m = np.isclose(d[:, None] + d[None, :], ov + ov.T)
    np.fill_diagonal(m, False)
    return m


def per_fable(L):
    return np.nanmean(pair_wins(L), axis=1)


def permutation_p(L, rng):
    obs = match_rate(L)
    n = L.shape[0]
    hits = sum(match_rate(L[:, p]) >= obs for p in (rng.permutation(n) for _ in range(PERMUTATIONS)))
    return (1 + hits) / (1 + PERMUTATIONS)


def sign_test(a, b):
    """One-sided: is a better than b, fable by fable?"""
    wins, losses = int((a > b).sum()), int((a < b).sum())
    n = wins + losses
    p = sum(comb(n, k) for k in range(wins, n + 1)) / 2 ** n if n else 1.0
    return wins, losses, p


def overlap_matrix(fables):
    words = lambda t: {w for w in tt.tok(t) if w.isalpha() and w not in STOP}
    F_ = [words(f) for _, f, _ in fables]
    M_ = [words(m) for _, _, m in fables]
    return np.array([[len(F_[i] & M_[j]) / max(1, len(M_[j])) for j in range(len(fables))]
                     for i in range(len(fables))])

# ---------------------------------------------------------------------------

def get_model(name, seed, units):
    vocab = tt.Vocab(units)
    path = MODELS / f"aesop_{name}_seed{seed}_ctx{tt.CTX}_steps{STEPS}.pt"
    model = tt.TinyGPT(len(vocab))
    if path.exists():
        model.load_state_dict(torch.load(path))
        model.eval()
    else:
        print(f"\n== training {name} seed {seed} on {len(units):,} units / {size(units):,} tokens", flush=True)
        model = tt.train(vocab, units, STEPS, seed)
        MODELS.mkdir(exist_ok=True)
        torch.save(model.state_dict(), path)
    return model, vocab


def main():
    fables = aesop_fables()
    corpora = build_corpora()
    print(f"Aesop fables with a moral line: {len(fables)}  (pairs: {len(fables) * (len(fables) - 1) // 2:,})")
    for k, v in corpora.items():
        print(f"  corpus {k:14s} {len(v):>7,} units  {size(v):>9,} tokens")

    results = json.loads(OUT.read_text()) if OUT.exists() else {}
    plan = [(c, s) for s in MAIN_SEEDS for c in ("stories", "novels", "bible")] + \
           [("rules", 0), ("stories_small", 0)]
    for name, seed in plan:
        key = f"{name}/seed{seed}"
        if key in results:
            continue
        model, vocab = get_model(name, seed, corpora[name])
        test_words = [w for _, f, m in fables for w in tt.tok(f + " " + m)]
        unknown = sum(w not in vocab.stoi for w in test_words) / len(test_words)
        L = moral_matrix(model, vocab, fables)
        results[key] = {"L": L.tolist(), "unknown_word_rate": round(unknown, 4)}
        OUT.write_text(json.dumps(results))
        print(f"  {key}: match rate {match_rate(L):.3f}  unknown words {unknown:.1%}", flush=True)

    analyse(results, fables)


def analyse(results, fables):
    rng = np.random.default_rng(0)
    mats = {}
    for name in ("stories", "novels", "bible", "rules", "stories_small"):
        Ls = [np.array(results[f"{name}/seed{s}"]["L"]) for s in MAIN_SEEDS if f"{name}/seed{s}" in results]
        if Ls:
            mats[name] = np.mean(Ls, 0)

    print("\n" + "=" * 72)
    print(f"AESOP MORAL TEST  ({len(fables)} fables never seen in training; 50% = guessing)")
    print("=" * 72)
    ov = overlap_matrix(fables)
    mask = no_clue_mask(fables)
    print(f"  word-overlap reference (no model):  {match_rate(ov):.3f}")
    print(f"  pairs with no word clue: {int(mask.sum() // 2):,} of {len(fables) * (len(fables) - 1) // 2:,}")
    for name, L in mats.items():
        runs = [match_rate(np.array(results[f'{name}/seed{s}']['L'])) for s in MAIN_SEEDS if f'{name}/seed{s}' in results]
        each = ", ".join(f"{r:.3f}" for r in runs)
        print(f"  {name:14s} averaged {match_rate(L):.3f}  (runs: {each})  p vs chance = {permutation_p(L, rng):.4f}"
              f"   | no-clue pairs {match_rate(L, mask):.3f}")

    def compare(a, b):
        w, l, p = sign_test(per_fable(mats[a]), per_fable(mats[b]))
        print(f"  {a} vs {b}: {a} better on {w} fables, worse on {l}  (p = {p:.4f})")
        return p

    print()
    p2 = compare("stories", "novels") if {"stories", "novels"} <= mats.keys() else float("nan")
    compare("stories", "bible") if {"stories", "bible"} <= mats.keys() else None
    compare("rules", "stories_small") if {"rules", "stories_small"} <= mats.keys() else None
    compare("stories_small", "rules") if {"rules", "stories_small"} <= mats.keys() else None

    if "stories" in mats:
        p1 = permutation_p(mats["stories"], np.random.default_rng(1))
        print("\n  PRE-REGISTERED VERDICT")
        print(f"    P1 stories beat chance:  {'CONFIRMED' if p1 < 0.05 else 'NOT CONFIRMED'}  (p = {p1:.4f})")
        print(f"    P2 stories beat novels:  {'CONFIRMED' if p2 < 0.05 else 'NOT CONFIRMED'}  (p = {p2:.4f})")


if __name__ == "__main__":
    main()
