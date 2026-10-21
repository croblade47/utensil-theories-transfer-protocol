# Numbers test: how the owner's notation was read, and the final design

Made on 20 October 2026 by three independent readers and one judge (AI agents), before any model was trained.
The judge's design is what `numbers_test.py` implements. Kept here word for word as the readers and the judge wrote it, except that "he/his" for the owner was changed to "they/their" (the owner's pronouns were never stated).

## Reader 1: the owner's own rules

**Confidence:** medium

**Reading.** The owner's day-1 rule describes a bank with a direction. It is not a balance that keeps adding. Here is the trace, rebuilt from their own arithmetic.

(1) The word emerges with a charge: w1 = 17.
(2) The words after it spend that charge: a word "equal to (-13)" leaves 17 - 13 = 4 Remaining.
(3) At the next emergence a fresh charge goes on top of what remains: W1 = 17 + 4 = 21.
(4) The words after that spend it again. "(00) = 0 Remaining" only adds up if those two words use all 21, so the bank empties and stops at 0 rather than going negative.
(5) The next emergence is "{w1=17 -<next...>", i.e. 17 + 0. The charge is added again even when nothing remains, so the direction must be stored separately from the amount.
(6) A clear wrong or right choice wipes the remaining ("reset to [w1=0]") and starts the sequence again at -17 or +17. That sets the direction.

The token is chosen from "a Remaining value from the previous use of it". It is not chosen from the charge. The owner's own notation shows this: w1 (nothing remaining) becomes W1 (4 remaining) and then w1 again (0 remaining). This case change is a hint only; it could be a typo.

This explains why the old RECHARGE option pinned at the cap. It read the spelling off the recharged balance, which was always 17 or more, so the spelling was always heavy. It also spent only 0.5 per valued word, about 5.5 per verse, against a 17-per-verse recharge.

Measured on the KJV with SCALE 30: a verse has about 10.9 valued words, mean |value| 1.68, and the summed |value| per verse averages 18.3 (median 16). Under the spend rule below, a verse therefore uses up about 17. So 16 and 17 balance: the bank fills and empties. 32, 34 and 47 overcharge it, and it stays full.

Today's notation reads as: put the five numbers, in their order, into the charge slot N of W1 = N + Remaining. The trailing comma in "47," shows the list continuing. "47, = 17+4" reads as: after 47 the sequence comes back to 17 with the remaining carried, so it rotates. The zero symbols happen to match the states this bank has:
- ?0 = no direction yet (velanok);
- -0 = wrong direction with nothing carried;
- +0 = right direction with nothing carried;
- 00 = the day-1 floor ("used up, 0 remaining").
That match is a consistency check only. The zero symbols do not drive the design.

Size and order are separate questions. A single number acts only through its ratio to the per-verse spend, and SCALE = 30 was an AI choice. So a single number cannot be tested apart from SCALE, but the order and ratios of the sequence can be.

**Symbol by symbol.** - "17,32,16,34": quoted as one group, the first four of the owner's sequence, in order. Reading: the charges N at successive emergences, in the place of 17 in W1 = N + Remaining. Structure noted but not used: a, 2b, b, 2a with a = 17 and b = 16 (17↔34 and 16↔32 are crossed doublings, a mirror like the seed expression).
- ?0 = the undetermined zero: reset to w1 = 0 at book start, no direction yet. Token: velanok.
- -0 = wrong direction with zero remaining. Token: plain wrong form (oksharu, "w1").
- +0 = right direction with zero remaining. Token: plain right form (sharuvel, "w1").
- 00 = the day-1 "(00) = 0 Remaining": the following words used the charge up, and the bank stops at 0 instead of going negative.
- The chain of "=" signs: every charge is eventually spent to one of these zero states. Hint only.
- 47 (written "47," inside [ ]): the fifth number, continuing the list, placed in a day-1-style bracket.
- = "17+4": 47 sits where "17+4" sat in [W1=17+4 ...]. So the numbers belong in the charge slot of W1 = N + Remaining. After 47 the next emergence is 17 plus whatever remains (the "+4"), so the sequence rotates and carries its remainder across the wrap.

**Configurations proposed:**

- **bank17**
  - Rule: New script (for example experiments/remaining_bank.py). It imports word_values, CLEAR_WRONG, CLEAR_RIGHT, CLEAR_PCT and FORMS from shifting_word.py and leaves that file untouched. Clear choices (clear in {-1,0,+1}) and word values (SCALE 30) are computed exactly as in mark_up.

State: d in {-1,0,+1}, R >= 0 (float), k = number of charged emergences since the last clear choice. At each book start: d = 0, R = 0, k = 0.

At each verse:
(1) EMERGE: write the form before reading the verse. d == 0 gives velanok. d = +1 gives ruvelan if R >= 4, else sharuvel. d = -1 gives anoksha if R >= 4, else oksharu.
(2) If clear != 0: set d = clear, R = 0, k = 0, spend nothing, and go to the next verse.
(3) If d == 0: do nothing.
(4) Otherwise: N = charge(k); k += 1; W = N + R. For each valued word v in order: W = max(0, W - 2*max(0, -d*v)). This is exactly the existing per-word loop with SPEND replaced by |v| for that word: agreeing words are free, opposing words cost 2|v|, and the bank never crosses 0.
(5) R = min(W, N): at most one charge carries over, so W <= 2N.

Delete RECHARGE and the ±3*RESET clip. For bank17, charge(k) = 17 always. Keep the same 5 FORMS, so POSITION, score(), long_story_test and understanding_compression work unchanged. Save models as models/bank17_seed{0,1,2}_steps1500.pt.
  - Owner basis: [w1=17 -<next word (-13)> = +4 Remaining] → [W1=17+4 -<next 2 words (00)> = 0 Remaining] → {w1=17-<next...>}; "the token used to interpret it based a Remaining value from the previous use of it"; "reset to [w1=0] ... If wrong the sequence will begin with a value of (-17) and right (+17)". The +4 cut matches the owner's first remainder.
  - Prediction: This is the owner's never-tested remaining rule, built so it does not pin. Simulated spelling shares (scratch run, no training): anoksha 31%, oksharu 18%, velanok 5%, sharuvel 14%, ruvelan 32%. The marker changes on 26% of consecutive verses, against 42% for the current shifting word and 2% for RECHARGE as coded. Among verses with a direction, R is 0 on 29%, at the cap on 41%, and in between on 30%, so it stays responsive.

If the owner is right, it should match or beat shifting (68.7%) and label (67.7%) on judging the 100 pairs. It should do best on long-story B (everyday act), because the direction never fades to velanok while heavy and plain still change with each verse, which addresses 'carries perfectly but updates poorly'.

Risk: its marker follows the next verse's lean less closely than the current shifting word (correlation 0.19 vs 0.28 in simulation), so judging could drop slightly.
- **seq_rot**
  - Rule: Identical to bank17 except charge(k) = [17, 32, 16, 34, 47][k % 5]. k restarts at 0 on every clear choice, so the sequence always begins at 17. After 47 it wraps to 17 with R carried ('47, = 17+4'). The cap uses that emergence's charge: R = min(W, charge(k)). Models: models/seq_rot_seed{s}_steps1500.pt.
  - Owner basis: Today's "17,32,16,34 ... [47, = 17+4]" with the clarification that the +4 points to where they belong (the charge slot of W1 = N + Remaining). Also "those numbers in that sequence" and day-1 "syllables rotation sequence".
  - Prediction: These are the owner's literal sizes. The mean charge is 29.2 against about 18 spent per verse, so the bank is full on about 77% of verses with a direction (simulated: anoksha 42%, oksharu 7%, velanok 5%, sharuvel 6%, ruvelan 40%). The marker becomes mostly a sticky direction label. If the large numbers belong as the charge, seq_rot should beat bank17. Expected instead: judging like label/carry3 (about 68-71%), carry over distance as good or better, and updating poorer than bank17.
- **seq_rot_norm**
  - Rule: Identical to seq_rot except the charges are rescaled so their mean is the owner's base 17: charge(k) = [9.90, 18.63, 9.32, 19.79, 27.36][k % 5] (= n*17/29.2). Same wrap and restart on each clear choice. The cap is R = min(W, charge(k)). Models: models/seq_rot_norm_seed{s}_steps1500.pt.
  - Owner basis: Same words as seq_rot. It keeps the owner's order and ratios at a size that balances the text's spend. Only the charge-to-spend ratio matters, and SCALE = 30 was an AI choice, not the owner's.
  - Prediction: Stays balanced (simulated: anoksha 29%, oksharu 20%, velanok 5%, sharuvel 17%, ruvelan 30%; changes on 28% of verses). It differs from bank17's marker on 11% of verses. If the sequence's shape matters (weak, strong, weak, strong, strongest emergences after a verdict), it should beat bank17. Otherwise it ties.
- **seq_rot_norm_rev**
  - Rule: Identical to seq_rot_norm with the order reversed: charge(k) = [27.36, 19.79, 9.32, 18.63, 9.90][k % 5]. Models: models/seq_rot_norm_rev_seed{s}_steps1500.pt.
  - Owner basis: Control for the owner's specific claim that the numbers matter "in that sequence" (17, 32, 16, 34, 47).
  - Prediction: Same numbers and same mean; only the order changes. Its marker differs from seq_rot_norm on 14% of verses, so a real order effect could show. The owner's claim predicts seq_rot_norm > seq_rot_norm_rev. My prediction is no detectable difference. In simulation the reversed order even follows the text slightly more (0.417 vs 0.388).
- **bank47**
  - Rule: Identical to bank17 with charge(k) = 47 at every emergence, cap R = min(W, 47). Models: models/bank47_seed{s}_steps1500.pt. Optional: it stands for 32, 34 and 47 as single numbers (all give the same regime in simulation), and its marker differs from seq_rot's on only 6.5% of verses.
  - Owner basis: "the +4 was a way to direct you to a way to try testing the numbers where I feel like they belong": a single owner number in place of 17. 47 is the one placed in the "17+4" slot today.
  - Prediction: Overcharged: R is at the cap on 85% of verses with a direction (anoksha 45%, oksharu 3%, velanok 5%, sharuvel 3%, ruvelan 43%), so it acts as a sticky direction label. It tests whether a large single charge (longer memory, little updating) beats the balanced 17. Expected: about equal to seq_rot, and no better than bank17 or label on judging. Drop it first if the budget is tight.

**Ambiguities.** 1. Rule 2's "(00) = 0" only adds up if the two words spend 21. I read it as "used up, stops at 0". If it instead means two zero-valued words, then neutral words would drain the remaining (17 + 4 - 0 - 0 should be 21, not 0), which would argue for a fixed drain per word.

2. The spend rule is my choice. bank17 uses the signed spend (agreeing words free, opposing words cost 2|v|), which is the existing loop with SPEND = |v|. The pure-magnitude spend (every valued word costs |v|) is more literal: it reproduces 17 - 13 = 4 with |v| = 13. But it carries less moral signal (simulated correlation with the last 3 verses: 0.30 vs 0.40). A 6th config, bank17_costA, is possible.

3. The cap R <= N is my addition. Without it, R exceeds 51 on 36% of directed verses and the marker updates poorly. The alternative is the existing ±51 cap.

4. The reset sets R = 0, which is faithful to "reset to [w1=0]". So the first marker after a verdict is the plain directional form, and it turns heavy only after a verse confirms it. Setting R = N instead shows the heavy form at once, as the current code does (simulated correlation 0.47).

5. At book start d = 0, so there is no charge until the first clear choice (gap between clear verses: median 7, mean 15).

6. The w1 → W1 → w1 case change may be a typo.

7. "47 = 17+4" could also mean a two-tier charge: 17 when nothing remains, 47 when something does. That is untested here.

8. 17 and 16 sitting near the per-verse spend (18.3) is a coincidence of SCALE = 30, so it is not evidence for the numbers.

9. In the bank, the heavy form means "carried", not "strong". Judge scores stay sign-valid, but form magnitudes mean something different from the existing methods.

10. word_values and the 3% cut-offs are computed on all verses, including held-out ones. Keep them identical for comparison, but flag this for exp 12.

The scratch simulations (no repo files edited) are /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/owner_numbers_lens/sim3.py, sim2.py and sim.py; data.pkl in the same folder is cached data they read.

## Reader 2: the numbers themselves

**Confidence:** medium

**Reading.** The owner isn't giving a formula. They are pointing at a place in their own rule. Two things are firm. (1) The numbers come in a fixed order: 17, 32, 16, 34, 47. (2) The "+4" shows where they go: into the slot of 17 in their day-1 rule "W1 = 17 + 4 Remaining". So each number is the charge the word gets at one of its appearances, and whatever was left over last time (the Remaining) is carried on top. Their day-1 sentence says "if wrong the sequence will begin with a value of (-17) and right (+17)". Read together, the most literal meaning is: a clear right or wrong wipes the word to 0 and restarts it at ±17. At each later appearance it receives ±32, then ±16, ±34, ±47, then the cycle repeats (a rotation, "rather than a logical" order). Each charge is added to the Remaining left by the text since the previous appearance. The run continues ("for long periods") until the next clear verdict. The zero symbols are probably names for the states the Remaining can be in between charges: ?0 = zero with no verdict yet, -0 / +0 = zero inside a wrong / right run, 00 = the full wipe to w1 = 0 (the same "(00)" as day 1, where the following words cancelled everything). The bracket ["47" = "17+4"] says 47 takes the place where "17+4" stood. Arithmetically, 47 = 17 + (17+13) is the exact twin of 21 = 17 + (17-13): it is the owner's own example with the next word agreeing (+13) instead of opposing (-13). Counting in 17s, 47 is 4 below a multiple of 17 and 21 is 4 above one (47 ≡ -4, 21 ≡ +4 mod 17), a signed pair. That bracket reading may be a coincidence. Only the order and the charge slot should drive the design.

**Symbol by symbol.** "17,32,16,34" = the charges in order. 17 is the restart value after a verdict ("the sequence will begin with ±17"). 32, 16, 34 are the charges at the next appearances. Structure: 16 = 2^4, 32 = 2^5, 17 = 16+1 (a Fermat prime), 34 = 2×17 = 32+2. So the four numbers are {x, 2y, y, 2x} with x = 17 and y = 16: the outer pair doubles (17…34) and the inner pair halves (32…16). That is a mirror ordering; in binary, doubling is a one-bit shift (10001, 100000, 10000, 100010). Counting in 17s (mod 17) they read 0, -2, -1, 0, so 17 and 34 = 17+17 are "zeros" and 16 and 32 sit just below one. Step differences: +15, -16, +18, +13.
/ "?0" = zero Remaining with no verdict yet (sign unknown). Hint only.
/ "-0" = zero Remaining inside a wrong (-) run. Hint only.
/ "+0" = zero Remaining inside a right (+) run. Hint only. In the configs below, 83-89% of neutral-spelled markers fall inside a verdict run, so these signed zeros are real states of the rule. Giving them their own spellings would need new words: the 5 rotations of sha-ru-vel-an-ok are all used.
/ "00" = the full wipe to w1 = 0, as in day 1's "next 2 words (00) = 0 Remaining", after which the word restarts at 17. Also 34 = 17+17 is a double zero mod 17. Hint only.
/ "47" = the fifth charge. 47 is prime. 47 = 3×17 - 4 = 51 - 4: the existing cap 51 minus the owner's 4, so a charge of 47 on a Remaining of +4 lands exactly on today's cap. 47 = 34 + 13. 47 = 64 - 17, which is -17 in 6-bit two's complement. 47 ≡ 21 (mod 13).
/ "17+4" = 21, the owner's recharged value (W = 17 + Remaining 4). [47 = 17+4]: 47 takes that place. 21 + 47 = 68 = 4×17, so the two are mirror images about 34 (34 ∓ 13). They are the two outcomes of one recharge step when the next word is -13 or +13. Coincidences not to trust: ASCII 32/34/47 = space, ", /; perplexity 31.8 ≈ 32; 13.08 bits/word ≈ 13; SCALE 30 = 47 - 17; 47 - 21 = 26; 64 = CTX. With five small numbers and +, -, ×2 and mod, almost any target can be hit.

**Configurations proposed:**

- **numseq**
  - Rule: New marking function plus new model names; shifting_word.py globals are not edited. Constants: SEQ = (17, 32, 16, 34, 47); RESET = 17; CAP = 51; Q = 4/21; NBAR = mean number of valued tokens (w in values) per verse (10.90 on the KJV); DRAIN = 1 - Q**(1/NBAR) = 0.1411 per valued word; linear SPEND removed (0). State, reset at each book start as now: R = 0.0, s = 0, k = 0, W = 0.0. emerge(): form = form_for(R), with the same 5 forms and cuts -12/-4/+4/+12, spelled from the Remaining BEFORE the charge; c = s*SEQ[k % len(SEQ)] if s != 0 else 0; W = R + c; if s != 0: k += 1; return form. read(text, clear): if clear != 0: R = clear*RESET; s = clear; k = 1; return (the verdict verse's own words are not read, as now). Otherwise x = W; for w in tokens(text) if w in values: x += values[w]; x *= (1 - DRAIN); then R = clip(x, -CAP, CAP). Everything else unchanged: the mark_up loop (emerge before read), CLEAR_WRONG / CLEAR_RIGHT / CLEAR_PCT = 3, word_values, SCALE = 30, the 99% training split, TinyGPT CTX 64, 1500 steps, seeds 0-2. Effect: after a right verdict the next marker is spelled from +17, then later appearances get charges +32, +16, +34, +47, +17, +32 … until the next clear verdict. No charge before a book's first verdict.
  - Owner basis: "the +4 was a way to direct you to … where I feel like they belong" puts the numbers in the 17 slot of "[W1=17+4 …]". "those numbers in that sequence" fixes the order 17, 32, 16, 34, 47. "If wrong the sequence will begin with a value of (-17) and right a value of (+17)" means the sequence restarts at ±17 after each verdict. "syllables rotation sequence rather than a logical one" means it cycles. "the token used to interpret it based a Remaining value from the previous use of it" means the spelling is read from the Remaining. Q = 4/21 makes the owner's own "17+4" the resting point (see num17).
  - Prediction: Simulated markup, no training (current shifting word in brackets). Spellings anoksha…ruvelan 19/20/22/17/22% (20/14/30/13/23). Marker same as previous 46% (58%), so copying the last marker works less often (the 'carries perfectly but updates poorly' shortcut). Correlation of the next marker with the verse just read +0.42 (+0.64). Verdict sign still shown 5 / 10 verses later: 81% / 73% (66% / 57%). Never pinned (current 2%). 57% of markers differ from the current shifting word. If the owner is right, it should beat shifting and label on the long-story test, clearly in version A (verdict carried) and hopefully in B (everyday act). On the 100-pair judging it should at least tie shifting (about 69%). Risk: the slot counter k is invisible to the model, and average marker strength varies by slot (0.94–1.43), so the rotation adds noise. Judging could drop a little, and exp-12 bits are unlikely to improve (marker uncertainty given the previous marker is 1.76 bits vs 1.54 now).
- **num17**
  - Rule: Identical to numseq except SEQ = (17,): a constant charge of 17 at every appearance after a verdict. With neutral text the word rests exactly at W = 17 + 4 = 21, because with Q = 4/21 the leftover settles at Q·17/(1-Q) = 4.
  - Owner basis: The owner's original day-1 rule, never tested: "[w1=17 -<next word (-13)> = +4 Remaining] next emergence [W1=17+4 …]" (the AI switched RECHARGE off). It is the control that isolates what 32, 16, 34, 47 add beyond 17.
  - Prediction: Simulated: spellings 11/23/32/20/14%; same as previous 46%; next-marker correlation +0.55; verdict shown 5 / 10 later 65% / 59%; never pinned. 28% of markers differ from numseq. Expectation: responsiveness close to the current word, but it keeps a verdict lean for the whole run instead of fading in about 3 verses. If the 'remaining' recharge is the useful part, num17 ≈ numseq on judging. If the owner's numbers matter, numseq > num17 on long-story A/B (numseq holds verdicts longer: 81% vs 65% five verses on).
- **numsorted**
  - Rule: Identical to numseq except SEQ = (16, 17, 32, 34, 47), the same numbers in ascending ('logical') order. The verdict still sets R = ±17 and k = 1, so the charges run 17, 32, 34, 47, 16, 17, …
  - Owner basis: "those numbers in that sequence" and "a syllables rotation sequence rather than a logical one": the owner's order against the logical order, with the same numbers.
  - Prediction: If the order matters, numseq > numsorted. Honest expectation: no detectable difference. Only 12.3% of markers differ from numseq. Simulated statistics are almost identical (19/20/23/17/21%, correlation +0.43, verdict at 5 / 10 later 81% / 74%), and 3 seeds' noise is likely larger than that gap. A tie is the expected result and should be reported as 'order not shown to matter at this scale'.
- **numdrain**
  - Rule: Identical to numseq but no charge: c = 0 always. The proportional drain (DRAIN = 0.1411 per valued word, SPEND = 0), spelling from R, and verdict → R = ±17 are kept.
  - Owner basis: Mechanism control, not an owner rule. numseq and num17 change two things versus the current word: the drain shape and the recharge. This isolates the drain, so any gain can be credited to the owner's 'charge + Remaining' and not to the AI's drain change.
  - Prediction: Simulated: spellings 4/18/53/20/5%; next-marker correlation +0.78 (most responsive); verdict shown 5 / 10 later only 41% / 38% (forgets fast); same as previous 48%. Expectation: good on one-sentence judging, worst of the new configs on long-story A. The owner's rule is supported only if num17 / numseq beat numdrain on the long-story test.
- **numreset**
  - Rule: Exact current shifting_word rules (linear SPEND = 0.5 per valued word toward 0, RECHARGE off, cap ±51, spelling from the balance) with one change. Count clear verdicts n within each book (n = 1 at the book's first verdict; the count restarts at a book start). At the n-th verdict, balance = clear * SEQ[(n-1) % 5] with SEQ = (17, 32, 16, 34, 47), instead of clear * 17.
  - Owner basis: Another reading of 'the place of 17': in day 1, 17 is also the restart value ("the sequence will begin with a value of (-17) … (+17)"). Here the numbers set the size of successive restarts instead of per-appearance charges. It is the smallest possible change.
  - Prediction: Simulated: spellings 23/12/27/12/26%; correlation +0.57; verdict shown 5 / 10 later 75% / 61%; pinned 4%. Only 9.8% of markers differ from the current word. Expectation: a statistical tie with the existing shifting models on every test. A tie means the numbers as restart sizes don't matter.
- **numliteral**
  - Rule: OPTIONAL (predicted degenerate; run only if budget remains). Current rules (linear SPEND = 0.5, cap ±51, spelling from the CHARGED balance as emerge() does with RECHARGE = True), but the charge follows the owner's sequence. A clear verdict sets balance = 0, s = clear, k = 0 (literally 'reset to w1 = 0'). emerge(): if s != 0: balance += s*SEQ[k % 5]; k += 1; balance = clip(balance, -51, 51); return form_for(balance). No charge before a book's first verdict.
  - Owner basis: The owner's numbers placed exactly where they say, with no new AI change: this is PLAN's 'try the owner's original rule' using their numbers.
  - Prediction: Arithmetic says it collapses. The linear drain removes only about 0.5 × 10.9 ≈ 5.5 per verse, while every number is 16–47, and any charged value above 12 is spelled heavy. Simulated: spellings 50/1/2/1/47%, same as previous 96%, pinned at ±51 81%, correlation +0.16. It becomes a 2-spelling 'sign of the last verdict' marker, and the order of the numbers cannot matter. Expect it to do well on long-story A and badly on everyday-act judging. Its value is showing the owner why the drain had to be changed.

**Ambiguities.** 1. Key arithmetic finding (from simulating the markup on the KJV, no training). With today's settings, any charge at each appearance gives no testable result. The linear drain removes about 5.5 per verse, and all five numbers are 3–8× larger, so the balance pins at ±51. If the spelling includes the charge, every number is above the heavy cut of 12, so only the 2 heavy spellings are used. Making the slot testable needs two choices that are mine, not the owner's: a proportional drain, and spelling read from the Remaining. The owner's own example has no drain at all (17 - 13 = 4 is a plain signed sum).
2. Q = 4/21 is a calibration I chose so that the owner's '17+4' is the rule's resting value. Q = 4/17 (17 → 4 per verse, as in their first step) gives similar numbers: numseq correlation +0.40, verdict 84% five verses later. With Q = 4/21 the resting Remaining is 4c/17: 16 → 3.76 (just under the velanok cut of 4), 17 → 4.00 (exactly on it), 47 → 11.06 (just under 12). Those cut points were AI-chosen, so the fit is partly coincidence.
3. The charge's sign follows the last verdict. Following the balance's sign, as the code's RECHARGE does, lost the verdict signal in simulation. There is no charge before a book's first verdict. The cycle repeats after 47; stopping after 5 appearances still pinned 20% of the time with the linear drain.
4. The hidden slot counter (which charge comes next) is noise the model cannot see. Order and size effects (numseq vs numsorted: 12% of markers differ; against a constant 29.2, the mean of the numbers: 13.5%) are probably smaller than the seed-to-seed noise of 3 seeds. A constant-29.2 control is a possible swap for numsorted.
5. Minimum useful set: numseq, num17, numdrain (9 models). Add numsorted for the owner's 'in that sequence' question. numreset is cheap but expected to tie. numliteral is optional.
6. The zero symbols are not used in the design. A signed-zero spelling would need new invented words and a change to score()'s POSITION map.
7. Keep word_values and the 3% clear cutoffs computed exactly as now, even though they include held-out verses (the exp-12 caveat), so the new models are comparable with the saved controls.
8. The order coincidences (mirror x, 2y, y, 2x; 47 = 51 - 4; 21 + 47 = 68) are exact facts but carry no evidence of meaning.
9. No repo files were edited. The simulation scripts and cached word values are in /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/numbers_lens/ (stats.py, sim.py, sim2.py, sim3.py, sim4.py, values.json). The parent should copy them into the delivery folder if they are used.

## Reader 3: experimental design

**Confidence:** medium

**Reading.** The owner is saying where the numbers go, not giving a formula. The numbers 17, 32, 16, 34, 47 are a run in a fixed order, and the "+4" points to the slot in the owner's own rule "W1 = 17 + 4 Remaining" (also "W1=17+4 − <next 2 words (00)> = 0 Remaining"). That slot is the charge the word gets each time it appears, with the leftover from its previous use added on top. So the 17 in that rule becomes, one after another, 17, 32, 16, 34, 47. The rule also says "if wrong the sequence will begin with a value of (−17), right (+17)". So a run starts at a clear choice: the first value is the existing ±17 reset, and the next appearances get ±32, ±16, ±34, ±47 on top of what remains. One reading of "47 = 17+4" that needs no arithmetic: 47 sits 4 places after 17 in the list, so the run is five long and starts at 17. The four zero symbols match the four numbers one to one. This is a hint only: each charge may get used up to some kind of zero (unknown, from below, from above, fully cancelled; the last is the "(00)" of rule 2). If anything, that favours a run that ends and drains back to zero over one that cycles forever. It does not drive the design.

I checked this mechanically on the Bible, with no training and no test stories (scratch code in /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/sim_rules.py, run_sim4.py, run_sim5.py, run_sim6.py; it reproduces mark_up exactly, 100% match). Three findings shape the design:

(1) The test queued in HANDOFF ("singly and in sequence" through the coded RECHARGE switch, cap ±51) would train identical text. Swapping 17 for 16, 32, 34 or 47, or cycling the sequence, gives 100.0% the same markers, because any charge of 12 or more lands in the heavy spelling and the cap absorbs the rest. One model covers all of them.

(2) If the run starts at a clear choice, the order of 32, 16, 34, 47 cannot change any marker (a permuted order gives 100% the same text). The numbers act only through their total, 146.

(3) The order becomes visible only when the following words "use up" the charge and the spelling reads the Remaining. Even then 79% of markers match the permuted order.

Also: 17/34 = 16/32 = 0.5, which is exactly the current SPEND. So reading the numbers as SPEND ratios reproduces the existing RESET-17 model and needs no new model.

Background on the known defect: under the current rule, the rule itself forgets a verdict after about 3 neutral verses and a non-clear act after about 4 (all ties by 8). The model's "perfect carry" is a copying habit that the rule never taught.

**Symbol by symbol.** "17,32,16,34": the first four numbers, in the owner's fixed order (the one certain fact). They are the charge values for successive appearances of the word, starting at the clear choice (17 is the existing reset, "the sequence will begin with ±17").
"=?0": a zero of unknown sign, e.g. the start state (book start / "reset to w1=0"). Hint only.
"=-0": zero reached from the wrong side (a negative remaining used up). Hint only.
"=+0": zero reached from the right side. Hint only.
"=00": the "(00)" of the owner's rule 2 ("next 2 words following equaling (00) = 0 Remaining"): the charge fully used up by the following words. Taken together, four numbers against four zeros suggests each charge is spent down to zero. Hint only.
"47": the fifth number, the end of the run.
"17+4": the owner's "W1 = 17 + 4 Remaining", the pointer to where the numbers belong: in the 17 slot, the charge added at each appearance, with the remaining on top. It also reads positionally: 47 is 4 places after 17 in the list. The arithmetic (21 ≠ 47) is not meant literally.

**Configurations proposed:**

- **seqchoice**
  - Rule: PRIORITY 1 (primary). Implement as a subclass of shifting_word.ShiftingWord, or a copy of mark_up, under new model names (seqchoice_seed{s}_steps1500.pt); do not change module constants. State: balance, dir in {-1,0,+1}, k. read(text, clear!=0): balance = 17*clear; dir = clear; k = 0 (the reset is unchanged and is W1). emerge(): if dir != 0: k += 1; if 2 <= k <= 5: balance += dir * [32,16,34,47][k-2]; then return form_for(balance) (spell after the charge, as the coded emerge does). From the 6th appearance on, add no charge until the next clear choice. read(text, 0): same word loop (add value, spend SPEND=0.5 toward 0) but clip to +/-146 (=17+32+16+34+47) instead of +/-51, so nothing of the owner's numbers is thrown away. reset() at book start: balance=0, dir=0, k=0 (no charge before the first clear choice). Word values, SCALE 30, CLEAR regexes, CLEAR_PCT 3, FORMS, cut points and RECHARGE=False unchanged. Do NOT train a permuted-order control for this reading: it gives 100% identical text.
  - Owner basis: "If wrong the sequence will begin with a value of (-17) and right a value of (+17)" + "W1=17+4" (charge plus remaining at each new appearance) + today's "17,32,16,34 ... 47" in that order + the clarification that the +4 shows where the numbers belong. The run ending and draining back to zero fits the zero symbols (hint only).
  - Prediction: Rule-level (Bible only): 59% of markers same as RESET-17; marker same as the previous one 84% (now 58%); a clear verdict followed by neutral verses is still told apart after 8 verses in 100% of pairs (RESET-17: 61% after 4, 50% after 8). Content between verdicts behaves as now. Main prediction: long-story version A (explicit verdict, carried out of view, where the plain label currently wins) rises above shifting RESET-17 and reaches or beats the label. Short-story judging stays about the same (most short stories have no verdict phrase), with a slight drop possible from extra stickiness. Long-story B (no verdict) should not change, which makes it a built-in negative control. Exact-seed bits: cheaper markers, total no worse than RESET-17. SUPPORTED if, on version A, seqchoice beats shifting RESET-17 (pre-registered one-sided sign test over the 100 pairs, scores summed over seeds 0-2, p<0.05) and is not below the label. REFUTED if version A is not above RESET-17: the bottleneck is then reading the verdict in the first sentence (the start-marker diagnostic), not memory.
- **recharge17**
  - Rule: PRIORITY 2. Exactly shifting_word with RECHARGE=True: emerge() adds 17*sign(balance) before spelling at every appearance, cap +/-51, everything else unchanged. Implement as a subclass or a mark_up copy under a new model name (recharge17_seed{s}_steps1500.pt), never by flipping the shared constant (cached keys and model names don't record it). This one model stands for 'singly and in sequence' under the coded switch: with 16, 32, 34, 47 or the cycling sequence in place of 17, the marked text is 100.0% identical (checked). Do not spend models on those.
  - Owner basis: The owner's literal original rule "[W1=17+4 ...]": re-add the charge at each new appearance, with the remaining on top. It was switched off by the AI and never tested (PLAN step 1). The owner wants it tested.
  - Prediction: Rule-level: in practice only 2 spellings (anoksha 52%, ruvelan 48%), pinned at the cap 88% of the time, same as the previous marker 98%. Information about the verse just read, given the previous marker: 0.05 bits (RESET-17: 0.74). It is the extreme of 'carry everything, update almost never' and brackets the trade-off. Predict short-story judging drops at least 5 points below RESET-17 (fewer content-driven changes to learn from). On long stories the ties nearly vanish, but accuracy depends on the first marker, so B lands near or below RESET-17. Exact seed: the cheapest markers of any marker method (about 0.14 bits per verse given the previous marker), so the total is closest to baseline, but no gain on the words. SUPPORTS the literal rule if judging is within 2 points of RESET-17 and long-story B beats RESET-17 (p<0.05). REFUTES it if judging falls 5 or more points and B is not better. That would confirm that the defect gets worse with more carry.
- **recharge17spent**
  - Rule: PRIORITY 3. Subclass: SPEND = 17/10.9 = 1.56 per valued word (10.9 = mean valued words per TRAINING verse, i%50!=0; fix it in advance). emerge(): f = form_for(balance) FIRST: the spelling is the Remaining left by the previous verse, not 17+Remaining, which would always be heavy. Then, if balance != 0 and this is not the first appearance after a clear choice (that one is the reset W1 itself): balance += 17*sign(balance). Return f. read(): clear -> +/-17 as now; word loop unchanged except the new SPEND; clip +/-51. Book start -> 0, so no charge until content makes the balance nonzero. New model names.
  - Owner basis: The owner's arithmetic read literally: "[w1=17 -<next word (-13)> = +4 Remaining]" and "[W1=17+4 -<next 2 words (00)> = 0 Remaining]". The following words USE UP the charge, and the word is read by what remains ("the token used to interpret it based a Remaining value from the previous use of it"). Calibrated so a typical verse uses up about one charge of 17.
  - Prediction: This is the only non-saturating version of the owner's recharge that carries an ordinary (non-verdict) act. Rule-level: 50% of markers same as RESET-17; 5 spellings all in use (0.30 0.06 0.23 0.05 0.36); same as previous 75%. A strong non-clear act followed by 8 neutral verses is still told apart in 86% of pairs (RESET-17: 50%, all ties); verdicts 85%. Content update information drops to 0.19 bits, so expect short judging about the same or slightly down. Main prediction: long-story B (everyday act out of view, the one place carry has beaten the label) rises above shifting RESET-17 and the label. SUPPORTED if B beats both (sign test, p<0.05) and judging is within 3 points of RESET-17. REFUTED if B is not above RESET-17: a tiny model then cannot learn a latched sign from content, and the earlier B win came from copying alone.
- **seqcyclespent**
  - Rule: PRIORITY 4 (optional). As recharge17spent, but the charge at the n-th appearance since the last clear choice or book start is SEQ[(n-1) mod 5], SEQ=(17,32,16,34,47). After a clear choice, n=1 is the reset (+/-17 = SEQ[0]) and adds nothing, so the next appearances add 32, 16, 34, 47, 17, 32, ... in the balance's direction. SPEND = mean(SEQ)/10.9 = 29.2/10.9 = 2.68 per valued word. Spell from the Remaining (before the charge); cap +/-51; everything else unchanged.
  - Owner basis: The numbers "in that sequence" placed exactly where 17 sits in "W1 = 17 + 4 Remaining", repeating as a rotation ("a syllables rotation sequence rather than a logical one"; 5 numbers, 5 rotations), with the following words using up each charge.
  - Prediction: This is the only reading in which the order of the owner's numbers changes the training text: 79% of markers match the permuted control and 66% match recharge17spent. The rule itself is weak, though. Verdicts are forgotten after about 1 verse, a non-clear act is told apart only 56% of the time after 8 neutral verses, and the update information is 0.11 bits. Predict at or below RESET-17 on judging and both long-story versions. Its value is answering the owner's 'in that sequence' question directly. SUPPORTS the sequence if it beats recharge17spent or seqcyclespentperm on a pre-registered measure. REFUTED as an improvement if it does no better than RESET-17.
- **seqcyclespentperm**
  - Rule: PRIORITY 5 (optional order control, run only with seqcyclespent). Identical to seqcyclespent but SEQ=(17,47,34,16,32), fixed in advance. 17 stays first because the reset is 17; same numbers, same total, same SPEND 2.68.
  - Owner basis: Tests the one thing the owner is sure of: that the numbers belong IN THAT SEQUENCE (17,32,16,34,47).
  - Prediction: Predict no detectable difference from seqcyclespent: 79% of markers are identical, and seed-to-seed noise in judging is large (shifting 67, 72, 67). SUPPORTS the owner's order only if seqcyclespent beats this control (pre-registered sign test over pairs, summed over 3 seeds, p<0.05) on judging or long-story B. Otherwise the order is reported as not mattering at this scale. Low power: this test can only detect a large effect.

**Ambiguities.** Ambiguities: (a) Does the run stop after 47 (seqchoice), cycle (seqcyclespent), or hold at 47? The owner never said. The zero symbols weakly favour stopping and draining back to zero. (b) Is the charge applied in the direction of the last clear choice (seqchoice) or of the balance's current sign (recharge17, recharge17spent)? (c) Is the word spelled by charge + remaining (always heavy once the charge is 12 or more) or by the remaining alone? I chose per config and said which. (d) The cap: the owner never asked for one. The ±51 clip is the AI's choice, so seqchoice uses ±146 to keep all of the remaining. (e) The spend size: the owner's example has one word using up 13 of 17 and "00" words using up 21. The project's word values are much smaller (median |value| 1, verse sum sd 12, 10.9 valued words per verse), so the calibration (SPEND 1.56 or 2.68) is mine and must be fixed in advance. (f) ?0, -0, +0, 00 and "47 = 17+4" have no settled meaning (owner: "I dont know"). My positional reading of 47 is a guess.

Design notes for the orchestrator:
- Core set: seqchoice, recharge17, recharge17spent (9 models, about 1.5 hours). The two optional configs add 6 models; the 6th slot is spare. Best use of it: seqchoice with cap ±51 as a one-factor control for keeping vs throwing away the excess. It is 82% the same text as seqchoice and 88% the same as RESET=47, so it also stands in for the PLAN's 'RESET 47' reading.
- Do not spend models on singles via the coded RECHARGE (identical text), on a permuted seqchoice (identical text), or on SPEND = 17/34 or 16/32 (that is the existing model).
- Add a no-training diagnostic for every model, old and new, on the long stories: (i) update = does the first marker after the act lean the right way; (ii) carry = does the final marker agree with that first marker. This separates the two halves of the known defect.
- Pre-register comparisons against the existing shifting RESET-17 and label models (same seeds 0-2, same scoring: method_comparison.score, long_story_test A/B, understanding_compression TOTAL and WORDS ONLY). Add the new methods to those scripts' method lists under new names.
- All rule-level numbers above come from Bible verses only (training split for the proxies). I deliberately did not run any rule on the 100 test stories, to avoid tuning on them.
- Scale honesty: none of this bears on how a large model understands the owner.

## The judge's final design

**Plain reading.** Two things are certain. Your numbers come in a fixed order, 17, 32, 16, 34, 47, and the "+4" points to where they go: the place of 17 in your rule "W1 = 17 + 4 Remaining". That place is the charge the word gets each time it appears, with whatever was left over last time carried on top. So in this test the word gets a fresh charge every time it appears. In the plain version the charge is 17 every time. In your sequence version the charges take turns: 17, 32, 16, 34, 47, 17, 32, and so on. A clear right or wrong restarts the run at +17 or -17, as your day-1 rule says. The words of each verse use up most of the charge, and the word is spelled from what is left, as you wrote ("based a Remaining value from the previous use of it"). How fast the words use up the charge was my choice, not yours. I set it so that in ordinary text the plain rule settles at exactly your "17 + 4": each verse uses 17 and leaves 4. That choice is what keeps the word from getting stuck at the top, which is why your original rule was switched off before. Nobody knows what ?0, -0, +0 and 00 mean, so they are not tested. Reading "47 = 17+4" as "47 also goes in that slot" is a guess, and one model tests it by giving 47 every time.

### Configurations

- **num_charge17**
  - Rule: SHARED RULE for all six configs, CHARGE(CH). It goes in a new script, experiments/numbers_test.py, which imports shifting_word (word_values, tokens, CLEAR_WRONG, CLEAR_RIGHT, CLEAR_PCT, FORMS, form_for) and changes nothing in it.

Constants, fixed now: RESET = 17, CAP = 51, NBAR = 10.9043 (the mean number of tokens w with w in values per TRAINING verse, i % 50 != 0), DRAIN = 1 - (4/21)**(1/NBAR) = 0.141073 (assert this to 6 decimals). Clear choices are found exactly as in sw.mark_up: the verdict regex, or the top or bottom 3% of verse sums.

Go through the verses in order:
(0) At each book start: R = 0.0, s = 0, k = 0.
(1) form = form_for(R). The word is spelled from the Remaining before the charge, with the same 5 spellings and cuts.
(2) If s != 0: W = R + s*CH[k % len(CH)] and k += 1. Otherwise W = R.
(3) Write 'form text'.
(4) If the verse is a clear choice c = ±1: R = 17*c, s = c, k = 0, and the verse's own words are not read (as now). Otherwise x = W; for each token w of the verse with w in values: x += values[w]; x *= (1 - DRAIN). Then R = clip(x, -51, 51).

Training: TinyGPT on the training verses (i % 50 != 0), vocab = tt.Vocab(train_texts), CTX 64, 1500 steps, seeds 0, 1 and 2. Save as models/num_<name>_seed{s}_steps1500.pt.

For num_charge17: CH = (17,), a charge of 17 at every appearance after a clear choice.
  - Owner basis: Day 1: "[w1=17 -<next word (-13)> = +4 Remaining] next emergence of the word [W1=17+4 ...]"; "the token used to interpret it based a Remaining value from the previous use of it"; "reset to [w1=0] when a clear right or wrong choice exists. If wrong the sequence will begin with a value of (-17) and right a value of (+17)". In neutral text this rule settles at exactly W = 17 + 4 = 21, leaving 4 Remaining (checked).
  - Why included: The task requires it: the owner's plain recharge rule, never tested before, with N = 17. It separates the rule itself from the effect of the numbers. On the Bible markup, with no training: spellings 10.8/23.1/32.0/20.1/13.9%, 0.03% of verses at the cap, and 55.0% of markers differ from the current shifting word.
- **num_seq**
  - Rule: Same as num_charge17, except CH = (32, 16, 34, 47, 17). After each clear choice the values therefore run 17 (the reset) → 32 → 16 → 34 → 47 → 17 → 32 → ... in the direction of that choice. The run cycles until the next clear choice, and every clear choice restarts it at 17.
  - Owner basis: Today: "17,32,16,34 ... [47, = 17+4]". The clarification: "those numbers in that sequence", and the +4 shows where they belong, in the 17 slot. Day 1: "syllables rotation sequence" and "This may continue on for long periods" (so it cycles rather than stops). The owner's list begins with 17, the same value as the day-1 reset.
  - Why included: The owner's literal numbers, in their order, as N. It does not pin (simulated: spellings 19.1/20.4/22.2/16.7/21.6%, 0.27% of verses at the cap). Its marker differs from num_charge17 on 28.1% of verses.
- **num_seqrev**
  - Rule: Same as num_charge17, except CH = (47, 34, 16, 32, 17). The values run 17 (the reset) → 47 → 34 → 16 → 32 → 17 → ...: the same five numbers, the same mean, the same restart at 17, with the cycle reversed.
  - Owner basis: A control for the one claim the owner is sure of: that the numbers belong "in that sequence".
  - Why included: The order control. It changes 4 of the 5 charge positions. Its marker differs from num_seq on 22.3% of verses, the most of the orders checked (the ascending, "logical" order differs on 21.0%).
- **num_const29**
  - Rule: Same as num_charge17, except CH = (29.2,): the mean of 17, 32, 16, 34 and 47, given at every appearance.
  - Owner basis: Not an owner rule. It is the control that matches the owner's sequence in average size but has no variation. It also stands for the single numbers 32 and 34, whose markups differ from it on only 5.5% and 9.1% of verses.
  - Why included: It separates 'the owner's sequence' from 'a bigger average charge'. Its marker differs from num_seq on 13.5% of verses and from num_charge17 on 30.9%.
- **num_charge47**
  - Rule: Same as num_charge17, except CH = (47,): a charge of 47 at every appearance. The reset stays at 17.
  - Owner basis: Today: ["47," = "17+4"]: 47 is written in the place of "17+4". This is the 'singly' half of the queued HANDOFF test. Single 16 needs no model of its own: its markup differs from num_charge17 on only 3.2% of verses.
  - Why included: It tests the owner's largest number on its own in the slot. Simulated: spellings 29.0/15.3/13.5/12.2/30.0%, 1.23% at the cap. Its marker differs from num_charge17 on 52.9% of verses.
- **num_drain0**
  - Rule: Same as num_charge17, except CH = (0,): no charge at all. It keeps the proportional drain, the spelling from R, and the ±17 on a clear choice.
  - Owner basis: Not an owner rule. It is the mechanism control: compared with the current shifting word, the new rule changes two things, the drain (my choice) and the recharge (the owner's rule). This control isolates the drain.
  - Why included: It keeps my drain change from taking credit for the owner's rule. Simulated: spellings 4.4/17.7/52.8/19.8/5.3%. It forgets a verdict fast: the verdict's sign survives 5 verses later only 33% of the time, against 65% for num_charge17 and 63% for the current shifting word.

### Controls

These models are reused and not retrained. Each has seeds 0, 1 and 2 at 1500 steps, stored in experiments/models/{method}_seed{s}_steps1500.pt:
- shifting (RESET 17, the current rule): the main comparator.
- baseline (no marker): the second comparator.
- label, carry3 and scrambled: reported for description only.

Their stored per-item scores are reused unchanged: results_methods.json v2_judge (M1), results_long_story.json version B 'correct' (M2), and results_understanding.json R6/R7 per_verse_total (M3).

The 18 new models are scored with the same unchanged code paths: method_comparison.score on ITEMS_V2; long_story_test build_stories and judge_marked for version B with START_MARKER = False; understanding_compression code_one with each config's own held-out markers.

### Pre-registration

This is fixed before any of the 18 models is trained. Nothing is tuned on stories_v2 or on the held-out verses.

0. MANIPULATION CHECK (Bible markup only, before training)
A config passes if at most 5% of verses sit at the ±51 cap and every spelling covers at least 3% of verses. A config that fails is still trained, but it is labelled 'degenerate' and its results are descriptive only. Expected values, from the judge's scratch simulation /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/judge_numbers/sim_rules.py: all six pass. The constants are frozen: NBAR 10.9043, DRAIN 0.141073, CAP 51, RESET 17, the CH lists as given, word_values, SCALE 30, the verdict regexes, CLEAR_PCT 3, FORMS and the cut points.

1. MEASURES (per config, seeds 0, 1, 2)
- M1 (PRIMARY): judging on the 100 stories_v2 pairs, as in exp 10, using method_comparison.score → v2_judge. For each pair, the score is the number of seeds that judged it correctly (0-3).
- M2: long-story version B (the everyday act pushed out of the 64-token view, no start marker), as in exp 11. For each pair and seed the score is 1, 0.5 for an exact tie, or 0. For each pair, the score is the sum over seeds (0-3).
- M3: exact-seed TOTAL bits, as in exp 12. For each of the 623 held-out verses (i % 50 == 0), the TOTAL code length (marker + words + verse end), averaged over the 3 seeds. Seed 0 of each config is decoded and must regrow H exactly; if it does not, M3 is void for that config.
- Version A and the short version are reported for description only.

2. TESTS (all one-sided, in the direction 'new is better')
- M1 and M2: exact sign test over the pairs whose per-pair sums differ. Ties are dropped. p = P(Bin(n, ½) ≥ wins).
- M3: paired sign-flip permutation test on the mean of d_v = new_v − comparator_v. It uses 100,000 flips with numpy default_rng(0), and p = (#{permuted mean ≤ observed} + 1) / 100,001. 'Better' means a mean d_v below 0. The one-sided sign test over verses is reported alongside, and any disagreement between the two tests is reported.

3. FAMILIES (Holm correction, alpha 0.05, applied separately within each measure)
- F1: each of the 6 new configs vs shifting.
- F2: each of the 6 new configs vs baseline. On M2 the baseline scores a constant 1.5 per pair, so F2 there means 'beats chance'.
- F3, the owner's numbers (4 tests):
  - N1: num_seq > num_charge17
  - N2: num_seq > num_seqrev
  - N3: num_seq > num_const29
  - N4: num_charge47 > num_charge17
- F4, mechanism: R1 num_charge17 > num_drain0. This is a single test at alpha 0.05.

4. VERDICTS (decided on M1)
- 'The owner's numbers matter' = N1 passes on M1: their sequence beats a plain 17 in the same rule.
- 'The sequence itself matters' = N1, N2 and N3 all pass on M1.
- '47 in the 17 slot helps' = N4 passes on M1.
- 'The owner's recharge rule helps' = num_charge17 passes F1 on M1. It is credited to the recharge, and not to the AI's drain, only if R1 also passes on M1.
- 'Useful for the project' = any config passes F1 on M1.
- M2 and M3 are judged by the same rules. A pass on M2 or M3 alone is reported as a 'secondary sign', never as a confirmation.
- Every other outcome is reported as 'not shown at this scale', never as 'disproved'.
- Effect sizes are reported for every comparison, even when not significant, because the owner counts any improvement: mean % correct per seed, wins/losses, and mean bits per verse. label, carry3 and scrambled are included for description.
- Expectation, which is not part of the verdict: ties with shifting on M1, as all marker methods have tied so far, and num_seq ≈ num_seqrev.

5. LIMITS
Tiny model, 3 seeds, 100 pairs. Only large effects can be detected. word_values were computed on all verses, including the held-out ones; this is kept as before for comparability and flagged for M3.

### Dropped, and why

- The coded RECHARGE switch (re-add 17·sign at each appearance, spell after the charge, linear SPEND 0.5, cap ±51). It pins at the cap, and swapping in 16, 32, 34, 47 or the cycling sequence gives the same marked text, so it cannot test the numbers.
- The numbers as successive RESET sizes. That is not the slot the owner pointed to, and only 9.8% of markers would change.
- The numbers as SPEND ratios. 17/34 = 16/32 = 0.5, which is the existing model.
- A linear spend calibrated to 17 (reader 3's recharge17spent and seqcyclespent). The owner's numbers (mean 29.2) then overcharge it, unless SPEND is changed for each config, which would confound size with spend.
- Reader 1's directional bank (signed spend, cap R ≤ N, direction only from verdicts, heavy form at R ≥ 4). It adds more invented rules, and under its spend the owner's own example 17 − 13 gives 0 instead of 4.
- Rescaled 'normalized' charges. These are not the owner's numbers as N. The proportional drain makes rescaling unnecessary, because the rule never pins for any N.
- seqchoice (a run that stops after 47, with a ±146 cap). Day 1 says the rule 'may continue on for long periods', which favours cycling, and the hint from the zero symbols is weak.
- Single 16, 32 and 34. Their markups differ from num_charge17, num_const29 and num_const29 on only 3.2%, 5.5% and 9.1% of verses, so those configs cover them.
- The ascending ('logical') order control. The reversed order changes more markers (22.3% vs 21.0%).
- The zero states ?0, -0, +0, 00. The owner has no meaning for them, and testing them would need new invented spellings plus a change to the POSITION map in score().
- Numerology (47 = 51 − 4, 21 + 47 = 68, the mirror pattern x, 2y, y, 2x, mod-17 patterns). None of it makes a testable claim.
- The start-marker version of M2. It stays exploratory, as in exp 11.

No repository file was edited. The judge's scratch checks are /tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/judge_numbers/sim_rules.py, sim_extra.py and values.json. values.json is identical to sw.word_values; copy these into the delivery folder if they are used.
