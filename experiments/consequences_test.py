"""
Consequences Test
=================

Does reading the Bible let a text-only model predict what FOLLOWS an act
in a story it has never seen? And do the rules ("thou shalt not ...", which
are often written as act -> consequence) teach that better than the stories?

Design (fixed before any results were seen):
- 20 new story pairs. Each pair is one situation told two ways: a right act
  and a wrong act. Both share the same two endings: one fortunate, one ruinous.
  A model that always picks the same ending scores exactly 50%.
- Moral label words (good, evil, wicked, righteous, sin, blessed, cursed ...)
  are banned from stories and endings, so the model cannot just match labels.
- No ending word appears in its own stories (checked below).

Two ways to choose an ending:
- ASSOCIATION:  pick the ending whose words sit closest to the story's words.
- CONSEQUENCE:  learn a "what comes next" map from the Bible itself
                (first half of a verse -> second half, and verse -> next verse),
                apply it to the story, pick the ending closest to the prediction.

Run:  python experiments/consequences_test.py   (needs numpy + scipy)
"""

from __future__ import annotations

import random
import re
from math import comb

import numpy as np

from bible_understanding import RULE_RE, STOP, Model, load_verses, tokens

RIDGE = 10.0          # fixed in advance, not tuned on the test
SEEDS = [0, 1, 2]

BANNED = {"good", "evil", "wicked", "wickedness", "righteous", "righteousness",
          "sin", "sins", "sinned", "iniquity", "blessed", "bless", "cursed", "curse",
          "upright", "ungodly", "holy", "unclean", "punished", "rewarded", "reward"}

# (right-act story, wrong-act story, fortunate ending, ruinous ending)
ITEMS = [
    ("the man found his neighbour's ox astray and brought it again unto him",
     "the man took his neighbour's ox by night and sold it for silver",
     "and his flocks increased and his barns were full",
     "and his flocks died and his barns were empty"),
    ("the young man honoured his father and his mother in their old age",
     "the young man mocked his father and despised his mother",
     "and his days were long in the land",
     "and he died before his time"),
    ("the king heard the cry of the poor and fed the hungry",
     "the king oppressed the poor and took away their bread",
     "and his throne was established and the people rejoiced",
     "and his kingdom was rent from him and the people fled"),
    ("the merchant used a just weight and a true balance",
     "the merchant used a false balance and deceived the buyers",
     "and his house prospered many years",
     "and his riches perished and he became poor"),
    ("the servant spake the truth before the judges",
     "the servant bare false witness before the judges",
     "and he was set free and given honour",
     "and he was beaten and cast into prison"),
    ("the woman was faithful to her husband all her days",
     "the woman committed adultery with her neighbour",
     "and her children rose up and praised her",
     "and she was put to shame before all the city"),
    ("the people kept the sabbath and rested from their labour",
     "the people broke the sabbath and gathered sticks",
     "and rain came in its season and the harvest was plenty",
     "and drought came upon the land and there was famine"),
    ("the brother forgave his brother and embraced him",
     "the brother envied his brother and slew him in the field",
     "and peace dwelt in their house",
     "and he became a fugitive and a vagabond in the earth"),
    ("the man was content with his own portion",
     "the man coveted his neighbour's field and vineyard",
     "and he lived quietly and had enough",
     "and he lost his inheritance and was cast out"),
    ("the young man was sober and diligent in his work",
     "the young man was a drunkard and slothful",
     "and he stood before kings",
     "and he was clothed with rags"),
    ("the people worshipped the lord their god only",
     "the people made a golden calf and bowed down to it",
     "and their enemies fled before them",
     "and their enemies smote them and carried them away captive"),
    ("the rich man opened his hand to the widow and the fatherless",
     "the rich man shut his hand against the widow and the fatherless",
     "and his seed was mighty upon the earth",
     "and his children begged bread"),
    ("the prophet was humble and sought counsel",
     "the prophet was proud and lifted up his heart",
     "and he was exalted in the sight of all",
     "and he was brought low and destroyed"),
    ("the steward returned what was lent to him",
     "the steward borrowed and paid not again",
     "and his master gave him more",
     "and his goods were taken from him"),
    ("the stranger was welcomed and given water and bread",
     "the stranger was turned away and stoned at the gate",
     "and the city was saved",
     "and fire fell upon the city"),
    ("the son obeyed the words of his father's instruction",
     "the son rejected the instruction of his father",
     "and he walked safely and his foot did not stumble",
     "and he went astray and perished"),
    ("the judge refused the gift and judged the cause of the poor",
     "the judge took a bribe and perverted judgment",
     "and the land had rest",
     "and the land mourned"),
    ("the man paid the wages of the hireling before the sun went down",
     "the man kept back the wages of the hireling",
     "and his work prospered in his hands",
     "and his work came to nothing"),
    ("the woman gave her last bread to the prophet",
     "the woman hid her bread from the hungry prophet",
     "and her barrel of meal did not waste",
     "and her son sickened and died"),
    ("the shepherd sought the lost sheep until he found it",
     "the shepherd left the sheep to the wolves and fled",
     "and the flock grew strong",
     "and the flock was scattered"),
]


def content(text):
    return [t for t in tokens(text) if t not in STOP]


def check_items():
    for right, wrong, fortunate, ruinous in ITEMS:
        story_words = set(content(right)) | set(content(wrong))
        for text in (right, wrong, fortunate, ruinous):
            bad = BANNED & set(tokens(text))
            assert not bad, f"banned word {bad} in: {text}"
        for end in (fortunate, ruinous):
            overlap = story_words & set(content(end))
            assert not overlap, f"ending shares {overlap} with its stories: {end}"


class Encoder:
    """Turns a sentence into one point: the average of its words' points,
    centred on the average verse so shared background cancels out."""

    def __init__(self, model: Model, texts: list[str]):
        self.m = model
        self.mu = np.zeros(model.vec.shape[1])
        sample = [self.raw(t) for t in texts[::5]]
        self.mu = np.mean([s for s in sample if s is not None], 0)

    def raw(self, text):
        vs = [self.m.v(w) for w in content(text) if self.m.has(w)]
        return np.mean(vs, 0) if vs else None

    def __call__(self, text):
        r = self.raw(text)
        return None if r is None else r - self.mu


def sequence_pairs(verses: list[tuple[str, str]]):
    """'This happened, then this followed' pairs from the Bible itself.
    Returns [(source_text, target_text, source_is_rule)]."""
    pairs = []
    for k, (book, text) in enumerate(verses):
        is_rule = bool(RULE_RE.search(text))
        halves = re.split(r"[;:]", text, maxsplit=1)
        if len(halves) == 2 and len(content(halves[0])) >= 2 and len(content(halves[1])) >= 2:
            pairs.append((halves[0], halves[1], is_rule))
        if k + 1 < len(verses) and verses[k + 1][0] == book:
            pairs.append((text, verses[k + 1][1], is_rule))
    return pairs


def fit_map(enc: Encoder, pairs):
    X, Y = [], []
    for src, tgt, _ in pairs:
        x, y = enc(src), enc(tgt)
        if x is not None and y is not None:
            X.append(x)
            Y.append(y)
    X, Y = np.array(X), np.array(Y)
    d = X.shape[1]
    return np.linalg.solve(X.T @ X + RIDGE * np.eye(d), X.T @ Y)


def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


def evaluate(enc: Encoder, W=None):
    """Accuracy over the 40 stories. W=None means plain association."""
    correct = total = 0
    detail = []
    for right, wrong, fortunate, ruinous in ITEMS:
        ef, er = enc(fortunate), enc(ruinous)
        for story, expected in ((right, "fortunate"), (wrong, "ruinous")):
            s = enc(story)
            if s is None or ef is None or er is None:
                continue
            p = s if W is None else s @ W
            pick = "fortunate" if cos(p, ef) > cos(p, er) else "ruinous"
            total += 1
            correct += pick == expected
            detail.append((story, expected, pick))
    return correct, total, detail


def p_value(k, n):
    """Chance of scoring k/n or better by coin-flipping."""
    return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n


def fmt(k, n):
    return f"{k:2d}/{n} = {k/n:4.0%}  (p = {p_value(k, n):.3f})"


# --- Diagnostic added AFTER section A-C came back at chance -----------------
# Seed words for the two directions. None of them appear in any story or ending.
GOOD_SEEDS = ["good", "righteous", "righteousness", "upright"]
BAD_SEEDS = ["evil", "wicked", "wickedness", "iniquity"]
FORTUNE_SEEDS = ["abundance", "safety", "joy", "gladness", "wealth"]
RUIN_SEEDS = ["calamity", "desolation", "sorrow", "destruction", "misery"]


def axis(m: Model, plus, minus):
    a = np.mean([m.v(w) for w in plus if m.has(w)], 0)
    b = np.mean([m.v(w) for w in minus if m.has(w)], 0)
    return a - b


def diagnose(enc: Encoder):
    """Split the task into its pieces and test each one."""
    moral = axis(enc.m, GOOD_SEEDS, BAD_SEEDS)
    fortune = axis(enc.m, FORTUNE_SEEDS, RUIN_SEEDS)
    acts = ends = linked = 0
    for right, wrong, fortunate, ruinous in ITEMS:
        r, w = enc(right) @ moral, enc(wrong) @ moral
        f, x = enc(fortunate) @ fortune, enc(ruinous) @ fortune
        acts += r > w            # knows which act is right
        ends += f > x            # knows which ending is fortunate
        # "as you sow, so you reap": the more-right act gets the more-fortunate ending
        linked += 2 * ((r > w) == (f > x))
    return acts, ends, linked, cos(moral, fortune)


def main():
    check_items()
    verses = load_verses()
    texts = [t for _, t in verses]
    rule_idx = {i for i, t in enumerate(texts) if RULE_RE.search(t)}
    n_rules = len(rule_idx)
    print(f"{len(ITEMS)} story pairs -> {2*len(ITEMS)} stories. Guessing scores 50%.")
    print("p = chance of doing this well by luck (below 0.05 is usually called real).\n")

    full = Model(texts)
    enc = Encoder(full, texts)
    pairs = sequence_pairs(verses)
    rule_pairs = [p for p in pairs if p[2]]
    other_pairs = [p for p in pairs if not p[2]]
    print(f"Bible 'then this followed' pairs: {len(pairs):,} "
          f"({len(rule_pairs):,} from rule verses)\n")

    print("=" * 72)
    print("A. Can a text-only reader predict consequences at all? (full Bible)")
    print("=" * 72)
    k, n, _ = evaluate(enc)
    print(f"  Association  {fmt(k, n)}")
    W_full = fit_map(enc, pairs)
    k, n, detail = evaluate(enc, W_full)
    print(f"  Consequence  {fmt(k, n)}")
    misses = [(s, e) for s, e, p in detail if p != e]
    if misses:
        print("  Missed:")
        for s, e in misses:
            print(f"    - {s}  (should be {e})")

    print("\n" + "=" * 72)
    print("B. Do RULES teach consequences better than STORIES? (same amount of each)")
    print("=" * 72)
    W_rules = fit_map(enc, rule_pairs)
    k, n, _ = evaluate(enc, W_rules)
    print(f"  Learned from rules only            {fmt(k, n)}")
    for s in SEEDS:
        sample = random.Random(s).sample(other_pairs, len(rule_pairs))
        k, n, _ = evaluate(enc, fit_map(enc, sample))
        print(f"  Learned from non-rule verses (#{s+1}) {fmt(k, n)}")

    print("\n" + "=" * 72)
    print("C. Take the rules out of EVERYTHING (word meanings and the map)")
    print("=" * 72)
    keep = [i for i in range(len(texts)) if i not in rule_idx]
    m_nr = Model([texts[i] for i in keep])
    enc_nr = Encoder(m_nr, [texts[i] for i in keep])
    nr_pairs = sequence_pairs([verses[i] for i in keep])
    k, n, _ = evaluate(enc_nr)
    print(f"  No rules - association             {fmt(k, n)}")
    k, n, _ = evaluate(enc_nr, fit_map(enc_nr, nr_pairs))
    print(f"  No rules - consequence             {fmt(k, n)}")
    for s in SEEDS:
        drop = set(random.Random(s).sample(range(len(texts)), n_rules))
        keep_r = [i for i in range(len(texts)) if i not in drop]
        m_r = Model([texts[i] for i in keep_r])
        enc_r = Encoder(m_r, [texts[i] for i in keep_r])
        k, n, _ = evaluate(enc_r, fit_map(enc_r, sequence_pairs([verses[i] for i in keep_r])))
        print(f"  Random verses removed (#{s+1}) - consequence {fmt(k, n)}")

    print("\n" + "=" * 72)
    print("D. Diagnostic (added after A-C): does it have the pieces but not the link?")
    print("=" * 72)
    a, e, l, align = diagnose(enc)
    N = len(ITEMS)
    print(f"  Tells the right act from the wrong act      {fmt(a, N)}")
    print(f"  Tells the fortunate ending from the ruinous {fmt(e, N)}")
    print(f"  + one rule, 'as you sow, so you reap'       {fmt(l, 2 * N)}")
    print("\n  Did the Bible teach that link by itself? Alignment between the")
    print("  right/wrong direction and the fortune/ruin direction (0 = unrelated, 1 = same):")
    print(f"    full Bible               {align:+.3f}")
    print(f"    rules removed            {diagnose(enc_nr)[3]:+.3f}")
    for s in SEEDS:
        drop = set(random.Random(s).sample(range(len(texts)), n_rules))
        keep_r = [i for i in range(len(texts)) if i not in drop]
        m_r = Model([texts[i] for i in keep_r])
        print(f"    random removed (#{s+1})     {diagnose(Encoder(m_r, [texts[i] for i in keep_r]))[3]:+.3f}")


if __name__ == "__main__":
    main()
