#!/bin/bash
# Start the full numbers test detached from the shell, and a saver that commits partial results every 10 minutes.
# Usage: bash NUMBERS_TEST_2026-10-21/code/run_full.sh   (from the repository top level)
set -e
cd "$(dirname "$0")/../.."
REPO=$(pwd)
D=NUMBERS_TEST_2026-10-21
LOG=$D/logs/full_run_log.txt
cd experiments
setsid nohup env PYTHONUNBUFFERED=1 python numbers_test.py >> "$REPO/$LOG" 2>&1 < /dev/null &
PID=$!
echo "$PID" > "$REPO/$D/logs/full_run.pid"
cd "$REPO"
setsid nohup bash "$D/code/autosave.sh" "$PID" >> "$REPO/$D/logs/autosave_log.txt" 2>&1 < /dev/null &
echo "numbers_test.py running as PID $PID; log $LOG"
