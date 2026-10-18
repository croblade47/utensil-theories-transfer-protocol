# Standing rules for any AI session working in this repository

## STRICT RULE: how files and artifacts are delivered to the owner
The owner must be able to find every file without searching. No exceptions.

1. **Real files, not links.** Every file or artifact you make goes to the owner as an actual file, sent with the file-sending tool (SendUserFile) so it appears on their screen in the app. A link, URL or bare path alone does not count.
2. **Real Word files.** Documents are true `.docx` files. Never a web page renamed `.doc`. Keep a `.md` or `.txt` copy only as an extra.
3. **One folder per delivery.** If there is more than one file, put them all in one folder named `<TOPIC>_<YYYY-MM-DD>`. Copy the files in; don't link them. Zip the folder and send the zip as well as the main doc.
4. **A master doc in every folder,** named `00_START_HERE_<topic>.docx`. In plain English, easy to read:
   - what the folder is;
   - a timeline of what was done;
   - technical details and breakdowns;
   - every file in the folder, with what it is, its path inside the folder, and where the original lives (branch and path).
5. **Commit and push the folder** to the repository too, so a copy survives after the cloud machine is deleted.
6. **Say plainly what you can't do.** A cloud session cannot place files on the owner's laptop desktop or phone home screen, or make desktop widgets. Send the files and say they need to be saved from the app. Never claim a file was placed somewhere it wasn't.

## Also read
- `experiments/HANDOFF.md`: the objective and drift guard.
- `experiments/COMMUNICATION_GUIDE.md`: how the owner communicates.
