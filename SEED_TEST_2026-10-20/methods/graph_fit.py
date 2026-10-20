"""
graph_fit: the owner's "data seed" graph idea, read as "the expression IS the shape
of the data".

PLACEHOLDER NAMES
    "strawberry", "orange" and "cucumber" in this file are PLACEHOLDER names for the
    shared library of factors. The owner has not shared their own factors yet. When
    they do, their factors should replace these placeholders.

THE PAGE OF BINARY
    Every byte of a file is a number from 0 to 255, which is 8 binary points (each 0
    or 1) stacked in a column. Put the columns side by side and you get a "page of
    binary": 8 rows tall, one column per byte. Row 7 (the top) is the 128s place,
    row 0 (the bottom) is the 1s place.

GROWING A PAGE FROM AN EXPRESSION
    Here an expression is a few starting numbers plus a fixed step rule. The rule
    works out the next number from earlier numbers by adding, subtracting and
    multiplying, keeping only the last 8 binary places ("mod 256"). Solving it step
    by step gives one number per step. Each number is written down as its 8 binary
    points, stacked into the next column of the page. The same expression always
    grows the same page. Every step rule here can also be run backwards.

THE SHARED LIBRARY (both sides keep it; it is written in this file and never sent)
    ORANGE: round, repeating expressions
        constant run   the same number again and again        5 5 5 5 5 ...
        cycle          a motif of 2 to 256 numbers going round  A B C A B C ...
                       step rule: next = the number one round back.  Factors (1)
    STRAWBERRY: straight-line and steady-step expressions
        line           add the same step every time            3 7 11 15 19 ...
                       next = 2 x (last) - (one before).        Factors (2, -1)
        curve          the step itself grows steadily          1 2 4 7 11 16 ...
                       next = 3 x last - 3 x one before + two before.  Factors (3, -3, 1)
        woven          2 to 32 lines (or 2 to 8 curves) taking turns, e.g. a counter
                       stored as 2- or 4-byte numbers
        multiply-add   next = previous x m + c
    FLAT ROWS (the bit-level plot)
        Inside a stretch, one row of the page may be flat: all 0 or all 1. In plain
        English text, for example, the top row is always 0. A flat row is a straight
        line in the 0/1 plot, so it costs one point for the whole stretch instead of
        one point per column. The rows that are not flat are stored as they are.
    CUCUMBER: the odd one out
        A stretch (or the rows of it) that no fruit expression fits, stored exactly
        as it is.

WHAT THE SEED CONTAINS
    A list of records, one per stretch, in order. Each record holds:
      - 1 byte: which library entry (top 4 bits) and a short length (bottom 4
        bits). Longer lengths spill into 1 to 3 more bytes.
      - the entry's settings, if it has any (cycle length, number of woven lines);
      - then the starting numbers (orange, strawberry), or the mask of flat rows
        followed by their values and the points of the other rows (half cucumber),
        or the bytes themselves (cucumber).
    Nothing else: no file name, no hidden table, no copy of the original.

HOW THE CUTS ARE CHOSEN (planting side only)
    1. Every library expression is tried at every place in the data: cycles of
       length 1 to 256, woven lines with 1 to 32 strands, curves with 1 to 8
       strands, and multiply-add. Every stretch where one of them fits EXACTLY is
       listed.
    2. A shortest-path search ("dynamic programming") picks the stretches that make
       the whole seed smallest. The gaps between the chosen stretches are cucumber.
    3. Each cucumber gap is cut again into pieces, so that the flat rows in each
       piece can be left out.
    4. The planting side grows the seed once itself, to prove the round trip is
       exact. (If that check ever failed, it would send the plain data instead, so
       the result is always exact.)

WHAT THIS CAN AND CANNOT DO (honest notes)
    - Data that really is a line, a curve or a repeating motif shrinks to almost
      nothing.
    - Ordinary text shrinks a little, mostly because flat rows (such as the top
      row of plain English) are left out. Words are not lines or cycles, so most
      text ends up as cucumber.
    - It does NOT "look back and copy an earlier phrase", which is the main trick
      inside zip, because that is a different idea from the graph/expression idea.
    - Random data has no shape. No expression fits it, so its seed comes out a few
      bytes BIGGER than the data.
    - grow() uses only the seed bytes and the fixed rules in this file.
"""

import re

NAME = "graph_fit"
SUMMARY = ("Cuts the data into stretches: a stretch that a small add/subtract/multiply "
           "expression regrows exactly (strawberry lines and curves, orange cycles) is "
           "stored as that expression, flat 0/1 rows are stored once, and the rest is "
           "stored as it is (cucumber).")


# =============================================================================
# THE SHARED LIBRARY: fixed rules both sides keep (placeholder names)
# =============================================================================

# Kinds of record (the top 4 bits of each record's first byte).
CUCUMBER = 0             # stretch stored exactly as it is
HALF_CUCUMBER = 1        # flat rows given once, the other rows stored as they are
ORANGE_CONSTANT = 2      # the same number repeated
ORANGE_CYCLE = 3         # a motif of p numbers going round (p = 2..256)
STRAWBERRY_LINE = 4      # add the same step each time
STRAWBERRY_CURVE = 5     # the step grows by the same amount each time
STRAWBERRY_WOVEN = 6     # p lines (or curves) taking turns
STRAWBERRY_MULTIPLY = 7  # next = previous x m + c

KIND_NAMES = {
    CUCUMBER: "cucumber (stored as is)",
    HALF_CUCUMBER: "half cucumber (flat 0/1 rows given once)",
    ORANGE_CONSTANT: "orange: constant run",
    ORANGE_CYCLE: "orange: repeating cycle",
    STRAWBERRY_LINE: "strawberry: straight line",
    STRAWBERRY_CURVE: "strawberry: curve",
    STRAWBERRY_WOVEN: "strawberry: woven lines/curves",
    STRAWBERRY_MULTIPLY: "strawberry: multiply-and-add",
}

# Step-rule factors. A rule of "order k" with spacing p says:
#     next = f1 x (point p back) + f2 x (point 2p back) + ... , mod 256
# Spacing p = 1 is a single line or curve; a bigger p means p strands taking turns.
FACTORS = {
    1: (1,),         # orange: repeat the point one round back
    2: (2, -1),      # strawberry line: keep the same step
    3: (3, -3, 1),   # strawberry curve: keep the same change of step
}

MAX_CYCLE = 256         # longest orange motif searched
MAX_WOVEN_LINES = 32    # most strands for woven lines
MAX_WOVEN_CURVES = 8    # most strands for woven curves
RAW_RESTART = 2.5       # planting estimate: extra bytes when a cucumber stretch is split

POPCOUNT = [bin(v).count("1") for v in range(256)]

# Inverse of every odd number mod 256 (used to find multiply-add steps).
INVERSE = [0] * 256
for _d in range(1, 256, 2):
    for _x in range(1, 256, 2):
        if (_d * _x) & 255 == 1:
            INVERSE[_d] = _x
            break


# =============================================================================
# Small helpers: lengths written as "varints" (7 bits per byte, a high bit
# meaning "more bytes follow")
# =============================================================================

def _varint(n):
    out = bytearray()
    while True:
        low = n & 127
        n >>= 7
        if n:
            out.append(low | 128)
        else:
            out.append(low)
            return bytes(out)


def _varint_len(n):
    size = 1
    while n >= 128:
        n >>= 7
        size += 1
    return size


def _read_varint(seed, pos):
    n = shift = 0
    while True:
        b = seed[pos]
        pos += 1
        n |= (b & 127) << shift
        if b < 128:
            return n, pos
        shift += 7


def _header(kind, field):
    """First byte = kind (top 4 bits) + field (bottom 4 bits); field 15 means 'see next bytes'."""
    if field < 15:
        return bytes([kind << 4 | field])
    return bytes([kind << 4 | 15]) + _varint(field - 15)


def _header_len(field):
    return 1 if field < 15 else 1 + _varint_len(field - 15)


# =============================================================================
# Flat-row tables (bit-level plot). For a mask of flat rows, the "free" rows are
# the others. extract: byte -> its free-row points packed together (top row first).
# deposit: packed points -> a byte with those points put back in the free rows.
# =============================================================================

_ROW_TABLES = {}


def _row_tables(mask):
    if mask not in _ROW_TABLES:
        free = [r for r in range(7, -1, -1) if not (mask >> r) & 1]
        width = len(free)
        free_bits = 255 ^ mask
        extract = []
        for b in range(256):
            v = 0
            for r in free:
                v = (v << 1) | ((b >> r) & 1)
            extract.append(v)
        as_text = [format(v, "0%db" % width) if width else "" for v in extract]
        # points (as text) -> byte with only the free rows filled in
        back = {as_text[b]: b & free_bits for b in range(256)}
        _ROW_TABLES[mask] = (width, as_text, back)
    return _ROW_TABLES[mask]


# =============================================================================
# GROW: seed -> original. Uses only the seed bytes and the fixed rules above.
# =============================================================================

def _grow_rule(start, k, p, length):
    """Solve an order-k, spacing-p step rule from its starting numbers, one step at a time."""
    if k == 1:                                   # orange: just go round the motif
        motif = bytes(start)
        return (motif * (length // len(motif) + 1))[:length]
    y = bytearray(start)
    factors = FACTORS[k]
    for j in range(k * p, length):
        v = 0
        for i, f in enumerate(factors):
            v += f * y[j - (i + 1) * p]
        y.append(v & 255)                        # keep the last 8 binary places
    return bytes(y[:length])


def _grow(seed, tally=None):
    out = bytearray()
    pos = 0
    while pos < len(seed):
        record_start = pos
        first = seed[pos]
        pos += 1
        kind, field = first >> 4, first & 15
        if field == 15:
            extra, pos = _read_varint(seed, pos)
            field = 15 + extra

        if kind == CUCUMBER:
            length = field + 1
            piece = seed[pos:pos + length]
            if len(piece) != length:
                raise ValueError("seed ends early")
            pos += length

        elif kind == HALF_CUCUMBER:
            length = field + 1
            mask = seed[pos]
            pos += 1
            m = POPCOUNT[mask]
            width, _, back = _row_tables(mask)
            nbytes = (m + length * width + 7) // 8
            chunk = seed[pos:pos + nbytes]
            if len(chunk) != nbytes or mask == 0:
                raise ValueError("bad half-cucumber record")
            pos += nbytes
            bits = bin(int.from_bytes(chunk, "big"))[2:].zfill(nbytes * 8)
            # the flat rows' single points come first
            flat_byte = _row_tables(255 ^ mask)[2][bits[:m]]
            if width == 0:
                piece = bytes([flat_byte]) * length
            else:
                piece = bytes(flat_byte | back[bits[i:i + width]]
                              for i in range(m, m + length * width, width))

        elif kind == ORANGE_CONSTANT:
            length = field + 1
            piece = _grow_rule(seed[pos:pos + 1], 1, 1, length)
            pos += 1

        elif kind == ORANGE_CYCLE:
            p, pos = _read_varint(seed, pos)
            p += 2
            length = field + p
            piece = _grow_rule(seed[pos:pos + p], 1, p, length)
            pos += p

        elif kind in (STRAWBERRY_LINE, STRAWBERRY_CURVE):
            k = 2 if kind == STRAWBERRY_LINE else 3
            length = field + k
            piece = _grow_rule(seed[pos:pos + k], k, 1, length)
            pos += k

        elif kind == STRAWBERRY_WOVEN:
            setting, pos = _read_varint(seed, pos)
            p, k = setting // 2 + 2, setting % 2 + 2
            length = field + k * p
            piece = _grow_rule(seed[pos:pos + k * p], k, p, length)
            pos += k * p

        elif kind == STRAWBERRY_MULTIPLY:
            length = field + 3
            y, m, c = seed[pos], seed[pos + 1], seed[pos + 2]
            pos += 3
            grown = bytearray([y])
            for _ in range(length - 1):
                y = (y * m + c) & 255
                grown.append(y)
            piece = bytes(grown)

        else:
            raise ValueError("unknown record kind %d" % kind)

        if pos > len(seed):
            raise ValueError("seed ends early")
        out += piece
        if tally is not None:
            row = tally.setdefault(KIND_NAMES[kind], [0, 0, 0])
            row[0] += 1                      # records
            row[1] += len(piece)             # original bytes regrown
            row[2] += pos - record_start     # seed bytes used
    return bytes(out)


def grow(seed: bytes) -> bytes:
    """Seed -> original data."""
    return _grow(bytes(seed))


def explain(seed: bytes) -> dict:
    """For reports: {kind name: [records, original bytes covered, seed bytes used]}."""
    tally = {}
    _grow(bytes(seed), tally)
    return tally


# =============================================================================
# PLANT: original -> seed
# =============================================================================

def _rule_layout(rule):
    """(record kind, settings bytes, how many numbers the record stores) for a fruit rule."""
    if rule[0] == "mul":
        return STRAWBERRY_MULTIPLY, b"", 3       # start, m, c
    _, k, p = rule
    if k == 1:
        if p == 1:
            return ORANGE_CONSTANT, b"", 1
        return ORANGE_CYCLE, _varint(p - 2), p
    if p == 1:
        return (STRAWBERRY_LINE if k == 2 else STRAWBERRY_CURVE), b"", k
    return STRAWBERRY_WOVEN, _varint((p - 2) * 2 + (k - 2)), k * p


def _fit_cost(rule, length):
    _, settings, stored = _rule_layout(rule)
    return _header_len(length - stored) + len(settings) + stored


def _encode_fit(data, start, end, rule):
    kind, settings, stored = _rule_layout(rule)
    if rule[0] == "mul":
        body = bytes([data[start], rule[1], rule[2]])
    else:
        body = data[start:start + stored]
    return _header(kind, end - start - stored) + settings + body


def _piece_cost(length, mask):
    """Seed bytes for a cucumber piece; mask = its flat rows (0 = stored fully as is)."""
    h = _header_len(length - 1)
    if mask == 0:
        return h + length
    m = POPCOUNT[mask]
    return h + 1 + (m + length * (8 - m) + 7) // 8


def _encode_piece(data, start, end, mask):
    length = end - start
    if mask == 0:
        return _header(CUCUMBER, length - 1) + data[start:end]
    _, as_text, _ = _row_tables(mask)
    flat_text = _row_tables(255 ^ mask)[1][data[start]]       # the flat rows' points
    bits = flat_text + "".join([as_text[b] for b in data[start:end]])
    bits += "0" * (-len(bits) % 8)
    packed = int(bits, 2).to_bytes(len(bits) // 8, "big")
    return _header(HALF_CUCUMBER, length - 1) + bytes([mask]) + packed


def _plan_rows(data, lo, hi):
    """
    Cut data[lo:hi] into cucumber pieces, choosing for each piece which rows of the
    0/1 page are flat (and so given once). Dynamic programming over end points.
    Candidate start points: the places where a row stops being flat, the start of
    the range, and the start of the best piece ending one byte earlier.
    Returns a list of (start, end, mask).
    """
    n = hi - lo
    cost = [0] * (n + 1)
    choice = [None] * (n + 1)
    q = [-1] * 8            # q[r]: last local index whose row-r point differs from the newest byte's
    prev = None
    for x in range(1, n + 1):
        b = data[lo + x - 1]
        if prev is not None:
            flips = b ^ prev
            r = 0
            while flips:
                if flips & 1:
                    q[r] = x - 2
                flips >>= 1
                r += 1
        prev = b
        # rows grouped by where they stop being flat (going backwards)
        groups = {}
        for r in range(8):
            groups[q[r]] = groups.get(q[r], 0) | (1 << r)
        cands = []
        flat = 0
        for v in sorted(groups):
            flat |= groups[v]
            cands.append((v + 1, flat))         # start just after v: rows with q <= v are flat
        if cands[0][0] > 0:
            cands.append((0, 0))
        if x > 1:
            j0 = choice[x - 1][0]
            cands.append((j0, sum(bits for v, bits in groups.items() if v < j0)))
        best = None
        best_c = None
        for j, mask in cands:
            length = x - j
            h = 1 if length <= 15 else 1 + _varint_len(length - 16)
            c_raw = cost[j] + h + length
            if best_c is None or c_raw < best_c:
                best_c, best = c_raw, (j, 0)
            if mask:
                m = POPCOUNT[mask]
                c = cost[j] + h + 1 + (m + length * (8 - m) + 7) // 8
                if c < best_c:
                    best_c, best = c, (j, mask)
        cost[x] = best_c
        choice[x] = best
    pieces = []
    x = n
    while x > 0:
        j, mask = choice[x]
        pieces.append((lo + j, lo + x, mask))
        x = j
    pieces.reverse()
    return pieces


def _xor(a, b):
    """Byte-by-byte XOR: a zero byte means the two bytes were equal."""
    return (int.from_bytes(a, "big") ^ int.from_bytes(b, "big")).to_bytes(len(a), "big")


def _steps(a, p):
    """The step sizes between points p apart, mod 256."""
    return bytes([(x - y) & 255 for x, y in zip(a[p:], a)])


def _find_fits(data):
    """
    List every stretch where a fruit expression fits exactly.
    Returns a list of (start, end_inclusive, rule), at most one rule per stretch.
    """
    n = len(data)
    best = {}

    def consider(s, e, rule):
        length = e - s + 1
        c = _fit_cost(rule, length)
        if c > length - 2:                 # must beat plain storage by at least 2 bytes
            return
        old = best.get((s, e))
        if old is None or c < old[0]:
            best[(s, e)] = (c, rule)

    def scan(residual, k, p):
        # residual[i] == 0 means the rule (k, p) correctly predicts point i + k*p
        _, settings, _ = _rule_layout(("rec", k, p))
        pattern = re.compile(b"\x00{%d,}" % (3 + len(settings)))
        for hit in pattern.finditer(residual):
            consider(hit.start(), hit.end() - 1 + k * p, ("rec", k, p))

    # ORANGE: point equals the point p back
    for p in range(1, min(MAX_CYCLE, n - 1) + 1):
        scan(_xor(data[p:], data[:-p]), 1, p)
    # STRAWBERRY lines (step p back is the same) and curves (change of step is the same)
    for p in range(1, MAX_WOVEN_LINES + 1):
        if 2 * p >= n:
            break
        d = _steps(data, p)
        scan(_xor(d[p:], d[:-p]), 2, p)
        if p <= MAX_WOVEN_CURVES and 3 * p < n:
            dd = _steps(d, p)
            scan(_xor(dd[p:], dd[:-p]), 3, p)
    # STRAWBERRY multiply-and-add: next = previous x m + c (m found when it is unique)
    j = 2
    while j < n:
        y0, y1, y2 = data[j - 2], data[j - 1], data[j]
        d0 = (y1 - y0) & 255
        if d0 & 1:
            m = (((y2 - y1) & 255) * INVERSE[d0]) & 255
            if m > 1:                      # m = 0 or 1 are constants and lines, found above
                c = (y1 - m * y0) & 255
                k = j + 1
                last = y2
                while k < n and data[k] == (m * last + c) & 255:
                    last = data[k]
                    k += 1
                if k - (j - 2) >= 6:
                    consider(j - 2, k - 1, ("mul", m, c))
                    j = k
                    continue
        j += 1
    return sorted((s, e, rule) for (s, e), (_, rule) in best.items())


def _choose_stretches(data, fits, weight):
    """
    Shortest-path search: which fruit stretches to use and where cucumber goes.
    weight[i] = estimated seed bytes for byte i if it stays cucumber.
    Returns a list of (start, end_exclusive, rule or None for cucumber).
    """
    n = len(data)
    inf = float("inf")
    at_cut = [inf] * (n + 1)       # best cost with a record ending exactly here
    in_raw = [inf] * (n + 1)       # best cost with a cucumber stretch still open here
    how_cut = [None] * (n + 1)     # "raw" or (fit start, rule)
    raw_began = [False] * (n + 1)
    at_cut[0] = 0.0
    by_start = {}
    for s, e, rule in fits:
        by_start.setdefault(s, []).append((e, rule, _rule_layout(rule)[2]))
    active = []
    for i in range(n + 1):
        if in_raw[i] < at_cut[i]:
            at_cut[i] = in_raw[i]
            how_cut[i] = "raw"
        here = at_cut[i]
        new = by_start.get(i)
        if new:
            active.extend(new)
        landed = how_cut[i] is not None and how_cut[i] != "raw"
        if new or landed:
            # a fit may start where its stretch starts, or right where another fit ended
            active = [a for a in active if a[0] > i]
            for e, rule, stored in (active if landed else new):
                length = e - i + 1
                if length <= stored:
                    continue
                c = here + _fit_cost(rule, length)
                if c < at_cut[e + 1]:
                    at_cut[e + 1] = c
                    how_cut[e + 1] = (i, rule)
        if i < n:
            go_on = in_raw[i] + weight[i]
            begin = here + RAW_RESTART + weight[i]
            if go_on <= begin:
                in_raw[i + 1] = go_on
            else:
                in_raw[i + 1] = begin
                raw_began[i + 1] = True
    # walk back along the cheapest path
    stretches = []
    i, inside_raw, raw_end = n, False, 0
    while i > 0:
        if not inside_raw:
            how = how_cut[i]
            if how == "raw":
                inside_raw, raw_end = True, i
            else:
                start, rule = how
                stretches.append((start, i, rule))
                i = start
        else:
            if raw_began[i]:
                stretches.append((i - 1, raw_end, None))
                inside_raw = False
            i -= 1
    stretches.reverse()
    return stretches


def plant(data: bytes) -> bytes:
    """Original data -> seed."""
    data = bytes(data)
    n = len(data)
    if n == 0:
        return b""

    # 1. First guess: all cucumber (with flat rows). Gives a cost per byte.
    whole = _plan_rows(data, 0, n)
    weight = [0.0] * n
    for s, e, mask in whole:
        per = _piece_cost(e - s, mask) / (e - s)
        for i in range(s, e):
            weight[i] = per

    # 2. Every stretch where a fruit expression fits exactly.
    fits = _find_fits(data)

    # 3. Choose the cheapest mix of fruit stretches and cucumber.
    stretches = _choose_stretches(data, fits, weight) if fits else [(0, n, None)]

    # 4. Write the records.
    out = bytearray()
    for s, e, rule in stretches:
        if rule is None:
            pieces = whole if (s, e) == (0, n) else _plan_rows(data, s, e)
            for ps, pe, mask in pieces:
                out += _encode_piece(data, ps, pe, mask)
        else:
            out += _encode_fit(data, s, e, rule)
    seed = bytes(out)

    # 5. Prove the round trip here before sending. If it ever failed (it should
    #    not), send one plain cucumber record instead, so the result is always exact.
    if _grow(seed) != data:
        global SELF_CHECK_FALLBACKS
        SELF_CHECK_FALLBACKS += 1
        seed = _encode_piece(data, 0, n, 0)
    return seed


SELF_CHECK_FALLBACKS = 0   # planting-side diagnostic only; grow() never reads it
