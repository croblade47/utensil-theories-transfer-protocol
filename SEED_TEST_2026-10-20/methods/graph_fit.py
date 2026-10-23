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
        constant run   the same number again and again           5 5 5 5 5 ...
        cycle          a motif of 2 to 256 numbers going round   A B C A B C ...
                       step rule: next = the number one round back.  Factors (1)
    STRAWBERRY: straight-line and steady-step expressions
        line           add the same step every time              3 7 11 15 19 ...
                       next = 2 x last - one before.             Factors (2, -1)
        curve          the step itself grows steadily            1 2 4 7 11 16 ...
                       next = 3 x last - 3 x one before + two before.
                                                                 Factors (3, -3, 1)
        woven          2 to 32 lines (or 2 to 8 curves) taking turns, e.g. a counter
                       stored as 2- or 4-byte numbers
        multiply-add   next = previous x m + c
    Library rule: an expression must keep working for at least one full round past
    its starting numbers (a cycle must go round at least twice). Otherwise a long
    "motif" seen only 1.1 times would just be a stored phrase plus a copy of its
    start, which is zip's look-back-and-copy trick and not the graph idea.

    LINE ROWS (the bit-level plot)
        Each row of the page is a plot of 0/1 points. Inside a stretch, a row may be
        a flat line: all 0 or all 1. In plain English text, for example, the top row
        is always 0. A row may also be a flat line with a few "dents", points that
        are off the line. A flat line costs one point. Each dent costs about one
        byte, because its position is written down. Rows that are neither are
        stored as they are.
    CUCUMBER: the odd one out
        A stretch, or the rows of it, that no fruit expression fits, stored exactly
        as it is.

WHAT THE SEED CONTAINS
    A list of records, one per stretch, in order. Each record starts with 1 byte:
    which library entry (top 4 bits) and a short length (bottom 4 bits). Longer
    lengths spill into 1 to 3 more bytes. Then come:
      orange / strawberry   the entry's settings (cycle length or number of woven
                            strands, if any), then the starting numbers
      cucumber              the bytes exactly as they are
      cucumber, flat rows   which rows are flat, their values, then the other rows
      cucumber, line rows   a 2-byte row plan (stored / line at 0 / line at 1 for
                            each row), the dent positions of each line row, then
                            the stored rows
    Nothing else: no file name, no hidden table, no copy of the original.

HOW THE CUTS ARE CHOSEN (planting side only)
    1. Every library expression is tried at every place in the data: cycles of
       length 1 to 256, woven lines with 1 to 32 strands, curves with 1 to 8
       strands, and multiply-add. Every stretch where one of them fits EXACTLY is
       listed.
    2. A shortest-path search ("dynamic programming") picks the stretches that make
       the whole seed smallest. The gaps between them are cucumber.
    3. Each cucumber gap is cut in two different ways: many short pieces with
       perfectly flat rows, or a few long pieces whose rows are lines with dents.
       The way that gives the smaller seed is kept. Each piece is then written in
       whichever cucumber form is smallest.
    4. The planting side grows the seed once itself, to prove the round trip is
       exact. (If that check ever failed, it would send the plain data instead, so
       the result is always exact.)

WHAT THIS CAN AND CANNOT DO (honest notes)
    - Data that really is a line, a curve or a repeating motif shrinks to almost
      nothing.
    - Ordinary text shrinks a little, mostly because some rows of its 0/1 page are
      flat lines (the top row of plain English is always 0, and the "32s" row is
      nearly always 1 except at capitals, brackets and line breaks). Words are not
      lines or cycles, so most of the text is still stored as it is.
    - It does NOT "look back and copy an earlier phrase", which is the main trick
      inside zip, and it does not give common letters shorter codes (zip's other
      trick). Both are different ideas from the graph/expression idea.
    - Random data has no shape. No expression fits it, so its seed comes out a few
      bytes BIGGER than the data.
    - grow() uses only the seed bytes and the fixed rules in this file.
      explain(seed) lists how much of the data each library entry covered.
"""

import re
from bisect import bisect_left
from collections import Counter, deque

NAME = "graph_fit"
SUMMARY = ("Cuts the data into stretches: a stretch that a small add/subtract/multiply "
           "expression regrows exactly (strawberry lines and curves, orange cycles) is "
           "stored as that expression, rows of the 0/1 page that are flat lines are "
           "stored as a line plus its dents, and the rest is stored as it is (cucumber).")


# =============================================================================
# THE SHARED LIBRARY: fixed rules both sides keep (placeholder names)
# =============================================================================

# Kinds of record (the top 4 bits of each record's first byte).
CUCUMBER = 0             # stretch stored exactly as it is
CUCUMBER_FLAT_ROWS = 1   # perfectly flat rows given once, the other rows stored as they are
ORANGE_CONSTANT = 2      # the same number repeated
ORANGE_CYCLE = 3         # a motif of p numbers going round (p = 2..256)
STRAWBERRY_LINE = 4      # add the same step each time
STRAWBERRY_CURVE = 5     # the step grows by the same amount each time
STRAWBERRY_WOVEN = 6     # p lines (or curves) taking turns
STRAWBERRY_MULTIPLY = 7  # next = previous x m + c
CUCUMBER_LINE_ROWS = 8   # some rows drawn as flat lines with dents, the others stored

KIND_NAMES = {
    CUCUMBER: "cucumber: stored as is",
    CUCUMBER_FLAT_ROWS: "cucumber with flat rows given once",
    CUCUMBER_LINE_ROWS: "cucumber with line rows (+dents)",
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

POPCOUNT = [bin(v).count("1") for v in range(256)]

# Inverse of every odd number mod 256 (used to find multiply-add steps).
INVERSE = [0] * 256
for _d in range(1, 256, 2):
    for _x in range(1, 256, 2):
        if (_d * _x) & 255 == 1:
            INVERSE[_d] = _x
            break

# Planting-side estimates only (they steer the search; grow() never uses them).
RAW_RESTART = 4.0       # extra seed bytes when a cucumber stretch is split by a fruit
DENT_COST = 1.0         # seed bytes per dent, roughly
PLAN_BLOCK = 512        # block size used to suggest row plans
MAX_PLANS = 24          # how many row plans the long-piece search considers


# =============================================================================
# Small helpers: numbers written as "varints" (7 bits per byte, a high bit
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
# Row tables for the 0/1 page.
# For a mask of rows that are NOT stored point by point, the other ("free") rows
# are stored: as_text[byte] = the byte's free-row points as text, top row first;
# back[text] = a byte with only those free-row points filled in.
# =============================================================================

_ROW_TABLES = {}

# _ROW_MARKS[r] turns each byte into 1 if its row-r point is 1, else 0.
_ROW_MARKS = [bytes((b >> r) & 1 for b in range(256)) for r in range(8)]


def _row_tables(mask):
    if mask not in _ROW_TABLES:
        free = [r for r in range(7, -1, -1) if not (mask >> r) & 1]
        width = len(free)
        free_bits = 255 ^ mask
        as_text = []
        for b in range(256):
            as_text.append("".join(str((b >> r) & 1) for r in free))
        back = {as_text[b]: b & free_bits for b in range(256)}
        _ROW_TABLES[mask] = (width, as_text, back)
    return _ROW_TABLES[mask]


def _unpack_free_rows(chunk, mask, length, nbits_before=0):
    """Read the free rows of `length` columns from packed bits (after nbits_before bits)."""
    width, _, back = _row_tables(mask)
    bits = bin(int.from_bytes(chunk, "big"))[2:].zfill(len(chunk) * 8) if chunk else ""
    if width == 0:
        return bits, [0] * length
    start = nbits_before
    return bits, [back[bits[i:i + width]] for i in range(start, start + length * width, width)]


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


def _take(seed, pos, count):
    chunk = seed[pos:pos + count]
    if len(chunk) != count:
        raise ValueError("seed ends early")
    return chunk, pos + count


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
            piece, pos = _take(seed, pos, field + 1)

        elif kind == CUCUMBER_FLAT_ROWS:
            length = field + 1
            mask = seed[pos]
            pos += 1
            if mask == 0:
                raise ValueError("bad flat-rows record")
            m = POPCOUNT[mask]
            width = 8 - m
            chunk, pos = _take(seed, pos, (m + length * width + 7) // 8)
            # the flat rows' single points come first, then the other rows
            bits, free_parts = _unpack_free_rows(chunk, mask, length, m)
            flat_byte = _row_tables(255 ^ mask)[2][bits[:m]]
            piece = bytes(flat_byte | f for f in free_parts)

        elif kind == CUCUMBER_LINE_ROWS:
            length = field + 1
            plan_bytes, pos = _take(seed, pos, 2)
            plan = plan_bytes[0] << 8 | plan_bytes[1]
            line_mask = line_byte = 0
            dents = []
            for r in range(7, -1, -1):
                code = (plan >> (2 * r)) & 3     # 0 stored, 1 line at 0, 2 line at 1
                if code == 0:
                    continue
                if code == 3:
                    raise ValueError("bad row plan")
                line_mask |= 1 << r
                if code == 2:
                    line_byte |= 1 << r
                count, pos = _read_varint(seed, pos)
                where = -1
                for _ in range(count):
                    gap, pos = _read_varint(seed, pos)
                    where += gap + 1
                    dents.append((where, 1 << r))
            width = 8 - POPCOUNT[line_mask]
            chunk, pos = _take(seed, pos, (length * width + 7) // 8)
            _, free_parts = _unpack_free_rows(chunk, line_mask, length)
            grown = bytearray(line_byte | f for f in free_parts)
            for where, bit in dents:
                if where >= length:
                    raise ValueError("dent outside the stretch")
                grown[where] ^= bit              # a dent: this point is off the line
            piece = bytes(grown)

        elif kind == ORANGE_CONSTANT:
            start, pos = _take(seed, pos, 1)
            piece = _grow_rule(start, 1, 1, field + 2)

        elif kind == ORANGE_CYCLE:
            p, pos = _read_varint(seed, pos)
            p += 2
            start, pos = _take(seed, pos, p)
            piece = _grow_rule(start, 1, p, field + 2 * p)

        elif kind in (STRAWBERRY_LINE, STRAWBERRY_CURVE):
            k = 2 if kind == STRAWBERRY_LINE else 3
            start, pos = _take(seed, pos, k)
            piece = _grow_rule(start, k, 1, field + k + 1)

        elif kind == STRAWBERRY_WOVEN:
            setting, pos = _read_varint(seed, pos)
            p, k = setting // 2 + 2, setting % 2 + 2
            start, pos = _take(seed, pos, k * p)
            piece = _grow_rule(start, k, p, field + (k + 1) * p)

        elif kind == STRAWBERRY_MULTIPLY:
            length = field + 4
            (y, m, c), pos = _take(seed, pos, 3)
            grown = bytearray([y])
            for _ in range(length - 1):
                y = (y * m + c) & 255
                grown.append(y)
            piece = bytes(grown)

        else:
            raise ValueError("unknown record kind %d" % kind)

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
    """For reports: {library entry: [records, original bytes covered, seed bytes used]}."""
    tally = {}
    _grow(bytes(seed), tally)
    return tally


# =============================================================================
# PLANT, part 1: fruit expressions (orange and strawberry)
# =============================================================================

def _rule_layout(rule):
    """
    For a fruit rule: (record kind, settings bytes, how many numbers the record
    stores, shortest stretch it may cover). rule is ("rec", k, p) for a step rule
    of order k and spacing p, or ("mul", m, c) for multiply-and-add.
    The shortest stretch is the library rule "at least one full round past the
    starting numbers".
    """
    if rule[0] == "mul":
        return STRAWBERRY_MULTIPLY, b"", 3, 4    # stores start, m, c
    _, k, p = rule
    if k == 1:
        if p == 1:
            kind, settings = ORANGE_CONSTANT, b""
        else:
            kind, settings = ORANGE_CYCLE, _varint(p - 2)
    elif p == 1:
        kind, settings = (STRAWBERRY_LINE if k == 2 else STRAWBERRY_CURVE), b""
    else:
        kind, settings = STRAWBERRY_WOVEN, _varint((p - 2) * 2 + (k - 2))
    return kind, settings, k * p, (k + 1) * p


def _fit_cost(rule, length):
    _, settings, stored, shortest = _rule_layout(rule)
    return _header_len(length - shortest) + len(settings) + stored


def _encode_fit(data, start, end, rule):
    kind, settings, stored, shortest = _rule_layout(rule)
    if rule[0] == "mul":
        body = bytes([data[start], rule[1], rule[2]])
    else:
        body = data[start:start + stored]
    return _header(kind, end - start - shortest) + settings + body


def _xor(a, b):
    """Byte-by-byte XOR: a zero byte means the two bytes were equal."""
    return (int.from_bytes(a, "big") ^ int.from_bytes(b, "big")).to_bytes(len(a), "big")


def _steps(a, p):
    """The step sizes between points p apart, mod 256."""
    return bytes([(x - y) & 255 for x, y in zip(a[p:], a)])


def _find_fits(data):
    """
    List every stretch where a fruit expression fits exactly.
    Returns a sorted list of (start, end_inclusive, rule), at most one rule per stretch.
    """
    n = len(data)
    best = {}

    def consider(s, e, rule):
        length = e - s + 1
        if length < _rule_layout(rule)[3]:
            return
        c = _fit_cost(rule, length)
        if c > length - 2:                 # must beat plain storage by at least 2 bytes
            return
        old = best.get((s, e))
        if old is None or c < old[0]:
            best[(s, e)] = (c, rule)

    def scan(residual, k, p):
        # residual[i] == 0 means the rule (k, p) correctly predicts point i + k*p.
        # A fit must last at least p more points (one full round) and save 2+ bytes.
        _, settings, _, _ = _rule_layout(("rec", k, p))
        pattern = re.compile(b"\x00{%d,}" % max(p, 3 + len(settings)))
        for hit in pattern.finditer(residual):
            consider(hit.start(), hit.end() - 1 + k * p, ("rec", k, p))

    # ORANGE: each point equals the point p back
    for p in range(1, min(MAX_CYCLE, n - 1) + 1):
        scan(_xor(data[p:], data[:-p]), 1, p)
    # STRAWBERRY lines (the step from p back stays the same) and
    # curves (the change of step stays the same)
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


# =============================================================================
# PLANT, part 2: cucumber pieces and their rows
# =============================================================================

def _pack_free_rows(block, mask, prefix=""):
    """Pack the free rows (rows not in mask) of every byte, after some prefix bits."""
    _, as_text, _ = _row_tables(mask)
    bits = prefix + "".join([as_text[b] for b in block])
    if not bits:
        return b""
    bits += "0" * (-len(bits) % 8)
    return int(bits, 2).to_bytes(len(bits) // 8, "big")


def _dent_bytes(positions):
    """Dent count, then the gaps between dents."""
    out = bytearray(_varint(len(positions)))
    prev = -1
    for where in positions:
        out += _varint(where - prev - 1)
        prev = where
    return bytes(out)


def _encode_cucumber(data, start, end):
    """Write one cucumber piece in whichever cucumber form is smallest."""
    block = data[start:end]
    length = len(block)
    options = [_header(CUCUMBER, length - 1) + block]

    flat_mask = 0
    line_rows = {}                        # row -> (line value, dent bytes)
    for r in range(8):
        marks = block.translate(_ROW_MARKS[r])
        ones = marks.count(1)
        if ones == 0 or ones == length:
            flat_mask |= 1 << r
        base = 0 if ones <= length - ones else 1
        if min(ones, length - ones) + 1 < length / 8:    # a dented line might beat storing
            positions = [hit.start() for hit in re.finditer(b"\x00" if base else b"\x01", marks)]
            dents = _dent_bytes(positions)
            if len(dents) * 8 < length:
                line_rows[r] = (base, dents)

    if flat_mask:
        flat_points = _row_tables(255 ^ flat_mask)[1][block[0]]
        options.append(_header(CUCUMBER_FLAT_ROWS, length - 1) + bytes([flat_mask]) +
                       _pack_free_rows(block, flat_mask, flat_points))
    if line_rows:
        plan = line_mask = 0
        dents = bytearray()
        for r in range(7, -1, -1):
            if r in line_rows:
                base, row_dents = line_rows[r]
                plan |= (1 + base) << (2 * r)
                line_mask |= 1 << r
                dents += row_dents
        options.append(_header(CUCUMBER_LINE_ROWS, length - 1) + bytes([plan >> 8, plan & 255]) +
                       bytes(dents) + _pack_free_rows(block, line_mask))
    return min(options, key=len)


def _cut_short(data, lo, hi):
    """
    Way 1: cut data[lo:hi] into short pieces with perfectly flat rows.
    Dynamic programming over end points x: cost[x] = fewest seed bytes for the
    first x bytes of the range. For each end point a short list of good start
    points is tried:
      - the places where a row stops being flat (looking backwards from x),
      - for each number of flat rows t, the start point that was cheapest so far
        among those that still allow t flat rows (kept in a sliding window),
      - the start of the best piece ending one byte earlier.
    Returns a list of (start, end, mask of flat rows).
    """
    n = hi - lo
    cost = [0] * (n + 1)
    choice = [None] * (n + 1)
    q = [-1] * 8    # q[r]: last local index whose row-r point differs from the newest byte's
    windows = [deque() for _ in range(9)]   # windows[t]: (score, start) candidates for t flat rows
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

        # rows grouped by where they stop being flat (looking backwards from x)
        groups = {}
        for r in range(8):
            groups[q[r]] = groups.get(q[r], 0) | (1 << r)
        breaks = sorted(groups)
        flat_after = []          # flat_after[i]: rows flat for any start > breaks[i]
        flat = 0
        for v in breaks:
            flat |= groups[v]
            flat_after.append(flat)

        def flat_rows(j):        # rows that are flat on the local range [j, x)
            i = bisect_left(breaks, j) - 1
            return flat_after[i] if i >= 0 else 0

        starts = {}
        for i, v in enumerate(breaks):
            starts[v + 1] = flat_after[i]
            if v >= 0:
                starts[v] = flat_after[i - 1] if i > 0 else 0
        starts.setdefault(0, flat_rows(0))
        if x > 1:
            j0 = choice[x - 1][0]
            starts[j0] = flat_rows(j0)
        # sliding windows: start x-1 joins; starts too early for t flat rows leave
        order = sorted(q)
        for t in range(9):
            score = 8 * cost[x - 1] - (x - 1) * (8 - t)
            w = windows[t]
            while w and w[-1][0] >= score:
                w.pop()
            w.append((score, x - 1))
            if t:
                earliest = order[t - 1] + 1
                while w[0][1] < earliest:
                    w.popleft()
            j = w[0][1]
            if j not in starts:
                starts[j] = flat_rows(j)

        best = None
        best_c = None
        for j, mask in starts.items():
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


def _rough_plan(block):
    """A suggested row plan for a block: per row (top first) None = store, 0/1 = line."""
    length = len(block)
    plan = []
    for r in range(7, -1, -1):
        ones = block.translate(_ROW_MARKS[r]).count(1)
        if min(ones, length - ones) * DENT_COST + 1 < length / 8:
            plan.append(1 if ones > length - ones else 0)
        else:
            plan.append(None)
    return tuple(plan)


def _cut_long(data, lo, hi, short_pieces):
    """
    Way 2: cut data[lo:hi] into a few long pieces whose rows are lines with dents.
    A handful of row plans is suggested (from blocks of the data and from the
    short pieces), then a shortest-path search over the bytes (Viterbi style)
    decides where to switch from one plan to another.
    Returns a list of (start, end).
    """
    n = hi - lo
    weight = Counter()
    for s in range(lo, hi, PLAN_BLOCK):
        block = data[s:min(hi, s + PLAN_BLOCK)]
        weight[_rough_plan(block)] += len(block)
    for s, e, mask in short_pieces:
        if mask:
            plan = tuple((data[s] >> r) & 1 if (mask >> r) & 1 else None for r in range(7, -1, -1))
            weight[plan] += e - s
    plans = [plan for plan, _ in weight.most_common(MAX_PLANS)]
    if (None,) * 8 not in plans:
        plans.append((None,) * 8)

    # estimated seed bytes per byte for each plan, and to start a piece with it
    per_byte, start_cost = [], []
    for plan in plans:
        stored = plan.count(None)
        table = []
        for b in range(256):
            c = stored / 8
            for idx, r in enumerate(range(7, -1, -1)):
                if plan[idx] is not None and ((b >> r) & 1) != plan[idx]:
                    c += DENT_COST
            table.append(c)
        per_byte.append(table)
        start_cost.append(2 + (0 if stored == 8 else 2 + (8 - stored)))

    count = len(plans)
    began = bytearray(n * count)      # began[x*count+i] = 1: plan i's piece started at byte x
    best_before = bytearray(n)        # which plan's piece ended just before byte x
    current = [float("inf")] * count
    for x in range(n):
        b = data[lo + x]
        if x == 0:
            closed, closed_plan = 0.0, 0
        else:
            closed = min(current)
            closed_plan = current.index(closed)
        best_before[x] = closed_plan
        nxt = []
        base = x * count
        for i in range(count):
            fresh = closed + start_cost[i]
            if fresh < current[i]:
                nxt.append(fresh + per_byte[i][b])
                began[base + i] = 1
            else:
                nxt.append(current[i] + per_byte[i][b])
        current = nxt
    plan_now = current.index(min(current))
    pieces = []
    end = x = n
    while x > 0:
        x -= 1
        if began[x * count + plan_now]:
            pieces.append((lo + x, lo + end))
            end = x
            plan_now = best_before[x]
    pieces.reverse()
    return pieces


def _cut_cucumber(data, lo, hi):
    """Cut a cucumber gap both ways and keep the smaller. Returns [(start, end, record)]."""
    short = _cut_short(data, lo, hi)
    way1 = [(s, e, _encode_cucumber(data, s, e)) for s, e, _ in short]
    way2 = [(s, e, _encode_cucumber(data, s, e)) for s, e in _cut_long(data, lo, hi, short)]
    size1 = sum(len(rec) for _, _, rec in way1)
    size2 = sum(len(rec) for _, _, rec in way2)
    return way1 if size1 <= size2 else way2


# =============================================================================
# PLANT, part 3: choose fruit stretches vs cucumber, then write the seed
# =============================================================================

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
        by_start.setdefault(s, []).append((e, rule, _rule_layout(rule)[3]))
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
            for e, rule, shortest in (active if landed else new):
                length = e - i + 1
                if length < shortest:
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


SELF_CHECK_FALLBACKS = 0   # planting-side diagnostic only; grow() never reads it


def plant(data: bytes) -> bytes:
    """Original data -> seed."""
    global SELF_CHECK_FALLBACKS
    data = bytes(data)
    n = len(data)
    if n == 0:
        return b""

    # 1. First guess: everything cucumber. Gives an estimated cost for each byte.
    whole = _cut_cucumber(data, 0, n)
    weight = [0.0] * n
    for s, e, record in whole:
        per = len(record) / (e - s)
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
            pieces = whole if (s, e) == (0, n) else _cut_cucumber(data, s, e)
            for _, _, record in pieces:
                out += record
        else:
            out += _encode_fit(data, s, e, rule)
    seed = bytes(out)

    # 5. Prove the round trip here before sending. If it ever failed (it should
    #    not), send one plain cucumber record instead, so the result is always exact.
    if _grow(seed) != data:
        SELF_CHECK_FALLBACKS += 1
        seed = _header(CUCUMBER, n - 1) + data
    return seed
