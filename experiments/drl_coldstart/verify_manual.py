"""Step 2 check: is every verbatim quote in the cold-start manual really in its source,
and are the user's three expected rules present in the archive?

Usage: python3 -I verify_manual.py <manual.json> <sources_dir> <out_report.json>
Matching ignores whitespace, markdown escapes/emphasis, LaTeX backslashes and quote style.
"""
import glob, json, os, re, sys

def canon(s):
    s = s.replace('\\', '').replace('*', '').replace('$', '')
    s = re.sub(r'[“”"]', '"', s); s = re.sub(r"[‘’']", "'", s)
    return re.sub(r'\s+', ' ', s).strip().lower()

EXPECTED = {  # the three rules as the user stated them, split into checkable phrases
    'R1 Objective & Drift Guard': ["comprehend", "understand", "improves communication",
                                   "every step must serve that", "drift guard"],
    'R2 Veridian DRL Gate': ["record keeping", "veridian", "technical invariants",
                             "troubleshooting noise", "transient"],
    'R3 CCG Phase IV (D.R.L.)': ["phase iv: dependent reconstruction logic (d.r.l.)",
                                 "p(s_{t} | s_{t-1})", "c_{text{ccg}} = (i times m) + e + d + delta"],
}

def main(manual_path, src_dir, out):
    m = json.load(open(manual_path))
    texts = {os.path.basename(p)[:-4]: canon(open(p).read()) for p in glob.glob(f'{src_dir}/*.txt')}
    corpus = ' '.join(texts.values())
    quotes = [('objective', m['objective'])] + [('drift_guard_rule', r) for r in m['drift_guard_rules']] \
           + [('definition', d) for d in m['definitions_and_formulas']]
    rows = []
    for kind, q in quotes:
        src = q.get('source_id')
        if src not in texts:
            rows.append({'kind': kind, 'source': q.get('source_title'), 'status': 'source not on disk', 'q': q['verbatim'][:90]})
            continue
        ok = canon(q['verbatim']) in texts[src]
        rows.append({'kind': kind, 'source': q.get('source_title'), 'status': 'VERBATIM' if ok else 'NOT FOUND', 'q': q['verbatim'][:90]})
    expected = {}
    for rule, phrases in EXPECTED.items():
        expected[rule] = {p: [k for k, t in texts.items() if p in t] for p in phrases}
    rep = {'quotes': rows, 'counts': {s: sum(r['status'] == s for r in rows) for s in {r['status'] for r in rows}},
           'expected_rules': expected, 'sources_checked': sorted(texts)}
    json.dump(rep, open(out, 'w'), indent=1, ensure_ascii=False)
    print('quote check:', rep['counts'])
    for r in rows:
        if r['status'] != 'VERBATIM':
            print(' ', r['status'], '|', r['source'], '|', r['q'])
    for rule, ph in expected.items():
        print(rule)
        for p, hits in ph.items():
            print(f"   {'FOUND' if hits else 'absent':6} {p!r} {len(hits)} source(s)")

if __name__ == '__main__':
    main(*sys.argv[1:4])
