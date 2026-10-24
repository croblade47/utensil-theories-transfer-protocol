#!/usr/bin/env python3
"""
Pig-Latin Airlock simulation.

Models the mantrap + per-principal cipher pattern described in
docs/examples ... summary in METAPHOR_SECURITY_FRAMEWORK section 5.

Deterministic. No randomness. Pure functions.
Run: python3 -I sims/pig_latin_airlock_sim.py
"""

from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field, asdict


# ---------- building blocks ----------

PAINT_SALT = b"airlock-v1"


def paint(badge_id: str, event_hash: str, variant: str) -> str:
    h = hashlib.sha256(
        PAINT_SALT + badge_id.encode() + event_hash.encode() + variant.encode()
    )
    return "PAINT-" + h.hexdigest()[:16].upper()


def event_hash(label: str, principal: str, phase: str) -> str:
    return hashlib.sha256(f"{label}|{principal}|{phase}".encode()).hexdigest()[:12]


# ---------- principal cards (per-employee cipher variants) ----------

CARDS = {
    # badge_id -> (variant_name, correct_phrase_phase2, correct_phrase_phase3)
    "alice":   ("alpha",   "upay-ownday-eftlay",      "oorday-opensway"),
    "bob":     ("bravo",   "ightray-eftlay-upay",     "allway-urnstay"),
    "carol":   ("charlie", "orthnay-outhsay-eastway", "ingkay-eetsmay-ouyay"),
}

CURRENT_ROTATION = "r42"  # changes periodically; stale phrases fail


# ---------- airlock ----------

@dataclass
class AirlockResult:
    attacker_profile: str
    badge_valid: bool
    reached_phase2: bool
    reached_phase3: bool
    reached_data_room: bool
    trapped_in_vestibule: str   # which vestibule, or ""
    painted: bool
    paint_marker: str
    verdict: str                # "caught", "stopped", "through"


def run_attempt(
    profile: str,
    badge_id: str,
    offered_phase2: str,
    offered_phase3: str,
    *,
    endpoint_compromised: bool = False,
) -> AirlockResult:
    # Phase 1 — front door (possession check)
    badge_valid = badge_id in CARDS

    if not badge_valid:
        return AirlockResult(
            attacker_profile=profile,
            badge_valid=False,
            reached_phase2=False, reached_phase3=False, reached_data_room=False,
            trapped_in_vestibule="",
            painted=False, paint_marker="",
            verdict="stopped",
        )

    variant, correct_p2, correct_p3 = CARDS[badge_id]

    # Enter vestibule 1 — always painted on entry
    eh2 = event_hash("vestibule1", badge_id, "phase2")
    marker = paint(badge_id, eh2, variant + ":" + CURRENT_ROTATION)

    # Phase 2 — knowledge check against principal's current card
    phase2_ok = (offered_phase2 == correct_p2)

    if not phase2_ok:
        # Endpoint-compromised attacker reads the challenge off the user's
        # live screen; they would only know phase 2 if that's where the
        # mid-session user currently is.
        return AirlockResult(
            attacker_profile=profile,
            badge_valid=True,
            reached_phase2=True, reached_phase3=False, reached_data_room=False,
            trapped_in_vestibule="v1",
            painted=True, paint_marker=marker,
            verdict="caught",
        )

    # Enter vestibule 2
    eh3 = event_hash("vestibule2", badge_id, "phase3")
    marker2 = paint(badge_id, eh3, variant + ":" + CURRENT_ROTATION)

    phase3_ok = (offered_phase3 == correct_p3)

    if not phase3_ok:
        return AirlockResult(
            attacker_profile=profile,
            badge_valid=True,
            reached_phase2=True, reached_phase3=True, reached_data_room=False,
            trapped_in_vestibule="v2",
            painted=True, paint_marker=marker + "|" + marker2,
            verdict="caught",
        )

    # Through
    return AirlockResult(
        attacker_profile=profile,
        badge_valid=True,
        reached_phase2=True, reached_phase3=True, reached_data_room=True,
        trapped_in_vestibule="",
        painted=True, paint_marker=marker + "|" + marker2,
        verdict="through",
    )


# ---------- attacker profiles ----------

PROFILES = [
    # (profile, badge_id, offered_p2, offered_p3, endpoint_compromised)
    ("Legitimate user (alice)",
     "alice", "upay-ownday-eftlay", "oorday-opensway", False),

    ("Badge only (phished Alice's badge, no card)",
     "alice", "", "", False),

    ("Badge + guessed single phrase",
     "alice", "random-guess-phrase", "", False),

    ("Badge + full card from DIFFERENT principal (used Bob's card w/ Alice's badge)",
     "alice", "ightray-eftlay-upay", "allway-urnstay", False),

    ("Badge + Alice's full card (physical theft)",
     "alice", "upay-ownday-eftlay", "oorday-opensway", False),

    ("Badge + phished phrase, dialect rotated since",
     "alice", "old-rotation-phrase", "", False),

    ("Badge + endpoint compromise mid-session (user at phase 2 only)",
     "alice", "upay-ownday-eftlay", "guessed-wrong-p3", True),

    ("No valid badge",
     "unknown-badge", "upay-ownday-eftlay", "oorday-opensway", False),
]


# ---------- runner ----------

def main() -> None:
    results = []
    for profile, badge, p2, p3, endpoint in PROFILES:
        r = run_attempt(profile, badge, p2, p3, endpoint_compromised=endpoint)
        results.append(r)

    print(f"{'Profile':<60}{'Verdict':<10}{'Vestibule':<12}{'Painted'}")
    print("-" * 100)
    for r in results:
        print(
            f"{r.attacker_profile[:58]:<60}"
            f"{r.verdict:<10}"
            f"{r.trapped_in_vestibule or '-':<12}"
            f"{'yes' if r.painted else 'no'}"
        )

    attackers = [r for r in results if not r.attacker_profile.startswith("Legitimate")]
    caught = sum(1 for r in attackers if r.verdict == "caught")
    stopped = sum(1 for r in attackers if r.verdict == "stopped")
    through = sum(1 for r in attackers if r.verdict == "through")
    painted = sum(1 for r in attackers if r.painted)

    print("-" * 100)
    print(f"Attacker profiles: {len(attackers)}")
    print(f"  Caught in a vestibule: {caught}")
    print(f"  Stopped at front door: {stopped}")
    print(f"  Through to data room:  {through}")
    print(f"  Painted:               {painted}/{len(attackers)}")
    viability = round(100 * (caught + stopped) / len(attackers), 1)
    print(f"Viability vs. tested profiles: {viability}%")

    with open("sims/pig_latin_airlock_results.json", "w") as f:
        json.dump({
            "results": [asdict(r) for r in results],
            "summary": {
                "attacker_profiles": len(attackers),
                "caught": caught,
                "stopped": stopped,
                "through": through,
                "painted": painted,
                "viability_pct": viability,
            },
        }, f, indent=2)


if __name__ == "__main__":
    main()
