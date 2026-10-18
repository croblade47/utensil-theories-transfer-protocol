"""
Aesop Moral Test: do lessons told as stories transfer to a culture never seen?
=============================================================================

Theory under test (from the project owner): lessons taught through story carry
more transferable meaning than lessons taught as rules.

The test material is Aesop's own text (Jacobs' 1894 edition), so nobody on this
project wrote it. Aesop is never in any training set. Each fable ends with a
moral. For every PAIR of fables (i, j) the model must prefer the true matching
over the swapped one:

    log P(moral_i | fable_i) + log P(moral_j | fable_j)
        >  log P(moral_j | fable_i) + log P(moral_i | fable_j)

How likely a moral is in general cancels out, so guessing scores 50%.

VERSION 2: revised after an adversarial pre-run review, BEFORE any training
---------------------------------------------------------------------------
- Parser fixed: 82 fables split correctly (v1 merged 5 into one and dropped 11).
- Leak removed: 8 test fables are retold inside the training stories, or have a
  moral that appears in training. They are excluded from the test:
  Wolf & Crane, Fox & Cat, Tortoise & Birds, Ass in the Lion's Skin,
  Milkmaid & Her Pail, Cat-Maiden, Man & Serpent, Young Thief & His Mother.
  Jacobs' prefaces and "Notes and References" (Indian, Celtic) and the Nigeria
  introduction, which discuss Aesop by name, are removed from training.
- Punctuation shortcut neutralized: a quoted moral follows a fable ending in a
  speech lead-in (": " / ", "). That alone scores 72%. All tests use only
  SAME-FORMAT pairs (both morals quoted, or both plain), where the shortcut
  scores exactly 50%.
- The sign test over fables was invalid (false alarms about 3x too often).
  Comparisons now use a paired row-swap permutation test.
- The "no word clue" mask is computed on the part of each fable the model actually
  sees, using 5-letter word stems, and is recomputed for every permutation.
- New control, stories_shuffled: the same story corpus with sentences shuffled
  across the whole corpus. Same words, characters and style; the
  story-to-lesson structure is destroyed.
- The rules test now compares against Bible narrative chapters, the same
  translation as the rules, with steps scaled to the same number of passes.

Training sets (same tiny transformer; main sets matched at ~750k tokens):
  stories           folk tales and myths from 9 cultures, no Aesop
  stories_shuffled  the same, with sentences shuffled (control)
  novels            Austen, Chesterton, Melville: coherent prose, fewer explicit
                    lessons, a different world (control for style)
  bible             King James Bible, whole chapters sampled to the same size
  rules             Bible rule verses + Proverbs + Ecclesiastes + Tao Te Ching (small)
  narrative         KJV narrative chapters without rule verses, same size as rules

PRE-REGISTERED (v2, committed before any training on these sets)
  All scores use same-format pairs.
  P1  sanity check: each set beats 50% (permutation test). Expected to pass,
      because word overlap alone scores well above 50%.
  P2  stories > novels:            paired row-swap permutation p < 0.05 AND
                                   stories wins in both seed-matched pairs
  P2b stories > stories_shuffled:  same rule
      P2 and P2b both confirmed = evidence that story structure, not just
      vocabulary or setting, carries the lessons.
  P3  stories beats 50% on no-word-clue pairs (mask recomputed per permutation),
      p < 0.05. A null here means "inconclusive, low power", not "no comprehension".
  S1  stories vs bible (descriptive; unknown-word rates printed alongside)
  S2  narrative > rules (paired permutation, 1 seed)

Run:  python experiments/aesop_test.py      (about 1.7 hours on 4 CPU cores)
"""

from __future__ import annotations

import hashlib
import json
import random
import re
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
MAIN_STEPS = 1500
MAIN_SEEDS = [0, 1]
CORPUS_SEED = 0                      # corpora are identical across model seeds
PERMUTATIONS = 2000
MAIN = ["stories", "novels", "stories_shuffled", "bible"]
SMALL = ["rules", "narrative"]
STORY_KEYS = ["grimm", "celtic", "india", "japan", "china", "arabian", "nigeria", "zitkala", "sioux"]
NOVELS = ["austen-emma", "chesterton-ball", "melville-moby_dick", "austen-sense",
          "chesterton-brown", "austen-persuasion", "chesterton-thursday"]
NARRATIVE_BOOKS = ["Genesis", "Judges", "Ruth", "I Samuel", "II Samuel", "I Kings", "II Kings", "Esther", "Jonah"]
NOVELS_URL = "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/gutenberg.zip"
EXCLUDE = {"The Wolf and the Crane", "The Fox and the Cat", "The Tortoise and the Birds",
           "The Ass in the Lion's Skin", "The Milkmaid and Her Pail", "The Cat-Maiden",
           "The Man and the Serpent", "The Young Thief and His Mother"}

# ---------------------------------------------------------------------------
# Test material
# ---------------------------------------------------------------------------

def aesop_fables(exclude=True):
    """[(title, fable_text, moral_text)] for fables that end in a short moral line."""
    text = ws.load("aesop")
    body = text[text.index("Aesop's Fables\n\n\n", 200):].split("\n", 1)[1]
    body = body.replace("\n .", "\n\n")               # some morals sit on a line starting " ."
    parts = re.split(r"\n\n\n {0,2}([A-Z][^\n]+)\n\n\n", "\n\n\n" + body)
    out = []
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", parts[i + 1]) if p.strip()]
        if len(paras) >= 2 and len(paras[-1].split()) <= 20 and not (exclude and title in EXCLUDE):
            out.append((title, " ".join(paras[:-1]), paras[-1]))
    return out


def room():
    """Fable tokens the model sees: the window minus the longest moral and two boundaries."""
    longest = max(len(tt.tok(m)) for _, _, m in aesop_fables(exclude=False))
    return tt.CTX - longest - 2


def visible(fable):
    return tt.tok(fable)[-room():]

# ---------------------------------------------------------------------------
# Training corpora (lists of text units: paragraphs or verses)
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


def story_text(key):
    """Story collection with scholarly apparatus that discusses Aesop removed."""
    t = ws.load(key)
    if key == "india":                                   # drop preface and notes (they discuss Aesop)
        t = t[t.index("\nThe Lion and the Crane\n"):t.rindex("\nNotes and References\n")]
    elif key == "celtic":
        t = t[t.index("CONNLA AND THE FAIRY MAIDEN\n\nConnla"):t.rindex("\nNOTES AND REFERENCES\n")]
    elif key == "nigeria":
        t = t[t.index("_The Tortoise with a Pretty Daughter_\n"):]
    return t


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


def shuffle_sentences(units, seed):
    """Same sentences, same unit sizes, but sentences shuffled across the whole corpus."""
    split = [re.split(r"(?<=[.!?])\s+", u) for u in units]
    pool = [s for ss in split for s in ss]
    random.Random(seed).shuffle(pool)
    out, k = [], 0
    for ss in split:
        out.append(" ".join(pool[k:k + len(ss)]))
        k += len(ss)
    return out


def build_corpora():
    stories = [p for k in STORY_KEYS for p in paragraphs(story_text(k))]
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

    rules = [v for book, _, verses in chapters for v in verses
             if book in ("Proverbs", "Ecclesiastes") or RULE_RE.search(v)]
    rules += paragraphs(ws.load("tao"), min_words=3)
    narrative = take([v for book, _, verses in chapters if book in NARRATIVE_BOOKS
                      for v in verses if not RULE_RE.search(v)], size(rules))

    return {"stories": stories, "novels": novels, "bible": bible,
            "stories_shuffled": shuffle_sentences(stories, CORPUS_SEED),
            "rules": rules, "narrative": narrative}


def corpus_hash(units):
    return hashlib.md5("\n".join(units).encode()).hexdigest()[:8]


def split_heldout(units):
    """Every 50th unit is held out to measure plain language skill."""
    return [u for i, u in enumerate(units) if i % 50], [u for i, u in enumerate(units) if i % 50 == 0]


def steps_for(name, train_units, main_tokens):
    if name in MAIN:
        return MAIN_STEPS
    passes = MAIN_STEPS * tt.BATCH * tt.CTX / main_tokens        # same number of passes as the main sets
    return max(100, int(round(passes * size(train_units) / (tt.BATCH * tt.CTX))))

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

@torch.no_grad()
def moral_matrix(model, vocab, fables):
    """L[i, j] = log P(moral_j | fable_i), fable cut to the same visible window for every moral."""
    morals = [vocab.encode(m) for _, _, m in fables]
    L = np.zeros((len(fables), len(fables)))
    for i, (_, fable, _) in enumerate(fables):
        ctx = [1] + [vocab.stoi.get(t, 0) for t in visible(fable)] + [1]
        for j, m in enumerate(morals):
            lp = F.log_softmax(model(torch.tensor([ctx + m]))[0], -1)
            L[i, j] = sum(lp[len(ctx) - 1 + k, t].item() for k, t in enumerate(m))
    return L


@torch.no_grad()
def mean_loss(model, vocab, texts):
    losses = []
    for t in texts:
        ids = ([1] + vocab.encode(t))[: tt.CTX + 1]
        if len(ids) < 3:
            continue
        x, y = torch.tensor([ids[:-1]]), torch.tensor(ids[1:])
        losses.append(F.cross_entropy(model(x)[0], y).item())
    return float(np.mean(losses))


def pair_wins(L):
    d = np.diag(L)
    true = d[:, None] + d[None, :]
    swap = L + L.T
    W = (true > swap).astype(float) + 0.5 * (true == swap)
    np.fill_diagonal(W, np.nan)
    return W


def match_rate(L, mask):
    return float(np.nanmean(np.where(mask, pair_wins(L), np.nan)))


def quoted_flags(fables):
    return np.array([m.lstrip().startswith('"') for _, _, m in fables])


def stems(tokens):
    return {w[:5] for w in tokens if w.isalpha() and w not in STOP and len(w) > 2}


def overlap_matrix(fables):
    Fs = [stems(visible(f)) for _, f, _ in fables]
    Ms = [stems(tt.tok(m)) for _, _, m in fables]
    return np.array([[len(Fs[i] & Ms[j]) / max(1, len(Ms[j])) for j in range(len(fables))]
                     for i in range(len(fables))])


def masks(fables, ov, quoted, perm=None):
    """(same-format mask, same-format AND no-word-clue mask) under a moral assignment."""
    p = np.arange(len(fables)) if perm is None else perm
    q = quoted[p]
    same = q[:, None] == q[None, :]
    o = ov[:, p]
    d = np.diag(o)
    ties = np.isclose(d[:, None] + d[None, :], o + o.T)
    np.fill_diagonal(same, False)
    return same, same & ties


def chance_p(L, fables, ov, quoted, which, rng):
    """Permutation test vs chance; masks recomputed for every permuted assignment."""
    k = 0 if which == "same" else 1
    obs = match_rate(L, masks(fables, ov, quoted)[k])
    hits = 0
    for _ in range(PERMUTATIONS):
        p = rng.permutation(len(fables))
        hits += match_rate(L[:, p], masks(fables, ov, quoted, p)[k]) >= obs
    return obs, (1 + hits) / (1 + PERMUTATIONS)


def paired_p(La, Lb, mask, rng):
    """One-sided paired row-swap permutation test: is model A better than model B?"""
    obs = match_rate(La, mask) - match_rate(Lb, mask)
    hits = 0
    for _ in range(PERMUTATIONS):
        s = rng.random(La.shape[0]) < 0.5
        Xa, Xb = np.where(s[:, None], Lb, La), np.where(s[:, None], La, Lb)
        hits += match_rate(Xa, mask) - match_rate(Xb, mask) >= obs
    return obs, (1 + hits) / (1 + PERMUTATIONS)

# ---------------------------------------------------------------------------

def main():
    fables = aesop_fables()
    titles = [t for t, _, _ in fables]
    corpora = build_corpora()
    ov, quoted = overlap_matrix(fables), quoted_flags(fables)
    same, noclue = masks(fables, ov, quoted)
    print(f"Aesop fables in test: {len(fables)} (excluded {len(EXCLUDE)} for leakage); "
          f"same-format pairs {int(same.sum() // 2):,}; no-clue pairs {int(noclue.sum() // 2):,}")
    main_tokens = None
    for k, v in corpora.items():
        print(f"  corpus {k:17s} {len(v):>7,} units {size(v):>9,} tokens  [{corpus_hash(v)}]")

    results = json.loads(OUT.read_text()) if OUT.exists() else {}
    plan = [(c, s) for s in MAIN_SEEDS for c in MAIN] + [(c, 0) for c in SMALL]
    for name, seed in plan:
        h = corpus_hash(corpora[name])
        key = f"{name}/seed{seed}/{h}"
        if key in results and results[key].get("titles") == titles:
            continue
        train_units, held = split_heldout(corpora[name])
        if main_tokens is None:
            main_tokens = size(split_heldout(corpora["stories"])[0])
        steps = steps_for(name, train_units, main_tokens)
        vocab = tt.Vocab(train_units)
        path = MODELS / f"aesop2_{name}_seed{seed}_{h}_steps{steps}.pt"
        model = tt.TinyGPT(len(vocab))
        if path.exists():
            model.load_state_dict(torch.load(path))
            model.eval()
        else:
            print(f"\n== training {name} seed {seed}: {size(train_units):,} tokens, {steps} steps", flush=True)
            model = tt.train(vocab, train_units, steps, seed)
            MODELS.mkdir(exist_ok=True)
            torch.save(model.state_dict(), path)
        words = [w for _, f, m in fables for w in tt.tok(f + " " + m)]
        L = moral_matrix(model, vocab, fables)
        results[key] = {
            "titles": titles, "L": L.tolist(), "steps": steps,
            "unknown_word_rate": round(sum(w not in vocab.stoi for w in words) / len(words), 4),
            "heldout_loss": round(mean_loss(model, vocab, held), 3),
            "fable_loss": round(mean_loss(model, vocab, [f for _, f, _ in fables]), 3),
        }
        OUT.write_text(json.dumps(results))
        r = results[key]
        print(f"  {key}: same-format match {match_rate(L, same):.3f}  no-clue {match_rate(L, noclue):.3f}  "
              f"unknown {r['unknown_word_rate']:.1%}  held-out loss {r['heldout_loss']}  fable loss {r['fable_loss']}",
              flush=True)

    analyse(results, fables, corpora)


def analyse(results, fables, corpora):
    titles = [t for t, _, _ in fables]
    ov, quoted = overlap_matrix(fables), quoted_flags(fables)
    same, noclue = masks(fables, ov, quoted)
    runs = {}
    for name in MAIN + SMALL:
        h = corpus_hash(corpora[name])
        seeds = MAIN_SEEDS if name in MAIN else [0]
        Ls = [np.array(results[f"{name}/seed{s}/{h}"]["L"]) for s in seeds
              if f"{name}/seed{s}/{h}" in results and results[f"{name}/seed{s}/{h}"]["titles"] == titles]
        if Ls:
            runs[name] = (Ls, [results[f"{name}/seed{s}/{h}"] for s in seeds if f"{name}/seed{s}/{h}" in results])
    avg = {k: np.mean(v[0], 0) for k, v in runs.items()}
    rng = np.random.default_rng(0)

    print("\n" + "=" * 76)
    print(f"AESOP MORAL TEST  ({len(fables)} fables never seen in training; 50% = guessing)")
    print("=" * 76)
    shortcut = np.array([[0.0 if quoted[j] == (visible(fables[i][1])[-1:] in ([":"], [","])) else -1.0
                          for j in range(len(fables))] for i in range(len(fables))])
    print(f"  references (no model): word overlap {match_rate(ov, same):.3f} on same-format pairs, "
          f"{match_rate(ov, noclue):.3f} on no-clue; punctuation shortcut {match_rate(shortcut, same):.3f} on same-format")
    print(f"  {'set':17s} {'same-format':>11s} {'runs':>15s} {'p vs 50%':>9s} {'no-clue':>8s} {'p':>7s} "
          f"{'unknown':>8s} {'held-out':>9s}")
    pvals = {}
    for name, L in avg.items():
        a, pa = chance_p(L, fables, ov, quoted, "same", rng)
        b, pb = chance_p(L, fables, ov, quoted, "noclue", rng)
        pvals[name] = (pa, pb)
        each = ", ".join(f"{match_rate(x, same):.3f}" for x in runs[name][0])
        unk = np.mean([r["unknown_word_rate"] for r in runs[name][1]])
        held = np.mean([r["heldout_loss"] for r in runs[name][1]])
        print(f"  {name:17s} {a:11.3f} {each:>15s} {pa:9.4f} {b:8.3f} {pb:7.4f} {unk:8.1%} {held:9.3f}")

    def compare(a, b, label, need_seeds=True):
        if a not in avg or b not in avg:
            return None
        d, p = paired_p(avg[a], avg[b], same, rng)
        seed_ok = all(match_rate(x, same) > match_rate(y, same) for x, y in zip(runs[a][0], runs[b][0]))
        ok = p < 0.05 and (seed_ok or not need_seeds)
        extra = f", wins in every seed-matched pair: {'yes' if seed_ok else 'no'}" if need_seeds else ""
        print(f"  {label}: {a} - {b} = {d:+.3f}  (p = {p:.4f}{extra})  -> {'CONFIRMED' if ok else 'NOT CONFIRMED'}")
        return ok

    print("\n  PRE-REGISTERED VERDICT")
    if "stories" in pvals:
        print(f"  P1  sanity, stories beat 50%: {'CONFIRMED' if pvals['stories'][0] < 0.05 else 'NOT CONFIRMED'} "
              f"(p = {pvals['stories'][0]:.4f})")
    compare("stories", "novels", "P2 ")
    compare("stories", "stories_shuffled", "P2b")
    if "stories" in pvals:
        print(f"  P3  stories beat 50% on no-clue pairs: "
              f"{'CONFIRMED' if pvals['stories'][1] < 0.05 else 'NOT CONFIRMED (inconclusive, low power)'} "
              f"(p = {pvals['stories'][1]:.4f})")
    print("\n  SECONDARY")
    compare("stories", "bible", "S1 ", need_seeds=False)
    compare("narrative", "rules", "S2 ", need_seeds=False)


if __name__ == "__main__":
    main()
