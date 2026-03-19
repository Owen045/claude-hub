"""
Code Tools MCP Server.
Provides repo analysis tools: file search, symbol lookup, dependency listing.
Run locally: fastmcp dev src/code_tools/server.py
"""
from __future__ import annotations

import ast
import os
import subprocess
from pathlib import Path

import structlog
from fastmcp import FastMCP
from pydantic import BaseModel, Field

from code_tools import __version__

log = structlog.get_logger().bind(service="code-tools", version=__version__)

mcp = FastMCP(
    name="code-tools",
    version=__version__,
    instructions=(
        "Repo analysis tools for searching and understanding code. "
        "Use search_code for grep-style search, get_file_symbols to see "
        "the structure of a Python file."
    ),
)


class SearchInput(BaseModel):
    pattern: str = Field(..., description="Search pattern (regex supported)")
    path: str = Field(".", description="Directory to search in")
    file_glob: str = Field("*.py", description="File pattern to restrict search")
    max_results: int = Field(20, ge=1, le=100)


class FileInput(BaseModel):
    file_path: str = Field(..., description="Absolute or repo-relative path to a Python file")


@mcp.tool()
async def search_code(input: SearchInput) -> list[dict]:
    """
    Search the codebase for a pattern using ripgrep.
    Returns a list of {file, line, content} matches.
    Use this to find where a function is defined, called, or a pattern is used.
    """
    try:
        result = subprocess.run(
            ["rg", "--json", "-g", input.file_glob, "-m", str(input.max_results),
             input.pattern, input.path],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except FileNotFoundError:
        raise RuntimeError("ripgrep (rg) not installed — run: brew install ripgrep")

    matches = []
    for line in result.stdout.splitlines():
        import json
        try:
            obj = json.loads(line)
            if obj.get("type") == "match":
                data = obj["data"]
                matches.append({
                    "file": data["path"]["text"],
                    "line": data["line_number"],
                    "content": data["lines"]["text"].strip(),
                })
        except (json.JSONDecodeError, KeyError):
            continue
    return matches


@mcp.tool()
async def get_file_symbols(input: FileInput) -> dict:
    """
    Parse a Python file and return its top-level structure.
    Returns {classes: [...], functions: [...], imports: [...]}.
    Use this to quickly understand the shape of a module.
    """
    path = Path(input.file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {input.file_path}")

    source = path.read_text()
    tree = ast.parse(source)

    classes = []
    functions = []
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "line": node.lineno,
                "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
            })
        elif isinstance(node, ast.FunctionDef) and isinstance(node.col_offset, int) and node.col_offset == 0:
            functions.append({"name": node.name, "line": node.lineno})
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))

    return {"classes": classes, "functions": functions, "imports": imports[:20]}


def main() -> None:
    transport = os.getenv("TRANSPORT", "stdio")
    port = int(os.getenv("PORT", "8081"))
    if transport == "sse":
        mcp.run(transport="sse", port=port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
