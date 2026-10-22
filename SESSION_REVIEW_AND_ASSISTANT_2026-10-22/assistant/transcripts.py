"""Exact index of Claude Code session transcripts: who said what, and when.

Garrett C. Gauthier is the owner and sole author of this project and its ideas.
This tool was built with Claude (Anthropic) in Claude Code, a tool used by the owner.

Input: transcript pages saved from the claude-code-remote list_events tool, one
folder per session (see README.md in this folder for how to fetch them). Each page is kept as
it was saved; this tool only reads them.

Usage:
    python3 transcripts.py build  PAGES_DIR [CACHE_DIR]   # parse every session folder
    python3 transcripts.py stats                          # counts per session and kind
    python3 transcripts.py owner  [SESSION]               # every owner message, numbered, full text
    python3 transcripts.py turn   SESSION N               # owner message N, the replies, the final reply
    python3 transcripts.py search TEXT [KIND]             # every entry containing TEXT (case-insensitive)
    python3 transcripts.py last   SESSION [K]             # the last K entries of a session

Kinds of entry:
    owner        typed by the owner in the app (client_platform present)
    relayed      sent into the session by another Claude session (inbound_origin);
                 it may carry the owner's words, but was not typed there
    interrupt    the owner stopped a reply
    hook         automatic hook feedback (not the owner)
    notice       automatic task notifications (not the owner)
    reply        a text block written by Claude in the main conversation
    final        the final reply that ended a turn (from the turn's result event)

The cache (index.jsonl) holds transcript text. It may contain personal details,
so keep it out of the public repository (default: ~/.cache/project_assistant).
"""
import glob, json, os, sys

CACHE = os.environ.get("ASSISTANT_CACHE", os.path.expanduser("~/.cache/project_assistant"))


def load_page(path):
    s = open(path, encoding="utf-8").read()
    i, j = s.find('{"ccr"'), s.rfind('}}') + 2
    return json.loads(s[i:j])["ccr"].get("data", [])


def text_of(content):
    if isinstance(content, str):
        return content, 0
    parts, images = [], 0
    for b in content or []:
        if b.get("type") == "text":
            parts.append(b.get("text", ""))
        elif b.get("type") == "image":
            images += 1
    return "\n".join(parts), images


def classify_user(inner, content):
    if isinstance(content, list) and any(b.get("type") == "tool_result" for b in content):
        return None
    text, images = text_of(content)
    origin = inner.get("origin") or {}
    if inner.get("isSynthetic") or text.startswith("Stop hook feedback"):
        kind = "hook"
    elif isinstance(origin, dict) and origin.get("kind") == "task-notification":
        kind = "notice"
    elif text.strip() == "[Request interrupted by user]":
        kind = "interrupt"
    elif inner.get("inbound_origin"):
        kind = "relayed"
    elif "client_platform" in inner:
        kind = "owner"
    else:
        kind = "notice"
    return kind, text, images


def build(pages_dir, cache=CACHE):
    os.makedirs(cache, exist_ok=True)
    out = []
    for sdir in sorted(glob.glob(os.path.join(pages_dir, "session_*"))):
        session = os.path.basename(sdir)
        seen, entries = set(), []
        for p in sorted(glob.glob(os.path.join(sdir, "*.txt"))):
            for e in load_page(p):
                kinds = [k for k in e if k != "created_at"]
                if not kinds:
                    continue
                k = kinds[0]
                body = e[k] if isinstance(e[k], dict) else {}
                inner = body.get("internal_anthropic_catchall", body)
                uuid = body.get("uuid") or inner.get("uuid")
                if uuid in seen:
                    continue
                seen.add(uuid)
                t = e.get("created_at", "")
                if k == "user":
                    r = classify_user(inner, inner.get("message", {}).get("content"))
                    if r:
                        kind, text, images = r
                        entries.append({"session": session, "uuid": uuid, "time": t, "kind": kind,
                                        "text": text, "images": images})
                elif k == "assistant" and not inner.get("parent_tool_use_id"):
                    text, _ = text_of(inner.get("message", {}).get("content"))
                    if text.strip():
                        entries.append({"session": session, "uuid": uuid, "time": t, "kind": "reply", "text": text})
                elif k == "result":
                    res = inner.get("result")
                    if isinstance(res, str) and res.strip():
                        entries.append({"session": session, "uuid": uuid, "time": t, "kind": "final", "text": res,
                                        "for": inner.get("user_message_uuids") or [inner.get("user_message_uuid")]})
        entries.sort(key=lambda x: x["time"])
        n = 0
        for x in entries:
            if x["kind"] in ("owner", "relayed"):
                n += 1
                x["n"] = n
        out.extend(entries)
    with open(os.path.join(cache, "index.jsonl"), "w", encoding="utf-8") as f:
        for x in out:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    return out


def index(cache=CACHE):
    with open(os.path.join(cache, "index.jsonl"), encoding="utf-8") as f:
        return [json.loads(l) for l in f]


def show(x, full=True):
    head = "[%s] %s %s%s" % (x["time"][:19].replace("T", " "), x["session"][-8:], x["kind"],
                            (" #%d" % x["n"]) if "n" in x else "")
    if x.get("images"):
        head += " (+%d image)" % x["images"]
    body = x["text"] if full else x["text"][:300].replace("\n", " ")
    print(head + "\n" + body + "\n")


if __name__ == "__main__":
    a = sys.argv[1:]
    cmd = a[0] if a else "stats"
    if cmd == "build":
        out = build(a[1], a[2] if len(a) > 2 else CACHE)
        print("indexed %d entries" % len(out))
        cmd = "stats"
    ix = index()
    if cmd == "stats":
        from collections import Counter
        c = Counter((x["session"], x["kind"]) for x in ix)
        for s in sorted({x["session"] for x in ix}):
            ts = [x["time"] for x in ix if x["session"] == s]
            print(s, ts[0][:16], "to", ts[-1][:16], {k: v for (ss, k), v in c.items() if ss == s})
    elif cmd == "owner":
        for x in ix:
            if x["kind"] in ("owner", "relayed", "interrupt") and (len(a) < 2 or x["session"].endswith(a[1])):
                show(x)
    elif cmd == "turn":
        s, n = a[1], int(a[2])
        sx = [x for x in ix if x["session"].endswith(s)]
        start = next(i for i, x in enumerate(sx) if x.get("n") == n)
        show(sx[start])
        for x in sx[start + 1:]:
            if x["kind"] in ("owner", "relayed"):
                break
            show(x)
    elif cmd == "search":
        q = a[1].lower()
        for x in ix:
            if q in x["text"].lower() and (len(a) < 3 or x["kind"] == a[2]):
                show(x, full=False)
    elif cmd == "last":
        s, k = a[1], int(a[2]) if len(a) > 2 else 5
        for x in [x for x in ix if x["session"].endswith(s)][-k:]:
            show(x)
