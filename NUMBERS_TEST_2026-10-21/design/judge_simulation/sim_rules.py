"""Judge's scratch simulation of the chosen charge-plus-remaining rules on the KJV markup.
No training, no test stories, repo untouched."""
import sys, json
sys.path.insert(0, "/home/user/utensil-theories-transfer-protocol/experiments")
import numpy as np
import shifting_word as sw
from bible_understanding import load_verses, tokens
from pathlib import Path
HERE = Path(__file__).parent
verses = load_verses(); texts = [t for _, t in verses]
values = json.loads((HERE / "values.json").read_text())
pool = [i for i in range(len(texts)) if i % 50]
nval = np.array([sum(w in values for w in tokens(t)) for t in texts])
NBAR = nval[pool].mean()
Q = 4 / 21
D = 1 - Q ** (1 / NBAR)
print(f"NBAR (training verses) = {NBAR:.4f}  DRAIN = {D:.6f}  (all verses NBAR {nval.mean():.4f})")

# reproduce mark_up exactly for the current shifting word
cur, _ = sw.mark_up(verses, values)
cur = np.array([sw.FORMS.index(m.split(' ', 1)[0]) for m in cur])

sums = np.array([sum(values.get(w, 0) for w in tokens(t)) for t in texts])
lo, hi = np.percentile(sums, [sw.CLEAR_PCT, 100 - sw.CLEAR_PCT])
clear = np.array([(-1 if sw.CLEAR_WRONG.search(t) or s <= lo else 1 if sw.CLEAR_RIGHT.search(t) or s >= hi else 0)
                  for t, s in zip(texts, sums)])
books = [b for b, _ in verses]
vals = [[values[w] for w in tokens(t) if w in values] for t in texts]

def mark(CH, reset=17, cap=51):
    out, Rs, pinned = [], [], 0
    prev = None
    for i in range(len(texts)):
        if books[i] != prev:
            R, s, k, prev = 0.0, 0, 0, books[i]
        f = sw.FORMS.index(sw.form_for(R)); out.append(f); Rs.append(R)
        if s:
            W = R + s * CH[k % len(CH)]; k += 1
        else:
            W = R
        if clear[i]:
            R, s, k = reset * clear[i], int(clear[i]), 0
            continue
        x = W
        for v in vals[i]:
            x += v; x *= (1 - D)
        pinned += abs(x) >= cap
        R = float(np.clip(x, -cap, cap))
    return np.array(out), np.array(Rs), pinned / len(texts)

CFG = {"charge17": (17,), "seq": (32, 16, 34, 47, 17), "seq_rev": (47, 34, 16, 32, 17),
       "charge47": (47,), "drain0": (0,), "const29": (29.2,)}
res = {k: mark(v) for k, v in CFG.items()}
res["shifting(current)"] = (cur, None, None)
same_book = np.array([books[i] == books[i - 1] for i in range(1, len(books))])
nxt = np.arange(1, len(texts))
def stats(name, f):
    share = np.bincount(f, minlength=5) / len(f)
    same = np.mean((f[1:] == f[:-1])[same_book])
    pos = f - 2
    # corr of marker with the lean of the verse just read (non-clear verses only)
    m = same_book & (clear[:-1] == 0)
    corr = np.corrcoef(pos[1:][m], sums[:-1][m])[0, 1]
    # verdict retention: L verses after a verdict with no new verdict in between, sign of marker == verdict
    ret = {}
    for L in (1, 3, 5, 10):
        ok = n = 0
        for i in np.where(clear != 0)[0]:
            j = i + L
            if j >= len(texts) or books[j] != books[i] or np.any(clear[i + 1:j] != 0):
                continue
            n += 1; ok += np.sign(pos[j]) == clear[i]
        ret[L] = ok / n
    print(f"{name:18s} shares {' '.join(f'{x*100:4.1f}' for x in share)}  same-as-prev {same*100:4.1f}%  "
          f"corr(last verse) {corr:+.2f}  verdict sign kept L=1/3/5/10: "
          + "/".join(f"{ret[L]*100:.0f}" for L in (1, 3, 5, 10)))
for k, (f, R, pin) in res.items():
    stats(k, f)
    if pin is not None:
        print(f"{'':18s} pinned at cap after a verse: {pin*100:.2f}%   mean |R| {np.mean(np.abs(R)):.1f}")
names = list(res)
print("\n% of verses whose marker differs:")
print(" " * 18 + "".join(f"{n[:9]:>10s}" for n in names))
for a in names:
    print(f"{a:18s}" + "".join(f"{100*np.mean(res[a][0]!=res[b][0]):10.1f}" for b in names))
# held-out verses share
held = [i for i in range(len(texts)) if i % 50 == 0]
print("held-out n", len(held))
