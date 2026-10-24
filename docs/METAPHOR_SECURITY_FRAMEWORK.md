# Metaphor-Driven Security Design (MDSD)

**A framework for turning narrative intuitions about defense into deployable security architectures.**

---

## Abstract

Security literature is dense with jargon that selects for people already trained in it. This excludes capable systems thinkers who reason naturally through analogy and story — people who can see the shape of an attack vividly in physical terms but cannot name its CVE class. Metaphor-Driven Security Design (MDSD) treats narrative as the primary design surface. The designer describes an attacker as a character and a defense as a physical scene, and the framework translates each metaphor into an established security primitive via a lookup table. The hypothesis: anyone who can tell a vivid story about an attacker can design a layered defense, given a disciplined translation step and an iterative test harness.

This document defines the framework, provides the translation table, and demonstrates three worked examples: the Slippery Door (external unknown-attack posture), the Pig-Latin Airlock (compromised-credential lateral-movement defense), and the LethalState progression (insider trust-root defense tested against CVE-2024-3094).

---

## 1. The problem

Security engineering has three common failure modes outside the specialist room:

1. **Jargon walls out contributors.** A product manager, a founder, a nurse running a clinical system, a librarian running a public kiosk — all have operational insight into the attackers they actually face, but cannot translate that insight into security vocabulary and are not taken seriously when they try.
2. **Pattern catalogs are inert.** OWASP, MITRE ATT&CK, MITRE D3FEND, and the NIST frameworks are comprehensive but entry-cost-high. They answer "what are the patterns?" but not "how do I compose them for my attacker?"
3. **Threat models are abstract.** STRIDE and PASTA are rigorous but strip away the narrative texture that makes a threat memorable and testable. A team that threat-models a system in STRIDE often cannot describe the attacker in a sentence afterwards.

MDSD responds to all three. It is a scaffold between vivid narrative and formal primitive, intended to be used by someone who is not primarily a security engineer, with the output reviewed by someone who is.

---

## 2. The framework

Six stages. Each is a single, concrete deliverable.

### Stage 1 — Tell the attacker's story

Write one paragraph in plain English. Who is the attacker? What do they want? How do they move? Avoid security vocabulary. Prefer physical nouns and verbs. Prefer the second person for the attacker (*"you approach the door, you carry a key you shouldn't have, you push through"*) because it forces specificity.

### Stage 2 — Name the goal in one sentence

The attacker's goal, in the attacker's own voice, in one line. *"I want to read what's in the vault."* Not *"exfiltrate PII."* The vocabulary of the goal determines which metaphors are honest.

### Stage 3 — Choose metaphors for the defense

Describe the defense as a scene. Doors, rooms, dialects, ground, mirrors, dye, ropes, shadows. Resist the urge to name technologies. If you cannot see the scene, you cannot test it.

### Stage 4 — Translate via the lookup table (Section 3)

For each metaphor you chose, consult the table. Each row maps a metaphor to one or more real security primitives. Pick the primitive that matches the behavior you described, not the one that sounds most impressive.

### Stage 5 — Compose and paper-test

Lay the primitives out as a flow. Walk the attacker's story through them step by step. At each step, write **blocked**, **slowed**, **painted**, or **passed**. A design is viable on paper if every step the attacker would take ends in **blocked**, **painted**, or **slowed**.

### Stage 6 — Simulate, then harden iteratively

Build a deterministic simulation (see `sims/` for templates). Run the attacker's story and variants. For each **passed** result, add one primitive and re-run. Stop when the fault return percentage is acceptable *for the threat model you wrote in Stage 1*. There is no universal threshold; a public kiosk and a central bank have different acceptable rates.

---

## 3. Translation table

Each row: metaphor → primitive → what it does → where it fails.

| Metaphor | Real primitive | What it does | Where it fails |
|---|---|---|---|
| Slippery ground | Tarpit / honeypot | Attacker expends time without gaining state | Attacker reads defensive literature and detects the pattern |
| Dye pack | Canary / honey token | Attacker is marked post-hoc | Marker is salt-dependent; salt leak defeats it |
| Airlock room | Mantrap / step-up auth with atomic transition | No backtrack between zones | Hostile insider inside the airlock |
| Door that closes behind you | Non-reversible session state | Attacker cannot retreat to probe | Session hijack to a session that already advanced |
| Secret dialect | Pre-shared cipher / challenge-response | Attacker inside cannot read or signal | Dialect compromise is total |
| Paper from the mail | Out-of-band key delivery | Compromise of online channel does not leak keys | Mail interception; social engineering of the mail step |
| Hall of mirrors | Polymorphic / dynamic surface | Each attempt sees a different system | Behavioral fingerprinting of the mirrors themselves |
| Rope that tightens | Exponential backoff / rate limiting | Progress asymptotes to zero | Distributed attack with many sources |
| Nail in the shoe | Behavioral fingerprinting | Attacker's own moves identify them | Low-and-slow attackers blend into noise |
| Watched spider | Reverse honeynet / deception | Attacker thinks they observe; is observed | Attacker performs no reconnaissance |
| Scepter | Capability token / signed grant | Explicit, auditable authorization | Scepter is held by the wrong hand |
| Co-sealer | m-of-n quorum signing | No single compromise is enough | n-way collusion |
| Trust that fades | Half-life / re-attestation | Old trust cannot pay for new access | Attestation theater — rubber-stamp renewals |
| Reproducible mold | Reproducible builds | Any build divergence is a flag | Compromise of the mold itself |
| Shadow in the room | Decoy / shadow surface | Attacker's writes land in `/dev/null` | Attacker distinguishes shadow from real |
| Vestibule | Network segmentation / microsegmentation | Lateral movement is bounded | Flat networks inside a segment |
| Receipt with no copy | Append-only ledger | Tampering is detectable | Ledger root compromise |
| The groundskeeper | SOC / human monitoring | Catches what rules miss | Groundskeeper burnout; alert fatigue |

The table is incomplete by design. Section 8 proposes it be grown as a community catalog.

---

## 4. Worked example 1 — Slippery Door (external unknown attack)

**Story:** You walk up to the front door of a building. You have never been here before, and you carry no invitation anyone has record of. You push on the door. It swings open freely. The floor inside is polished glass and you are already moving fast; you cannot stop. You slide through hallways. You see rooms with ledgers on tables. You reach for one. Your hand passes through — it was never real, only a careful painting. You keep sliding. You come out the front door with nothing. You are also covered in bright red paint that will not wash off, and the people who own the building have your fingerprints.

**Goal (attacker voice):** *"I want to steal what's inside before anyone knows I'm here."*

**Scene:** Open front door → polished floor (no dwell possible) → painted mirror rooms → closed loop back to entry → dye-pack on exit.

**Translation:**
| Scene element | Primitive |
|---|---|
| Open front door | Non-blocking admission for unknown tokens |
| Polished floor | Acceleration / forced transit speed |
| Painted mirror rooms | Shadow surface, writes to `/dev/null` |
| Loop back to entry | Non-exfiltration routing |
| Dye-pack | SHA-256 behavioral marker, salt-sealed |

**Validation:** `sims/slippery_door_sim.py` — 8 of 9 attack shapes handled, 100% paint coverage, 88.9% viability. Fails on insider-with-trust (Example 3 handles that).

---

## 5. Worked example 2 — Pig-Latin Airlock (compromised credentials, lateral movement)

### Story

You stole an employee's badge. You walk up to the front door. The badge opens it. You step inside. You are in a small room, not a hallway — just a vestibule. There is a second door in front of you. The badge does nothing to it. On the wall are signs, but the signs are written in a dialect you have never seen. The words look familiar but every ending is wrong, every vowel is shifted. You cannot tell which sign is "exit," which is "continue," which is "stop." Behind you, the first door locks. You hear it. You try to turn around — it will not open from this side.

A real employee would have memorized this dialect from a paper card mailed to their home address three months ago. They would speak the right phrase, the second door would open, and the lock behind them would release just long enough for them to pass. You do not know the phrase. You guess. The room grows warmer. You guess again. The lights change color. You keep guessing. Every guess is logged. Every move is painted. You will not leave this room until the people who own the building let you.

### Goal (attacker voice)

*"I have a working badge. I want to move laterally and reach the data."*

### Scene

Vestibule between every two rooms → front door opens for the badge → inner doors open only for a dialect the badge cannot carry → outer door locks when inner is approached → dialect is delivered by paper mail, not stored in any online system → each badge opens the vestibule but not the inner door → attacker trapped on wrong phrase → painted → telemetry captured.

### Translation

| Scene element | Primitive |
|---|---|
| Badge opens front door | Possession-factor authentication (what you have) |
| Dialect on signs | Knowledge-factor authentication (what you know) via pre-shared cipher |
| Paper card from the mail | Out-of-band key delivery (initial trust bootstrap) |
| Dialect varies per employee | Per-principal key material (no shared secret across the fleet) |
| Dialect rotates | Periodic re-attestation / key rotation |
| Vestibule | Mantrap / airlock pattern |
| Outer door locks before inner opens | Atomic non-reversible transition |
| Attacker cannot leave | Egress gated on same factor as ingress |
| Signs look like familiar text | Steganographic challenge (attacker cannot distinguish real content from challenge) |
| Guessing logged | Behavioral fingerprinting + rate limiting with exponential backoff |
| Painted on entry | Canary token, bound to badge + vestibule event |

### Composition

```
Phase 1 — Front door
  Input:  badge
  Check:  possession
  Open:   vestibule

Phase 2 — Vestibule (airlock)
  Lock:   front door closes atomically
  Prompt: steganographic challenge in principal-specific dialect
  Timer:  session clock starts
  Paint:  SHA-256 marker bound to (badge_id, event_hash, dialect_variant)

Phase 3 — Inner door
  Input:  dialect response
  Check:  knowledge, matched against principal's current card
  On success: inner door opens; vestibule → room; vestibule relocks
  On failure after N attempts: vestibule state frozen; telemetry escalated;
                               principal's card marked compromised;
                               next card issuance scheduled

Egress: identical sequence in reverse. No shortcut exits.
```

### Why it stops the attacker in the story

- The badge, by itself, buys them only the vestibule — a room with no onward exit.
- The dialect cannot be guessed in bounded tries; attempts are logged and the vestibule is gated by exponential backoff.
- The dialect was never on any computer the attacker could have compromised — it arrived by paper.
- Each principal has a different variant; stealing one card does not help in another vestibule.
- The attacker is painted the moment they enter the vestibule, before they fail.
- They cannot retreat, which denies them the chance to probe for a different weakness.

### Honest limits

- **Operational burden.** Mailing paper cards is expensive, slow, and error-prone. Lost cards strand real employees. Address changes create a race condition.
- **Phishing shifts, does not vanish.** An attacker who phishes an employee for the current phrase gets through until rotation. The design does not stop phishing — it reduces its blast radius and gives rotation teeth.
- **Legitimate user friction is real.** Users will complain. Some will write the phrase on a sticky note on their monitor, which is the entire failure mode this design is meant to prevent. The paper card itself is the authorized note; a second note is a leak.
- **Compromise of the card issuer is catastrophic.** The third-party card printer and mailer is a single point of total failure. It must itself be defended with Example 3's quorum pattern or stronger.
- **The dialect must be humanly usable.** If employees cannot learn their variant in reasonable time, they will not. Simplicity of the dialect bounds the design.
- **No defense against a compromised endpoint.** If the attacker is reading from the user's screen in real time (RAT, shoulder surf, compromised keyboard), the dialect is observable in use.
- **Legal considerations.** Steganographic challenges that masquerade as ordinary signage may violate consent-to-monitor expectations in some jurisdictions. Policy review required.

### Validation

See `sims/pig_latin_airlock_sim.py` for the deterministic simulation. Summary:

| Attacker profile | Result |
|---|---|
| Badge only, no dialect | Trapped in vestibule, painted |
| Badge + guessed single phrase | Trapped at next vestibule (per-principal variant) |
| Badge + full card from the same principal | Through (expected: requires physical theft) |
| Badge + full card from a different principal | Trapped at second vestibule (variant mismatch) |
| Badge + phished current phrase, dialect rotated since | Trapped at next vestibule |
| Badge + endpoint compromise (user mid-session) | Through (acknowledged limit) |

---

## 6. Worked example 3 — LethalState progression (insider threat, CVE-2024-3094 class)

See `docs/LETHALSTATE_PROTOCOL_NOTES.md` for the full progression. In MDSD terms:

**Story:** A trusted staff member of several years begins to make small changes to the building's rules. Each change is reasonable. Over time the changes accumulate until the rules themselves no longer deny what they used to deny. One day a stranger walks in holding the exact key the modified rules now accept, and no alarm fires.

**Goal (attacker voice):** *"I will become the authority that writes the rules, and then write a rule that lets me in."*

**Translation:** co-sealer, trust that fades, reproducible mold, scepter attested by quorum.

**Result:** four hardening loops reduce paper fault return rate from 87.5% to 0.0%. Full details in the notes file.

---

## 7. Honest limits of the framework itself

MDSD is a scaffolding, not a substitute. Specifically:

- **Paper viability is not security.** A paper-clean design can be shredded by a competent red team. Simulate, then test adversarially, then deploy to production in stages.
- **Translation ambiguity.** A single metaphor can honestly translate to several primitives, and the wrong choice produces an impressive-looking but inert design. The lookup table is a conversation starter with a specialist, not a self-service checkout.
- **Catalog gaps.** Many real-world attacks have no clean metaphor (side channels, timing attacks, hardware fault injection, formal protocol flaws). MDSD cannot design against what it cannot picture.
- **Social dynamics unaddressed.** The framework says nothing about how to run a security team, write policy, do IR, or build a culture. It is a design aid, not an operations manual.
- **Review is mandatory.** No MDSD output ships without specialist review. The framework widens the funnel of contributors; it does not replace the specialist at the end.

---

## 8. Future work

- **Catalog expansion.** The translation table (Section 3) should grow as a community wiki. Each row would carry one case study and one failure case.
- **Simulation DSL.** The `sims/` harness is Python today. A small DSL — "GIVEN an attacker who holds X, WHEN they attempt Y, THEN the system should Z" — would let non-programmers write their own tests.
- **Review protocol.** A checklist for the specialist reviewer: which translations deserve scrutiny, which combinations commonly fail, which simulation gaps are typical.
- **Educational curriculum.** The three worked examples here could become the first three lessons in a short course aimed at people who have operational insight but not formal training.
- **Red-team integration.** MDSD designs should enter a formal red-team cycle before production. The framework should define what that handoff looks like.

---

## 9. Attribution and license

This document was drafted collaboratively. It stands on prior art including MITRE ATT&CK, MITRE D3FEND, MITRE Engage, OWASP, honeypot and canary token literature (notably Thinkst's work), the mantrap/vestibule pattern as used in physical security, and the mountain of research on multi-factor and out-of-band authentication. MDSD claims no new primitive; its contribution, if any, is in the shape of the funnel.

License: inherited from the repository.
