# Metaphor-Driven Security Design — Start Here

A framework and a small set of documents for designing layered defenses by telling stories about attackers and translating those stories into real security moves.

**Who should read this page:** anyone opening the MDSD docs for the first time. It will take you one minute to figure out where to go next.

---

## The one-sentence pitch

If you can describe an attacker vividly in plain English, you can design a layered defense — provided you have a translation table from metaphor into security primitive and a specialist to review the result.

---

## Pick your starting point

### I'm a non-specialist. I have a system I want to defend.

Read in this order:

1. **`MDSD_HOW_TO_GUIDE.md`** — a plain-language, six-step walkthrough. Includes a full worked example and a printable worksheet.
2. **`MDSD_ATTACKER_STORY_STARTERS.md`** — ten pre-written attacker paragraphs you can adapt. Save you from staring at a blank page in Step 1.
3. **`METAPHOR_SECURITY_FRAMEWORK.md`** (just Section 3) — the translation table. You'll need it in Step 4.
4. **`MDSD_RECEIVING_A_REVIEW.md`** — one page on what to expect after a specialist reads your draft.

Skip the rest until a reviewer refers you to it.

### I'm a security specialist. Someone handed me a MDSD draft.

Read in this order:

1. **`MDSD_REVIEW_PROTOCOL.md`** — a five-phase protocol for reviewing a non-specialist draft. Includes a blind-spot catalog and a one-page reply template.
2. **`METAPHOR_SECURITY_FRAMEWORK.md`** — the full framework the author used. Section 3's translation table and Section 7's limits are the parts you'll reach for most.

The how-to guide is background; skim it to see how the author was taught to think.

### I'm thinking about the framework itself. I want to critique or extend it.

Read in this order:

1. **`METAPHOR_SECURITY_FRAMEWORK.md`** — the full research write-up, including abstract, limits, future work.
2. **`LETHALSTATE_PROTOCOL_NOTES.md`** — the original transcript that led to the framework. Historical, but useful for seeing where it came from.
3. The two simulations in `../sims/`.

---

## What each document is for

| Document | Audience | Length | Purpose |
|---|---|---|---|
| `MDSD_INDEX.md` (this file) | Everyone | 1 page | Pick your path |
| `MDSD_HOW_TO_GUIDE.md` | Non-specialists | Medium | Teach the six-step process |
| `MDSD_ATTACKER_STORY_STARTERS.md` | Non-specialists | Medium | Ten starter paragraphs to adapt |
| `MDSD_WORKED_EXAMPLES.md` | Non-specialists | Medium | Each of the ten starters carried through scene, translation, and walkthrough |
| `METAPHOR_SECURITY_FRAMEWORK.md` | Everyone | Long | Full framework, translation table, worked examples |
| `MDSD_REVIEW_PROTOCOL.md` | Specialists | Medium | How to review a draft |
| `MDSD_RECEIVING_A_REVIEW.md` | Non-specialists | 1 page | How to read a review back |
| `LETHALSTATE_PROTOCOL_NOTES.md` | Historians | Medium | Where the framework came from |

---

## What's in `../sims/`

- `slippery_door_sim.py` — simulation of the "open the doors and accelerate the attacker through a shadow surface" posture. Nine attack shapes, deterministic, no network.
- `pig_latin_airlock_sim.py` — simulation of the mantrap + per-principal cipher pattern (badge is possession factor, dialect is knowledge factor, delivered out-of-band on paper). Eight profiles, deterministic.

Both are templates you can copy for your own design.

```
python3 -I sims/slippery_door_sim.py
python3 -I sims/pig_latin_airlock_sim.py
```

---

## What this framework is not

- **Not a certification.** No MDSD document attests that any system is secure.
- **Not an operations manual.** Says nothing about on-call, incident response, hiring, or policy.
- **Not comprehensive.** Attacks without clean physical metaphors (timing, side channels, formal protocol flaws, hardware fault injection, parts of the compliance landscape) are intentionally outside the framework's reach — see Section 7 of the framework doc.
- **Not a substitute for a specialist.** The framework widens the funnel of contributors; the specialist review at the end is mandatory.

---

## The short history

A conversation starting from a notation for a story in a 2,500-year-old book, iterated through a bug fix, a test against a real-world 2024 supply-chain attack, four hardening rounds, a defense posture for unknown attacks, a simulation harness, and finally an abstraction into the framework and these documents. The whole trail is in the repo's commit history.

Nothing here is a new security primitive. The contribution — if any — is the shape of the funnel from narrative to primitive, and the discipline of making that funnel explicit, reviewable, and useful to people who were previously shut out of the design room by jargon.

---

## License and attribution

Inherited from the repository.

Drafted collaboratively. Open to revision as more drafts, reviews, and simulations accumulate.
