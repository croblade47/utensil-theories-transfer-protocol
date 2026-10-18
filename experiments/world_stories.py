"""
World story library: public-domain wisdom stories, myths and fables from many
cultures, fetched from GITenberg (Project Gutenberg mirrored on GitHub).

    python experiments/world_stories.py      # downloads into experiments/data/world/

Each book is stripped of the Project Gutenberg header/footer.
All are public domain in the US. The two Dakota collections were written by
Dakota authors (Zitkala-Sa; Marie L. McLaughlin) and published for sharing.
"""

from __future__ import annotations

import re
import urllib.request
from pathlib import Path

WORLD = Path(__file__).parent / "data" / "world"
BASE = "https://raw.githubusercontent.com/GITenberg/"

# key: (culture, title, GITenberg path)
SOURCES = {
    "aesop":    ("Greek",          "Aesop's Fables",                        "Aesop-s-Fables_28/master/28.txt"),
    "grimm":    ("German",         "Grimms' Fairy Tales",                   "Grimms-Fairy-Tales_2591/master/2591.txt"),
    "celtic":   ("Celtic",         "Celtic Fairy Tales (Jacobs)",           "Celtic-Fairy-Tales_7885/master/7885.txt"),
    "india":    ("Indian",         "Indian Fairy Tales (Jacobs)",           "Indian-Fairy-Tales_7128/master/7128.txt"),
    "japan":    ("Japanese",       "Japanese Fairy Tales (Ozaki)",          "Japanese-Fairy-Tales_4018/master/4018.txt"),
    "china":    ("Chinese",        "Myths and Legends of China (Werner)",   "Myths-and-Legends-of-China_15250/master/15250.txt"),
    "tao":      ("Chinese",        "Tao Teh King (Legge)",                  "The-Tao-Teh-King-or-the-Tao-and-its-Characteristics_216/master/216.txt"),
    "arabian":  ("Arabic/Persian", "The Arabian Nights (Lang)",             "The-Arabian-Nights-Entertainments_128/master/128.txt"),
    "nigeria":  ("West African",   "Folk Stories from Southern Nigeria",    "Folk-Stories-from-Southern-Nigeria-West-Africa_34655/master/34655.txt"),
    "zitkala":  ("Dakota",         "Old Indian Legends (Zitkala-Sa)",       "Old-Indian-Legends_338/master/338.txt"),
    "sioux":    ("Dakota",         "Myths and Legends of the Sioux (McLaughlin)", "Myths-and-Legends-of-the-Sioux_341/master/341.txt"),
    "gilgamesh": ("Mesopotamian",  "Old Babylonian Gilgamesh Epic",         "An-Old-Babylonian-Version-of-the-Gilgamesh-Epic_11000/master/11000-8.txt"),
}

_START = re.compile(r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG.*?\*\*\*", re.I)
_END = re.compile(r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG", re.I)


def clean(raw: str) -> str:
    m = _START.search(raw)
    if m:
        raw = raw[m.end():]
    m = _END.search(raw)
    if m:
        raw = raw[:m.start()]
    return raw.strip()


def fetch(key: str) -> Path:
    WORLD.mkdir(parents=True, exist_ok=True)
    out = WORLD / f"{key}.txt"
    if not out.exists():
        with urllib.request.urlopen(BASE + SOURCES[key][2], timeout=60) as r:
            raw = r.read().decode("utf-8", errors="replace")
        out.write_text(clean(raw), encoding="utf-8")
    return out


def load(key: str) -> str:
    return fetch(key).read_text(encoding="utf-8")


def main():
    total = 0
    for key, (culture, title, _) in SOURCES.items():
        n = len(re.findall(r"[A-Za-z]+", load(key)))
        total += n
        print(f"  {culture:15s} {title:45s} {n:>9,} words")
    print(f"  {'':15s} {'TOTAL':45s} {total:>9,} words")


if __name__ == "__main__":
    main()
