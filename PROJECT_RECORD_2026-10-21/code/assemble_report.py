"""Assemble the project record from the five section drafts, in section order, with a title page, contents,
the one-page short version and the events after the drafts were written.

Usage: python assemble_report.py <sections folder> <output .md>
"""
import re
import sys
from pathlib import Path

FRONT = """# Project Record: Utensil Theories Transfer Protocol

**Increasing an AI's comprehension to improve communication - a full record, 17 to 21 October 2026**

Prepared for the project owner, 21 October 2026.

**How to read this:**
- Start with section 1, the short version (one page).
- Section 3 is the full timeline, day by day: every request, what was done, and what changed.
- Section 12 explains every technical term in plain words.

## Contents

1. The short version
2. The goal, and how it was sharpened
3. Timeline, beginning to end
4. The owner's ideas, in their own words, and what was built from each
5. Every experiment (part A: the first script and experiments 1 to 11; part B: the seed test, the graph method, the greenhouse ladder, the numbers test)
6. Changes, adaptations, mistakes and corrections
7. The comprehension test across AIs
8. What already exists in research, and where the owner's credit could come from
9. Where things stand now, and what comes next
10. Every file and where it lives
11. How to reproduce the work
12. Plain-language glossary
13. Things outside the AI's control

## 1. The short version

**The goal,** in the owner's words: "Increase an LLM's ability to 'Comprehend' and 'Understand' in a way that improves communication." The Bible, fables and moral stories were training material, not the goal.

**How it was tested.** Tiny language models (about 3.4 million numbers each, trained from scratch on the King James Bible on a 4-core cloud computer) were scored on stories and verses they had never seen. Each test had controls. Where possible, the pass/fail rules were written down before any result was seen.

**Strong and repeated:**
- **Marking right and wrong in the training text helps.** A tiny model then judges new stories better: about 69 right per 100, against about 50 with no marking (experiments 8 and 10). This was a side measure, not the pre-registered main one.
- **Understanding shrinks the exact seed** (experiment 12). The tiny Bible model regrew 623 verses it had never seen (83,757 characters) byte for byte from a 12.2 KB seed: 85.4% smaller, and less than half of what xz needs. Each rung of shared understanding gave a smaller seed. The principle is already published (Shannon, 1951 onward). The measurement here is the project's own.

**Supported once:** the owner's carried balance (the shifting word) beat a plain good/bad label only in long stories, where the act had scrolled out of the model's view. That was about 59 vs 53 right per 100 (p = 0.004), in a re-run after two fixes, with about 65 of 100 pairs tied.

**Not confirmed:**
- predicting consequences (chance every time);
- Aesop morals carrying across cultures (no training set beat chance);
- the shifting word making seeds smaller (they came out about 2% larger);
- the shifting word beating the plain label in short stories (a tie).

**The seed and graph method** regrows any file exactly.
- It shrinks patterns (99.99%), but not ordinary text (6-19%, where zip manages 70%) or random data (0%).
- The owner's reported 98.9% is most likely explained by a shared library: naming an item already on the shelf. With the Bible on the shelf this measured 98.6%.

**Running now:** the first test of the owner's own recharge rule, "W1 = 17 + 4 Remaining", with the owner's numbers 17, 32, 16, 34 and 47.
- 18 tiny models are being trained.
- The test passed an independent review and two dry runs.
- The full run started at 17:45 UTC on 21 October and takes about 4 to 5 hours. No results yet.

**Queued (owner-approved):**
- the "2" test: numbers the model can read;
- then the +/- agent, with the owner's scoring rule: many small negatives, fewer but larger positives, every input pulling a little negative, and the two sides balancing.

**The honest limit.** Everything here comes from tiny models. None of it changes how a large AI understands anyone. The next real step needs outside help: more computing power, a large-model API key, or a fresh expert reading.

"""

TIMELINE_ADD = """
### 21 October 2026, later (added after this timeline was drafted)

- **02:21 #60** - The owner suggested emailing some people a link and inviting them to the repository.
  - The AI explained that the repository is already public, so a link is enough. Collaborator invites (which let people edit) are made by the owner in GitHub settings.
  - It offered to write a Gmail draft for the owner to send once recipients are named. None have been named yet.
- **02:22 #61** - The owner observed that the branch's diff has stayed large and similar while progress has slowed: "We need other people, someone else to know."
  - The AI measured the branch: +156,235 lines against `main`, 141,791 of them on 20 October, mostly copies of data files (the Bible text and one results file, each stored twice). Line counts are not progress.
  - It agreed the real limit is scale (tiny models on 4 CPU cores). It proposed outside help: computing power, a large-model API key and a fresh critical reading. It offered a one-page summary for newcomers and an outreach draft.
- **Early 21 October** - The session hit its usage limit (reset 06:30 UTC). It stopped this report and the numbers-test review part-way.
- **13:07 #62** - The owner shared another AI's Python blueprint, "ComprehensionSeed": a living memory of concept weights that are added to and subtracted from, with human errors treated as signal and a look beneath the literal words.
  - The AI's reading: it is an outline, and the seven functions that would do the hard part are undefined. It matches the owner's thesis and the planned +/- agent.
  - It has three flaws the experiments already showed: weights never fade; contradictions are only checked for new concepts; nothing is ever removed.
  - One framework name in it contains a person's full name, which is kept out of this public record.
- **13:12 #63** - The owner gave the scoring rule for the +/- agent:
  - **Positive:** moral high ground, telling the truth, highly reasonable information.
  - **Negative:** questionable morals, nonsense, misspelling.
  - "Should always pull a negative." More negatives than positives, but the positives are larger, and it balances.
  - It is recorded in `HANDOFF.md` (`a8a0cd7`). The AI measured today's word values as symmetric (36.0% vs 37.4%; average sizes 2.31 vs 2.27).
  - The size of a positive against a negative is still the owner's to choose.
- **13:10 to 13:30** - The review and this report resumed, then hit the usage limit again (reset 17:00 UTC).
- **17:37 to 17:45** - The AI did the remaining run-safety checks itself and applied 10 small fixes that leave the frozen design unchanged. A second dry run passed. **The full 18-model run started at 17:45 UTC** (`55f6817`).

**Updated totals:** 63 owner messages; 4 usage-limit stops (2 on 20 October, 2 on 21 October).
"""

NUMBERS_UPDATE = """**Update, 21 October, 17:45 UTC:** the review finished.
- Three of four reviewers said "ready", with no blocking problems and 12 minor notes.
- The run-safety checks were done directly after the fourth reviewer was cut off twice by the usage limit.
- Ten small fixes leave the frozen design unchanged. Among them, the inputs are now pinned: the run refuses to start if the word values or any of the six markings differ from the verified versions.
- A second dry run passed, and **the full run started at 17:45 UTC.**
- Every finding is in `NUMBERS_TEST_2026-10-21/review/review_findings_and_fixes.md`.

"""


def chunks(text):
    parts = re.split(r"(?m)^(?=## )", text)
    return [p for p in parts if p.startswith("## ")]


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    secs = {}
    for f in sorted(src.glob("*.md")):
        for ch in chunks(f.read_text(encoding="utf-8")):
            m = re.match(r"## (\d+)\.", ch)
            key = m.group(1)
            if key == "5":
                key = "5A" if "part A" in ch.splitlines()[0] else "5B"
            secs[key] = ch.rstrip() + "\n\n"
    order = ["2", "3", "4", "5A", "5B", "6", "7", "8", "9", "10", "11", "12", "13"]
    missing = [k for k in order if k not in secs]
    assert not missing, f"missing sections: {missing}"
    secs["3"] = secs["3"].rstrip() + "\n" + TIMELINE_ADD + "\n"
    secs["9"] = secs["9"].replace("### 9.2 The numbers test right now\n",
                                  "### 9.2 The numbers test right now\n\n" + NUMBERS_UPDATE, 1)
    secs["5B"] = re.sub(r"(?m)^- \*\*Review running:\*\*.*$",
                        "- **Review passed (21 Oct):** three of four reviewers said \"ready\" with no blocking problems; "
                        "the run-safety checks were done directly; ten small fixes left the frozen design unchanged; "
                        "a second dry run passed; the full run started at 17:45 UTC.", secs["5B"])
    text = FRONT + "".join(secs[k] for k in order)
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out}: {len(text):,} characters")


if __name__ == "__main__":
    main()
