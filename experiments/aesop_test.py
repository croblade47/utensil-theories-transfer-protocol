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

VERSION 3: second pre-run review, still BEFORE any training
-----------------------------------------------------------
- Shuffled control now shuffles sentences only WITHIN blocks of 10 consecutive
  paragraphs. Each story keeps its words, characters and topic, but the order
  of events is broken. (v2 shuffled across the whole corpus, which also
  destroyed topic, so word copying alone would have beaten it.) The held-out
  split happens before shuffling, so stories and shuffled train on the same text.
- Training-run luck now counts: stories, novels and stories_shuffled get 4 seeds
  each, and comparisons need a model-level permutation test (4 vs 4) as well
  as the fable-level test.
- The fable-level comparison test double-centres each matrix first. That
  removes each model's general preference for some morals, which made v2 too
  strict.
- The "no word clue" mask uses related word forms (shared first 4 letters, or
  one word a prefix of the other), so safe/safety and enemy/enemies count as
  clues. Its null keeps the observed mask fixed (the strict direction).
- Sentence splitting keeps closing quotes; a garbled "WARRA WARRA" run is removed.

Training sets (same tiny transformer; main sets matched at ~714k tokens):
  stories           folk tales and myths from 9 cultures, no Aesop
  stories_shuffled  the same, with sentences shuffled inside each 10-paragraph block (control)
  novels            Austen, Chesterton, Melville: coherent prose, fewer explicit
                    lessons, a different world (control for style)
  bible             King James Bible, whole chapters sampled to the same size
  rules             Bible rule verses + Proverbs + Ecclesiastes + Tao Te Ching (small)
  narrative         KJV narrative chapters without rule verses, same size as rules

PRE-REGISTERED (v3, committed before any training on these sets)
  All scores use same-format pairs.
  P1  sanity check: each set beats 50% (permutation test). Expected to pass,
      because word overlap alone scores well above 50%.
  P2  stories > novels: CONFIRMED only if BOTH
        (a) fable-level paired row-swap permutation (double-centred) p < 0.05, and
        (b) model-level permutation over the 4 + 4 trained models p < 0.05
  P2b stories > stories_shuffled: same rule
      P2 and P2b both confirmed = evidence that story structure, not just
      vocabulary or setting, carries the lessons.
  P3  stories beats 50% on no-word-clue pairs (fixed observed mask), p < 0.05.
      A null here means "inconclusive, low power", not "no comprehension".
      Reported beside it: the same rate for novels and stories_shuffled, and
      stories vs novels on those pairs.
  S1  stories vs bible (descriptive; 2 seeds; unknown-word rates alongside)
  S2  narrative > rules (descriptive; 1 seed; note: rules include Legge's Tao,
      not only KJV)
  Every comparison is also printed as a difference beside the largest
  same-set gap between seeds, so small effects can be judged against noise.

Run:  python experiments/aesop_test.py      (about 3 hours on 4 CPU cores)
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
SEEDS = {"stories": [0, 1, 2, 3], "novels": [0, 1, 2, 3], "stories_shuffled": [0, 1, 2, 3],
         "bible": [0, 1], "rules": [0], "narrative": [0]}
BLOCK = 10                           # paragraphs per shuffle block
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
    body = re.sub(r"(WARRA\s*)+", "", body)            # garbled run in The Wolf and the Lamb
    parts = re.split(r"\n\n\n {0,2}([A-Z][^\n]+)\n\n\n", "\n\n\n" + body)
    out = []
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", parts[i + 1]) if p.strip()]
        if len(paras) >= 2 and len(paras[-1].split()) <= 20 and not (exclude and title in EXCLUDE):
            out.append((title, " ".join(paras[:-1]), paras[-1]))
    return out


_ROOM = None


def room():
    """Fable tokens the model sees: the window minus the longest moral and two boundaries."""
    global _ROOM
    if _ROOM is None:
        _ROOM = tt.CTX - max(len(tt.tok(m)) for _, _, m in aesop_fables(exclude=False)) - 2
    return _ROOM


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


SENTENCE_END = re.compile(r"(?<=[.!?][\"'\u2019\u201d])\s+|(?<=[.!?])\s+")


def shuffle_within_blocks(units, seed, block=BLOCK):
    """Same sentences and unit sizes; sentences shuffled only inside each block of paragraphs,
    so each story keeps its words, characters and topic but loses the order of events."""
    rng = random.Random(seed)
    out = []
    for b in range(0, len(units), block):
        split = [SENTENCE_END.split(u) for u in units[b:b + block]]
        pool = [x for ss in split for x in ss]
        rng.shuffle(pool)
        k = 0
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

    sets = {k: split_heldout(v) for k, v in
            {"stories": stories, "novels": novels, "bible": bible, "rules": rules, "narrative": narrative}.items()}
    s_train, s_held = sets["stories"]
    sets["stories_shuffled"] = (shuffle_within_blocks(s_train, CORPUS_SEED), s_held)
    return sets


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


def content_words(tokens):
    return {w for w in tokens if w.isalpha() and w not in STOP and len(w) > 2}


def related(a, b):
    """Same word family: shared first 4 letters, or one word is a prefix of the other."""
    return a[:4] == b[:4] or a.startswith(b) or b.startswith(a)


def overlap_matrix(fables):
    Fs = [content_words(visible(f)) for _, f, _ in fables]
    Ms = [content_words(tt.tok(m)) for _, _, m in fables]
    return np.array([[sum(any(related(m, w) for w in Fs[i]) for m in Ms[j]) / max(1, len(Ms[j]))
                      for j in range(len(fables))] for i in range(len(fables))])


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
    """Permutation test vs chance. Same-format: mask recomputed per permuted assignment.
    No-clue: the observed mask is kept fixed (exact for a no-information model, strict otherwise)."""
    same0, noclue0 = masks(fables, ov, quoted)
    obs = match_rate(L, same0 if which == "same" else noclue0)
    hits = 0
    for _ in range(PERMUTATIONS):
        p = rng.permutation(len(fables))
        m = masks(fables, ov, quoted, p)[0] if which == "same" else noclue0
        hits += match_rate(L[:, p], m) >= obs
    return obs, (1 + hits) / (1 + PERMUTATIONS)


def paired_p(La, Lb, mask, rng):
    """One-sided paired row-swap permutation test: is model A better than model B?
    Each matrix is double-centred first; this leaves every within-model pair outcome unchanged
    but removes each model's general preference for some morals before rows are swapped."""
    c = lambda L: L - L.mean(0, keepdims=True) - L.mean(1, keepdims=True) + L.mean()
    La, Lb = c(La), c(Lb)
    obs = match_rate(La, mask) - match_rate(Lb, mask)
    hits = 0
    for _ in range(PERMUTATIONS):
        s = rng.random(La.shape[0]) < 0.5
        Xa, Xb = np.where(s[:, None], Lb, La), np.where(s[:, None], La, Lb)
        hits += match_rate(Xa, mask) - match_rate(Xb, mask) >= obs
    return obs, (1 + hits) / (1 + PERMUTATIONS)

def model_level_p(rates_a, rates_b):
    """Exact permutation over trained models: is set A's mean rate above set B's?"""
    from itertools import combinations
    allr, na = list(rates_a) + list(rates_b), len(rates_a)
    obs = np.mean(rates_a) - np.mean(rates_b)
    diffs = [np.mean([allr[i] for i in c]) - np.mean([allr[i] for i in range(len(allr)) if i not in c])
             for c in combinations(range(len(allr)), na)]
    return float(np.mean([d >= obs - 1e-12 for d in diffs]))

# ---------------------------------------------------------------------------

def result_key(name, seed, train_units, steps):
    return f"{name}/seed{seed}/{corpus_hash(train_units)}/ctx{tt.CTX}/steps{steps}"


def plan_runs():
    """Seeds 0-1 of every main set first (so an early look is possible), then seeds 2-3, then the small sets."""
    first = [(c, s) for s in (0, 1) for c in MAIN if s in SEEDS[c]]
    later = [(c, s) for s in (2, 3) for c in MAIN if s in SEEDS[c]]
    return first + later + [(c, 0) for c in SMALL]


def main():
    fables = aesop_fables()
    titles = [t for t, _, _ in fables]
    corpora = build_corpora()
    ov, quoted = overlap_matrix(fables), quoted_flags(fables)
    same, noclue = masks(fables, ov, quoted)
    print(f"Aesop fables in test: {len(fables)} (excluded {len(EXCLUDE)} for leakage); "
          f"same-format pairs {int(same.sum() // 2):,}; no-clue pairs {int(noclue.sum() // 2):,}")
    for k, (tr, he) in corpora.items():
        print(f"  corpus {k:17s} train {size(tr):>9,} tokens  held-out {size(he):>7,}  [{corpus_hash(tr)}]")
    main_tokens = size(corpora["stories"][0])

    results = json.loads(OUT.read_text()) if OUT.exists() else {}
    for name, seed in plan_runs():
        train_units, held = corpora[name]
        steps = steps_for(name, train_units, main_tokens)
        key = result_key(name, seed, train_units, steps)
        if key in results and results[key].get("titles") == titles:
            continue
        vocab = tt.Vocab(train_units)
        path = MODELS / f"aesop3_{name}_seed{seed}_{corpus_hash(train_units)}_steps{steps}.pt"
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
        print(f"  {name}/seed{seed}: same-format match {match_rate(L, same):.3f}  no-clue {match_rate(L, noclue):.3f}  "
              f"unknown {r['unknown_word_rate']:.1%}  held-out loss {r['heldout_loss']}  fable loss {r['fable_loss']}",
              flush=True)

    analyse(results, fables, corpora)


def analyse(results, fables, corpora):
    titles = [t for t, _, _ in fables]
    ov, quoted = overlap_matrix(fables), quoted_flags(fables)
    same, noclue = masks(fables, ov, quoted)
    main_tokens = size(corpora["stories"][0])
    runs = {}                                   # name -> {seed: result}
    for name in MAIN + SMALL:
        tr = corpora[name][0]
        steps = steps_for(name, tr, main_tokens)
        got = {s: results[result_key(name, s, tr, steps)] for s in SEEDS[name]
               if result_key(name, s, tr, steps) in results
               and results[result_key(name, s, tr, steps)]["titles"] == titles}
        if got:
            runs[name] = got
    Ls = {k: {s: np.array(r["L"]) for s, r in v.items()} for k, v in runs.items()}
    avg = {k: np.mean(list(v.values()), 0) for k, v in Ls.items()}
    rate = lambda name, mask: {s: match_rate(L, mask) for s, L in Ls[name].items()}
    gap = lambda name, mask: (max(rate(name, mask).values()) - min(rate(name, mask).values())) if len(Ls[name]) > 1 else float("nan")
    rng = np.random.default_rng(0)

    print("\n" + "=" * 78)
    print(f"AESOP MORAL TEST  ({len(fables)} fables never seen in training; 50% = guessing)")
    print("=" * 78)
    shortcut = np.array([[0.0 if quoted[j] == (visible(fables[i][1])[-1:] in ([":"], [","])) else -1.0
                          for j in range(len(fables))] for i in range(len(fables))])
    print(f"  pairs: same-format {int(same.sum() // 2):,}, no word clue {int(noclue.sum() // 2):,}")
    print(f"  references (no model): word-family overlap {match_rate(ov, same):.3f} same-format / "
          f"{match_rate(ov, noclue):.3f} no-clue; punctuation shortcut {match_rate(shortcut, same):.3f} same-format")
    print(f"\n  {'set':17s} {'same-format':>11s}  {'per seed':30s} {'p vs 50%':>8s} {'no-clue':>8s} {'p':>7s} "
          f"{'unknown':>8s} {'held-out':>8s}")
    pv = {}
    for name in avg:
        a, pa = chance_p(avg[name], fables, ov, quoted, "same", rng)
        b, pb = chance_p(avg[name], fables, ov, quoted, "noclue", rng)
        pv[name] = (pa, pb)
        each = ", ".join(f"{x:.3f}" for x in rate(name, same).values())
        unk = np.mean([r["unknown_word_rate"] for r in runs[name].values()])
        held = np.mean([r["heldout_loss"] for r in runs[name].values()])
        print(f"  {name:17s} {a:11.3f}  {each:30s} {pa:8.4f} {b:8.3f} {pb:7.4f} {unk:8.1%} {held:8.3f}")

    def compare(a, b, label, mask=same, strict=True):
        if a not in avg or b not in avg:
            print(f"  {label}: missing results")
            return
        d, pf = paired_p(avg[a], avg[b], mask, rng)
        ra, rb = list(rate(a, mask).values()), list(rate(b, mask).values())
        pm = model_level_p(ra, rb) if len(ra) > 1 and len(rb) > 1 else float("nan")
        gaps = [g for g in (gap(a, mask), gap(b, mask)) if not np.isnan(g)]
        noise = max(gaps) if gaps else float("nan")
        line = (f"  {label}: {a} - {b} = {d:+.3f}  (largest seed-to-seed gap {noise:.3f}); "
                f"fable-level p = {pf:.4f}, model-level p = {pm:.4f}")
        if strict:
            ok = pf < 0.05 and pm < 0.05
            line += f"  -> {'CONFIRMED' if ok else 'NOT CONFIRMED'}"
        print(line)

    print("\n  PRE-REGISTERED VERDICT")
    for name in avg:
        if name in MAIN:
            print(f"  P1  {name} beats 50%: {'yes' if pv[name][0] < 0.05 else 'no'} (p = {pv[name][0]:.4f})")
    compare("stories", "novels", "P2 ")
    compare("stories", "stories_shuffled", "P2b")
    if "stories" in pv:
        print(f"  P3  stories beat 50% on no-clue pairs: "
              f"{'CONFIRMED' if pv['stories'][1] < 0.05 else 'NOT CONFIRMED (inconclusive, low power)'} "
              f"(p = {pv['stories'][1]:.4f})")
    print("\n  DESCRIPTIVE")
    compare("stories", "novels", "P3 context, no-clue pairs: stories vs novels  ", mask=noclue, strict=False)
    compare("stories", "stories_shuffled", "P3 context, no-clue pairs: stories vs shuffled", mask=noclue, strict=False)
    compare("stories", "bible", "S1 ", strict=False)
    compare("narrative", "rules", "S2 ", strict=False)


if __name__ == "__main__":
    main()
