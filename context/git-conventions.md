# Git Conventions

## Branch Naming
```
feat/short-description       # New feature
fix/short-description        # Bug fix
chore/short-description      # Maintenance, deps, config
eval/short-description       # Eval suite additions or improvements
docs/short-description       # Documentation only
refactor/short-description   # Refactoring without feature change
```

## Commit Format (Conventional Commits)
```
<type>(<scope>): <short summary>

[optional body]

[optional footer: BREAKING CHANGE, Closes #123]
```

### Types
| Type | When to Use |
|---|---|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `chore` | Build, deps, tooling, config |
| `docs` | Documentation only |
| `refactor` | Code change without feature/fix |
| `test` | Adding or fixing tests |
| `eval` | Eval dataset or suite changes |
| `perf` | Performance improvement |
| `ci` | CI/CD pipeline changes |

### Scopes (this repo)
`mcp`, `agents`, `workflows`, `evals`, `mlops`, `infra`, `skills`, `context`

### Examples
```
feat(mcp): add ingest_document tool to knowledge-base server
fix(evals): handle empty dataset.jsonl gracefully
chore(infra): upgrade aws-cdk-lib to 2.140.0
eval(mcp): add 5 retrieval accuracy cases for search_documents
```

## Pull Request Standards
- PR title follows Conventional Commits format.
- PR description includes: what changed, why, how to test.
- All CI checks must pass before merge.
- At least one passing eval suite required for feat/fix PRs touching AI code.
- Squash merge to keep main history clean.

## Branch Protection (main)
- Require PR + review for all merges.
- Require status checks: lint, typecheck, tests, evals.
- No direct pushes to main.
