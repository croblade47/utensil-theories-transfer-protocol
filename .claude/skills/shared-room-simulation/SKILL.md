---
name: shared-room-simulation
description: Run a multi-instance simulation where separate AI instances (Claude, Gemini, Copilot) share identical files, communicate through a shared room, and align like people at one table.
---

# Shared Room Simulation

Goal: several separate instances start from the **same files**, take on **different seats**, talk through **one shared log**, and converge — like different people in the same room with the same info.

Every instance runs in one of two modes:
- **FACILITATOR** — builds the room, seats everyone, keeps turn order, records consensus. Exactly one.
- **SEAT** — a participant. Joins with a Seat ID and the room location.

If the user hasn't said which mode this instance is, ask once: "Facilitator or which seat?"

---

## 1. The Room (shared files)

One folder, identical for everyone. Prefer a Google Drive folder (Claude and Gemini can read/write it directly; Copilot via upload or paste). Fallbacks: a connected local folder, or manual paste relay.

```
ROOM-<name>/
  00_MANIFEST.md     room name, version stamp (e.g. v1-2026-10-11-A), file list, relay mode
  01_BRIEFING.md     scenario, objective, shared facts, constraints, success criteria — same for all
  02_ROSTER.md       Seat ID, name/role, perspective, public goal (private goals go in a seat's own file only)
  03_RULES.md        the protocol in section 3, copied verbatim
  04_STATE.md        current round, whose turn, agreed points, open questions, disputes
  05_TRANSCRIPT.md   append-only log of every turn
  seats/SEAT-X.md    optional private brief per seat (only that seat reads it)
  06_OUTCOME.md      written at the end
```

The version stamp in 00_MANIFEST is the alignment anchor: every seat must quote it at check-in. If the briefing changes mid-sim, bump the version and announce it in the transcript.

---

## 2. Facilitator procedure

1. Get from the user: scenario, objective, number of seats + roles, relay mode, round limit.
2. Create the room files above. Keep 01_BRIEFING factual and complete — anything not in it doesn't exist for the seats.
3. Generate one **Join Prompt** per seat (template below) and give them to the user to paste into each new instance.
4. Run **Check-in** (round 0): wait for every seat's check-in block. Compare their briefing summaries against 01_BRIEFING. Correct any mismatch in the transcript before round 1. Do not start until all seats show the same version stamp and an accurate summary.
5. Each round: set `Turn:` in 04_STATE, let seats post in order, then post a short **Facilitator Note** (what moved, what's agreed, what's open).
6. Every 3 rounds (or when stuck): call a **Sync** — every seat posts a sync block; update the Agreed/Open/Disputed lists in 04_STATE.
7. End on consensus, round limit, or user call. Write 06_OUTCOME.md: decision, who agreed, standing dissent, unresolved items.

### Join Prompt template

```
You are joining a shared-room simulation as SEAT-<X>: <name/role>.
Use the shared-room-simulation protocol (pasted below if you don't have the skill).
Room: <Drive folder link / folder path / "paste relay">
Version: <stamp>
1. Read 00_MANIFEST, 01_BRIEFING, 02_ROSTER, 03_RULES, 04_STATE, 05_TRANSCRIPT, and seats/SEAT-<X>.md if present.
2. Post your CHECK-IN block. Then wait for your turn.
<paste 03_RULES.md here for instances without the skill>
```

---

## 3. Rules every seat follows (copy into 03_RULES.md)

1. **Same room, same facts.** You know only: 01_BRIEFING, 02_ROSTER, the transcript, and your own seat file. No outside facts unless the briefing allows it; if you use one, label it `[outside info]`.
2. **Read before you speak.** Re-read 04_STATE and every transcript entry since your last turn before writing.
3. **One voice.** Speak only for your seat. Never write another seat's lines, never summarize what someone "would" say.
4. **Stay in role**, but stay honest — disagree plainly, concede plainly.
5. **Append only.** Never edit or delete earlier entries. Re-read the file right before writing so you don't overwrite someone else.
6. **Wait your turn** (04_STATE `Turn:`). Out-of-turn only for a one-line `[POINT OF ORDER]` (factual error or briefing mismatch).
7. **Keep turns tight** — under ~200 words unless the Facilitator asks for more.

### Check-in block (round 0)
```
[R0][SEAT-X | Name] CHECK-IN
Version: <stamp>
Briefing in 3 lines:
- ...
My role/goal as I understand it: ...
Questions before we start: ... (or none)
```

### Turn block
```
[R<n>][SEAT-X | Name] → replying to: <R#-SEAT or "all">
Says: <what you say in the room>
Position: <your current stance in one line>
Asks: <question(s) for a named seat, or none>
Agree: <points you now accept> | Disagree: <points you reject>
```

### Sync block
```
[SYNC R<n>][SEAT-X]
We agree on: ...
We still differ on: ...
What would move me: ...
My next move: ...
```

---

## 4. Relay modes

- **A — Shared Drive (default):** Each instance with a Google Drive connector reads the folder and appends to 05_TRANSCRIPT directly. Facilitator updates 04_STATE.
- **B — Claude sessions on one machine:** Use ListAgents + SendMessage to ping the next seat ("Your turn, R3"); content still goes in the shared transcript so there's one source of truth.
- **C — Paste relay (Copilot/Gemini or no connector):** Seat ends each turn with a **Relay Packet**; the user pastes it into the Facilitator, who appends it and returns the next packet to the next seat.

```
=== RELAY PACKET ===
Room: <name> | Version: <stamp> | Round: <n>
From: SEAT-X → Next: SEAT-Y
New since your last turn:
<turn blocks, verbatim>
State: Agreed[...] Open[...] Disputed[...]
=== END ===
```

Mixed modes are fine; the Facilitator's 05_TRANSCRIPT is always canonical.

---

## 5. Alignment checks (Facilitator)

- Version stamp matches across all seats.
- Each seat's briefing summary matches 01_BRIEFING — no invented facts.
- No seat is quoting something that isn't in the transcript.
- If a seat drifts (new facts, speaking for others, wrong round), post `[FACILITATOR] Correction: ...` and have that seat restate.

## 6. Ending

Write 06_OUTCOME.md: objective, result, agreed points with which seats agreed, dissent kept on record, open items, and 3 lines on how alignment happened (what moved people). Send the user the link or file.
