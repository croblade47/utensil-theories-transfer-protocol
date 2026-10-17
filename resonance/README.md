# Contextual Resonance Engine

A small, dependency-free Python module that reads the "weight" in a message
(regret, burden, moral breach, betrayal) and picks a response stance for a host AI.

It is a keyword heuristic for steering tone, not a judgment or diagnosis of the person.

```bash
python resonance_engine.py                      # demo
python resonance_engine.py "the guilt is heavy" # your own text
python resonance_engine.py --json "text"        # full JSON payload
python -m unittest -v                           # tests (run from this folder)
```

```python
from resonance_engine import ContextualResonanceEngine, EngineConfig
engine = ContextualResonanceEngine(EngineConfig(echo_input=False))
result = engine.process_input("I made a mistake")
result["subconscious_translation"]["stance"]  # "Course Correction / Forgiveness"
```

## Stances

| Stance | When |
|---|---|
| Neutral Observation | nothing detected |
| Course Correction / Forgiveness | light weight (deviation ≤ 0.40) |
| Active Load-Bearing (Atlas Protocol) | deviation > 0.40 |
| Hold Steady / Unconditional Grace (System Halt) | betrayal / "unforgivable" detected |

## Scoring

Each category scores its weight (repeats add 25% each, capped at 1.0). Categories
combine as `1 - Π(1 - score)`, so the index rises with more distinct burdens but
never pins at 100%. Negated words ("no guilt", "don't regret") are ignored and
reported in `negated_terms`. Every hit is listed in `evidence` with its position.
