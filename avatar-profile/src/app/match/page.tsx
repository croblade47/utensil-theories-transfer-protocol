'use client';

import { useState } from 'react';
import { Loader2, RefreshCw } from 'lucide-react';

const QUESTIONS = [
  'Do you prefer oranges or bananas?',
  'If you had to guess a number from 1 to 10, what would it be?',
  'Using 3 to 5 words, greet a stranger coming in from the rain.',
  'Coffee or tea, and why?',
  'What do you say to a close friend walking in the door?',
  'Describe a good idea in one short sentence.',
];

type Phase = 'ask' | 'answering' | 'reveal';
type Score = 'match' | 'close' | 'miss';

export default function Match() {
  const [qIndex, setQIndex] = useState(0);
  const [custom, setCustom] = useState('');
  const [phase, setPhase] = useState<Phase>('ask');
  const [mine, setMine] = useState('');
  const [avatar, setAvatar] = useState('');
  const [busy, setBusy] = useState(false);
  const [scores, setScores] = useState<Score[]>([]);

  const question = phase === 'ask' && custom.trim() ? custom.trim() : QUESTIONS[qIndex];

  async function lockIn() {
    if (!mine.trim() || busy) return;
    setBusy(true);
    setPhase('answering');
    try {
      const r = await fetch('/api/avatar', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ message: question, history: [] }),
      });
      const data = await r.json();
      setAvatar(data.reply ?? '(no reply)');
    } catch {
      setAvatar('(the avatar dropped — try again)');
    } finally {
      setBusy(false);
      setPhase('reveal');
    }
  }

  function rate(s: Score) {
    setScores([...scores, s]);
    // next round
    setMine(''); setAvatar(''); setCustom('');
    setQIndex((i) => (i + 1) % QUESTIONS.length);
    setPhase('ask');
  }

  const total = scores.length;
  const matched = scores.filter((s) => s !== 'miss').length;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Matching Game</h1>
        <p className="mt-1 max-w-2xl text-sm text-neutral-400">
          The point isn&apos;t an identical answer — it&apos;s an answer that&apos;s <em>like</em> yours. Write yours
          before you see the Avatar&apos;s. Then reveal, and rate how close it got.
        </p>
      </div>

      {total > 0 && (
        <div className="flex items-center gap-4 rounded-lg border border-neutral-800 bg-neutral-900/50 px-4 py-3 text-sm">
          <span className="font-mono text-amber-400">{matched}/{total}</span>
          <span className="text-neutral-400">rounds where the Avatar landed close or dead-on</span>
        </div>
      )}

      <div className="rounded-xl border border-neutral-800 bg-neutral-900/40 p-5">
        <div className="font-mono text-xs uppercase tracking-widest text-amber-400">The question</div>
        <p className="mt-2 text-lg text-white">{question}</p>

        {phase === 'ask' && (
          <div className="mt-4 space-y-3">
            <textarea
              value={mine}
              onChange={(e) => setMine(e.target.value)}
              placeholder="Your answer (the Avatar can't see this)…"
              rows={2}
              className="w-full resize-none rounded-lg border border-neutral-700 bg-neutral-900 px-4 py-2.5 text-sm text-white outline-none focus:border-amber-500"
            />
            <div className="flex flex-wrap items-center gap-2">
              <button onClick={lockIn} disabled={!mine.trim()} className="rounded-lg bg-amber-500 px-5 py-2 font-medium text-neutral-950 transition hover:bg-amber-400 disabled:opacity-40">
                Lock in &amp; reveal
              </button>
              <button onClick={() => { setQIndex((i) => (i + 1) % QUESTIONS.length); setMine(''); setCustom(''); }} className="inline-flex items-center gap-1.5 rounded-lg border border-neutral-700 px-3 py-2 text-sm text-neutral-300 transition hover:bg-neutral-800">
                <RefreshCw className="h-3.5 w-3.5" /> Different question
              </button>
            </div>
            <input
              value={custom}
              onChange={(e) => setCustom(e.target.value)}
              placeholder="…or type your own question"
              className="w-full rounded-lg border border-neutral-800 bg-neutral-900 px-4 py-2 text-sm text-neutral-300 outline-none focus:border-amber-500"
            />
          </div>
        )}

        {phase === 'answering' && (
          <div className="mt-4 flex items-center gap-2 text-sm text-neutral-500"><Loader2 className="h-4 w-4 animate-spin" /> Avatar is answering, blind…</div>
        )}

        {phase === 'reveal' && (
          <div className="mt-4 space-y-3">
            <div className="rounded-lg border border-neutral-700 bg-neutral-800/60 p-4">
              <div className="font-mono text-[10px] uppercase tracking-wider text-neutral-400">You said</div>
              <p className="mt-1 text-sm text-neutral-100">{mine}</p>
            </div>
            <div className="rounded-lg border border-amber-500/40 bg-amber-500/5 p-4">
              <div className="font-mono text-[10px] uppercase tracking-wider text-amber-400">Echo said</div>
              <p className="mt-1 text-sm text-neutral-100">{avatar}</p>
            </div>
            <div className="pt-1">
              <div className="mb-2 text-xs text-neutral-500">How close is that to you?</div>
              <div className="flex flex-wrap gap-2">
                <button onClick={() => rate('match')} className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-emerald-500">That&apos;s me</button>
                <button onClick={() => rate('close')} className="rounded-lg bg-amber-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-amber-500">Close</button>
                <button onClick={() => rate('miss')} className="rounded-lg bg-neutral-700 px-4 py-2 text-sm font-medium text-white transition hover:bg-neutral-600">Not me</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
