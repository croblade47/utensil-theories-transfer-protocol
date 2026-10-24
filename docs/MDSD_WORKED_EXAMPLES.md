# Ten MDSD Worked Examples

**Companion to `MDSD_ATTACKER_STORY_STARTERS.md`.** Each starter is carried through Steps 3, 4, and 5 of the how-to guide — scene, translation, walkthrough — as a reference pattern. These are illustrative, not prescriptive: your actual draft should specialize the story to your own system before translating.

Each example ends with **one honest limit** the design does not cover.

---

## Example 1 — Small online shop vs. card testing

**Scene:** Buying anything on the storefront requires the browser to first wait in a short "preparing checkout" screen that always takes the same amount of time regardless of outcome. On that screen, the device is fingerprinted and the card is scored against a reputation signal shared across many small shops. Any card that has failed anywhere in the network in the last 30 days quietly resolves as "payment declined, please try another card" without ever touching the real processor. Legitimate buyers barely notice the wait; a script sending hundreds of attempts sees no useful difference between a live decline and a shadow decline.

**Translation:**

| What I pictured | What that actually is |
|---|---|
| Fixed-time checkout screen | Response-time normalization (anti-side-channel) |
| Device fingerprint on load | Browser/device telemetry |
| Shared network reputation | Federated card reputation / fraud consortium |
| Shadow decline | Deception response / honeypot decline path |
| Attempts don't reach processor | Pre-gateway filtering |

**Walkthrough:**

| Attacker move | Result |
|---|---|
| Opens checkout, sends card #1 | Slowed (fixed wait) |
| Card #1 fails on another shop → repeats here | Painted (reputation hit) |
| Switches to card #2 | Slowed again |
| Sees a success response | Painted (shadow decline; no real transaction) |
| Resells "verified" cards | Blocked (next buyer runs into reputation immediately) |

**Honest limit:** Fresh cards not in any reputation network pass through the design. First-use fraud needs an additional layer (small-amount prepayment hold or 3DS challenge).

---

## Example 2 — Clinic patient portal vs. records theft

**Scene:** The admin login requires a password *and* a hardware key the staff carry on their person. If someone logs in from a device the clinic has never seen, the account can read but not download, and the first attempted download triggers an SMS to a nurse manager who must approve before any record leaves. Any single account downloading more than 20 records in a day quietly stops working and the person has to walk into the office in the morning for a conversation.

**Translation:**

| What I pictured | What that actually is |
|---|---|
| Hardware key | Phishing-resistant second factor |
| New-device read-only mode | Device trust tier / risk-based access |
| SMS approval before export | Out-of-band step-up for bulk export |
| 20-record daily cap | Rate-limited data egress |
| Account "quietly stops working" | Soft-lock with human review |

**Walkthrough:**

| Attacker move | Result |
|---|---|
| Guesses password | Blocked (hardware key required) |
| Phishes password | Still blocked (hardware key is phishing-resistant) |
| Steals hardware key physically | Slowed (new device = read-only) |
| Attempts bulk download | Painted + Blocked (nurse manager pings, account locks) |
| Does 19 downloads/day, waits a day, repeats | Painted (anomaly detection catches the pattern over time) |

**Honest limit:** An insider with their own hardware key and legitimate reason to see records is not stopped by this design. Trusted-insider misuse needs quorum review (Example 3 of the framework doc, Loop 1+).

---

## Example 3 — Public kiosk vs. bait-and-switch

**Scene:** Each session is bound to a physical presence signal — the kiosk's seat has a weight sensor, or a motion sensor confirms a continuous user. When presence breaks (person stands up), the browser is terminated, cookies are flushed, downloads deleted, and the next user starts on a fresh profile. The screen also shows a short, randomly generated phrase in the top corner from the moment the session starts; if a page claims to be a bank or login page but the phrase isn't there, the kiosk's own browser frame flashes a banner that the page may be impersonating a real site.

**Translation:**

| What I pictured | What that actually is |
|---|---|
| Presence sensor | Physical attestation of session continuity |
| Full flush between users | Ephemeral per-session environment |
| Random phrase on screen | Trusted UI indicator / anti-phishing watermark |
| Browser frame banner | Browser chrome signals (out of band from page content) |

**Walkthrough:**

| Attacker move | Result |
|---|---|
| Opens fake bank page, walks away | Blocked (session terminates on stand-up) |
| Loads fake page quickly before standing | Painted (banner names it as unverified) |
| Camera overlay to spoof the phrase | Slowed (phrase rotates per session; victim's phrase differs from any pre-recorded one) |
| Shoulder surf next user | Out of scope |

**Honest limit:** This design does not stop a social-engineering overlay that the victim trusts for reasons unrelated to the screen (e.g., the attacker standing nearby in a uniform telling them what to do).

---

## Example 4 — Mobile app vs. API abuse

**Scene:** The server never trusts the app's claims. Every price, every user ID, every "I'm allowed to see this" is verified server-side against the authenticated session. Requests that come in with fields the server didn't send out in a recent response are rejected and the sending IP is thrown into a slow-lane for an hour. The app binary is signed and every request includes a short-lived attestation that it came from an unmodified install; requests without one are routed to a shadow API that returns plausible-looking but synthetic data.

**Translation:**

| What I pictured | What that actually is |
|---|---|
| Server verifies everything | Server-side authorization, no client trust |
| Unknown fields = rejected | Strict input schema validation |
| Slow-lane bad senders | Adaptive rate limiting |
| App attestation | DeviceCheck / Play Integrity / app attestation API |
| Shadow API for unattested | Deception + honey data |

**Walkthrough:**

| Attacker move | Result |
|---|---|
| Reads traffic from the app | Allowed (not an attack by itself) |
| Sends crafted request with another user's ID | Blocked (server-side authorization) |
| Adds unknown field hoping server honors it | Blocked (schema rejects) |
| Switches to emulator to bypass app checks | Painted (no attestation → shadow API) |
| Writes own client, replays known-good tokens | Slowed (short-lived attestation expires) |

**Honest limit:** App attestation can be bypassed on jailbroken/rooted devices by skilled attackers. The design degrades gracefully (shadow API) but doesn't block determined reverse engineering.

---

## Example 5 — Internal portal vs. phished credential + lateral movement

**Scene:** Login requires the password plus a phishing-resistant factor (hardware key or platform passkey). Every sensitive action — anything that changes data, requests access, or exports — requires a second factor touch, not just the initial login. A login from a new location or new device opens a *limited session* that cannot request new access, cannot export data, and cannot see the fleet-wide employee directory. Access requests to additional systems require two humans (the manager *and* the owner of the target system) to approve independently.

**Translation:**

| What I pictured | What that actually is |
|---|---|
| Phishing-resistant factor | FIDO2 / passkey / hardware key |
| Second-factor touch per sensitive action | Step-up auth / transaction authorization |
| New-location limited mode | Risk-based conditional access |
| Two independent approvals | Dual control / four-eyes principle |
| No fleet-wide directory in limited mode | Need-to-know scoping |

**Walkthrough:**

| Attacker move | Result |
|---|---|
| Phishes password | Blocked (second factor required) |
| Phishes password + session cookie | Slowed (sensitive actions require fresh touch) |
| Logs in from attacker's laptop | Painted (new device → limited session) |
| Requests access to another system | Blocked (needs dual approval) |
| Tries to enumerate employees | Blocked (directory hidden in limited mode) |

**Honest limit:** An attacker with physical access to the employee's unlocked laptop in a known location gets around every limit here. Endpoint compromise remains out of scope.

---

## Example 6 — Payment terminal vs. physical skimmer

**Scene:** The terminal cryptographically attests to the point-of-sale system every 60 seconds that it is the same device it was last minute, using a key burned into its secure element. A shell slipped over the real reader cannot forward that attestation. When attestation stops arriving, the POS freezes card acceptance and surfaces a banner telling the clerk to inspect the terminal. The real terminal also displays a short, store-specific phrase on its screen between transactions; if the shell covers it, the clerk notices immediately.

**Translation:**

| What I pictured | What that actually is |
|---|---|
| Cryptographic heartbeat | Device attestation with a hardware-backed key |
| Freeze on silence | Fail-safe behavior |
| Clerk-visible banner | Operator alerting at the physical point |
| Store-specific phrase | Visible tamper indicator |

**Walkthrough:**

| Attacker move | Result |
|---|---|
| Slips shell over reader | Painted (attestation stops within 60s) |
| Terminal freezes | Blocked (no cards accepted while silent) |
| Attacker tries to leave shell for later | Blocked (clerk sees banner on next sale) |
| Attempts to spoof attestation | Slowed (key is in secure element, not extractable) |

**Honest limit:** A compromise of the terminal firmware *before* it reaches the store (supply chain) bypasses the heartbeat because the attacker holds the real key. Firmware provenance is a separate design (Example 3 in the framework doc).

---

## Example 7 — School grade portal vs. insider grade change

**Scene:** Changing a grade requires the teacher's login *and* a second teacher's independent confirmation within 24 hours. Every grade change is recorded in an append-only ledger that students, parents, and administrators can view. The ledger shows the old value, the new value, both teachers' names, and a free-text reason. A grade that changes without a reason, or a reason that doesn't match a documented reassessment, is flagged automatically. A student logging in from a teacher's account triggers a device-change alert even if the password is correct.

**Translation:**

| What I pictured | What that actually is |
|---|---|
| Two-teacher confirmation | Dual control for sensitive writes |
| Append-only ledger | Audit log with cryptographic integrity |
| Reason required | Workflow enforcement on write |
| Device-change alert | Behavioral authentication |

**Walkthrough:**

| Attacker move | Result |
|---|---|
| Logs in with teacher's password | Painted (device change → alert) |
| Changes a grade | Blocked (needs second teacher) |
| Convinces second teacher to confirm socially | Slowed (reason is in the record; audit visible) |
| Grade changes without reason | Blocked (workflow rejects) |
| Student reads ledger, sees own grade untouched | Blocked (no change happened) |

**Honest limit:** Two colluding teachers can change a grade and co-sign each other. Collusion by trusted parties needs structural separation of duties and periodic external audit.

---

## Example 8 — IoT device vs. botnet recruitment

**Scene:** The device ships with no default password. On first boot it requires the owner to set one via a short code the owner reads from a physical sticker on the device. The device only accepts firmware updates signed by the manufacturer's key and verified against a reproducible build. Outbound connections are limited to a pre-registered set of destinations; anything else is dropped and logged to the manufacturer's cloud. If the device starts sending traffic that doesn't match its declared purpose, the manufacturer can push a kill-switch and the owner's app shows what happened.

**Translation:**

| What I pictured | What that actually is |
|---|---|
| No default password + sticker code | Unique-per-device bootstrapping credential |
| Signed firmware + reproducible build | Verified secure boot and build provenance |
| Egress allowlist | Network segmentation on the device itself |
| Kill-switch + owner app transparency | Remote attestation + user-facing incident disclosure |

**Walkthrough:**

| Attacker move | Result |
|---|---|
| Tries common default passwords | Blocked (no default exists) |
| Pushes unsigned firmware | Blocked (signature check) |
| Pushes signed-but-malicious firmware | Slowed (reproducible build mismatch surfaces) |
| Device talks to attacker's C2 | Blocked + Painted (egress drop logged) |
| Convinces owner to install something | Slowed (owner sees a disclosure on install) |

**Honest limit:** Compromise of the manufacturer's signing infrastructure defeats everything downstream. That compromise is Example 3 in the framework (CVE-2024-3094 class).

---

## Example 9 — SaaS admin console vs. supply chain / insider

**Scene:** No single engineer can read customer data unilaterally. Every production read of a customer record requires an engineer to open a case tied to a customer-approved request, and that case is reviewed in real time by a second engineer on another team. All reads are logged customer-visibly in their own audit log. Access that fits normal patterns is instant; access that doesn't (unusual customer, unusual time, unusual volume) requires a third approver and a reason posted to a public internal channel.

**Translation:**

| What I pictured | What that actually is |
|---|---|
| Case tied to customer request | Just-in-time access with ticket binding |
| Real-time second-engineer review | Human-in-the-loop approval |
| Customer-visible audit log | Transparent logging / customer accountability |
| Three approvers for anomalies | Risk-tiered authorization |

**Walkthrough:**

| Attacker move | Result |
|---|---|
| Reads a customer's data as normal part of job | Painted (visible to customer) |
| Reads a customer the attacker wasn't assigned to | Blocked (no open case) |
| Opens a case with fabricated reason | Slowed (second engineer sees it live) |
| Does small reads over many days to stay under threshold | Painted (aggregated anomaly detection) |
| Attempts to disable logging | Blocked (log is append-only, outside admin's reach) |

**Honest limit:** A sufficiently coordinated group inside the company can approve each other's requests and tell a plausible story. Quorum size and tier escalation reduce this but cannot eliminate it.

---

## Example 10 — Personal email vs. account takeover

**Scene:** The email account requires a passkey or hardware key, not just a password. Password reset requires access to the device the passkey lives on *and* a 24-hour cooldown. Any other services using this email as recovery are periodically audited by the user in a dashboard the provider offers. Login notifications from unknown devices go to the account owner's phone *before* access is granted, not after. The provider offers a "freeze" button that locks all recovery flows for 72 hours while the owner investigates.

**Translation:**

| What I pictured | What that actually is |
|---|---|
| Passkey / hardware key | Phishing-resistant primary factor |
| 24-hour reset cooldown | Delayed sensitive action with user notification |
| Recovery audit dashboard | User-managed federated-identity view |
| Pre-approval login notifications | Authorization-prompt instead of after-the-fact alerts |
| Freeze button | User-controlled kill switch |

**Walkthrough:**

| Attacker move | Result |
|---|---|
| Guesses or buys the password | Blocked (passkey required) |
| Phishes passkey | Blocked (phishing-resistant by design) |
| SIM-swaps the phone for SMS recovery | Blocked (SMS not used as recovery here) |
| Requests reset | Slowed (24h cooldown + notification) |
| Attempts in-session hijack after legitimate login | Slowed (sensitive actions prompt reauth) |

**Honest limit:** An attacker with physical access to the device holding the passkey, or with the owner's biometrics (coerced or captured), bypasses most of this. Device compromise is upstream of the account.

---

## How to use these examples

Pick the one closest to your system. Replace the generic nouns with your own ("customer," "clinic," "device" → your actual thing). Walk your attacker through the specialized version and see which rows still come out blocked, slowed, painted, or passed.

If none of these fits, write your own from scratch — the pattern is the same: short scene paragraph, five-ish-row translation, five-ish-row walkthrough, one honest limit stated out loud.
