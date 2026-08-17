---
name: harness-mcp-and-plugins
description: Authors and consumes Model Context Protocol (MCP) 2.x SDK servers, exposing
  @mcp.tool() actions and @mcp.resource() URIs over stdio JSON-RPC, and bundles agent
  skills into .claude-plugin/plugin.json manifests. Trigger when building custom MCP
  servers, declaring read-only application resources, or configuring plugin manifests.
version: 1.0.0
author: Harness Engineering Team
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Harness MCP & Plugins

## Overview
Authors and consumes Model Context Protocol (MCP) 2.x SDK servers exposing typed tools and read-only resources over JSON-RPC stdio transports, bundled via Claude Plugin manifests.

## Structure & Progressive Disclosure
- `scripts/`: Executable helper and verification tools.
- `references/`: Detailed specifications, guides, and architectural rules.
- `assets/`: Configuration templates and machine-readable schemas.

## When to Use
- When creating custom MCP 2.x Python servers using `@mcp.tool()` and `@mcp.resource()`.
- When authoring `.claude-plugin/plugin.json` manifests to bundle skills and MCP servers.
- When inspecting tool and resource registrations over stdio communication.

## Required Inputs
- MCP server script path (`mcp_server_demo.py`).
- Plugin manifest configuration (`.claude-plugin/plugin.json`).

## Instructions
1. Declare executable actions using `@mcp.tool()` with typed docstrings.
2. Declare read-only state endpoints using `@mcp.resource("uri://...")`.
3. Execute `python scripts/inspect_mcp_server.py` to inspect tools and resources over stdio.
4. Bundle the server and skills into `.claude-plugin/plugin.json` using `assets/plugin_manifest_template.json`.
5. Consult `references/mcp-2x-spec.md` for MCP 2.x architectural guidelines.

## Output Format
Always format output adhering to this structure:
```json
{
  "server_name": "harness-mcp-server",
  "tools": ["verify_spec", "run_tests", "scan_secrets"],
  "resources": ["harness://metrics/live"],
  "transport": "stdio"
}
```

## Examples
### Declaring MCP Tools and Resources
```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("HarnessServer")

@mcp.tool()
def validate_code(code: str) -> bool:
    """Validates Python code syntax."""
    return True

@mcp.resource("harness://metrics/live")
def metrics_live() -> str:
    """Read-only application metrics endpoint."""
    return '{"status": "ok"}'
```

## Key Implementation Links (GitHub)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-mcp-and-plugins/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-mcp-and-plugins/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-mcp-and-plugins/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-mcp-and-plugins/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_07_skills_plugins_mcp/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_07_skills_plugins_mcp/)
