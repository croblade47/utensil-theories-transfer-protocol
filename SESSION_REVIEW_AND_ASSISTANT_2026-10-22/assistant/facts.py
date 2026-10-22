"""Project fact checker: recompute every headline result from the raw files.

Garrett C. Gauthier is the owner and sole author of this project and its ideas.
This tool was built with Claude (Anthropic) in Claude Code, a tool used by the owner.

Usage (from the repository top):
    python3 tools/assistant/facts.py            # all facts and claim checks
    python3 tools/assistant/facts.py long_story # one topic (see TOPICS below)
    python3 tools/assistant/facts.py --json     # machine-readable

Every number printed here is computed from a raw results file (named next to
it), or read from git. Nothing is typed in by hand except the CLAIMS, which are
the handoff's wording, so each claim can be checked against the raw data.
"""
import json, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EXP = os.path.join(ROOT, "experiments")


def load(name):
    with open(os.path.join(EXP, name), encoding="utf-8") as f:
        return json.load(f)


def pct(xs):
    return 100.0 * sum(xs) / len(xs) if xs else float("nan")


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


facts = []   # (topic, name, value, source)
checks = []  # (topic, claim, computed, verdict)


def fact(topic, name, value, source):
    facts.append((topic, name, value, source))


def check(topic, claim, computed, ok):
    checks.append((topic, claim, computed, "MATCH" if ok else "DIFFERS"))


def close(a, b, tol):
    return abs(a - b) <= tol


# ---------- experiment 8: judging and consequences (100 new pairs) ----------
def judging():
    d = load("results_confirm.json")
    out = {}
    for m in ("shifting", "baseline", "scrambled"):
        per = [pct(d["%s/seed%d" % (m, s)]["v2_judge"]) for s in range(3)]
        cons = [pct(d["%s/seed%d" % (m, s)]["v2_shift"]) for s in range(3)]
        out[m] = (per, cons)
        fact("judging", "%s judging, 3 runs" % m, "%s (mean %.1f)" % (per, mean(per)),
             "results_confirm.json %s/seed*/v2_judge" % m)
        fact("judging", "%s consequences, 3 runs" % m, "%s (mean %.1f)" % (cons, mean(cons)),
             "results_confirm.json %s/seed*/v2_shift" % m)
    s, b = mean(out["shifting"][0]), mean(out["baseline"][0])
    check("judging", "Labeling right/wrong: judging about 69 vs 50 per 100",
          "%.1f vs %.1f" % (s, b), close(s, 69, 1) and close(b, 50, 1))
    beats = all(x > y for x, y in zip(out["shifting"][0], out["baseline"][0]))
    check("judging", "...in all 3 runs", "shifting > no marker in each run: %s" % beats, beats)


# ---------- experiment 10: shifting word vs plain label (method comparison) ----------
def methods():
    d = load("results_methods.json")
    res = {}
    for m in ("shifting", "label", "carry3", "baseline", "scrambled"):
        keys = sorted(k for k in d if k.startswith(m + "/"))
        per = [pct(d[k]["v2_judge"]) for k in keys]
        res[m] = per
        fact("methods", "%s judging (exp 10)" % m, "%s (mean %.1f)" % (per, mean(per)),
             "results_methods.json %s/seed*/v2_judge" % m)
    s, l = mean(res["shifting"]), mean(res["label"])
    check("methods", "Exp 10: shifting word ties the plain label on short stories (about 68-71% each)",
          "shifting %.1f, label %.1f" % (s, l), abs(s - l) <= 3 and 66 <= min(s, l) and max(s, l) <= 72)


# ---------- experiment 11: long stories ----------
def long_story():
    d = load("results_long_story.json")
    res = {}
    for m in ("shifting", "label", "carry3", "baseline", "scrambled"):
        for cond in ("B", "A", "short"):
            per, ties = [], []
            for s in range(3):
                c = d["%s/seed%d/%s" % (m, s, cond)]["correct"]
                per.append(round(pct(c), 1))
                ties.append(sum(1 for x in c if x == 0.5))
            res[(m, cond)] = per
            fact("long_story", "%s condition %s" % (m, cond),
                 "%s (mean %.1f), ties per run %s" % (per, mean(per), ties),
                 "results_long_story.json %s/seed*/%s/correct" % (m, cond))
    sB, lB = mean(res[("shifting", "B")]), mean(res[("label", "B")])
    check("long_story", "Long stories, everyday act: carry 59 vs label 53",
          "%.1f vs %.1f" % (sB, lB), close(sB, 59, 1) and close(lB, 53, 1))
    check("long_story", "Stated verdict (A): label won (73, 51, 97)",
          "label %s vs shifting %s" % (res[("label", "A")], res[("shifting", "A")]),
          res[("label", "A")] == [73.0, 51.0, 97.0])
    # where the gap comes from: answered vs tie
    both = sr = lr = sa = sar = la = lar = 0
    for s in range(3):
        a = d["shifting/seed%d/B" % s]["correct"]
        b = d["label/seed%d/B" % s]["correct"]
        for x, y in zip(a, b):
            if x != 0.5 and y != 0.5:
                both += 1; sr += x == 1; lr += y == 1
        sa += sum(x != 0.5 for x in a); sar += sum(x == 1 for x in a)
        la += sum(y != 0.5 for y in b); lar += sum(y == 1 for y in b)
    fact("long_story", "B, pairs answered (not a tie), 300 in all",
         "carry answered %d (right %d); label answered %d (right %d)" % (sa, sar, la, lar),
         "results_long_story.json shifting|label/seed*/B/correct")
    fact("long_story", "B, pairs both answered",
         "%d pairs: carry right %d, label right %d" % (both, sr, lr),
         "results_long_story.json shifting|label/seed*/B/correct")
    check("long_story", "Drift check (22 Oct): the gap comes from answering more often, not judging better",
          "both answered %d: carry %d vs label %d right" % (both, sr, lr), sr == lr)


# ---------- experiment 7 and 6: the 20-pair tests ----------
def small_tests():
    d = load("results_shifting_word.json")
    sw = [d[k]["self_shift"] / d[k]["n_pairs"] * 100 for k in sorted(d) if k.startswith("shifting_word")]
    sc = [d[k]["self_shift"] / d[k]["n_pairs"] * 100 for k in sorted(d) if k.startswith("scrambled")]
    fact("small_tests", "Exp 7 shifting word, consequence pairs (20)", "%s (mean %.1f)" % (sw, mean(sw)),
         "results_shifting_word.json shifting_word/*/self_shift")
    fact("small_tests", "Exp 7 scrambled control (20)", "%s (mean %.1f)" % (sc, mean(sc)),
         "results_shifting_word.json scrambled_control/*/self_shift")
    check("small_tests", "Exp 7: 68% vs 52% scrambled on 20 stories", "%.1f vs %.1f" % (mean(sw), mean(sc)),
          close(mean(sw), 68, 1) and close(mean(sc), 52, 1))
    t = load("results_transformer.json")["full/seed0/steps1500"]
    v = 100.0 * t["shift"] / t["n_pairs"]
    fact("small_tests", "Exp 6 tiny transformer, consequences (20)", "%.0f%%" % v,
         "results_transformer.json full/seed0/steps1500/shift")
    check("small_tests", "Exp 6: chance on consequences (45-55%)", "%.0f%%" % v, 45 <= v <= 55)


# ---------- experiment 9: Aesop (from the script's own printed summary) ----------
def aesop():
    txt = open(os.path.join(EXP, "results_aesop.txt"), encoding="utf-8").read()
    got = {}
    for name in ("stories", "novels", "stories_shuffled", "bible", "rules", "narrative"):
        m = re.search(r"^\s+%s\s+([0-9.]+)\s" % re.escape(name), txt.split("AESOP MORAL TEST")[-1], re.M)
        if m:
            got[name] = float(m.group(1)) * 100
            fact("aesop", "%s, same-format pairs" % name, "%.1f" % got[name], "results_aesop.txt summary table")
    for line in re.findall(r"^\s+(P\d\w*.*)$", txt.split("PRE-REGISTERED VERDICT")[-1].split("DESCRIPTIVE")[0], re.M):
        fact("aesop", "verdict line", line.strip(), "results_aesop.txt PRE-REGISTERED VERDICT")
    claim = {"stories": 52.3, "novels": 54.1, "stories_shuffled": 53.1, "bible": 43.6}
    ok = all(close(got.get(k, -1), v, 0.05) for k, v in claim.items())
    check("aesop", "Aesop: folk tales 52.3, novels 54.1, shuffled 53.1, Bible 43.6",
          ", ".join("%s %.1f" % (k, got.get(k, float("nan"))) for k in claim), ok)


# ---------- experiment 12: understanding as compression ----------
def compression():
    d = load("results_understanding.json")
    r = d["rungs"]
    for k in ("R0_raw", "R1_zlib9", "R1_xz9e", "R4_word_freq", "R5_word_pairs",
              "R6_baseline_seed0", "R6_baseline_seed1", "R6_baseline_seed2"):
        if k in r:
            fact("compression", k, "%s bytes, %.3f bits/char, exact %s" % (r[k]["seed_bytes"], r[k]["bpc"], r[k]["exact"]),
                 "results_understanding.json rungs/%s" % k)
    p = d["preregistered"]
    fact("compression", "pre-registered: shifting vs baseline",
         "%+.2f bits per verse, p = %s, %s" % (p["mean_diff_bits_per_verse"], p["perm_p_one_sided"], p["verdict"]),
         "results_understanding.json preregistered")
    b = d["method_summary"]["baseline"]["bpc_total_mean"]
    check("compression", "Compression ladder: 8.0 -> 1.17 bits per character",
          "raw %.3f -> transformer mean %.3f" % (r["R0_raw"]["bpc"], b),
          close(r["R0_raw"]["bpc"], 8.0, 0.01) and close(b, 1.17, 0.01))
    x = r["R6_baseline_seed0"]["seed_bytes"] / r["R1_xz9e"]["seed_bytes"]
    check("compression", "Tiny model seed is less than half of xz", "ratio %.2f" % x, x < 0.5)
    check("compression", "Shifting word did not help compression (about +3.45 bits/verse, NOT CONFIRMED)",
          "%+.2f, %s" % (p["mean_diff_bits_per_verse"], p["verdict"]),
          p["verdict"] == "NOT CONFIRMED" and close(p["mean_diff_bits_per_verse"], 3.45, 0.01))


# ---------- numbers test (paused) ----------
def numbers():
    d = load("results_numbers.json")
    done = sorted(d.get("M1", {}))
    cfg = d["meta"]["frozen"]["CONFIGS"]
    total = len(cfg) * len(d["meta"]["frozen"]["seeds"])
    fact("numbers", "models finished", "%d of %d (%s)" % (len(done), total, ", ".join(done)),
         "results_numbers.json M1 keys; meta/frozen CONFIGS x seeds")
    for k in done:
        fact("numbers", "%s judging (partial, no verdict)" % k, "%.0f" % pct(d["M1"][k]["v2_judge"]),
             "results_numbers.json M1/%s/v2_judge" % k)
    check("numbers", "Numbers test paused at 3 of 18 models", "%d of %d" % (len(done), total),
          len(done) == 3 and total == 18)


# ---------- git: when the pass/fail rules were saved ----------
def git_times():
    commits = {"99622d3": "long-story rules saved", "c93f383": "long-story fix: ties count 0.5",
               "6fc220d": "long-story fix: first marker out of view", "6e365ef": "exp 10 rules saved",
               "01b9050": "exp 11 write-up (message says 'L2 confirmed')"}
    for h, what in commits.items():
        try:
            t = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%cI %s", h],
                               capture_output=True, text=True, check=True).stdout.strip()
        except Exception as e:
            t = "not found (%s)" % e.__class__.__name__
        fact("git", "%s %s" % (h, what), t, "git log")


TOPICS = {"judging": judging, "methods": methods, "long_story": long_story, "small_tests": small_tests,
          "aesop": aesop, "compression": compression, "numbers": numbers, "git": git_times}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for name in (args or TOPICS):
        TOPICS[name]()
    if "--json" in sys.argv:
        print(json.dumps({"facts": facts, "checks": checks}, indent=1))
        sys.exit(0)
    topic = None
    for t, n, v, s in facts:
        if t != topic:
            print("\n== %s ==" % t); topic = t
        print("  %s: %s\n      [%s]" % (n, v, s))
    print("\n== CLAIM CHECKS (handoff wording vs raw data) ==")
    for t, c, v, ok in checks:
        print("  %-7s %s\n          computed: %s" % (ok, c, v))
    bad = sum(1 for c in checks if c[3] != "MATCH")
    print("\n%d claims checked, %d differ." % (len(checks), bad))
