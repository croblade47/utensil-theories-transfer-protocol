"""
SEED TEST: a fair, AI-free check for any seed-and-grow method.

Run every method on the built-in test files:
    python seed_test.py
Run one method, and add your own files:
    python seed_test.py --method graph_fit photo.jpg letter.txt

It works on any computer with Python 3 (standard library only), including an old MacBook.

Each method is a small file in the methods/ folder with two functions:
    plant(data: bytes) -> bytes      original data  -> seed
    grow(seed: bytes)  -> bytes      seed           -> original data
"zip_example" (ordinary zip compression) is built in, for comparison.

What it checks, for each test file:
  1. Size:   bytes of the seed vs bytes of the original (both counted as raw bytes,
             so different syntax or encodings can't hide size).
  2. Exact:  the regrown file must match the original byte for byte (SHA-256 fingerprint).
  3. Fair:   grow() runs in a SEPARATE process, started in an EMPTY folder that holds only
             the seed file, so it cannot peek at the original (the way a chat can see
             earlier messages).
  4. Hard cases: random bytes (no pattern at all) and fresh files you choose.
"""

import hashlib
import importlib.util
import lzma
import os
import shutil
import subprocess
import sys
import tempfile
import time
import types
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
METHODS_DIR = os.path.join(HERE, "methods")


# ---------------------------------------------------------------------------
# Built-in example method: ordinary zip compression
# ---------------------------------------------------------------------------

_zip = types.SimpleNamespace(
    NAME="zip_example",
    SUMMARY="Ordinary zip compression (zlib), for comparison.",
    plant=lambda data: zlib.compress(data, 9),
    grow=lambda seed: zlib.decompress(seed),
    __file__=None,
)


def available_methods():
    names = ["zip_example"]
    if os.path.isdir(METHODS_DIR):
        names += sorted(f[:-3] for f in os.listdir(METHODS_DIR)
                        if f.endswith(".py") and not f.startswith("_"))
    return names


def load_method(name):
    if name == "zip_example":
        return _zip
    path = os.path.join(METHODS_DIR, name + ".py")
    spec = importlib.util.spec_from_file_location("method_" + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    return hashlib.sha256(b).hexdigest()


def grow_elsewhere(method_name, seed):
    """Grow the seed in a separate Python process, in an empty temporary folder."""
    box = tempfile.mkdtemp(prefix="grow_box_")
    try:
        with open(os.path.join(box, "seed.bin"), "wb") as f:
            f.write(seed)
        t = time.perf_counter()
        out = subprocess.run([sys.executable, "-I", os.path.abspath(__file__),
                              "--grow", method_name, "seed.bin"],
                             cwd=box, capture_output=True)
        seconds = time.perf_counter() - t
        if out.returncode != 0:
            return None, seconds, out.stderr.decode(errors="replace").strip().splitlines()[-1:]
        return out.stdout, seconds, None
    finally:
        shutil.rmtree(box, ignore_errors=True)


def run_method(name, files):
    method = load_method(name)
    print(f"\n=== Method: {name} ===")
    print(getattr(method, "SUMMARY", ""))
    print(f"{'test file':34s} {'original':>9s} {'seed':>9s} {'reduction':>9s} {'exact?':>7s} "
          f"{'plant s':>8s} {'grow s':>7s} {'xz size':>9s}")
    rows = []
    for fname, data in files.items():
        t = time.perf_counter()
        seed = method.plant(data)
        plant_s = time.perf_counter() - t
        regrown, grow_s, err = grow_elsewhere(name, seed)
        exact = regrown is not None and fingerprint(regrown) == fingerprint(data)
        reduction = 100 * (1 - len(seed) / len(data)) if data else 0.0
        print(f"{fname[:34]:34s} {len(data):9,d} {len(seed):9,d} {reduction:8.1f}% "
              f"{('YES' if exact else 'NO'):>7s} {plant_s:8.2f} {grow_s:7.2f} "
              f"{len(lzma.compress(data)):9,d}")
        if err:
            print(f"    grow failed: {err}")
        rows.append((fname, len(data), len(seed), reduction, exact))
    rule_files = [os.path.abspath(__file__)] + ([method.__file__] if method.__file__ else [])
    rule_bytes = sum(os.path.getsize(p) for p in rule_files)
    print(f"Grow instructions (the test script + this method's file) are {rule_bytes:,} bytes; "
          f"they are shared once, not sent with each seed.")
    return rows


def main():
    args = sys.argv[1:]
    if len(args) == 3 and args[0] == "--grow":            # the separate "receiving device"
        method = load_method(args[1])
        with open(args[2], "rb") as f:
            seed = f.read()
        sys.stdout.buffer.write(method.grow(seed))
        return

    names = available_methods()
    if len(args) >= 2 and args[0] == "--method":
        names = [args[1]]
        args = args[2:]
    files = test_files(args)             # the same files are used for every method in this run
    print("Methods:", ", ".join(names))
    print("Test files:", ", ".join(f"{k} ({len(v):,} bytes)" for k, v in files.items()))
    summary = {}
    for name in names:
        summary[name] = run_method(name, files)

    print("\n=== Summary: total seed bytes vs total original bytes, and exact regrowth ===")
    total = sum(len(v) for v in files.values())
    for name, rows in summary.items():
        seeds = sum(r[2] for r in rows)
        ok = sum(r[4] for r in rows)
        print(f"{name:22s} seeds {seeds:>11,d} of {total:,} bytes  "
              f"({100 * (1 - seeds / total):5.1f}% smaller)   exact: {ok}/{len(rows)} files")


if __name__ == "__main__":
    main()
