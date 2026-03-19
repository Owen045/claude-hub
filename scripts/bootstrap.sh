#!/usr/bin/env bash
set -euo pipefail

echo "=== claude-central bootstrap ==="

# Check prerequisites
command -v uv >/dev/null 2>&1 || { echo "uv not found. Install: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "node not found. Install via https://nodejs.org"; exit 1; }
command -v pnpm >/dev/null 2>&1 || { echo "pnpm not found. Install: npm install -g pnpm"; exit 1; }

# Copy .env if not present
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example — fill in your API keys."
fi

# Install Python workspace
echo ""
echo "--- Installing Python packages ---"
uv sync --all-packages

# Install Node packages (infra)
echo ""
echo "--- Installing Node packages ---"
pnpm install

echo ""
echo "=== Bootstrap complete ==="
echo ""
echo "Next steps:"
echo "  1. Fill in .env with your API keys"
echo "  2. cd mcp-servers/knowledge-base && uv run fastmcp dev src/knowledge_base/server.py"
echo "  3. Run evals: ./scripts/run_evals.sh"
