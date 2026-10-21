#!/bin/bash
# While the numbers test runs, copy its partial results into the delivery folder and commit + push every 10 minutes.
cd "$(dirname "$0")/../.."
PID=$1
D=NUMBERS_TEST_2026-10-21
BRANCH=ccr-1be0d913-1tlzao
save() {
  [ -f experiments/results_numbers.json ] && cp experiments/results_numbers.json $D/results/results_numbers.json
  [ -f experiments/results_numbers.txt ] && cp experiments/results_numbers.txt $D/results/results_numbers.txt
  git add experiments/results_numbers.json experiments/results_numbers.txt $D/results $D/logs/full_run_log.txt 2>/dev/null
  if ! git diff --cached --quiet; then
    git commit -q -m "Numbers test: partial results ($1)

Claude-Session: https://claude.ai/code/session_01VCh7XeJpj5JpCzQtSzh7gK"
    for wait in 2 4 8 16; do
      git pull -q --rebase --autostash origin $BRANCH && git push -q origin $BRANCH && break
      sleep $wait
    done
    echo "$(date -u +%H:%M:%S) saved ($1)"
  fi
}
while kill -0 "$PID" 2>/dev/null; do
  sleep 600
  save auto-save
done
save "run ended"
