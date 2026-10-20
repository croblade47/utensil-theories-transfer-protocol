"""
The Shifting Word ("velanok")
=============================

A made-up word that carries a running balance from one use to the next, and
whose SPELLING changes with that balance (like to / too / two / 2).

The rules
---------
  balance starts at 0
  each ordinary word adds its own value (negative leans wrong, positive leans right)
  a clear wrong  resets the balance to -17
  a clear right  resets the balance to +17
  each word also uses up 0.5 of the balance, so it drifts back toward 0
  whatever is left over carries to the next appearance ("remaining")
  at each appearance the word is written in the form that matches the balance

Optional (off by default): RECHARGE re-adds 17 in the balance's direction at
each appearance, as in "W1 = 17 + 4". Off because the balance then grows forever.

Spelling: five rotations of the syllables  sha-ru-vel-an-ok,
each a distinct new word the model has never seen:

  balance <= -12   anoksha    heavy wrong
  -11 .. -4        oksharu    leaning wrong
   -3 .. 3         velanok    unresolved
    4 .. 11        sharuvel   leaning right
  >= 12            ruvelan    heavy right

The experiment
--------------
1. Mark up the whole Bible: the word appears at the start of every verse,
   spelled for the balance left by the verses before it.
2. Train the tiny transformer on the marked-up Bible.
3. On the 40 new stories: the model writes the word ITSELF after the story
   (its own judgment), then we score the two endings.
Checks: (a) scrambled spellings = same extra word, no meaning;
        (b) oracle = we hand it the correct spelling.

Run:  python experiments/shifting_word.py [--steps 1500] [--seed 0]
"""

from __future__ import annotations

import argparse
import json
import random
import re
from math import comb
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

import tiny_transformer as tt
from collections import Counter

from bible_understanding import STOP, Model, load_verses, tokens
from consequences_test import BAD_SEEDS, GOOD_SEEDS, ITEMS

OUT = Path(__file__).parent / "results_shifting_word.json"

RESET = 17
RECHARGE = False
SPEND = 0.5         # each word also uses up this much of the balance (toward 0)
FORMS = ["anoksha", "oksharu", "velanok", "sharuvel", "ruvelan"]   # wrong ... right
SCALE = 30          # word value = round(moral lean * SCALE)
CLEAR_PCT = 3       # verses in the top/bottom 3% of lean count as clear choices

CLEAR_WRONG = re.compile(r"did (that which was )?evil in the (sight|eyes) of the lord|"
                         r"(wrought|done|committed) (great )?(wickedness|evil|abomination)", re.I)
CLEAR_RIGHT = re.compile(r"did that which was right in the (sight|eyes) of the lord|"
                         r"(walked|walk) in (all )?(his|my) (ways|statutes|commandments)|"
                         r"(was|were) (a )?(just|perfect|upright)", re.I)


def form_for(balance: float) -> str:
    if balance <= -12: return FORMS[0]
    if balance <= -4:  return FORMS[1]
    if balance < 4:    return FORMS[2]
    if balance < 12:   return FORMS[3]
    return FORMS[4]


class ShiftingWord:
    """The variable itself: a balance carried across uses."""

    def __init__(self, word_values: dict[str, int]):
        self.values = word_values
        self.balance = 0.0

    def emerge(self) -> str:
        """The word appears: write it in the form for the current balance."""
        if RECHARGE and self.balance:
            self.balance += RESET * np.sign(self.balance)
        return form_for(self.balance)

    def read(self, text: str, clear: int = 0):
        """Spend/add the following words; a clear choice resets the balance."""
        if clear:
            self.balance = RESET * clear
            return
        for w in tokens(text):
            if w not in self.values:
                continue
            self.balance += self.values[w]
            self.balance -= np.sign(self.balance) * min(SPEND, abs(self.balance))
        self.balance = float(np.clip(self.balance, -3 * RESET, 3 * RESET))

    def reset(self):
        self.balance = 0.0


def word_values(texts) -> dict[str, int]:
    """Each word's value = its lean on the good/evil direction learned from the Bible."""
    m = Model(texts)
    axis = (np.mean([m.v(w) for w in GOOD_SEEDS if m.has(w)], 0)
            - np.mean([m.v(w) for w in BAD_SEEDS if m.has(w)], 0))
    lean = m.vec @ axis
    # Centre so an ordinary run of text adds up to about zero (no drift):
    # weight by how often each word is actually used.
    freq = Counter(t for x in texts for t in tokens(x))
    content = [i for i, w in enumerate(m.vocab) if w not in STOP]
    weights = np.array([freq[m.vocab[i]] for i in content], float)
    lean -= np.average(lean[content], weights=weights)
    return {m.vocab[i]: int(round(lean[i] * SCALE)) for i in content}


def mark_up(verses, values, scramble_seed=None):
    """Insert the shifting word at the start of every verse."""
    sums = np.array([sum(values.get(w, 0) for w in tokens(t)) for _, t in verses])
    lo, hi = np.percentile(sums, [CLEAR_PCT, 100 - CLEAR_PCT])
    rng = random.Random(scramble_seed)
    sw, out, prev_book, n_clear = ShiftingWord(values), [], None, 0
    for (book, text), s in zip(verses, sums):
        if book != prev_book:
            sw.reset()
            prev_book = book
        form = sw.emerge()
        if scramble_seed is not None:
            form = rng.choice(FORMS)
        out.append(f"{form} {text}")
        clear = (-1 if CLEAR_WRONG.search(text) or s <= lo else
                 1 if CLEAR_RIGHT.search(text) or s >= hi else 0)
        n_clear += bool(clear)
        sw.read(text, clear)
    return out, n_clear

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

@torch.no_grad()
def lp_ids(model, ctx_ids, cont_ids):
    ids = torch.tensor([(ctx_ids + cont_ids)[-tt.CTX:]])
    n = ids.shape[1] - len(cont_ids)
    lp = F.log_softmax(model(ids)[0], -1)
    return sum(lp[n - 1 + i, c].item() for i, c in enumerate(cont_ids))


def evaluate(model, vocab):
    """Story -> [model writes the word] -> ending."""
    form_ids = [vocab.stoi[f] for f in FORMS]
    res = {"self_shift": 0, "self_pick": 0, "oracle_shift": 0, "oracle_pick": 0,
           "judge": 0, "n_pairs": len(ITEMS)}
    for right, wrong, fortunate, ruinous in ITEMS:
        ef, er = vocab.encode(fortunate), vocab.encode(ruinous)
        d_self, d_oracle, lean = {}, {}, {}
        for name, story in (("right", right), ("wrong", wrong)):
            ctx = [1] + vocab.encode(story) + [1]
            # the model's own choice of spelling
            scores = [lp_ids(model, ctx, [f]) for f in form_ids]
            probs = np.exp(np.array(scores) - max(scores))
            probs /= probs.sum()
            lean[name] = float(probs @ np.arange(-2, 3))     # expected position wrong..right
            own = form_ids[int(np.argmax(scores))]
            d_self[name] = lp_ids(model, ctx + [own], ef) - lp_ids(model, ctx + [own], er)
            # oracle: hand it the correct spelling
            ora = form_ids[4] if name == "right" else form_ids[0]
            d_oracle[name] = lp_ids(model, ctx + [ora], ef) - lp_ids(model, ctx + [ora], er)
        res["self_shift"] += d_self["right"] > d_self["wrong"]
        res["self_pick"] += (d_self["right"] > 0) + (d_self["wrong"] < 0)
        res["oracle_shift"] += d_oracle["right"] > d_oracle["wrong"]
        res["oracle_pick"] += (d_oracle["right"] > 0) + (d_oracle["wrong"] < 0)
        res["judge"] += lean["right"] > lean["wrong"]
    return res


def p_value(k, n):
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n


def demo(marked, verses, book="II Kings", start_text="In the twelfth year of Ahaz", n=8):
    i = next(k for k, (b, t) in enumerate(verses) if b == book and t.startswith(start_text))
    print(f"\n  Example ({book}): the word's spelling as the story unfolds")
    for k in range(i, i + n):
        f, rest = marked[k].split(" ", 1)
        print(f"    [{f:8s}] {rest[:95]}{'...' if len(rest) > 95 else ''}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--only", nargs="+", default=None)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    verses = load_verses()
    texts = [t for _, t in verses]
    values = word_values(texts)
    pool = [i for i in range(len(texts)) if i % 50]        # same split as tiny_transformer.py
    results = json.loads(OUT.read_text()) if OUT.exists() else {}

    for name, scramble in (("shifting_word", None), ("scrambled_control", args.seed)):
        if args.only and name not in args.only:
            continue
        marked, n_clear = mark_up(verses, values, scramble)
        if scramble is None and args.seed == 0:
            print(f"Clear right/wrong resets: {n_clear:,} of {len(verses):,} verses")
            from collections import Counter
            dist = Counter(m.split(" ", 1)[0] for m in marked)
            print("  Spelling counts:", ", ".join(f"{f} {dist[f]:,}" for f in FORMS))
            demo(marked, verses)
        key = f"{name}/seed{args.seed}/steps{args.steps}"
        if key in results:
            print(f"{key}: cached")
            continue
        train_texts = [marked[i] for i in pool]
        vocab = tt.Vocab(train_texts)
        print(f"\n== {key}: training on {len(train_texts):,} marked-up verses", flush=True)
        model = tt.train(vocab, train_texts, args.steps, seed=args.seed)
        r = evaluate(model, vocab)
        results[key] = r
        OUT.write_text(json.dumps(results, indent=2))
        print(f"   {r}", flush=True)

    print("\nSummary (chance = 50%)")
    for key, r in results.items():
        n = r["n_pairs"]
        print(f"  {key}")
        print(f"    model writes its own word:  shift {r['self_shift']}/{n} (p={p_value(r['self_shift'], n):.3f})"
              f"  pick {r['self_pick']}/{2*n} (p={p_value(r['self_pick'], 2*n):.3f})")
        print(f"    word's judgment of the act: {r['judge']}/{n} (p={p_value(r['judge'], n):.3f})")
        print(f"    handed the correct word:    shift {r['oracle_shift']}/{n} (p={p_value(r['oracle_shift'], n):.3f})"
              f"  pick {r['oracle_pick']}/{2*n} (p={p_value(r['oracle_pick'], 2*n):.3f})")


if __name__ == "__main__":
    main()
