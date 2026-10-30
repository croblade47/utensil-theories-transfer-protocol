"""Merge Drive manifest + local Claude chats and split the timeline into sequential eras.

Usage: python3 -I plan_eras.py <manifest.json> <claude_index.json> <out_dir>
"""
import json, os, sys

ERAS = [  # (name, first month, last month) — contiguous, chronological
    ('E1', '2023-07', '2025-04'),
    ('E2', '2025-05', '2025-08'),
    ('E3', '2025-09', '2026-01'),
    ('E4', '2026-02', '2026-02'),
    ('E5', '2026-03', '2026-08'),
    ('E6', '2026-09', '2026-10'),
]

def main(manifest, claude_index, out):
    docs = json.load(open(manifest))['docs'] + json.load(open(claude_index))
    docs.sort(key=lambda d: d['created'])
    os.makedirs(out, exist_ok=True)
    # The Drive connector can't open AI Studio chat files (unsupported mime type),
    # so they're listed per era as a coverage gap instead of being sent to the agents.
    for name, lo, hi in ERAS:
        sel = [d for d in docs if lo <= d['month'] <= hi and d['kind'] != 'aistudio_chat']
        gap = [d for d in docs if lo <= d['month'] <= hi and d['kind'] == 'aistudio_chat']
        json.dump({'era': name, 'from': lo, 'to': hi, 'docs': sel, 'unreadable': gap},
                  open(os.path.join(out, f'era_{name}.json'), 'w'), indent=1, ensure_ascii=False)
        print(name, lo, hi, len(sel), 'docs readable,', len(gap), 'AI Studio chats unreadable')

if __name__ == '__main__':
    main(*sys.argv[1:4])
