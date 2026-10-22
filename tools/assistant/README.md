# Project assistant

Garrett C. Gauthier is the owner and sole author of this project and its ideas. This assistant was built with Claude (Anthropic) in Claude Code, a tool used by the owner.

**What it is:** a small set of tools that let any session answer questions about this project quickly, with a source for every answer. The owner asked for it on 22 Oct 2026: "build yourself an assistant so you can answer quickly and be confident in the data also".

## The parts
| File | What it does |
|---|---|
| `facts.py` | Recomputes every headline result from the raw files in `experiments/`, reads key dates from git, and checks each handoff claim against the raw data (MATCH or DIFFERS). |
| `transcripts.py` | Builds an exact index of every session transcript: owner messages (numbered, full text), replies and final replies, and keeps them apart from hook feedback, task notices and messages relayed by other sessions. Search, list and show any turn. |
| `cursor.py` | Shows where a saved transcript page ends, so the next page can be fetched. |
| `../../.claude/agents/project-assistant.md` | The agent definition. Sessions on this repository can call it as the "project-assistant" subagent. |

## Quick use
```
python3 tools/assistant/facts.py
python3 tools/assistant/transcripts.py search "Trinity" owner
```

## Fetching transcripts (needed once per new session)
The transcript cache lives outside the repository, because transcripts hold personal details and the repository is public.

1. List sessions with the `list_sessions` tool (claude-code-remote).
2. For each session, call `list_events` with `limit` 100 and **no** `kinds` filter. Full pages are too large to show, so the tool saves each one to a file and prints its path.
3. Copy each saved page to `<pages>/<session id>/page_NNNN.txt`. Then run `python3 cursor.py <that file>` to get `last_id` and `first_id`.
4. Page forward with `after_id = last_id`, or backward from the newest page with `before_id = first_id`, until `has_more` is missing.
5. Build the index: `python3 transcripts.py build <pages> [cache]`.

The index sorts every page by time and drops repeated events, so the order you fetch in doesn't matter.

## What it does not do
- It does not read tool output (code runs, file contents) word for word. That work is kept in git, and `facts.py` reads the results files directly.
- It cannot see sessions or chats outside this account's Claude Code sessions (for example Gemini or Copilot chats), unless the owner adds them as files.
