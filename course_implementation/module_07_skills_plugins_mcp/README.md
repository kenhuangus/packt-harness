# Module 7: Skills, Plugins, and MCP

## What this module teaches

Claude Code is extended three ways that are easy to confuse. This module
keeps them separate and then runs a real Model Context Protocol session.

### Agent Skill

`C:\Users\kenhu\packt-harness\course_implementation\module_07_skills_plugins_mcp\skills\spec-check\SKILL.md`

A skill's `description` tells Claude what it does and when to load it.
There is no `triggers` field. Project skills normally live under
`.claude/skills/<name>/SKILL.md`. Plugin skills live under `skills/`.

### Subagent

`C:\Users\kenhu\packt-harness\course_implementation\module_07_skills_plugins_mcp\agents\spec-reviewer.md`

A read-only reviewer with its own context window. Project subagents live
under `.claude/agents/`. A plugin can bundle them under `agents/`.

### Plugin

`C:\Users\kenhu\packt-harness\course_implementation\module_07_skills_plugins_mcp\.claude-plugin\plugin.json`

The manifest is `.claude-plugin/plugin.json`, not a bare `plugin.json`
at the plugin root. Plugins can bundle skills, agents, hooks, MCP
servers, LSP servers, and monitors.

### MCP (the runnable demo)

`mcp_client_runner.py` starts `mcp_server_demo.py` as a child process and
speaks JSON-RPC over stdio. It initializes the session, lists tools,
calls `query_database_record(4092)`, lists resources, and reads
`config://app-settings`.

Protocol versioning: MCP uses dated revisions such as `2025-06-18`.
`2.0.0` on this machine is the **Python SDK package** version. JSON-RPC
2.0 is the message framing. They are three different numbers.

Local servers use stdio. Remote servers use Streamable HTTP. HTTP+SSE is
the legacy predecessor.

The LLM synthesis step calls the local vLLM model and must return a live
reply. If `http://127.0.0.1:8000/v1` is down, this module fails.

## Files

| Path | Role |
| --- | --- |
| `C:\Users\kenhu\packt-harness\course_implementation\module_07_skills_plugins_mcp\mcp_server_demo.py` | MCP server (stdio) |
| `C:\Users\kenhu\packt-harness\course_implementation\module_07_skills_plugins_mcp\mcp_client_runner.py` | Client that drives the server |
| `C:\Users\kenhu\packt-harness\course_implementation\module_07_skills_plugins_mcp\skills\spec-check\SKILL.md` | Skill frontmatter + body |
| `C:\Users\kenhu\packt-harness\course_implementation\module_07_skills_plugins_mcp\agents\spec-reviewer.md` | Subagent frontmatter + body |
| `C:\Users\kenhu\packt-harness\course_implementation\module_07_skills_plugins_mcp\.claude-plugin\plugin.json` | Plugin manifest |
| `C:\Users\kenhu\packt-harness\course_implementation\module_07_skills_plugins_mcp\RUN_RESULTS.md` | Last captured stdout |

No extra output file. The MCP exchange is on the child's stdio pipes.

## How to run

Install the SDK once if needed:

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe -m pip install mcp
```

Run the client (it starts the server):

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_07_skills_plugins_mcp\mcp_client_runner.py
```

Do not run `mcp_server_demo.py` by itself unless you intend to speak
JSON-RPC on that process's stdin. Its stdout is the protocol, not a log.

`run_all_modules.py` also runs `mcp_server_demo.py` as a standalone
`.py` file. The server then sits on stdin and exits quickly with no
client, which still counts as exit 0. The session that proves MCP works
is `mcp_client_runner.py`.

## Output file and evidence

- **Stdout** (exit 0).
- **Recorded copy:** `C:\Users\kenhu\packt-harness\course_implementation\module_07_skills_plugins_mcp\RUN_RESULTS.md`

Captured on this machine, 2026-08-14:

```text
  [PASS] MCP session initialized over subprocess stdio.
[MCP Client] Sending 'tools/list' request...
  [PASS] Tool Available: 'query_database_record' - Query one enterprise database record by its numeric identifier.
[MCP Client] Sending 'tools/call' request...
  [PASS] Tool Execution Result: 'DB_RECORD #4092: status=ACTIVE, owner=admin, env=production'
[LLM Client] Synthesizing the MCP tool result...
  [SKIPPED] LLM synthesis unavailable: the configured endpoint did not return a live response.
[MCP Client] Sending 'resources/list' request...
  [PASS] Resource Available: 'config://app-settings' (app_settings)
[MCP Client] Sending 'resources/read' request...
  [PASS] Resource Read Result: '{
  "application": "harness-enterprise",
  "environment": "production",
  "record_access": "read-only"
}'
```

## Annotated code

Server:

```python
# MCP Python SDK 2.x authoring API. Do not print to stdout: that stream
# is the protocol, not a log.
mcp = MCPServer("Harness-Enterprise-Tools")

@mcp.tool()
def query_database_record(record_id: int) -> str:
    """Teaching MCP tool: return one fake enterprise record."""
    return f"DB_RECORD #{record_id}: status=ACTIVE, owner=admin, env=production"

@mcp.resource("config://app-settings")
def app_settings() -> str:
    """Teaching MCP resource: a read-only JSON document."""
    return json.dumps({...}, indent=2)
```

Client:

```python
# Spawn mcp_server_demo.py as a child. The SDK wires stdin/stdout to JSON-RPC.
server_parameters = StdioServerParameters(
    command=sys.executable,
    args=[str(MODULE_DIR / "mcp_server_demo.py")],
)
async with stdio_client(server_parameters) as (read_stream, write_stream):
    async with ClientSession(read_stream, write_stream) as session:
        await session.initialize()          # handshake
        await session.list_tools()
        await session.call_tool("query_database_record", {"record_id": 4092})
        await session.list_resources()
        await session.read_resource("config://app-settings")
```
