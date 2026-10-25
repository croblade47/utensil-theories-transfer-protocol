# The Echo Key

A pipeline that compiles a person's own words into a persona an LLM can wear.

```
sources/            curated, reviewed inputs (safe to publish)
  curated_traits.md     hand-written notes on how Garrett thinks and talks, with sources
  public_samples.jsonl  Garrett's own work lines (email + a friend's name removed)
private/            NOT committed (see .gitignore) — raw transcripts the notes came from
compiled/           reserved for future compiled artifacts
```

The compiler lives in `../avatar-profile/scripts/compile-echo-key.mjs` and writes the
persona into the app. It reads **only** `sources/`, never `private/`.

## Rule
Nothing identifying or sensitive goes in `sources/` or anywhere committed: no contact info,
no account names, no biometric data, no private documents. A speaking style only. This repo is public.

Built by Garrett C. Gauthier. Compiled with Claude (Anthropic) in Claude Code.
