"""
SEED TEST: a fair, AI-free check for any seed-and-grow method.

Put your rules into plant() and grow() below. Then run:  python seed_test.py
It works on any computer with Python 3, including an old MacBook.

What it checks, for each test file:
  1. Size:   bytes of the seed vs bytes of the original (both counted as raw bytes,
             so different syntax or encodings can't hide size).
  2. Exact:  the regrown file must match the original byte for byte (SHA-256 fingerprint).
  3. Fair:   grow() runs in a SEPARATE process that only receives the seed file,
             so it cannot peek at the original (the way a chat can see earlier messages).
  4. Hard cases: random bytes (no pattern at all) and a fresh file you choose.

Until you fill in your own rules, it uses ordinary zip compression (zlib) as an example,
so you can see what the numbers look like.
"""

import hashlib
import lzma
import os
import subprocess
import sys
import zlib

# ---------------------------------------------------------------------------
# YOUR METHOD GOES HERE
# ---------------------------------------------------------------------------

def plant(data: bytes) -> bytes:
    """Turn the original data into a seed. Replace with your rules."""
    return zlib.compress(data, 9)          # example only


def grow(seed: bytes) -> bytes:
    """Turn the seed back into the original data. Replace with your rules.
    It may use only the seed and these fixed rules, nothing else."""
    return zlib.decompress(seed)           # example only

# ---------------------------------------------------------------------------

def test_files(extra_paths):
    sample_text = (b"The quick brown fox jumps over the lazy dog. " * 3 +
                   b"Seeds only need water and sunlight to grow. " * 3)
    files = {
        "random bytes (no pattern at all)": os.urandom(100_000),
        "repeating pattern": b"ABC123" * 20_000,
        "short ordinary text": sample_text,
    }
    for p in extra_paths:                  # your own fresh files: photos, documents, anything
        with open(p, "rb") as f:
            files[os.path.basename(p)] = f.read()
    return files


def fingerprint(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--grow":     # the separate "receiving device"
        with open(sys.argv[2], "rb") as f:
            seed = f.read()
        sys.stdout.buffer.write(grow(seed))
        return

    print(f"{'test file':34s} {'original':>9s} {'seed':>9s} {'reduction':>9s} {'exact?':>7s} {'xz (normal zip-style)':>22s}")
    for name, data in test_files(sys.argv[1:]).items():
        seed = plant(data)
        with open("seed.bin", "wb") as f:
            f.write(seed)
        regrown = subprocess.run([sys.executable, __file__, "--grow", "seed.bin"],
                                 capture_output=True, check=True).stdout
        exact = fingerprint(regrown) == fingerprint(data)
        reduction = 100 * (1 - len(seed) / len(data))
        print(f"{name[:34]:34s} {len(data):9,d} {len(seed):9,d} {reduction:8.1f}% {('YES' if exact else 'NO'):>7s} "
              f"{len(lzma.compress(data)):22,d}")
    os.remove("seed.bin")
    with open(__file__, "rb") as f:
        print(f"\nGrow instructions (this script) are {len(f.read()):,} bytes; they are shared once, not sent with each seed.")


if __name__ == "__main__":
    main()
