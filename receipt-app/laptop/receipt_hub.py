#!/usr/bin/env python3
"""Door Receipts laptop hub.

Run:  python3 receipt_hub.py            (start the hub, open the dashboard)
      python3 receipt_hub.py rebuild    (rebuild all reports from saved data)
      python3 receipt_hub.py surveys    (send survey emails that are due)
      python3 receipt_hub.py analyze    (send the AI report to Claude, needs `pip install anthropic`)

What it does:
  * Serves the phone app at http://localhost:8765 and receives syncs from it.
  * Watches for an Android phone on USB and links it automatically (adb reverse),
    so the phone can reach the laptop as "localhost" as soon as it is plugged in.
  * Builds printable shift reports, single receipts, an Excel tax/hours spreadsheet,
    an AI pattern report, and survey emails.
Only the Python standard library is required.
"""
import base64
import csv
import html
import io
import json
import os
import re
import shutil
import smtplib
import subprocess
import sys
import threading
import time
import webbrowser
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from email.message import EmailMessage
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import xlsx

HERE = Path(__file__).resolve().parent
PHONE_DIR = HERE.parent / "phone"
DATA = Path(os.environ.get("DOOR_RECEIPTS_DATA", HERE / "data"))
VISITS, SHIFTS, POINTS = DATA / "visits", DATA / "shifts", DATA / "points"
PHOTOS, SIGS, INBOX = DATA / "photos", DATA / "signatures", DATA / "inbox"
REPORTS = DATA / "reports"
CONFIG_PATH = DATA / "config.json"
SURVEYS_PATH = DATA / "surveys_sent.json"
PORT = int(os.environ.get("DOOR_RECEIPTS_PORT", "8765"))

DEFAULT_CONFIG = {
    "business_name": "",
    "your_name": "",
    "survey_url": "https://forms.gle/your-survey-link",
    "survey_days_after": 2,
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "",
    "smtp_password": "",
    "from_email": "",
    "_help": "For Gmail, smtp_password must be an App Password (Google Account > Security > App passwords). "
             "Leave smtp_user blank to only create draft .eml files instead of sending.",
}

OUTCOME = {"sale": "SALE", "no": "NO", "not_home": "NOT HOME", "callback": "COME BACK"}
lock = threading.Lock()


# ---------------------------------------------------------------- storage
def setup_dirs():
    for d in (VISITS, SHIFTS, POINTS, PHOTOS, SIGS, INBOX, REPORTS / "shifts", REPORTS / "receipts",
              REPORTS / "outbox", REPORTS / "ai"):
        d.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(DEFAULT_CONFIG, indent=2))


def load_config():
    try:
        return {**DEFAULT_CONFIG, **json.loads(CONFIG_PATH.read_text())}
    except Exception:
        return dict(DEFAULT_CONFIG)


def safe_id(s):
    return re.sub(r"[^A-Za-z0-9_-]", "", str(s))[:64] or "x"


def save_data_url(data_url, path):
    if not data_url or "," not in data_url:
        return None
    path.write_bytes(base64.b64decode(data_url.split(",", 1)[1]))
    return path.name


def ingest(payload):
    """Save a sync payload from the phone. Safe to call repeatedly with the same data."""
    n_v = n_s = 0
    with lock:
        for v in payload.get("visits", []):
            vid = safe_id(v.get("id"))
            v = dict(v, id=vid)
            v["photo_file"] = save_data_url(v.pop("photo", None), PHOTOS / f"{vid}.jpg")
            v["signature_file"] = save_data_url(v.pop("signature", None), SIGS / f"{vid}.png")
            old = VISITS / f"{vid}.json"
            if old.exists():  # keep files from an earlier sync if this copy has none
                prev = json.loads(old.read_text())
                v["photo_file"] = v["photo_file"] or prev.get("photo_file")
                v["signature_file"] = v["signature_file"] or prev.get("signature_file")
            v.pop("synced", None)
            old.write_text(json.dumps(v, indent=1))
            n_v += 1
        for s in payload.get("shifts", []):
            sid = safe_id(s.get("id"))
            s = dict(s, id=sid)
            s.pop("synced", None)
            (SHIFTS / f"{sid}.json").write_text(json.dumps(s, indent=1))
            n_s += 1
        by_shift = defaultdict(list)
        for p in payload.get("points", []):
            by_shift[safe_id(p.get("shiftId"))].append(p)
        for sid, pts in by_shift.items():
            f = POINTS / f"{sid}.json"
            existing = json.loads(f.read_text()) if f.exists() else []
            seen = {p["t"] for p in existing}
            existing += [{"t": p["t"], "lat": p["lat"], "lng": p["lng"], "acc": p.get("acc")} for p in pts if p["t"] not in seen]
            existing.sort(key=lambda p: p["t"])
            f.write_text(json.dumps(existing))
    return n_v, n_s


def import_inbox():
    """Import any sync files dropped into data/inbox (iPhone / no-cable route)."""
    count = 0
    for f in sorted(INBOX.glob("*.json")):
        try:
            ingest(json.loads(f.read_text()))
            f.rename(f.with_suffix(".imported"))
            count += 1
        except Exception as e:
            print(f"  ! could not import {f.name}: {e}")
    return count


def load_all():
    visits = [json.loads(f.read_text()) for f in VISITS.glob("*.json")]
    shifts = {s["id"]: s for s in (json.loads(f.read_text()) for f in SHIFTS.glob("*.json"))}
    visits.sort(key=lambda v: v.get("createdAt", 0))
    for sid in {v.get("shiftId") for v in visits} - shifts.keys():
        ts = [v["createdAt"] for v in visits if v.get("shiftId") == sid]
        shifts[sid] = {"id": sid, "start": min(ts), "end": max(ts), "untracked": True}
    return visits, shifts


def load_points(sid):
    f = POINTS / f"{safe_id(sid)}.json"
    return json.loads(f.read_text()) if f.exists() else []


# ---------------------------------------------------------------- math helpers
def dt(ms):
    return datetime.fromtimestamp((ms or 0) / 1000)


def miles_for(points):
    from math import asin, cos, radians, sin, sqrt
    total = 0.0
    for a, b in zip(points, points[1:]):
        dlat, dlng = radians(b["lat"] - a["lat"]), radians(b["lng"] - a["lng"])
        h = sin(dlat / 2) ** 2 + cos(radians(a["lat"])) * cos(radians(b["lat"])) * sin(dlng / 2) ** 2
        d = 2 * 6371000 * asin(sqrt(h))
        if 15 < d < 5000:
            total += d
    return total / 1609.344


def shift_stats(shift, visits):
    vs = [v for v in visits if v.get("shiftId") == shift["id"]]
    sales = [v for v in vs if v.get("type") == "sale"]
    gross = round(sum(float(v.get("amount") or 0) for v in sales), 2)
    hours = 0.0 if shift.get("untracked") else max(0.0, ((shift.get("end") or shift["start"]) - shift["start"]) / 3600000)
    pts = load_points(shift["id"])
    return {
        "visits": vs, "sales": sales, "gross": gross, "hours": round(hours, 2),
        "miles": round(miles_for(pts), 1), "points": pts, "doors": len(vs),
        "no": sum(v.get("type") == "no" for v in vs),
        "not_home": sum(v.get("type") == "not_home" for v in vs),
        "callback": sum(v.get("type") == "callback" for v in vs),
    }


def street_of(address):
    a = (address or "").strip()
    a = re.sub(r"^\s*\d+[A-Za-z]?\s+", "", a)   # drop house number
    a = a.split(",")[0].strip()
    return a.title() or "(no address)"


def e(s):
    return html.escape(str(s if s is not None else ""))


def money(n):
    return f"${float(n or 0):,.2f}"


def maps_link(v):
    if v.get("lat") is None:
        return ""
    return f'<a href="https://maps.google.com/?q={v["lat"]},{v["lng"]}">map</a>'


# ---------------------------------------------------------------- printable reports
PRINT_CSS = """
body{font:14px/1.4 system-ui,Segoe UI,Roboto,sans-serif;color:#111;margin:24px;max-width:900px}
h1{margin:0 0 4px} .muted{color:#555} table{border-collapse:collapse;width:100%;margin:10px 0}
td,th{border-bottom:1px solid #ddd;padding:5px 6px;text-align:left;vertical-align:top} th{background:#f2f4f3}
.num{text-align:right} .receipt{border:1px solid #999;border-radius:8px;padding:14px;margin:14px 0;page-break-inside:avoid;display:grid;grid-template-columns:220px 1fr;gap:14px}
.receipt img.house{width:220px;height:165px;object-fit:cover;border-radius:6px} .sig{height:70px;max-width:260px;border-bottom:1px solid #666;object-fit:contain}
.amt{font-size:22px;font-weight:800} .totals td{font-weight:700} .pb{page-break-after:always}
.btn{display:inline-block;padding:8px 14px;background:#0f766e;color:#fff;border-radius:8px;text-decoration:none;border:0;font:inherit;cursor:pointer}
@media print{.noprint{display:none} body{margin:0}}
"""


def receipt_block(v, img_prefix):
    photo = f'<img class="house" src="{img_prefix}photos/{e(v["photo_file"])}">' if v.get("photo_file") else "<div></div>"
    sig = f'<img class="sig" src="{img_prefix}signatures/{e(v["signature_file"])}">' if v.get("signature_file") else "<i>not signed</i>"
    t = dt(v["createdAt"])
    return f"""<div class="receipt">{photo}<div>
      <b>Receipt #{e(v.get('receiptNo'))}</b> · {t:%a %b %d %Y, %I:%M %p}<br>
      <b>{e(v.get('address'))}</b> {maps_link(v)}<br>{e(v.get('description'))}<br>
      <span class="amt">{money(v.get('amount'))}</span> · {e(v.get('payment'))}<br>
      Customer: <b>{e(v.get('customerName'))}</b> {('· ' + e(v['email'])) if v.get('email') else ''}<br>{sig}
    </div></div>"""


def build_shift_report(shift, st, cfg):
    start = dt(shift["start"])
    end = dt(shift.get("end") or shift["start"])
    rate = st["gross"] / st["hours"] if st["hours"] else 0
    answered = st["doors"] - st["not_home"]
    close = (len(st["sales"]) / answered * 100) if answered else 0
    stops = "".join(
        f"<tr><td>{dt(v['createdAt']):%I:%M %p}</td><td>{OUTCOME.get(v.get('type'), v.get('type'))}</td>"
        f"<td>{e(v.get('address'))} {maps_link(v)}</td><td>{e(v.get('reason') or v.get('description') or '')}</td>"
        f"<td class='num'>{money(v.get('amount')) if v.get('type') == 'sale' else ''}</td></tr>"
        for v in st["visits"])
    track = ""
    if st["points"]:
        first, last = st["points"][0], st["points"][-1]
        track = (f"<p class='muted'>GPS: {len(st['points'])} location points from {dt(first['t']):%I:%M %p} "
                 f"to {dt(last['t']):%I:%M %p}. Start <a href='https://maps.google.com/?q={first['lat']},{first['lng']}'>map</a>, "
                 f"end <a href='https://maps.google.com/?q={last['lat']},{last['lng']}'>map</a>.</p>")
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Shift {start:%Y-%m-%d}</title><style>{PRINT_CSS}</style></head><body>
<p class="noprint"><button class="btn" onclick="print()">Print / Save as PDF</button> <a href="/dashboard">← Dashboard</a></p>
<div class="pb">
<h1>{e(cfg.get('business_name') or 'Shift Report')}</h1>
<div class="muted">{e(shift.get('worker') or cfg.get('your_name'))} · {start:%A, %B %d, %Y}</div>
<table>
<tr><th>Started</th><td>{start:%I:%M %p}</td><th>Ended</th><td>{'(no timer)' if shift.get('untracked') else f'{end:%I:%M %p}'}</td></tr>
<tr><th>Hours worked</th><td>{st['hours']:.2f}</td><th>Miles tracked</th><td>{st['miles']:.1f}</td></tr>
<tr><th>Doors</th><td>{st['doors']}</td><th>Sales / No / Not home / Later</th><td>{len(st['sales'])} / {st['no']} / {st['not_home']} / {st['callback']}</td></tr>
<tr><th>Close rate</th><td>{close:.0f}% of people who answered</td><th>Per hour</th><td>{money(rate)}</td></tr>
<tr class="totals"><th>Total collected</th><td colspan="3">{money(st['gross'])}</td></tr>
</table>{track}
<h2>All stops</h2><table><tr><th>Time</th><th>Result</th><th>Address</th><th>Notes</th><th class="num">Amount</th></tr>{stops}
<tr class="totals"><td colspan="4">Total</td><td class="num">{money(st['gross'])}</td></tr></table>
</div>
<h2>Receipts ({len(st['sales'])})</h2>
{''.join(receipt_block(v, '../../') for v in st['sales']) or '<p>No sales this shift.</p>'}
</body></html>"""
    name = f"{start:%Y-%m-%d}_{shift['id']}.html"
    (REPORTS / "shifts" / name).write_text(doc)
    return name


def data_uri(path, mime):
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}" if path and path.exists() else ""


def build_single_receipt(v, cfg):
    """Self-contained receipt (images embedded) — used for email attachments."""
    photo = data_uri(PHOTOS / v["photo_file"], "image/jpeg") if v.get("photo_file") else ""
    sig = data_uri(SIGS / v["signature_file"], "image/png") if v.get("signature_file") else ""
    t = dt(v["createdAt"])
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Receipt #{e(v.get('receiptNo'))}</title>
<style>body{{font:15px/1.45 system-ui,Segoe UI,Roboto,sans-serif;max-width:520px;margin:20px auto;color:#111}}
img{{max-width:100%;border-radius:8px}} td{{padding:3px 8px 3px 0;vertical-align:top}} .amt{{font-size:28px;font-weight:800}}</style></head><body>
<h2>{e(v.get('business') or cfg.get('business_name') or 'Receipt')}</h2>
<div>{e(v.get('bizPhone') or '')}</div>
<p>Receipt #{e(v.get('receiptNo'))} · {t:%B %d, %Y %I:%M %p}</p>
{f'<img src="{photo}" alt="House">' if photo else ''}
<table><tr><td>Address</td><td>{e(v.get('address'))}</td></tr><tr><td>Service</td><td>{e(v.get('description'))}</td></tr>
<tr><td>Paid by</td><td>{e(v.get('payment'))}</td></tr><tr><td>Provided by</td><td>{e(v.get('worker') or cfg.get('your_name'))}</td></tr>
<tr><td>Customer</td><td>{e(v.get('customerName'))}</td></tr></table>
<p class="amt">{money(v.get('amount'))}</p>
{f'<img src="{sig}" alt="Signature" style="max-height:110px;border-bottom:1px solid #999">' if sig else ''}
<div>Customer signature</div></body></html>"""
    path = REPORTS / "receipts" / f"receipt-{v.get('receiptNo') or v['id']}.html"
    path.write_text(doc)
    return path


# ---------------------------------------------------------------- spreadsheet
def build_spreadsheet(visits, shifts, stats):
    S = xlsx
    sales = [v for v in visits if v.get("type") == "sale"]
    receipts = [[(h, S.BOLD) for h in ["Receipt #", "Date", "Time", "Address", "Description", "Customer",
                                       "Amount", "Paid by", "Email", "Shift ID"]]]
    for v in sales:
        t = dt(v["createdAt"])
        receipts.append([v.get("receiptNo") or "", f"{t:%Y-%m-%d}", f"{t:%I:%M %p}", v.get("address", ""),
                         v.get("description", ""), v.get("customerName", ""), (float(v.get("amount") or 0), S.MONEY),
                         v.get("payment", ""), v.get("email", ""), v.get("shiftId", "")])
    n = len(receipts)
    receipts.append([])
    receipts.append([("", S.BOLD), "", "", "", "", ("TOTAL", S.BOLD), (f"=SUM(G2:G{n})", S.BOLD_MONEY)])

    shift_rows = [[(h, S.BOLD) for h in ["Date", "Start", "End", "Worker", "Hours", "Miles", "Doors", "Sales",
                                         "Gross", "$ / hour", "Shift ID"]]]
    ordered = sorted(shifts.values(), key=lambda s: s["start"])
    for i, s in enumerate(ordered, start=2):
        st = stats[s["id"]]
        shift_rows.append([f"{dt(s['start']):%Y-%m-%d}", "" if s.get("untracked") else f"{dt(s['start']):%I:%M %p}",
                           "" if s.get("untracked") else f"{dt(s.get('end') or s['start']):%I:%M %p}",
                           s.get("worker", ""), (st["hours"], S.DEC), (st["miles"], S.DEC), st["doors"], len(st["sales"]),
                           (f"=SUMIFS(Receipts!G:G,Receipts!J:J,K{i})", S.MONEY),
                           (f"=IF(E{i}>0,I{i}/E{i},0)", S.MONEY), s["id"]])
    m = len(shift_rows)
    shift_rows.append([])
    shift_rows.append([("TOTAL", S.BOLD), "", "", "", (f"=SUM(E2:E{m})", S.DEC), (f"=SUM(F2:F{m})", S.DEC),
                       f"=SUM(G2:G{m})", f"=SUM(H2:H{m})", (f"=SUM(I2:I{m})", S.BOLD_MONEY),
                       (f"=IF(E{m + 2}>0,I{m + 2}/E{m + 2},0)", S.MONEY)])

    # Weekly hours & money (Mon-Sun weeks)
    weeks = defaultdict(lambda: {"hours": 0.0, "gross": 0.0, "doors": 0, "sales": 0})
    for s in ordered:
        d = dt(s["start"]).date()
        wk = d - timedelta(days=d.weekday())
        st = stats[s["id"]]
        weeks[wk]["hours"] += st["hours"]; weeks[wk]["gross"] += st["gross"]
        weeks[wk]["doors"] += st["doors"]; weeks[wk]["sales"] += len(st["sales"])
    weekly = [[(h, S.BOLD) for h in ["Week of (Mon)", "Hours", "Gross", "$ / hour", "Doors", "Sales"]]]
    for i, (wk, w) in enumerate(sorted(weeks.items()), start=2):
        weekly.append([f"{wk:%Y-%m-%d}", (round(w["hours"], 2), S.DEC), (round(w["gross"], 2), S.MONEY),
                       (f"=IF(B{i}>0,C{i}/B{i},0)", S.MONEY), w["doors"], w["sales"]])

    tax = [
        [("Tax & Take-Home Estimate", S.TITLE)],
        ["Change the yellow cells to match your situation. Everything else updates automatically."],
        [],
        [("Inputs", S.BOLD)],
        ["Federal income tax rate (your bracket)", (0.12, S.INPUT_PCT)],
        ["State income tax rate", (0.05, S.INPUT_PCT)],
        ["Self-employment tax rate (Social Security + Medicare)", (0.153, S.INPUT_PCT)],
        ["Portion of profit subject to SE tax", (0.9235, S.INPUT_PCT)],
        ["IRS mileage rate ($ per mile) — check irs.gov for this year", (0.70, S.INPUT_MONEY)],
        ["Count tracked miles as business driving? (1 = yes, 0 = no)", (1, S.INPUT)],
        ["Other business expenses (supplies, phone, etc.)", (0, S.INPUT_MONEY)],
        [],
        [("Results", S.BOLD)],
        ["Gross income (all receipts)", (f"=Receipts!G{n + 2}", S.MONEY)],     # B14
        ["Hours worked", ("=Shifts!E" + str(m + 2), S.DEC)],                          # B15
        ["Miles tracked", ("=Shifts!F" + str(m + 2), S.DEC)],                         # B16
        ["Mileage deduction", ("=B16*B9*B10", S.MONEY)],                              # B17
        ["Net profit (taxable)", ("=MAX(0,B14-B17-B11)", S.MONEY)],                   # B18
        ["Self-employment tax", ("=B18*B8*B7", S.MONEY)],                             # B19
        ["Federal income tax (estimate)", ("=MAX(0,B18-B19/2)*B5", S.MONEY)],         # B20
        ["State income tax (estimate)", ("=B18*B6", S.MONEY)],                        # B21
        [("TOTAL TO SET ASIDE FOR TAXES", S.BOLD), ("=B19+B20+B21", S.BOLD_MONEY)],    # B22
        ["Set-aside as % of gross", ("=IF(B14>0,B22/B14,0)", S.PCT)],                 # B23
        [("Take-home after taxes & expenses", S.BOLD), ("=B14-B11-B22", S.BOLD_MONEY)],  # B24
        ["Average $ per hour (before tax)", ("=IF(B15>0,B14/B15,0)", S.MONEY)],
        ["Average $ per hour (after tax)", ("=IF(B15>0,B24/B15,0)", S.MONEY)],
        [],
        ["Quarterly estimated payments: if you expect to owe $1,000+ for the year, the IRS wants payments "
         "in April, June, September and January (Form 1040-ES)."],
        ["These are estimates, not tax advice. The federal line ignores the standard deduction and credits, "
         "so it usually runs high. Confirm with a tax preparer."],
    ]

    door_rows = [[(h, S.BOLD) for h in ["Date", "Time", "Weekday", "Hour", "Result", "Reason / note", "Street",
                                        "Address", "Amount", "Lat", "Lng", "Photo file"]]]
    for v in visits:
        t = dt(v["createdAt"])
        door_rows.append([f"{t:%Y-%m-%d}", f"{t:%I:%M %p}", f"{t:%A}", t.hour, OUTCOME.get(v.get("type"), v.get("type")),
                          " — ".join(x for x in [v.get("reason"), v.get("note")] if x), street_of(v.get("address")),
                          v.get("address", ""), (float(v.get("amount") or 0), S.MONEY) if v.get("type") == "sale" else "",
                          v.get("lat") if v.get("lat") is not None else "", v.get("lng") if v.get("lng") is not None else "",
                          v.get("photo_file") or ""])

    path = REPORTS / "earnings.xlsx"
    xlsx.write_xlsx(path, [
        {"name": "Tax Estimate", "rows": tax, "widths": [58, 18]},
        {"name": "Receipts", "rows": receipts, "widths": [10, 12, 10, 30, 30, 22, 12, 12, 26, 18], "freeze": 1},
        {"name": "Shifts", "rows": shift_rows, "widths": [12, 10, 10, 16, 8, 8, 8, 8, 12, 10, 18], "freeze": 1},
        {"name": "Weekly", "rows": weekly, "widths": [14, 8, 12, 10, 8, 8], "freeze": 1},
        {"name": "All Doors", "rows": door_rows, "widths": [12, 10, 11, 6, 11, 30, 20, 30, 10, 11, 11, 18], "freeze": 1},
    ])
    # Plain CSV copy for anything that can't open .xlsx
    with open(REPORTS / "all_doors.csv", "w", newline="") as f:
        w = csv.writer(f)
        for row in door_rows:
            w.writerow([c[0] if isinstance(c, tuple) else c for c in row])
    return path


# ---------------------------------------------------------------- AI report
AI_PROMPT = """You are helping a door-to-door service worker earn more per hour.
Attached are photos of houses I knocked on. Each photo's file name starts with the result:
SALE (bought, with the amount), NO (answered and declined), NOT-HOME, or COME-BACK.

Please:
1. Compare the SALE houses with the NO houses. List visible features that show up more in one group
   (yard care, cars in the driveway, house size/age, kids' toys, decorations, existing work that needs doing,
   security cameras/Ring doorbells, "No Soliciting" signs, gates, dogs, etc.). Say how confident you are.
2. Give me a simple "knock / skip / knock later" checklist I can use from the sidewalk in 3 seconds.
3. Using the numbers below, tell me the best days/hours and streets, and which ones to drop.
4. Suggest 3 things to say or change to turn more NOs and COME BACKs into sales.
5. Tell me what extra info I should log to make next week's analysis better.
Be honest when the sample is too small to be sure."""


def build_ai_report(visits, shifts, stats, cfg):
    out = REPORTS / "ai"
    sales = [v for v in visits if v.get("type") == "sale"]
    answered = [v for v in visits if v.get("type") in ("sale", "no", "callback")]
    hours = sum(st["hours"] for st in stats.values())
    gross = sum(float(v.get("amount") or 0) for v in sales)

    def table(title, key):
        groups = defaultdict(lambda: Counter())
        money_by = defaultdict(float)
        for v in visits:
            k = key(v)
            groups[k][v.get("type")] += 1
            if v.get("type") == "sale":
                money_by[k] += float(v.get("amount") or 0)
        lines = [f"### {title}", "", "| | Doors | Answered | Sales | Close rate | $ |", "|---|---|---|---|---|---|"]
        for k in sorted(groups, key=lambda k: (str(k))):
            c = groups[k]
            ans = c["sale"] + c["no"] + c["callback"]
            lines.append(f"| {k} | {sum(c.values())} | {ans} | {c['sale']} | "
                         f"{(c['sale'] / ans * 100 if ans else 0):.0f}% | {money_by[k]:,.0f} |")
        return "\n".join(lines) + "\n"

    reasons = Counter(v.get("reason") or "(none given)" for v in visits if v.get("type") == "no")
    md = [f"# Door-to-door performance report — {datetime.now():%B %d, %Y}", "",
          f"Worker: {cfg.get('your_name') or ''}  ", f"Business: {cfg.get('business_name') or ''}", "",
          "## Totals", "",
          f"- Shifts: {len(shifts)} · Hours: {hours:.1f} · Miles tracked: {sum(s['miles'] for s in stats.values()):.1f}",
          f"- Doors knocked: {len(visits)} · Answered: {len(answered)} · Sales: {len(sales)}",
          f"- Close rate (of people who answered): {(len(sales) / len(answered) * 100 if answered else 0):.0f}%",
          f"- Money made: ${gross:,.2f} · Average sale: ${(gross / len(sales) if sales else 0):,.2f}",
          f"- Per hour: ${(gross / hours if hours else 0):,.2f} · Per door: ${(gross / len(visits) if visits else 0):,.2f}",
          "",
          table("By weekday", lambda v: f"{dt(v['createdAt']).isoweekday()} {dt(v['createdAt']):%A}"),
          table("By hour of day", lambda v: f"{dt(v['createdAt']):%H}:00"),
          table("By street", lambda v: street_of(v.get("address"))),
          "### Reasons people said no", "",
          *[f"- {r}: {n}" for r, n in reasons.most_common()], "",
          "## Every door", "", "| Photo file | Result | When | Street | Amount | Reason / note |", "|---|---|---|---|---|---|"]

    zpath = out / "ai_package.zip"
    contact = []
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for i, v in enumerate(visits, start=1):
            res = OUTCOME.get(v.get("type"), "?").replace(" ", "-")
            amt = f"_${float(v.get('amount') or 0):.0f}" if v.get("type") == "sale" else ""
            street = re.sub(r"[^A-Za-z0-9]+", "-", street_of(v.get("address")))[:30]
            label = f"{i:04d}_{res}{amt}_{street}.jpg"
            if v.get("photo_file") and (PHOTOS / v["photo_file"]).exists():
                z.write(PHOTOS / v["photo_file"], f"photos/{label}")
                contact.append((v, label))
            t = dt(v["createdAt"])
            note = " — ".join(x for x in [v.get("reason"), v.get("note"), v.get("description")] if x)
            md.append(f"| {label if v.get('photo_file') else '(no photo)'} | {res} | {t:%a %I:%M %p} | {street_of(v.get('address'))} | "
                      f"{('$' + format(float(v.get('amount') or 0), ',.0f')) if v.get('type') == 'sale' else ''} | {note.replace('|', '/')} |")
        md += ["", "## Prompt for the AI", "", AI_PROMPT, ""]
        report = "\n".join(md)
        z.writestr("REPORT.md", report)
    (out / "REPORT.md").write_text(report)

    cells = "".join(
        f"<figure><img src='../../photos/{e(v['photo_file'])}'><figcaption><b class='{v.get('type')}'>{e(OUTCOME.get(v.get('type')))}"
        f"{(' ' + money(v.get('amount'))) if v.get('type') == 'sale' else ''}</b><br>{dt(v['createdAt']):%a %I:%M %p} · "
        f"{e(street_of(v.get('address')))}<br><small>{e(v.get('reason') or v.get('description') or '')}</small></figcaption></figure>"
        for v, _ in contact)
    (out / "contact_sheet.html").write_text(f"""<!doctype html><html><head><meta charset="utf-8"><title>House photo contact sheet</title>
<style>body{{font:13px system-ui,sans-serif;margin:16px}} .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}}
figure{{margin:0;border:1px solid #ccc;border-radius:8px;overflow:hidden;page-break-inside:avoid}} img{{width:100%;height:150px;object-fit:cover}}
figcaption{{padding:6px}} .sale{{color:#15803d}} .no{{color:#b91c1c}} .not_home{{color:#b45309}} .callback{{color:#1d4ed8}}
@media print{{.noprint{{display:none}}}}</style></head><body>
<p class="noprint"><button onclick="print()">Print / Save as PDF</button> <a href="/dashboard">← Dashboard</a></p>
<h2>House photos by result</h2><div class="grid">{cells or '<p>No photos yet.</p>'}</div></body></html>""")
    return zpath


def analyze_with_claude():
    """Optional: send the AI report and photos straight to Claude. Needs `pip install anthropic` and an API key."""
    try:
        import anthropic
    except ImportError:
        return "The 'anthropic' package isn't installed. Run:  pip install anthropic   then set ANTHROPIC_API_KEY."
    zpath = REPORTS / "ai" / "ai_package.zip"
    if not zpath.exists():
        rebuild()
    content = []
    with zipfile.ZipFile(zpath) as z:
        report = z.read("REPORT.md").decode()
        photos = [n for n in z.namelist() if n.startswith("photos/")]
        # Keep a balanced sample: every sale and an equal share of the rest, max 40 images.
        sale_p = [n for n in photos if "_SALE_" in n]
        other = [n for n in photos if "_SALE_" not in n]
        pick = sale_p[:20] + other[:40 - min(20, len(sale_p))]
        for n in pick:
            content.append({"type": "text", "text": n.split("/", 1)[1]})
            content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                         "data": base64.b64encode(z.read(n)).decode()}})
    content.append({"type": "text", "text": report})
    client = anthropic.Anthropic()
    resp = client.beta.messages.create(
        model="claude-opus-5-5",
        max_tokens=16000,
        betas=["server-side-fallback-2026-07-01"],
        extra_body={"fallbacks": "default"},  # retry on another model if this one declines
        messages=[{"role": "user", "content": content}],
    )
    if resp.stop_reason == "refusal":
        return "Claude declined to analyze this batch. Try removing unusual photos and run again."
    text = "".join(b.text for b in resp.content if b.type == "text")
    out = REPORTS / "ai" / f"analysis_{datetime.now():%Y-%m-%d_%H%M}.md"
    out.write_text(text)
    return f"Saved: {out}\n\n{text}"


# ---------------------------------------------------------------- survey emails
def load_sent():
    try:
        return json.loads(SURVEYS_PATH.read_text())
    except Exception:
        return {}


def due_surveys(visits, cfg):
    sent = load_sent()
    cutoff = (time.time() - float(cfg.get("survey_days_after") or 0) * 86400) * 1000
    return [v for v in visits if v.get("type") == "sale" and v.get("email") and "@" in v["email"]
            and v["id"] not in sent and v["createdAt"] <= cutoff]


def survey_message(v, cfg):
    biz = v.get("business") or cfg.get("business_name") or "us"
    first = (v.get("customerName") or "").split(" ")[0] or "there"
    msg = EmailMessage()
    msg["Subject"] = f"Your receipt from {biz} + a quick 1-minute survey"
    msg["From"] = cfg.get("from_email") or cfg.get("smtp_user") or "me@example.com"
    msg["To"] = v["email"]
    when = dt(v["createdAt"])
    text = (f"Hi {first},\n\nThanks for choosing {biz} on {when:%B %d}. Your receipt is attached "
            f"(#{v.get('receiptNo')}, {money(v.get('amount'))} for {v.get('description') or 'service'}).\n\n"
            f"Would you take one minute to tell us how we did?\n{cfg.get('survey_url')}\n\n"
            f"Thank you!\n{v.get('worker') or cfg.get('your_name') or ''}\n{biz}\n\n"
            "You got this email because you asked for a copy of your receipt. Reply STOP and we won't email again.")
    msg.set_content(text)
    msg.add_alternative(f"""<p>Hi {e(first)},</p><p>Thanks for choosing <b>{e(biz)}</b> on {when:%B %d}.
Your receipt is attached (#{e(v.get('receiptNo'))}, <b>{money(v.get('amount'))}</b> for {e(v.get('description') or 'service')}).</p>
<p><a href="{e(cfg.get('survey_url'))}" style="background:#0f766e;color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none">Take the 1-minute survey</a></p>
<p>Thank you!<br>{e(v.get('worker') or cfg.get('your_name') or '')}<br>{e(biz)}</p>
<p style="color:#777;font-size:12px">You got this email because you asked for a copy of your receipt. Reply STOP and we won't email again.</p>""",
                        subtype="html")
    rpath = build_single_receipt(v, cfg)
    msg.add_attachment(rpath.read_bytes(), maintype="text", subtype="html", filename=rpath.name)
    return msg


def send_surveys(force_all=False):
    cfg = load_config()
    visits, _ = load_all()
    for v in reversed(visits):
        cfg["your_name"] = cfg.get("your_name") or v.get("worker") or ""
        cfg["business_name"] = cfg.get("business_name") or v.get("business") or ""
    due = due_surveys(visits, cfg) if not force_all else [v for v in visits if v.get("email") and v.get("type") == "sale"]
    if not due:
        return "No surveys are due yet."
    sent = load_sent()
    results = []
    use_smtp = bool(cfg.get("smtp_user") and cfg.get("smtp_password"))
    server = None
    try:
        if use_smtp:
            server = smtplib.SMTP(cfg["smtp_host"], int(cfg["smtp_port"]), timeout=30)
            server.starttls()
            server.login(cfg["smtp_user"], cfg["smtp_password"])
        for v in due:
            msg = survey_message(v, cfg)
            if server:
                server.send_message(msg)
                sent[v["id"]] = {"at": time.time(), "to": v["email"], "how": "smtp"}
                results.append(f"sent → {v['email']}")
            else:
                p = REPORTS / "outbox" / f"survey-{v.get('receiptNo') or v['id']}.eml"
                msg["X-Unsent"] = "1"  # opens as a draft in Outlook / Apple Mail
                p.write_bytes(bytes(msg))
                sent[v["id"]] = {"at": time.time(), "to": v["email"], "how": "draft"}
                results.append(f"draft saved → {p.name}")
    finally:
        if server:
            server.quit()
        SURVEYS_PATH.write_text(json.dumps(sent, indent=1))
    if not use_smtp:
        results.append(f"Drafts are in {REPORTS / 'outbox'} — double-click to open in your mail app and press Send. "
                       f"To send automatically, fill in the email settings in {CONFIG_PATH}.")
    return "\n".join(results)


# ---------------------------------------------------------------- rebuild + dashboard
_last = {"msg": ""}


def rebuild():
    with lock:
        import_inbox()
        cfg = load_config()
        visits, shifts = load_all()
        # Fill name/business from the phone if the laptop config doesn't have them
        for v in reversed(visits):
            cfg["your_name"] = cfg.get("your_name") or v.get("worker") or ""
            cfg["business_name"] = cfg.get("business_name") or v.get("business") or ""
        for s in shifts.values():
            cfg["your_name"] = cfg.get("your_name") or s.get("worker") or ""
        stats = {sid: shift_stats(s, visits) for sid, s in shifts.items()}
        links = {sid: build_shift_report(s, stats[sid], cfg) for sid, s in shifts.items()}
        for v in visits:
            if v.get("type") == "sale":
                build_single_receipt(v, cfg)
        build_spreadsheet(visits, shifts, stats)
        build_ai_report(visits, shifts, stats, cfg)
        build_dashboard(visits, shifts, stats, links, cfg)
    return len(visits), len(shifts)


def build_dashboard(visits, shifts, stats, links, cfg):
    rows = []
    for s in sorted(shifts.values(), key=lambda s: -s["start"]):
        st = stats[s["id"]]
        hrs = "—" if s.get("untracked") else f"{st['hours']:.2f}"
        rows.append(f"<tr><td><a href='/files/reports/shifts/{e(links[s['id']])}'>{dt(s['start']):%a %b %d %Y}</a></td>"
                    f"<td class='num'>{hrs}</td>"
                    f"<td class='num'>{st['miles']:.1f}</td><td class='num'>{len(st['sales'])}/{st['doors']}</td>"
                    f"<td class='num'>{money(st['gross'])}</td></tr>")
    hours = sum(st["hours"] for st in stats.values())
    gross = sum(st["gross"] for st in stats.values())
    week0 = datetime.now().date() - timedelta(days=datetime.now().weekday())
    wk = [s for s in shifts.values() if dt(s["start"]).date() >= week0]
    wk_gross = sum(stats[s["id"]]["gross"] for s in wk)
    wk_hours = sum(stats[s["id"]]["hours"] for s in wk)
    due = len(due_surveys(visits, cfg))
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Door Receipts Dashboard</title><style>{PRINT_CSS}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}} .c{{border:1px solid #ddd;border-radius:10px;padding:12px}}
.c b{{display:block;font-size:22px}} pre{{white-space:pre-wrap;background:#f6f6f6;padding:10px;border-radius:8px}} .drop{{border:2px dashed #aaa;padding:16px;border-radius:10px;text-align:center}}</style></head><body>
<h1>{e(cfg.get('business_name') or 'Door Receipts')} — Dashboard</h1>
<p class="muted">Data folder: {e(DATA)} · Updated {datetime.now():%I:%M %p}</p>
<div class="cards">
 <div class="c"><b>{money(wk_gross)}</b>This week ({wk_hours:.1f} h)</div>
 <div class="c"><b>{money(gross)}</b>All time</div>
 <div class="c"><b>{hours:.1f}</b>Hours worked</div>
 <div class="c"><b>{money(gross / hours if hours else 0)}</b>Per hour</div>
 <div class="c"><b>{sum(v.get('type') == 'sale' for v in visits)}/{len(visits)}</b>Sales / doors</div>
</div>
<h2>Reports</h2>
<p><a class="btn" href="/files/reports/earnings.xlsx">⬇ Tax &amp; hours spreadsheet (.xlsx)</a>
<a class="btn" href="/files/reports/all_doors.csv">⬇ All doors (.csv)</a></p>
<h2>Shifts</h2>
<table><tr><th>Shift (click to print)</th><th class="num">Hours</th><th class="num">Miles</th><th class="num">Sales/Doors</th><th class="num">Money</th></tr>
{''.join(rows) or '<tr><td colspan=5>No data yet — sync from your phone.</td></tr>'}</table>
<h2>AI coach</h2>
<p>Upload these to your AI chat: the <a href="/files/reports/ai/REPORT.md">report</a> plus the
<a href="/files/reports/ai/ai_package.zip">photo package (.zip)</a>, or print the
<a href="/files/reports/ai/contact_sheet.html">photo contact sheet</a> to PDF and upload that.</p>
<p><button class="btn" onclick="act('/api/analyze', this)">Ask Claude directly (needs API key)</button></p>
<h2>Customer surveys</h2>
<p>{due} survey email(s) due (sent {e(cfg.get('survey_days_after'))} days after the visit).
<button class="btn" onclick="act('/api/surveys', this)">Send due surveys</button></p>
<p class="muted">Email settings &amp; survey link: {e(CONFIG_PATH)}</p>
<h2>Import a sync file (iPhone / no cable)</h2>
<div class="drop"><input type="file" id="imp" accept=".json"> </div>
<pre id="out" hidden></pre>
<script>
async function act(url, btn) {{
  const out = document.getElementById('out'); out.hidden = false; out.textContent = 'Working…'; btn.disabled = true;
  try {{ const r = await fetch(url, {{method:'POST'}}); out.textContent = (await r.json()).message; }}
  catch (err) {{ out.textContent = 'Error: ' + err; }} finally {{ btn.disabled = false; }}
}}
document.getElementById('imp').onchange = async ev => {{
  const f = ev.target.files[0]; if (!f) return;
  const out = document.getElementById('out'); out.hidden = false; out.textContent = 'Importing…';
  const r = await fetch('/api/sync', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: await f.text()}});
  await fetch('/api/rebuild', {{method:'POST'}}); out.textContent = (await r.json()).message; setTimeout(() => location.reload(), 800);
}};
</script></body></html>"""
    (REPORTS / "dashboard.html").write_text(doc)


# ---------------------------------------------------------------- web server
class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        if args and "/api/" in str(args[0]):
            sys.stderr.write("  " + fmt % args + "\n")

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def translate_path(self, path):
        p = urlparse(path).path
        if p.startswith("/files/"):
            base, rel = DATA, p[len("/files/"):]
        else:
            base, rel = PHONE_DIR, p.lstrip("/")
        target = (base / rel).resolve()
        if base.resolve() not in target.parents and target != base.resolve():
            return str(base / "__nope__")
        return str(target)

    def end_headers(self):
        if not self.path.startswith("/files/"):
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/api/ping":
            return self._json({"ok": True, "hub": "door-receipts", "time": time.time()})
        if p in ("/dashboard", "/dashboard/"):
            f = REPORTS / "dashboard.html"
            if not f.exists():
                rebuild()
            body = f.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            return self.wfile.write(body)
        return super().do_GET()

    def do_POST(self):
        p = urlparse(self.path).path
        try:
            n = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(n) if n else b"{}"
            if p == "/api/sync":
                nv, ns = ingest(json.loads(raw or b"{}"))
                print(f"  ✓ received {nv} visits, {ns} shifts")
                return self._json({"ok": True, "message": f"Imported {nv} visits and {ns} shifts."})
            if p == "/api/rebuild":
                nv, ns = rebuild()
                return self._json({"ok": True, "message": f"Reports rebuilt ({nv} visits, {ns} shifts)."})
            if p == "/api/surveys":
                return self._json({"ok": True, "message": send_surveys()})
            if p == "/api/analyze":
                return self._json({"ok": True, "message": analyze_with_claude()})
        except Exception as ex:
            return self._json({"ok": False, "message": f"Error: {ex}"}, 500)
        self._json({"ok": False, "message": "unknown"}, 404)


def find_adb():
    """Find adb on PATH or in the usual places people unzip platform-tools."""
    found = shutil.which("adb")
    if found:
        return found
    exe = "adb.exe" if os.name == "nt" else "adb"
    home = Path.home()
    for folder in (HERE / "platform-tools", HERE.parent / "platform-tools", Path("C:/platform-tools"),
                   home / "platform-tools", home / "Downloads" / "platform-tools",
                   home / "Desktop" / "platform-tools",
                   home / "AppData/Local/Android/Sdk/platform-tools", home / "Library/Android/sdk/platform-tools"):
        if (folder / exe).exists():
            return str(folder / exe)
    return None


def adb_watcher():
    """Link any USB-connected Android phone to this hub (phone's localhost:PORT -> laptop)."""
    adb = find_adb()
    if not adb:
        print("  (USB tool not found — unzip Android platform-tools into C:\\platform-tools or your Downloads folder, then restart)")
        return
    linked = set()
    while True:
        try:
            out = subprocess.run([adb, "devices"], capture_output=True, text=True, timeout=10).stdout
            now = {l.split()[0] for l in out.splitlines()[1:] if l.strip().endswith("\tdevice")}
            for serial in now - linked:
                r = subprocess.run([adb, "-s", serial, "reverse", f"tcp:{PORT}", f"tcp:{PORT}"],
                                   capture_output=True, text=True, timeout=10)
                if r.returncode == 0:
                    print(f"  📱 Phone connected ({serial}) — open the Receipts app and tap Sync")
                    linked.add(serial)
            for serial in linked - now:
                print(f"  📱 Phone unplugged ({serial})")
            linked &= now
            for line in out.splitlines()[1:]:
                if line.strip().endswith("\tunauthorized"):
                    print("  📱 Phone found — tap 'Allow USB debugging' on the phone screen")
        except Exception:
            pass
        time.sleep(3)


def serve():
    setup_dirs()
    rebuild()
    host = "0.0.0.0" if "--lan" in sys.argv else "127.0.0.1"
    httpd = ThreadingHTTPServer((host, PORT), Handler)
    threading.Thread(target=adb_watcher, daemon=True).start()
    print(f"\nDoor Receipts hub running.\n  Dashboard: http://localhost:{PORT}/dashboard\n"
          f"  Phone app: plug in your phone, then open http://localhost:{PORT} in Chrome on the phone\n"
          f"  Data:      {DATA}\n  Press Ctrl+C to stop.\n")
    if "--no-browser" not in sys.argv:
        threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PORT}/dashboard")).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "serve"
    setup_dirs()
    if cmd == "serve":
        serve()
    elif cmd == "rebuild":
        print("Rebuilt: %d visits, %d shifts" % rebuild())
    elif cmd == "surveys":
        rebuild()
        print(send_surveys())
    elif cmd == "analyze":
        rebuild()
        print(analyze_with_claude())
    else:
        print(__doc__)
