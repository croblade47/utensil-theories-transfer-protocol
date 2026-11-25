"""Extract plain text from Google Docs API JSON (as saved by the read_doc tool).

Usage: python3 -I gdoc_text.py <out_dir> <read_doc_result.json>...
Writes <out_dir>/<documentId>.txt for each input.
"""
import json, os, sys

def walk(content, out):
    for el in content or []:
        if 'paragraph' in el:
            for pe in el['paragraph'].get('elements', []):
                tr = pe.get('textRun')
                if tr:
                    out.append(tr.get('content', ''))
                elif 'equation' in pe or 'inlineObjectElement' in pe:
                    out.append(' ')
        elif 'table' in el:
            for row in el['table'].get('tableRows', []):
                for cell in row.get('tableCells', []):
                    walk(cell.get('content'), out)
                    out.append('\t')
                out.append('\n')
        elif 'tableOfContents' in el:
            walk(el['tableOfContents'].get('content'), out)

def doc_text(d):
    d = d.get('content', d)
    out = []
    tabs = d.get('tabs') or [{'documentTab': {'body': d.get('body', {})}}]
    stack = list(tabs)
    while stack:
        t = stack.pop(0)
        walk(t.get('documentTab', {}).get('body', {}).get('content'), out)
        stack[0:0] = t.get('childTabs', [])
    return d.get('documentId'), d.get('title', ''), ''.join(out)

if __name__ == '__main__':
    os.makedirs(sys.argv[1], exist_ok=True)
    for p in sys.argv[2:]:
        doc_id, title, text = doc_text(json.load(open(p)))
        open(os.path.join(sys.argv[1], f'{doc_id}.txt'), 'w').write(f'# {title}\n{text}')
        print(f'{doc_id}\t{len(text)} chars\t{title}')
