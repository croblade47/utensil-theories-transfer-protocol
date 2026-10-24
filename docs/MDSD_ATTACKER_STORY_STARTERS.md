# Attacker Story Starters

**Ten short attacker paragraphs you can adapt as the opening of a MDSD draft (Step 1 of the how-to guide).**

Each starter is written in plain English in the attacker's own voice. Each one is deliberately generic. Your job is to **edit it until it describes a specific attacker going after your specific system**. The more specific the final version, the stronger the design that comes out of it.

For each starter you'll find:

- **System type** — what kind of system it fits.
- **Story** — the paragraph. Copy and edit.
- **Goal in one sentence** — Step 2 of the guide, pre-written.
- **Prompt** — three questions to help you specialize the story.

---

## 1. Small online shop — card testing

**System type:** E-commerce checkout, small-business web storefront, any site that accepts card payments.

**Story:** You bought a list of a few thousand credit card numbers from a forum. Most are expired or canceled, but somewhere in the pile there are live ones. You wrote a short script that opens the checkout page of a dozen small shops and tries one card at a time, buying the cheapest thing in each store — a $1 digital gift card, a $3 download, a $5 e-book. If the purchase goes through, that card is live and worth $20 to $50 to the next buyer. You don't care about the merchandise. You don't care if 95% of the attempts fail. The ones that work pay for the whole operation.

**Goal in one sentence:** *"I want to find out which of these card numbers still work."*

**Prompt to specialize:**
1. What is the cheapest thing you sell, and what's the exact flow to buy it?
2. How would you tell a human buying one gift card from a script buying 500?
3. If a card fails on your site today, is anything about that failure visible to the next shop the attacker tries?

---

## 2. Clinic or medical office — records theft

**System type:** Patient portal, electronic health record system, any system holding sensitive personal data.

**Story:** You work from a laptop in another country. You've compiled a list of small clinics with online patient portals, picked from a public directory. You know their software is probably off-the-shelf and probably not patched this quarter. You have a quiet afternoon. You try the common administrator passwords on each portal. On the ones that don't block you after three tries, you start reading. You download whatever lists of patients and diagnoses you can find. The data isn't for ransom — it's for selling to a broker who resells it to insurers, scammers, and political researchers.

**Goal in one sentence:** *"I want to copy as much patient data as I can before anyone notices."*

**Prompt to specialize:**
1. Who in your clinic has an administrator account on the portal? Is their password strong, and do they use it anywhere else?
2. What is the maximum number of patient records someone could download in an hour without an alarm firing?
3. If someone did download them, how long would it take you to notice, and from what signal?

---

## 3. Public kiosk or library computer — bait and switch

**System type:** Shared public computer, self-service kiosk, library terminal, hotel-lobby station.

**Story:** You walk into a public library on a Tuesday afternoon. You sit down at one of the free-use computers. You open a browser, go to a site that looks like a bank login, and leave the page open on screen when you walk away. The next person who sits down sees what looks like the bank's login page. They might assume someone forgot to close it. They might log in. If they do, the credentials go to you by whatever back channel you set up before you walked out.

**Goal in one sentence:** *"I want the next user of this computer to hand me their password without knowing."*

**Prompt to specialize:**
1. What state does your kiosk hold between users? Browser history, open tabs, downloaded files, cached logins?
2. How does a new session start — automatically, on a timer, by a button, by a staff member?
3. Can the user see what the previous person did on this machine, or is it hidden?

---

## 4. Mobile app — reverse engineering and API abuse

**System type:** iOS or Android app with a backend API; any app that talks to a server to get or send data.

**Story:** You downloaded the app from the store. You installed it on an emulator so you can watch what it says to its server. You see every request go out and every response come back. You read the responses carefully. There are fields in the responses the app never shows the user — internal flags, user IDs that aren't yours, prices before discount. You start sending your own crafted requests, bypassing the app entirely. The server answers them. You start finding what else you can get the server to answer with the right-shaped request.

**Goal in one sentence:** *"I want to make the server do things the app would never let me do."*

**Prompt to specialize:**
1. Does your app assume the request came from your app, or does the server verify it independently?
2. If a user calls your API with values that would never come from the app (negative numbers, other users' IDs, impossible dates), what happens?
3. Does the server tell the app anything the user shouldn't see — in a hidden field, a debug flag, an unused response key?

---

## 5. Internal company portal — phished credentials, lateral movement

**System type:** Any internal web application, SaaS admin console, VPN gateway, or employee portal.

**Story:** You sent a convincing email yesterday to twenty employees of a small company. One of them clicked the link and typed their username and password into a page you built that looked exactly like the real login. Today you log in as them. You don't want to break anything right away. You want to look around. You open everything you have access to, screenshot it, download what you can. You note which systems your victim could reach that look more valuable than what you're in now. You find a page where they can request access to another system; you request it, hoping their manager approves without thinking.

**Goal in one sentence:** *"I'm already in as a real user — now I want to move deeper."*

**Prompt to specialize:**
1. If an employee logs in from a laptop you've never seen before, in a city they've never worked from, does anything change?
2. How far could one phished employee reach into the company? Draw the rooms their badge opens.
3. Who approves access requests, and what do they look at before approving?

---

## 6. Payment terminal or point of sale — skimming

**System type:** In-store payment terminal, point-of-sale system, any device where cards are swiped or tapped.

**Story:** You visit a busy coffee shop. You bring a thin plastic shell that looks exactly like the card reader on their counter — same color, same shape, same brand. When the barista turns to make a drink, you slip it over the real reader. For the next six hours, every customer who taps or swipes a card is routed through your shell. Their card data flows into a small radio in your pocket. You walk back in at closing time and peel it off. You sell the data by midnight.

**Goal in one sentence:** *"I want every card used at this terminal to also be read by me."*

**Prompt to specialize:**
1. Would an employee notice if the card reader looked slightly different today than it did yesterday?
2. Does the payment terminal verify to the back-end system that it is still the device it was supposed to be?
3. What is the exact physical path a card number takes from the customer's hand to the bank?

---

## 7. School grade portal — insider misuse

**System type:** Student information system, grade portal, HR system, or any system where the user is also the subject of the data.

**Story:** You're a student. You know the grade portal uses your student ID and a password. You also know some of the older teachers write their passwords on sticky notes under their keyboards. During your free period you walk into an empty classroom, flip the keyboard, and photograph the note. That afternoon from your phone you log in as the teacher. You change one of your grades from a C to a B+. You change nothing else. You hope it will be months before anyone notices, and if they do, nothing points to you.

**Goal in one sentence:** *"I want to change a record about me without being traced."*

**Prompt to specialize:**
1. Can a teacher's account change a grade without any second person involved?
2. If a grade changes, does the system remember who it used to be, and who changed it, and when?
3. Could a student's own account impersonate a teacher if the student knew the teacher's password?

---

## 8. Smart-home or IoT device — botnet recruitment

**System type:** Internet-connected device sold to consumers — thermostat, camera, doorbell, light bulb, speaker, router.

**Story:** You're building a network of a hundred thousand compromised devices to rent out to anyone who wants to flood a target with traffic. You scan the public internet for devices that still have their default admin password. You find thousands every day. You log in, install a small program that calls home to your command server, and move on. The device still works for the family that owns it; they'll never know. When you need traffic, you tell all of them at once to send requests to whatever target your customer specified.

**Goal in one sentence:** *"I want this device to also work for me, while continuing to work for its owner."*

**Prompt to specialize:**
1. What is the password on this device when it ships, and how does the owner change it (and do they)?
2. If this device starts sending traffic to a strange destination, would the owner's internet provider notice, or would the owner?
3. What does the device do when it receives a software update, and who can send it one?

---

## 9. SaaS admin console — supply chain or insider

**System type:** B2B SaaS platform where one company's admins can affect many customer organizations; infrastructure provider, HR platform, payments platform.

**Story:** You interviewed for an engineering job at a SaaS company nine months ago. You got the job. You were a good hire. You've been a solid contributor. Last month you were given access to the production admin console as part of a project. You have, from that console, the ability to read any customer's data. You've never used it beyond your project. Yesterday someone contacted you with an offer: a payment per customer record you can extract, matched with cryptocurrency you can't trace. You are considering it.

**Goal in one sentence:** *"I already have the keys. I need the extraction to look like my job."*

**Prompt to specialize:**
1. Which actions in your admin console look identical whether taken for the normal reason or the attacker's reason?
2. Does any single engineer have unilateral read access to any customer's data?
3. If an engineer began reading customer data at an unusual pace or for unusual customers, what signal would surface where?

---

## 10. Personal email — account takeover for everything else

**System type:** A single personal email account. Note: this starter is more useful than it sounds, because many systems treat email as the root of identity.

**Story:** You know a target's email address. You go to each of the online services that person is likely to use — their bank, their social accounts, their shopping, their work. On each, you click "forgot password." The password reset emails flow into their inbox. If you can read that inbox, you can click those links. So the whole attack reduces to: get into the email. You phish, you buy a credential dump, you try the common weak passwords. You keep going until the inbox opens.

**Goal in one sentence:** *"If I own the inbox, I own everything that trusts the inbox."*

**Prompt to specialize:**
1. If someone reset the password on your email account today, what second step would stop them? What if that second step is also in the inbox?
2. What accounts of yours use that email as the recovery address? Make a list — the list will be longer than you expect.
3. Who has access to your email besides you? Devices you've forgotten, apps you authorized years ago, former assistants or partners.

---

## How to use a starter

1. Pick the one closest to your system.
2. Rewrite every "you" sentence to describe *your* system — your checkout, your clinic, your terminal. Replace generic nouns with specific ones.
3. Add one detail only you would know. The detail that is specific to your system is the detail the generic templates can't give you, and it's the one that makes the design actually fit.
4. Answer the three Prompt questions in your notebook. Your answers often become new sentences in the story.
5. Proceed to Step 2 of the how-to guide with the specialized version.

If none of these ten fits, write your own from scratch using the how-to guide. These are starters, not boxes. The more your draft looks like a story only you could have written, the better it will serve the design.

---

## Note on scope

These starters cover common attacker shapes. They do not cover: nation-state actors with time and budget, physical theft at scale, cryptographic protocol flaws, hardware fault injection, or legal and regulatory attacks (which are real and matter). If your threat model includes any of those, write the story directly and flag it clearly for specialist review — do not try to retrofit it from one of these templates.
