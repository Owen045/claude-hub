#!/usr/bin/env bash
set -euo pipefail

echo "=== MCP Server Benchmarks ==="

bench_server() {
  local name="$1"
  local bench_module="$2"
  echo ""
  echo "--- $name ---"
  uv run python "$bench_module"
}

bench_server "knowledge-base" "mcp-servers/knowledge-base/benchmarks/bench_tools.py"
# bench_server "code-tools" "mcp-servers/code-tools/benchmarks/bench_tools.py"

echo ""
echo "=== Benchmark complete ==="
