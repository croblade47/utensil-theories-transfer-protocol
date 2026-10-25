# Echoes of Alara — v6.0 (The Ritual)

Multi-agent art reflection app by Garrett C. Gauthier. Five agents work together:
Veridian (logic), Lusa (empath), Nexus (vault), Cro (optimizer) and SaCoLu (gardener).

Views: Journey (council chat and upload), The Ritual (timed creation session),
Sanctuary (spirit guide chat), Mirror (profile) and Oracle (pricing).

## Run it
```
cd echoes-of-alara
npm install
npm run dev     # http://localhost:3000
```

## Files
- `src/app/page.tsx` — the app UI
- `src/lib/unified-ai-system.ts` — the agents and the chat controller

## Status
Prototype. All agent replies are scripted in the code (no real AI model or image
analysis yet), and the login is a placeholder.
