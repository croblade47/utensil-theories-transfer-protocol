# START HERE: Project Record (21 October 2026)

## What this folder is
A full record of the project from 17 to 21 October 2026, written for the owner to keep and review later. The owner asked for it on 21 October: "Include as much as you can from beginning to end, changes, adaption, any kind of information you think I'll need, just for later review and a record for myself."

It covers:
- the goal;
- a day-by-day timeline of every request and what was done;
- the owner's ideas in their own words;
- every experiment and its result;
- every change, fix and mistake;
- the tests across other AIs;
- what already exists in research;
- where things stand, every file, how to reproduce the work, and a glossary.

The same report comes in four formats, so it opens anywhere (phone or laptop):
- **PDF** (`Project_Record_2026-10-21.pdf`), with clickable bookmarks;
- **Word** (`.docx`);
- **Markdown** (`.md`), the master copy;
- **plain text** (`.txt`).

## Timeline of what was done
1. **21 Oct, 02:15 UTC:** the owner asked for the report by email as a PDF, with text and Markdown copies.
2. **02:16:** the sources were gathered:
   - all 59 owner messages so far, with times;
   - the AI's 281 replies;
   - all 119 commits;
   - every results file and delivery folder.
3. **02:17 onward:** five writers (AI agents) each drafted part of the report from those sources. The session's usage limit stopped them twice; they finished at 13:21 UTC.
4. **17:50:** the sections were assembled in order (`code/assemble_report.py`), with a one-page short version and the events after the drafts were written.
5. **Checks:** a privacy and tone editor removed personal details, because the repository is public. A fact checker then verified numbers, dates and commit hashes against the sources. Their change logs are in `checks/`.
6. **Built** into PDF, Word and text (`code/build_outputs.py`), emailed to the owner, sent in the app, and committed.

## Technical details
- **Email limits:** the email tool takes attachments only as text pasted into the send request. So the emailed PDF is split into parts small enough to send one at a time (`email_parts/`). The full single PDF is in this folder and was also sent in the app.
- **PDF:** built with ReportLab's standard fonts (nothing embedded) and maximum compression, to keep files small.
- **Privacy:** personal details from the owner's messages and uploaded documents are left out or summarized in one neutral line. The owner keeps the originals.

## Every file in this folder

| File (path inside this folder) | What it is | Where the original lives |
|---|---|---|
| `00_START_HERE_Project_Record.docx` / `.md` | This guide (Word file, plus a text copy) | branch `ccr-1be0d913-1tlzao`, `PROJECT_RECORD_2026-10-21/` |
| `Project_Record_2026-10-21.md` | The report, master copy (Markdown) | here |
| `Project_Record_2026-10-21.pdf` | The report as one PDF, with bookmarks | made from the `.md` |
| `Project_Record_2026-10-21.docx` | The report as a Word file | made from the `.md` |
| `Project_Record_2026-10-21.txt` | The report as plain text | made from the `.md` |
| `email_parts/Project_Record_part_K_of_N.pdf` | The report split into small PDFs, as emailed | made from the `.md` |
| `checks/privacy_and_fact_checks.md` | Every change the privacy and fact checkers made, and why | made in this session; only here |
| `code/assemble_report.py` | Puts the section drafts in order and adds the short version and later events | made in this session; only here |
| `code/build_outputs.py`, `code/md2pdf.py` | Build the PDF, Word, text and email parts from the Markdown | made in this session; only here |
| `Project_Record_2026-10-21.zip` (next to the folder) | This whole folder as a plain zip | repository top level |

## Things outside this folder's control
- **The repository is public** on GitHub (MIT license): anyone can read these files. Changing that is the owner's decision, in GitHub settings.
- **A cloud session can't place files on your devices.** The files are sent to you in the app and by email for you to save.
- **Scale:** every result in the report comes from tiny models. None of it changes how a large AI like Claude understands anyone.
