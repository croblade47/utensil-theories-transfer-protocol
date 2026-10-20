"""
graph_backwards: the owner's "data seed" graph idea, solved BACKWARDS from the data.

PLACEHOLDER NAMES (please read first)
    "strawberry", "orange" and "cucumber" in this file are PLACEHOLDER names for the
    shared library of factors. The owner has not shared their own factors yet. The
    three entries below are this file's best guess at what such a library could hold.
    When the owner shares their real factors, they should replace these placeholders.

1. A PAGE OF BINARY
    Every byte of a file is 8 binary points (each 0 or 1). Write all the points of a
    file in one long line, byte after byte, biggest place first, and you have the
    file's "page of binary". Regrowing the file exactly means regrowing that page
    exactly, point for point.

2. GROWING A PAGE FROM AN EXPRESSION (forwards: what the receiver does)
    An expression here is a step rule plus a few unknowns (the "?" marks in the
    owner's example seed "[+2x y(27/5.2+t=y/?)/(?\\y=t+2.5\\72)yx2]"). The receiver
    solves the rule step by step. Each step uses only adding, subtracting,
    multiplying, and "mod" (keep the remainder, so every answer stays a whole number).
    Each step plots points that are 0 or 1, and the points stack up into a page.
    The same expression always grows the same page. Nothing random, no AI.

    STRAWBERRY: a rule for the points themselves.
        next point = (c1 x point 1 back + c2 x point 2 back + ... + cL x point L back) mod 2
        The unknowns are L, the factors c1..cL (each 0 or 1) and the first L points.
        Example: L = 1, c1 = 1, first point 0  ->  0 0 0 0 0 0 ...
        A rule like this with L = 48 can regrow "ABC123ABC123..." forever.

    ORANGE: a rule for whole numbers (0 to 255), each plotted as its 8 points.
        next number = (a x the number k steps back + c) mod 256
        The unknowns are k (1 to 255), a, c and the first k numbers.
        Examples: k=1, a=1, c=0 -> 7 7 7 7 ...   k=1, a=1, c=1 -> 0 1 2 3 4 ...
                  k=6, a=1, c=0, first numbers "ABC123" -> ABC123ABC123ABC123 ...

    CUCUMBER: the odd one out. A stretch that no strawberry or orange expression fits
        is stored exactly as it is (with a flag saying so).

3. WORKING BACKWARDS (planting: what the sender does)
    The sender walks through the data and, at each place, solves BACKWARDS from the
    data to the unknowns, instead of guessing:
      - Strawberry is solved with the Berlekamp-Massey method (a known piece of
        maths from 1968). Given a run of points, it directly computes the SHORTEST
        strawberry rule that regrows them. No trial and error.
      - Orange is solved with remainder arithmetic. Two neighbouring steps give
        "a x (difference back then) = (difference now)  mod 256", which is solved
        for a straight from a precomputed answer table; then c follows. The rule is
        then run forward to see how far it keeps matching the data exactly.
      - Strawberry rules can also be "run backwards": once a rule is found, the
        sender checks whether it also explains the bytes just BEFORE where it was
        found, and if so starts the stretch earlier.
    A stretch is cut out ("a block") wherever an expression regrows it exactly AND
    writing the expression down costs fewer bytes than the stretch itself. Every
    other byte is cucumber. Search budgets (how far back k may reach, how long a
    strawberry rule may be, how often strawberry is tried) are fixed below so planting
    stays within about a minute on the test files.

4. WHAT THE SEED CONTAINS (and nothing else)
    A list of records, one per block, in order. Each record starts with one number
    (1 to 3 bytes) that holds the block's length in bytes and which library entry it
    uses. Then:
      cucumber:   the bytes themselves.
      strawberry: L, then the factors c1..cL and the first L points, packed 8 to a byte.
      orange:     k and which kind of (a, c) it is, then a and/or c if needed, then
                  the first k numbers.
    No file name, no hidden table, no copy of the original. The receiver needs only
    the seed and the rules written in this file.

5. WHAT TO EXPECT (honestly)
    Orange and strawberry rules regrow data that REPEATS or COUNTS (runs, cycles,
    steady steps). That is the only kind of data a short rule can regrow exactly. On
    ordinary text, compressed files (like .docx) and random bytes, almost no stretch
    can be regrown by a rule cheaper than the stretch itself, so most of it stays
    cucumber. Also note: orange with a=1, c=0 means "repeat the last k bytes", which is
    the same trick ordinary zip uses for repeats; gains on text come mainly from that.
"""

NAME = "graph_backwards"
SUMMARY = ("Works backwards from the data to small add/multiply/mod expressions whose "
           "page of 0/1 points equals a stretch exactly (strawberry: a 0/1 point rule "
           "solved by Berlekamp-Massey; orange: a number rule solved by remainder "
           "arithmetic), and stores stretches no expression fits as they are (cucumber).")


# ===========================================================================
# THE SHARED LIBRARY: fixed rules and constants both sides keep. Never sent.
# ===========================================================================

CUCUMBER = 0      # record kind: bytes stored as they are
STRAWBERRY = 1    # record kind: a 0/1 point rule (linear recurrence mod 2)
ORANGE = 2        # record kind: a number rule (affine recurrence mod 256)

# Orange "forms": which of a and c are written in the seed.
ORANGE_REPEAT = 0  # a = 1, c = 0   (nothing written: "repeat the number k back")
ORANGE_SHIFT = 1   # a = 1, c given (1 byte)
ORANGE_FULL = 2    # a and c given  (2 bytes)

# Search budgets (sender side only; they never change how a seed is read).
OR_KMAX = 255          # orange may reach back at most 255 numbers
OR_MIN_STEPS = 3       # an orange block must regrow at least 3 numbers by its rule
SB_STEP = 16           # inside cucumber areas, try strawberry every 16 bytes
SB_WINDOW_BYTES = 128  # strawberry looks at up to 128 bytes (1,024 points) at once
SB_MIN_BYTES = 8       # ... and at least 8 bytes
SB_MAX_L = 480         # longest strawberry rule searched for (points looked back)
SB_STABLE_BITS = 64    # a rule must predict 64 points in a row before it is run onward
JUMP_GAIN = 64         # a block saving 64+ bytes is not searched inside again
RAW_HEADER_GUESS = 2   # cucumber header size the cut planner assumes (1 to 3 bytes)


# ---------------------------------------------------------------------------
# Small helpers shared by both sides
# ---------------------------------------------------------------------------

try:                                   # count the 1s in a whole number's binary form
    _ones = int.bit_count              # fast, Python 3.10 and newer
except AttributeError:                 # older Pythons (old laptops)
    def _ones(x):
        return bin(x).count("1")


def _varint(n):
    """Write a whole number in 7-bit pieces (small numbers take 1 byte)."""
    out = bytearray()
    while True:
        piece = n & 0x7F
        n >>= 7
        if n:
            out.append(piece | 0x80)
        else:
            out.append(piece)
            return bytes(out)


def _varint_len(n):
    size = 1
    while n >= 0x80:
        n >>= 7
        size += 1
    return size


def _read_varint(seed, pos):
    value, shift = 0, 0
    while True:
        b = seed[pos]
        pos += 1
        value |= (b & 0x7F) << shift
        shift += 7
        if not b & 0x80:
            return value, pos


# ===========================================================================
# GROWING SIDE (the receiver): seed -> page of points -> original bytes
# ===========================================================================

def strawberry_page(L, taps, start_bits, length):
    """Grow `length` bytes (8 x length points) from a strawberry rule.

    Point j for j < L is given (bit j of start_bits). After that, every new point is
        (c1 x point j-1 + c2 x point j-2 + ... + cL x point j-L) mod 2,
    where ci is bit (i-1) of taps. `state` holds the last L points (newest at bit 0),
    so "multiply and add, mod 2" is: count the 1s in (state AND taps), keep odd/even.
    """
    out = bytearray()
    mask = (1 << L) - 1
    state = 0
    byte = 0
    for j in range(8 * length):
        if j < L:
            point = (start_bits >> j) & 1
        else:
            point = _ones(state & taps) & 1
        state = ((state << 1) | point) & mask
        byte = (byte << 1) | point
        if j & 7 == 7:                      # 8 points stacked -> one byte of the page
            out.append(byte)
            byte = 0
    return bytes(out)


_AFFINE_CACHE = {}


def _affine_table(a, c):
    """The orange step for every possible number: x -> (a*x + c) mod 256."""
    table = _AFFINE_CACHE.get((a, c))
    if table is None:
        table = bytes(((a * x + c) & 0xFF) for x in range(256))
        _AFFINE_CACHE[(a, c)] = table
    return table


def orange_numbers(k, a, c, start, length):
    """Grow `length` numbers: the first k are given, then y[t] = (a*y[t-k] + c) mod 256."""
    y = bytearray(start[:length])
    if len(y) >= length:
        return bytes(y)
    if a == 1 and c == 0:                   # plain repeat: copy the first k numbers round
        return (bytes(start) * (length // k + 1))[:length]
    table = _affine_table(a, c)
    while len(y) < length:                  # the next k numbers come from the last k
        y += bytes(y[-k:]).translate(table)
    return bytes(y[:length])


def _records(seed):
    """Read the seed record by record: yields (kind, length, settings)."""
    pos = 0
    while pos < len(seed):
        head, pos = _read_varint(seed, pos)
        kind, length = head & 3, head >> 2
        if kind == CUCUMBER:
            yield kind, length, (seed[pos:pos + length],)
            pos += length
        elif kind == STRAWBERRY:
            L, pos = _read_varint(seed, pos)
            nbytes = (2 * L + 7) // 8
            packed = int.from_bytes(seed[pos:pos + nbytes], "little")
            pos += nbytes
            taps = packed & ((1 << L) - 1)       # factors c1..cL
            start_bits = packed >> L             # first L points
            yield kind, length, (L, taps, start_bits)
        elif kind == ORANGE:
            kf, pos = _read_varint(seed, pos)
            k, form = kf >> 2, kf & 3
            if form == ORANGE_REPEAT:
                a, c = 1, 0
            elif form == ORANGE_SHIFT:
                a, c = 1, seed[pos]
                pos += 1
            elif form == ORANGE_FULL:
                a, c = seed[pos], seed[pos + 1]
                pos += 2
            else:
                raise ValueError("unknown orange form in seed")
            start = seed[pos:pos + k]
            pos += k
            yield kind, length, (k, a, c, start)
        else:
            raise ValueError("unknown record kind in seed")


def grow(seed: bytes) -> bytes:
    """Seed -> original bytes, using only the seed and the rules in this file."""
    out = bytearray()
    for kind, length, settings in _records(seed):
        if kind == CUCUMBER:
            out += settings[0]
        elif kind == STRAWBERRY:
            out += strawberry_page(settings[0], settings[1], settings[2], length)
        else:
            k, a, c, start = settings
            out += orange_numbers(k, a, c, start, length)
    return bytes(out)


def describe(seed: bytes, examples: int = 3) -> dict:
    """Count the blocks in a seed: how many were found by working backwards.

    Reads only the seed. Returns block counts and bytes covered per library entry,
    plus a few found expressions written out in plain form. "rule_bytes" counts only
    what the rules themselves grew: a found block's stored starting numbers/points
    are copied from the seed, so they are NOT counted there.
    """
    stats = {"blocks": 0, "found_blocks": 0, "bytes": 0, "found_bytes": 0,
             "rule_bytes": 0.0,
             "strawberry_blocks": 0, "strawberry_bytes": 0,
             "orange_blocks": 0, "orange_bytes": 0,
             "cucumber_blocks": 0, "cucumber_bytes": 0, "examples": []}
    for kind, length, settings in _records(seed):
        stats["blocks"] += 1
        stats["bytes"] += length
        name = ("cucumber", "strawberry", "orange")[kind]
        stats[name + "_blocks"] += 1
        stats[name + "_bytes"] += length
        if kind != CUCUMBER:
            stats["found_blocks"] += 1
            stats["found_bytes"] += length
            if kind == STRAWBERRY:
                stats["rule_bytes"] += min(length, max(0.0, length - settings[0] / 8))
            else:
                stats["rule_bytes"] += length - min(settings[0], length)
            if len(stats["examples"]) < examples:
                if kind == STRAWBERRY:
                    L, taps, _ = settings
                    terms = [f"p[t-{i}]" for i in range(1, L + 1) if (taps >> (i - 1)) & 1]
                    rule = (f"strawberry: p[t] = ({' + '.join(terms) or '0'}) mod 2, "
                            f"L={L}, {length} bytes")
                else:
                    k, a, c, start = settings
                    rule = (f"orange: y[t] = ({a}*y[t-{k}] + {c}) mod 256, "
                            f"first numbers {bytes(start[:12])!r}{'...' if k > 12 else ''}, "
                            f"{length} bytes")
                stats["examples"].append(rule)
    return stats


# ===========================================================================
# PLANTING SIDE (the sender): original bytes -> seed, by working backwards
# ===========================================================================

def _strawberry_cost(L, length):
    """Seed bytes for one strawberry block."""
    return _varint_len(length * 4 + STRAWBERRY) + _varint_len(L) + (2 * L + 7) // 8


def _orange_cost(k, form, length):
    """Seed bytes for one orange block."""
    extra = (0, 1, 2)[form]
    return _varint_len(length * 4 + ORANGE) + _varint_len(k * 4 + form) + extra + k


class _Tables:
    """Precomputed answer tables used by the sender to solve orange backwards."""

    def __init__(self):
        # MUL[a]: x -> a*x mod 256, for every x (lets a whole slice be multiplied at once)
        self.MUL = [bytes(((a * x) & 0xFF) for x in range(256)) for a in range(256)]
        # SOL[u][v]: every a with a*u = v (mod 256). This "solves backwards" for a.
        self.SOL = [[[] for _ in range(256)] for _ in range(256)]
        for u in range(256):
            row = self.SOL[u]
            for a in range(256):
                row[(a * u) & 0xFF].append(a)
        self.SOL = [[tuple(cell) for cell in row] for row in self.SOL]


def _longest(pred, good, limit):
    """Largest m in [good, limit] with pred(m) True, given pred(good) is True and
    pred only ever goes from True to False as m grows. Gallops, then halves."""
    if good >= limit:
        return limit
    step = 16
    while True:
        m = good + step
        if m >= limit:
            if pred(limit):
                return limit
            bad = limit
            break
        if pred(m):
            good = m
            step *= 2
        else:
            bad = m
            break
    while bad - good > 1:
        mid = (good + bad) // 2
        if pred(mid):
            good = mid
        else:
            bad = mid
    return good


def _orange_search(data, D, p, T):
    """Orange blocks starting exactly at byte p (the best one for short, medium and
    long reach-back, so the cut planner has choices).

    Works backwards: for each reach-back k, the data's own differences give
    a x D[p] = D[p+k] (mod 256), which is solved for a with the SOL table; c follows
    from the first step; then the rule is run forward to see how far it matches.
    Returns a list of (gain, start, length, ORANGE, (k, form, a, c)).
    """
    n = len(data)
    kmax = min(OR_KMAX, n - p - OR_MIN_STEPS)
    if kmax < 1:
        return []
    dp0, dp1 = D[p], D[p + 1]

    # Quick filter (exact, no guessing): if a rule with reach-back k exists, then
    # D[q+1]*D[p] = D[q]*D[p+1] (mod 256) with q = p+k. Test every k at once.
    if dp0 or dp1:
        X = D[p + 2:p + 2 + kmax].translate(T.MUL[dp0])
        Y = D[p + 1:p + 1 + kmax].translate(T.MUL[dp1])
        z = (int.from_bytes(X, "big") ^ int.from_bytes(Y, "big")).to_bytes(kmax, "big")
        lags = []
        i = z.find(0)
        while i >= 0:
            lags.append(i + 1)
            i = z.find(0, i + 1)
    else:
        lags = range(1, kmax + 1)

    best = {}            # reach-back group (short / medium / long) -> best block
    top_gain = 0
    for k in lags:
        if top_gain >= n - p - k:           # no longer reach-back can do better
            break
        q = p + k
        # --- solve for the factor a (backwards, from the data's differences) ---
        if dp0:
            cands = [a for a in T.SOL[dp0][D[q]] if (a * dp1) & 0xFF == D[q + 1]]
        elif dp1:
            if D[q]:
                continue
            cands = T.SOL[dp1][D[q + 1]]
        else:
            if D[q] or D[q + 1]:
                continue
            cands = (1,)
            j = 2
            while j < 8 and q + j <= n - 2:  # look a little further for a non-flat step
                if D[p + j]:
                    cands = T.SOL[D[p + j]][D[q + j]]
                    break
                if D[q + j]:
                    cands = ()
                    break
                j += 1
        group = 0 if k <= 8 else (1 if k <= 64 else 2)
        for a in cands:
            c = (data[q] - a * data[p]) & 0xFF
            if a == 1 and c == 0:
                form = ORANGE_REPEAT

                def pred(m, p=p, q=q):
                    return data[q:q + m] == data[p:p + m]
            else:
                form = ORANGE_SHIFT if a == 1 else ORANGE_FULL
                table = _affine_table(a, c)

                def pred(m, p=p, q=q, table=table):
                    return data[q:q + m] == data[p:p + m].translate(table)
            if not pred(OR_MIN_STEPS):
                continue
            m = _longest(pred, OR_MIN_STEPS, n - q)   # numbers grown by the rule
            length = k + m
            gain = length - _orange_cost(k, form, length)
            if gain > 0 and (group not in best or gain > best[group][0]):
                best[group] = (gain, p, length, ORANGE, (k, form, a, c))
                top_gain = max(top_gain, gain)
    return list(best.values())


def _strawberry_holds(data, C, L, lo, hi):
    """True if every point j in [lo, hi) of the data's page obeys the rule C."""
    if lo >= hi:
        return True
    b0, b1 = (lo - L) // 8, (hi + 7) // 8
    R = int.from_bytes(data[b0:b1], "big")
    top = 8 * b1 - 1
    for j in range(lo, hi):
        if _ones(C & (R >> (top - j))) & 1:
            return False
    return True


def _strawberry_run_on(data, pos, taps, L, state):
    """Run a strawberry rule forward from byte pos; count bytes that match exactly."""
    mask = (1 << L) - 1
    n = len(data)
    count = 0
    while pos + count < n:
        byte = 0
        for _ in range(8):
            point = _ones(state & taps) & 1
            state = ((state << 1) | point) & mask
            byte = (byte << 1) | point
        if byte != data[pos + count]:
            break
        count += 1
    return count


def _strawberry_search(data, p, earliest, bar):
    """Best strawberry block found from byte p (it may be moved to start earlier,
    but not before `earliest`).

    Berlekamp-Massey reads the page point by point and keeps the SHORTEST rule
    C(x) = 1 + c1 x + ... + cL x^L that regrows every point read so far. At each
    whole byte we note what a block ending there would save. If the rule is still
    predicting at the end of the window, it is run onward through the data.
    Returns (gain, start, length, STRAWBERRY, (L, C)) or None.
    """
    n = len(data)
    wbytes = min(SB_WINDOW_BYTES, n - p)
    if wbytes < SB_MIN_BYTES:
        return None
    N = 8 * wbytes
    R = int.from_bytes(data[p:p + wbytes], "big")   # bit (N-1-j) is point j
    C, B, L, m = 1, 1, 0, 1
    last_miss = -1
    best, best_gain = None, 0
    aborted = False
    for t in range(N):
        # Does the current rule predict point t? (R >> (N-1-t)) puts point t-i at bit i.
        if _ones(C & (R >> (N - 1 - t))) & 1:
            last_miss = t
            if 2 * L <= t:                       # rule must get longer
                C, B = C ^ (B << m), C
                L = t + 1 - L
                m = 1
            else:                                # same length, corrected factors
                C ^= B << m
                m += 1
        else:
            m += 1
        if t & 7 == 7:
            nbytes = (t + 1) >> 3
            gain = nbytes - _strawberry_cost(L, nbytes)
            if gain > best_gain:
                best_gain, best = gain, (nbytes, C, L)
        if L > SB_MAX_L:
            aborted = True
            break

    # Run a steady rule onward past the window, if that could beat what we have.
    if (not aborted and p + wbytes < n and N - 1 - last_miss >= SB_STABLE_BITS
            and (n - p) - _strawberry_cost(L, n - p) > max(best_gain, bar)):
        more = _strawberry_run_on(data, p + wbytes, C >> 1, L, R & ((1 << L) - 1))
        total = wbytes + more
        gain = total - _strawberry_cost(L, total)
        if gain > best_gain:
            best_gain, best = gain, (total, C, L)
    if best is None:
        return None

    # Run the rule BACKWARDS: does it also explain the bytes just before p?
    total, C, L = best
    end_bit = 8 * (p + total)
    start = p
    while start > earliest:
        lo = 8 * (start - 1) + L
        hi = min(8 * start + L, end_bit)
        if not _strawberry_holds(data, C, L, lo, hi):
            break
        start -= 1
    length = p + total - start
    return (length - _strawberry_cost(L, length), start, length, STRAWBERRY, (L, C))


def _find_blocks(data, D, T):
    """Planting step 1: at every place in the data, work backwards to the blocks
    (expressions) that could start there. Returns {start: [block, ...]}."""
    n = len(data)
    found = {}
    i, next_sb = 0, 0
    skip_from = skip_to = 0
    while i < n:
        here = _orange_search(data, D, i, T)
        top = max(here) if here else None
        if i >= next_sb:                        # strawberry is slower: every SB_STEP bytes
            next_sb = i + SB_STEP
            sb = _strawberry_search(data, i, max(0, i - SB_STEP), top[0] if top else 0)
            if sb:
                found.setdefault(sb[1], []).append(sb)
                if top is None or sb[0] > top[0]:
                    top = sb
        if here:
            found.setdefault(i, []).extend(here)
        # Deep inside the rule-grown part of a very long block nothing new can start
        # that beats it, so skip to just before its end (where a next block might
        # begin). The first 2 strawberry tries inside it are still made, in case a
        # shorter rule starts there.
        if top and top[0] >= JUMP_GAIN:
            grown_from = top[1] + (top[4][0] if top[3] == ORANGE else (top[4][0] + 7) // 8)
            grown_from += 2 * SB_STEP
            ahead = top[1] + top[2] - OR_KMAX - 8
            if ahead > grown_from and ahead > skip_to:
                skip_from, skip_to = grown_from, ahead
        i += 1
        if skip_from <= i < skip_to:
            i = skip_to
    return found


def _choose_cuts(n, found):
    """Planting step 2: choose which blocks to use, and where to cut them short, so the
    whole seed is as small as possible (dynamic programming, from the end backwards).

    F[i] = fewest seed bytes for data[i:] when a new record starts at i.
    G[i] = the same, when a cucumber record is already open at i (its header paid).
    A block may be cut short anywhere after its first rule step, so for each block
    we need the smallest F[j] over a range of ends j: a small "tournament tree" keeps
    those minimums. Returns, for each i, the block to use (or None for cucumber).
    """
    size = 1
    while size < n + 1:
        size *= 2
    BIG = 1 << 62
    tree = [BIG] * (2 * size)
    M = n + 1                                   # pack (F value, end) into one number

    def put(j, value):
        pos = j + size
        tree[pos] = value * M + (n - j)         # ties go to the longer block
        pos >>= 1
        while pos:
            a, b = tree[2 * pos], tree[2 * pos + 1]
            tree[pos] = a if a < b else b
            pos >>= 1

    def smallest(lo, hi):                       # min over ends lo..hi (inclusive)
        res = BIG
        lo += size
        hi += size + 1
        while lo < hi:
            if lo & 1:
                if tree[lo] < res:
                    res = tree[lo]
                lo += 1
            if hi & 1:
                hi -= 1
                if tree[hi] < res:
                    res = tree[hi]
            lo >>= 1
            hi >>= 1
        return res

    G = [0] * (n + 1)
    pick_new = [None] * (n + 1)
    pick_open = [None] * (n + 1)
    put(n, 0)
    for i in range(n - 1, -1, -1):
        best, pick = BIG, None
        for block in found.get(i, ()):
            _, start, length, kind, settings = block
            if kind == ORANGE:
                k, form = settings[0], settings[1]
                cost = _orange_cost(k, form, length)
                lo = start + k + OR_MIN_STEPS
            else:
                L = settings[0]
                cost = _strawberry_cost(L, length)
                lo = start + max(1, (L + 7) // 8)
            hi = start + length
            if lo > hi:
                continue
            v = smallest(lo, hi)
            if cost + v // M < best:
                best, pick = cost + v // M, (block, n - v % M)
        keep_raw = 1 + G[i + 1]                 # one more cucumber byte
        if best < keep_raw:
            G[i], pick_open[i] = best, pick
        else:
            G[i] = keep_raw
        new_raw = RAW_HEADER_GUESS + keep_raw   # open a new cucumber record here
        if best <= new_raw:
            F_i = best
            pick_new[i] = pick
        else:
            F_i = new_raw
        put(i, F_i)
    return pick_new, pick_open


def _encode(data, block, end):
    """Write one found block, cut to end at byte `end`, as seed bytes."""
    _, start, _, kind, settings = block
    length = end - start
    if kind == ORANGE:
        k, form, a, c = settings
        out = _varint(length * 4 + ORANGE) + _varint(k * 4 + form)
        if form == ORANGE_SHIFT:
            out += bytes([c])
        elif form == ORANGE_FULL:
            out += bytes([a, c])
        return out + data[start:start + k]          # the first k numbers
    L, C = settings
    taps = C >> 1                                   # c1..cL
    start_bits = 0                                  # the first L points of the block
    first = int.from_bytes(data[start:start + (L + 7) // 8], "big")
    width = 8 * ((L + 7) // 8)
    for j in range(L):
        start_bits |= ((first >> (width - 1 - j)) & 1) << j
    packed = taps | (start_bits << L)
    return (_varint(length * 4 + STRAWBERRY) + _varint(L)
            + packed.to_bytes((2 * L + 7) // 8, "little"))


def _cucumber(chunk):
    return _varint(len(chunk) * 4 + CUCUMBER) + chunk


def plant(data: bytes) -> bytes:
    """Original bytes -> seed, by working backwards from the data to expressions."""
    data = bytes(data)
    n = len(data)
    if n == 0:
        return b""
    T = _Tables()
    # D[i] = (data[i+1] - data[i]) mod 256: the step from each number to the next.
    D = bytes(((data[i + 1] - data[i]) & 0xFF) for i in range(n - 1))

    found = _find_blocks(data, D, T)            # step 1: work backwards everywhere
    pick_new, pick_open = _choose_cuts(n, found)  # step 2: choose the cuts

    parts = []                                  # step 3: write the seed
    i, raw_from = 0, None
    while i < n:
        pick = pick_new[i] if raw_from is None else pick_open[i]
        if pick is None:                        # this byte is cucumber
            if raw_from is None:
                raw_from = i
            i += 1
            continue
        if raw_from is not None:
            parts.append(_cucumber(data[raw_from:i]))
            raw_from = None
        block, end = pick
        parts.append(_encode(data, block, end))
        i = end
    if raw_from is not None:
        parts.append(_cucumber(data[raw_from:n]))
    seed = b"".join(parts)

    # Safety net: check the seed regrows the data exactly. If it ever did not, the
    # whole file would be stored as cucumber instead (never seen in testing).
    if grow(seed) != data:
        seed = _cucumber(data)
    return seed


if __name__ == "__main__":
    # Try it on your own files:  python graph_backwards.py file1 file2 ...
    import sys
    import time
    for path in sys.argv[1:]:
        with open(path, "rb") as f:
            original = f.read()
        t0 = time.perf_counter()
        s = plant(original)
        t1 = time.perf_counter()
        ok = grow(s) == original
        t2 = time.perf_counter()
        info = describe(s)
        print(f"{path}: {len(original):,} -> {len(s):,} bytes, exact={ok}, "
              f"plant {t1 - t0:.1f}s, grow {t2 - t1:.1f}s")
        print(f"   blocks {info['blocks']}, found by working backwards "
              f"{info['found_blocks']} (strawberry {info['strawberry_blocks']}, "
              f"orange {info['orange_blocks']}), cucumber {info['cucumber_blocks']}; "
              f"bytes in found blocks {info['found_bytes']:,} of {info['bytes']:,}, "
              f"of which grown by rule steps (not stored starts) {info['rule_bytes']:,.0f}")
        for e in info["examples"]:
            print("   e.g.", e)
