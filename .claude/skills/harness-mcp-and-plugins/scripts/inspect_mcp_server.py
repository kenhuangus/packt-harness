"""MCP 2.x Server Inspector."""
from __future__ import annotations

import asyncio
import os
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def inspect(server_script: str | None = None) -> int:
    if server_script is None:
        here = Path(__file__).resolve()
        if ".claude" in here.parts:
            repo_root = here.parents[4]
            server_path = repo_root / "course_implementation" / "module_07_skills_plugins_mcp" / "mcp_server_demo.py"
        else:
            server_path = here.parents[3] / "mcp_server_demo.py"
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


def main() -> int:
    server_path = sys.argv[1] if len(sys.argv) > 1 else None
    return asyncio.run(inspect(server_path))


if __name__ == "__main__":
    sys.exit(main())
