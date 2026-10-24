# MDSD Review Protocol

**For security specialists reviewing a Metaphor-Driven Security Design draft produced by a non-specialist.**

---

## What you've been handed

The author wrote one paragraph about an attacker in plain English, picked metaphors for the defense, used the translation table in `METAPHOR_SECURITY_FRAMEWORK.md` to turn each metaphor into a security primitive, and walked the attacker through the design on paper. They may have run a small simulation. They know they aren't you. They are asking you to find what they couldn't see.

This document is the protocol for that review. It is structured to produce a reply the author can actually use — one that respects their contribution, catches the holes, and leaves the next version better.

## The attitude

Three things to remember before you open the draft:

1. **The author is not your junior.** They are a domain expert in the thing being defended, which is a kind of expertise you probably don't have. Their draft is a client brief, not a homework assignment.
2. **The framework is designed to produce incomplete drafts.** Gaps are the expected output, not a failure. The gaps are where you earn your pay.
3. **Your review is primarily a translation back.** You take security findings and write them in the same plain-English register the author used. If your review is full of acronyms the author can't act on, you have failed the review, no matter how technically correct it was.

---

## The review in five phases

### Phase A — Read for the story (10 minutes)

Read Step 1 of the draft (the attacker's story) and Step 2 (the goal). Nothing else yet. Do not look at the translation choices.

Ask yourself:

1. **Can I picture this attacker?** If not, mark the story as insufficient and send it back for detail. Do not design against a cartoon.
2. **Does the goal match the story?** Authors often write a vivid attacker whose goal turns out to be smaller than what the story implied. Flag the mismatch.
3. **What would I add to this story?** Write down, before you look at the design, what *you* think the attacker would also do that the story doesn't mention. These are your candidate blind spots.
4. **Threat-model classification.** Internally, note the STRIDE / MITRE ATT&CK tactics you'd attach to this story. Do not put the acronyms in your review reply. Use them to drive your own search in later phases.

**Output of Phase A:** A short list of attacker moves the story leaves out, in the author's own register. Example: *"The story doesn't mention what happens if the attacker already works here."*

### Phase B — Review the translation table (15 minutes)

Open Step 4 of the draft. Go row by row.

For each row, ask:

1. **Is the metaphor an honest match for the primitive?** The translation table has rows that are close but not identical. "Hall of mirrors" and "shadow in the room" both involve deception but behave differently in incident response. Catch a wrong pick.
2. **Does the primitive deliver what the author pictured?** Primitives have operational realities the metaphor hides. A canary token "paints" an attacker in a specific technical way, but the author may have pictured it as instant notification; find the gap.
3. **Did the author pick the strongest-sounding row rather than the right one?** This is common. The row that sounds most impressive is rarely the right one.
4. **Did they omit a primitive the scene implied?** The scene often includes something the author didn't write a row for ("the lights get warmer" implies a feedback loop that needs rate limiting, not just logging).
5. **Did they include a primitive the scene didn't imply?** Occasionally authors add a row because they heard it was good. Flag primitives that don't appear in the scene; they are either an unstated design intent or dead code.

**Output of Phase B:** Line-by-line notes on each row — keep as-is / wrong primitive / needs addition / needs removal. Each note is one sentence the author can act on.

### Phase C — Attack the walkthrough (20 minutes)

Open Step 5. The author has walked their attacker through the design and labeled each row **blocked**, **slowed**, **painted**, or **passed**.

Your job:

1. **Challenge every "blocked" row.** Why can't the attacker try again from a different angle? What state does "blocked" leave in the system? Does the attacker learn anything from the block itself?
2. **Challenge every "slowed" row.** How much slower? Enough that a determined attacker gives up, or just enough to annoy them? Is "slower" measured, or asserted?
3. **Challenge every "painted" row.** Who sees the paint, and in what timeframe? If the paint is a signal to an on-call engineer who doesn't exist, the paint is not real.
4. **Add rows the author didn't.** Use your list from Phase A. Walk the attacker's unspoken moves through the design. Mark each with your verdict. The new rows are the real deliverable of this phase.
5. **Challenge the ordering.** Can the attacker reach row N without first passing rows 1 through N-1? If the walkthrough assumes a path and the system doesn't enforce that path, the walkthrough is fiction.

**Output of Phase C:** An expanded walkthrough — the author's rows plus yours, with your verdicts. Anything that comes out **passed** is a hole and gets flagged for Phase D.

### Phase D — Hunt for metaphor blind spots (15 minutes)

MDSD's known weakness is that attacks without clean physical metaphors are invisible to the author. This phase is your job alone. For the system under review, check the following categories by hand, regardless of what the author wrote:

- **Timing and side channels.** Does the design leak information through how long operations take, how much memory they use, how much power they draw? No metaphor in the standard table covers this.
- **Formal protocol flaws.** If the design uses crypto, authentication, or state machines, are the primitives being used in the way their standards actually require? A pre-shared cipher used wrong is worse than no cipher.
- **Boundary violations.** Where does untrusted input cross into trusted code? Injection categories (SQL, command, template, deserialization) rarely show up in metaphor-form.
- **Supply chain.** What does the design depend on — libraries, services, humans, printers, mail carriers? Each is a potential compromise path the metaphor erases.
- **Operational realities.** On-call rotations, alert fatigue, employee turnover, key rotation friction, patch cadence. These eat security designs that look fine on paper.
- **Compliance and legal.** Jurisdictional constraints on deception, logging, data handling, breach disclosure. The author almost certainly did not consider these.
- **Denial of service.** The design may defend confidentiality and integrity while being trivial to knock offline.
- **Insider cases.** The author may have scoped out insiders by assumption; check whether the design degrades gracefully if that assumption fails.

For each applicable category, write one plain-language note. Not "SQLi" — write *"If the attacker can type into any input box that eventually becomes part of a database query, they may be able to make the database do things you didn't intend. We should review every place user text ends up."*

**Output of Phase D:** A category-by-category list of blind spots, each with a plain-language explanation and a recommended next step.

### Phase E — Write the review reply (20 minutes)

The reply has four parts. In order:

1. **What's right.** Start by naming what the author got right. Be specific. "Your choice of airlock pattern for the compromised-credential case is appropriate — this is a real primitive and it does what you described." Vague praise is condescending; specific praise is useful. If very little is right, say "the story is clear and specific" and move on — do not invent praise.
2. **The expanded walkthrough.** Give them your Phase C output as the walkthrough they should use next, with your added rows and verdicts marked distinctly from theirs. This is the single most actionable deliverable.
3. **The blind-spot list.** Phase D output, in plain English, each with a suggested next step. Prioritize: critical / important / nice-to-have. The author decides which to address in revision versus which to accept with mitigations.
4. **A verdict.** One of five, no middle ground:
   - **Ready to simulate** — minor cleanups only; proceed to Step 6 of the author's process.
   - **Revise and resubmit** — specific holes to close; one more round with you.
   - **Needs broader review** — the system class is outside what MDSD alone can cover; bring in additional specialists (compliance, cryptographer, red team) and name who.
   - **Not viable as designed** — the fundamental scene has a flaw no amount of primitive-swapping fixes. Explain why in plain language. Suggest what a viable scene might look like.
   - **Needs re-scoped story** — the attacker story is too thin for a design to stand on. Return it with specific questions about the attacker.

**Output of Phase E:** The review reply. Delivered in the same register the author wrote in. No acronyms the author can't act on.

---

## Review timing

A thorough first review runs about 80 minutes for a one-page draft. A re-review (after revisions) runs about 30. Build this into your estimate when agreeing to the work.

If a review is taking you three hours, the draft needs re-scoping — stop and send Phase A back as "needs more attacker story" rather than finishing a Herculean review of a thin draft.

---

## Known review failure modes

### Failure mode 1 — Rewriting the design

If you find yourself rewriting the author's design in your head, stop. The point of the framework is to teach the author to design. Flag what's wrong, suggest a direction, and let them revise. A review that becomes a redesign is a review that trained no one.

### Failure mode 2 — Jargon leakage

If your reply uses an acronym without defining it in plain English, cut it. The author won't ask you to clarify — they will nod and nothing will change. Every uncovered acronym is a review finding that will not be acted on.

### Failure mode 3 — Scope creep

MDSD is a design framework, not an operations manual. If you find yourself writing about on-call rotation structure, incident response playbooks, or hiring plans in the review, that content belongs in a separate conversation. Flag it, don't fold it in.

### Failure mode 4 — Theatrical rigor

Finding ten minor issues when there are two critical ones is noise. Rank mercilessly. The author has limited bandwidth and will fix what you flag first; make sure the first things are the right things.

### Failure mode 5 — Over-caution

Not every design needs to withstand a nation-state actor. Match your review's rigor to the threat model the author wrote. A kiosk at a public library and a treasury system of record get different reviews. If the author's threat model is honest, respect it; if it's unrealistic, say so in Phase E as "the attacker you described is weaker than the one you'll actually face" and let them revise.

---

## Appendix A — Common blind spots catalog

A non-exhaustive list of things authors reliably miss, grouped by how they manifest in a draft. Use this during Phase D as a prompt list.

**Authentication and session**
- Session fixation; cookies that survive logout; concurrent-session rules.
- Password reset flows (often the weakest path to an account).
- Account recovery via mail or phone (defeats most 2FA designs).

**Input handling**
- Any place user text becomes part of a query, command, URL, template, or filename.
- File uploads (type validation, path traversal, storage location).
- Imported data (CSV formulas, deserialization).

**State and transitions**
- Race conditions between parallel requests.
- Partial failure (what if step 3 of 5 crashes mid-way).
- Idempotency (what if the same request arrives twice).

**Trust boundaries**
- Where does the attacker become "inside"? Does the design degrade from there?
- Where do systems trust each other that shouldn't? Shared caches, shared databases, shared users.

**Operational**
- Who gets alerted? When? Via what channel? What if they're asleep?
- Key rotation — who, how often, what breaks when they don't rotate.
- Logging — is anything logged that shouldn't be (passwords, tokens, PII)?
- Backups — can an attacker read a backup instead of the live system?

**Supply chain**
- Dependencies (packages, services, humans).
- Build systems and release pipelines.
- Third-party integrations and their failure modes.

**Side channels**
- Timing of yes/no answers (login enumeration, access-check enumeration).
- Error messages that reveal structure.
- Response sizes, header patterns, cache behavior.

**Denial of service**
- Any unbounded operation (regex, parse, resize, allocation).
- Resource exhaustion on behalf of attackers (expensive queries, retry storms).

**Compliance and legal**
- Data residency and cross-border flow.
- Breach notification requirements and timelines.
- Deception legality (varies widely).
- Logging and consent in regulated industries.

**Human factors**
- Social engineering of the people in the design, including help desk.
- Shoulder surfing, screen capture, physical access.
- Phishing-resistance of the chosen auth factors.

---

## Appendix B — The one-page review reply template

Give this to new reviewers as a scaffold. Copy, fill in, delete the hints.

```
MDSD REVIEW — [system name]
Author: [name]        Reviewer: [your name]        Date: [date]

VERDICT: [Ready to simulate / Revise and resubmit / Needs broader
          review / Not viable as designed / Needs re-scoped story]

WHAT'S RIGHT
[2-4 specific sentences. No vague praise.]

EXPANDED WALKTHROUGH
[The author's walkthrough, plus your added rows, each marked (R) so the
 author can see what came from the review. One line per row.]

BLIND SPOTS
Critical:
  1. [plain language description]
     Suggested next step: [what the author does]
  2. ...

Important:
  1. ...

Nice to have:
  1. ...

NEXT ROUND
[One short paragraph: what you need from the author next. If verdict
 is "Needs broader review," name the additional specialists.]
```

---

## Appendix C — When to decline the review

Decline, and say why in writing, if:

- The system is already in production and under active attack. The author needs incident response, not a design review. Help them find IR.
- The design is being presented as finished to a regulator, customer, or insurer and your review is sought as rubber-stamp cover. Decline, in writing, and explain that MDSD review is a design aid, not a certification.
- The author refuses to add detail to Phase A after being asked twice. The framework cannot defend against an attacker the author will not describe.
- You lack domain expertise in the thing being defended (not in security — in the business or system). Say so, name a reviewer who has it, and offer to pair.
- The design is outside the MDSD table's reach entirely (cryptographic protocol design, hardware root-of-trust, formal verification). Route to the right specialist directly.

Declining honestly is better than reviewing badly.

---

## Attribution

This protocol was drafted alongside the framework and the how-to guide. It is intended to be revised as reviewers accumulate experience. Section 8 of `METAPHOR_SECURITY_FRAMEWORK.md` reserves this document as living guidance.
