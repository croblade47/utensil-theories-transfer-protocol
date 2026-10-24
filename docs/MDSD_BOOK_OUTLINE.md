# MDSD — Book Outline

**Working title:** *Think Like an Attacker, Design Like a Storyteller*
**Alternate titles for A/B testing:**
- *Security for People Who Think in Stories*
- *The Metaphor Method: Designing Security Without a Security Degree*
- *The Attacker, the Door, and the Slippery Ground*

**Format:** ~130-page ebook, ready for Leanpub, Gumroad, Payhip, or Amazon KDP.

**Price points to test:** $29 introductory, $49 standard, $249 for a ten-seat team license.

**Audience:** Non-specialist decision-makers in small-to-medium systems. Founders, PMs, operators, clinicians, teachers, educators, administrators.

---

## Chapter structure (12 chapters, ~10 pages each)

### Part I — The problem

**1. Why security advice doesn't reach you**
Jargon as a gatekeeper. The three failure modes of standard security guidance (walled out, inert catalogs, abstract threat models). Why the people closest to a system are usually the first ones to see its attackers clearly.

**2. The insight: attackers live in stories**
Why vivid attackers produce stronger designs. The physical nouns test. Why security specialists accidentally train the vividness out of their own threat models over time.

### Part II — The method

**3. Step 1 — Tell the attacker's story**
How to write the paragraph. Second person. Specific details. The common mistakes. Five worked rewrites from "bad" to "good."

**4. Step 2 — Name the goal in one sentence**
Why "exfiltrate data" is weaker than "find out which cards still work." The attacker's voice. Testing your sentence against the paragraph.

**5. Step 3 — Describe the defense as a scene**
Doors, rooms, dialects, ground, mirrors. Why clever is wrong and boring is right. When to extend an existing metaphor and when to switch.

**6. Step 4 — Translate via the table**
The 18-row table. How to pick between adjacent rows. What to do when nothing matches. The "needs specialist review" marker as a feature.

**7. Step 5 — Walk the attacker through**
The four verdicts: blocked, slowed, painted, passed. Challenging your own walkthrough. The specialist's extra rows.

**8. Step 6 — Simulate, then specialist review**
When to simulate and when to skip it. The role of the specialist. How to receive a review without losing heart.

### Part III — The examples

**9. Six worked examples at full length**
Small shop vs. card testing. Clinic patient portal vs. records theft. Internal portal vs. phished credentials. Mobile app vs. API abuse. IoT device vs. botnet recruitment. SaaS admin vs. supply chain / insider. Each with the full story, scene, translation, walkthrough, honest limit, and simulation notes.

**10. Four more examples at compact length**
Public kiosk, payment terminal, school portal, personal email. Compressed to the pattern.

### Part IV — Beyond the first draft

**11. The specialist review — a chapter for both sides**
The protocol in prose. For non-specialists: how to find a reviewer, how to prepare the draft, how to read the reply. For reviewers who've been handed a draft: the five-phase protocol with the one-page template.

**12. What this framework can't do**
The honest limits chapter. Side channels, formal protocol flaws, hardware fault injection, regulatory landscape. Why these are off-ramps to specialists, not design failures. When your scene says "we need a cryptographer" the right answer is to find a cryptographer.

### Back matter

**Appendices:**
- A. Ten starter attacker stories (the full set, with specialization prompts)
- B. The translation table (standalone, printable)
- C. One-page MDSD worksheet
- D. One-page review-reply template
- E. Reading list: what to read next from established security literature
- F. Changelog and open invitation to extend the catalog

---

## Writing plan

- **Weeks 1–2:** Edit existing docs into Part I and Part II. Minimal new writing.
- **Weeks 3–4:** Write the "problem" and "insight" chapters (1–2). These are the only two chapters that need to be written mostly from scratch.
- **Weeks 5–6:** Expand six examples to full length (Chapter 9). Compress four (Chapter 10). Both of these pull heavily from the existing worked examples.
- **Week 7:** Write chapters 11 and 12 from the existing review protocol and limits sections.
- **Week 8:** Appendices, cover design, final edit, format for Leanpub/Gumroad, publish.

**Realistic effort:** 40–80 hours of focused writing on top of what's already in the repo.

---

## Cover and marketing

**Cover concept:** A simple visual. A door standing open on polished ground, slippery and bright, with a figure mid-slide. Red dye marking their footprint behind them. No security iconography (locks, shields, hooded figures) — the cover should look nothing like the fifty other security books on the shelf.

**Back cover copy (short):**

> You can describe how your system is going to get attacked. You can picture the attacker. You can draw the scene in your head. Nobody has given you a way to turn that picture into a real security design — until now.
>
> This book is a six-step method for designing layered defenses by telling stories about attackers and translating the stories into real security moves. It is written for people without security training, and it ends with a protocol for handing the draft to a specialist responsibly.
>
> Ten worked examples. An 18-row translation table from metaphor to real security primitive. A simulation harness. Honest limits in every chapter.
>
> If you have ever been in a security meeting where you felt stupid, this book is for you.

---

## Platform choice

- **Leanpub:** Royalties are high (~80%). Audience is technical. Pricing is flexible. Best for serial updates. Lowest friction to publish; harder to reach non-technical readers.
- **Gumroad:** Royalties high. Easier for non-technical audience discovery. Simple paywall. Good first platform.
- **Amazon KDP:** Largest audience. Lower royalty on cheaper prices. Required if you want to be in bookstores (physical print-on-demand possible). Best for the long-tail reader.

**Recommendation:** Launch on Gumroad first (one week to publish). Add Leanpub two weeks later (free, more reach into security audience). Add KDP in month two if sales support it.

---

## Launch sequence for the book

- **Pre-launch (2 weeks):** Build a landing page. Collect email addresses. Send one weekly update with a chapter excerpt. Pre-announce on LinkedIn and X.
- **Launch day:** Post to the email list first. Post Thread A on X. Post the LinkedIn launch. Post a Hacker News "Show HN" linking to the Gumroad page.
- **Week 1:** Reply to every comment. Collect three testimonials from early buyers. Add them to the landing page.
- **Week 4:** Raise price from $29 to $49 if sales support it. Announce the price change a week ahead to drive a buying spike.
- **Month 3:** Publish on Leanpub and KDP. Add the paperback.
- **Month 6:** Second edition with reader feedback incorporated. Price up again.

---

## Revenue projection (honest range)

| Scenario | Month 1 | Month 3 | Month 6 | Year 1 total |
|---|---|---|---|---|
| No promotion | 2 sales | 5 sales | 10 sales | $500–$1,000 |
| Modest promotion (HN, LinkedIn, X) | 50 sales | 100 sales | 200 sales | $5,000–$12,000 |
| Strong promotion (podcasts, newsletter mentions, co-author push) | 200 sales | 400 sales | 1,000 sales | $25,000–$60,000 |
| Viral or picked up by a major voice | 2,000 sales in a week | 5,000 total | 10,000 total | $150,000+ |

The viral case is improbable but not impossible. The strong case requires significant time investment in promotion through month three. The modest case requires one solid launch week. The no-promotion case is what happens if the ebook ships and sits.

---

## What to use the book revenue for

In order:

1. **Reinvest in production.** A proofreader and a cover designer each cost $200–$600. Both pay for themselves in reviews.
2. **Fund the first paid Facebook/LinkedIn/X ads** experiment. $200/month to test whether paid acquisition works for this audience.
3. **Pay a co-author or technical reviewer** for a cleaned-up edition. $500–$2,000 for a credentialed name on the cover is the single highest-leverage spend you can make.
4. **Save it** or spend it on anything you want. If the book is making $1,000/month and you want to keep running it as passive income, that is a complete and sufficient outcome.
