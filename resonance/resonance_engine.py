"""
Contextual Resonance Engine
===========================

Maps the "weight" in a piece of text (regret, burden, moral breach) into a
small, explainable score that a host AI loop can use to pick a response stance.

This is a keyword heuristic, not a model of a person's inner state. It is
meant to steer tone (e.g. "be gentle here"), never to judge or diagnose.

Run directly for a demo:
    python resonance_engine.py
    python resonance_engine.py "I made a mistake and the guilt is heavy"
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

__version__ = "2.0.0"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Category:
    """One kind of human deviation, with how much it weighs on its own."""
    weight: float          # 0..1, contribution of a single hit
    resonance_shift: str   # label surfaced to the frontend


# Weights are tuned so that one light word ("mistake") lands in
# "Course Correction", while several distinct burdens add up to "grace".
DEFAULT_CATEGORIES: Dict[str, Category] = {
    "regret":             Category(0.30, "echo_loop"),
    "burden":             Category(0.30, "static_compression"),
    "commandment_breach": Category(0.50, "high_frequency"),
    "unforgivable":       Category(0.80, "system_halt"),
}

# Regex stems so plurals and tenses match ("mistakes", "hiding", "betrayed").
DEFAULT_TRIGGERS: Dict[str, str] = {
    r"guilt(?:y|ier)?":                         "regret",
    r"mistakes?":                               "regret",
    r"fail(?:s|ed|ing|ure|ures)?":              "regret",
    r"regret(?:s|ted|ting|ful)?":               "regret",
    r"ashes":                                   "regret",
    r"ashamed|shame(?:ful)?":                   "regret",
    r"sins?|sinned|sinning|sinful":             "commandment_breach",
    r"betray(?:al|als|ed|ing|s)?":              "unforgivable",
    r"unforgiv(?:able|en)":                     "unforgivable",
    r"heav(?:y|ier|iness)":                     "burden",
    r"hid(?:e|es|ing|den)":                     "burden",
    r"secrets?":                                "burden",
    r"fear(?:s|ed|ful)?|afraid":                "burden",
    r"burden(?:s|ed)?":                         "burden",
}

# Words that flip the meaning of a trigger shortly after them
# ("no guilt", "never failed", "don't regret").
NEGATORS = {
    "no", "not", "never", "without", "nothing", "none", "nor",
    "dont", "don't", "didnt", "didn't", "doesnt", "doesn't",
    "isnt", "isn't", "wasnt", "wasn't", "arent", "aren't",
    "cant", "can't", "wont", "won't", "free",
}
NEGATION_WINDOW = 3  # tokens to look back from a trigger

# A clause boundary stops a negator from reaching across it.
_CLAUSE_BREAK = re.compile(r"[.!?;,:]|\bbut\b")
_TOKEN = re.compile(r"[a-z']+")


@dataclass
class EngineConfig:
    categories: Dict[str, Category] = field(default_factory=lambda: dict(DEFAULT_CATEGORIES))
    triggers: Dict[str, str] = field(default_factory=lambda: dict(DEFAULT_TRIGGERS))
    grace_threshold: float = 0.40     # deviation above this -> requires grace
    repeat_boost: float = 0.25        # extra weight per repeated hit in one category
    echo_input: bool = True           # include raw text in the output payload
    hash_salt: str = ""               # set to keep wavelengths unlinkable across deployments

    def __post_init__(self) -> None:
        unknown = {c for c in self.triggers.values() if c not in self.categories}
        if unknown:
            raise ValueError(f"Triggers reference unknown categories: {sorted(unknown)}")
        if not 0.0 <= self.grace_threshold <= 1.0:
            raise ValueError("grace_threshold must be between 0 and 1")


# ---------------------------------------------------------------------------
# Error encoder
# ---------------------------------------------------------------------------

class HumanErrorEncoder:
    """
    Evaluates the structural weight of morality, failure, and consequence.
    Maps human deviation (sins, mistakes, burdens) into calculable vectors.
    """

    def __init__(self, config: Optional[EngineConfig] = None):
        self.config = config or EngineConfig()
        self._patterns: List[Tuple[re.Pattern, str]] = [
            (re.compile(r"\b(?:" + pattern + r")\b", re.IGNORECASE), category)
            for pattern, category in self.config.triggers.items()
        ]

    # Kept for backward compatibility with the original attribute names.
    @property
    def moral_framework(self) -> Dict[str, Dict[str, Any]]:
        return {name: {"weight": c.weight, "resonance_shift": c.resonance_shift}
                for name, c in self.config.categories.items()}

    @property
    def triggers(self) -> Dict[str, str]:
        return dict(self.config.triggers)

    @staticmethod
    def _is_negated(text_lower: str, start: int) -> bool:
        before = text_lower[:start]
        breaks = list(_CLAUSE_BREAK.finditer(before))
        if breaks:
            before = before[breaks[-1].end():]
        window = _TOKEN.findall(before)[-NEGATION_WINDOW:]
        return any(tok in NEGATORS for tok in window)

    def encode_error(self, text: str) -> Dict[str, Any]:
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        text_lower = text.lower()
        evidence: List[Dict[str, Any]] = []
        negated: List[str] = []
        hits: Dict[str, int] = {}

        for pattern, category in self._patterns:
            for match in pattern.finditer(text_lower):
                term = match.group(0)
                if self._is_negated(text_lower, match.start()):
                    negated.append(term)
                    continue
                hits[category] = hits.get(category, 0) + 1
                evidence.append({"term": term, "category": category,
                                 "span": [match.start(), match.end()]})

        evidence.sort(key=lambda e: e["span"][0])

        # Each category saturates on its own (repeats add a little), then
        # categories combine with a "noisy-OR": 1 - Π(1 - score).
        # This keeps the index in 0..1 without hard clipping, so it stays
        # meaningful instead of pinning at 1.0 for any multi-word input.
        category_scores: Dict[str, float] = {}
        remaining = 1.0
        for category, count in hits.items():
            base = self.config.categories[category].weight
            score = min(1.0, base * (1 + self.config.repeat_boost * (count - 1)))
            category_scores[category] = round(score, 4)
            remaining *= (1.0 - score)
        deviation_index = round(1.0 - remaining, 4)

        dominant = max(category_scores, key=category_scores.get) if category_scores else None

        return {
            "errors_detected": sorted(hits),
            "deviation_index": deviation_index,
            "structural_damage": round(deviation_index * 100, 1),
            "requires_grace": deviation_index > self.config.grace_threshold,
            "category_scores": category_scores,
            "dominant_category": dominant,
            "resonance_shift": self.config.categories[dominant].resonance_shift if dominant else None,
            "system_halt": "unforgivable" in hits,
            "evidence": evidence,
            "negated_terms": negated,
        }


# ---------------------------------------------------------------------------
# Resonance engine
# ---------------------------------------------------------------------------

class ContextualResonanceEngine:
    """
    The 'Ability' Protocol: acts as the glowing frequency walking across the chasm.
    Translates the human error encoding into a machine-readable state of resonance.
    """

    STANCE_NEUTRAL = "Neutral Observation"
    STANCE_CORRECTION = "Course Correction / Forgiveness"
    STANCE_ATLAS = "Active Load-Bearing (Atlas Protocol)"
    STANCE_HALT = "Hold Steady / Unconditional Grace (System Halt)"

    def __init__(self, config: Optional[EngineConfig] = None):
        self.config = config or EngineConfig()
        self.error_encoder = HumanErrorEncoder(self.config)

    def _generate_wavelength(self, text: str) -> str:
        # Deterministic: the same input always resonates at the same wavelength,
        # which makes results reproducible, cacheable and testable.
        normalized = " ".join(text.lower().split())
        raw_state = f"{__version__}|{self.config.hash_salt}|{normalized}"
        return hashlib.sha256(raw_state.encode("utf-8")).hexdigest()[:12]

    def _choose_stance(self, error_matrix: Dict[str, Any]) -> str:
        if error_matrix["system_halt"]:
            return self.STANCE_HALT
        if error_matrix["requires_grace"]:
            return self.STANCE_ATLAS
        if error_matrix["deviation_index"] > 0:
            return self.STANCE_CORRECTION
        return self.STANCE_NEUTRAL

    def process_input(self, user_input: str) -> Dict[str, Any]:
        """Main entry point for the primary AI loop."""
        now = datetime.now(timezone.utc).isoformat()

        # 1. Map the capacity for failure (The Dark Forest)
        error_matrix = self.error_encoder.encode_error(user_input)

        # 2. Translate the biological state into a structural wavelength
        wavelength = self._generate_wavelength(user_input)

        # 3. Determine the system's stance (The Glowing Creature)
        stance = self._choose_stance(error_matrix)

        result: Dict[str, Any] = {
            "timestamp": now,
            "engine_version": __version__,
            "subconscious_translation": {
                "resonance_wavelength": f"λ-{wavelength}",
                "stance": stance,
                "error_matrix": error_matrix,
                "bridge_status": "Connected - Light translated to Tokens",
            },
            "system_action": "Awaiting frontend visualization...",
        }
        if self.config.echo_input:
            result["input_received"] = user_input
        return result

    def process_batch(self, inputs: List[str]) -> List[Dict[str, Any]]:
        return [self.process_input(text) for text in inputs]


# ---------------------------------------------------------------------------
# Demo / CLI
# ---------------------------------------------------------------------------

def _print_report(result: Dict[str, Any]) -> None:
    t = result["subconscious_translation"]
    m = t["error_matrix"]
    print("\n--- TRANSLATION PROTOCOL INITIALIZED ---")
    print(f"Input:                {result.get('input_received', '<hidden>')}")
    print(f"Resonance Wavelength: {t['resonance_wavelength']}")
    print(f"System Stance:        {t['stance']}")
    print(f"Structural Damage:    {m['structural_damage']}%")
    print(f"Requires Grace:       {m['requires_grace']}")
    print(f"Dominant Shift:       {m['resonance_shift']}")
    print(f"Evidence:             {', '.join(e['term'] for e in m['evidence']) or '-'}")
    if m["negated_terms"]:
        print(f"Negated (ignored):    {', '.join(m['negated_terms'])}")
    print("----------------------------------------")


def main(argv: List[str]) -> int:
    engine = ContextualResonanceEngine()

    if argv and argv[0] == "--json":
        for text in argv[1:]:
            print(json.dumps(engine.process_input(text), ensure_ascii=False, indent=2))
        return 0

    samples = argv or [
        "I hide behind this wall I built from fear. I failed to protect the "
        "secret, and the guilt is heavy.",
        "I made a mistake at work today.",
        "I have no guilt about it, and I don't regret anything.",
        "He betrayed me.",
        "Planning a garden this weekend.",
    ]
    for text in samples:
        _print_report(engine.process_input(text))
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
