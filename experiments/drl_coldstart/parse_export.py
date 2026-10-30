"""Recover complete records from a Drive-rendered (markdown-escaped, truncated) JSON export.

Usage: python3 -I parse_export.py <raw_text_file> <out_jsonl>
"""
import json, re, sys

MD_ESC = re.compile(r'\\([\\`*_{}\[\]()#+\-.!|<>~"\'=&])')

def unescape(s: str) -> str:
    return MD_ESC.sub(r'\1', s)

def recover(text: str):
    dec = json.JSONDecoder()
    i = text.index('[') + 1
    out = []
    while True:
        while i < len(text) and text[i] in ' \n\r\t,':
            i += 1
        if i >= len(text) or text[i] == ']':
            break
        try:
            obj, i = dec.raw_decode(text, i)
        except json.JSONDecodeError:
            break  # truncated tail
        out.append(obj)
    return out

if __name__ == '__main__':
    raw = open(sys.argv[1], encoding='utf-8').read()
    recs = recover(unescape(raw))
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f'recovered {len(recs)} complete records')
