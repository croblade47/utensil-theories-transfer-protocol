"""Turn a plain Markdown report into a compact PDF with ReportLab's built-in fonts (nothing embedded, so the file
stays small enough to attach to an email).

Usage: python md2pdf.py report.md report.pdf ["Footer title"] [--no-bookmarks]
Bookmarks are made for # and ## headings only (each one adds a little to the file size).
Handles: # to #### headings, paragraphs, - / * / 1. lists (nested by indentation), > quotes, ``` code blocks,
pipe tables, --- rules, **bold**, *italic*, `code`.
"""
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)
from reportlab.platypus.flowables import HRFlowable

ASCII = {"→": "->", "←": "<-", "↔": "<->", "⇒": "=>", "≥": ">=", "≤": "<=",
         "−": "-", "≈": "~", "≠": "!=", "∞": "infinity", "✓": "yes", "✗": "no",
         "✔": "yes", "✘": "no", " ": " ", " ": " ", " ": " ", "​": "",
         "‑": "-", "‐": "-", "′": "'", "″": '"', "│": "|", "─": "-",
         "√": "sqrt", "π": "pi", "∆": "delta", "Δ": "Delta", "∑": "sum",
         "∈": "in", "≡": "==", "≅": "~=", "⋅": "*", "∙": "*", "●": "*"}


def clean(s):
    s = "".join(ASCII.get(ch, ch) for ch in s)
    out = []
    for ch in s:
        try:
            ch.encode("cp1252")
            out.append(ch)
        except UnicodeEncodeError:
            out.append("?")
    return "".join(out)


def inline(s):
    s = clean(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"(?<![\w_])_([^_\s][^_]*?)_(?![\w_])", r"<i>\1</i>", s)
    return s


BASE = ParagraphStyle("base", fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=5, alignment=TA_LEFT)
ST = {
    "h1": ParagraphStyle("h1", parent=BASE, fontName="Helvetica-Bold", fontSize=17, leading=21, spaceBefore=6,
                         spaceAfter=8),
    "h2": ParagraphStyle("h2", parent=BASE, fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceBefore=12,
                         spaceAfter=6, textColor=colors.HexColor("#1f3b5c")),
    "h3": ParagraphStyle("h3", parent=BASE, fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8,
                         spaceAfter=4),
    "h4": ParagraphStyle("h4", parent=BASE, fontName="Helvetica-BoldOblique", fontSize=10, leading=13, spaceBefore=6,
                         spaceAfter=3),
    "p": BASE,
    "li": ParagraphStyle("li", parent=BASE, spaceAfter=2),
    "quote": ParagraphStyle("quote", parent=BASE, leftIndent=14, textColor=colors.HexColor("#333333"),
                            fontName="Helvetica-Oblique"),
    "cell": ParagraphStyle("cell", parent=BASE, fontSize=8.3, leading=10.2, spaceAfter=0),
    "cellh": ParagraphStyle("cellh", parent=BASE, fontSize=8.3, leading=10.2, spaceAfter=0,
                            fontName="Helvetica-Bold"),
    "code": ParagraphStyle("code", parent=BASE, fontName="Courier", fontSize=7.8, leading=9.6, leftIndent=8),
}
WIDTH = letter[0] - 1.5 * inch


def table_flow(rows):
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    lens = [max(min(len(r[c]), 60) for r in rows) + 4 for c in range(ncol)]
    widths = [WIDTH * L / sum(lens) for L in lens]
    data = [[Paragraph(inline(cell), ST["cellh"] if i == 0 else ST["cell"]) for cell in r]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e4eaf1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")


def list_flow(items):
    """items: list of (indent, ordered, text). Builds nested ListFlowables."""
    def build(i, level_indent):
        flows, ordered = [], None
        while i < len(items):
            ind, ordd, text = items[i]
            if ind < level_indent:
                break
            if ind > level_indent and flows:
                sub, i = build(i, ind)
                flows[-1][1].append(sub)
                continue
            ordered = ordd if ordered is None else ordered
            flows.append((text, []))
            i += 1
        lis = []
        for text, subs in flows:
            lis.append(ListItem([Paragraph(inline(text), ST["li"])] + subs, leftIndent=12 if not ordered else 16))
        kw = dict(bulletType="1", bulletFontSize=9) if ordered else dict(bulletType="bullet", start="-",
                                                                          bulletFontSize=9)
        return ListFlowable(lis, leftIndent=12 if not ordered else 16, **kw), i
    flow, _ = build(0, items[0][0])
    return flow


def convert(src, dst, footer, bookmarks=True):
    lines = open(src, encoding="utf-8").read().splitlines()
    story, i, para = [], 0, []

    def flush():
        if para:
            story.append(Paragraph(inline(" ".join(x.strip() for x in para)), ST["p"]))
            para.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith("```"):
            flush()
            j, block = i + 1, []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                block.append(clean(lines[j]))
                j += 1
            story.append(Preformatted("\n".join(block), ST["code"]))
            i = j + 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            flush()
            lvl = len(m.group(1))
            p = Paragraph(inline(m.group(2)), ST[f"h{lvl}"])
            p._bookmark = (lvl, clean(re.sub(r"[*`]", "", m.group(2))))
            story.append(p)
            i += 1
            continue
        if s.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            if rows:
                story.append(table_flow(rows))
                story.append(Spacer(1, 6))
            continue
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s):
            flush()
            story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#999999"),
                                    spaceBefore=4, spaceAfter=6))
            i += 1
            continue
        if s.startswith(">"):
            flush()
            q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(lines[i].strip().lstrip(">").strip())
                i += 1
            story.append(Paragraph(inline(" ".join(q)), ST["quote"]))
            continue
        if LIST_RE.match(ln):
            flush()
            items = []
            while i < len(lines):
                mm = LIST_RE.match(lines[i])
                if mm:
                    items.append([len(mm.group(1).expandtabs(4)), mm.group(2)[0].isdigit(), mm.group(3)])
                    i += 1
                elif lines[i].strip() and items and lines[i].startswith(" ") and not lines[i].strip().startswith("|"):
                    items[-1][2] += " " + lines[i].strip()
                    i += 1
                else:
                    break
            story.append(list_flow(items))
            story.append(Spacer(1, 3))
            continue
        if not s:
            flush()
            i += 1
            continue
        para.append(ln)
        i += 1
    flush()

    class Doc(SimpleDocTemplate):
        def afterFlowable(self, f):
            bm = getattr(f, "_bookmark", None)
            if bm and bookmarks and bm[0] <= 2:
                lvl, title = bm
                key = f"h{id(f)}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(title[:90], key, level=min(lvl - 1, 2), closed=lvl > 1)

    def deco(canv, doc):
        canv.saveState()
        canv.setFont("Helvetica", 7.5)
        canv.setFillColor(colors.HexColor("#666666"))
        canv.drawString(0.75 * inch, 0.5 * inch, clean(footer))
        canv.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, f"page {doc.page}")
        canv.restoreState()

    doc = Doc(dst, pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.7 * inch,
              bottomMargin=0.75 * inch, title=footer, author="Prepared by Claude (AI) for the project owner",
              pageCompression=1)
    doc.build(story, onFirstPage=deco, onLaterPages=deco)
    try:                                   # recompress at the highest zlib level to keep email attachments small
        from pypdf import PdfReader, PdfWriter
        w = PdfWriter(clone_from=PdfReader(dst))
        for page in w.pages:
            page.compress_content_streams(level=9)
        w.compress_identical_objects()
        w.write(dst)
    except ImportError:
        pass


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--no-bookmarks"]
    convert(args[0], args[1], args[2] if len(args) > 2 else "Report", bookmarks="--no-bookmarks" not in sys.argv)
    print("wrote", sys.argv[2])
