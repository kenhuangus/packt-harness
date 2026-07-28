# Module 7: Skills, Plugins & Model Context Protocol (MCP)

## Overview

This module demonstrates three real Claude Code extension mechanisms: Agent
Skills, subagents packaged in plugins, and a Model Context Protocol client/server
exchange.

## Agent Skill

`skills/spec-check/SKILL.md` uses documented frontmatter. A skill's
`description` tells Claude what it does and when to load it; there is no
`triggers` field. Project skills normally live under
`.claude/skills/<name>/SKILL.md`, while plugin skills live under `skills/`.

## Subagent

`agents/spec-reviewer.md` is a read-only reviewer with its own context window.
Claude Code project subagents normally live under `.claude/agents/`; a plugin
can bundle them under `agents/`.

## Plugin

`.claude-plugin/plugin.json` is the plugin manifest. The manifest is not a bare
`plugin.json` at the plugin root. Plugins can bundle skills, agents, hooks, MCP
servers, LSP servers, and monitors.

## Real MCP stdio Demo

This machine has version `2.0.0` of the MCP Python SDK package installed. In
that SDK line, the server class is `MCPServer`:

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Harness-Enterprise-Tools")


@mcp.tool()
def query_database_record(record_id: int) -> str:
    return f"DB_RECORD #{record_id}"


@mcp.resource("config://app-settings")
def app_settings() -> str:
    return '{"environment": "production"}'


if __name__ == "__main__":
    mcp.run()  # stdio is the default transport
```

`mcp_client_runner.py` starts `mcp_server_demo.py` in a separate Python
subprocess, creates a `ClientSession`, initializes the session, and invokes
`list_tools()`, `call_tool()`, `list_resources()`, and `read_resource()` over
stdio.

Run it from the repository root:

```powershell
& 'C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe' 'course_implementation\module_07_skills_plugins_mcp\mcp_client_runner.py'
```

The MCP protocol uses dated revisions, such as `2025-06-18`; it does not use a
`2.0` protocol version. JSON-RPC 2.0 is the message framing version, while
`2.0.0` here is the Python SDK package version. Local servers commonly use
stdio. Remote servers use Streamable HTTP; HTTP+SSE is its legacy predecessor.

The course LLM client remains part of the demo. If its configured endpoint is
not reachable, the MCP exchange still runs and the optional synthesis step
prints a clear `[SKIPPED]` result.
