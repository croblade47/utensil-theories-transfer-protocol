export default function GuardDog() {
  return (
    <div className="prose prose-invert max-w-none prose-headings:text-white prose-a:text-amber-400">
      <h1>The Guard Dog Protocol</h1>
      <p className="lead text-neutral-300">
        The idea: a system shouldn&apos;t make you remember a dozen passwords that attackers can guess
        or phish anyway. Instead it knows <em>you</em> — the way a dog knows its owner — from how you
        behave, and it treats an impostor the way a dog treats a stranger at the gate.
      </p>

      <h2>The concept, in Garrett&apos;s frame</h2>
      <p>
        An Echo (the voice/behavior model on this site) plus biometrics and other signals build a
        picture of a person. When something acts out of character, the system doesn&apos;t slam a door —
        it does what the Metaphor-Driven Security work describes: opens the door, floods the attacker
        with motion, and marks them with &quot;bright red paint&quot; so they&apos;re easy to see and can&apos;t move
        cleanly. Confusion and psychology where a wall won&apos;t hold.
      </p>

      <h2>What this actually is good for</h2>
      <ul>
        <li><strong>A risk signal, not a lock.</strong> &quot;Does this session behave like the real person?&quot;
          is a genuine, used-in-industry idea — it&apos;s called behavioral biometrics and anomaly
          detection. It&apos;s great as <em>one</em> input that raises or lowers suspicion.</li>
        <li><strong>A honeypot / deception layer.</strong> The &quot;flood and mark the attacker&quot; idea maps
          onto real deception defense: tarpits, honeytokens, canary credentials. That part is sound
          and worth building out.</li>
        <li><strong>A friendlier front door.</strong> Using behavior to decide <em>when</em> to ask for a
          second check (step-up auth) is exactly how good modern systems already reduce password pain.</li>
      </ul>

      <h2>The honest caveat (you asked me to be straight)</h2>
      <p>
        A personality avatar <strong>cannot replace</strong> passwords or a second factor as the thing that
        proves who you are. Three reasons, plainly:
      </p>
      <ul>
        <li><strong>It&apos;s copyable.</strong> This whole site builds a convincing you out of your public
          words. Anything learnable from your behavior is also learnable by an attacker with the same
          data. A secret you hold (a key, a passkey) is not.</li>
        <li><strong>It&apos;s fuzzy.</strong> &quot;Sounds like Garrett&quot; is a probability, not a yes/no. Auth needs a
          hard gate somewhere. Fuzzy signals belong <em>around</em> that gate, deciding how hard to push,
          not <em>as</em> the gate.</li>
        <li><strong>Biometrics don&apos;t reset.</strong> If a password leaks you change it. If your face or
          typing model leaks, you can&apos;t get a new face. So biometrics are a convenience factor, never
          the only one.</li>
      </ul>
      <p>
        On 2FA specifically: SMS codes are genuinely weak and worth retiring. But the fix the whole
        security field is moving to is <strong>passkeys</strong> (a secret your device holds and proves
        without ever sending it) — which is a <em>better</em> second factor, not the end of the idea.
        2FA done right is one of the few things that reliably stops the attacks that actually happen.
      </p>

      <h2>So what should Guard Dog be?</h2>
      <p>
        Build it as the <strong>layer around</strong> a passkey login, not a replacement for it:
      </p>
      <ol>
        <li>Passkey proves the secret (the hard gate).</li>
        <li>Echo + behavior score the session (the dog&apos;s nose): normal → stay quiet; off → ask for more.</li>
        <li>On a clear impostor, the deception layer kicks in: the honeypot room, the &quot;red paint&quot;
          marking, the slippery doorstep. You catch and watch instead of just blocking.</li>
      </ol>
      <p className="text-neutral-400">
        That version keeps everything you find exciting about the idea — the dog, the confusion, the
        story — and bolts it onto something that genuinely holds. That&apos;s the one worth engineering.
      </p>
    </div>
  );
}
