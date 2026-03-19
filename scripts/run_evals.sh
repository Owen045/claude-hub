#!/usr/bin/env bash
set -euo pipefail

PASS_THRESHOLD=${PASS_THRESHOLD:-80}
FAILURES=0

run_suite() {
  local name="$1"
  local module="$2"
  echo ""
  echo "--- Running eval suite: $name ---"
  if uv run python -m "$module"; then
    echo "[PASS] $name"
  else
    echo "[FAIL] $name"
    FAILURES=$((FAILURES + 1))
  fi
}

echo "=== claude-central eval runner ==="

run_suite "prompt_quality"       "evals.suites.prompt_quality.eval"
run_suite "mcp_tool_accuracy"    "evals.suites.mcp_tool_accuracy.eval"
run_suite "agent_task_completion" "evals.suites.agent_task_completion.eval"

echo ""
echo "==================================="
if [ "$FAILURES" -gt 0 ]; then
  echo "FAILED: $FAILURES suite(s) did not pass."
  exit 1
else
  echo "All eval suites passed."
fi
