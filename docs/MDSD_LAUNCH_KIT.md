# MDSD Launch Kit

**The commercial playbook: positioning, pricing, launch copy, outreach templates, and a 90-day plan to turn the Metaphor-Driven Security Design framework into revenue and reputation.**

---

## 1. Positioning

**One-line pitch:**
> *The security design framework for people who think in stories.*

**Elevator pitch (30 seconds):**
> Most security guidance is written for people who already speak security. That shuts out most of the people who actually run the systems being attacked — founders, product managers, clinicians, teachers, operators. MDSD flips the funnel: describe your attacker as a character and your defense as a physical scene, and the framework translates each metaphor into a real security primitive, with a specialist review protocol so the drafts can be finished responsibly. The whole method, the translation table, two simulations, ten worked examples, and the review playbook are open and on GitHub.

**Who it's for:**

- Startup founders and solo operators who can't afford a CISO.
- Product and operations leaders in regulated industries (health, finance, education).
- Security professionals who need a way to collaborate with non-specialist stakeholders.
- Bootcamps, incubators, and training programs that want an accessible security module.

**Why it exists:**

Because every month there is another breach that could have been prevented if the people closest to the system had been able to describe the attacker clearly. Jargon walls that conversation out. MDSD opens it back up without pretending that doing so replaces specialist review.

**What makes it credible:**

- Tested against a real-world 2024 supply-chain attack (CVE-2024-3094) in the public write-up.
- Two deterministic simulations with recorded results.
- Honest limits section in every document.
- The whole method is open; the paid parts are time, review, teaching, and curation.

---

## 2. Three paid offers

Priced for the realistic market, not the aspirational one. Raise prices after each successful engagement.

### Offer 1 — The Guide (self-serve)

**Format:** A polished PDF/ebook version of the doc set — the index, how-to guide, framework, worked examples, review protocol, receiving-a-review, and starter templates — plus a one-page printable worksheet. Delivered via Gumroad, Leanpub, Payhip, or similar.

**Price:** $29 (introductory). Raise to $49 after 100 sales or 90 days, whichever first. Enterprise bundle (10-seat site license) at $249.

**Target buyers:** Individuals, students, small-team leads.

**Why this price:** Below the price friction point most people pay without approval, which maximizes volume for the early reputation phase. The ebook is a lead generator for Offers 2 and 3; most of the money is downstream.

**Realistic revenue year one:** $0–$3,000 depending entirely on promotion.

**What to ship:** The existing docs, edited for consistency and formatted properly. Add one new chapter: "What to do when the specialist isn't available." See `MDSD_BOOK_OUTLINE.md` for the structure.

### Offer 2 — Design review service

**Format:** A written MDSD review of someone's design, following the review protocol. Delivered as a PDF reply within five business days.

**Price:** $500 for the first ten engagements (case-study phase). $1,500 after. $5,000 for engagements with a public case study and testimonial.

**Target buyers:** Pre-launch SaaS startups, non-profits with donor-sensitive data, small clinics, local government, bootstrapped tech companies.

**Why this price:** $500 is below most consulting friction thresholds. $1,500 matches the market for a junior security consulting day. Named case studies are worth more because they feed Offer 3.

**Realistic revenue year one:** $2,000–$15,000 if actively prospected.

**What to ship:** A review template (section headings), an intake form (short — what's the system, what's the attacker, what's your scene), and a scheduling link. Keep delivery to five business days to maintain cash flow.

### Offer 3 — Workshop and training

**Format:** A two-hour live workshop. Walks the group through an MDSD draft of a system they bring. Private Slack/Discord channel for 30 days after.

**Price:** First three workshops free in exchange for a public testimonial and permission to use the company name. After that: $1,500 for a startup/non-profit, $3,000 for a mid-sized company, $7,500 for an enterprise half-day with custom content. Multi-session series at a 20% discount.

**Target buyers:** Startup accelerators and incubators, bootcamps, product teams at mid-sized companies, non-profits.

**Why this price:** Workshops at this format and length run $1k–$5k in the current market for unknown trainers. Known trainers charge $5k–$20k/day. You start at the low end and raise as you accumulate testimonials.

**Realistic revenue year one:** $0–$15,000 side income (3–5 paid workshops after 3 free). Year two with momentum: $20k–$80k.

**What to ship:** Slide deck (16–24 slides), one worked example done live, pre-workshop intake form, post-workshop homework (fill in the worksheet for your own system), 30-day Slack/Discord channel.

### Offer 4 (contingent) — Enterprise license and co-authored engagement

**Format:** Custom. Internal training rolled out across a company, often with a security engineering co-author or endorser.

**Price:** $15,000–$60,000 per engagement.

**Prerequisite:** Credentialed co-author or endorser. Do not pitch this without one; large companies will not buy "accessible security" from an unknown name.

**Target buyers:** Mid-market and enterprise companies with distributed engineering teams, especially post-incident.

**Realistic revenue year two or later:** $30,000–$150,000/year if the co-author path works out.

---

## 3. Launch copy

### Hacker News launch post

**Title:** *Show HN: A security design framework for people who don't speak security*

**Body:**
```
I'm not a security engineer. I'm a [your role]. A few weeks ago I was
trying to describe to a developer how I thought our system was going to
get attacked. I used a metaphor — someone running at a locked door and
slipping on ice on the other side.

The developer didn't laugh. They said that was actually a security
pattern (honeypot + tarpit) and asked me to describe more.

That conversation turned into a framework for designing layered defenses
by describing attackers as characters and defenses as physical scenes,
then translating each metaphor into an established security primitive
via a lookup table. There is a specialist review protocol so the drafts
can be finished responsibly.

The whole thing is open on GitHub, including:
- A 6-step how-to guide for non-specialists
- An 18-row metaphor → primitive translation table
- Ten starter attacker stories (shop, clinic, kiosk, mobile app,
  internal portal, PoS, school portal, IoT device, SaaS admin, personal
  email) with full worked examples
- Two deterministic simulations (one against the CVE-2024-3094 class)
- A specialist review protocol with a blind-spot catalog
- Honest limits in every doc

I'm looking for feedback from both non-specialists (does the how-to
guide actually work for you?) and specialists (what's missing from the
review protocol? what did I get wrong in the translation table?).

Repo: [link]
Start-here index: [link to MDSD_INDEX.md]
```

**Posting tips:** Tuesday or Wednesday morning Pacific. Don't title-stuff. Reply to every comment in the first four hours. If it dies on `/new`, don't repost — try `/r/netsec` and `/r/cybersecurity` and LinkedIn instead.

### LinkedIn launch post

```
Most security advice assumes you already speak security.

That excludes most of the people who actually run the systems being
attacked — founders, operators, PMs, clinicians, teachers. People who
can describe an attacker vividly in physical terms but can't translate
that into security vocabulary.

I spent the last few weeks building a framework that bridges the two.
You describe your attacker as a character and your defense as a
physical scene. The framework translates each metaphor into a real
security primitive via a lookup table. A specialist reviews the draft
with a protocol designed for that specific handoff.

It's called Metaphor-Driven Security Design. It is not a replacement
for a security engineer. It is a way to produce a draft that a security
engineer can actually improve, instead of one they have to redo from
scratch.

The whole thing is open — the six-step guide, an 18-row translation
table, ten worked examples across common system types (small shop to
IoT to SaaS admin), two deterministic simulations, the review protocol,
and the honest limits.

If you've ever been in a room where the security conversation went
over your head, this is the framework I wish I'd had.

Link in comments. Feedback welcome from both sides of the wall.

#security #startups #appsec
```

**Posting tips:** Thursday morning. Put the link in the first comment, not the post itself (LinkedIn's algorithm suppresses posts with external links in the body). Tag two or three people whose feedback you actually want.

### Twitter / X thread (three variations)

**Thread A — the "I'm not a security engineer" angle:**

```
1/ I'm not a security engineer. But I built a security framework. Here's
   why that's not actually ridiculous.

2/ The problem: most security advice is written by specialists for
   specialists. Jargon walls out the people who actually run the systems.
   PMs, founders, operators, teachers, clinicians. You can't ask them to
   defend what they can't describe in their own words.

3/ The insight: those people describe attackers VIVIDLY — in physical
   terms. "Someone slips a fake card reader over the real one." That's a
   skimmer attack, which has a real security countermeasure (device
   attestation). The description was always correct. The vocabulary was
   the gatekeeper.

4/ So I built a framework. You tell a story about the attacker in plain
   English. Then you describe your defense as a physical scene. Then a
   lookup table translates each metaphor into a real security primitive.

5/ There are ten worked examples (small shop, clinic, kiosk, mobile app,
   internal portal, PoS terminal, school portal, IoT device, SaaS admin,
   personal email). Each one walks the attacker through the design and
   labels each step blocked / slowed / painted / passed.

6/ There's also a specialist review protocol. The framework doesn't
   replace a security engineer. It produces a draft the security
   engineer can actually improve, instead of starting from "what do you
   mean by 'password reset'?"

7/ Full disclosure of what it doesn't cover: nation-state actors,
   formal protocol flaws, hardware fault injection, parts of the legal
   landscape. Attacks without clean physical metaphors are intentionally
   out of scope. The honesty is in every doc.

8/ Everything is open. The guide, the table, the worked examples, two
   simulations (one against CVE-2024-3094), the review protocol. If
   you've ever been in a security meeting where you felt stupid, this is
   for you.

   [link]
```

**Thread B — the CVE-2024-3094 angle (security audience):**

```
1/ I ran a toy security framework through CVE-2024-3094 (the XZ Utils
   backdoor). The design failed badly on first attempt. Here's what
   broke, and the hardening progression that got it to 0% paper fault
   rate.

2/ CVE-2024-3094: trusted maintainer (Jia Tan) spent ~2 years earning
   trust before planting a backdoor in liblzma that compromised sshd.
   Caught by Andres Freund noticing a 500ms perf regression.

3/ Baseline framework: an authorization override pattern. 8 vectors
   tested. 6 fail, 2 weak. Fault rate 87.5%. The whole design assumed
   the authority was trustworthy. CVE-2024-3094 assumes exactly the
   opposite.

4/ Loop 1: added co-sign (two independent maintainers must agree).
   Closes the maintainer-compromise case and partially closes the
   social-engineering case. Fault rate drops to 56.3%.

5/ Loop 2: added reproducible builds + no binary blobs in build path.
   Closes the hidden-payload and IFUNC resolver cases. Fault rate drops
   to 31.3%.

6/ Loop 3: added immutable-until-quorum and trust half-life. Closes the
   dormant-backdoor case; immutability from loop 0 was actively harmful
   until there was a quorum to guard it. Fault rate drops to 12.5%.

7/ Loop 4: added validator attestation. Closes the compromised
   RSA_public_decrypt case. The hook was in the auth validator itself,
   so no earlier layer helped until the validator was itself attested.
   Fault rate 0.0%.

8/ The caveat the write-up ends on: 0% on paper ≠ 0% in production.
   The hardening raises the cost of attack, it doesn't eliminate it. A
   patient quorum-level insider still wins. Freund's 500ms is still the
   real defense.

9/ Full write-up and simulation: [link]
```

**Thread C — the ten-starter angle (startup/PM audience):**

```
1/ I wrote ten pre-made attacker stories for common systems. You can
   adapt one in 15 minutes and have the first page of a real security
   design.

2/ Small online shop: someone with a dump of credit cards tests them
   against your checkout. They don't care which fail. The ones that
   work pay for everything.

3/ Clinic patient portal: someone works from a laptop in another
   country, tries common admin passwords on a dozen small portals,
   downloads records on any that answer, sells to brokers.

4/ Public kiosk: someone leaves a fake bank login page open on the
   screen before walking away. The next user assumes someone forgot to
   close it.

5/ Mobile app: someone runs your app in an emulator, watches every
   request, finds fields in responses the app never shows, starts
   crafting direct API calls that bypass the app entirely.

6/ Internal portal: someone phishes one employee, logs in as them,
   looks around for valuable systems, requests access to one hoping
   the manager approves without thinking.

7/ Payment terminal: someone slips a thin plastic shell over your
   real card reader during a busy afternoon. Reads every card for six
   hours. Peels it off at closing.

8/ School grade portal: a student photographs a teacher's password
   from under their keyboard, logs in as them from their phone, changes
   one grade from C to B+, logs out.

9/ IoT device: someone scans the public internet for devices still on
   default passwords, installs a program that calls their server,
   recruits the device into a botnet without the owner noticing.

10/ SaaS admin: an engineer with legitimate production access is
    offered cryptocurrency per customer record. They have the keys. The
    extraction can look like their job.

11/ Each one has a full worked example: the scene your defense creates,
    the translation into real security primitives, and the attacker's
    walkthrough with blocked/slowed/painted labels on every step.

    [link]
```

---

## 4. Outreach templates

### 4.1 Co-author / endorsement outreach to a security engineer

Target: security engineers with a public presence writing about accessible security, deception, honeypots, developer-facing security. Look at Thinkst's team, authors who've written about honey tokens, people active in r/netsec, speakers at BSides.

```
Subject: A framework for non-security-engineers, and a question for you

[Name],

I've been reading [specific thing they wrote]. The point about [specific
point] matched something I was wrestling with.

I'm not a security engineer. I built a framework over the last few weeks
that lets non-specialists design layered defenses by describing attackers
as characters and defenses as physical scenes, then translating each
metaphor into a real primitive. The whole method, ten worked examples,
two simulations (one against CVE-2024-3094), and a specialist review
protocol are at [link].

Two asks, either fine on their own:

1. If you have 20 minutes, I'd love your reaction to the translation
   table in Section 3 of the framework doc. I know some rows are wrong;
   I don't know which.

2. If you ever teach or write about this stuff and the framework
   resonates, I'd welcome co-authorship or an endorsement on the next
   version. The honest story is that this method hits a credibility
   ceiling without a security engineer attached to it, and I'd rather
   build with the right person than publish alone.

Either way, thank you for the writing — [specific thing] in particular
changed how I was thinking.

[Your name]
```

### 4.2 Free workshop pitch — to a startup accelerator or incubator

```
Subject: Free 2-hour security workshop for your current cohort

[Name],

I'm offering three free 2-hour security design workshops to accelerators,
bootcamps, and non-profits over the next 60 days, in exchange for a
public testimonial and permission to list the program.

The workshop is designed for founders who don't have a security
background. Each team brings one system they're worried about; we walk
through designing a layered defense using a framework I built called
Metaphor-Driven Security Design. By the end of the session each team
has the first page of a real security design — one a security
consultant could pick up and extend.

I'd like to run one with your current cohort if the timing works. Remote
or in-person. Materials are open-source and at [link] if you want to
read them first.

Three slots total, first ask gets the first slot.

[Your name]
```

### 4.3 Paid design review cold outreach — to a small SaaS

```
Subject: A 90-minute security design review for [company]

[Name],

I run a design review service for small SaaS teams whose data would
hurt customers if it leaked. I spotted [specific thing on their site
or in their changelog] and thought it might fit.

Format: you fill out a short intake form, I review your system against
the Metaphor-Driven Security Design framework ([link to the open docs]),
and five business days later you have a 10–15 page PDF with: a model of
the attackers who'd most likely target you, a walkthrough showing what
your current defense does and doesn't block, and a prioritized list of
specific gaps to close with suggested next steps.

$500 flat for the first ten engagements while I build case studies.

If this is useful, reply and I'll send the intake form. If it isn't, no
hard feelings — but I'd welcome a line on what would be more useful.

[Your name]
```

### 4.4 Podcast / newsletter pitch

```
Subject: Pitch — a security framework for people who don't speak security

[Host name],

I pitch rarely so I'll be short. I built a security design framework
for non-specialists, published everything open, and ran it against the
XZ Utils CVE-2024-3094 class publicly to see where it fails. The whole
thing lives at [link].

A guest spot could work for your audience if you cover [specific thing
their show covers that this fits]. I can bring:

- A live walkthrough of one worked example (we pick the system from
  your audience's domain beforehand)
- The uncomfortable honest take: this doesn't make anyone a security
  engineer, and here's why that matters more than most frameworks
  admit
- The CVE-2024-3094 teardown as a worked case

Happy to send a 2-minute audio clip if that helps you evaluate.

[Your name]
```

---

## 5. The 90-day plan

Realistic cadence. Assumes 5–8 hours per week on this. Adjust up or down.

### Days 1–14 — Ship the storefront

- Clean up the doc set for consistency (one editing pass across all files).
- Build the HTML landing page (there is a published one at [URL to be filled in after Artifact publish]).
- Create Gumroad listing for Offer 1 ($29 PDF). Use the existing docs as content; add one new chapter from the book outline.
- Set up a simple email list (ConvertKit, Buttondown, or Substack free tier). One welcome email with a free excerpt.
- Add a "work with me" section to the landing page with all three paid offers and a scheduling link.

### Days 15–30 — First visibility push

- Post the Hacker News launch (Tuesday or Wednesday).
- Post the LinkedIn launch (Thursday of the same week).
- Post Thread A on Twitter/X.
- DM three security engineers you respect (not cold mass outreach — just three, personally written). Use the Section 4.1 template.
- Offer the first free workshop. One accelerator or bootcamp, personally written. Use the Section 4.2 template.

### Days 31–60 — Case studies

- Deliver the first free workshop. Record a short video testimonial from the host.
- Deliver two more free workshops.
- Publish the three free-workshop case studies on the landing page.
- Push Thread B on Twitter/X. Post one essay per week on LinkedIn applying MDSD to a current security news item.
- Start accepting Offer 2 (design review) at $500. First five customers.

### Days 61–90 — Price up and compound

- Raise Offer 1 (ebook) to $49 if sales support it.
- Raise Offer 3 (workshops) to $1,500 (startups) / $3,000 (mid-sized).
- Pursue one co-author conversation from the Section 4.1 outreach — make it a specific co-authored piece or endorsement, not an open-ended "collaborate."
- Pitch one podcast or newsletter using the Section 4.5 template.
- Review and decide: is this working enough to scale? If yes, double the hours. If no, retreat to passive ebook sales + the GitHub repo as a portfolio piece.

---

## 6. Metrics worth tracking

Don't obsess, but check monthly:

- **Repo stars** — proxy for public attention. 50 stars in month one is good; 500 is excellent.
- **Email subscribers** — the real audience. 100 is a start; 500 means something; 2,000 is a business.
- **Gumroad sales** — raw dollars. Any revenue beats zero. $100/month means the funnel works and can be scaled.
- **Workshop requests** — demand signal. One a month is modest; one a week means consider it a career.
- **Design review requests** — highest-value demand signal. One a quarter is realistic; one a month means you have a service business.
- **Co-author replies to Section 4.1 outreach** — the single highest-leverage metric. Even one yes changes the ceiling of everything.

---

## 7. Honest ceiling with and without a co-author

| Scenario | Year 1 revenue | Year 2 | Reputation ceiling |
|---|---|---|---|
| Solo, part-time, no co-author | $500–$5,000 | $5,000–$20,000 | Niche authority in accessible security |
| Solo, part-time, with co-author or endorser | $2,000–$15,000 | $20,000–$60,000 | Recognized name in a specific sub-field |
| Solo, full-time, with co-author | $15,000–$50,000 | $50,000–$150,000 | Known teacher/consultant |
| Full-time + co-author + funded startup | $0–$30,000 (burn phase) | $0–$200,000 | Depends entirely on execution |

The single most important variable is the co-author. The second most important is consistency over 12 months. The third is willingness to charge money and keep raising prices on each successful engagement.

---

## 8. Legal and ethical fine print

Before taking money for any security work:

- **Business entity.** An LLC or similar is standard protection. Your call, but worth it before Offer 2 or 3 engagements.
- **Insurance.** Professional liability (E&O) is $300–$1,200/year for solo consultants. Required by many enterprise buyers.
- **Scope-of-engagement letter.** Every paid review needs one. Spell out: what's reviewed, what's not reviewed, who the client is, what deliverable they get, what they can and cannot do with it, limits of liability.
- **Honest limits in every deliverable.** The honesty is itself a differentiator against the long tail of security grifters. Protect it.
- **Deception legality.** Several patterns in the framework (shadow surface, dialect-as-honeypot) have jurisdiction-specific legal implications. Flag this to buyers; don't advise on it.

---

## 9. What not to do

- **Don't promise security.** You cannot deliver it. You can deliver a framework and a review.
- **Don't attack competitors.** The field has long memory.
- **Don't let the ebook become the business.** $29 PDFs are the top of a funnel, not the base of a company.
- **Don't skip the free workshops.** Case studies compound. The three free workshops in month two unlock everything in months three onward.
- **Don't price down after raising.** Discounting signals desperation. If an engagement is bigger, add scope, not drop price.
- **Don't take enterprise money without a co-author.** The deliverable gap is too wide, and the reputation damage from a bad outcome is permanent.

---

## 10. The one thing to do today

Open the Hacker News launch post from Section 3, personalize the first paragraph with your actual role and the actual conversation that started this, and schedule it for next Tuesday at 7am Pacific. Everything else in this document is downstream of that single post.
