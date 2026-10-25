import Link from 'next/link';
import { ArrowRight, MessageSquare, Target, ShieldQuestion } from 'lucide-react';
import { ECHO_KEY_META } from '@/lib/echo-key.generated';

const projects = [
  { name: 'Echoes of Alara', when: '2025–2026', what: 'A multi-agent art-reflection app. Five voices — Veridian, Lusa, Nexus, Cro, SaCoLu — read a piece of art and talk back.' },
  { name: 'Metaphor-Driven Security Design', when: 'Oct 2026', what: 'Turning an attack into a story so a non-specialist can design the defense. The attacker slips on the doorstep instead of breaking the door.' },
  { name: 'Comprehension research', when: 'Oct 2026', what: 'Does teaching through story transfer better than teaching through rules? A shifting word that carries a running balance, tested on small models.' },
  { name: 'The Echo Key', when: 'ongoing', what: 'Compiling a person’s own words into a persona an LLM can wear. This profile is the first live test of it.' },
];

export default function Home() {
  return (
    <div className="space-y-14">
      <section className="pt-6">
        <p className="font-mono text-xs uppercase tracking-widest text-amber-400">Conceptual Engineer</p>
        <h1 className="mt-3 text-4xl font-bold text-white sm:text-5xl">Garrett C. Gauthier</h1>
        <p className="mt-5 max-w-2xl text-lg leading-relaxed text-neutral-300">
          I work in pictures. An idea shows up as a glowing creature crossing a log in a dark forest,
          and the real, testable thing is hiding inside the picture. My job — and the AI&apos;s job — is to
          translate that into something that actually runs.
        </p>
        <p className="mt-4 max-w-2xl leading-relaxed text-neutral-400">
          This page has an Avatar of me you can talk to. It&apos;s built from my own words across every
          project. Then there&apos;s a game: ask it and me the same question, apart, and see how close it lands.
        </p>
        <div className="mt-7 flex flex-wrap gap-3">
          <Link href="/room" className="inline-flex items-center gap-2 rounded-lg bg-amber-500 px-5 py-2.5 font-medium text-neutral-950 transition hover:bg-amber-400">
            Talk to the Avatar <ArrowRight className="h-4 w-4" />
          </Link>
          <Link href="/match" className="inline-flex items-center gap-2 rounded-lg border border-neutral-700 px-5 py-2.5 font-medium text-neutral-200 transition hover:bg-neutral-800">
            Play the matching game
          </Link>
        </div>
      </section>

      <section className="grid gap-4 sm:grid-cols-3">
        {[
          { icon: MessageSquare, title: 'The Room', body: 'A simulation room. Sit down and talk to the Avatar like it’s me.', href: '/room' },
          { icon: Target, title: 'Matching Game', body: 'Same question to the Avatar and to me, blind. Score how alike the answers are.', href: '/match' },
          { icon: ShieldQuestion, title: 'Guard Dog', body: 'The security idea behind it — and an honest note on what it can and can’t do.', href: '/guard-dog' },
        ].map((c) => (
          <Link key={c.title} href={c.href} className="group rounded-xl border border-neutral-800 bg-neutral-900/50 p-5 transition hover:border-amber-500/40">
            <c.icon className="h-5 w-5 text-amber-400" />
            <h3 className="mt-3 font-semibold text-white">{c.title}</h3>
            <p className="mt-1 text-sm leading-relaxed text-neutral-400">{c.body}</p>
          </Link>
        ))}
      </section>

      <section>
        <h2 className="text-sm font-semibold uppercase tracking-widest text-neutral-500">The work</h2>
        <div className="mt-4 space-y-3">
          {projects.map((p) => (
            <div key={p.name} className="rounded-xl border border-neutral-800 bg-neutral-900/50 p-5">
              <div className="flex items-baseline justify-between gap-3">
                <h3 className="font-semibold text-white">{p.name}</h3>
                <span className="shrink-0 font-mono text-xs text-neutral-500">{p.when}</span>
              </div>
              <p className="mt-2 text-sm leading-relaxed text-neutral-400">{p.what}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-xl border border-neutral-800 bg-neutral-900/30 p-5 text-sm text-neutral-400">
        <h2 className="font-semibold text-neutral-300">How the Avatar is built</h2>
        <p className="mt-2 leading-relaxed">
          A small compiler reads curated notes on how I write and a set of my real lines ({ECHO_KEY_META.sampleCount} of
          them), and turns them into one persona the Avatar wears. No private data, no accounts, no contact info —
          just a speaking style, the way an actor gets notes on a character. Re-running the compiler updates the Avatar.
        </p>
      </section>
    </div>
  );
}
