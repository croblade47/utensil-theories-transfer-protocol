"""
The ladder of greenhouses: understanding measured as compression, with REAL exact seeds
=======================================================================================

The owner's picture
-------------------
"As if I was given you instructions to find the soil needed and to build a greenhouse,
I told you the humidity and I explained the rotation of the sun. We checked the air
inside of it and checked to ensure the microbial and bugs were thriving within it.
Then I gave you a seed and told you to grow it."

What we test: understanding and compression are two sides of one thing. If two people
already share knowledge (a "greenhouse"), a sender only has to send what the receiver
could NOT have guessed (the surprise). The better the shared understanding, the smaller
the seed that regrows the exact message. So: better understanding = smaller exact seed.

How the metaphor maps onto this script
--------------------------------------
  SOIL        the training verses of the King James Bible (every verse except every
              50th). Every greenhouse below is built ONLY from this soil.
  THE PLANT   H, the held-out verses (every 50th verse, 623 verses) that no model or
              word list ever saw. Every rung must regrow H byte for byte.
  HUMIDITY AND THE SUN'S ROTATION
              the fixed, shared grow instructions, the same on both sides and NOT in
              the seed: the normalisation rule, the arithmetic coder, the probability
              rounding rule (freq = max(1, floor(p * 2**20))), the 64-token window,
              the split of H into 12 segments, the letter speller for unknown words.
  THE GREENHOUSE
              the shared knowledge both sides keep in advance (a word list, word
              counts, a trained model). It is NOT counted in the seed, exactly like a
              dictionary both people already own. Its size is printed for honesty:
              a greenhouse is worth building only if it is reused for many messages.
  THE SEED    the bitstream. It carries only what the greenhouse could not predict.
  CHECKING THE AIR AND THE BUGS
              the checks: we decode for real, token by token, from the seed bytes plus
              the greenhouse, and compare with H byte for byte (and by SHA-256).

The rungs (each one = more shared understanding inside the greenhouse)
  R0  no greenhouse, no seed trick: send every letter as it is (8 bits per character).
  R1  zip (zlib level 9) and xz (preset 9 + extreme): the seed has to carry its own tiny
      greenhouse, because these learn only from the message itself.
  R2  zip with a shared library: both sides keep the last 32 KB of the training text as
      a zlib preset dictionary. The owner's "strawberry / orange library" idea in its
      plainest form: shared pieces the message can point back to.
  R3  knowing the NAMES of the plants: a shared word list only (every training word
      equally likely, plus an escape for unknown words).
  R4  knowing how COMMON each plant is: word frequencies (add-one smoothing).
  R5  knowing which plant grows NEXT TO which: word pairs (bigram, Witten-Bell
      interpolation with R4; no settings to tune).
  R6  a gardener who studied the whole field: the tiny transformer trained on the plain
      Bible (baseline), 3 training seeds.
  R7  gardeners trained with the owner's ideas, and the control: shifting (the owner's
      shifting word), label (plain per-verse good/bad label), carry3 (carried balance,
      3 spellings), scrambled (random spellings: the control). 3 seeds each.
  R8  "the greenhouse built gradually": the baseline seed-0 gardener allowed to see only
      the last k tokens (k = 1, 2, 4, 8, 16, 64), like instructions given step by step.

The text H (the same for every rung, so the comparison is fair)
  verses = load_verses(); texts = [t for _, t in verses]
  held   = [texts[i] for i in range(0, len(texts), 50)]
  each verse -> " ".join(tiny_transformer.tok(verse)), verses joined with "\n".
  Capitals and verse numbers (and apostrophes, hyphens etc.) are dropped for EVERY rung
  alike; the models only ever saw this form.

How the exact seeds are made (R3 to R8)
  * H is split into 12 contiguous groups of verses (fixed rule from the verse count N).
    Each group is one token stream laid out exactly as in training (tiny_transformer.
    stream): token 1 (<v>) before each verse; for marker models the marker word comes
    first in each verse, as in training. A final token 1 closes each group.
    The very first <v> of a group is implied (not coded).
  * At each step the 12 groups advance together: one batched model call on the 12
    windows (the last <= 64 tokens of each group), then one token per group is coded.
    The decoder makes the identical call on the identical windows, so its probabilities
    are bit-for-bit the same. This is what makes the regrowth exact.
  * Probabilities -> integer frequencies: freq = max(1, floor(p * 2**20)), computed in
    float64 numpy from the model's float32 logits, identically on both sides.
  * An exact integer arithmetic coder (Witten-Neal-Cleary style, 62-bit registers, Python
    big ints) turns the frequencies into bits; the decoder inverts it.
  * Unknown words: the model codes <unk> (token 0), then the word is spelled with a fixed
    letter coder (26 letters + end mark, each 1/27). These letters ARE in the seed.
  * Seed file = 4-byte header (N, the number of verses) + the coder's bytes.
    bits per character (bpc) = seed file bits / characters of H.

Marker models (shifting, label, carry3, scrambled)
  They were trained with a marker word in front of each verse. Each held-out verse gets
  the marker the project's own marking rule gives it (the same marked text the model was
  trained from: shifting_word.mark_up / method_comparison.mark_label / mark_carry3; the
  scrambled seed-s model uses scramble seed s, as in confirm.py).
  (a) TOTAL:      the marker tokens are coded by the model and paid for in the seed.
                  This is the real, decoded seed. Fair and conservative.
  (b) WORDS ONLY: the cost of everything except the markers (verse words, spelled
                  unknown words and verse ends), given the marker. This is an
                  accounting number from the same probabilities, NOT a stand-alone seed:
                  a decoder would need the markers from somewhere else.
  Caveat: the project's word values that choose the markers (shifting_word.word_values)
  were computed by the earlier experiments from ALL verses, including the held-out ones.
  We keep that rule unchanged because the models were trained with it. It can only
  matter for (b); in (a) every marker is paid for.

PRE-REGISTRATION (written into this file before any rung was run on H)
----------------------------------------------------------------------
  MAIN QUESTION: does the shifting-word model regrow the held-out verses with a smaller
  TOTAL seed than the baseline model?
  Measure: per held-out verse, the TOTAL code length in bits (marker + words + verse end;
  ideal lengths -log2(freq/total) of the same quantised probabilities the coder uses),
  averaged over the 3 seeds of each method. d_v = shifting_v - baseline_v.
  Test: one-sided paired permutation (sign-flip) test on the mean of d_v,
  100,000 random flips, numpy default_rng(0). CONFIRMED if p < 0.05 and the mean of d_v
  is below 0. The one-sided sign test over verses is reported alongside; if the two
  tests disagree we say so.
  Everything else is DESCRIPTIVE: WORDS ONLY; label, carry3 and scrambled vs baseline;
  shifting vs scrambled and shifting vs label; all of R0-R5 and R8.
  Nothing is tuned on the held-out verses: all settings above are fixed in advance,
  the models were trained days ago, and the --dev mode below uses TRAINING verses only.

Run (from experiments/):
  python understanding_compression.py          # full run, about 30-45 minutes
  python understanding_compression.py --dev    # quick self-test on 40 TRAINING verses
Writes results_understanding.json and results_understanding.txt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import math
import os
import sys
import tempfile
import time
import zlib
from collections import Counter, defaultdict
from math import comb
from pathlib import Path

import numpy as np
import torch

import method_comparison as mc
import shifting_word as sw
import tiny_transformer as tt
from bible_understanding import load_verses

torch.set_num_threads(2)     # another job shares this 4-CPU machine (tiny_transformer sets 4)

HERE = Path(__file__).parent
MODELS = HERE / "models"
SEEDS = [0, 1, 2]
STEPS = 1500
METHODS = ["baseline", "shifting", "label", "carry3", "scrambled"]
MARKED = ["shifting", "label", "carry3", "scrambled"]
SEGMENTS = 12                 # fixed grow instruction: H is coded as 12 groups side by side
QBITS = 20                    # probability rounding: freq = max(1, floor(p * 2**QBITS))
LETTERS = "abcdefghijklmnopqrstuvwxyz"
END_LETTER = 26               # 27th symbol of the letter speller = end of word
HEADER_BYTES = 4              # N, the number of verses
K_LADDER = [1, 2, 4, 8, 16, 64]
N_PERM = 100_000
DECODE_BUDGET_S = 40 * 60     # optional decodes (label, carry3, scrambled) only while under 40 min


def norm(verse: str) -> str:
    """Exactly what the models see: lowercase words and . , ; : ? ! separated by spaces."""
    return " ".join(tt.tok(verse))


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

# ---------------------------------------------------------------------------
# The exact integer arithmetic coder (the "seed packer" and the "seed grower")
# ---------------------------------------------------------------------------

PREC = 62
FULL = 1 << PREC
HALF = FULL >> 1
QUARTER = FULL >> 2


class Encoder:
    """Witten-Neal-Cleary arithmetic coder with exact integers (Python big ints)."""

    def __init__(self):
        self.low, self.high, self.pending = 0, FULL - 1, 0
        self.bits = []

    def _emit(self, bit):
        self.bits.append(bit)
        self.bits.extend([1 - bit] * self.pending)
        self.pending = 0

    def encode(self, lo, hi, total):
        """Code a symbol that owns the integer slice [lo, hi) of [0, total)."""
        rng = self.high - self.low + 1
        self.high = self.low + rng * hi // total - 1
        self.low = self.low + rng * lo // total
        while True:
            if self.high < HALF:
                self._emit(0)
            elif self.low >= HALF:
                self._emit(1)
                self.low -= HALF
                self.high -= HALF
            elif self.low >= QUARTER and self.high < 3 * QUARTER:
                self.pending += 1
                self.low -= QUARTER
                self.high -= QUARTER
            else:
                break
            self.low = 2 * self.low
            self.high = 2 * self.high + 1

    def finish(self) -> bytes:
        self.pending += 1
        self._emit(0 if self.low < QUARTER else 1)
        n_bits = len(self.bits)
        return np.packbits(np.array(self.bits, dtype=np.uint8)).tobytes(), n_bits


class Decoder:
    """Reads the seed bits back; bits past the end are read as 0 (as the encoder assumes)."""

    def __init__(self, data: bytes):
        self.bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8)).tolist()
        self.i = 0
        self.low, self.high, self.value = 0, FULL - 1, 0
        for _ in range(PREC):
            self.value = 2 * self.value + self._bit()

    def _bit(self):
        b = self.bits[self.i] if self.i < len(self.bits) else 0
        self.i += 1
        return b

    def target(self, total):
        rng = self.high - self.low + 1
        return ((self.value - self.low + 1) * total - 1) // rng

    def consume(self, lo, hi, total):
        rng = self.high - self.low + 1
        self.high = self.low + rng * hi // total - 1
        self.low = self.low + rng * lo // total
        while True:
            if self.high < HALF:
                pass
            elif self.low >= HALF:
                self.low -= HALF
                self.high -= HALF
                self.value -= HALF
            elif self.low >= QUARTER and self.high < 3 * QUARTER:
                self.low -= QUARTER
                self.high -= QUARTER
                self.value -= QUARTER
            else:
                break
            self.low = 2 * self.low
            self.high = 2 * self.high + 1
            self.value = 2 * self.value + self._bit()

# ---------------------------------------------------------------------------
# Greenhouses ("predictors"): each turns windows of earlier tokens into integer
# frequencies for the next token. Same function, same input -> same integers.
# ---------------------------------------------------------------------------

def quantise(p: np.ndarray) -> np.ndarray:
    """Probabilities (float64) -> integer frequencies, the same on both sides."""
    return np.maximum(1, np.floor(p * float(1 << QBITS))).astype(np.int64)


class Uniform:
    """R3: a shared word list; every word (and the <v> and <unk> escape) equally likely."""

    def __init__(self, n_vocab):
        self.row = np.ones(n_vocab, dtype=np.int64)
        self.k = 1

    def freqs(self, windows):
        return np.tile(self.row, (len(windows), 1))


class Unigram:
    """R4: word frequencies from the training stream, add-one smoothing (exact integers)."""

    def __init__(self, vocab, train_texts):
        c = np.bincount(tt.stream(vocab, train_texts).numpy(), minlength=len(vocab))
        self.row = (c + 1).astype(np.int64)
        self.p = self.row / self.row.sum()
        self.k = 1

    def freqs(self, windows):
        return np.tile(self.row, (len(windows), 1))


class Bigram:
    """R5: word pairs. P(w|h) = (c(h,w) + T(h) * P_uni(w)) / (c(h) + T(h))  (Witten-Bell)."""

    def __init__(self, vocab, train_texts, unigram: Unigram):
        ids = tt.stream(vocab, train_texts).numpy()
        pairs = Counter(zip(ids[:-1].tolist(), ids[1:].tolist()))
        self.follow = defaultdict(dict)
        for (h, w), n in pairs.items():
            self.follow[h][w] = n
        self.p_uni = unigram.p
        self.cache = {}
        self.k = 1

    def row(self, h):
        if h not in self.cache:
            f = self.follow.get(h, {})
            c_h, t_h = sum(f.values()), len(f)
            if c_h == 0:
                p = self.p_uni.copy()
            else:
                p = t_h * self.p_uni
                ws = np.fromiter(f.keys(), dtype=np.int64)
                p[ws] += np.fromiter(f.values(), dtype=np.float64)
                p /= (c_h + t_h)
            self.cache[h] = quantise(p)
        return self.cache[h]

    def freqs(self, windows):
        return np.stack([self.row(w[-1]) for w in windows])


class Neural:
    """R6-R8: a trained tiny transformer that sees the last k (<= 64) tokens."""

    def __init__(self, model, k=tt.CTX):
        self.model, self.k = model, k

    @torch.no_grad()
    def freqs(self, windows):
        x = torch.tensor(windows, dtype=torch.long)
        m, T = self.model, x.shape[1]
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool), 1)
        h = m.tok(x) + m.pos(torch.arange(T))          # positions 0..T-1, as in training
        for b in m.blocks:
            h = b(h, mask)
        logits = m.head(m.ln(h[:, -1])).double().numpy()   # only the next-token row is needed
        logits -= logits.max(1, keepdims=True)
        e = np.exp(logits)
        return quantise(e / e.sum(1, keepdims=True))

# ---------------------------------------------------------------------------
# Laying out the message and running the coder
# ---------------------------------------------------------------------------

def segment_bounds(n_verses):
    return [(j * n_verses // SEGMENTS, (j + 1) * n_verses // SEGMENTS) for j in range(SEGMENTS)]


def layout(held_norm, vocab, markers=None):
    """Per segment: the list of verses; each verse = list of (token id, spelled word or None,
    kind) with kind 'm' (marker) or 'w' (word). The verse end (token 1) is added by the coder."""
    segs = []
    for a, b in segment_bounds(len(held_norm)):
        verses = []
        for v in range(a, b):
            items = []
            if markers is not None:
                items.append((vocab.stoi[markers[v]], None, "m"))
            for w in held_norm[v].split(" ") if held_norm[v] else []:
                i = vocab.stoi.get(w, 0)
                items.append((i, w if i == 0 else None, "w"))
            verses.append(items)
        segs.append(verses)
    return segs


def run_coder(pred, n_verses, segs=None, seed=None, has_marker=False):
    """ENCODE when `segs` is given (returns seed bytes and per-verse bits);
    DECODE when `seed` is given (returns the regrown token layout).
    Both directions walk exactly the same steps and make exactly the same model calls."""
    encoding = segs is not None
    bounds = segment_bounds(n_verses)
    n_in_seg = [b - a for a, b in bounds]
    coder = Encoder() if encoding else Decoder(seed[HEADER_BYTES:])
    hist = [[1] for _ in range(SEGMENTS)]               # the implied first <v> of each group
    out = [[[]] if n_in_seg[j] else [] for j in range(SEGMENTS)]   # decoded verses per group
    vi = [0] * SEGMENTS                                 # verse index inside the group
    ti = [0] * SEGMENTS                                 # token index inside the verse
    bits = {"m": np.zeros(n_verses), "w": np.zeros(n_verses), "e": np.zeros(n_verses)}
    active = [j for j in range(SEGMENTS) if n_in_seg[j] > 0]
    while active:
        L = min(len(hist[active[0]]), pred.k)
        windows = [hist[j][-L:] for j in active]
        assert all(len(w) == L for w in windows)
        freq = pred.freqs(windows)
        cum = np.zeros((len(active), freq.shape[1] + 1), dtype=np.int64)
        np.cumsum(freq, axis=1, out=cum[:, 1:])
        still = []
        for r, j in enumerate(active):
            c = cum[r]
            total = int(c[-1])
            g = bounds[j][0] + vi[j]                    # global verse number
            if encoding:
                verse = segs[j][vi[j]]
                if ti[j] < len(verse):
                    tok, word, kind = verse[ti[j]]
                else:
                    tok, word, kind = 1, None, "e"      # verse end (or group end)
                coder.encode(int(c[tok]), int(c[tok + 1]), total)
            else:
                t = coder.target(total)
                tok = int(np.searchsorted(c, t, side="right")) - 1
                coder.consume(int(c[tok]), int(c[tok + 1]), total)
                word = None
                if tok == 1:
                    kind = "e"
                elif has_marker and ti[j] == 0:
                    kind = "m"
                else:
                    kind = "w"
            b = math.log2(total / int(freq[r, tok]))
            if tok == 0:                                # unknown word: spell it, 27 symbols each 1/27
                if encoding:
                    for ch in word:
                        coder.encode(LETTERS.index(ch), LETTERS.index(ch) + 1, 27)
                    coder.encode(END_LETTER, END_LETTER + 1, 27)
                else:
                    letters = []
                    while True:
                        s = coder.target(27)
                        coder.consume(s, s + 1, 27)
                        if s == END_LETTER:
                            break
                        letters.append(LETTERS[s])
                    word = "".join(letters)
                b += math.log2(27) * (len(word) + 1)
            bits[kind][g] += b
            hist[j].append(tok)
            if tok == 1:                                # verse finished
                vi[j] += 1
                ti[j] = 0
                if vi[j] < n_in_seg[j]:
                    out[j].append([])
                    still.append(j)
            else:
                out[j][-1].append((tok, word))
                ti[j] += 1
                still.append(j)
        active = still
    if encoding:
        data, n_bits = coder.finish()
        return n_verses.to_bytes(HEADER_BYTES, "big") + data, n_bits, bits
    return out


def regrow_text(out, itos, has_marker):
    """Decoded tokens -> the exact normalised text H."""
    lines = []
    for verses in out:
        for verse in verses:
            toks = verse[1:] if has_marker else verse
            lines.append(" ".join(w if t == 0 else itos[t] for t, w in toks))
    return "\n".join(lines)


def code_one(name, pred, held_norm, vocab, markers, H, decode, log):
    """Encode, optionally decode for real, check byte-for-byte equality."""
    t0 = time.time()
    segs = layout(held_norm, vocab, markers)
    seed, n_bits, bits = run_coder(pred, len(held_norm), segs=segs)
    t_enc = time.time() - t0
    res = {"seed_bytes": len(seed), "coder_bits": n_bits, "seed_sha256": sha(seed),
           "ideal_bits": float(sum(v.sum() for v in bits.values())),
           "marker_bits": float(bits["m"].sum()),
           "per_verse_total": np.round(bits["m"] + bits["w"] + bits["e"], 4).tolist(),
           "per_verse_words": np.round(bits["w"] + bits["e"], 4).tolist(),
           "encode_s": round(t_enc, 1), "decoded": False, "exact": None}
    if decode:
        t1 = time.time()
        n = int.from_bytes(seed[:HEADER_BYTES], "big")
        out = run_coder(pred, n, seed=seed, has_marker=markers is not None)
        text = regrow_text(out, vocab.itos, markers is not None)
        res.update(decoded=True, exact=text.encode() == H.encode(),
                   regrown_sha256=sha(text.encode()), decode_s=round(time.time() - t1, 1))
    log(f"  {name:22s} seed {res['seed_bytes']:7,d} B  "
        f"({8 * res['seed_bytes'] / len(H):.3f} bpc)  "
        f"ideal {res['ideal_bits'] / 8:9,.0f} B  "
        f"{'decoded, EXACT' if res['exact'] else ('decoded, MISMATCH' if res['decoded'] else 'encoded only')}"
        f"  ({res['encode_s']:.0f}s{'+%.0fs' % res['decode_s'] if res['decoded'] else ''})")
    return res

# ---------------------------------------------------------------------------
# Statistics (paired over verses)
# ---------------------------------------------------------------------------

def sign_test(d):
    """d < 0 means the method needs fewer bits. One-sided p for 'method smaller'."""
    wins, losses = int((d < 0).sum()), int((d > 0).sum())
    n = wins + losses
    p1 = sum(comb(n, i) for i in range(wins, n + 1)) / 2 ** n if n else 1.0
    p_low = sum(comb(n, i) for i in range(0, wins + 1)) / 2 ** n if n else 1.0
    return wins, losses, p1, min(1.0, 2 * min(p1, p_low))


def perm_test(d, n_perm=N_PERM):
    """Paired sign-flip permutation test on the mean of d (one-sided: mean < 0; two-sided)."""
    rng = np.random.default_rng(0)
    obs = d.mean()
    le = ge_abs = 0
    for start in range(0, n_perm, 10_000):
        m = min(10_000, n_perm - start)
        flips = rng.integers(0, 2, size=(m, len(d))) * 2 - 1
        perm = (flips * d).mean(1)
        le += int((perm <= obs).sum())
        ge_abs += int((np.abs(perm) >= abs(obs)).sum())
    return (le + 1) / (n_perm + 1), (ge_abs + 1) / (n_perm + 1)


def compare(a, b):
    d = np.asarray(a) - np.asarray(b)
    wins, losses, s1, s2 = sign_test(d)
    p1, p2 = perm_test(d)
    return {"mean_diff_bits_per_verse": float(d.mean()), "total_diff_bits": float(d.sum()),
            "verses_smaller": wins, "verses_larger": losses, "ties": int((d == 0).sum()),
            "sign_p_one_sided": s1, "sign_p_two_sided": s2,
            "perm_p_one_sided": p1, "perm_p_two_sided": p2}

# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev", action="store_true",
                    help="self-test on 40 TRAINING verses (never the held-out ones)")
    args = ap.parse_args()
    T0 = time.time()
    script_sha = sha(Path(__file__).read_bytes())
    lines = []

    def log(s=""):
        print(s, flush=True)
        lines.append(s)

    verses = load_verses()
    texts = [t for _, t in verses]
    pool = [i for i in range(len(texts)) if i % 50]
    held_idx = list(range(0, len(texts), 50))
    if args.dev:                       # training verses only: checks the machinery, peeks at nothing
        held_idx = [i for i in range(1, len(texts), 50)][:40]
    held_norm = [norm(texts[i]) for i in held_idx]
    H = "\n".join(held_norm)
    n_chars = len(H)
    raw_bits = 8 * n_chars
    assert H.isascii()
    train_norm = "\n".join(norm(texts[i]) for i in pool)

    log("THE LADDER OF GREENHOUSES: understanding measured as compression, with exact seeds")
    log("=" * 96)
    log(f"Message H: {len(held_idx)} held-out verses (every 50th verse; no model or word list saw them)"
        + ("   [DEV MODE: 40 TRAINING verses, a machinery check only]" if args.dev else ""))
    log(f"  {n_chars:,} characters, {sum(len(v.split()) for v in held_norm):,} word/punctuation tokens. "
        f"SHA-256 of H: {sha(H.encode())[:16]}...")
    log("  Normalised exactly as the models see text: lowercase words and . , ; : ? ! with single spaces,")
    log("  one verse per line. Capitals, verse numbers, apostrophes and hyphens are dropped for EVERY rung alike.")
    log(f"Soil: {len(pool):,} training verses. Script SHA-256 {script_sha[:16]}...  started "
        f"{time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    log()

    results = {"meta": {"script_sha256": script_sha, "started_utc": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                        "dev_mode": args.dev, "n_verses": len(held_idx), "n_chars": n_chars,
                        "H_sha256": sha(H.encode()), "held_verse_index": held_idx,
                        "segments": SEGMENTS, "qbits": QBITS,
                        "coder_precision_bits": PREC, "header_bytes": HEADER_BYTES,
                        "torch": torch.__version__, "numpy": np.__version__,
                        "python": sys.version.split()[0], "threads": torch.get_num_threads()},
               "rungs": {}}
    R = results["rungs"]

    def row(key, label, seed_bytes, exact, note=""):
        R.setdefault(key, {}).update(seed_bytes=seed_bytes, bpc=8 * seed_bytes / n_chars,
                                     pct_smaller_than_raw=100 * (1 - 8 * seed_bytes / raw_bits),
                                     exact=exact, label=label, note=note)

    # ---- R0 to R2: classic compressors, exact by construction (decompressed and compared) ----
    log("R0-R2  classic compressors (decompressed and compared byte for byte)")
    Hb = H.encode()
    row("R0_raw", "raw text, 8 bits per character", n_chars, True)
    z = zlib.compress(Hb, 9)
    row("R1_zlib9", "zip (zlib level 9), no shared greenhouse", len(z), zlib.decompress(z) == Hb)
    x = lzma.compress(Hb, preset=9 | lzma.PRESET_EXTREME)
    row("R1_xz9e", "xz (preset 9 extreme), no shared greenhouse", len(x), lzma.decompress(x) == Hb,
        "includes the xz container header (~60 bytes)")
    zd = train_norm.encode()[-32768:]
    co = zlib.compressobj(level=9, zdict=zd)
    zz = co.compress(Hb) + co.flush()
    do = zlib.decompressobj(zdict=zd)
    row("R2_zlib9_library32KB", "zip + shared library (last 32 KB of training text as zdict)", len(zz),
        do.decompress(zz) + do.flush() == Hb)
    for k in ("R0_raw", "R1_zlib9", "R1_xz9e", "R2_zlib9_library32KB"):
        log(f"  {k:22s} seed {R[k]['seed_bytes']:7,d} B  ({R[k]['bpc']:.3f} bpc)  exact: {R[k]['exact']}")
    log()

    # ---- greenhouses built from the soil ----
    base_train = [texts[i] for i in pool]
    base_vocab = tt.Vocab(base_train)
    values = sw.word_values(texts)                 # the project's own marking rule (see caveat)
    marked_all = {"shifting": sw.mark_up(verses, values)[0],
                  "label": mc.mark_label(verses, values),
                  "carry3": mc.mark_carry3(verses, values)}
    for s in SEEDS:
        marked_all[f"scrambled{s}"] = sw.mark_up(verses, values, s)[0]

    def marked_for(method, s):
        return marked_all[f"scrambled{s}"] if method == "scrambled" else marked_all[method]

    # ---- R3 to R5: word list, word frequencies, word pairs (fully decoded) ----
    log("R3-R5  shared word statistics from the training verses (all fully decoded)")
    uni = Unigram(base_vocab, base_train)
    bi = Bigram(base_vocab, base_train, uni)
    for key, label, pred in (
            ("R3_word_list", "word list only (uniform, + <unk> escape)", Uniform(len(base_vocab))),
            ("R4_word_freq", "word frequencies (unigram, add-one)", uni),
            ("R5_word_pairs", "word pairs (bigram, Witten-Bell)", bi)):
        R[key] = code_one(key, pred, held_norm, base_vocab, None, H, True, log)
        row(key, label, R[key]["seed_bytes"], R[key]["exact"])
    log()

    # ---- R6 and R7: the tiny transformers ----
    def load(method, s):
        train_texts = base_train if method == "baseline" else [marked_for(method, s)[i] for i in pool]
        vocab = tt.Vocab(train_texts)
        model = tt.TinyGPT(len(vocab))
        model.load_state_dict(torch.load(MODELS / f"{method}_seed{s}_steps{STEPS}.pt", map_location="cpu"))
        model.eval()
        return model, vocab

    def held_markers(method, s):
        if method == "baseline":
            return None
        m = marked_for(method, s)
        return [m[i].split(" ", 1)[0] for i in held_idx]

    def r67(method, s):
        model, vocab = load(method, s)
        key = f"{'R6' if method == 'baseline' else 'R7'}_{method}_seed{s}"
        required = method in ("baseline", "shifting")
        decode = required or args.dev or (time.time() - T0 < DECODE_BUDGET_S)
        res = code_one(key, Neural(model), held_norm, vocab, held_markers(method, s), H, decode, log)
        res["vocab_size"] = len(vocab)
        R[key] = res
        row(key, f"tiny transformer, {method}, seed {s}", res["seed_bytes"], res["exact"])
        if method != "baseline":
            R[key]["words_only_bits"] = float(np.sum(res["per_verse_words"]))
        return sum(p.numel() for p in model.parameters())

    # Required decodes first (every baseline and shifting model, and R8), optional ones last.
    log("R6-R7  tiny transformers (window = last 64 tokens). Marker models: TOTAL seed pays for the markers")
    for method in ("baseline", "shifting"):
        for s in SEEDS:
            n_params = r67(method, s)
    log()

    # ---- R8: the same gardener, given more and more context ----
    log("R8  baseline seed 0, allowed to see only the last k tokens (greenhouse built gradually)")
    model, vocab = load("baseline", 0)
    for k in K_LADDER:
        key = f"R8_baseline_seed0_k{k}"
        if k == tt.CTX:                 # identical computation to R6 seed 0: reuse it
            R[key] = dict(R["R6_baseline_seed0"])
            R[key].update(label="baseline seed 0, sees last 64 tokens",
                          note="identical to R6_baseline_seed0 (same model, same 64-token windows)")
            log(f"  {key:22s} = R6_baseline_seed0 ({R[key]['bpc']:.3f} bpc)")
            continue
        R[key] = code_one(key, Neural(model, k), held_norm, vocab, None, H, True, log)
        row(key, f"baseline seed 0, sees last {k} tokens", R[key]["seed_bytes"], R[key]["exact"])
    log()

    log(f"R7 (continued)  label, carry3, scrambled: decoded while the run is under {DECODE_BUDGET_S // 60} minutes")
    for method in ("label", "carry3", "scrambled"):
        for s in SEEDS:
            r67(method, s)
    log()

    # ------------------------------------------------------------------
    # Tables
    # ------------------------------------------------------------------
    log("=" * 96)
    log("TABLE 1  THE LADDER: exact seeds that regrow H byte for byte")
    log("=" * 96)
    log(f"  raw H = {n_chars:,} bytes = {raw_bits:,} bits.  bpc = seed bits / characters.  "
        "Greenhouse = shared in advance, NOT in the seed.")
    log(f"  {'rung':28s} {'seed bytes':>10s} {'bpc':>7s} {'smaller':>8s}  {'regrown exactly?':18s}")

    def status(k):
        r = R[k]
        if k.startswith(("R0", "R1", "R2")):
            return "yes (decompressed)" if r["exact"] else "NO"
        if not r.get("decoded"):
            return "encoded only"
        return "yes (decoded)" if r["exact"] else "NO - MISMATCH"

    def show(k, label=None):
        r = R[k]
        log(f"  {label or k:28s} {r['seed_bytes']:10,d} {r['bpc']:7.3f} {r['pct_smaller_than_raw']:7.1f}%  {status(k)}")

    for k in ("R0_raw", "R1_zlib9", "R1_xz9e", "R2_zlib9_library32KB", "R3_word_list", "R4_word_freq",
              "R5_word_pairs"):
        show(k)
    for method in METHODS:
        for s in SEEDS:
            show(f"{'R6' if method == 'baseline' else 'R7'}_{method}_seed{s}")
    for k in K_LADDER:
        show(f"R8_baseline_seed0_k{k}")
    log()

    # method summary
    log("TABLE 2  TINY TRANSFORMERS, mean of 3 seeds (TOTAL = real decoded seed; WORDS ONLY = markers not paid)")
    log("  (ideal = -log2 code lengths of the same rounded probabilities, no 4-byte header; use it to compare")
    log("   TOTAL with WORDS ONLY on the same footing)")
    log(f"  {'method':10s} {'TOTAL seed B':>12s} {'TOTAL bpc':>9s} {'per seed (B)':>26s} "
        f"{'marker bits/verse':>17s} {'TOTAL ideal bpc':>15s} {'WORDS ONLY bpc':>14s}")
    summary = {}
    for method in METHODS:
        keys = [f"{'R6' if method == 'baseline' else 'R7'}_{method}_seed{s}" for s in SEEDS]
        sb = [R[k]["seed_bytes"] for k in keys]
        words = [float(np.sum(R[k]["per_verse_words"])) for k in keys]
        mk = [R[k]["marker_bits"] / len(held_idx) for k in keys]
        summary[method] = {"seed_bytes_mean": float(np.mean(sb)), "bpc_total_mean": 8 * float(np.mean(sb)) / n_chars,
                           "seed_bytes_per_seed": sb, "marker_bits_per_verse_mean": float(np.mean(mk)),
                           "words_only_bpc_mean": float(np.mean(words)) / n_chars,
                           "total_ideal_bpc_mean": float(np.mean([R[k]["ideal_bits"] for k in keys])) / n_chars}
        log(f"  {method:10s} {np.mean(sb):12,.0f} {8 * np.mean(sb) / n_chars:9.4f} "
            f"{', '.join(f'{v:,}' for v in sb):>26s} {np.mean(mk):17.2f} "
            f"{summary[method]['total_ideal_bpc_mean']:15.4f} {summary[method]['words_only_bpc_mean']:14.4f}")
    results["method_summary"] = summary
    log()

    # paired tests
    per = {}
    for method in METHODS:
        keys = [f"{'R6' if method == 'baseline' else 'R7'}_{method}_seed{s}" for s in SEEDS]
        per[method] = {m: np.mean([R[k][f"per_verse_{m}"] for k in keys], 0) for m in ("total", "words")}
    tests = {}
    log("TABLE 3  EACH METHOD vs BASELINE, paired verse by verse (3-seed average per verse)")
    log("  diff = method minus baseline, bits per verse (negative = smaller seed = better).")
    log("  p one-sided tests 'method smaller'; two-sided in brackets. Permutation: 100,000 sign flips.")
    log(f"  {'comparison':26s} {'measure':10s} {'mean diff':>9s} {'smaller/larger':>15s} "
        f"{'sign p':>16s} {'permutation p':>18s}")
    pairs = [(m, "baseline") for m in MARKED] + [("shifting", "scrambled"), ("shifting", "label")]
    for a, b in pairs:
        for measure in ("total", "words"):
            t = compare(per[a][measure], per[b][measure])
            tests[f"{a}_vs_{b}/{measure}"] = t
            log(f"  {a + ' vs ' + b:26s} {('TOTAL' if measure == 'total' else 'WORDS ONLY'):10s} "
                f"{t['mean_diff_bits_per_verse']:+9.3f} {t['verses_smaller']:>7d}/{t['verses_larger']:<7d} "
                f"{t['sign_p_one_sided']:7.4f} ({t['sign_p_two_sided']:.4f}) "
                f"{t['perm_p_one_sided']:8.5f} ({t['perm_p_two_sided']:.5f})")
    results["paired_tests"] = tests
    log()

    main_t = tests["shifting_vs_baseline/total"]
    confirmed = main_t["perm_p_one_sided"] < 0.05 and main_t["mean_diff_bits_per_verse"] < 0
    sign_agrees = (main_t["sign_p_one_sided"] < 0.05) == confirmed
    results["preregistered"] = {
        "question": "Does the shifting-word model regrow held-out verses with a smaller TOTAL seed than baseline?",
        "test": "one-sided paired permutation test on mean per-verse TOTAL bits (3-seed average), p < 0.05",
        "mean_diff_bits_per_verse": main_t["mean_diff_bits_per_verse"],
        "perm_p_one_sided": main_t["perm_p_one_sided"], "sign_p_one_sided": main_t["sign_p_one_sided"],
        "verdict": "CONFIRMED" if confirmed else "NOT CONFIRMED", "sign_test_agrees": sign_agrees}
    log("PRE-REGISTERED VERDICT")
    log(f"  Does the shifting-word model regrow the held-out verses with a smaller TOTAL seed than baseline?")
    log(f"  mean difference {main_t['mean_diff_bits_per_verse']:+.3f} bits per verse "
        f"({main_t['total_diff_bits'] / 8:+,.0f} bytes over all of H);  permutation p = {main_t['perm_p_one_sided']:.5f};"
        f"  sign test p = {main_t['sign_p_one_sided']:.4f}")
    log(f"  -> {'CONFIRMED' if confirmed else 'NOT CONFIRMED'}"
        + ("" if sign_agrees else "   (the sign test DISAGREES with the permutation test)"))
    log()

    # context growth
    log("TABLE 4  THE GREENHOUSE BUILT GRADUALLY: baseline seed 0 given the last k tokens")
    log(f"  {'k tokens seen':>13s} {'seed bytes':>10s} {'bpc':>7s} {'smaller than raw':>17s}")
    growth = []
    for k in K_LADDER:
        r = R[f"R8_baseline_seed0_k{k}"]
        growth.append({"k": k, "seed_bytes": r["seed_bytes"], "bpc": r["bpc"]})
        log(f"  {k:13d} {r['seed_bytes']:10,d} {r['bpc']:7.3f} {r['pct_smaller_than_raw']:16.1f}%")
    results["context_growth"] = growth
    log()

    # exact regrowth summary
    dec = [k for k in R if R[k].get("decoded")]
    ok = [k for k in dec if R[k]["exact"]]
    enc_only = [k for k in R if k.startswith(("R3", "R4", "R5", "R6", "R7", "R8")) and not R[k].get("decoded")]
    log("EXACT REGROWTH")
    log(f"  Fully decoded token by token from seed bytes + greenhouse: {len(dec)} runs; "
        f"byte-for-byte identical to H: {len(ok)} of {len(dec)}.")
    log(f"  Encoded only (seed size real, not decoded): {', '.join(enc_only) if enc_only else 'none'}")
    log("  R0-R2 were decompressed and compared byte for byte.")
    log()

    log("SIZE OF THE GREENHOUSES (shared in advance, NOT in any seed)")
    log(f"  R2 library: 32,768 bytes of training text.  R3-R5 word list: {len(base_vocab):,} entries "
        f"(R4/R5 add counts; R5 knows {sum(len(v) for v in bi.follow.values()):,} word pairs).")
    log(f"  R6-R8 tiny transformer: {n_params:,} numbers (about {4 * n_params / 1e6:.1f} MB as float32), "
        f"far larger than H ({n_chars / 1e3:.0f} KB).")
    log("  A greenhouse pays off only when it is reused for many messages, like a dictionary both people own.")
    log()
    log("NOTES")
    log("  * Per-verse bits are ideal code lengths -log2(freq/total) of the SAME rounded probabilities the coder")
    log("    uses; their sum is within a few bytes of the real seed (see ideal_bits vs seed_bytes in the JSON).")
    log("  * WORDS ONLY is accounting, not a stand-alone seed: the decoder would need the markers from elsewhere.")
    log("  * Marker word values were computed by the earlier experiments from all verses, held-out ones included;")
    log("    kept unchanged because the models were trained with them. In TOTAL every marker is paid for.")
    log("  * Each held-out verse is coded with the previous held-out verses (50 verses back) as context, not its")
    log("    true neighbours; this is the same for every rung. The 12 groups each restart their context once.")
    elapsed = time.time() - T0
    log(f"  * Run time {elapsed / 60:.1f} minutes on {torch.get_num_threads()} threads "
        f"(torch {torch.__version__}, numpy {np.__version__}, Python {sys.version.split()[0]}).")
    results["meta"]["runtime_s"] = round(elapsed, 1)
    results["meta"]["fully_decoded"] = dec
    results["meta"]["exact_matches"] = ok
    results["meta"]["encoded_only"] = enc_only

    suffix = "_dev" if args.dev else ""
    # dev-mode outputs go to a scratch folder (UC_DEV_DIR), never next to the real results
    out_dir = Path(os.environ.get("UC_DEV_DIR", tempfile.gettempdir())) if args.dev else HERE
    (out_dir / f"results_understanding{suffix}.json").write_text(json.dumps(results, indent=1))
    (out_dir / f"results_understanding{suffix}.txt").write_text("\n".join(lines) + "\n")
    print(f"\nWrote {out_dir / f'results_understanding{suffix}.json'} and .txt")


if __name__ == "__main__":
    main()
