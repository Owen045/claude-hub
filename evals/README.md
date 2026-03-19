# Evals

Lightweight eval framework and test suites for measuring AI system quality.

## Philosophy
Build your own eval runner before adopting a framework — this forces you to
understand what evals *are*: (input, expected) → (score, pass/fail).

## Framework (`framework/`)

| Module | Purpose |
|---|---|
| `runner.py` | Async parallel eval runner |
| `scorers.py` | LLM-as-judge, exact match, semantic similarity |
| `datasets.py` | JSONL dataset loading utilities |
| `reporter.py` | Results output (JSON, HTML, Weights & Biases) |

## Eval Suites (`suites/`)

| Suite | What It Measures | Cases |
|---|---|---|
| `prompt_quality` | LLM response quality for key prompts | 10 |
| `mcp_tool_accuracy` | MCP tool call correctness | 10 |
| `agent_task_completion` | Multi-agent task completion rate | 5 |

## Running

```bash
# Run a specific suite
cd evals
uv run python -m suites.prompt_quality.eval

# Run all suites
../scripts/run_evals.sh
```

## Adding a New Suite

1. Create `suites/my_suite/dataset.jsonl` with `{id, input, expected}` lines.
2. Create `suites/my_suite/eval.py` using `run_eval_suite` from the framework.
3. Add to `scripts/run_evals.sh`.

## Pass Rate Targets

All suites must maintain ≥ 80% pass rate in CI.
