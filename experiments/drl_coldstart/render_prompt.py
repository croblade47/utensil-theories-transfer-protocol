"""Fill ingest_prompt.md for one era. The output is the exact prompt given to that era's agent.

Usage: python3 -I render_prompt.py <era> <scratch_dir>    (era = E1..E6)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def render(era, sp):
    n = int(era[1:])
    prior = ('There is no prior state: this is the first era, so S_{t-1} is empty (S_0). '
             'Build the initial direction from what you read.') if n == 1 else \
            (f'Read {sp}/ingest/E{n-1}.json and take its "state_out" as S_{{t-1}} '
             '(direction, open threads, invariant index). Glance at its last few docs\' X/Y too.')
    vals = {'MANUAL': f'{sp}/coldstart/drl_manual.json', 'PRIOR': prior,
            'PLAN': f'{sp}/ingest/plan/era_{era}.json', 'OUT': f'{sp}/ingest/{era}.json',
            'TEXT_DIR': f'{sp}/ingest/text', 'SCRIPTS': HERE, 'ERA': era}
    s = open(os.path.join(HERE, 'ingest_prompt.md')).read()
    for k, v in vals.items():
        s = s.replace('{' + k + '}', v)
    return s

if __name__ == '__main__':
    print(render(*sys.argv[1:3]))
