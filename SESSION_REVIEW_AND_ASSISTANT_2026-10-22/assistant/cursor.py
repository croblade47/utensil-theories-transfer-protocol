"""Show where a saved transcript page ends, so the next page can be fetched.

Usage: python3 cursor.py [saved_page_file]
With no file, it uses the newest saved list_events page in the session's
tool-results folder. Prints: has_more, number of events, first and last
event id, first and last time. Page forward with after_id=last_id,
or backward with before_id=first_id.
"""
import glob, json, os, sys

def load_page(path):
    s = open(path, encoding="utf-8").read()
    i = s.find('{"ccr"')
    j = s.rfind('}}') + 2
    return json.loads(s[i:j])["ccr"]

def newest_page():
    files = glob.glob("/root/.claude/projects/*/*/tool-results/mcp-claude-code-remote-list_events-*.txt")
    return max(files, key=os.path.getmtime)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else newest_page()
    d = load_page(path)
    ev = d.get("data", [])
    times = [e.get("created_at") for e in ev if e.get("created_at")]
    print(os.path.basename(path), "has_more=%s" % d.get("has_more"), "n=%d" % len(ev),
          "first_id=%s" % d.get("first_id"), "last_id=%s" % d.get("last_id"), "time=%s..%s" % (times[0] if times else "?", times[-1] if times else "?"))
