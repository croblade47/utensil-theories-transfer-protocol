# Standing rules for any AI session working in this repository

## STRICT RULE 1: every file is a real file, saved into the folder as it is made
The owner must be able to find, open, review and share every file without searching and without being stopped. No exceptions.

1. **Save as you go.** Every file or artifact you generate goes into the current delivery folder **the moment it is created**, not at the end of the task. This covers documents, code, results, logs, charts, prompts and drafts. Name the folder `<TOPIC>_<YYYY-MM-DD>`, at the top of the repository.
2. **Actual files, never links.** Copy the real file into the folder. A link, URL, shortcut, symlink or bare path is not a substitute. If a file lives somewhere else (another branch, a published artifact, a cloud doc), put a full copy in the folder.
3. **Send each finished file to the owner** with the file-sending tool (SendUserFile), so it appears on their screen in the app. Re-send the folder zip whenever its contents change meaningfully.
4. **Real Word files.** Documents are true `.docx` files. Never a web page renamed `.doc`. Keep a `.md` or `.txt` copy as an extra.
5. **One folder per delivery, plus a zip.** If there is more than one file, keep them together in the folder. Zip the folder and send the zip along with the master doc.
6. **A master doc in every folder,** named `00_START_HERE_<topic>.docx`. In plain English, easy to read:
   - what the folder is;
   - a timeline of what was done;
   - technical details and breakdowns;
   - every file in the folder, with what it is, its path inside the folder, and where the original lives (branch and path).
   Update it each time a file is added.
7. **Commit and push the folder** to the repository after each step, so a copy survives after the cloud machine is deleted. If the main working branch is busy (another session is pushing to it), push to a separate branch and say which one.

## STRICT RULE 2: nothing locked, nothing permission-blocked
The owner decides what to review and who to share with. Never put anything in their way.
1. **No locks of any kind:** no passwords, no encrypted zips, no read-only or restricted flags, no DRM, no expiring links, no "confidential, do not share" labels.
2. **Open permissions.** Files are readable and writable by the owner (for example `chmod 644`). Zips are plain, unencrypted archives.
3. **Open formats** that work on a phone and a laptop without special software: `.docx`, `.pdf`, `.txt`, `.md`, `.csv`, `.json`, `.zip`, `.py`.
4. **Never hold a file back** from the owner, never deliver only a preview of it, and never require extra sign-ups or approvals to open it.
5. **Say plainly what you can't control,** instead of implying it's handled. For example:
   - the repository is public on GitHub (MIT license): anyone can read it. Changing that is the owner's decision, made in GitHub settings;
   - a cloud session cannot place files on the owner's laptop desktop or phone home screen, or make widgets. Send the files so the owner can save them.
   Never claim a file was placed somewhere it wasn't.

## Also read
- `experiments/HANDOFF.md`: the objective and drift guard.
- `experiments/COMMUNICATION_GUIDE.md`: how the owner communicates.
