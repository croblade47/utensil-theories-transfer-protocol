"""Aggregate per-era ingestion output into (a) the monthly [X, Y, noise] vector table and
(b) the t = 0 wake state consumed by drl_decay_daemon.py.

Usage: python3 -I build_wake_state.py <manual.json> <ingest_dir> <out_wake_state_t0.json> <out_table.md>

Per-doc fields come from the aligned ingestion agents (see ingest_prompt.md).
Month rows are plain means over scorable docs; the chain step (S_t given S_{t-1})
is in chain_state() below.
"""
import glob, json, re, sys
from collections import OrderedDict

# Salience at t = 0 for each decaying memory kind (1.0 decays slowest).
SALIENCE = {'drift_event': 1.0, 'evidence': 0.8, 'prompt_trace': 0.6, 'noise_episode': 0.3}


def clamp(v):
    return max(-1.0, min(1.0, float(v)))


def norm(s):
    return re.sub(r'\W+', ' ', s.lower()).strip()


def chain_state(rows):
    """S_t evaluated conditionally on S_{t-1}: Delta is the step change in each axis,
    and the gap Y - X flags drift (literal grasp without intent grasp)."""
    prev = None
    for r in rows:
        if r['X'] is None:
            r.update(dX=None, dY=None, gap=None, flag='no scorable docs')
            continue
        r['gap'] = round(r['Y'] - r['X'], 2)
        if prev is None:
            r['dX'] = r['dY'] = 0.0
        else:
            r['dX'] = round(r['X'] - prev['X'], 2)
            r['dY'] = round(r['Y'] - prev['Y'], 2)
        flags = []
        if r['gap'] <= -0.3:
            flags.append('DRIFT: syntax held, intent lost')
        if prev is not None and r['dY'] <= -0.3:
            flags.append('Y dropped vs prior segment')
        if r['noise'] <= -0.3:
            flags.append('unresolved noise loops')
        r['flag'] = '; '.join(flags)
        prev = r
    return rows


def main(manual_path, ingest_dir, out_state, out_table):
    manual = json.load(open(manual_path))
    docs = []
    for p in sorted(glob.glob(f'{ingest_dir}/E*.json')):
        docs += json.load(open(p))['docs']
    docs.sort(key=lambda d: d['date'])

    months = OrderedDict()
    decaying, invariants, seen_inv, per_doc = [], [], set(), []
    for d in docs:
        m = d['date'][:7]
        months.setdefault(m, []).append(d)
        noise = d.get('noise') or {}
        nv = clamp(noise.get('direction', 0) * noise.get('fraction', 0))
        d['_noise'] = nv
        tag = d['id'][-8:]
        if d.get('scorable'):
            per_doc.append([d['date'][:10], tag, round(clamp(d['X']), 2), round(clamp(d['Y']), 2), round(nv, 2)])
        for i, line in enumerate(d.get('prompt_trace') or []):
            decaying.append({'kind': 'prompt_trace', 'doc': tag, 'n': i + 1, 'text': line,
                             's': SALIENCE['prompt_trace']})
        for k in ('X_evidence', 'Y_evidence'):
            if d.get(k):
                decaying.append({'kind': 'evidence', 'doc': tag, 'axis': k[0], 'text': d[k],
                                 's': SALIENCE['evidence']})
        for e in d.get('drift_events') or []:
            decaying.append({'kind': 'drift_event', 'doc': tag, 'text': e.get('quote', ''),
                             'note': e.get('what', ''), 's': SALIENCE['drift_event']})
        for e in noise.get('episodes') or []:
            decaying.append({'kind': 'noise_episode', 'doc': tag, 'text': e.get('what', ''),
                             'turns': e.get('turns'), 'resolved': e.get('resolved'),
                             's': SALIENCE['noise_episode']})
        for inv in d.get('invariants') or []:
            key = norm(inv['verbatim'])[:160]
            if key and key not in seen_inv:
                seen_inv.add(key)
                invariants.append({'v': inv['verbatim'], 'type': inv.get('type'),
                                   'src': d['id'], 'date': d['date'][:10],
                                   'priority': inv.get('priority', 0.5)})

    rows = []
    for m, ds in months.items():
        sc = [d for d in ds if d.get('scorable')]
        rows.append({'segment': m, 'docs': len(ds), 'scored': len(sc),
                     'X': round(sum(clamp(d['X']) for d in sc) / len(sc), 2) if sc else None,
                     'Y': round(sum(clamp(d['Y']) for d in sc) / len(sc), 2) if sc else None,
                     'noise': round(sum(d['_noise'] for d in ds) / len(ds), 2)})
    rows = chain_state(rows)

    state = {
        'meta': {'built_from': sorted(glob.glob(f'{ingest_dir}/E*.json')), 'docs': len(docs),
                 'sources': {d['id'][-8:]: [d['date'][:10], d['title'][:60]] for d in docs}},
        'manual': {'objective': manual.get('objective', {}).get('verbatim'),
                   'steps': [s.get('instruction') for s in manual.get('operating_manual_steps', [])]},
        'vector_graph': {'segments': rows,
                         'per_doc_cols': ['date', 'doc', 'X', 'Y', 'noise'], 'per_doc': per_doc},
        'invariants': invariants,
        'decaying': decaying,
    }
    json.dump(state, open(out_state, 'w'), ensure_ascii=False)

    fmt = lambda v: '—' if v is None else f'{v:+.2f}'
    lines = ['| Segment | Docs (scored) | X Comprehension | Y Understanding | Noise (+/-) | ΔY | Flag |',
             '|---|---|---|---|---|---|---|']
    for r in rows:
        lines.append(f"| {r['segment']} | {r['docs']} ({r['scored']}) | {fmt(r['X'])} | {fmt(r['Y'])} | "
                     f"{fmt(r['noise'])} | {fmt(r['dY'])} | {r['flag']} |")
    open(out_table, 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    print(f"\nwake state t0: {len(decaying)} decaying items, {len(invariants)} invariants, "
          f"{len(per_doc)} scored docs")


if __name__ == '__main__':
    main(*sys.argv[1:5])
