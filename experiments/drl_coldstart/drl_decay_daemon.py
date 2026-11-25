"""60-minute "waking from a dream" decay daemon.

t = 0      : the full wake state is loaded into memory (prompt-by-prompt traces,
             per-episode noise weights, invariants, vector graph).
t = 1..60  : every tick, each decaying item's weight becomes
             w_i(t) = s_i * exp(-LAMBDA * t)     (s_i = item salience in (0, 1])
             and items with w_i(t) < PRUNE_AT are dropped from memory.
             Invariants and the [X, Y, noise] vector graph are locked (never decay).
t = 60     : the locked part is written to drl_wake_state.json, which must be < 50 KB.

LAMBDA is set so a salience-1.0 item falls to 1% at t = 60 (half-life ~9 min).

Usage:
  python3 -I drl_decay_daemon.py <wake_state_t0.json> <out_dir> [--minutes 60] [--tick-seconds 60]
"""
import argparse, json, math, os, time
from datetime import datetime, timezone

MINUTES = 60
LAMBDA = math.log(100) / MINUTES
PRUNE_AT = 0.01  # salience 1.0 items survive to t = 60; 0.3 items fade by ~t = 44
SIZE_LIMIT = 50_000  # bytes


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def locked_state(state, t, trimmed=0):
    return {
        'schema': 'drl_wake_state/v1',
        'written_at': now(),
        'decay': {'t_minutes': t, 'lambda_per_min': round(LAMBDA, 5),
                  'half_life_min': round(math.log(2) / LAMBDA, 2), 'prune_at': PRUNE_AT,
                  'raw_items_at_t0': state['meta']['raw_items_at_t0'],
                  'raw_items_now': len(state['decaying'])},
        'manual': state['manual'],
        'vector_graph': state['vector_graph'],
        'invariants': state['invariants'],
        'invariants_trimmed_for_size': trimmed,
        'sources': state['meta'].get('sources', {}),
    }


def fit_under_limit(state, t):
    """Drop lowest-priority invariants until the locked file fits in SIZE_LIMIT."""
    inv = sorted(state['invariants'], key=lambda i: -i.get('priority', 0.5))
    trimmed = 0
    while True:
        state['invariants'] = inv
        blob = json.dumps(locked_state(state, t, trimmed), ensure_ascii=False, separators=(',', ':'))
        if len(blob.encode()) < SIZE_LIMIT or not inv:
            return blob
        inv = inv[:-1]
        trimmed += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('wake_state')
    ap.add_argument('out_dir')
    ap.add_argument('--minutes', type=int, default=MINUTES)
    ap.add_argument('--tick-seconds', type=float, default=60.0)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)

    state = json.load(open(a.wake_state))           # t = 0: everything in memory
    state['meta']['raw_items_at_t0'] = len(state['decaying'])
    log = open(os.path.join(a.out_dir, 'decay_log.jsonl'), 'w')

    for t in range(0, a.minutes + 1):
        if t:
            time.sleep(a.tick_seconds)
        kept = []
        for item in state['decaying']:
            item['w'] = round(item['s'] * math.exp(-LAMBDA * t), 5)
            if item['w'] >= PRUNE_AT:
                kept.append(item)
        state['decaying'] = kept
        live = json.dumps(state, ensure_ascii=False)
        with open(os.path.join(a.out_dir, 'drl_wake_state.live.json'), 'w') as f:
            f.write(live)
        rec = {'t': t, 'at': now(), 'raw_items': len(kept),
               'mean_w': round(sum(i['w'] for i in kept) / len(kept), 4) if kept else 0,
               'memory_bytes': len(live.encode())}
        log.write(json.dumps(rec) + '\n'); log.flush()
        print(json.dumps(rec), flush=True)

    blob = fit_under_limit(state, a.minutes)
    with open(os.path.join(a.out_dir, 'drl_wake_state.json'), 'w') as f:
        f.write(blob)
    os.remove(os.path.join(a.out_dir, 'drl_wake_state.live.json'))  # process "wakes": raw memory gone
    print(f'final drl_wake_state.json: {len(blob.encode())} bytes '
          f'(limit {SIZE_LIMIT}); raw items left in memory: {len(state["decaying"])}', flush=True)


if __name__ == '__main__':
    main()
