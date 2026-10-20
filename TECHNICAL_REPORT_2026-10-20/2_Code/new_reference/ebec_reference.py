"""
EBEC reference implementation and honest benchmark
==================================================

Rebuilt from the written description in "EBEC_FULL_RECONSTRUCTION.md", because
the original V4 code was only in screenshots and was not among the sources:

  * Polynomial rolling hash:  H = sum(ord(c) * 31**pos) mod 46656
  * Base-36 encoding, 3 characters per token  (36**3 = 46,656 possible codes)
  * Prime shift (+17) to resolve collisions
  * Levenshtein "failsafe" that maps a typo to the closest known word
  * A local JSON dictionary that grows as new words arrive
  * decompress_sentence() as written in the reconstruction document
  * The "Excess Bank" idea from EBEC V1/V2: keep what modulo throws away

It also measures the claims instead of repeating them:
  1. Is it lossless (does every text come back exactly)?
  2. How small is the result, counting the dictionary, compared with ordinary
     compressors (gzip, bz2, xz) on the same text?
  3. Do 12 deliberately similar words all get distinct codes?
  4. What does the typo failsafe do to losslessness?

Run:  python ebec_reference.py [path/to/text.txt ...]
"""

from __future__ import annotations

import bz2
import gzip
import json
import lzma
import re
import sys
from pathlib import Path

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SPACE = 36 ** 3          # 46,656 three-character codes
PRIME_SHIFT = 17


def base36(n: int, width: int = 3) -> str:
    out = []
    for _ in range(width):
        n, r = divmod(n, 36)
        out.append(ALPHABET[r])
    return "".join(reversed(out))


def rolling_hash(word: str) -> int:
    """H = sum(ASCII * 31**pos) mod 46656."""
    return sum(ord(c) * pow(31, i, SPACE) for i, c in enumerate(word)) % SPACE


def excess_bank(word: str) -> tuple[int, int]:
    """EBEC V1/V2 'subtraction rule': subtract 46,656 until the value fits and count
    how many times (the 'excess bank'). This equals divmod(H_full, 46656): the bank is
    the quotient that plain modulo throws away. Keeping it keeps all the information,
    but the code is then no longer 3 characters."""
    full = sum(ord(c) * 31 ** i for i, c in enumerate(word))
    bank = 0
    while full >= SPACE:            # written as repeated subtraction, as described
        full -= SPACE
        bank += 1
        if bank > 10 ** 6:          # very long words: finish with divmod (same result)
            extra, full = divmod(full, SPACE)
            bank += extra
            break
    return bank, full


def levenshtein(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


class EBEC:
    """Word-level dictionary coder with rolling-hash codes."""

    def __init__(self, seed: dict[str, str] | None = None, typo_failsafe: bool = False,
                 max_typo_distance: int = 1):
        self.local_dict: dict[str, str] = dict(seed or {})
        self.used: set[str] = set(self.local_dict.values())
        self.typo_failsafe = typo_failsafe
        self.max_typo_distance = max_typo_distance
        self.collisions = 0

    def verify_outside(self, word: str) -> bool:
        """'In a full system, this is where it Goes Outside to verify.'
        Stub kept honest: this reference accepts every word. A real check would
        confirm the new entry with a spell-checker or a larger model."""
        return True

    def code_for(self, word: str) -> str:
        if word in self.local_dict:
            return self.local_dict[word]
        if self.typo_failsafe and word.isalpha() and len(word) > 3:
            for known in self.local_dict:
                if known.isalpha() and abs(len(known) - len(word)) <= self.max_typo_distance \
                        and levenshtein(known, word) <= self.max_typo_distance:
                    return self.local_dict[known]        # NOTE: this changes the text
        if len(self.used) >= SPACE:
            raise OverflowError("All 46,656 three-character codes are used: the vocabulary is too large.")
        if not self.verify_outside(word):
            raise ValueError(f"Outside verification rejected {word!r}")
        h = rolling_hash(word)
        code = base36(h)
        while code in self.used:                         # collision: prime shift +17
            self.collisions += 1
            h = (h + PRIME_SHIFT) % SPACE
            code = base36(h)
        self.local_dict[word] = code
        self.used.add(code)
        return code

    def compress_sentence(self, text: str) -> str:
        # Words, single punctuation marks and whitespace runs are all tokens, so
        # nothing (case, punctuation, line breaks) is dropped.
        return "".join(self.code_for(t) for t in re.findall(r"\w+|\s+|[^\w\s]", text))

    def decompress_sentence(self, token_string: str) -> str:
        reverse_dict = {v: k for k, v in self.local_dict.items()}
        tokens = [token_string[i:i + 3] for i in range(0, len(token_string), 3)]
        return "".join(reverse_dict.get(t, f"[{t}?]") for t in tokens)

    def dictionary_bytes(self) -> int:
        return len(json.dumps(self.local_dict, ensure_ascii=False).encode("utf-8"))


def stress_test() -> dict:
    """12 deliberately similar words; every one must get its own code and come back exactly."""
    words = ["tion", "tino", "toin", "noit", "itno", "otin",
             "pro", "por", "rop", "con", "cno", "inter"]
    e = EBEC()
    codes = {w: e.code_for(w) for w in words}
    text = " ".join(words)
    ok = e.decompress_sentence(e.compress_sentence(text)) == text
    return {"words": words, "distinct_codes": len(set(codes.values())) == len(words),
            "round_trip_ok": ok, "collisions_resolved": e.collisions, "codes": codes}


def benchmark(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    raw = text.encode("utf-8")
    e = EBEC()
    try:
        packed = e.compress_sentence(text)
    except OverflowError as err:
        return {"file": path.name, "error": str(err)}
    restored = e.decompress_sentence(packed)
    payload = len(packed.encode("ascii"))
    dict_b = e.dictionary_bytes()
    ebec_total = payload + dict_b
    ebec_xz = len(lzma.compress(packed.encode("ascii"))) + len(lzma.compress(
        json.dumps(e.local_dict).encode("utf-8")))

    # Typo failsafe: how much text does it silently change?
    ef = EBEC(typo_failsafe=True)
    sample = text[:200_000]
    restored_f = ef.decompress_sentence(ef.compress_sentence(sample))
    changed_words = sum(a != b for a, b in zip(re.findall(r"\w+", sample), re.findall(r"\w+", restored_f)))

    return {
        "file": path.name,
        "original_bytes": len(raw),
        "distinct_tokens": len(e.local_dict),
        "collisions_resolved": e.collisions,
        "lossless_round_trip": restored == text,
        "ebec_payload_bytes": payload,
        "ebec_dictionary_bytes": dict_b,
        "ebec_total_bytes": ebec_total,
        "ebec_total_vs_original": round(ebec_total / len(raw), 3),
        "ebec_then_xz_bytes": ebec_xz,
        "gzip_bytes": len(gzip.compress(raw, 9)),
        "bz2_bytes": len(bz2.compress(raw, 9)),
        "xz_bytes": len(lzma.compress(raw, preset=9)),
        "typo_failsafe_words_changed_in_first_200k_chars": changed_words,
    }


def main(argv):
    out = {"stress_test": stress_test(), "benchmarks": []}
    paths = [Path(p) for p in argv] or []
    for p in paths:
        out["benchmarks"].append(benchmark(p))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
