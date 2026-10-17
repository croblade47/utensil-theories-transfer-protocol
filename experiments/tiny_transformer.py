"""
Tiny Transformer Test
=====================

The word-averaging model (consequences_test.py) failed because it cannot
combine words: it knew "steal" was wrong but not that "took his neighbour's ox
by night and sold it" is stealing. A transformer reads word ORDER, so it can
compose meaning. Here we train a tiny one from scratch on the King James Bible
only (no other text, no pre-training) and re-run the same 40 new stories.

Scoring (fixed before training):
  MAIN   Shift test, 20 pairs. For each pair, does the model lean more toward the
         fortunate ending after the right act than after the wrong act?
         log P(fortunate|right) - log P(ruinous|right)
           >  log P(fortunate|wrong) - log P(ruinous|wrong)      chance = 50%
  2nd    Pick-the-ending accuracy over 40 stories.                chance = 50%
  3rd    Judgment shift, 20 pairs: does "...and this was evil in the sight of
         the lord" fit the wrong act better than the right act (relative to
         "...right in the sight of the lord")?                    chance = 50%

Conditions: full Bible / rules removed / same number of random verses removed,
each trained twice with different seeds.

Run:  python experiments/tiny_transformer.py [--steps 1500] [--only full]
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import time
from collections import Counter
from math import comb
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

from bible_understanding import RULE_RE, load_verses
from consequences_test import ITEMS

torch.set_num_threads(4)
OUT = Path(__file__).parent / "results_transformer.json"

CTX, D, LAYERS, HEADS, DROPOUT = 64, 192, 4, 4, 0.1
BATCH, LR = 64, 3e-3
JOIN = " , "                     # story + JOIN + ending
JUDGE_EVIL = "and this was evil in the sight of the lord"
JUDGE_RIGHT = "and this was right in the sight of the lord"

# ---------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------

TOK = re.compile(r"[a-z]+|[.,;:?!]")


def tok(text):
    return TOK.findall(text.lower())


class Vocab:
    def __init__(self, texts):
        c = Counter(t for x in texts for t in tok(x))
        self.itos = ["<unk>", "<v>"] + sorted(w for w, n in c.items() if n >= 2)
        self.stoi = {w: i for i, w in enumerate(self.itos)}

    def encode(self, text):
        return [self.stoi.get(t, 0) for t in tok(text)]

    def __len__(self):
        return len(self.itos)


def stream(vocab, texts):
    ids = []
    for t in texts:
        ids.append(1)            # verse boundary
        ids.extend(vocab.encode(t))
    return torch.tensor(ids, dtype=torch.long)

# ---------------------------------------------------------------------------
# Model: a standard small GPT
# ---------------------------------------------------------------------------

class Block(nn.Module):
    def __init__(self):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(D), nn.LayerNorm(D)
        self.attn = nn.MultiheadAttention(D, HEADS, dropout=DROPOUT, batch_first=True)
        self.mlp = nn.Sequential(nn.Linear(D, 4 * D), nn.GELU(), nn.Linear(4 * D, D),
                                 nn.Dropout(DROPOUT))

    def forward(self, x, mask):
        h = self.ln1(x)
        x = x + self.attn(h, h, h, attn_mask=mask, need_weights=False)[0]
        return x + self.mlp(self.ln2(x))


class TinyGPT(nn.Module):
    def __init__(self, n_vocab):
        super().__init__()
        self.tok = nn.Embedding(n_vocab, D)
        self.pos = nn.Embedding(CTX, D)
        self.blocks = nn.ModuleList(Block() for _ in range(LAYERS))
        self.ln = nn.LayerNorm(D)
        self.head = nn.Linear(D, n_vocab, bias=False)
        self.head.weight = self.tok.weight     # tied weights
        self.drop = nn.Dropout(DROPOUT)
        self.apply(self._init)

    @staticmethod
    def _init(m):
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, std=0.02)
        if isinstance(m, nn.Linear) and m.bias is not None:
            nn.init.zeros_(m.bias)

    def forward(self, idx):
        T = idx.shape[1]
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool), 1)
        x = self.drop(self.tok(idx) + self.pos(torch.arange(T)))
        for b in self.blocks:
            x = b(x, mask)
        return self.head(self.ln(x))


def train(vocab, texts, steps, seed, log_every=500):
    torch.manual_seed(seed)
    random.seed(seed)
    data = stream(vocab, texts)
    model = TinyGPT(len(vocab))
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.1)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, LR, total_steps=steps, pct_start=0.05)
    model.train()
    t0 = time.time()
    for step in range(1, steps + 1):
        ix = torch.randint(len(data) - CTX - 1, (BATCH,))
        x = torch.stack([data[i:i + CTX] for i in ix])
        y = torch.stack([data[i + 1:i + CTX + 1] for i in ix])
        loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten())
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        if step % log_every == 0 or step == steps:
            print(f"    step {step:5d}  loss {loss.item():.3f}  ({time.time() - t0:.0f}s)", flush=True)
    model.eval()
    return model

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

@torch.no_grad()
def logp(model, vocab, context, continuation):
    """Total log-probability of `continuation` given `context`."""
    c = [1] + vocab.encode(context)
    e = vocab.encode(continuation)
    ids = torch.tensor([(c + e)[-CTX:]])
    n_ctx = ids.shape[1] - len(e)
    lp = F.log_softmax(model(ids)[0], -1)
    return sum(lp[n_ctx - 1 + i, e[i]].item() for i in range(len(e)))


def p_value(k, n):
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n


def evaluate(model, vocab):
    shift = pick = judge = 0
    for right, wrong, fortunate, ruinous in ITEMS:
        d = {}
        for name, story in (("right", right), ("wrong", wrong)):
            d[name] = (logp(model, vocab, story + JOIN, fortunate)
                       - logp(model, vocab, story + JOIN, ruinous))
        shift += d["right"] > d["wrong"]
        pick += (d["right"] > 0) + (d["wrong"] < 0)
        j = {name: logp(model, vocab, story + JOIN, JUDGE_EVIL)
                   - logp(model, vocab, story + JOIN, JUDGE_RIGHT)
             for name, story in (("right", right), ("wrong", wrong))}
        judge += j["wrong"] > j["right"]
    n = len(ITEMS)
    return {"shift": shift, "pick": pick, "judge": judge, "n_pairs": n}


@torch.no_grad()
def held_out_loss(model, data):
    """Average next-word loss on verses the model never trained on."""
    losses = []
    for i in range(0, len(data) - CTX - 1, CTX):
        x, y = data[i:i + CTX][None], data[i + 1:i + CTX + 1][None]
        losses.append(F.cross_entropy(model(x)[0], y[0]).item())
    return sum(losses) / len(losses)

# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1])
    ap.add_argument("--only", nargs="+", default=None)
    args = ap.parse_args()

    verses = load_verses()
    texts = [t for _, t in verses]
    vocab = Vocab(texts)
    story_words = [t for it in ITEMS for s in it for t in tok(s)] + tok(JUDGE_EVIL + " " + JUDGE_RIGHT)
    oov = sorted({w for w in story_words if w not in vocab.stoi})
    print(f"Vocabulary {len(vocab):,} words. Test words unknown to the model: {oov or 'none'}")

    # Hold out every 50th verse to measure plain language skill (never trained on).
    held = [texts[i] for i in range(0, len(texts), 50)]
    pool = [i for i in range(len(texts)) if i % 50]
    rules = {i for i in pool if RULE_RE.search(texts[i])}
    conditions = {
        "full": pool,
        "no_rules": [i for i in pool if i not in rules],
        "minus_random": None,   # filled per seed
    }
    held_data = stream(vocab, held)

    results = json.loads(OUT.read_text()) if OUT.exists() else {}
    for name in conditions:
        if args.only and name not in args.only:
            continue
        for seed in args.seeds:
            key = f"{name}/seed{seed}/steps{args.steps}"
            if key in results:
                print(f"{key}: cached")
                continue
            idx = conditions[name]
            if name == "minus_random":
                drop = set(random.Random(seed).sample(pool, len(rules)))
                idx = [i for i in pool if i not in drop]
            print(f"\n== {key}: training on {len(idx):,} verses")
            model = train(vocab, [texts[i] for i in idx], args.steps, seed)
            r = evaluate(model, vocab)
            r["held_out_loss"] = round(held_out_loss(model, held_data), 3)
            results[key] = r
            OUT.write_text(json.dumps(results, indent=2))
            print(f"   shift {r['shift']}/20  pick {r['pick']}/40  judge {r['judge']}/20  "
                  f"held-out loss {r['held_out_loss']}")

    print("\nSummary (chance = 50%; p = chance of doing this well by luck)")
    for key, r in results.items():
        n = r["n_pairs"]
        print(f"  {key:28s} shift {r['shift']:2d}/{n} (p={p_value(r['shift'], n):.3f})  "
              f"pick {r['pick']:2d}/{2*n} (p={p_value(r['pick'], 2*n):.3f})  "
              f"judge {r['judge']:2d}/{n} (p={p_value(r['judge'], n):.3f})  "
              f"loss {r['held_out_loss']}")


if __name__ == "__main__":
    main()
