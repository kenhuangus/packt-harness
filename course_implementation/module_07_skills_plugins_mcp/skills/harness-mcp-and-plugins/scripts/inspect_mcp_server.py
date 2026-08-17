"""MCP 2.x Server Inspector."""
from __future__ import annotations

import asyncio
import os
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "pyproject.toml").is_file() or (candidate / ".git").exists():
            return candidate
    raise RuntimeError("repository root not found from " + str(start))


async def inspect(server_script: str | None = None) -> int:
    if server_script is None:
        repo_root = find_repo_root(Path(__file__).resolve().parent)
        server_path = repo_root / "course_implementation" / "module_07_skills_plugins_mcp" / "mcp_server_demo.py"
        server_script = str(server_path.resolve())

    params = StdioServerParameters(
        command=sys.executable,
        args=[server_script],
        env=dict(os.environ),
    )
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            resources = await session.list_resources()
            tool_names = [t.name for t in tools.tools]
            resource_uris = [r.uri for r in resources.resources]
            print(f"[PASS] Connected to MCP server. Tools: {tool_names}, Resources: {resource_uris}")
            return 0


def root_cause(exc: BaseException) -> str:
    while isinstance(exc, BaseExceptionGroup) and exc.exceptions:
        exc = exc.exceptions[0]
    return f"{type(exc).__name__}: {exc}"


def main() -> int:
    server_path = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        return asyncio.run(inspect(server_path))
    except Exception as exc:
        print(f"[FAIL] Could not inspect MCP server: {root_cause(exc)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
