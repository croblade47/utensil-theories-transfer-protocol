# START HERE: MeAgent (22 October 2026)

## What this folder is
**MeAgent** is a PowerShell script for Windows. It slowly learns how you use your PC and then tries to guess what you will do next, just for fun. Garrett C. Gauthier is the owner and author. It was written with Claude (Anthropic) in Claude Code, a tool the owner uses.

## What it learns
- **Apps:** which app is in front and for how long, one row per session.
- **When you're on the device:** time per hour of the day. After 2 minutes with no mouse or keyboard input it counts you as "idle".
- **Typing speed:** keys per minute and words per minute, plus your fastest minute.
- **Vocabulary:** how often you type each word. It keeps **counts only, never the order** of what you typed.
- **Workflow:** which app usually follows which, overall and for each hour of the day.
- **Predictions:** every time you switch apps, it shows its guess for your next app and keeps score of how often it's right.

## How to use it
1. Copy `MeAgent.ps1` to your PC, for example into `Documents`.
2. Open PowerShell in that folder and run:
   `powershell -ExecutionPolicy Bypass -File .\MeAgent.ps1`
3. Leave the window open; it learns while it runs. Close the window, or press Ctrl+C, to stop. It saves every minute and again when it stops.
4. To see what it has learned, and its guess for right now:
   `powershell -ExecutionPolicy Bypass -File .\MeAgent.ps1 -Report`

Other options:

| Option | What it does |
|---|---|
| `-NoVocab` | Learn everything except words |
| `-Install` | Start automatically (minimized in the taskbar) whenever you sign in |
| `-Uninstall` | Stop starting automatically |
| `-Forget` | Delete everything it has learned (asks you to type YES) |
| `-IdleSeconds 300` | Count you as away after 5 minutes instead of 2 |

## Privacy (built in)
- **Everything stays on your PC,** in `%USERPROFILE%\MeAgent` (`state.json`, `sessions.csv`, `typing.csv`). The script makes no network connections.
- **No words are recorded in private windows:** while a password manager is in front, or the window title contains words like password, sign in, login, bank, payment, checkout, credential, verification code, incognito or InPrivate.
- **Digits are never recorded** as words. The script never reads the screen or the clipboard.
- **It runs in a visible window.** It never hides itself.
- **Limit:** it can't see inside every app. A password typed in a window whose title doesn't look private can still count as a word. If you type passwords often, use `-NoVocab`.

## Technical details
- **Reading the PC:** it uses standard Windows functions: the window in front, the process that owns it, the time since your last input, and key up/down state, checked about every 30 ms.
- **Prediction:** "after app A comes app B" counts, with double weight for the current hour of the day. The most likely next app is shown with its percentage.
- **Words per minute** is keys divided by 5, the usual typing measure. Only minutes with some typing count toward the average.
- **Requirements:** Windows PowerShell 5.1 (built into Windows 10 and 11) or PowerShell 7. No installs needed.
- **Not tested on Windows yet.** It was written in a Linux cloud session with no PowerShell to run it. If it shows an error, send the error text and it can be fixed.

## Timeline
- 22 Oct 2026: the owner asked for an agent that learns their behaviour, workflow, vocabulary, typing speed and device time, and predicts what they'll do next. The script and this guide were written.

## Every file in this folder
| File | What it is | Where the original lives |
|---|---|---|
| `00_START_HERE_MeAgent.docx` / `.md` | This guide | branch `ccr-1be0d913-1tlzao`, `ME_AGENT_2026-10-22/` |
| `MeAgent.ps1` | The script | same folder |
| `ME_AGENT_2026-10-22.zip` (next to the folder) | This folder as a plain zip | repository top level |

## Things outside this folder's control
- **The repository is public:** anyone can read the script. That's fine, since it holds no data. Your learned data stays only on your PC.
- **A cloud session can't install anything on your PC.** Copy the script over yourself.
