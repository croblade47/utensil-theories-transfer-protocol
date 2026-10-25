import Anthropic from '@anthropic-ai/sdk';
import { ECHO_SYSTEM_PROMPT, ECHO_SAMPLE_LINES } from '@/lib/echo-key.generated';

export const runtime = 'nodejs';

type Turn = { role: 'user' | 'assistant'; content: string };

// Build a few-shot opener from real sample lines so the voice is anchored
// even on the first reply.
function sampleContext(): string {
  const picks = ECHO_SAMPLE_LINES.slice(0, 12).map((s) => `- "${s}"`).join('\n');
  return `Here are real lines Garrett has written, for voice reference only (do not quote them back):\n${picks}`;
}

// Used when there is no API key, so the demo still works offline.
function scriptedReply(message: string): string {
  const m = message.toLowerCase();
  if (/orange|banana/.test(m)) return "Oranges. More work to peel but the payoff's better — kind of how I like most things.";
  if (/\b1\s*(-|to)\s*10\b|number.*1.*10|guess a number/.test(m)) return "17's not on the board, so... 7. No — 4. Going with 4.";
  if (/greet|stranger|rain/.test(m)) return "Come in, you're soaked — grab a seat.";
  if (/who are you|are you (garrett|real|ai)/.test(m)) return "I'm Echo — a voice model built from Garrett's own words. Not the real guy, just shaped like how he talks.";
  return "Mah, I hear you. Say a bit more and I'll give you a straight answer — I'm shooting a little in the dark without the key hooked up.";
}

export async function POST(req: Request) {
  let body: { message?: string; history?: Turn[] } = {};
  try { body = await req.json(); } catch { /* ignore */ }
  const message = (body.message || '').slice(0, 2000);
  const history = Array.isArray(body.history) ? body.history.slice(-10) : [];

  if (!message.trim()) {
    return Response.json({ error: 'empty message' }, { status: 400 });
  }

  if (!process.env.ANTHROPIC_API_KEY) {
    return Response.json({ reply: scriptedReply(message), mode: 'scripted' });
  }

  try {
    const client = new Anthropic();
    const resp = await client.messages.create({
      model: 'claude-opus-4-8',
      max_tokens: 400,
      system: `${ECHO_SYSTEM_PROMPT}\n\n${sampleContext()}`,
      messages: [
        ...history.map((t) => ({ role: t.role, content: t.content })),
        { role: 'user' as const, content: message },
      ],
    });
    const text = resp.content
      .filter((b): b is Anthropic.TextBlock => b.type === 'text')
      .map((b) => b.text)
      .join('')
      .trim();
    return Response.json({ reply: text || scriptedReply(message), mode: 'live' });
  } catch {
    // Key present but call failed (quota, network): fall back, don't 500.
    return Response.json({ reply: scriptedReply(message), mode: 'scripted' });
  }
}
