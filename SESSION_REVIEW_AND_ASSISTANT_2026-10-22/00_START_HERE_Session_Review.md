# START HERE: Session Review and Project Assistant (22 October 2026)

Garrett C. Gauthier is the owner and sole author of this project and its ideas. This folder was put together with Claude (Anthropic) in Claude Code, a tool used by the owner.

## What this folder is
The owner asked: "Suggest what is next and review where the other instances are and compare our progress against theirs. Be sure to read everything word for word. I would suggest building an agent or bot for your own update."

**Status: done.** The assistant is built and tested, and every session has been compared. The next steps are proposals; nothing has been started.

## Timeline (22 Oct, UTC)
- Listed every Claude Code session on the account: 6 in all, and only this one is running.
- Downloaded every transcript page to a private cache (not the repository): all 6 sessions, 878 indexed entries.
- Read word for word: all 83 owner messages in the research session, and every message and reply in the audit session and the three small sessions.
- Found two unanswered requests: the '+4' review (21 Oct, messages 50-55, blocked 5 times by a safety check) and 'Where is an app key' (21 Oct).
- Wrote the comparison and next steps (`1_Sessions_Compared_and_Next`).
- Built the project assistant (`assistant/`): a fact checker, a transcript index and an agent definition.
- Ran the fact checker: 13 handoff claims checked against the raw results, 0 differ.

## Files
| File (path in this folder) | What it is | Original |
|---|---|---|
| `00_START_HERE_Session_Review.docx` / `.md` | This guide | here (branch `ccr-1be0d913-1tlzao`) |
| `1_Sessions_Compared_and_Next.docx` / `.md` | Every session side by side, what was found only by reading every word, and the proposed next steps | here |
| `2_Fact_Check_Output.txt` | Output of the fact checker: every headline number from the raw files, with sources, and the claim checks | made by `tools/assistant/facts.py` |
| `assistant/facts.py` | Fact checker | `tools/assistant/facts.py` |
| `assistant/transcripts.py` | Exact transcript index (owner messages, replies, final replies) | `tools/assistant/transcripts.py` |
| `assistant/cursor.py` | Helper for downloading transcript pages | `tools/assistant/cursor.py` |
| `assistant/README.md` | How to use the assistant | `tools/assistant/README.md` |
| `assistant/project-assistant_agent.md` | The agent definition | `.claude/agents/project-assistant.md` |

## Outside this folder's control
- The repository is public. Transcript text and personal details stay in the private cache on this cloud machine, which is deleted when the session ends. The tools can rebuild the cache in any new session.
