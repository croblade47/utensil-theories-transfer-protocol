"""Build every format of the project record from its Markdown master.

Usage (from the repository top level):
    python PROJECT_RECORD_2026-10-21/code/build_outputs.py PROJECT_RECORD_2026-10-21/Project_Record_2026-10-21.md

Makes, next to the Markdown file:
    .pdf   the full report, with bookmarks
    .docx  a real Word file (pandoc)
    .txt   a plain-text copy (pandoc)
    email_parts/Project_Record_part_K_of_N.pdf   the same report split at section boundaries into PDFs small
           enough to attach to an email one at a time (each <= MAX_PART_BYTES)
"""
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import md2pdf  # noqa: E402

MAX_PART_BYTES = 22_000
FOOTER = "Project Record - Utensil Theories Transfer Protocol - 17 to 21 October 2026"


def sections(text):
    """Split at '## ' headings; the part before the first one is the front matter."""
    idx = [m.start() for m in re.finditer(r"^## ", text, flags=re.M)]
    if not idx:
        return [text]
    return [text[:idx[0]]] + [text[a:b] for a, b in zip(idx, idx[1:] + [len(text)])]


def split_parts(secs, n):
    """Greedy split of the sections into n parts of similar length (order kept)."""
    total = sum(len(s) for s in secs)
    parts, cur, target = [], [], total / n
    for s in secs:
        if cur and sum(len(x) for x in cur) + len(s) / 2 > target and len(parts) < n - 1:
            parts.append(cur)
            cur = []
        cur.append(s)
    parts.append(cur)
    return parts


def title_of(sec):
    m = re.match(r"^## (.*)$", sec, flags=re.M)
    return m.group(1).strip() if m else "Title page and contents"


def main():
    md = Path(sys.argv[1]).resolve()
    stem = md.with_suffix("")
    text = md.read_text(encoding="utf-8")

    md2pdf.convert(str(md), str(stem) + ".pdf", FOOTER, bookmarks=True)
    subprocess.run(["pandoc", str(md), "-f", "gfm", "-t", "docx", "-o", str(stem) + ".docx"], check=True)
    subprocess.run(["pandoc", str(md), "-f", "gfm", "-t", "plain", "--columns=100", "--wrap=auto",
                    "-o", str(stem) + ".txt"], check=True)

    outdir = md.parent / "email_parts"
    outdir.mkdir(exist_ok=True)
    for old in outdir.glob("Project_Record_part_*"):
        old.unlink()
    secs = sections(text)
    for n in range(1, 12):
        parts = split_parts(secs, n)
        files = []
        for k, part in enumerate(parts, 1):
            head = (f"# Project Record - part {k} of {len(parts)}\n\n"
                    f"*Utensil Theories Transfer Protocol, 17 to 21 October 2026. This part holds: "
                    + "; ".join(title_of(s) for s in part) + ".*\n\n")
            pmd = outdir / f"Project_Record_part_{k}_of_{len(parts)}.md"
            pmd.write_text(head + "".join(part), encoding="utf-8")
            ppdf = pmd.with_suffix(".pdf")
            md2pdf.convert(str(pmd), str(ppdf), f"{FOOTER} - part {k} of {len(parts)}", bookmarks=False)
            pmd.unlink()
            files.append(ppdf)
        sizes = [f.stat().st_size for f in files]
        if max(sizes) <= MAX_PART_BYTES or n == 11:
            break
        for f in files:
            f.unlink()
    for f, s in zip(files, sizes):
        print(f"{f.name}: {s:,} bytes")
    for ext in (".pdf", ".docx", ".txt"):
        print(f"{stem.name}{ext}: {os.path.getsize(str(stem) + ext):,} bytes")


if __name__ == "__main__":
    main()
