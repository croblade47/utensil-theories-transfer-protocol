# START HERE: Seed Test (20 October 2026)

## What this folder is
A small, fair test for any seed-and-grow method. It needs no AI: just Python on any computer.

## How to use it
1. Open `seed_test.py`.
2. Put your rules into `plant()` (data to seed) and `grow()` (seed to data).
3. Run `python seed_test.py`, optionally followed by your own files, for example `python seed_test.py photo.jpg letter.txt`.

## What the test does
- **Counts** the size of each seed in raw bytes.
- **Checks** that the regrown file matches the original exactly (a SHA-256 fingerprint).
- **Grows each seed in a separate process** that never sees the original.
- **Includes random bytes,** the hardest possible case.

## Files

| File | What it is |
|---|---|
| `seed_test.py` | The test. Until your rules are added, it uses ordinary zip compression as an example |
| `SEED_TEST_2026-10-20.zip` | This folder as a zip (next to the folder) |

The repository is public.
