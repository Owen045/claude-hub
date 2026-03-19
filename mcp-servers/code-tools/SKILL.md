---
name: code-tools-mcp
description: >
  Context for working on the code-tools MCP server.
  Provides repo analysis tools: file search, symbol lookup, dependency graph.
---

# Code Tools MCP Server

## What It Does
Provides code analysis capabilities as MCP tools, allowing Claude to search and
understand codebases without file-by-file reads.

## Planned Tools

| Tool | Description |
|---|---|
| `search_code` | Grep-style search across the repo |
| `get_symbol` | Find definition of a function/class/variable |
| `list_dependencies` | List imports and dependencies for a module |
| `summarise_file` | Return structure summary (classes, functions) of a file |
