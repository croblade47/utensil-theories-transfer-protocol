import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';

export const metadata: Metadata = {
  title: 'Garrett C. Gauthier — Conceptual Engineer',
  description: 'Interactive profile, an Avatar you can talk to, and a matching game that tests how close it gets.',
};

const nav = [
  { href: '/', label: 'Profile' },
  { href: '/room', label: 'The Room' },
  { href: '/match', label: 'Matching Game' },
  { href: '/guard-dog', label: 'Guard Dog' },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-neutral-950 text-neutral-200 antialiased">
        <header className="sticky top-0 z-20 border-b border-neutral-800 bg-neutral-950/80 backdrop-blur">
          <nav className="mx-auto flex max-w-4xl items-center gap-1 overflow-x-auto px-4 py-3 text-sm">
            <span className="mr-3 shrink-0 font-mono text-xs text-amber-400">echo://garrett</span>
            {nav.map((n) => (
              <Link key={n.href} href={n.href} className="shrink-0 rounded-md px-3 py-1.5 text-neutral-400 transition hover:bg-neutral-800 hover:text-white">
                {n.label}
              </Link>
            ))}
          </nav>
        </header>
        <main className="mx-auto max-w-4xl px-4 py-8">{children}</main>
        <footer className="mx-auto max-w-4xl px-4 py-10 text-xs text-neutral-600">
          Built by Garrett C. Gauthier. The Avatar is a voice model shaped from his own words — not the real person, and not a login. Made with Claude (Anthropic) in Claude Code.
        </footer>
      </body>
    </html>
  );
}
