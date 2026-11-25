"""Write recovered Claude conversations as turn-numbered text files (one per chat).

Usage: python3 -I export_claude_convs.py <conversations.jsonl> <out_dir>
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_manifest import EXCLUDE

def text_of(m):
    parts = [m.get('text') or '']
    for c in m.get('content') or []:
        if c.get('type') == 'text' and c.get('text') and c['text'] not in parts:
            parts.append(c['text'])
    return '\n'.join(p for p in parts if p).strip()

def main(src, out):
    os.makedirs(out, exist_ok=True)
    index = []
    for line in open(src):
        c = json.loads(line)
        if EXCLUDE.search(c['name']):
            continue
        fn = f"{c['created_at'][:10]}_{c['uuid'][:8]}.txt"
        with open(os.path.join(out, fn), 'w') as f:
            f.write(f"# {c['name']}\n# created {c['created_at']}\n\n")
            for i, m in enumerate(c.get('chat_messages') or [], 1):
                f.write(f"--- turn {i} [{m.get('sender')}] ---\n{text_of(m)}\n\n")
        index.append({'id': 'claude_export:' + c['uuid'], 'title': c['name'], 'created': c['created_at'],
                      'month': c['created_at'][:7], 'kind': 'claude_chat_local',
                      'path': os.path.join(out, fn), 'turns': len(c.get('chat_messages') or [])})
    json.dump(index, open(os.path.join(out, 'index.json'), 'w'), indent=1, ensure_ascii=False)
    print(len(index), 'project conversations written')

if __name__ == '__main__':
    main(*sys.argv[1:3])
