# How to Design a Security Defense Without Being a Security Engineer

**A plain-language guide to the Metaphor-Driven Security Design framework.**

---

## Who this is for

You have a system you care about. A website, an office, a clinic, a kiosk, a shop, an app, a workflow. You know in your gut that someone could try to break into it, misuse it, steal from it, or cause it to lie. You can picture the attacker in your head — maybe not every detail, but the shape of them. You know roughly what they'd want.

What you don't have is a security degree. You can't read the acronyms. You've looked at OWASP once and closed the tab. You've been told "we need to harden this" and had no idea what that meant in practice.

This guide is for you. It will walk you through designing a layered defense for your system by telling a story about the attacker and then translating that story into real security moves, one piece at a time. You will not need to learn jargon. At the end you will have a design on paper that a real security engineer can review and finish.

**It will not make you a security engineer.** It will make you a useful partner to one, and it will produce a design that is a lot stronger than nothing.

---

## What you'll need

- Half an hour of quiet time.
- A notebook or a text file.
- Honesty about what you don't know.
- Access to the framework doc (`METAPHOR_SECURITY_FRAMEWORK.md`) for the translation table in Step 4.

That's it.

---

## The six steps

### Step 1 — Tell the attacker's story

Write one paragraph. One. Keep it short. Describe the attacker as a person doing something physical. Use the word *you* for the attacker — it forces you to be specific.

Do not use any security words. No "exploit," no "vector," no "payload," no "privilege escalation." If you catch yourself reaching for one, replace it with what it actually looks like to a human.

**Example (bad):** *"An unauthenticated external threat actor attempts credential stuffing against the login endpoint to achieve lateral movement."*

**Example (good):** *"You're sitting in a coffee shop with a laptop and a list of usernames and passwords you bought online. You open our login page and try them one after another, fast. When one works, you log in and start poking around looking for anything to sell."*

The second version is better because you can see it. You can see the coffee shop, the laptop, the list, the speed. Each of those details becomes a design clue later.

### Step 2 — Name the goal in one sentence

What does the attacker want? Say it in their voice. One line.

**Bad:** *"Compromise system integrity."*

**Good:** *"I want a login that works so I can take whatever's inside."*

If you can't say it in one line, you don't understand the attacker well enough yet. Go back to Step 1 and add detail.

### Step 3 — Describe your defense as a scene

Now you get creative. Describe what the attacker runs into, as if it were a physical place. Doors, rooms, ropes, hallways, guards, ground, paint, mirrors, signs. Anything you can picture.

Keep going with the plain-English style. No technology names. No product names. You are the writer of a short, slightly weird story about the attacker's trip through your system.

**Example:** *"The front door opens for anyone, but inside is just a tiny room with no other exit visible. On the walls are signs in a dialect the person has to have memorized from a letter we mailed them. If they can't speak it, they try to guess, and every guess rings a quiet bell somewhere else in the building. The lights get warmer and warmer. They can't leave because the front door has already locked behind them. They don't know yet, but they are also covered in a kind of invisible dye that will show up under certain lights for weeks."*

If you can see the scene, you have enough to work with. If you can't, you're still writing in security words — restart.

### Step 4 — Translate your scene into real moves

Open the translation table in `METAPHOR_SECURITY_FRAMEWORK.md` (Section 3). For each physical thing in your scene, find the row that matches it. Each row tells you the real security move that behaves the way you described.

Make a two-column list:

| What I pictured | What that actually is |
|---|---|
| Front door opens for anyone | Non-blocking admission for unknown tokens |
| Tiny room with no exit | Mantrap / airlock pattern |
| Dialect from a mailed letter | Pre-shared cipher delivered out-of-band |
| Bell on every guess | Behavioral fingerprinting + rate limiting |
| Lights get warmer | Exponential backoff |
| Front door locks behind them | Atomic non-reversible transition |
| Invisible dye | Canary token / honey token |

If a piece of your scene doesn't have a row, don't invent one. Either simplify the scene until it does, or write down "needs specialist review" and move on. That's a feature, not a failure — it tells the engineer later which parts you need help on.

### Step 5 — Walk the attacker through it on paper

Take your attacker's story from Step 1 and your translated moves from Step 4. Walk the attacker through, one step at a time. At each step write one of four words:

- **Blocked** — they couldn't do it.
- **Slowed** — they could do it, but it cost them time or attempts.
- **Painted** — they did it, but we now know who they are and can find them later.
- **Passed** — they did it and we don't know, and they got something.

The design is good enough for a first draft when every step the attacker takes ends in **blocked**, **slowed**, or **painted**, and no step ends in **passed**. Any **passed** is a hole that needs another layer or a specialist's eyes.

**Example walkthrough:**

| Attacker step | Result |
|---|---|
| Walks up with stolen password | Front door opens — not blocked, as designed |
| Steps into tiny room | **Painted** (dye on entry), **Slowed** (now has to speak the dialect) |
| Tries to turn around and leave | **Blocked** (door locked behind them) |
| Guesses dialect | **Slowed** (backoff after each miss), **Painted** again (each guess logged with their fingerprint) |
| Keeps guessing | **Blocked** (vestibule freezes after N tries) |
| Attempts to signal outside for help | **Blocked** (no outbound anything from the vestibule) |

Every row is blocked, slowed, or painted. No row is passed. First draft looks okay.

### Step 6 — Simulate, then show it to a specialist

A design on paper is a draft. Before anything ships:

1. If you can code, or you know someone who can, build a small simulation like the two in the `sims/` folder. Have the simulation pretend to be each attacker you can imagine, and see what happens. Fix the holes.
2. **Then show it to a real security engineer.** The framework is a bridge, not a destination. The engineer's job is to find the attacks you couldn't picture — the ones with no clean metaphor, the ones that use timing or hardware tricks, the ones that only make sense if you've read the research.

Do not skip the specialist. The framework is designed to make their job easier, not to replace them.

---

## A full worked example from scratch

Let's do one together, start to finish. Say you run a small online store.

### Step 1 — Attacker's story

*"You bought a dump of credit card numbers for cheap. You've written a script that tries each one at our checkout, really fast, buying a $1 digital gift card each time. The ones that go through are live cards you can resell for a lot more. You don't care if 99% of them fail — the 1% that work pay for everything."*

### Step 2 — Goal in one sentence

*"I want to find out which of these card numbers still work."*

### Step 3 — Scene

*"When someone tries to buy a gift card, we only let them try one time per minute from the same device, no matter what card they use. If they try again fast, our checkout starts acting strange — maybe the page loads but no confirmation ever comes, maybe the price shows as something odd. Any card that fails more than three times in a row — any card, from anyone, anywhere — gets a mark that follows it. If a card with that mark later tries to make a real purchase from someone's real account, we quietly let it fail and flag the account. And we send a copy of every single attempt to a notebook that the owner of the card number can look at themselves."*

### Step 4 — Translation

| What I pictured | What that actually is |
|---|---|
| One try per minute per device | Rate limiting per device fingerprint |
| Checkout acting strange on retries | Tarpit / honeypot response |
| Mark that follows a failing card | Reputation signal on card primary account number |
| Letting marked cards quietly fail | Shadow decline / deception response |
| Notebook the real cardholder can see | User-facing fraud transparency / audit log |

### Step 5 — Walkthrough

| Attacker step | Result |
|---|---|
| Runs script against checkout | **Slowed** (one try per minute) |
| Switches device fingerprints with proxies | **Slowed** (per-card reputation still catches it after 3 fails on any device) |
| Finds a card that goes through | **Painted** (reputation mark follows the card, cardholder notified) |
| Tries to resell the card | **Blocked** (next buyer runs into the mark immediately) |
| Reports look clean to the attacker | **Painted** (shadow decline makes the attacker think it worked) |

No **passed** rows. First draft looks okay. Needs **simulation** and **specialist review** before anyone wires it into the real checkout.

### Step 6 — Hand it off

You take this to a developer and a payments expert. They tell you two things you didn't know: that the per-card reputation needs to be shared with the card network (which has its own fraud scoring already — you may be duplicating work), and that shadow decline has legal disclosure requirements in some jurisdictions. You update the design. You never had to learn what "card primary account number" meant to get here. You just told the story.

---

## When to stop and call a professional

Call a professional immediately — do not try to finish the design yourself — if any of these are true:

- The system touches **money, health records, or identity documents** at any scale beyond a hobby.
- The system is already in production and already being attacked.
- You can picture the attacker but you can't picture their next move, and you keep writing "and then somehow they…"
- Your scene has more than one place marked "needs specialist review."
- Someone is asking you to sign something that says the system is secure.
- You feel like you're over your head. You probably are. That's not a weakness; that's the whole reason this framework ends with "then show it to a specialist."

---

## Common mistakes

### Mistake 1 — Writing the attacker as a cartoon

**Bad:** *"A hacker in a hoodie types really fast and gets into our stuff."*

**Good:** *"You have a working email address of a real employee, a laptop, three hours, and a willingness to send fake meeting invites. You know we use a specific calendar tool because our job listings mention it."*

Real attackers are specific, patient, and have resources. A cartoon attacker produces a cartoon defense.

### Mistake 2 — Making the defense too clever

If your scene reads like a heist movie, something is wrong. Real security is boring. One door, one lock, one log. Boring works. Clever often introduces new ways to fail.

### Mistake 3 — Writing the defense before the attack

If you start with "we should add two-factor authentication," you've skipped Steps 1 through 3. You've named a product, not a scene. Go back and tell the story first. You might find out two-factor isn't the right answer, or isn't the whole answer.

### Mistake 4 — Treating paper as proof

A design that passes on paper has passed on paper. It has not been attacked. Someone capable will find holes you couldn't see. That is why Step 6 is simulate, then specialist. Both. Not one.

### Mistake 5 — Hiding your limits in the design

If a step in your walkthrough comes out as **passed**, do not reword it until it looks better. Write down "this is a hole" and bring it to the specialist. The honest draft is more valuable than the pretty one.

---

## A one-page worksheet

Copy this. Print it. Fill it in.

```
MDSD WORKSHEET

System I'm designing a defense for:
____________________________________________________________

Step 1 — Attacker's story (one paragraph, plain English, no jargon):
____________________________________________________________
____________________________________________________________
____________________________________________________________
____________________________________________________________

Step 2 — Attacker's goal in their own voice, one sentence:
____________________________________________________________

Step 3 — My defense as a physical scene:
____________________________________________________________
____________________________________________________________
____________________________________________________________

Step 4 — Translation table (fill in from METAPHOR_SECURITY_FRAMEWORK.md Section 3):
   What I pictured             |  What that actually is
   ______________________      |  ______________________
   ______________________      |  ______________________
   ______________________      |  ______________________
   ______________________      |  ______________________
   ______________________      |  ______________________

Step 5 — Walkthrough:
   Attacker step               |  Result (Blocked/Slowed/Painted/Passed)
   ______________________      |  ______________________
   ______________________      |  ______________________
   ______________________      |  ______________________
   ______________________      |  ______________________
   ______________________      |  ______________________

Any "Passed" rows? If yes, those are holes. Mark them.
____________________________________________________________

Step 6 — Hand-off:
   [ ] I've written a simulation OR I don't know how (specialist handles)
   [ ] I'm scheduling a review with a security engineer
   [ ] I've listed the parts I know I need help on

Specialist's name: _____________________    Date: _____________
```

---

## Frequently asked questions

**Do I really not need to learn any security vocabulary?**
Not for the design step. You'll pick some up by reading the translation table rows, and that's fine — but you don't need to know it in advance. If someone tells you otherwise, they're gatekeeping.

**What if my attacker's story matches more than one row in the translation table?**
Good. Write both down. The specialist will help you choose, or you'll end up with two layers instead of one, which is often correct.

**What if the translation table doesn't have what I need?**
Write down what you pictured in plain language, mark it "needs specialist review," and keep going. The gaps are useful data for the person who reviews your draft.

**How do I know if my design is "done"?**
A design is never done. A design is **ready for review** when every row in your walkthrough is blocked, slowed, or painted, and you've written down every place you're unsure. The specialist decides what "done" looks like after review.

**Can I use this for personal stuff, like my home network?**
Yes, and it's probably the single best starting point if you're worried about something specific. The whole thing scales down well. Keep the attacker story to one you actually fear and the scene to one you actually control.

**I'm a specialist and someone brought me a MDSD design. How should I review it?**
Treat it like a well-structured client brief, not a finished design. The attacker story tells you the threat model in their words. The walkthrough tells you what they thought their defense would do. Your job is to find the moves they couldn't picture, the attacks that don't fit the metaphor, and the translation-table rows they chose but shouldn't have. Review guidelines are future work in Section 8 of the framework doc.

---

## Credit where it's due

This framework exists because someone with no formal security background described an attack by comparing it to someone running at a door and slipping on ice. That image was accurate, useful, and would never have come out of a standard threat-modeling template. If you have images like that, this framework exists so your images don't get lost in translation.

Go design something.
