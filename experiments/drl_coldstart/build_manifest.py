"""Merge Drive search results into a deduped, chronological corpus manifest.

Usage: python3 -I build_manifest.py <out_manifest.json> <search_result.json>...
Keeps chat logs and project docs; drops unrelated personal/legal/medical files,
binary formats the reader can't open, and "Copy of"/"Branch of" duplicates.
"""
import json, re, sys
from collections import OrderedDict

KEEP_MIME = {
    'application/vnd.google-apps.document': 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'application/vnd.google-makersuite.prompt': 'aistudio_chat',
    'text/markdown': 'md', 'text/plain': 'txt', 'application/json': 'json',
}
# Personal, legal, medical or off-project titles. Matching is case-insensitive.
EXCLUDE = re.compile(r"lawyer|claim|contingency|ombudsperson|complaint|tax |throuple|my likes|"
    r"mental ?health|decriminal|\bmva\b|legal|settlement|who the fuck|mustang|christie|candy|"
    r"jokes|superman|love's|loan|adolescent|microsoft store|class notes|m[ée]tis|stoic|avery|"
    r"sandvik|reviewed- gauthier|creature image|global reset|call forwarding|lease_|"
    r"conversations\.json|projects\.json|applet_access_history|cybersecurity|solidus", re.I)
DATE_IN_TITLE = re.compile(r'^(\d{4}-\d{2}-\d{2})T')
START = '2023-07'  # experiment window: July 2023 -> today
DUP_PREFIX = re.compile(r'^((copy of|branch of)\s+)+', re.I)

def main(out, paths):
    seen = OrderedDict()
    for p in paths:
        for f in json.load(open(p)).get('files', []):
            seen.setdefault(f['id'], f)
    rows, dropped = [], {'mime': 0, 'excluded': 0, 'duplicate': 0}
    titles = {}
    for f in seen.values():  # export files carry their real date in the filename
        m = DATE_IN_TITLE.match(f['title'])
        f['_date'] = m.group(1) + 'T00:00:00Z' if m else f['createdTime']
    for f in sorted(seen.values(), key=lambda f: f['_date']):
        kind = KEEP_MIME.get(f['mimeType'])
        if not kind:
            dropped['mime'] += 1; continue
        if EXCLUDE.search(f['title']):
            dropped['excluded'] += 1; continue
        if f['_date'][:7] < START:
            dropped.setdefault('before_window', []).append(f"{f['_date'][:10]} {f['title']}"); continue
        size = int(f.get('fileSize', 0) or 0)
        base = DUP_PREFIX.sub('', f['title']).strip().lower()
        prev = titles.get(base)
        is_copy = bool(DUP_PREFIX.match(f['title']))
        if prev is not None and (is_copy or abs(prev - size) <= max(64, 0.02 * size)):
            dropped['duplicate'] += 1; continue
        titles.setdefault(base, size)
        rows.append({'id': f['id'], 'title': f['title'], 'created': f['_date'],
                     'month': f['_date'][:7], 'kind': kind, 'bytes': size})
    json.dump({'docs': rows, 'dropped': dropped}, open(out, 'w'), indent=1, ensure_ascii=False)
    print(f'{len(rows)} docs kept; dropped {dropped}')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
