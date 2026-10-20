"""
GRAPH_LOCATE: the page of 0/1 plot points is fixed; the seed is a list of plot points.

This is one reading ("interpretation B") of the owner's graph method, written so it can
be tested fairly. Python 3 standard library only. No AI, no network, no zip/lzma/bz2.

PLACEHOLDER NOTICE
    "strawberry", "orange" and "cucumber" below are PLACEHOLDER names. The owner has not
    shared their own library factors yet. The numbers inside each page are built from
    numbers the owner likes (17, 32, 16, 34, 47, 27, 72). When the owner shares their real
    factors, they can be dropped into LIBRARY below without changing anything else.

1. HOW A PAGE OF BINARY GROWS FROM AN EXPRESSION
    Each library page is one fixed expression, solved step by step with whole numbers
    (adding, subtracting, multiplying, and keeping the remainder):

        y  <-  ( y x 2 x TIMES  +  27 x t  +  72  -  MINUS )  remainder after dividing by 2,147,483,647
        t  <-  t + 1

    (It loosely echoes the owner's example "+2xy ... 27 ... t ... 72".)
    After every step we plot ONE point: one binary digit of y (digit number DIGIT),
    which is either 0 or 1. Stacking the plotted points gives a long page of binary:
        0110100111010001011...
    The same expression always gives the same page, on any computer, because only
    whole numbers are used (no rounding). Both sides can regrow the page in under a second.

2. THE LIBRARY (the shared rules both sides keep)
    Three pages: the strawberry page, the orange page and the cucumber page. Each one is
    the expression above with its own TIMES, MINUS, starting value and plotted DIGIT.
    The chunk size (16 bits) and the longest page allowed are also library rules.

3. PLANT (original data -> seed)
    a. Cut the data's bits into chunks of 16 bits (2 bytes each). A chunk of 16 bits can
       be any one of 65,536 different patterns.
    b. For each chunk, look along the page for the first place where that exact
       16-bit pattern appears. That place is the chunk's PLOT POINT.
       (We index the page once, so finding a chunk is instant.)
    c. Write down the plot point. Two ways of numbering plot points are tried:
         - "plain position": the step number where the pattern starts on the page.
         - "compact number": only count the useful spots on the page, i.e. the spots where
           a pattern shows up for the FIRST time (spot 0, spot 1, ... spot 65,535).
           This is the smallest honest way to name a plot point.
    d. If a chunk's pattern never appears on the page, it is stored as it is, with a flag.
    e. A last odd byte (if the data has an odd number of bytes) is stored as it is.
    f. Every page (strawberry, orange, cucumber) and both numbering styles are tried;
       the smallest seed is kept, and the seed says which page and style were used.

4. WHAT THE SEED CONTAINS (every byte the receiver needs, nothing else)
    An empty file gives an empty seed. Otherwise:
      byte 0 : which page (0 strawberry, 1 orange, 2 cucumber)        -> bits 0-1
               numbering style (0 plain position, 1 compact number)    -> bit 2
               "some chunks are stored as-is" flag                      -> bit 3
      byte 1 : how many bits each plot point uses in this seed (W)
      then   : the original length in bytes (a few bytes, 7 bits per byte)
      then   : the plot points, W bits each, one per 16-bit chunk
               (if the flag is on: plot point number 0 means "16 raw bits follow",
                and every other number is the plot point plus 1)
      then   : the last odd byte as it is, if any, padded with 0 bits to a whole byte.

5. GROW (seed -> original data)
    Read the header, regrow the chosen page from its expression, then for every plot
    point read the 16 bits sitting at that spot on the page, and stack them up.
    grow() uses only the seed plus the fixed rules in this file.

6. WHAT THE MEASUREMENTS SHOW (and why)
    To be able to point at ANY of the 65,536 possible 16-bit chunks, the page needs
    65,536 different useful spots, and picking one out of 65,536 spots takes exactly
    16 bits: the same as the chunk itself. Plain positions cost more (about 17-20 bits
    per 16-bit chunk), because the page has to run for roughly a million steps before
    every pattern has shown up, and numbers that large need about 20 binary digits.
    Bigger chunks do not help: a 24-bit chunk needs a page of hundreds of millions of
    steps, and with a page we can grow in seconds most 24-bit chunks are missing.
    Using several pages does not help either: picking the best of 3 pages saves about
    1.6 bits of position but costs about 1.6 bits to say which page was picked.
    So with a fixed page, the seed comes out the same size as the data or a little
    bigger, for every kind of file. Run this file directly to see the numbers:
        python3 graph_locate.py some_file.txt
"""

NAME = "graph_locate"
SUMMARY = ("A fixed page of 0/1 plot points grows from a library expression; the seed "
           "lists, for each 16-bit chunk, the plot point where that chunk sits on the page.")


# ---------------------------------------------------------------------------
# THE SHARED LIBRARY (fixed rules; both sides keep an identical copy)
# ---------------------------------------------------------------------------

MODULUS = 2_147_483_647          # keep the remainder after dividing by this (a prime number)
CHUNK_BITS = 16                  # each chunk of data is 16 bits = 2 bytes
ALL_PATTERNS = 1 << CHUNK_BITS   # 65,536 possible 16-bit patterns
MAX_PAGE_STEPS = 2_000_000       # a page stops here even if some pattern never showed up

# PLACEHOLDER factors. Names and numbers are stand-ins until the owner shares the real ones.
LIBRARY = [
    {"name": "strawberry", "start": 17, "times": 17 * 32 * 16 * 34 * 47, "minus": 16 * 34, "digit": 16},
    {"name": "orange",     "start": 32, "times": 47 * 34 * 27 * 72 + 1,  "minus": 17 * 47, "digit": 15},
    {"name": "cucumber",   "start": 47, "times": 17 * 16 * 47 * 27 * 72, "minus": 34 * 47, "digit": 14},
]

PLAIN, COMPACT = 0, 1            # the two ways of numbering a plot point


def grow_page(page_number):
    """Solve one library expression step by step and plot one 0/1 point per step.

    Returns three things:
      page        - the plotted points, one 0 or 1 per step (a bytearray of 0s and 1s)
      first_spot  - for each of the 65,536 patterns, the step where it FIRST appears
                    on the page (or -1 if it never appears)
      new_spots   - the list of useful spots in page order: new_spots[n] is where the
                    n-th never-seen-before pattern starts (the "compact numbers")
    The page stops as soon as every pattern has appeared, or at MAX_PAGE_STEPS.
    """
    factors = LIBRARY[page_number]
    y = factors["start"]
    times_two = 2 * factors["times"]
    minus = factors["minus"]
    digit = factors["digit"]

    page = bytearray()
    first_spot = [-1] * ALL_PATTERNS
    new_spots = []
    window = 0                                   # the last 16 points plotted, as a number
    for t in range(MAX_PAGE_STEPS):
        y = (y * times_two + 27 * t + 72 - minus) % MODULUS    # solve one step
        point = (y >> digit) & 1                                # plot one point: 0 or 1
        page.append(point)
        window = ((window << 1) | point) & (ALL_PATTERNS - 1)
        if t >= CHUNK_BITS - 1:                  # a full 16-point stretch is on the page
            start = t - (CHUNK_BITS - 1)
            if first_spot[window] < 0:           # first time this pattern is seen
                first_spot[window] = start
                new_spots.append(start)
                if len(new_spots) == ALL_PATTERNS:
                    break                        # every pattern is on the page: stop
    return page, first_spot, new_spots


# ---------------------------------------------------------------------------
# Small helpers: writing and reading bits, and writing a length
# ---------------------------------------------------------------------------

def _write_length(n):
    """Write a whole number using 7 bits per byte; the top bit says 'more bytes follow'."""
    out = bytearray()
    while True:
        low = n & 0x7F
        n >>= 7
        if n:
            out.append(low | 0x80)
        else:
            out.append(low)
            return bytes(out)


def _read_length(seed, i):
    n = shift = 0
    while True:
        b = seed[i]
        i += 1
        n |= (b & 0x7F) << shift
        shift += 7
        if not b & 0x80:
            return n, i


def _bits_to_bytes(bit_text):
    """'0110...' -> bytes, padding the end with 0 bits up to a whole byte."""
    if not bit_text:
        return b""
    pad = (-len(bit_text)) % 8
    bit_text += "0" * pad
    return int(bit_text, 2).to_bytes(len(bit_text) // 8, "big")


def _bytes_to_bits(data):
    return "".join(format(b, "08b") for b in data)


def _cut_into_chunks(data):
    """Cut data into 16-bit chunks (2 bytes each). An odd last byte is returned separately."""
    whole = len(data) // 2 * 2
    chunks = [(data[i] << 8) | data[i + 1] for i in range(0, whole, 2)]
    tail = data[whole:]
    return chunks, tail


# ---------------------------------------------------------------------------
# PLANT: original -> seed
# ---------------------------------------------------------------------------

def _make_seed(data_length, chunks, tail, page_number, style, first_spot, compact_number):
    """Build one candidate seed for one page and one numbering style."""
    # The plot point for each chunk (or None if the pattern is not on this page).
    if style == PLAIN:
        points = [first_spot[c] if first_spot[c] >= 0 else None for c in chunks]
    else:
        points = [compact_number[c] if compact_number[c] >= 0 else None for c in chunks]

    some_missing = any(p is None for p in points)
    if some_missing:
        codes = [0 if p is None else p + 1 for p in points]     # 0 = "stored as it is"
    else:
        codes = points
    width = max(codes).bit_length() if codes else 0              # W: bits per plot point
    width = max(width, 1) if codes else 0

    parts = []
    fmt = "0%db" % width if width else ""
    for c, code in zip(chunks, codes):
        parts.append(format(code, fmt))
        if some_missing and code == 0:
            parts.append(format(c, "016b"))                      # the raw chunk itself
    parts.append(_bytes_to_bits(tail))                           # odd last byte, as it is

    header = bytes([page_number | (style << 2) | (int(some_missing) << 3), width])
    return header + _write_length(data_length) + _bits_to_bytes("".join(parts))


def plant(data: bytes) -> bytes:
    """Turn data into a seed: a list of plot points on one fixed library page."""
    if not data:
        return b""                               # nothing to send
    chunks, tail = _cut_into_chunks(data)
    best = None
    for page_number in range(len(LIBRARY)):      # try strawberry, orange, cucumber
        page, first_spot, new_spots = grow_page(page_number)
        compact_number = [-1] * ALL_PATTERNS     # pattern -> its compact spot number
        for n, spot in enumerate(new_spots):
            compact_number[_read_pattern(page, spot)] = n
        for style in (PLAIN, COMPACT):           # try both numbering styles
            seed = _make_seed(len(data), chunks, tail, page_number, style,
                              first_spot, compact_number)
            if best is None or len(seed) < len(best):
                best = seed                      # keep the smallest seed
    return best


def _read_pattern(page, spot):
    """Read the 16 points sitting at one spot on the page, as a number."""
    value = 0
    for point in page[spot:spot + CHUNK_BITS]:
        value = (value << 1) | point
    return value


# ---------------------------------------------------------------------------
# GROW: seed -> original (runs on the receiving side with ONLY the seed)
# ---------------------------------------------------------------------------

def grow(seed: bytes) -> bytes:
    if not seed:
        return b""
    page_number = seed[0] & 0b11
    style = (seed[0] >> 2) & 1
    some_missing = (seed[0] >> 3) & 1
    width = seed[1]
    data_length, i = _read_length(seed, 2)
    bits = _bytes_to_bits(seed[i:])

    page, first_spot, new_spots = grow_page(page_number)     # regrow the same page

    out = bytearray()
    at = 0                                                    # reading place in the bit list
    for _ in range(data_length // 2):
        code = int(bits[at:at + width], 2)
        at += width
        if some_missing:
            if code == 0:                                     # this chunk was stored as it is
                value = int(bits[at:at + CHUNK_BITS], 2)
                at += CHUNK_BITS
                out += value.to_bytes(2, "big")
                continue
            code -= 1
        spot = code if style == PLAIN else new_spots[code]
        out += _read_pattern(page, spot).to_bytes(2, "big")   # read the bits at the plot point
    if data_length % 2:                                       # the odd last byte, as it is
        out.append(int(bits[at:at + 8], 2))
    return bytes(out)


# ---------------------------------------------------------------------------
# MEASURE: how many bits does a plot point need, compared with the 16-bit chunk?
# (Not used by plant/grow. Here so anyone can check the numbers on their own files.)
# ---------------------------------------------------------------------------

def measure(data: bytes):
    chunks, tail = _cut_into_chunks(data)
    rows = []
    for page_number, factors in enumerate(LIBRARY):
        page, first_spot, new_spots = grow_page(page_number)
        found = [first_spot[c] for c in chunks if first_spot[c] >= 0]
        compact_number = [-1] * ALL_PATTERNS
        for n, spot in enumerate(new_spots):
            compact_number[_read_pattern(page, spot)] = n
        found_compact = [compact_number[c] for c in chunks if compact_number[c] >= 0]
        rows.append({
            "page": factors["name"],
            "page length (steps)": len(page),
            "patterns on page": len(new_spots),
            "chunks": len(chunks),
            "chunks found on page": len(found),
            "average binary digits in a plain position":
                round(sum(max(1, p.bit_length()) for p in found) / max(1, len(found)), 2),
            "bits per plain position (fixed width W)":
                max(found).bit_length() if found else 0,
            "bits per compact number (fixed width W)":
                max(1, max(found_compact).bit_length()) if found_compact else 0,
            "bits per chunk": CHUNK_BITS,
        })
    return rows


if __name__ == "__main__":
    import sys
    page, first_spot, new_spots = grow_page(0)
    print("First 64 plot points of the strawberry page (placeholder):")
    print("".join(str(p) for p in page[:64]))
    print(f"The page ran {len(page):,} steps until all {len(new_spots):,} patterns appeared.\n")
    for path in sys.argv[1:]:
        with open(path, "rb") as f:
            data = f.read()
        print(path)
        for row in measure(data):
            print("  ", row)
        seed = plant(data)
        print(f"   seed {len(seed):,} bytes for {len(data):,} bytes; exact: {grow(seed) == data}\n")
