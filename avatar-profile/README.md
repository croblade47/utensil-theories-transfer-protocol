# Garrett C. Gauthier — Conceptual Engineer (interactive profile)

An interactive profile with three live pieces:

- **The Room** — a simulation room where you talk to an **Avatar** ("Echo") built from Garrett's own words.
- **The Matching Game** — ask the Avatar and Garrett the same question, blind, and rate how close the Avatar lands. The goal isn't an identical answer, it's one that's *like* his.
- **Guard Dog** — the security idea the Avatar feeds into, with an honest engineering assessment of what it can and can't do.

## How the Avatar ("Echo Key") works
`scripts/compile-echo-key.mjs` reads two curated source files in `../echo-key/sources/`
(voice notes + public writing samples) and compiles them into one persona prompt
(`src/lib/echo-key.generated.ts`). The chat API wears that persona.

- Re-run the compiler any time the sources change: `npm run compile-echo-key`.
- The sources hold **only** a speaking style and already-public work lines — no contact
  info, no accounts, no biometric data. The raw session transcripts the notes were drawn
  from are kept private and are **not** in this repo.

## Live vs offline
- With `ANTHROPIC_API_KEY` set in the environment, the Avatar runs on Claude (`claude-opus-4-8`).
- With no key, it falls back to a few canned answers so the demo still runs. The Room shows
  an "offline mode" note when that happens.

## Run it
```
cd avatar-profile
npm install
npm run dev        # http://localhost:3000
```
Set a key for live answers: add `ANTHROPIC_API_KEY` in the environment's settings (not in the repo).

## Honest status
This is a prototype and a portfolio piece. The Avatar is a character study, not the real person
and not a login. See the Guard Dog page for why a personality model plus biometrics is a useful
*risk signal* but not a replacement for passwords or a second factor.

Made with Claude (Anthropic) in Claude Code.
