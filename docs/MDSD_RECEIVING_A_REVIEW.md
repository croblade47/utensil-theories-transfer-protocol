# How to Receive a Review Without Losing Heart

**One page for authors on reading, understanding, and acting on a specialist review of your MDSD draft.**

---

## What's about to happen

A specialist is going to read what you wrote and reply. The reply will probably be longer than your draft. It may list things you missed, things you got wrong, and things that scared them that didn't scare you. This is a good day, not a bad one.

The framework is designed to produce drafts the specialist can improve. If your reviewer finds a dozen things, that is twelve things you now know. If they find none, either you're a specialist and didn't need the framework, or your reviewer skimmed and you need a different one.

## Read the reply in this order

1. **The verdict first.** It will be one of five words or phrases. Read that and nothing else for a moment. It tells you where the next round goes.
2. **What's right next.** Specifically what you got right. Not for your ego — because it tells you which parts don't need to change in revision.
3. **Walkthrough third.** The reviewer added rows to the attacker's path. Read those as if the reviewer were telling you a short story about the attacker you missed.
4. **Blind spots last.** This is where the real work is. Expect the Critical items to add weeks to your project. That is normal and okay.

## Five things to do, five things not to do

**Do:**

- Read the whole reply twice before you reply yourself. First read is for shock. Second read is for understanding.
- Ask for plain-language clarification on anything you don't understand. "I don't know what you mean by 'session fixation,' can you describe that as a scene?" is a perfectly good question and a reviewer who follows this protocol will answer it.
- Treat the Critical blind spots as design-level, not polish. They usually mean the scene itself needs to change, not that you need to add one more primitive.
- Revise your attacker's story if the reviewer added moves. The story is the source of everything else; strengthen it first.
- Thank the reviewer. Specifically. "The row about session hijack after step 3 was the one I needed." It helps them calibrate for next time.

**Don't:**

- Defend the draft reflexively. The reviewer isn't attacking you; they're attacking the design. The design is not you.
- Argue the first finding before reading the rest. The findings often make more sense in order.
- Try to close every finding in the first revision. Address Critical first; Important and Nice-to-Have can wait a round if there's a reason.
- Rewrite in acronyms you don't understand just because the reviewer used them. If a finding doesn't yet make sense in plain language, you can't yet act on it; ask.
- Fire the reviewer because the review was long. The long reviews are the useful ones.

## What each verdict means for you

- **Ready to simulate.** Build the simulation (`sims/` has templates). The specialist will see it before deploy.
- **Revise and resubmit.** Close the Critical items, maybe some Important ones, and send back. Expect one more full round.
- **Needs broader review.** The design touches a specialty your current reviewer isn't the right one for. They'll name who to bring in. Don't skip this; the finding exists because something in the design is outside what one person can safely sign off.
- **Not viable as designed.** Not a judgment on you — a judgment on the scene. The reviewer will suggest what a viable scene might look like. Start over at Step 1 with that nudge, not at Step 4 with the current primitives.
- **Needs re-scoped story.** Your attacker paragraph is too thin. The reviewer will have questions. Answer those first, then re-draft from there.

## Reasonable turnaround

A first revision after review usually takes about half the time the original draft took. If it's taking longer, the verdict was probably "Not viable" or "Re-scoped" and the review is being treated as "Revise." Reread the verdict.

## One honest reminder

A clean review on your second draft doesn't mean the design is secure. It means the specialist is out of findings *at the metaphor layer*. Simulation, red team, and production hardening still come after. The framework is a bridge, not a destination.

Go read the reply.
