const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  HeadingLevel, ShadingType, LevelFormat, AlignmentType, BorderStyle, Footer, PageNumber } = require('docx');

const OUT = process.argv[2];
const W = 9360; // content width, US Letter with 1" margins

const p = (text, opts = {}) => new Paragraph({ spacing: { after: 120 }, ...opts,
  children: Array.isArray(text) ? text : [new TextRun(text)] });
const b = (t) => new TextRun({ text: t, bold: true });
const t = (s) => new TextRun(s);
const h1 = (s) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 160 }, children: [new TextRun(s)] });
const h2 = (s) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 120 }, children: [new TextRun(s)] });
const bullet = (runs) => new Paragraph({ numbering: { reference: 'bul', level: 0 }, spacing: { after: 60 },
  children: typeof runs === 'string' ? [new TextRun(runs)] : runs });
const num = (runs, ref = 'num') => new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 80 },
  children: typeof runs === 'string' ? [new TextRun(runs)] : runs });

const border = { style: BorderStyle.SINGLE, size: 4, color: 'A0A0A0' };
const borders = { top: border, bottom: border, left: border, right: border };
function table(headers, rows, widths) {
  const mk = (txt, w, head, fill) => new TableCell({
    width: { size: w, type: WidthType.DXA }, borders,
    shading: head ? { type: ShadingType.CLEAR, fill: '1F3A5F', color: 'auto' } : (fill ? { type: ShadingType.CLEAR, fill, color: 'auto' } : undefined),
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: String(txt).split('\n').map(line => new Paragraph({ children: [new TextRun({ text: line, bold: head, color: head ? 'FFFFFF' : undefined, size: 18 })] })),
  });
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: headers.map((h, i) => mk(h, widths[i], true)) }),
      ...rows.map(r => {
        const flag = r[r.length - 1] && /PROBLEM|OVERSTATED/.test(r[r.length - 1]);
        return new TableRow({ children: r.map((c, i) => mk(c, widths[i], false, flag ? 'FDEDEC' : undefined)) });
      })],
  });
}
const gap = () => new Paragraph({ spacing: { after: 120 }, children: [] });

// ---------- content ----------
const timeline = [
  ['17 Oct 21:41', 'Previous session ("Human error encoding system") starts.', '-', ''],
  ['17 Oct 21:43', 'First script: a keyword detector that reads people\'s emotional "weight". Later dropped: the goal is the AI\'s understanding, not reading people.', 'd8ebeec\nresonance/', 'Off-goal start, corrected'],
  ['17 Oct 22:08', 'Experiments 1-4: a word-meaning model of the Bible. Color learned 10 of 14 (chance 17%). Rules alone were no better than stories.', 'ec22991\nbible_understanding.py', 'No pass/fail rules saved first; can\'t be checked from git'],
  ['17 Oct 22:16', 'Experiment 5: predict consequences in 20 new stories. Chance.', '939d60f', 'Failure, reported plainly'],
  ['17 Oct 22:42', 'Experiment 6: tiny transformer on the Bible. Learned the language, chance on consequences.', '1a4dfac\ntiny_transformer.py', 'Failure, reported plainly'],
  ['17 Oct 23:03-23:46', 'Experiment 7: the owner\'s shifting word (velanok). 68% vs 52% scrambled, on the same 20 pairs, 2 runs. Called "the first result above chance".', 'f676eed-c918cb7\nshifting_word.py', 'PROBLEM: no pass/fail rules first; 20 pairs only. Later shown to be luck'],
  ['18 Oct 00:52', 'Pass/fail rules saved for experiment 8 (100 new story pairs). Good practice starts here.', '5538b46\nconfirm.py', ''],
  ['18 Oct 01:03-02:21', 'Experiment 8 models score one by one. Judging is visibly strong in the early results.', 'results_confirm.json', ''],
  ['18 Oct 01:57-02:37', 'Aesop test rules drafted, then fixed twice, all before any training.', '87cccf9, 194fc7c, 910e9cb', 'Done right'],
  ['18 Oct 01:58-02:02', 'Communication guide, first handoff and plan written.', 'b58b583, cde3dac, 6143fa8', ''],
  ['18 Oct 02:17', 'Pass/fail rules saved for experiment 10, with judging as the main measure.', '6e365ef\nmethod_comparison.py', 'PROBLEM: 7 of 9 experiment-8 models had already shown judging was strong. Measure chosen after a peek'],
  ['18 Oct 02:35', 'Experiment 8 written up: consequences NOT confirmed (51/100; experiment 7 was luck). Judging 69 vs ~50, but only a side measure.', 'a5f1a6b', 'Honest result'],
  ['18 Oct 02:58', 'Scoring fix for the 3-spelling method, after the first experiment-10 model had scored.', 'ca1f8c9', 'Minor: the write-up says results for the 5-spelling methods were unchanged'],
  ['18 Oct 03:40', 'Aesop test (experiment 9) starts on the other machine. 16 models, about 6-8 hours.', 'aesop_test.py', 'Still running at audit time'],
  ['18 Oct 03:41', 'Experiment 10 written up: carry and plain label tie on short stories (68.7 vs 67.7).', '9c6fb86', 'Honest result'],
  ['18 Oct 03:44', 'Pass/fail rules saved for experiment 11 (long stories).', '99622d3\nlong_story_test.py', ''],
  ['18 Oct 03:45', 'Scoring changed: exact ties count as half right. Found after the first model scored 0/100.', 'c93f383', 'PROBLEM (mild): change after a result was seen'],
  ['18 Oct 03:51', 'Test design changed during run 1: stories made longer so the first marker is also out of view. First-run results were not kept.', '6fc220d', 'PROBLEM: design changed after peeking; evidence lost'],
  ['18 Oct 04:04', 'Experiment 11 written up: "L2 CONFIRMED". Carry 59 vs label 53 per 100, all 3 runs.', '01b9050', 'OVERSTATED: should be "supported once"'],
  ['18 Oct 04:10', 'Exploratory start-marker run: the carry model "carries perfectly but updates poorly".', '11982b6', 'Exploratory, labeled as such'],
  ['18 Oct 04:16', 'Accuracy pass by three review agents.', '226f68c', 'PROBLEM: missed the 03:45 / 03:51 changes'],
  ['18 Oct 04:17-05:4x', 'Aesop partial results pushed (7 of 16 models).', 'results_aesop.json', ''],
  ['18 Oct 05:47', 'Objective and "drift guard" added to the handoff. The owner restates the goal: communication.', '2b3d28e\nHANDOFF.md', 'Drift admitted, not yet acted on'],
  ['18 Oct 05:47-06:40', 'New session (this audit) re-checks every headline number against the raw files. Numbers match. Wording and timing problems found.', 'this folder', ''],
  ['Separate project, 18 Oct 02:51', 'A "Master Patent-Ready Theory" file for the zine project, made in another session.', 'f6f4c6e on branch ccr-4507ebbb-bfz236', 'PROBLEM: named .doc but is a web page, so many phone apps can\'t open it. Real .docx copy made here'],
];

const wrong = [
  ['Drift from the goal', 'All 11 experiments measure moral judging of Bible-style sentences in a 3.4-million-parameter model. None measures communication, and none uses a real-size AI.', 'HANDOFF.md, "Objective and drift guard"', 'Next step: a conversation test (does carried state keep a model true to what a person said early on?), with a large AI as the reader.'],
  ['Claim before proof (exp 7)', '68% on 20 pairs was announced as the first result above chance, with no pass/fail rules saved first. On 100 new pairs it was 51%: luck.', 'c918cb7, a5f1a6b, results_shifting_word.json, results_confirm.json', 'Already corrected in README. Rule: no headline without saved pass/fail rules.'],
  ['Main measure chosen after a peek (exp 10)', 'Judging became the main measure at 02:17, after most experiment-8 models had shown judging was strong.', '6e365ef vs commits 01:03-02:08', 'Say so in README. The judging claim needs a fresh test with judging as the main measure from the start.'],
  ['Test changed mid-run (exp 11)', 'Two changes at 03:45 and 03:51, after the first scores, and the first-run results were thrown away. "Confirmed" is too strong.', 'c93f383, 6fc220d, 01b9050', 'Call it "supported once". Repeat it on fresh stories at several distances.'],
  ['Same stories reused', 'Experiment 11 reused the same 100 story acts as experiments 8 and 10.', 'long_story_test.py (ITEMS_V2)', 'The fresh-story re-test fixes this.'],
  ['Hidden shape of the effect', '"+6 per 100" hides that the carry model gives no answer on about 65 of 100 pairs. When it answers, it is right 81 times, wrong 25.', 'results_long_story.json; 6_Number_Check output', 'Report both numbers.'],
  ['Wrong wording', 'README says the plain label is blind to the act "by design". It isn\'t: it writes its own markers too, which is how it scored 97 in one run.', 'README.md exp 11; long_story_test.py judge_marked()', 'Delete "by design" and explain.'],
  ['Headline without its caveat', 'HANDOFF opens with "Works:" for judging, but judging was never pre-registered as the main measure.', 'HANDOFF.md "In short"', 'Change to "strong and repeated, not yet pre-registered".'],
  ['Lost evidence', 'Marker diagnostics and the first experiment-11 run were never saved. Trained models and data aren\'t in git, so a fresh machine must retrain (about 2.5 hours for exp 8/10).', 'README exp 11; HANDOFF "Files"', 'Save every run, flawed ones included. Consider storing models outside git.'],
  ['Files hard to find or open', 'Results live on a side branch, not main. The zine master file is a web page named .doc. Nothing was sent as a downloadable file.', 'branches; 5_Other_Master_Files', 'This folder. Strict file rule added to CLAUDE.md.'],
  ['Missing tools', 'No API key, so the large-AI test was never run. Gutenberg and Archive.org were blocked. A new container has no torch or saved models.', 'HANDOFF "How to run"', 'Add an API key, or use helper AI copies as readers with blind, rule-based scoring.'],
  ['Review missed things', 'Three review agents (04:16) did not catch the mid-run test changes.', '226f68c', 'Reviewers should be given the git timeline, not just the write-ups.'],
];

const held = [
  ['Judging, short stories (exp 8/10)', 'Shifting word 67, 72, 67 (avg 68.7)\nPlain label 71, 69, 63 (67.7)\n3-spelling carry 66, 72, 74 (70.7)\nNo marker 49, 60, 40 (49.7)\nScrambled 56, 42, 60 (52.7)', 'Labeling right/wrong in training text: about 19 more right per 100 than plain text. Strong, repeated, not pre-registered as main measure.'],
  ['Shifting vs plain label, short (exp 10)', '20 better, 18 worse pairs (p = 0.44)', 'Tie. Matches the write-up.'],
  ['Shifting vs no marker / scrambled', '54-26 (p = 0.001) / 57-25 (p = 0.0003)', 'Matches the write-up.'],
  ['Long story, everyday act (exp 11, L2)', 'Shifting 59, 56, 63 vs label 54.5, 51, 54\n43 better, 21 worse (p = 0.004)', 'About 6 more right per 100. Supported once, not confirmed (see timeline).'],
  ['Long story, verdict stated (L1)', 'Label won 74 pairs, shifting 11', 'Failure for the carry idea. Reported plainly.'],
  ['Consequences (exp 5, 6, 8)', '51 per 100 in exp 8', 'Chance. Failure.'],
  ['Aesop (exp 9)', '7 of 16 models in results_aesop.json', 'Not analysed in this audit, so as not to peek before it finishes.'],
];

const specs = [
  ['Repository', 'github.com/croblade47/utensil-theories-transfer-protocol (private)'],
  ['Research branch', 'ccr-1be0d913-1tlzao (NOT on main). 34 research commits, 17 Oct 21:43 to 18 Oct 05:47 UTC, plus "partial results" commits.'],
  ['This folder in the repo', 'AUDIT_PACK_2026-10-18/ on branch ccr-1be0d913-audit-pack (kept separate so it can\'t clash with the running Aesop session).'],
  ['Software (reported by previous session)', 'Python 3.13.16, torch 2.14.1, numpy 2.5.3, 4 CPU cores. Exact seed reproduction needs these versions.'],
  ['Model', 'Small GPT-style transformer trained from scratch: 4 layers, 4 heads, width 192, window 64 tokens (Aesop: 128), dropout 0.1, tied embeddings, AdamW (weight decay 0.1) with one-cycle schedule, 1,500 steps. About 3.4 million parameters. Word-level tokenizer.'],
  ['Training text', 'King James Bible: 31,102 verses, about 793,000 words. Every 50th verse held out to check language learning.'],
  ['Shifting word settings', 'RESET = 17 on a clear right/wrong; SPEND = 0.5 per word toward zero; cap ±51; RECHARGE off. Five spellings: anoksha, oksharu, velanok (unresolved), sharuvel, ruvelan. Clear choices = Bible verdict phrases plus the 3% most strongly worded verses at each end (2,029 verses). Word values from a good/evil direction in a word-meaning model.'],
  ['Methods compared', 'baseline (no marker), scrambled (random spelling), shifting (carry, 5 spellings), label (per-verse only, no carry), carry3 (carry, 3 spellings). Seeds 0, 1, 2.'],
  ['Judging score', 'Marked models: the model writes its own marker after the story; the score is the probability-weighted lean of that marker. No-marker model: log-probability of the "right" phrase minus the "evil" phrase.'],
  ['Long-story setup (exp 11)', 'Act, then neutral filler sentences (max 10) until both the act and the first marker are outside the 64-token window. The model writes a marker after each sentence (greedy choice). Exact ties count as 0.5.'],
  ['Statistics', 'Pair-by-pair one-sided sign test (binomial), 3 runs summed per pair.'],
  ['Aesop test (exp 9)', '67 fables (none in training), 1,131 same-format pairs, 284 no-word-clue pairs. Training sets of about 700k tokens: folk tales (9 collections, 8 cultures), shuffled folk tales, novels (Austen, Chesterton, Melville), Bible. Pass/fail rules P1, P2, P2b, P3 in the aesop_test.py docstring.'],
  ['Not saved anywhere', 'experiments/data/ (re-downloads automatically) and experiments/models/ (must be retrained).'],
  ['Re-check the numbers', 'Run: python3 6_Number_Check/check_numbers.py. It reads the copies in 4_Raw_Results and should print exactly 6_Number_Check/check_numbers_output.txt.'],
];

const files = [
  ['00_START_HERE_Master_Audit.docx', 'This document.'],
  ['1_Prompt_for_Other_AI.docx / .md / .txt', 'Draft prompt to bring the running session back on track. For you to review and edit before sending. Same text in three formats.'],
  ['2_Research_Notes/HANDOFF (.docx, .md)', 'Previous session\'s summary of where things stand.'],
  ['2_Research_Notes/COMMUNICATION_GUIDE (.docx, .md)', 'How you explain things, and how an AI should translate them.'],
  ['2_Research_Notes/PLAN (.docx, .md)', 'Planned next steps.'],
  ['2_Research_Notes/README (.docx, .md)', 'Full write-up of every experiment.'],
  ['2_Research_Notes/PRIOR_WORK (.docx, .md)', 'Related published research, and what looks new.'],
  ['2_Research_Notes/NEXT_SESSION_PROMPT (.docx, .md)', 'Prompt used to start new sessions.'],
  ['3_Code/*.py', 'All experiment scripts (experiments 1-11), plus the early resonance engine in 3_Code/resonance/.'],
  ['4_Raw_Results/results_*.json, *.txt', 'Raw scores every claim is based on. results_aesop.json is partial (Aesop still running).'],
  ['5_Other_Master_Files/MASTER_PATENT_READY_THEORY.docx', 'Zine project master file, converted to a real Word file so it opens anywhere.'],
  ['5_Other_Master_Files/..._original_webpage.doc', 'The original file as made (a web page with a .doc name). Kept for the record.'],
  ['7_Strict_File_Rules (.docx, .md)', 'Your standing rules for every AI session: real files saved into the folder as they are made, never links, nothing locked or permission-blocked. Same text as CLAUDE.md at the top of the repo, which sessions read automatically.'],
  ['8_Build_Scripts/build_master_doc.js', 'The script that builds this master doc (run: node build_master_doc.js out.docx). Kept so anyone can rebuild or check it.'],
  ['6_Number_Check/check_numbers.py + output', 'Script that recomputes the headline numbers from the raw results, and what it printed.'],
];

const questions = [
  'Do the headline numbers in README.md match the raw files in 4_Raw_Results? (Run 6_Number_Check.)',
  'Compare the git timeline above with each claim. Was any pass/fail rule changed after results were seen, beyond the ones listed?',
  'Is "supported once" the right label for experiment 11, L2? Would you go weaker or stronger?',
  'Does the long-story test leak information other than the carried markers (for example story length, or the label model\'s own markers)?',
  'Which single next experiment would move closest to the real goal: better communication by a real-size AI?',
  'Is anything in the write-ups stated more strongly than the numbers allow?',
];

// ---------- document ----------
const children = [
  new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun('Audit Pack: Comprehension Research')] }),
  p([t('Built 18 October 2026 by a Claude Code session (a second AI checking the first). Ideas and direction: Garrett Gauthier. Code and experiments: built with Claude.')]),
  p([b('Start here. '), t('This folder holds actual copies of every file, not links. Everything a reviewer (you or another AI) needs is inside it.')]),

  h1('1. The short answer'),
  bullet([b('Goal: '), t('make an AI understand people better, so it communicates better.')]),
  bullet([b('How close: '), t('about rung 1 of 5. Two small signs of better understanding inside a very small model. Communication has not been tested, and nothing has been tried on a real-size AI.')]),
  bullet([b('Numbers: '), t('all headline numbers match the raw results files.')]),
  bullet([b('Problems: '), t('some wording is stronger than the evidence. One test was changed after a peek. The work drifted toward the measuring tool and away from the goal.')]),

  h1('2. Timeline (UTC; rows shaded red are problems)'),
  p('Commit codes (like 6fc220d) can be looked up in the repository to see exactly what changed and when.'),
  table(['When', 'What happened', 'File / commit', 'Verdict'], timeline, [1400, 4160, 1800, 2000]),

  h1('3. What went wrong, and the fix'),
  table(['Problem', 'What happened', 'Evidence', 'Fix'], wrong, [1600, 3360, 2000, 2400]),

  h1('4. What held up (re-checked from raw files)'),
  table(['Test', 'Raw numbers (per 100 pairs)', 'Plain meaning'], held, [2300, 3400, 3660]),
  p([t('Scale caveat: these are results in a 3.4-million-parameter model trained on one book. They do not change how a large AI like Claude understands anyone.')], { spacing: { before: 160, after: 120 } }),

  h1('5. Technical details for reviewers'),
  table(['Item', 'Detail'], specs, [2400, 6960]),

  h1('6. Every file in this folder'),
  p('Paths are relative to the AUDIT_PACK_2026-10-18 folder. The same folder is in the repository on branch ccr-1be0d913-audit-pack.'),
  table(['File (path in this folder)', 'What it is'], files, [3800, 5560]),
  h2('Where the originals live'),
  bullet([b('Research files: '), t('branch ccr-1be0d913-1tlzao, folders experiments/ and resonance/.')]),
  bullet([b('Zine master file: '), t('branch ccr-4507ebbb-bfz236, file MASTER_PATENT_READY_THEORY.doc.')]),
  bullet([b('Where this pack was built: '), t('/home/user/utensil-theories-transfer-protocol/AUDIT_PACK_2026-10-18 in a temporary cloud machine. That machine is deleted later, so the repository and your downloaded copy are the lasting ones.')]),

  h1('7. Questions to give another AI reviewer'),
  ...questions.map(q => num(q)),
  p('Give the reviewer the whole folder, and ask it to cite file names and commit codes for every claim it makes.', { spacing: { before: 160 } }),
];

const doc = new Document({
  creator: 'Claude Code', title: 'Audit Pack: Comprehension Research',
  styles: {
    default: { document: { run: { font: 'Calibri', size: 21 } } },
    paragraphStyles: [
      { id: 'Title', name: 'Title', basedOn: 'Normal', run: { size: 40, bold: true, color: '1F3A5F' }, paragraph: { spacing: { after: 200 } } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 30, bold: true, color: '1F3A5F' }, paragraph: { outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 24, bold: true, color: '333333' }, paragraph: { outlineLevel: 1 } },
    ],
  },
  numbering: { config: [
    { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
    { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: 'Audit Pack 2026-10-18 - page ', size: 16 }), new TextRun({ children: [PageNumber.CURRENT], size: 16 })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log('wrote', OUT); });
