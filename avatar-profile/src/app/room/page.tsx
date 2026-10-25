'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';

type Turn = { role: 'user' | 'assistant'; content: string };

const STARTERS = [
  'Do you prefer oranges or bananas?',
  'Pick a number 1 to 10.',
  'In 3 to 5 words, greet a stranger coming in from the rain.',
];

export default function Room() {
  const [turns, setTurns] = useState<Turn[]>([]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [mode, setMode] = useState<string | null>(null);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [turns, busy]);

  async function send(text: string) {
    const msg = text.trim();
    if (!msg || busy) return;
    const next = [...turns, { role: 'user' as const, content: msg }];
    setTurns(next);
    setInput('');
    setBusy(true);
    try {
      const r = await fetch('/api/avatar', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ message: msg, history: turns }),
      });
      const data = await r.json();
      setMode(data.mode ?? null);
      setTurns([...next, { role: 'assistant', content: data.reply ?? '(no reply)' }]);
    } catch {
      setTurns([...next, { role: 'assistant', content: '(the room dropped — try again)' }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-bold text-white">The Room</h1>
        <p className="mt-1 text-sm text-neutral-400">
          You&apos;re sitting across from Echo — a voice model of Garrett. Talk to it like it&apos;s him.
          {mode === 'scripted' && <span className="ml-1 text-amber-400">(offline mode: canned answers until an API key is set)</span>}
        </p>
      </div>

      <div className="min-h-[320px] space-y-3 rounded-xl border border-neutral-800 bg-neutral-900/40 p-4">
        {turns.length === 0 && (
          <div className="pt-10 text-center text-sm text-neutral-500">
            <p>Nobody&apos;s said anything yet. Try one:</p>
            <div className="mt-3 flex flex-wrap justify-center gap-2">
              {STARTERS.map((s) => (
                <button key={s} onClick={() => send(s)} className="rounded-full border border-neutral-700 px-3 py-1.5 text-xs text-neutral-300 transition hover:bg-neutral-800">
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}
        {turns.map((t, i) => (
          <div key={i} className={t.role === 'user' ? 'flex justify-end' : 'flex justify-start'}>
            <div className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${t.role === 'user' ? 'rounded-br-sm bg-amber-500 text-neutral-950' : 'rounded-bl-sm border border-neutral-700 bg-neutral-800 text-neutral-100'}`}>
              {t.role === 'assistant' && <div className="mb-0.5 font-mono text-[10px] uppercase tracking-wider text-amber-400">Echo</div>}
              {t.content}
            </div>
          </div>
        ))}
        {busy && <div className="flex items-center gap-2 text-sm text-neutral-500"><Loader2 className="h-4 w-4 animate-spin" /> Echo is thinking…</div>}
        <div ref={endRef} />
      </div>

      <form onSubmit={(e) => { e.preventDefault(); send(input); }} className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Say something…"
          className="flex-1 rounded-lg border border-neutral-700 bg-neutral-900 px-4 py-2.5 text-sm text-white outline-none focus:border-amber-500"
        />
        <button type="submit" disabled={busy} className="inline-flex items-center gap-2 rounded-lg bg-amber-500 px-4 py-2.5 font-medium text-neutral-950 transition hover:bg-amber-400 disabled:opacity-50">
          <Send className="h-4 w-4" />
        </button>
      </form>
    </div>
  );
}
