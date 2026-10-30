"""Aggregate per-era ingestion output into (a) the monthly [X, Y, noise] vector table and
(b) the t = 0 wake state consumed by drl_decay_daemon.py.

Usage: python3 -I build_wake_state.py <manual.json> <ingest_dir> <out_wake_state_t0.json> <out_table.md>

Month rows are plain means over scorable docs. The locked vector graph follows the archive's
own DRL / CCG rules (verified verbatim in the cold-start manual):
  - "only the trajectory seed and delta transforms are retained"  -> seed + per-segment deltas
  - P(S_t | S_{t-1})                                               -> S_t = S_{t-1} + Δ_t
  - "cryptography verifies"                                        -> SHA-256 hash chain over Δ_t
Values are stored as integer hundredths so replaying the deltas reproduces the table exactly.
"""
import glob, hashlib, json, re, sys
from collections import OrderedDict

# Salience at t = 0 for each decaying memory kind (1.0 decays slowest).
SALIENCE = {'drift_event': 1.0, 'evidence': 0.8, 'prompt_trace': 0.6, 'noise_episode': 0.3}


def clamp(v):
    return max(-1.0, min(1.0, float(v)))


def norm(s):
    return re.sub(r'\W+', ' ', s.lower()).strip()


def h100(v):
    return int(round(v * 100))


def flags_for(r, prev):
    f = []
    if r['X'] is None:
        return 'no scorable docs'
    if r['Y'] - r['X'] <= -0.3:
        f.append('DRIFT: syntax held, intent lost')
    if prev is not None and r['Y'] - prev['Y'] <= -0.3:
        f.append('Y fell ≥0.3 vs prior segment')
    if r['noise'] <= -0.3:
        f.append('unresolved noise loops')
    return '; '.join(f)


def encode_chain(rows):
    """Seed + deltas + hash chain. Segments without scorable docs carry S_{t-1} forward (ΔX=ΔY=0)."""
    state, prev_hash, deltas, seed = None, '0' * 64, [], None
    for r in rows:
        cur = [h100(r['X']) if r['X'] is not None else None,
               h100(r['Y']) if r['Y'] is not None else None, h100(r['noise'])]
        if state is None:
            if cur[0] is None:
                continue  # chain starts at the first scored segment
            seed = {'segment': r['segment'], 'S_hundredths': cur}
            state = cur[:]
            d = [0, 0, 0]
        else:
            nxt = [cur[0] if cur[0] is not None else state[0],
                   cur[1] if cur[1] is not None else state[1], cur[2]]
            d = [nxt[i] - state[i] for i in range(3)]
            state = nxt
        link = hashlib.sha256(f"{prev_hash}|{r['segment']}|{d}".encode()).hexdigest()
        deltas.append([r['segment'], *d, r['docs'], r['scored'], r['flag'], link[:12]])
        prev_hash = link
    return {'encoding': 'S_t = S_{t-1} + delta_t, values in hundredths [X, Y, noise]; '
                        'hash_t = sha256(hash_{t-1}|segment|delta_t)',
            'seed': seed, 'deltas_cols': ['segment', 'dX', 'dY', 'dNoise', 'docs', 'scored', 'flag', 'hash12'],
            'deltas': deltas, 'head_hash': prev_hash}


def replay(chain):
    """Rebuild every S_t from seed + deltas and re-derive the hash chain."""
    s, h, out = None, '0' * 64, []
    for seg, dx, dy, dn, *_rest, h12 in chain['deltas']:
        s = chain['seed']['S_hundredths'][:] if s is None else [s[0] + dx, s[1] + dy, s[2] + dn]
        h = hashlib.sha256(f"{h}|{seg}|{[dx, dy, dn]}".encode()).hexdigest()
        assert h[:12] == h12, f'hash mismatch at {seg}'
        out.append((seg, s[:]))
    assert h == chain['head_hash']
    return out


def main(manual_path, ingest_dir, out_state, out_table):
    manual = json.load(open(manual_path))
    files = sorted(glob.glob(f'{ingest_dir}/E*.json'))
    docs = []
    for p in files:
        docs += json.load(open(p))['docs']
    docs.sort(key=lambda d: d['date'])

    months = OrderedDict()
    decaying, invariants, seen_inv, per_doc = [], [], set(), []
    for d in docs:
        if d.get('read_status') == 'skipped_off_project':
            continue
        months.setdefault(d['date'][:7], []).append(d)
        noise = d.get('noise') or {}
        nv = clamp((noise.get('direction') or 0) * (noise.get('fraction') or 0))
        d['_noise'] = nv
        tag = d['id'][-8:]
        if d.get('scorable'):
            per_doc.append([d['date'][:10], tag, round(clamp(d['X']), 2), round(clamp(d['Y']), 2), round(nv, 2)])
        for i, line in enumerate(d.get('prompt_trace') or []):
            decaying.append({'kind': 'prompt_trace', 'doc': tag, 'n': i + 1, 'text': line, 's': SALIENCE['prompt_trace']})
        for k in ('X_evidence', 'Y_evidence'):
            if d.get(k):
                decaying.append({'kind': 'evidence', 'doc': tag, 'axis': k[0], 'text': d[k], 's': SALIENCE['evidence']})
        for e in d.get('drift_events') or []:
            decaying.append({'kind': 'drift_event', 'doc': tag, 'text': e.get('quote', ''),
                             'note': e.get('what', ''), 's': SALIENCE['drift_event']})
        for e in noise.get('episodes') or []:
            decaying.append({'kind': 'noise_episode', 'doc': tag, 'text': e.get('what', ''),
                             'turns': e.get('turns'), 'resolved': e.get('resolved'), 's': SALIENCE['noise_episode']})
        for inv in d.get('invariants') or []:
            key = norm(inv.get('verbatim', ''))[:160]
            if key and key not in seen_inv:
                seen_inv.add(key)
                invariants.append({'v': inv['verbatim'], 'type': inv.get('type'), 'src': tag,
                                   'date': d['date'][:10], 'priority': inv.get('priority', 0.5)})

    rows, prev = [], None
    for m, ds in months.items():
        sc = [d for d in ds if d.get('scorable')]
        r = {'segment': m, 'docs': len(ds), 'scored': len(sc),
             'X': round(sum(clamp(d['X']) for d in sc) / len(sc), 2) if sc else None,
             'Y': round(sum(clamp(d['Y']) for d in sc) / len(sc), 2) if sc else None,
             'noise': round(sum(d['_noise'] for d in ds) / len(ds), 2)}
        r['flag'] = flags_for(r, prev)
        r['dY'] = round(r['Y'] - prev['Y'], 2) if (r['Y'] is not None and prev) else None
        rows.append(r)
        if r['X'] is not None:
            prev = r

    chain = encode_chain(rows)
    rebuilt = dict(replay(chain))
    for r in rows:  # replay must reproduce every scored segment exactly
        if r['X'] is not None:
            assert rebuilt[r['segment']][:2] == [h100(r['X']), h100(r['Y'])], r['segment']

    state = {
        'meta': {'built_from': files, 'docs': len(docs),
                 'sources': {d['id'][-8:]: [d['date'][:10], d['title'][:60]] for d in docs}},
        'manual': {'objective_archive': manual.get('objective', {}).get('verbatim'),
                   'objective_operator': "Increase an LLM's ability to 'comprehend' and 'understand' in a way "
                                         "that improves communication. Every step must serve that.",
                   'steps': [s.get('instruction') for s in manual.get('operating_manual_steps', [])]},
        'vector_graph': {**chain, 'per_doc_cols': ['date', 'doc', 'X', 'Y', 'noise'], 'per_doc': per_doc},
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
    print(f"\nreplay check passed; head hash {chain['head_hash'][:16]}…")
    print(f"wake state t0: {len(decaying)} decaying items, {len(invariants)} invariants, {len(per_doc)} scored docs")


if __name__ == '__main__':
    main(*sys.argv[1:5])
